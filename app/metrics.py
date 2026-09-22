"""Bounded HTTP metrics for the single-process Uvicorn deployment."""

from time import perf_counter

from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "http_requests_total", "Completed HTTP requests", ["method", "route", "status"]
)
ERRORS = Counter(
    "http_errors_total", "HTTP responses with status >= 400", ["method", "route", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration through response completion",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)


class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["path"] in {"/metrics", "/health"}:
            await self.app(scope, receive, send)
            return

        started = perf_counter()
        status = 500

        async def tracked_send(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, tracked_send)
        finally:
            # Route templates prevent user IDs and arbitrary 404 paths becoming labels.
            route = getattr(scope.get("route"), "path", "unmatched")
            method = scope["method"]
            if method not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE", "CONNECT"}:
                method = "OTHER"
            REQUESTS.labels(method, route, str(status)).inc()
            LATENCY.labels(method, route).observe(perf_counter() - started)
            if status >= 400:
                ERRORS.labels(method, route, str(status)).inc()
