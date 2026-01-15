# Kubernetes Real Scenarios (Mid to Senior)

## Scenario 1: Pods Stuck in Pending
- Symptoms/logs:
```text
FailedScheduling: 0/6 nodes are available
```
- Constraints: production, no new nodes for 30 minutes.
- Investigation plan: check resource requests, node capacity, taints, PVC binding.
- Final fix + prevention: reduce requests or free capacity; add capacity alerts.
- Postmortem notes: resource sizing guidelines.

## Scenario 2: CrashLoopBackOff After Config Change
- Symptoms/logs:
```text
Back-off restarting failed container
```
- Constraints: only one replica can be restarted at a time.
- Investigation plan: inspect logs, check env/config, confirm exit code.
- Final fix + prevention: rollback config, add validation checks.
- Postmortem notes: config review process.

## Scenario 3: Rolling Update Hangs
- Symptoms/logs:
```text
Deployment exceeded its progress deadline
```
- Constraints: rollback must be safe for DB migrations.
- Investigation plan: check readiness probe failures, maxUnavailable, events.
- Final fix + prevention: fix probe or service dependency; add pre-deploy checks.
- Postmortem notes: rollout gates.

## Scenario 4: ImagePullBackOff
- Symptoms/logs:
```text
Failed to pull image: unauthorized
```
- Constraints: registry access via secret.
- Investigation plan: verify image tag, registry secret, node egress.
- Final fix + prevention: update imagePullSecret; validate tags in CI.
- Postmortem notes: registry credential rotation.

## Scenario 5: Service Returns 503 Intermittently
- Symptoms/logs:
```text
upstream reset or 503
```
- Constraints: no full redeploy.
- Investigation plan: check readiness probes, endpoints, pod restarts, upstream latency.
- Final fix + prevention: tune probes, increase resources, add circuit breaker.
- Postmortem notes: dependency stability.

## Scenario 6: Node NotReady
- Symptoms/logs:
```text
Node status: NotReady
```
- Constraints: cannot restart all nodes.
- Investigation plan: check kubelet logs, disk pressure, network.
- Final fix + prevention: fix disk or kubelet issue; add node health automation.
- Postmortem notes: node lifecycle runbook.

## Scenario 7: PVC Pending
- Symptoms/logs:
```text
volume binding timeout
```
- Constraints: production stateful app.
- Investigation plan: check storage class, access modes, PV capacity.
- Final fix + prevention: correct storage class and size; add validation.
- Postmortem notes: storage provisioning checklist.

## Scenario 8: Cluster DNS Outage
- Symptoms/logs:
```text
SERVFAIL from kube-dns
```
- Constraints: impacts all services.
- Investigation plan: check CoreDNS pods, CPU/memory, node network.
- Final fix + prevention: scale CoreDNS, add resource limits and alerts.
- Postmortem notes: DNS SLO.

## Scenario 9: Deployment Causes Config Drift
- Symptoms/logs:
```text
diff between Git and live resources
```
- Constraints: GitOps enforced.
- Investigation plan: find manual changes, identify actor, restore from Git.
- Final fix + prevention: enforce RBAC, auto-sync.
- Postmortem notes: access review.

## Scenario 10: Ingress 502 After TLS Update
- Symptoms/logs:
```text
upstream connect error or TLS handshake failed
```
- Constraints: must fix without downtime.
- Investigation plan: validate cert secret, ingress controller logs, backend readiness.
- Final fix + prevention: rollback cert or reissue; add expiry alerts.
- Postmortem notes: cert rotation process.

## Scenario 11: HPA Thrashing
- Symptoms/logs:
```text
replicas oscillate every minute
```
- Constraints: noisy traffic.
- Investigation plan: check metrics window, cooldown, resource requests.
- Final fix + prevention: adjust stabilization window and min/max.
- Postmortem notes: autoscaling guidance.

## Scenario 12: etcd Latency Spike
- Symptoms/logs:
```text
apiserver timeouts, etcd slow requests
```
- Constraints: control plane instability.
- Investigation plan: check etcd disk IO, defrag, client load.
- Final fix + prevention: reduce write load, tune IO, schedule maintenance.
- Postmortem notes: control plane health checks.