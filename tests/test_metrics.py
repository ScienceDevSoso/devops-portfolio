import pytest
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from prometheus_client import REGISTRY
from prometheus_client.parser import text_string_to_metric_families

from app.main import app
from app.metrics import MetricsMiddleware


def value(name, labels):
    return REGISTRY.get_sample_value(name, labels) or 0


def test_metrics_exposition_and_exclusions():
    with TestClient(app) as client:
        before = client.get('/metrics').text
        client.get('/health')
        response = client.get('/metrics')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/plain')
    assert list(text_string_to_metric_families(response.text))
    for body in (before, response.text):
        assert 'route="/metrics"' not in body
        assert 'route="/health"' not in body


@pytest.mark.parametrize('path,status', [('/', 200), ('/not-found-one', 404), ('/not-found-two', 404)])
def test_requests_latency_and_errors(path, status):
    route = '/' if status == 200 else 'unmatched'
    labels = dict(method='GET', route=route, status=str(status))
    duration_labels = dict(method='GET', route=route)
    requests = value('http_requests_total', labels)
    errors = value('http_errors_total', labels)
    count = value('http_request_duration_seconds_count', duration_labels)
    duration = value('http_request_duration_seconds_sum', duration_labels)
    with TestClient(app) as client:
        assert client.get(path).status_code == status
    assert value('http_requests_total', labels) == requests + 1
    assert value('http_errors_total', labels) == errors + (status >= 400)
    assert value('http_request_duration_seconds_count', duration_labels) == count + 1
    assert value('http_request_duration_seconds_sum', duration_labels) > duration


def test_templates_exceptions_and_streaming():
    test_app = FastAPI()
    test_app.add_middleware(MetricsMiddleware)

    @test_app.get('/items/{item_id}')
    def item(item_id: int):
        return {'id': item_id}

    @test_app.get('/handled')
    def handled():
        raise HTTPException(503, 'test only')

    @test_app.get('/unhandled')
    def unhandled():
        raise RuntimeError('test only')

    @test_app.get('/stream')
    def stream():
        return StreamingResponse(iter([b'one', b'two']))

    with TestClient(test_app, raise_server_exceptions=False) as client:
        labels = dict(method='GET', route='/items/{item_id}', status='200')
        before = value('http_requests_total', labels)
        for item_id in (11, 22):
            assert client.get(f'/items/{item_id}').status_code == 200
        assert value('http_requests_total', labels) == before + 2
        for path, status in [('/handled', 503), ('/unhandled', 500)]:
            labels = dict(method='GET', route=path, status=str(status))
            before = value('http_errors_total', labels)
            assert client.get(path).status_code == status
            assert value('http_errors_total', labels) == before + 1
        assert client.get('/stream').content == b'onetwo'
        assert value('http_requests_total', dict(method='GET', route='/stream', status='200')) >= 1
        assert client.get('/items/not-an-int').status_code == 422


def test_unknown_http_methods_are_bounded():
    labels = dict(method='OTHER', route='/', status='405')
    before = value('http_requests_total', labels)
    with TestClient(app) as client:
        assert client.request('ARBITRARY', '/').status_code == 405
    assert value('http_requests_total', labels) == before + 1
