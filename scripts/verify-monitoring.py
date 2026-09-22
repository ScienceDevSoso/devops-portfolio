#!/usr/bin/env python3
"""Read-only checks against a localhost Prometheus port-forward (stdlib only)."""
import argparse
import json
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:9090')
parser.add_argument('--skip-app', action='store_true', help='Verify infrastructure only; app remains unverified')
args = parser.parse_args()


def get(path, **params):
    with urlopen(args.url + path + '?' + urlencode(params), timeout=15) as response:
        payload = json.load(response)
    if payload['status'] != 'success':
        raise RuntimeError(payload)
    return payload['data']


jobs = {'prometheus', 'kube-state-metrics', 'kubelet', 'cadvisor', 'node-resource'}
if not args.skip_app:
    jobs.add('fastapi')
failed = False
try:
    targets = get('/api/v1/targets')['activeTargets']
    for job in sorted(jobs):
        selected = [t for t in targets if t['labels'].get('job') == job]
        healthy = bool(selected) and all(t['health'] == 'up' for t in selected)
        print(f'{job}: {"PASS" if healthy else "FAIL"} ({len(selected)} targets)')
        for target in selected:
            if target['health'] != 'up':
                print('  ' + target.get('lastError', 'unknown scrape error'))
        failed |= not healthy
    queries = {
        'node CPU': 'node_cpu_usage_seconds_total{job="node-resource"}',
        'node memory': 'node_memory_working_set_bytes{job="node-resource"}',
        'container CPU': 'container_cpu_usage_seconds_total{job="cadvisor",container!="",container!="POD"}',
        'container memory': 'container_memory_working_set_bytes{job="cadvisor",container!="",container!="POD"}',
        'node ready': 'kube_node_status_condition{condition="Ready",status="true"} == 1',
        'app deployment available': 'kube_deployment_status_replicas_available{namespace="default",deployment="devops-portfolio"} >= 1',
        'pod restarts': 'kube_pod_container_status_restarts_total',
    }
    if not args.skip_app:
        queries.update({
            'app requests': 'http_requests_total{job="fastapi"}',
            'app latency': 'http_request_duration_seconds_count{job="fastapi"}',
            'app test 404': 'http_errors_total{job="fastapi",status="404"}',
        })
    for label, query in queries.items():
        found = bool(get('/api/v1/query', query=query)['result'])
        print(f'{label}: {"PASS" if found else "FAIL (no series)"}')
        failed |= not found
except Exception as error:
    print(f'FAIL: {error}', file=sys.stderr)
    sys.exit(1)
if args.skip_app:
    print('Application metrics explicitly skipped; full milestone verification remains pending.')
sys.exit(1 if failed else 0)
