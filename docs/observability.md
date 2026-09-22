# Observability runbook

## Design and capacity

This is an ephemeral learning stack for one `t3.small`, not an HA monitoring
service. A local chart avoids an operator, CRDs, Alertmanager, exporters as
DaemonSets, dashboard sidecars, and persistent volumes. Kubelet already exposes
node and container usage; kube-state-metrics supplies Kubernetes object state.

| Workload | CPU request / limit | Memory request / limit | Pods |
| --- | --- | --- | --- |
| Prometheus | 100m / 400m | 256Mi / 384Mi | 1 |
| Grafana | 50m / 250m | 128Mi / 256Mi | 1 |
| kube-state-metrics | 20m / 100m | 32Mi / 64Mi | 1 |
| App | 50m / 250m | 64Mi / 128Mi | 1 |

Monitoring adds 170m CPU and 416Mi memory requests, with 704Mi memory limits.
The initial worker inspection found 1,930m CPU, 1,433.7Mi memory, and 11 pod slots
allocatable; five pods were occupied and existing requests were 350m CPU/140Mi.
With app requests and monitoring, the expected total is 570m CPU/620Mi and eight
pods. These are scheduling estimates, not proof of sustained fit. EKS agents and
the OS also need memory, and CPU credits constrain a burstable node.

Scrape/evaluation intervals are 60 seconds. Prometheus retains at most 6 hours
or 256MB of blocks, whichever is reached first; its WAL/head also consume space.
The data `emptyDir` is capped at 768Mi, with a 1Gi ephemeral-storage limit.
Grafana's `emptyDir` is 128Mi. Optional plugin preinstallation and plugin
management are disabled to keep downloads within that budget. Pod replacement loses history and UI changes;
datasource and dashboard provisioning restore the version-controlled view.
Monitoring Deployments use `Recreate` to avoid surge resource demand, so upgrades
interrupt monitoring. Review upgrades before applying; do not delete pods as a drill.

All Services are ClusterIP. Port-forwards bind to localhost. Grafana uses a
pre-existing Secret, anonymous access is disabled, and no password is committed.
Prometheus is unauthenticated inside the cluster: this setup assumes trusted
cluster users/workloads. No public ingress, LoadBalancer, PVC, or additional AWS
resource is created. RBAC grants Prometheus pod discovery in the app namespace,
node discovery and `nodes/metrics`; it does not grant `nodes/proxy` or Secret access.
TLS verification remains enabled for direct kubelet scraping.

## Install

First check the expected EKS context, existing releases, free pod slots, node
conditions, and resource requests:

```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl describe nodes
kubectl get pods -A
helm list -A
helm lint helm/devops-portfolio helm/monitoring
helm template monitoring helm/monitoring --namespace monitoring
```

The intended release is `monitoring` in namespace `monitoring`; install only once.
Create the namespace and credential Secret without printing the password or
placing it in command arguments/history (requires Python and kubectl):

```bash
kubectl create namespace monitoring
python3 - <<'PY'
import json, secrets, subprocess
secret = {'apiVersion': 'v1', 'kind': 'Secret',
          'metadata': {'name': 'grafana-admin', 'namespace': 'monitoring'},
          'type': 'Opaque', 'stringData': {'admin-password': secrets.token_urlsafe(32)}}
subprocess.run(['kubectl', 'create', '-f', '-'], input=json.dumps(secret),
               text=True, check=True)
PY
helm install monitoring helm/monitoring --namespace monitoring --wait --timeout 5m
kubectl get pods -n monitoring
```

If the namespace or Secret already exists, inspect ownership and reuse it; do
not replace credentials blindly. For later chart changes, inspect the rendered
diff before `helm upgrade monitoring helm/monitoring -n monitoring --wait --timeout 5m`.
No automatic uninstall/rollback-on-failure is used. If a rollout fails, inspect
it and stop before deletion, forced replacement, or infrastructure resizing.

Keep the app's current image until the PR is merged and its main-branch image is
published. Then deploy that immutable SHA using the README command. Until then,
Prometheus's `fastapi` target may return 404 from the old image; this is not a
monitoring capacity problem.

## Access and verify

Run each port-forward in its own terminal:

```bash
kubectl port-forward -n monitoring service/monitoring-prometheus 9090:9090
kubectl port-forward -n monitoring service/monitoring-grafana 3000:3000
kubectl port-forward service/devops-portfolio 8000:8000
```

Open Prometheus at http://127.0.0.1:9090 and Grafana at http://127.0.0.1:3000.
Log in as `admin`; retrieve the generated password locally (do not paste it into
issues, screenshots, or logs):

```bash
kubectl get secret -n monitoring grafana-admin \
  -o jsonpath='{.data.admin-password}' | base64 --decode
```

The provisioned **Portfolio / Portfolio observability** dashboard includes target
health, request/error rates, p95 latency, node and container usage, available
replicas, restarts, and node readiness. Healthy targets alone do not prove that
required metric series exist:

```bash
curl -fsS http://127.0.0.1:8000/
curl -fsS http://127.0.0.1:8000/version
curl -i http://127.0.0.1:8000/observability-test-not-found
curl -fsS http://127.0.0.1:8000/metrics
# Wait for at least two 60-second scrapes before examining rates.
python3 scripts/verify-monitoring.py
# Explicit partial verification while the new app image is unpublished:
python3 scripts/verify-monitoring.py --skip-app
```

Success requires every selected target up and nonempty node, container,
Kubernetes, and app metric queries. `--skip-app` explicitly does not complete app
verification. After several scrapes, inspect actual usage and node conditions;
retain spare memory and pod slots for app rollouts. Metrics Server is not needed
for this setup, so `kubectl top` may be unavailable.

Useful PromQL (5xx measures server failures; 4xx is separate client traffic):

```promql
sum(rate(http_requests_total{job="fastapi"}[5m]))
sum by (status) (rate(http_errors_total{job="fastapi"}[5m]))
(sum(rate(http_requests_total{job="fastapi",status=~"5.."}[5m])) or vector(0))
  / clamp_min(sum(rate(http_requests_total{job="fastapi"}[5m])), 0.000001)
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job="fastapi"}[5m])))
node_memory_working_set_bytes{job="node-resource"}
sum by (node) (rate(node_cpu_usage_seconds_total{job="node-resource"}[5m]))
sum by (pod) (container_memory_working_set_bytes{job="cadvisor",namespace="monitoring",container!="",container!="POD"})
kube_node_status_allocatable{resource="memory"}
kube_pod_status_phase{phase="Pending"} == 1
```

Idle error counters may have no series until the first error. A zero fallback in
the dashboard is not evidence that a target is healthy: always check `up` too.
Do not add raw URLs, user IDs, query strings, or exception messages as labels.

## Safe troubleshooting scenarios

| Symptom / safe exercise | Checks | Action boundary |
| --- | --- | --- |
| Generate one unknown URL (404) | Compare the `unmatched`, status `404` counter before/after; confirm 5xx stays unchanged | No intentional production 500 endpoint; exercise 500s in pytest |
| No app traffic graph | Request `/` and `/version`, wait two scrapes; inspect `up{job="fastapi"}` | `/health` is intentionally excluded; do not change probes to manufacture traffic |
| Target down or metrics missing | Prometheus Targets shows HTTP status/TLS/auth errors; inspect pod labels and `/metrics` directly | 404 usually means old image; inspect deployed SHA before upgrading |
| Kubelet 401/403 or TLS error | Inspect Prometheus service account, `nodes/metrics` RBAC, CA and node addresses | Do not disable TLS verification or grant cluster-admin |
| Pending monitoring pod | `kubectl describe pod -n monitoring POD`; events identify memory, CPU, or pod-slot limits | Stop and report; no node resize or removal of system pods |
| OOMKilled / rising restarts | Describe pod, prior logs, memory series and node conditions | Stop and report resource limits/usage; do not run a stress test |
| Grafana empty dashboard | Check datasource health, target health, time window and provisioned dashboard logs | UI changes are ephemeral; fix configuration in Git |
| Local port-forward stopped | Stop/restart only the local forwarding process, then retry curl | Does not require deleting or restarting a cluster pod |
| EKS timeout after WSL restart | Check DNS, AWS identity and API allowlist against current developer IP | Do not broaden API access to `0.0.0.0/0`; infrastructure changes require review |

Read-only commands:

```bash
kubectl get events -n monitoring --sort-by=.lastTimestamp
kubectl describe pods -n monitoring
kubectl logs -n monitoring deployment/monitoring-prometheus --tail=100
kubectl logs -n monitoring deployment/monitoring-grafana --tail=100
kubectl logs deployment/devops-portfolio --tail=100 --since=10m
kubectl logs POD --previous --tail=100
kubectl describe nodes
```

Uvicorn access/error logs and monitoring logs use stdout/stderr. `kubectl logs`
provides short-lived diagnostics; it is not a durable audit archive. Loki,
Elasticsearch, Fluent Bit, and CloudWatch log shipping are intentionally absent
to preserve worker resources and avoid adding cost.

## Configuration validation

`helm lint` and rendering validate chart structure. The following also validates
Prometheus syntax and every provisioned dashboard query using the matching
Prometheus 3.14.0 `promtool`; Python's PyYAML is a validation-only dependency:

```bash
helm template monitoring helm/monitoring -n monitoring > /tmp/monitoring.yaml
python3 scripts/extract-monitoring-config.py /tmp/monitoring.yaml /tmp/monitoring-check
promtool check config --syntax-only /tmp/monitoring-check/prometheus.yml
promtool check rules /tmp/monitoring-check/dashboard-rules.yml
```

Syntax checks do not validate EKS permissions, image pulls, resource fit, or live
series. Use the runtime checks above for those.

References: [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/),
[Kubernetes kubelet authorization](https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/),
[Kubernetes metrics endpoints](https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/),
[Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/),
[Python Prometheus client](https://prometheus.github.io/client_python/).
