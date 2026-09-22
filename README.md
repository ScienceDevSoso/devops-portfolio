# DevOps Portfolio

A FastAPI service built, tested, and published with GitHub Actions, running on a
single `t3.small` Amazon EKS worker. Terraform manages AWS infrastructure; Helm
manages the app and a small Prometheus/Grafana monitoring stack.

```text
GitHub PR -> pytest + Docker build + monitoring validation
main push -> GHCR image (:latest and :commit-SHA)
                         |
Terraform -> EKS -> Helm application -> FastAPI :8000
                         |
                 Prometheus -> Grafana
                    |           (localhost port-forward)
                    +-> app /metrics
                    +-> kubelet: node/container usage
                    +-> kube-state-metrics: readiness/restarts/requests
```

## Repository

| Path | Purpose |
| --- | --- |
| `app/`, `tests/`, `requirements.txt` | API, HTTP metrics, automated tests, pinned dependencies |
| `.github/workflows/` | PR validation and main-only GHCR publication |
| `terraform/` | EKS, node group, IAM, restricted API access |
| `helm/devops-portfolio/` | Application Deployment, probes, resources, ClusterIP Service |
| `helm/monitoring/` | Pinned images, scrape configuration, RBAC, provisioned Grafana dashboard |
| `scripts/verify-monitoring.py` | Read-only scrape and metric verification |
| `k8s/` | Historical learning manifests; use Helm for current deployments |
| [Observability runbook](docs/observability.md) | Installation, queries, verification, safe troubleshooting |
| [Project status](PROJECT_STATUS.md) | Validated results and remaining work |

## Develop and test

Use the Linux filesystem in WSL, with Docker Desktop's Ubuntu integration enabled
for container builds. Python 3.14 is used locally, in CI, and in the image.

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Endpoints: `/` identifies the service, `/health` serves Kubernetes probes,
`/version` reports the API version, and `/metrics` exposes Prometheus text.

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/metrics
# Safe 404 to create an error series:
curl -i http://127.0.0.1:8000/observability-test-not-found
```

`http_requests_total{method,route,status}` counts completed requests;
`http_errors_total` counts responses with status >= 400; and
`http_request_duration_seconds{method,route}` is a latency histogram in seconds.
Rates are calculated in PromQL. Route templates and one `unmatched` label bound
cardinality; unknown methods use `OTHER`. `/health` and `/metrics` are excluded so
probes and scrapes do not inflate traffic. Unhandled exceptions count as 500.
Streaming duration includes response completion. Counters reset on process restart.
The image runs **one Uvicorn process**; multiple workers require explicit
Prometheus multiprocess configuration before use.

## Build and deploy

```bash
docker build -t devops-portfolio:local .
docker run --rm -p 127.0.0.1:8001:8000 devops-portfolio:local
helm lint helm/devops-portfolio helm/monitoring
helm template devops-portfolio helm/devops-portfolio
```

CI publishes images only after a merge to `main`. After that workflow passes,
set `APP_SHA` to the published commit SHA and update the existing app release:

```bash
helm upgrade devops-portfolio helm/devops-portfolio --namespace default \
  --set-string image.tag="$APP_SHA" --server-side=false --wait --timeout 5m
kubectl rollout status deployment/devops-portfolio --timeout=120s
kubectl port-forward service/devops-portfolio 8000:8000
```

Review the active Kubernetes context and capacity before deploying. The app
requests 50m CPU/64Mi memory and is limited to 250m/128Mi. Monitoring has separate
configuration and lifecycle; see the runbook. Never apply the historical `k8s/`
manifests over the Helm-managed app.

Terraform changes require reviewing the plan. Do not resize the worker or make
destructive Kubernetes changes to make monitoring fit. Report Pending pods,
OOMs, or pressure first. Logs stay on stdout/stderr and are read with
`kubectl logs`; this lab has no centralized log store.
