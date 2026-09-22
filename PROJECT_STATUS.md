# Project status

Updated: 2026-09-22. Repository baseline: `main` after PR #22.

## Current architecture

- FastAPI on one `t3.small` EKS worker in `eu-north-1`.
- Terraform manages EKS, IAM, the managed node group, and restricted API access.
- Helm release `devops-portfolio` in `default` manages the app; the deployed image
  predates the observability changes.
- Helm release `monitoring` in `monitoring` runs Prometheus, Grafana, and
  kube-state-metrics. Kubelet supplies node/container metrics without another
  DaemonSet. Monitoring release revision 2 disables optional Grafana plugins.
- GitHub Actions tests PRs and builds containers; GHCR publication runs only on
  `main`, using `latest` and commit-SHA tags. This PR must not be merged automatically.
- Logs remain stdout/stderr plus `kubectl logs`. No centralized logging stack.

## Observability implemented

- Pinned `prometheus-client==0.26.0`; `/metrics` endpoint, request/error counters,
  and latency histogram. Bounded method/route/status labels; probes and scrapes
  excluded. Tests cover 2xx, 4xx, handled/unhandled 5xx, route templates, unknown
  methods, and streaming responses.
- Existing app Helm chart updated only for CPU/memory requests and limits and
  chart version. The live app release has not been changed.
- Version-controlled monitoring images, limits, RBAC, 60-second scrapes,
  six-hour/256MB retention, Grafana datasource, and 12-panel dashboard.
- Three monitoring pods request 170m CPU/416Mi memory in total. No persistent
  volumes, public ingress, operator, Alertmanager, or additional AWS resources.
- Added configuration/PromQL validation to CI and a read-only runtime verifier.
- README and [observability runbook](docs/observability.md) document deployment,
  queries, credentials, safe troubleshooting, and resource boundaries.

## Validation evidence

- Python 3.14: **9 tests passed**, with two existing dependency deprecation
  warnings. `pip check` reported no broken dependencies.
- Both charts passed `helm lint` and rendering.
- Prometheus 3.14.0 `promtool` accepted the scrape configuration and all 12
  dashboard PromQL expressions.
- Real local Uvicorn + Prometheus integration verified a healthy scrape,
  successful request counts, 404 error counts, histogram observations, positive
  request rate, and p95 latency.
- Live EKS: Prometheus, kube-state-metrics, kubelet, cAdvisor, and node-resource
  targets passed. Queries returned node CPU/memory, container CPU/memory,
  node Ready, application deployment availability, and pod restarts.
- After the Grafana configuration fix, all three monitoring pods were Ready;
  the worker was Ready with MemoryPressure, DiskPressure, and PIDPressure false.
  Eight running pods occupy the worker's eleven allocatable pod slots.
- Grafana's database health, authenticated Prometheus datasource health, and
  provisioned 12-panel dashboard passed API checks. The replacement Grafana pod
  remained Ready without restarts during the follow-up checks.
- Live resource requests total 520m CPU/556Mi memory before the app chart update.
  A short sample showed about 1,033Mi node memory working set and 0.28 CPU cores
  used; these observations are not a sustained capacity guarantee.

## Final observability verification

- The metrics-enabled application image was published from `main` and deployed
  to EKS through Helm revision 2.
- The live `/metrics` endpoint was verified on EKS.
- Prometheus successfully scrapes the FastAPI target.
- End-to-end monitoring verification passed for application requests, latency,
  test 404/error metrics, node CPU and memory, container CPU and memory,
  deployment availability, Pod restarts, kubelet, cAdvisor, and
  kube-state-metrics.
- The local Docker CLI is unavailable after the WSL restart. Container build
  validation therefore relies on the PR's Docker CI job until integration is
  restored.
- Short verification is not a sustained load or capacity test. Watch resource
  usage and node conditions during normal use. Stop and report any capacity
  problem; do not resize AWS or remove system workloads to accommodate monitoring.

## Issues resolved during this milestone

- Sandbox restrictions prevented snap tools from running and caused TestClient
  to hang. Approved execution outside the sandbox allowed checks to proceed.
- WSL/Helm DNS intermittently timed out while system DNS and kubectl worked.
  Helm connected using a freshly resolved EKS API IP with the original TLS
  hostname still verified. No kubeconfig, DNS, or AWS network policy was changed.
- Grafana's default optional plugin downloads exceeded the 128Mi data-volume
  quota and caused eviction. Disabled plugin preinstallation/management through
  Helm without increasing resource limits. Evicted pods were not manually deleted.
- Prometheus target discovery starts asynchronously; integration validation now
  waits for a healthy target before evaluating rates.

## Earlier milestones completed

- FastAPI endpoints, tests, Docker packaging, GitHub Actions, protected `main`,
  required PR checks, and GHCR images with immutable SHA tags.
- Manual EC2 deployment, Terraform networking/EC2, and reproducible bootstrap;
  standalone EC2 resources subsequently retired through a reviewed plan.
- Local Minikube deployment, probes, Service networking, and self-healing exercises.
- Terraform-managed EKS with one `t3.small`, followed by non-destructive adoption
  of the existing app Deployment/Service into Helm.

Detailed historical milestone notes remain available in earlier Git revisions.
The `k8s/` directory remains learning material; current deployments use Helm.
