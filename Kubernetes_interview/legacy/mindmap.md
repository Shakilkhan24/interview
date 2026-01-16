Below is a **heavily expanded, multi-case, production-grade rewrite of the README**.
This version is intentionally **long, exhaustive, and scenario-driven**—the kind of document senior SREs keep bookmarked.

You can **replace your README entirely with this**.

---

# Kubernetes Deep Dive — Production, Failure, and Scale (Zero Gaps, Multi-Case)

> This README is **not a tutorial for beginners**.
> It is a **systems-level Kubernetes reference** covering **behavior, edge cases, and failure modes** you only learn after running real clusters.

Every section follows this pattern:

1. **Concept**
2. **Internal mechanics**
3. **Multiple real-world cases**
4. **YAML / commands**
5. **Common failure patterns**
6. **Debug checklist**

---

# 1) Pod Lifecycle & Scheduling (Deep Internals)

---

## 1.1 Pod Phases — What *Actually* Happens

### Internal Flow

```
kubectl apply
 → API Server
 → etcd write
 → Scheduler binds pod to node
 → kubelet pulls image
 → containers created
```

### Phase Breakdown with Scenarios

| Phase   | Scenario                     |
| ------- | ---------------------------- |
| Pending | No node fits requests        |
| Pending | PVC not bound                |
| Pending | Image pull backoff           |
| Running | Containers started           |
| Running | Readiness=false (no traffic) |
| Failed  | App exits non-zero           |
| Unknown | Node unreachable             |

#### Case 1: Pending forever

```bash
kubectl describe pod
```

Typical reasons:

* `Insufficient cpu`
* `node(s) had taint`
* `pod affinity mismatch`

---

## 1.2 Restart Policies (Edge Cases)

```yaml
restartPolicy: OnFailure
```

### Case Matrix

| Controller | RestartPolicy | Result                |
| ---------- | ------------- | --------------------- |
| Deployment | Always        | kubelet restarts      |
| Job        | OnFailure     | retries until success |
| Pod        | Never         | manual debugging      |

⚠️ **Hidden trap**
A container exiting `0` under `OnFailure` will **NOT restart** → Job completes.

---

## 1.3 Termination Flow (Traffic-Safe Shutdown)

### Timeline

```
T0   Pod marked Terminating
T0+  Endpoint removed (if readiness fails)
T0+  SIGTERM sent
T0+  preStop hook
T0+N grace period
SIGKILL
```

```yaml
terminationGracePeriodSeconds: 60
```

### Case 1: Graceful HTTP shutdown

* readiness probe fails immediately
* Ingress stops routing
* app drains connections

### Case 2: Bad shutdown

* no SIGTERM handler
* SIGKILL
* partial writes, corrupt state

---

## 1.4 Init Containers vs Sidecars (Multi-Pattern)

### Init Containers — Blocking Gate

```yaml
initContainers:
- name: migrate
  image: app
  command: ["./migrate.sh"]
```

**Used for**

* DB migrations
* schema validation
* secrets fetch

**Failure case**

* migration fails → Pod never starts → rollout stuck

---

### Sidecars — Parallel Execution

```yaml
containers:
- name: app
- name: log-agent
```

**Used for**

* log shipping
* config reloaders
* service mesh proxies

**Anti-pattern**

* sidecar blocks app readiness → traffic blackhole

---

## 1.5 Probes — Failure Loop Taxonomy

### Probe Types (Expanded)

| Probe     | Controls        | Breaks When     |
| --------- | --------------- | --------------- |
| startup   | container start | slow boot       |
| readiness | traffic         | dependency down |
| liveness  | restart         | false positives |

---

### Case A: Infinite CrashLoop

```yaml
livenessProbe:
  httpGet:
    path: /health
```

* `/health` checks DB
* DB down
* liveness fails
* container restarts forever

✅ Fix: move DB check to **readiness**

---

### Case B: Startup Probe Missing

* app needs 2 minutes
* liveness starts at 10s
* never reaches Running

---

## 1.6 QoS Classes & Evictions (Real Behavior)

### Memory Pressure Scenario

```
node memory < evictionHard
 → BestEffort evicted
 → Burstable evicted
 → Guaranteed last
```

```yaml
resources:
  requests:
    memory: 512Mi
  limits:
    memory: 512Mi
```

**Guaranteed pods survive longest**

---

## 1.7 Scheduling Internals (Modern Scheduler)

### Plugin Phases

1. PreFilter
2. Filter
3. PreScore
4. Score
5. Reserve
6. Permit
7. Bind

### Case: Pod never scheduled

* passes Filter
* scores poorly
* starves forever under load

---

## 1.8 Affinity Explosion (Large Clusters)

```yaml
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution
```

### Failure

* N replicas
* M nodes
* O(N×M) scheduling cost
* Scheduler CPU spikes

✅ Prefer **preferredDuringScheduling**

---

## 1.9 Taints, Drain, and PDB Interaction

```bash
kubectl drain node --ignore-daemonsets
```

### Drain stops when:

* PDB violated
* local storage
* static pods

---

## 1.10 Topology Spread (Zonal Survival)

### Case: Single AZ outage

* no spread constraints
* all replicas in same zone
* full outage

---

## 1.11 Priority & Preemption (Cluster Survival)

### Case: System under pressure

* high-priority API pods preempt batch jobs
* batch evicted gracefully

---

## 1.12 PDB Semantics (Misunderstood)

```yaml
minAvailable: 2
```

* applies only to **voluntary disruptions**
* ignored on node crash

---

# 2) Workload Controllers (Multi-Failure)

---

## 2.1 Deployment Rollout Deadlocks

### Case A: Readiness fails

* new RS never ready
* old RS never scaled down

### Case B: maxUnavailable=0 + PDB

* no pod can be removed
* rollout frozen

---

## 2.2 StatefulSet Failure Patterns

### Case: PVC stuck

* WaitForFirstConsumer
* affinity mismatch
* pod Pending forever

### Case: Rolling update deadlock

* ordered rollout
* pod-0 unhealthy
* pod-1 never updates

---

## 2.3 DaemonSets on Drain

* ignored by default
* must be manually stopped
* common CNI upgrade pain

---

## 2.4 Jobs & CronJobs (Hidden Kill Switches)

```yaml
activeDeadlineSeconds: 300
```

Job killed even if making progress.

---

## 2.5 Canary & Blue/Green (Native)

### Canary

* duplicate Deployment
* weighted routing (Ingress)

### Blue/Green

* switch Service selector
* instant rollback

---

## 2.6 Finalizers — Cluster Bricking Risk

### Case

* webhook adds finalizer
* webhook down
* resource stuck forever

---

# 3) Services & Networking (Failure-First)

---

## 3.1 Service Resolves but Won’t Connect

### Possible Causes

* readiness false
* NetworkPolicy blocks
* wrong targetPort
* app binds localhost

---

## 3.2 kube-proxy Scaling Pain

| Mode     | Issue          |
| -------- | -------------- |
| iptables | rule explosion |
| IPVS     | better scale   |

---

## 3.3 CoreDNS Failure Modes

| Symptom  | Cause            |
| -------- | ---------------- |
| NXDOMAIN | stubDomain wrong |
| Timeout  | NetworkPolicy    |
| Slow     | cache disabled   |

---

## 3.4 EndpointSlices at Scale

* Services >1000 pods
* legacy Endpoints break
* slices shard updates

---

## 3.5 NetworkPolicy DNS Trap (Classic)

```yaml
egress:
- to:
  - namespaceSelector: {}
```

Blocks DNS unless explicitly allowed.

---

# 4) Ingress & Gateway (Production Traffic)

---

## 4.1 503 from Ingress — Matrix

| Cause           | Check       |
| --------------- | ----------- |
| No endpoints    | readiness   |
| Wrong port      | targetPort  |
| Health mismatch | controller  |
| TLS error       | cert secret |

---

## 4.2 North-South vs East-West

* Ingress → user traffic
* Service mesh → internal

---

# 5) Config & Secrets (Rotation Reality)

---

## 5.1 Config Reload Patterns

| Method   | Downtime   |
| -------- | ---------- |
| env vars | restart    |
| volume   | app reload |
| sidecar  | zero       |

---

## 5.2 Secret Rotation Strategies

* restart
* hot reload
* reloader controller

---

## 5.3 Encryption at Rest (Concept)

* KMS provider
* etcd envelope encryption
* rotate keys without rewrite

---

# 6) Resource & Autoscaling (Reality)

---

## 6.1 CPU Throttling Symptoms

* latency spikes
* no OOM
* `kubectl top` looks fine

---

## 6.2 HPA Not Scaling

| Cause                  | Fix     |
| ---------------------- | ------- |
| metrics-server missing | install |
| wrong target           | adjust  |
| stabilization window   | wait    |

---

## 6.3 Cluster Autoscaler Blockers

* PDB
* node affinity
* insufficient instance types

---

# 7) Storage (Stateful Pain)

---

## 7.1 PVC Pending Debug

```bash
kubectl describe pvc
```

| Reason        | Fix      |
| ------------- | -------- |
| No SC         | create   |
| Zone mismatch | WFFC     |
| Quota         | increase |

---

## 7.2 Volume Expansion Failure

* filesystem not resized
* pod restart required

---

# 8) Security (Hard Failures)

---

## 8.1 RBAC Silent Denials

Controller loops without errors — only logs show `Forbidden`.

---

## 8.2 Admission Webhook Outage

* webhook timeout
* API server blocks ALL creates
* cluster frozen

---

## 9) Control Plane (Why Clusters Die)

---

## 9.1 etcd Disk Full

Symptoms:

* kubectl hangs
* leader elections fail
* controllers stop

---

## 9.2 API Server Throttling

* client QPS exceeded
* controllers slow
* cascading failures

---

# 10) Observability & Debugging (Battle Tested)

---

## 10.1 Debug Flow (Always Same)

1. `kubectl get`
2. `describe`
3. `events`
4. `logs`
5. `exec`
6. `port-forward`

---

## 10.2 Ephemeral Containers (Live Debug)

* no restart
* inspect prod safely

---

# 11) Failure & Recovery (Chaos Reality)

---

## 11.1 Node Failure

* Deployment → rescheduled
* StatefulSet → waits
* DaemonSet → gone until node returns

---

## 11.2 Control Plane Degradation

* workloads run
* kubectl unusable
* autoscaling broken

---

# 12) Upgrades & Day-2 Ops

---

## Safe Upgrade Order

1. etcd
2. control plane
3. nodes
4. addons

---

# 13) Performance & Scale (Large Clusters)

---

## Scale Killers

* excessive anti-affinity
* too many Services
* too many watches

---

# 14) Real-World Failure Cookbook

| Symptom               | Root Cause     |
| --------------------- | -------------- |
| Pending forever       | affinity / PVC |
| Rollout stuck         | PDB / probes   |
| Random OOM            | limits too low |
| DNS works, no connect | NetworkPolicy  |
| All pods blocked      | webhook        |

---

# 15–17) Helm, Operators, Service Mesh (Advanced)

* Helm ≠ config language
* Operators only for complex lifecycle
* Service mesh trades simplicity for control

---

## Final Principle (Memorize)

> **Kubernetes does not “run” your app.
> It continuously tries to make reality match what you declared — even when that hurts you.**

---
