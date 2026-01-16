--------------------------------------------------
Q1. Pod Termination: SIGTERM, preStop, and Grace Periods
Difficulty: Medium

What the interviewer is testing:
- Understanding of termination flow and signals
- How kubelet handles grace periods
- preStop hook timing and pitfalls
- Readiness during termination
- Differences between SIGTERM/SIGKILL
- Impact of slow shutdowns
- Deployment rollout interactions
- Service endpoints update timing
- Use of terminationGracePeriodSeconds
- Handling in-flight requests
- Behavior with sidecars
- Observability of termination events

Question:
- Your API pods take 20-40 seconds to drain in-flight requests. During rollouts, some requests fail. How would you implement a safe termination flow, and what can still go wrong?

Answer:
- Explanation: Kubelet sends SIGTERM, runs preStop, waits up to terminationGracePeriodSeconds, then SIGKILLs. Readiness should flip to false early so Services stop routing. preStop can trigger app-level drain.
- Why this matters in production: Improper termination causes request loss, inconsistent state, and failed rollouts.

Solution:
- kubectl commands (if applicable)
- YAML manifests (if applicable)
- Config snippets (if applicable)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  strategy:
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: api
        image: myrepo/api:1.2.3
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh","-c","/app/drain --timeout=45"]
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          periodSeconds: 5
```

Edge Cases & Tradeoffs:
- Readiness may not flip fast enough before SIGTERM
- preStop adds to total shutdown time, can exceed grace
- SIGTERM ignored by app; SIGKILL causes abrupt stop
- Long TCP keepalives can still hit terminating pods
- PodDisruptionBudget can slow rollouts
- Sidecar proxies may keep connections open
- HPA scale-down triggers same termination flow
- Node drain uses shorter grace if forced
- Slow shutdown increases rollout duration
- App drains but background workers still running
- In-flight requests may exceed grace and be cut
- Termination hook failures are ignored after timeout

Red Flags (Bad Answers):
- "Just increase terminationGracePeriodSeconds to 5 minutes"
- "Kubernetes guarantees no requests during shutdown"
- "preStop is always executed successfully"
--------------------------------------------------
Q2. Init Containers vs Sidecars Patterns
Difficulty: Medium

What the interviewer is testing:
- Correct usage of init containers
- Startup ordering guarantees
- Sidecar lifecycle implications
- Shared volume coordination
- Anti-patterns (sidecar used for setup)
- Dependency management
- Failure behavior differences
- Resource requests placement
- Security isolation considerations
- Observability of init failures
- Impact on startup time
- Compatibility with probes

Question:
- You need to fetch a schema and run migrations before the app starts, plus a log shipper for runtime. How would you model this?

Answer:
- Explanation: Use init containers for one-time setup that must finish before app starts. Use sidecars for continuous runtime services (log shipper, proxy). Init containers block pod readiness; sidecars run with app.
- Why this matters in production: Misusing sidecars for init logic can lead to race conditions and repeated work.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  initContainers:
  - name: migrate
    image: myrepo/migrate:2.0
    command: ["/bin/sh","-c","/migrate --dsn=$DSN"]
    envFrom:
    - secretRef:
        name: db-secret
  containers:
  - name: app
    image: myrepo/app:5.1
  - name: log-shipper
    image: myrepo/shipper:1.0
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  volumes:
  - name: logs
    emptyDir: {}
```

Edge Cases & Tradeoffs:
- Init container failure keeps pod Pending
- Init containers extend startup SLO
- Migrations in init can block scale-out
- Multiple pods running migrations simultaneously
- Sidecar restart does not restart app
- Sidecar resource requests impact scheduling
- Log shipper needs access to logs volume
- Init containers cannot use readiness probes
- Long migrations can exceed rollout progress deadlines
- Secrets used by init may differ from app
- Job-based migrations can be safer
- Init container output may be lost on restart

Red Flags (Bad Answers):
- "Use sidecar to do migrations every time"
- "Init containers can be started after app"
- "Sidecars are ignored by scheduler"
--------------------------------------------------
Q3. Probes: Liveness vs Readiness vs Startup
Difficulty: Medium

What the interviewer is testing:
- Correct probe selection
- Avoiding crash loops from liveness misuse
- Startup probes for slow boot
- Readiness gating traffic
- Probe timing tuning
- Failure thresholds and delay interaction
- Endpoint updates vs kube-proxy behavior
- Probe endpoints vs app health
- Probes with gRPC
- Impact on rollouts
- Failure observability
- Common probe anti-patterns

Question:
- A Java service takes 90 seconds to boot. It's getting restarted repeatedly during deploys. What probe setup fixes this and why?

Answer:
- Explanation: Use startupProbe for slow initialization, then readinessProbe for traffic gating and livenessProbe for runtime health. Liveness should not gate startup.
- Why this matters in production: Misconfigured probes cause endless restarts and broken rollouts.

Solution:
- YAML manifests:
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
  failureThreshold: 3
livenessProbe:
  httpGet:
    path: /live
    port: 8080
  periodSeconds: 10
  failureThreshold: 3
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  failureThreshold: 18
  periodSeconds: 5
```

Edge Cases & Tradeoffs:
- Startup probe too strict delays readiness
- Liveness probes can kill when dependencies down
- Readiness false doesn't stop existing connections
- HTTP 200 from shallow handler hides issues
- gRPC needs `grpc` probe or exec/HTTP workaround
- Aggressive probes increase load on app
- Slow disk can cause probe timeouts
- Probe timeouts too low for TLS handshakes
- Sidecar proxy health vs app health mismatch
- Misconfigured ports cause false failures
- kubelet probe timeout defaults may be too low
- Distinguish startup failures from readiness failures in alerts

Red Flags (Bad Answers):
- "Use only liveness for everything"
- "Disable probes to avoid restarts"
- "Readiness restarts the pod"
--------------------------------------------------
Q4. QoS Classes, Eviction, and Node Pressure
Difficulty: Medium

What the interviewer is testing:
- QoS classification logic
- Eviction order under pressure
- Behavior with memory pressure
- OOMKill vs eviction difference
- System reserved vs kube reserved
- Ephemeral storage pressure
- Priority vs QoS interplay
- Requests/limits tuning
- Impact on scheduling
- kubelet eviction signals
- Observability via events
- Tradeoffs in burstable vs guaranteed

Question:
- During node memory pressure, some pods die unpredictably. How do you control eviction behavior using requests/limits and QoS?

Answer:
- Explanation: Guaranteed pods (requests=limits for CPU/memory) are last to be evicted; BestEffort first. Burstable in between. Evictions occur on node pressure; OOMKill happens when memory exceeds cgroup limit.
- Why this matters in production: Predictable eviction avoids losing critical workloads.

Solution:
- YAML manifests:
```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "1"
    memory: "1Gi"
```
- kubectl commands:
  - `kubectl describe node <node>`
  - `kubectl get events --sort-by=.lastTimestamp`

Edge Cases & Tradeoffs:
- Guaranteed doesn't prevent OOMKill if limit too low
- Burstable pods can still be evicted early
- High requests reduce bin packing
- CPU limits cause throttling even without pressure
- Memory pressure triggers kubelet eviction thresholds
- Ephemeral storage eviction is independent of memory
- PriorityClass can override QoS eviction ordering
- Node allocatable depends on system reserved
- Overcommitting memory increases eviction frequency
- OOMKill can occur without eviction events
- Eviction may ignore PDB if node pressure is severe
- Pods with emptyDir can trigger disk pressure

Red Flags (Bad Answers):
- "Set limits only; requests don't matter"
- "Guaranteed pods can't be killed"
- "Eviction only happens when pods exceed limits"
--------------------------------------------------
Q5. Scheduling Plugins: Filtering, Scoring, and Extenders
Difficulty: Medium

What the interviewer is testing:
- Scheduler phases: filtering and scoring
- Modern scheduler plugins
- Node fit logic
- Resource and topology constraints
- PriorityScore behavior
- Extender use cases
- Debugging scheduling failures
- Impact of custom schedulers
- Configuration via profiles
- Preemption basics
- Pod affinity scoring effects
- Scheduler events interpretation

Question:
- A pod is Pending with "no nodes available" despite free CPU. Explain the scheduler flow and how you'd debug.

Answer:
- Explanation: Scheduler filters nodes by constraints (resources, taints, affinity, volumes), then scores remaining. "No nodes available" means filter phase rejected all nodes. Use events and `kubectl describe pod` to identify the failed predicate/plugin.
- Why this matters in production: Scheduling failures can halt rollouts even when resources exist.

Solution:
- kubectl commands:
  - `kubectl describe pod <pod>`
  - `kubectl get events --field-selector involvedObject.name=<pod>`
- Config snippet:
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
  plugins:
    score:
      enabled:
      - name: NodeResourcesBalancedAllocation
```

Edge Cases & Tradeoffs:
- Volume zone constraints can filter all nodes
- Pod affinity can cause combinatorial constraints
- Node taints without tolerations block scheduling
- HostPort conflicts filter nodes
- Huge resource requests exceed single node capacity
- Extenders can veto scheduling
- Scoring doesn't matter if filter yields zero nodes
- StatefulSet PVC binding can delay scheduling
- Topology spread constraints can block scheduling
- Preemption can be disabled or blocked by PDB
- Scheduler cache lag can delay decisions
- Custom scheduler profiles can diverge behavior

Red Flags (Bad Answers):
- "The scheduler only checks CPU"
- "If nodes are free, scheduling will work"
- "Scoring errors cause Pending pods"
--------------------------------------------------
Q6. Node Affinity vs Pod Affinity/Anti-Affinity
Difficulty: Medium

What the interviewer is testing:
- Node selector vs node affinity
- Required vs preferred rules
- Pod affinity/anti-affinity semantics
- Topology keys usage
- Scheduling impact and cost
- Anti-affinity hard constraints risks
- Multi-tenant isolation patterns
- Label hygiene requirements
- Impact on rolling updates
- Failure modes in small clusters
- Soft constraints for availability
- Debugging affinity failures

Question:
- You need to keep replica pods in different zones and avoid noisy neighbors. How do you use affinity rules without blocking scheduling?

Answer:
- Explanation: Use preferred pod anti-affinity for zone distribution and required node affinity for hardware class. Prefer soft constraints for availability in small clusters.
- Why this matters in production: Hard anti-affinity can deadlock scheduling during failures.

Solution:
- YAML manifests:
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["m5.large","m5.xlarge"]
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: api
        topologyKey: topology.kubernetes.io/zone
```

Edge Cases & Tradeoffs:
- Required anti-affinity can block all scheduling
- Topology key must exist on nodes
- Labels drift causes unexpected placement
- Preferred rules can be ignored under pressure
- Pod anti-affinity increases scheduling latency
- Rolling updates may violate spread temporarily
- StatefulSet with hard anti-affinity can block scale
- Node affinity can conflict with PV zone constraints
- Small clusters can't satisfy strict constraints
- Taints/tolerations can override intended placement
- Affinity rules are not re-evaluated at runtime
- Label cardinality impacts scheduler performance

Red Flags (Bad Answers):
- "Use required anti-affinity for everything"
- "NodeSelector and affinity are identical"
- "Affinity guarantees perfect distribution"
--------------------------------------------------
Q7. Taints, Tolerations, Cordon/Drain
Difficulty: Medium

What the interviewer is testing:
- Taints vs labels
- Toleration effects and durations
- NoSchedule vs PreferNoSchedule vs NoExecute
- Drain behavior with PDBs
- Cordon vs drain differences
- DaemonSet eviction behavior
- Eviction API use
- Dedicated node pools
- Pod eviction ordering
- Node maintenance workflow
- System taints (control-plane)
- Failure impacts during drain

Question:
- You need to maintenance a node without disrupting critical workloads. Explain how cordon/drain, taints, and PDBs interact.

Answer:
- Explanation: Cordon prevents new scheduling. Drain evicts pods (except DaemonSets, unless forced) and respects PDBs. Taints enforce long-term isolation; tolerations allow exceptions.
- Why this matters in production: Poor drain strategy can cause outages during maintenance.

Solution:
- kubectl commands:
  - `kubectl cordon <node>`
  - `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`
  - `kubectl taint nodes <node> workload=dedicated:NoSchedule`
- YAML manifests:
```yaml
tolerations:
- key: "workload"
  operator: "Equal"
  value: "dedicated"
  effect: "NoSchedule"
```

Edge Cases & Tradeoffs:
- PDBs can block drain indefinitely
- DaemonSet pods are not evicted by default
- Local storage pods require `--delete-emptydir-data`
- NoExecute taints evict existing pods after tolerationSeconds
- Force drain can break stateful workloads
- Cordoned node still runs existing pods
- Taints don't affect already-running pods
- Grace periods may extend maintenance windows
- Eviction can trigger cascade in dependent services
- Drain order can matter for stateful clusters
- System-critical pods may be protected
- Not all controllers handle eviction gracefully

Red Flags (Bad Answers):
- "Cordon drains the node"
- "Taints evict all pods immediately"
- "PDBs are ignored during drain"
--------------------------------------------------
Q8. Topology Spread Constraints
Difficulty: Medium

What the interviewer is testing:
- maxSkew semantics
- whenUnsatisfiable effects
- topologyKeys usage
- labelSelector correctness
- Scheduling impact on scale
- Interaction with HPA/rollouts
- Soft vs hard constraints
- Small cluster behavior
- Failure handling with zones
- Scheduler scoring vs filtering
- Multi-topology constraints
- Debugging skew issues

Question:
- You want replicas evenly spread across zones and nodes. How do you set topology spread constraints without blocking scheduling?

Answer:
- Explanation: Use `maxSkew` with `whenUnsatisfiable: ScheduleAnyway` for soft spread and `DoNotSchedule` for strict. Ensure selector matches pod labels.
- Why this matters in production: Incorrect constraints can cause Pending pods during incidents.

Solution:
- YAML manifests:
```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: ScheduleAnyway
  labelSelector:
    matchLabels:
      app: api
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: api
```

Edge Cases & Tradeoffs:
- Wrong selector results in no spreading
- DoNotSchedule blocks pods in small clusters
- Skew computed per topology domain
- Rollouts can temporarily violate skew
- Missing topology labels break scheduling
- Pod affinity can conflict with spread rules
- DaemonSets ignore spread constraints
- StatefulSets may need strict ordering
- Autoscaler may add nodes in wrong zone
- Pod counts with odd numbers can still skew
- Preemption may bypass soft constraints
- High cardinality topologies increase scheduler cost

Red Flags (Bad Answers):
- "Topology spread always guarantees even spread"
- "Use only DoNotSchedule for production"
- "Selectors don't matter for spread"
--------------------------------------------------
Q9. PriorityClass and Preemption
Difficulty: Medium

What the interviewer is testing:
- PriorityClass usage and scope
- Preemption behavior
- GlobalDefault priority
- Starvation risks
- PDB impact on preemption
- Graceful vs forced evictions
- Scheduling fairness
- Critical workloads configuration
- Risk of cascading evictions
- Observability via events
- PodPriority feature dependencies
- Use in multi-tenant clusters

Question:
- During incident response, you need critical pods to schedule even when the cluster is full. How do you use PriorityClass safely?

Answer:
- Explanation: Define a high PriorityClass for critical workloads. Preemption can evict lower-priority pods if no fit is found. Use sparingly to avoid cluster churn.
- Why this matters in production: Misuse can cause widespread evictions and instability.

Solution:
- YAML manifests:
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical
value: 100000
globalDefault: false
description: "Critical system workload"
```
```yaml
priorityClassName: critical
```

Edge Cases & Tradeoffs:
- Preemption doesn't help if no node fits
- PDBs can block eviction, preemption fails
- Too many high-priority pods cause starvation
- PriorityClass is global across namespaces
- Preempted pods may not reschedule quickly
- Short-lived spikes can trigger repeated evictions
- Preemption can violate topology spread goals
- Guaranteed QoS with low priority still evicted
- Cluster autoscaler may respond late
- Critical addons should avoid preemption storm
- Priority changes don't re-evaluate existing pods
- Event logs may be noisy and hard to parse

Red Flags (Bad Answers):
- "Set all pods to highest priority"
- "Preemption always schedules the pod"
- "PriorityClass is namespace-scoped"
--------------------------------------------------
Q10. PodDisruptionBudget Semantics
Difficulty: Medium

What the interviewer is testing:
- PDB minAvailable vs maxUnavailable
- Voluntary disruptions vs involuntary
- Eviction API interactions
- Effect on drain and upgrades
- Scaling interactions with PDB
- StatefulSet considerations
- PDB across multiple controllers
- Pod readiness requirement
- PDB with unhealthy pods
- Risk of blocking maintenance
- PDB and preemption interplay
- Failure mode when PDB is too strict

Question:
- Your node drains are stuck. There's a PDB on a StatefulSet. Explain how PDB works and how to unblock safely.

Answer:
- Explanation: PDBs only apply to voluntary disruptions (evictions). If minAvailable is too high relative to replicas or pods are unhealthy, evictions are blocked. Adjust PDB or scale up before drain.
- Why this matters in production: PDBs can prevent upgrades and maintenance.

Solution:
- kubectl commands:
  - `kubectl get pdb`
  - `kubectl describe pdb <name>`
  - `kubectl scale statefulset db --replicas=5`
- YAML manifests:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: db-pdb
spec:
  minAvailable: 4
  selector:
    matchLabels:
      app: db
```

Edge Cases & Tradeoffs:
- Unhealthy pods reduce available count
- Single-replica workloads can't have minAvailable:1
- PDBs don't stop involuntary evictions
- Using maxUnavailable with small replica counts
- PDB selector mismatch gives false safety
- Evictions ignore PDB during node pressure
- StatefulSet ordinal ordering can slow drain
- PDB with HPA scaling down can block eviction
- PDBs don't cover DaemonSets
- Preemption can bypass PDB in some cases
- Misconfigured PDB can cause rollout failures
- PDB updates themselves can be blocked by RBAC

Red Flags (Bad Answers):
- "PDB prevents all pod restarts"
- "PDB applies to OOMKills"
- "PDBs don't affect drain"
--------------------------------------------------
Q11. RuntimeClass and GPU Scheduling Basics
Difficulty: Medium

What the interviewer is testing:
- RuntimeClass usage
- Multiple runtimes on same node
- GPU resource requests
- Device plugin role
- Scheduling constraints for GPUs
- Taints on GPU nodes
- Isolation vs performance tradeoffs
- Security implications of runtime
- RuntimeClass overhead
- Compatibility with node pools
- Observability of device allocation
- Failure modes with device plugin

Question:
- You need to run GPU workloads on a subset of nodes with a specific runtime. Describe the setup.

Answer:
- Explanation: Use RuntimeClass to select a runtime (e.g., NVIDIA). Request GPU resources. Taint GPU nodes and tolerate from GPU pods to avoid accidental scheduling.
- Why this matters in production: Prevents non-GPU workloads from consuming expensive nodes.

Solution:
- YAML manifests:
```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: nvidia
handler: nvidia
```
```yaml
spec:
  runtimeClassName: nvidia
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
  containers:
  - name: trainer
    image: myrepo/train:1.0
    resources:
      limits:
        nvidia.com/gpu: "1"
```

Edge Cases & Tradeoffs:
- Device plugin must be installed and healthy
- GPU requests are limits-only; no overcommit
- Taints block scheduling without tolerations
- RuntimeClass missing causes pod failure
- GPU node scarcity causes Pending pods
- Cluster autoscaler may not scale GPU pools
- RuntimeClass affects all containers in pod
- GPU memory is not isolated by default
- Version mismatch between driver and runtime
- Pod security restrictions may block runtime
- Monitoring GPU usage requires node-level tooling
- Preemption does not guarantee GPU availability

Red Flags (Bad Answers):
- "GPU nodes automatically pick GPU pods"
- "RuntimeClass is a security policy"
- "You can overcommit GPUs safely"
--------------------------------------------------
Q12. Deployment Rollouts: Surge and Unavailable
Difficulty: Medium

What the interviewer is testing:
- Rolling update mechanics
- maxSurge/maxUnavailable tuning
- ProgressDeadlineSeconds
- Readiness gating
- Rollback behavior
- Observability of rollout status
- Availability tradeoffs
- Impact on cluster capacity
- Strategies for zero-downtime
- Interaction with PDBs
- Deployment vs ReplicaSet ownership
- Failure modes with bad probes

Question:
- A critical API must have zero downtime during rollouts. Explain how to configure Deployment strategy and what risks remain.

Answer:
- Explanation: Set maxUnavailable: 0 and a small maxSurge. Ensure readiness probes are correct. Rollouts still depend on capacity and proper draining.
- Why this matters in production: Bad rollout tuning can cause outages or stuck deployments.

Solution:
- YAML manifests:
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
progressDeadlineSeconds: 600
```
- kubectl commands:
  - `kubectl rollout status deploy/api`
  - `kubectl rollout history deploy/api`

Edge Cases & Tradeoffs:
- Need spare capacity for surge
- Readiness probe flaps cause rollout stalls
- PDB can block new pod scheduling
- Large images slow rollout
- Progress deadline can trigger rollback
- Surge pods may violate quotas
- Rolling update can still drop connections
- Old pods may terminate before new pods ready if misconfig
- HPA scale events interact with rollout
- Stateful dependencies might require ordered updates
- Canary/blue-green may be safer for breaking changes
- Cluster autoscaler may add nodes too late

Red Flags (Bad Answers):
- "Set replicas to 1 and maxUnavailable 0"
- "Rollouts are always safe by default"
- "maxSurge doesn't affect capacity"
--------------------------------------------------
Q13. StatefulSet Identity and Ordered Rollouts
Difficulty: Medium

What the interviewer is testing:
- Stable network identity
- Ordered scale-up/down
- volumeClaimTemplates
- Partitioned rollouts
- Headless Service requirements
- PodManagementPolicy implications
- StatefulSet vs Deployment selection
- Data consistency concerns
- DNS patterns for StatefulSet
- Scale-down behavior
- Storage reclaim policies
- Upgrade sequencing tradeoffs

Question:
- You run a database that requires stable identities and ordered upgrades. How do you use StatefulSet and what pitfalls exist?

Answer:
- Explanation: StatefulSet provides stable pod names, stable storage via PVCs, and ordered rollout/scale. Use headless Service for DNS. Partitioned rollouts can control update order.
- Why this matters in production: Incorrect setup can lead to data loss or split-brain.

Solution:
- YAML manifests:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: db
  replicas: 3
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 1
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: db
        image: myrepo/db:4.2
        volumeMounts:
        - name: data
          mountPath: /var/lib/db
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

Edge Cases & Tradeoffs:
- PVCs persist even after pod deletion
- Scaling down leaves PVCs orphaned by default
- Partitioned rollout requires manual bump
- Headless Service is required for stable DNS
- PodManagementPolicy Parallel can break ordering
- DNS caches can cause stale endpoints
- Updates can block if one pod doesn't become Ready
- Zone constraints can block scheduling with PVCs
- StatefulSet doesn't guarantee data replication safety
- Deleting StatefulSet doesn't delete PVCs
- Restoring from backups is still manual
- In-place resizing depends on StorageClass support

Red Flags (Bad Answers):
- "StatefulSet guarantees data consistency"
- "You can safely use Deployment for databases"
- "Headless Service is optional"
--------------------------------------------------
Q14. Jobs and CronJobs: Backoff and Deadlines
Difficulty: Medium

What the interviewer is testing:
- Job retry semantics
- backoffLimit behavior
- activeDeadlineSeconds
- CronJob concurrencyPolicy
- startingDeadlineSeconds
- TTLAfterFinished cleanup
- History limits
- Failure modes with missed schedules
- Idempotency requirements
- Parallelism/completions
- Resource requests for batch
- Observability and debugging

Question:
- A CronJob runs a cleanup task but sometimes overlaps and overloads the DB. How do you prevent overlap and handle retries safely?

Answer:
- Explanation: Use `concurrencyPolicy: Forbid` to prevent overlap. Configure backoffLimit and activeDeadlineSeconds. Ensure job is idempotent for retries.
- Why this matters in production: Overlapping batch jobs can cause outages and data corruption.

Solution:
- YAML manifests:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup
spec:
  schedule: "0 * * * *"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 300
  jobTemplate:
    spec:
      backoffLimit: 3
      activeDeadlineSeconds: 600
      ttlSecondsAfterFinished: 3600
      template:
        spec:
          restartPolicy: Never
          containers:
          - name: cleanup
            image: myrepo/cleanup:1.0
```

Edge Cases & Tradeoffs:
- Forbid can skip runs if previous job hangs
- Allow can cause overlapping workloads
- Replace can kill active jobs mid-flight
- Time drift on nodes can affect schedules
- Missed schedules beyond deadline are skipped
- Jobs must be idempotent under retries
- backoffLimit applies per job, not per pod
- activeDeadlineSeconds kills jobs prematurely
- High parallelism can overload dependencies
- CronJob controller lag at scale
- TTL cleanup can remove logs too early
- Cluster upgrades can pause CronJobs

Red Flags (Bad Answers):
- "CronJob ensures exactly once"
- "backoffLimit controls CronJob frequency"
- "Use restartPolicy Always for Jobs"
--------------------------------------------------
Q15. Service Types and External Access
Difficulty: Medium

What the interviewer is testing:
- ClusterIP vs NodePort vs LoadBalancer
- ExternalName limitations
- Source IP preservation
- ExternalTrafficPolicy effects
- Health checks vs readiness
- Use cases for each type
- Security exposure risks
- NodePort port range constraints
- Load balancer provisioning behavior
- Hairpin traffic considerations
- Service selectors vs endpoints
- Failure modes with no endpoints

Question:
- A service needs internal cluster access and optional external access for debugging. Which service type(s) do you use, and what pitfalls exist?

Answer:
- Explanation: Use ClusterIP for internal access; add NodePort or LoadBalancer only when needed. ExternalTrafficPolicy: Local preserves source IP but requires local endpoints.
- Why this matters in production: Wrong service type can expose services unintentionally or break client IP logging.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8080
```
```yaml
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
```

Edge Cases & Tradeoffs:
- NodePort exposes on all nodes, broad attack surface
- ExternalTrafficPolicy Local drops traffic without local pods
- LoadBalancer provisioning can be slow or unsupported
- ExternalName doesn't create endpoints or health checks
- Health checks may hit non-ready pods if misconfigured
- Session affinity can mask rollout issues
- Hairpin traffic may fail on some CNIs
- Port collisions in NodePort range
- Source IP preserved only in Local policy
- No endpoints yields 503 from LBs or kube-proxy
- Mixed protocols on same service can be tricky
- Cloud LB health checks may bypass readiness

Red Flags (Bad Answers):
- "Use NodePort for internal traffic"
- "ExternalName works like ClusterIP"
- "LoadBalancer always preserves source IP"
--------------------------------------------------
Q16. Headless Services and StatefulSet DNS
Difficulty: Hard

What the interviewer is testing:
- Headless service behavior
- DNS records per pod
- StatefulSet stable identities
- SRV records and port discovery
- Endpoint vs EndpointSlice representation
- Client-side load balancing
- Failure modes with stale DNS
- Service discovery in stateful apps
- Readiness gating of DNS records
- Pod readiness and endpoints
- Use in databases and queues
- Observability of endpoints

Question:
- You're deploying a distributed database that needs peer discovery. How do you set up headless Service and what can go wrong?

Answer:
- Explanation: Headless Service (`clusterIP: None`) exposes pod IPs directly and creates DNS records per pod for StatefulSet. Clients do their own load balancing and retries.
- Why this matters in production: Incorrect DNS or readiness settings can cause split-brain or failed joins.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: db
spec:
  clusterIP: None
  selector:
    app: db
  ports:
  - name: db
    port: 5432
```

Edge Cases & Tradeoffs:
- DNS caching can keep stale IPs
- Pod readiness controls endpoint publication
- Without readinessProbe, unready pods get DNS
- Clients must handle multiple A records
- Some libraries ignore SRV records
- Headless service bypasses kube-proxy load balancing
- NetworkPolicy must allow pod-to-pod traffic
- Dual-stack DNS can confuse older clients
- Large StatefulSets can increase DNS response size
- EndpointSlice limits can affect DNS
- Pod IP changes break clients using cached IPs
- Incorrect selector yields empty DNS records

Red Flags (Bad Answers):
- "Headless service load balances pods"
- "StatefulSet doesn't need a Service"
- "DNS always updates instantly"
--------------------------------------------------
Q17. kube-proxy: iptables vs IPVS
Difficulty: Hard

What the interviewer is testing:
- Differences between proxy modes
- Scaling behavior
- IPVS requirements
- Conntrack and performance
- Debugging service routing
- Failure modes under high endpoints
- Node-level dependencies
- Health check and session affinity behavior
- Observability commands
- Tradeoffs in large clusters
- How kube-proxy programs rules
- Interaction with CNI

Question:
- In a large cluster, Service traffic is slow and kube-proxy CPU is high. How does switching to IPVS help, and what risks exist?

Answer:
- Explanation: IPVS uses kernel load balancing tables, more efficient at scale than iptables. It reduces rule churn but requires kernel modules and IPVS tools.
- Why this matters in production: Service scale impacts latency and node CPU.

Solution:
- kubectl commands:
  - `kubectl -n kube-system get configmap kube-proxy -o yaml`
- Config snippet:
```yaml
mode: "ipvs"
ipvs:
  strictARP: true
```

Edge Cases & Tradeoffs:
- Missing kernel modules prevent IPVS
- strictARP required for some L2 load balancers
- IPVS still relies on conntrack; exhaustion causes drops
- Debugging IPVS requires ipvsadm
- Inconsistent mode across nodes complicates ops
- kube-proxy reload restarts can disrupt traffic
- Very large EndpointSlices still create overhead
- IPVS scheduling algorithms may differ from expectations
- sessionAffinity handling can differ in edge cases
- iptables fallback if IPVS fails
- CNI may have its own service handling (eBPF)
- kube-proxy config changes require rollout

Red Flags (Bad Answers):
- "IPVS always faster and simpler"
- "Switching modes requires no kernel changes"
- "kube-proxy does CNI routing"
--------------------------------------------------
Q18. CoreDNS: Upstream, StubDomains, Caching
Difficulty: Hard

What the interviewer is testing:
- CoreDNS configuration
- Upstream DNS forwarding
- Stub domains usage
- Cache behavior and TTL
- Failure modes (SERVFAIL, NXDOMAIN)
- DNS latency impact on apps
- Split-horizon DNS patterns
- Metrics and logging
- Config reload behavior
- Pod DNS policy
- Search paths and ndots
- Debugging DNS issues

Question:
- Some internal domains resolve slowly; others fail with SERVFAIL. How do you configure CoreDNS and what failure modes do you check?

Answer:
- Explanation: Use `forward` to upstream resolvers, `stubDomains` for internal zones, and `cache` to reduce latency. Misconfigured upstreams or loops cause SERVFAIL.
- Why this matters in production: DNS is a critical dependency for service discovery.

Solution:
- Config snippet:
```yaml
data:
  Corefile: |
    .:53 {
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa
        forward . 10.0.0.2 10.0.0.3
        cache 30
        reload
    }
    corp.internal:53 {
        forward . 10.1.0.10
        cache 60
    }
```
- kubectl commands:
  - `kubectl -n kube-system logs deploy/coredns`

Edge Cases & Tradeoffs:
- Upstream timeouts cause pod DNS delays
- ndots default (5) can cause slow lookups
- StubDomains bypass Kubernetes DNS
- Cache can serve stale records
- CoreDNS pods need proper resource limits
- DNS loops if forward points to cluster DNS
- Large responses can exceed UDP and fail
- Search domains cause unexpected queries
- NetworkPolicy can block CoreDNS egress
- NodeLocal DNSCache can mitigate latency
- Multi-tenant zones require careful config
- Config reload can briefly drop queries

Red Flags (Bad Answers):
- "CoreDNS always uses `/etc/resolv.conf` only"
- "DNS failures are always network issues"
- "StubDomains are for public DNS only"
--------------------------------------------------
Q19. EndpointSlices vs Endpoints at Scale
Difficulty: Hard

What the interviewer is testing:
- Why EndpointSlices exist
- Scaling limits of Endpoints
- Watch/list pressure on API server
- Service routing behavior
- Controller updates and churn
- Observability of EndpointSlices
- Label selectors for endpoints
- Session affinity interactions
- EndpointSlice topology hints
- Impact on kube-proxy
- Migration considerations
- Failure cases with stale endpoints

Question:
- A Service has thousands of endpoints and kube-proxy is lagging. How do EndpointSlices help and what should you monitor?

Answer:
- Explanation: EndpointSlices split endpoints into smaller objects, reducing watch payloads and update churn. kube-proxy reads slices for routing, improving scale.
- Why this matters in production: Large services can overload API server and kube-proxy.

Solution:
- kubectl commands:
  - `kubectl get endpointslices -l kubernetes.io/service-name=api`
  - `kubectl describe endpointslice <name>`

Edge Cases & Tradeoffs:
- EndpointSlice controller lag can delay updates
- Mixed Endpoints and EndpointSlices during migration
- Too many slices still create high churn
- Topology hints require controller support
- Some tools still read Endpoints only
- Missing labels can break selector-based queries
- Stale endpoints can cause 503s
- Large namespaces with many services increase watch pressure
- IPVS/iptables still need per-endpoint rules
- EndpointSlice features depend on Kubernetes version
- ExternalTrafficPolicy Local changes endpoints selection
- DNS uses EndpointSlices but caching can lag

Red Flags (Bad Answers):
- "EndpointSlices are just cosmetic"
- "Endpoints scale to any size"
- "kube-proxy doesn't use EndpointSlices"
--------------------------------------------------
Q20. NetworkPolicies: Default Deny and DNS Pitfalls
Difficulty: Hard

What the interviewer is testing:
- Default deny behavior
- Namespace vs pod selectors
- Egress rules for DNS
- Common DNS failures with policies
- Policy enforcement by CNI
- Ingress vs egress semantics
- Label hygiene for policy targets
- Order of evaluation
- Limitations (L7 not supported)
- Troubleshooting dropped traffic
- Cross-namespace access patterns
- Behavior with hostNetwork pods

Question:
- After adding a default deny policy, apps can't resolve DNS. How do you fix it and what else might break?

Answer:
- Explanation: You must explicitly allow egress to DNS (CoreDNS) and any required external services. NetworkPolicies are additive; without egress rules, DNS is blocked.
- Why this matters in production: Default deny is safe, but can silently break dependencies.

Solution:
- YAML manifests:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
spec:
  podSelector: {}
  policyTypes: ["Egress"]
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

Edge Cases & Tradeoffs:
- CNI must support NetworkPolicy
- DNS runs on different labels in some distros
- NodeLocal DNSCache requires different targets
- HostNetwork pods bypass policies
- Egress to external IPs requires IPBlock
- Policies are namespace-scoped
- Service IPs vs pod IPs for DNS access
- Policies don't apply to Services, only pods
- Default deny can block metrics scraping
- Selector mistakes can allow unintended traffic
- UDP DNS fallback to TCP may be blocked
- Some CNIs implement policy differently at scale

Red Flags (Bad Answers):
- "NetworkPolicy is enforced by kube-proxy"
- "Default deny only blocks ingress"
- "DNS uses Service IP so no policy needed"
--------------------------------------------------
Q21. CNI vs kube-proxy Responsibilities
Difficulty: Hard

What the interviewer is testing:
- CNI role in pod networking
- kube-proxy role in service routing
- Overlay vs routed network models
- IPAM responsibilities
- Differences between CNI plugins
- Host-to-pod vs pod-to-pod paths
- Service VIP handling alternatives (eBPF)
- Node-level networking configuration
- Debugging pod connectivity
- NetworkPolicy enforcement location
- MTU issues in overlay networks
- Failure modes with CNI crashes

Question:
- A pod can ping another pod's IP but cannot reach the Service IP. Explain why and how you'd troubleshoot.

Answer:
- Explanation: Pod IP connectivity is CNI, Service VIP routing is kube-proxy (or eBPF). If Service IP fails, check kube-proxy health, iptables/IPVS rules, and endpoints.
- Why this matters in production: Distinguishing CNI vs kube-proxy issues speeds resolution.

Solution:
- kubectl commands:
  - `kubectl get endpoints api`
  - `kubectl -n kube-system get pods -l k8s-app=kube-proxy`
- Config snippet:
```yaml
# kube-proxy configmap should match desired mode
mode: "iptables"
```

Edge Cases & Tradeoffs:
- Endpoints empty due to readiness failure
- kube-proxy crash loops remove service rules
- iptables rules exceed limits in large clusters
- Service IP conflicts with node routes
- CNI MTU mismatch causes dropped packets
- eBPF dataplanes may bypass kube-proxy
- NodeLocal DNSCache interacts with Service IPs
- Pod network policy blocks Service traffic
- Dual-stack misconfig breaks Service IP for one family
- Hairpin mode may block pod-to-service on same node
- ExternalTrafficPolicy affects routing
- EndpointSlice controller lag yields stale routing

Red Flags (Bad Answers):
- "CNI handles Service VIPs"
- "If pods can ping, services must work"
- "kube-proxy only does DNS"
--------------------------------------------------
Q22. Ingress vs Gateway API
Difficulty: Hard

What the interviewer is testing:
- API model differences
- Separation of concerns (GatewayClass, Gateway, Route)
- Multitenancy
- Extensibility and policy attachment
- Migration considerations
- Controller support differences
- Listener and hostname matching
- Shared vs dedicated gateways
- Security boundaries
- Observability and status reporting
- Feature parity with Ingress
- Failure modes in routing

Question:
- Your platform team wants to standardize north-south routing. When would you choose Gateway API over Ingress, and what are the operational implications?

Answer:
- Explanation: Gateway API provides richer, more structured model with separation between infrastructure and routes, enabling safer multi-tenant configs. Ingress is simpler but less expressive.
- Why this matters in production: Correct model prevents configuration sprawl and unsafe overrides.

Solution:
- YAML manifests:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: edge
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    hostname: "*.example.com"
```
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api
spec:
  parentRefs:
  - name: edge
  hostnames: ["api.example.com"]
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /v1
    backendRefs:
    - name: api
      port: 80
```

Edge Cases & Tradeoffs:
- Controller support for Gateway API is uneven
- Policy attachment varies by controller
- Multi-namespace routes require ReferenceGrant
- Migration from Ingress can be non-trivial
- Status conditions can be confusing
- GatewayClass config is cluster-wide
- TLS cert management differs by controller
- Route conflicts require clear precedence
- Missing listeners cause 404/503
- Controller upgrades can change behavior
- Some features only in experimental APIs
- Ingress may still be needed for legacy tools

Red Flags (Bad Answers):
- "Gateway API is just a renamed Ingress"
- "Ingress is obsolete everywhere"
- "Gateway API doesn't need controller support"
--------------------------------------------------
Q23. TLS Termination and SNI in Ingress
Difficulty: Hard

What the interviewer is testing:
- TLS secret formats
- SNI routing behavior
- Wildcard vs SAN certs
- Secret scope and namespace rules
- Controller-specific expectations
- TLS passthrough vs termination
- Cert rotation impacts
- HTTP/2 and ALPN behavior
- Misconfigured hostnames
- Security implications of shared certs
- Debugging 404/503 for TLS
- IngressClass usage

Question:
- A multi-tenant cluster serves multiple domains via one Ingress controller. Explain how SNI-based TLS works and common pitfalls.

Answer:
- Explanation: Ingress controllers use SNI to pick the correct cert based on hostname. TLS secrets must be in the same namespace as the Ingress (for most controllers). Mismatched hostnames cause default cert use.
- Why this matters in production: TLS misconfig breaks customer traffic and security guarantees.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-tls
type: kubernetes.io/tls
data:
  tls.crt: <base64>
  tls.key: <base64>
```
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
spec:
  ingressClassName: nginx
  tls:
  - hosts: ["api.example.com"]
    secretName: api-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 80
```

Edge Cases & Tradeoffs:
- Secret in wrong namespace won't be found
- Wildcard certs don't cover apex domain
- SNI requires clients supporting TLS SNI
- Default cert used if host mismatch
- TLS passthrough bypasses Ingress routing
- Cert rotation can cause brief reload errors
- Multiple Ingresses for same host can conflict
- ALPN can affect HTTP/2 behavior
- Incorrect IngressClass routes to wrong controller
- Certificate chain issues cause handshake failures
- Hostname case sensitivity in some clients
- Large number of certs can slow controller reloads

Red Flags (Bad Answers):
- "TLS secrets are cluster-wide"
- "SNI works without host rules"
- "Wildcard cert covers all subdomains and root"
--------------------------------------------------
Q24. Ingress 404/503 Failure Modes
Difficulty: Hard

What the interviewer is testing:
- Difference between 404 and 503 at Ingress
- Backend Service/port mismatches
- Readiness gating endpoints
- Health check behavior
- Path matching and rewrite issues
- IngressClass misrouting
- Controller logs and events
- Service selector mismatches
- Endpoints vs EndpointSlices
- NetworkPolicy and CNI effects
- TLS vs HTTP mismatch
- Debugging methodology

Question:
- An Ingress returns 503 for a healthy service. Walk through the most likely causes and how you'd verify.

Answer:
- Explanation: 503 often means no healthy endpoints or controller can't reach backend. Check Service selectors, pod readiness, endpoint slices, ports, and NetworkPolicies.
- Why this matters in production: Ingress failures are user-facing outages.

Solution:
- kubectl commands:
  - `kubectl get ingress api -o yaml`
  - `kubectl get endpoints api`
  - `kubectl describe svc api`
  - `kubectl logs -n ingress-nginx deploy/ingress-nginx-controller`

Edge Cases & Tradeoffs:
- Service selector doesn't match pod labels
- targetPort mismatch sends traffic to wrong port
- Readiness probe failing, so endpoints empty
- IngressClass points to wrong controller
- NetworkPolicy blocks ingress controller to pods
- Backend service in different namespace unsupported
- Path rewrite strips required prefix
- HTTPS backend but HTTP configured
- Ingress controller sync delay after updates
- EndpointSlice controller lag
- Pods on hostNetwork not reachable via cluster IP
- TLS termination misconfigured causes 400/503

Red Flags (Bad Answers):
- "503 always means Ingress is down"
- "If pods are Running, endpoints must exist"
- "Ingress ignores readiness"
--------------------------------------------------
Q25. ConfigMaps: Reload Patterns and Pitfalls
Difficulty: Hard

What the interviewer is testing:
- Env vs volume mounts
- Immutable ConfigMaps
- Reload behavior for volume mounts
- Application reload patterns
- Sidecar reloader pattern
- Risk of partial updates
- Update propagation delay
- Interaction with Deployments
- Config drift and consistency
- Resource versioning
- Security of config contents
- Failure modes on missing config

Question:
- You need to update config without redeploying. How do you do it safely, and what can go wrong?

Answer:
- Explanation: Mount ConfigMaps as volumes; updates are eventually consistent. Use an app-side reload or sidecar reloader. For env vars, you must restart pods.
- Why this matters in production: Mismanaged config reloads can cause inconsistent behavior.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: "safe"
```
```yaml
volumeMounts:
- name: config
  mountPath: /etc/app
volumes:
- name: config
  configMap:
    name: app-config
```

Edge Cases & Tradeoffs:
- Volume updates can lag (up to minutes)
- Apps must watch file changes to reload
- Atomic update via symlink can break naive watchers
- Immutable ConfigMaps require rolling restart
- Large ConfigMaps can slow kubelet
- Missing ConfigMap blocks pod startup
- Env var config requires pod restart
- Rolling updates can yield mixed config versions
- Sidecar reloaders add resource overhead
- Config changes can break backwards compatibility
- Mutating config in-place can be overwritten by kubelet
- Relying on `kubectl edit` in production is risky

Red Flags (Bad Answers):
- "Env vars reload automatically"
- "ConfigMaps are immutable by default"
- "Config changes are instantly consistent"
--------------------------------------------------
Q26. Secrets: Mounting, Injection, and Encryption at Rest
Difficulty: Hard

What the interviewer is testing:
- Secrets as env vs volume
- Base64 misconceptions
- Secret rotation patterns
- Encryption at rest
- KMS provider concepts
- Secret distribution risks
- ServiceAccount token projection
- Avoiding secret sprawl
- ReadOnly filesystem concerns
- Observability of secret access
- RBAC for secrets
- Failure modes on missing secrets

Question:
- You must store database credentials securely and support rotation. Describe the best practices and operational caveats.

Answer:
- Explanation: Store as Secret, mount as volume for rotation. Base64 is not encryption. Use encryption at rest with KMS. Rotate by updating Secret and reloading or restarting pods.
- Why this matters in production: Secrets leakage is a critical security risk.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: dXNlcg==
  password: c2VjdXJl
```
```yaml
volumeMounts:
- name: db-secret
  mountPath: /etc/secret
  readOnly: true
volumes:
- name: db-secret
  secret:
    secretName: db-secret
```

Edge Cases & Tradeoffs:
- Env vars don't rotate without restart
- Mounted secrets update with delay
- Secrets in logs or crash dumps leak
- RBAC misconfig exposes secrets broadly
- KMS misconfig can break API server startup
- Encrypting at rest doesn't protect in-memory usage
- Secret size limits (~1MiB) can be exceeded
- Sidecar reloaders need access to secrets
- Secret rotation can cause app reconnect storms
- ImagePullSecrets are separate from runtime secrets
- External secrets require controller availability
- Base64 strings can be accidentally copied

Red Flags (Bad Answers):
- "Base64 makes Secrets secure"
- "Secrets are encrypted automatically"
- "Use ConfigMaps for credentials"
--------------------------------------------------
Q27. Requests vs Limits: CPU Throttling and OOMKills
Difficulty: Hard

What the interviewer is testing:
- CPU throttling behavior
- Memory limits and OOMKill
- Requests impact on scheduling
- Burstable vs Guaranteed QoS
- Observability of throttling
- Impact on latency
- Overcommit strategies
- LimitRange policy usage
- Node allocatable behavior
- Pod eviction ordering
- Headroom planning
- Failure modes with too-low limits

Question:
- A latency-sensitive service has intermittent spikes and occasional OOMKills. How do you tune requests/limits and detect CPU throttling?

Answer:
- Explanation: CPU limits throttle; memory limits kill. Set requests to guaranteed baseline and either remove or increase CPU limits for latency-sensitive workloads. Watch `throttled_time` in cgroup metrics.
- Why this matters in production: Misconfigured limits cause hidden performance regressions.

Solution:
- YAML manifests:
```yaml
resources:
  requests:
    cpu: "1"
    memory: "2Gi"
  limits:
    cpu: "2"
    memory: "3Gi"
```
- kubectl commands:
  - `kubectl top pod -n prod`
  - `kubectl describe pod <pod> | findstr -i OOM`

Edge Cases & Tradeoffs:
- No CPU limits can cause noisy neighbor
- CPU limits too low cause throttling spikes
- Memory limits too low cause OOMKill loops
- Requests too high reduce bin packing
- Burstable pods may be evicted under pressure
- HPA scaling can mask throttling
- Node allocatable differs from capacity
- Large pages and page cache consume memory
- JVM heap tuning must align with limits
- QoS class influences eviction priority
- CPU throttling not visible in kubectl top
- Spiky workloads need headroom for burst

Red Flags (Bad Answers):
- "Limits are optional for memory"
- "CPU limits improve performance"
- "OOMKills are unrelated to limits"
--------------------------------------------------
Q28. HPA: Metrics Sources and Stabilization
Difficulty: Hard

What the interviewer is testing:
- Metrics-server vs custom metrics
- HPA target utilization vs value
- Stabilization windows
- Scale-up/down behavior
- Missing metrics failures
- HPA v2 behavior
- Cooldowns vs stabilization
- Interaction with PDB and rollouts
- Scaling based on external metrics
- Resource request requirement for CPU scaling
- Observability of HPA decisions
- Failure modes with custom metrics

Question:
- HPA isn't scaling despite high CPU. Explain why and how you'd fix it.

Answer:
- Explanation: HPA uses CPU utilization relative to requests; if requests are too high or missing, scaling may not occur. Ensure metrics-server is healthy and requests are set. Adjust behavior and stabilization.
- Why this matters in production: Misconfigured HPA leads to poor performance or wasted resources.

Solution:
- YAML manifests:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```
- kubectl commands:
  - `kubectl describe hpa api-hpa`

Edge Cases & Tradeoffs:
- Missing CPU requests disables utilization-based scaling
- Metrics-server outage causes "unknown" metrics
- Custom metrics pipeline can lag
- Scale-up too aggressive can overload dependencies
- Scale-down stabilization delays cost savings
- HPA conflicts with manual scaling
- HPA ignores pods not Ready for some metrics
- Warm-up time for new pods can cause oscillation
- High request values suppress scaling
- Multiple metrics choose the max required replicas
- HPA doesn't change resource requests
- PDBs can prevent scale-down

Red Flags (Bad Answers):
- "HPA scales on CPU usage directly"
- "No need to set requests"
- "HPA will work without metrics-server"
--------------------------------------------------
Q29. VPA Safety and Eviction Impact
Difficulty: Hard

What the interviewer is testing:
- VPA modes (Off/Initial/Auto)
- Evictions for updates
- Incompatibility with HPA on CPU
- Safe workloads for VPA
- Metrics requirements
- Resource tuning strategy
- Impact on stateful services
- Vertical Pod Autoscaler recommender
- PDB interactions
- Node fragmentation risks
- Memory-based recommendations
- Operational rollout patterns

Question:
- You want to use VPA to optimize resource usage. Which workloads are safe, and how do you avoid downtime?

Answer:
- Explanation: VPA Auto evicts pods to apply new requests. It's safer for stateless workloads or with PDBs and sufficient replicas. Avoid HPA CPU conflicts; use VPA for memory or in Initial mode.
- Why this matters in production: VPA can cause hidden disruptions.

Solution:
- YAML manifests:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: "Auto"
```

Edge Cases & Tradeoffs:
- VPA Auto evicts pods at any time
- HPA and VPA both on CPU conflict
- Stateful workloads may not tolerate evictions
- PDBs can block VPA updates
- Large increases can prevent scheduling
- Recommendation lag causes oscillation
- Requests increase can reduce bin packing
- VPA initial mode only applies at creation
- Recommender needs metrics-server
- VPA does not change limits by default
- OOMKills still possible if limits too low
- Evictions during rollout can extend downtime

Red Flags (Bad Answers):
- "VPA is safe for stateful databases"
- "VPA replaces HPA completely"
- "VPA doesn't evict pods"
--------------------------------------------------
Q30. Cluster Autoscaler: Node Groups and Blockers
Difficulty: Hard

What the interviewer is testing:
- Autoscaler triggers (Pending pods)
- Node group configuration
- Scaling blockers (PDBs, taints, affinities)
- Balance across zones
- DaemonSet overhead handling
- Priority and preemption effects
- Scale-down logic and grace periods
- Expander strategies
- Capacity types (spot/on-demand)
- Cost vs availability tradeoffs
- Observability of autoscaler decisions
- Common misconfigs

Question:
- Pods are Pending but the cluster doesn't scale up. Explain why and how you'd debug.

Answer:
- Explanation: Cluster Autoscaler scales based on unschedulable pods. Constraints like node affinity, taints, or insufficient node group capacity can block scale-up. Check autoscaler logs and pod scheduling events.
- Why this matters in production: Scaling failures lead to outages during load spikes.

Solution:
- kubectl commands:
  - `kubectl describe pod <pending>`
  - `kubectl -n kube-system logs deploy/cluster-autoscaler`
- Config snippet:
```yaml
--balance-similar-node-groups=true
--expander=least-waste
```

Edge Cases & Tradeoffs:
- Pod affinity requires specific labels not in node groups
- Taints require tolerations; autoscaler won't add nodes for unschedulable due to taints
- PVC zone constraints may block scale-up in a zone
- DaemonSet overhead can make nodes appear full
- Max node group size reached
- Scale-up delay due to cloud API limits
- Spot instance availability failures
- PDBs can prevent scale-down, not scale-up
- Overprovisioning pods can trigger premature scale-up
- Priority class can affect preemption not scaling
- GPU requests require GPU node group
- Custom scheduler can bypass autoscaler detection

Red Flags (Bad Answers):
- "Autoscaler scales on CPU usage directly"
- "Any Pending pod triggers scale-up"
- "PDBs block scale-up"
--------------------------------------------------
Q31. ResourceQuotas and LimitRanges
Difficulty: Hard

What the interviewer is testing:
- Enforcing resource limits by namespace
- LimitRange default requests/limits
- Quota scopes
- Effects on scheduling and HPA
- Preventing noisy neighbors
- Interaction with PriorityClass
- Storage quota usage
- Quota for object counts
- Failure modes for missing requests
- Operational guardrails for teams
- Monitoring quota usage
- Tradeoffs in shared clusters

Question:
- A team repeatedly deploys pods without requests and exhausts node capacity. How do you prevent this?

Answer:
- Explanation: Use LimitRanges to set default requests/limits and ResourceQuotas to cap total usage. This enforces fairness and prevents BestEffort bursts.
- Why this matters in production: Unbounded resource use destabilizes clusters.

Solution:
- YAML manifests:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
  - type: Container
    default:
      cpu: "1"
      memory: "1Gi"
    defaultRequest:
      cpu: "200m"
      memory: "256Mi"
```
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    limits.cpu: "40"
    limits.memory: "80Gi"
```

Edge Cases & Tradeoffs:
- Quotas can block deployments unexpectedly
- Default requests may be too high for small apps
- HPA behavior depends on requests
- Storage quotas include PVC requests
- Quotas don't apply to node-level resources
- Object count quotas can block controllers
- Namespace migration requires quota adjustments
- LimitRange doesn't set pod-level requests if containers differ
- Large quotas can still allow noisy neighbors
- Quota usage updates may lag
- Different teams need different profiles
- Misconfigured quotas lead to Pending pods

Red Flags (Bad Answers):
- "Quotas are optional in shared clusters"
- "LimitRanges only apply to CPU"
- "Quotas affect only running pods"
--------------------------------------------------
Q32. PV/PVC Binding and Reclaim Policies
Difficulty: Hard

What the interviewer is testing:
- Binding workflow
- Immediate vs WaitForFirstConsumer
- Reclaim policies (Delete/Retain)
- StorageClass defaulting
- PVC resizing requirements
- Access modes limitations
- Zone constraints
- Finalizers on PVs
- Cleanup responsibilities
- StorageClass parameters
- Failure modes for Pending PVC
- Data retention risks

Question:
- A PVC is stuck in Pending. Explain the binding flow and how to fix it without data loss.

Answer:
- Explanation: PVC binds to a PV that matches size, access modes, and StorageClass. In dynamic provisioning, StorageClass provisions PV. WaitForFirstConsumer defers until scheduling. Fix by matching class, size, and zone.
- Why this matters in production: Storage misconfiguration blocks workloads or causes data loss.

Solution:
- kubectl commands:
  - `kubectl describe pvc data`
  - `kubectl get storageclass`
- YAML manifests:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: csi.example.com
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain
```

Edge Cases & Tradeoffs:
- Wrong StorageClass name keeps PVC Pending
- AccessModes not supported by provisioner
- PVC size larger than available storage
- WaitForFirstConsumer requires scheduler decision
- Zone constraints can block scheduling
- Retain policy leaves PVs orphaned
- Delete policy can remove data unexpectedly
- PV finalizers can block deletion
- Resize requires allowVolumeExpansion
- In-use PVC expansion requires filesystem support
- Binding can be to undesired PV if selectors are wrong
- Manual PV creation requires correct labels

Red Flags (Bad Answers):
- "PVC always auto-provisions storage"
- "Reclaim policy doesn't matter"
- "Pending PVC means storage is full only"
--------------------------------------------------
Q33. CSI Snapshots and Expansion
Difficulty: Hard

What the interviewer is testing:
- CSI snapshot architecture
- VolumeSnapshot resources
- Driver support requirements
- Expansion workflows
- Online vs offline expansion
- Snapshot consistency concerns
- Backup vs snapshot differences
- Restore patterns
- Permission and RBAC for snapshots
- Failure handling in snapshot creation
- Impact on StatefulSets
- Limitations for RWX volumes

Question:
- You need a backup and restore strategy for stateful workloads using CSI. Explain how snapshots and expansion work and their caveats.

Answer:
- Explanation: CSI snapshots use VolumeSnapshot/VolumeSnapshotContent and require a snapshot controller and driver support. Expansion depends on StorageClass and filesystem support. Snapshots are point-in-time, not a full backup strategy.
- Why this matters in production: Incorrect snapshot use can lead to inconsistent backups.

Solution:
- YAML manifests:
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: db-snap
spec:
  volumeSnapshotClassName: fast-snap
  source:
    persistentVolumeClaimName: data-db-0
```

Edge Cases & Tradeoffs:
- Snapshot controller not installed
- Driver doesn't support snapshots
- App-level consistency not guaranteed without quiesce
- Snapshots can consume storage space
- Restore requires new PVC from snapshot
- Expansion may require pod restart
- RWX snapshots may not be supported
- Snapshot creation can be slow for large volumes
- Deleting snapshot might not delete underlying data
- Snapshot class misconfiguration blocks creation
- RBAC can prevent snapshot operations
- Backups still needed for DR and corruption recovery

Red Flags (Bad Answers):
- "Snapshots replace backups"
- "All CSI drivers support snapshots"
- "Expansion is always online"
--------------------------------------------------
Q34. Pod Security Standards and Admission Control
Difficulty: Hard

What the interviewer is testing:
- Baseline vs Restricted policies
- Namespace-level enforcement
- Pod security labels
- Common violations (privileged, hostPath, runAsRoot)
- Migration strategies
- Admission controller failure modes
- Audit vs warn modes
- Workload exceptions
- Security vs usability tradeoffs
- Impact on system workloads
- Debugging admission rejections
- Policy versioning

Question:
- You need to enforce restricted Pod Security Standards without breaking existing workloads. How do you roll it out safely?

Answer:
- Explanation: Start with `audit`/`warn` modes to identify violations, fix workloads, then enforce. Use namespace labels to apply policies gradually.
- Why this matters in production: Sudden enforcement can block critical deployments.

Solution:
- YAML manifests:
```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: "restricted"
    pod-security.kubernetes.io/enforce-version: "v1.27"
    pod-security.kubernetes.io/audit: "restricted"
    pod-security.kubernetes.io/warn: "restricted"
```

Edge Cases & Tradeoffs:
- System namespaces may need exemptions
- Restricted blocks privileged and hostPath
- Image builds may require root, causing violations
- Existing pods are not evicted by default
- Audit logs can be noisy at scale
- Version drift across clusters can cause confusion
- Admission webhook failures can block all pods
- Mutating webhooks can conflict with policies
- DaemonSets may need elevated privileges
- PodSecurity admission is namespace-scoped
- Enforcement can break debugging workflows
- Legacy workloads may need redesign

Red Flags (Bad Answers):
- "Enable enforce everywhere immediately"
- "Pod Security Standards replace RBAC"
- "Restricted still allows hostPath"
--------------------------------------------------
Q35. RBAC: Roles, ClusterRoles, and Aggregation
Difficulty: Hard

What the interviewer is testing:
- Verbs, resources, and API groups
- Role vs ClusterRole scope
- RoleBinding vs ClusterRoleBinding
- Aggregated ClusterRoles
- Least privilege design
- ServiceAccount binding patterns
- Common RBAC debugging steps
- Impersonation for testing
- Permissions for CRDs
- Risks of wildcard permissions
- System roles and escalation
- Failure modes for controllers

Question:
- A controller can't list Pods in all namespaces. Diagnose and fix with least privilege.

Answer:
- Explanation: Listing across namespaces requires ClusterRole and ClusterRoleBinding. Use aggregation or custom roles with `get/list/watch` on pods.
- Why this matters in production: Overprivileged controllers are security risks; underprivileged controllers fail silently.

Solution:
- YAML manifests:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get","list","watch"]
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: pod-reader-binding
subjects:
- kind: ServiceAccount
  name: controller
  namespace: ops
roleRef:
  kind: ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```
- kubectl commands:
  - `kubectl auth can-i list pods --as=system:serviceaccount:ops:controller --all-namespaces`

Edge Cases & Tradeoffs:
- RoleBinding to ClusterRole still namespace-scoped
- Wildcards can grant too much access
- Aggregation labels must match correctly
- CRD permissions require API group name
- Controllers often need watch, not just list
- Impersonation requires special permissions
- RBAC cache delay can mask changes
- Deleting a RoleBinding breaks controller silently
- ClusterRoleBinding affects all namespaces
- Namespaced roles can't list cluster resources
- Using `*` verbs is risky for production
- ServiceAccount token leakage elevates risk

Red Flags (Bad Answers):
- "Use cluster-admin for controllers"
- "RoleBinding gives cluster-wide access"
- "RBAC errors always surface in events"
--------------------------------------------------
Q36. etcd Performance, Backup, and Restore
Difficulty: Very Hard

What the interviewer is testing:
- etcd's role and impact on control plane
- Performance bottlenecks (disk latency)
- Backup/restore strategy
- Consistency requirements
- Defragmentation
- Quorum and member health
- Snapshots vs live data
- Impact of large object counts
- API server timeouts due to etcd
- Disaster recovery planning
- Security of etcd data
- Operational indicators of etcd trouble

Question:
- Your API server is slow; etcd disk latency is high. Explain symptoms, mitigation, and backup/restore approach.

Answer:
- Explanation: etcd is the source of truth; high disk latency causes API server timeouts and controller lag. Use SSDs, monitor latency, and take regular snapshots. Restore requires stopping API server and restoring consistent snapshot.
- Why this matters in production: etcd issues can render the whole cluster unusable.

Solution:
- Config snippet:
```yaml
# etcd static pod args (example)
- --snapshot-count=10000
- --metrics=extensive
```
- kubectl commands:
  - `kubectl -n kube-system get pods -l component=etcd`

Edge Cases & Tradeoffs:
- Snapshot must be taken from a healthy member
- Restore requires correct cluster ID and peer URLs
- Defrag can temporarily increase latency
- Large CRDs increase etcd size and latency
- Frequent writes (events) can churn etcd
- Disk full leads to read-only behavior
- Clock skew can destabilize quorum
- Compaction misconfig can cause data loss
- API server timeouts may appear as 5xx
- Restore in HA clusters requires careful rejoin
- etcd encryption keys must be available
- Backup schedule must align with RPO

Red Flags (Bad Answers):
- "etcd can be restored without stopping API server"
- "etcd performance doesn't affect API server"
- "Backups are optional because etcd is replicated"
--------------------------------------------------
Q37. API Server Authn/Authz and Admission Chain
Difficulty: Very Hard

What the interviewer is testing:
- Request flow through API server
- Authentication methods
- Authorization (RBAC, ABAC)
- Admission controllers order
- Mutating vs validating behavior
- Webhook timeouts and failures
- Side effects of admission on latency
- Audit logging placement
- Failure policies
- Common misconfigurations
- Security boundaries in multi-tenant clusters
- Debugging forbidden vs rejected errors

Question:
- A deployment is rejected with a validation error from a webhook. Explain the full API server flow and how to troubleshoot.

Answer:
- Explanation: Requests go through authentication, authorization, then admission (mutating and validating). Webhooks can deny or mutate. Check webhook configs, timeout, and failurePolicy.
- Why this matters in production: Admission outages can block all deployments.

Solution:
- kubectl commands:
  - `kubectl get validatingwebhookconfiguration`
  - `kubectl describe validatingwebhookconfiguration <name>`
  - `kubectl logs -n <ns> deploy/<webhook>`
- Config snippet:
```yaml
failurePolicy: Fail
timeoutSeconds: 5
```

Edge Cases & Tradeoffs:
- failurePolicy Fail can block cluster-wide writes
- Mutating webhook order affects final object
- Timeout too low causes flaky failures
- Webhook TLS issues cause rejections
- Namespace selector mismatch skips enforcement
- SideEffects field affects dry-run operations
- API server retries can double-call webhooks
- Large objects may exceed webhook limits
- Admission latency increases API server response time
- Webhook unavailability during upgrade causes outages
- Validating webhook cannot mutate
- Audit logs may not include full webhook context

Red Flags (Bad Answers):
- "Admission happens before authz"
- "Webhooks can't block writes"
- "failurePolicy doesn't matter"
--------------------------------------------------
Q38. Kubelet Responsibilities and Node Status
Difficulty: Very Hard

What the interviewer is testing:
- Kubelet node status updates
- Pod lifecycle management
- CRI interactions
- Static pods handling
- Eviction management
- Health checks for containers
- Node condition updates
- Lease vs status
- TLS bootstrap and certificates
- Failure behavior when kubelet down
- NodeNotReady and taints
- Debugging node-level issues

Question:
- A node shows Ready but pods are not starting. Explain kubelet responsibilities and how to diagnose.

Answer:
- Explanation: Kubelet starts pods via CRI, reports node status, and runs probes. Node Ready can be stale if status updates are delayed. Check kubelet logs, container runtime health, and node conditions.
- Why this matters in production: Node-level issues can silently block workloads.

Solution:
- kubectl commands:
  - `kubectl describe node <node>`
  - `kubectl get pods -o wide --field-selector spec.nodeName=<node>`

Edge Cases & Tradeoffs:
- Node lease updates can mask status issues
- Container runtime down causes pods stuck in ContainerCreating
- Disk pressure triggers eviction and NotReady
- Clock skew affects node heartbeats
- Static pods may run even if API server is down
- Kubelet certificate expiration blocks API server auth
- Node taints can prevent scheduling
- CNI plugin failure blocks pod networking
- Image pulls can hang due to registry issues
- Kubelet logs may be on node only
- Node Ready doesn't guarantee kube-proxy health
- Misconfigured cgroups can break resource enforcement

Red Flags (Bad Answers):
- "Scheduler starts pods on nodes"
- "Node Ready means everything is healthy"
- "Kubelet doesn't manage probes"
--------------------------------------------------
Q39. HA Control Plane and API Server Load Balancing
Difficulty: Very Hard

What the interviewer is testing:
- Multi-control-plane architecture
- API server load balancer requirements
- etcd quorum design
- Failure domains
- Certificate distribution
- Kubeconfig server endpoints
- Control-plane upgrade sequencing
- Static pod bootstrapping
- Resiliency to node failures
- Latency impacts
- Disaster recovery assumptions
- Operational pitfalls

Question:
- You need a highly available control plane. Describe the design and operational considerations.

Answer:
- Explanation: Use multiple control-plane nodes with etcd quorum, fronted by a load balancer for the API server. Keep versions in sync and manage cert rotation.
- Why this matters in production: Control plane outages impact scheduling, scaling, and cluster operations.

Solution:
- Config snippet:
```yaml
clusters:
- cluster:
    server: https://api.example.com:6443
```

Edge Cases & Tradeoffs:
- etcd requires odd-number quorum
- Load balancer health checks must hit /healthz
- Split-brain possible if etcd network partitions
- Cert rotation must cover all control-plane nodes
- Control-plane nodes need dedicated resources
- API server overload can cause throttling
- kubelet bootstrap tokens must be secured
- Static pod manifests require consistent config
- etcd backup restore in HA needs careful sequencing
- Time sync across control-plane nodes is critical
- Upgrades must follow version skew rules
- External LB must handle TLS passthrough or termination

Red Flags (Bad Answers):
- "Two control-plane nodes are enough"
- "etcd can be single-node in HA"
- "Load balancer is optional for HA"
--------------------------------------------------
Q40. Version Skew and Upgrade Order
Difficulty: Very Hard

What the interviewer is testing:
- Version skew rules
- Safe upgrade order
- kubelet vs API server compatibility
- Add-on upgrades (CNI, CoreDNS)
- Draining strategy
- Handling deprecated APIs
- Rolling upgrade planning
- Monitoring during upgrades
- Rollback planning
- PodDisruptionBudget interactions
- Node pool upgrade strategies
- Risk of feature gate changes

Question:
- You need to upgrade a production cluster from 1.25 to 1.27. Outline a safe upgrade plan and failure points.

Answer:
- Explanation: Upgrade control plane first, then nodes, respecting skew (kubelet <=2 minor behind API server). Upgrade add-ons after control plane. Drain nodes with PDB awareness.
- Why this matters in production: Misordered upgrades can break the cluster.

Solution:
- kubectl commands:
  - `kubectl version --short`
  - `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`
- Config snippet:
```yaml
# Ensure deprecated APIs are migrated before upgrade
```

Edge Cases & Tradeoffs:
- Removed APIs break controllers
- CNI version may not support new Kubernetes
- CoreDNS version skew can break DNS
- PDBs can block draining
- Webhooks might be incompatible after upgrade
- Feature gate defaults can change behavior
- Rollback is not always possible for etcd
- CRDs may need conversion
- Node images may lack required kernel modules
- Upgrade windows must cover long drain times
- Workloads with disruption budgets may require scaling
- Monitoring must detect partial failures quickly

Red Flags (Bad Answers):
- "Upgrade all nodes first"
- "Version skew doesn't matter"
- "Add-ons can be upgraded anytime"
--------------------------------------------------
Q41. API Server Throttling and Client QPS
Difficulty: Very Hard

What the interviewer is testing:
- Client-side throttling behavior
- API server QPS limits
- Controller-runtime defaults
- Symptoms of throttling
- Impact on rollout speed
- Watch vs list efficiency
- Rate limiting headers
- Tuning kubeconfig QPS/Burst
- Effects on CI/CD pipelines
- Multi-tenant API usage
- Audit logging impacts
- Backoff strategies

Question:
- Your CI pipeline gets `Too Many Requests` and rollouts slow down under load. Explain why and how to mitigate.

Answer:
- Explanation: API server enforces QPS/burst limits; clients also throttle. Too many list/watch calls or high QPS triggers 429s. Tune client QPS/Burst and reduce poll loops.
- Why this matters in production: Excessive API calls degrade control plane performance.

Solution:
- Config snippet:
```yaml
# kubeconfig for client
QPS: 20
Burst: 40
```
- kubectl commands:
  - `kubectl get --raw /metrics | findstr apiserver_request_total`

Edge Cases & Tradeoffs:
- Increasing client QPS can overload API server
- List-heavy clients scale poorly
- Watch reconnect storms create bursts
- Audit logging increases API server CPU
- Custom controllers with low resync periods cause churn
- Aggregated APIs can add latency
- 429s can cause retries and amplify load
- kubectl polling loops are inefficient
- API server priority and fairness can limit requests
- Network latency can look like throttling
- Large objects increase bandwidth costs
- Client timeouts may hide throttling root cause

Red Flags (Bad Answers):
- "Just increase API server QPS limits"
- "429s are network errors"
- "Throttling only affects kubectl"
--------------------------------------------------
Q42. Scheduler Scale: Anti-Affinity Explosion
Difficulty: Very Hard

What the interviewer is testing:
- Scheduler performance bottlenecks
- Anti-affinity cost
- Topology spread constraints at scale
- Preemption cost
- Scoring plugin complexity
- Scheduler profiling
- Workload design for scale
- Reducing constraints
- Impact on pending time
- Cache efficiency
- Node labels cardinality
- Large-cluster best practices

Question:
- In a 5,000-node cluster, scheduling latency spikes. There's heavy pod anti-affinity. Explain why and how to mitigate.

Answer:
- Explanation: Required anti-affinity forces scheduler to evaluate many pods and nodes, leading to O(N^2) checks. Use preferred rules, reduce label selectors, or use topology spread instead.
- Why this matters in production: Scheduling delays slow rollouts and autoscaling.

Solution:
- YAML manifests:
```yaml
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
  - weight: 50
    podAffinityTerm:
      labelSelector:
        matchLabels:
          app: api
      topologyKey: kubernetes.io/hostname
```

Edge Cases & Tradeoffs:
- Required anti-affinity can deadlock scheduling
- High label cardinality slows scheduler cache
- Spread constraints can also be expensive
- Preemption evaluation increases scheduling time
- Multiple scheduler profiles add overhead
- Node affinity with many terms increases filter cost
- Large namespace counts increase object watches
- Cluster autoscaler may lag due to pending pods
- Scheduler cache staleness can create retries
- Overly strict constraints reduce bin packing
- Scheduler logs can be too verbose at scale
- CNI bandwidth can also be bottleneck, not scheduler

Red Flags (Bad Answers):
- "Anti-affinity has no performance cost"
- "More scheduler replicas always fix latency"
- "Use required anti-affinity for all workloads"
--------------------------------------------------
Q43. Service Resolves but Can't Connect
Difficulty: Very Hard

What the interviewer is testing:
- DNS vs connectivity troubleshooting
- Service endpoints inspection
- NetworkPolicy effects
- kube-proxy vs CNI issues
- Pod readiness and endpoints
- Port mismatch issues
- Node-level firewall/NAT
- MTU problems
- Hairpin traffic
- TLS mismatches
- Debugging with exec and nettools
- Hypothesis-driven troubleshooting

Question:
- A pod can resolve `api.default.svc` but cannot connect. Walk through your debugging process and possible causes.

Answer:
- Explanation: DNS resolution only confirms Service existence. Check endpoints, readiness, Service port mapping, NetworkPolicies, and node-level routing.
- Why this matters in production: DNS success is often misinterpreted as full connectivity.

Solution:
- kubectl commands:
  - `kubectl get svc api -o yaml`
  - `kubectl get endpoints api`
  - `kubectl exec -it <pod> -- sh -c "nc -zv api 80"`
- Config snippet:
```yaml
ports:
- port: 80
  targetPort: 8080
```

Edge Cases & Tradeoffs:
- Endpoints empty due to readiness failure
- targetPort mismatch sends to wrong port
- NetworkPolicy blocks egress or ingress
- kube-proxy rules stale or missing
- CNI misroutes pod traffic
- MTU mismatch drops packets silently
- Hairpin mode disabled for same-node access
- TLS required on backend but client uses HTTP
- Service selector mismatch
- Pod IP reachable but Service IP not
- ExternalTrafficPolicy Local impacts routing
- CoreDNS caches stale records

Red Flags (Bad Answers):
- "DNS resolution means service is up"
- "It's always a network issue"
- "Just restart CoreDNS"
--------------------------------------------------
Q44. Rollout Stuck: PDB, Probes, and Capacity
Difficulty: Very Hard

What the interviewer is testing:
- Rollout progress conditions
- PDB interactions
- maxUnavailable/maxSurge behavior
- Capacity constraints
- Readiness probe failures
- Image pull errors
- Observability and event analysis
- Deployment controller behavior
- Rollback strategy
- HPA interactions
- Taint/affinity scheduling failures
- Diagnosing at scale

Question:
- A deployment rollout is stuck for 30 minutes. You see some pods Pending and some not Ready. Diagnose root causes and remediation.

Answer:
- Explanation: Check events: Pending may be due to insufficient resources, taints, affinity, or PVC binding. Not Ready indicates probes or dependencies failing. PDB can block eviction of old pods.
- Why this matters in production: Stuck rollouts cause partial outages and delayed fixes.

Solution:
- kubectl commands:
  - `kubectl rollout status deploy/api`
  - `kubectl describe deploy/api`
  - `kubectl describe pod <pod>`
  - `kubectl get events --sort-by=.lastTimestamp`

Edge Cases & Tradeoffs:
- maxUnavailable 0 with no surge capacity blocks rollout
- PDB minAvailable too strict
- Readiness probe tied to external dependency
- ImagePullBackOff slows rollout
- Resource requests exceed node capacity
- Taints without tolerations block new pods
- PVC Pending in WaitForFirstConsumer
- HPA scaling up/down during rollout adds churn
- ProgressDeadlineSeconds triggers rollback
- nodeSelector excludes all nodes
- Cluster autoscaler not scaling due to constraints
- Deployment paused accidentally

Red Flags (Bad Answers):
- "Rollouts always complete eventually"
- "Pending pods mean image issue"
- "Just force delete old pods"
--------------------------------------------------
Q45. NetworkPolicy Broke DNS at Scale
Difficulty: Very Hard

What the interviewer is testing:
- DNS dependency awareness
- egress policy requirements
- CoreDNS IPs vs labels
- Namespace selectors
- NodeLocal DNSCache behavior
- UDP/TCP for DNS
- Multiple DNS domains
- Debugging denied traffic
- CNI-specific nuances
- Logging and observability
- Repair strategy without removing policy
- Testing with debug pods

Question:
- After enabling strict egress policies, multiple services fail due to DNS resolution issues. How do you fix without disabling policies?

Answer:
- Explanation: Add explicit egress rules to CoreDNS pods or NodeLocal DNSCache, allow UDP/TCP 53, and ensure namespace selectors match labels. Validate with debug pods.
- Why this matters in production: DNS is a dependency for service discovery and external access.

Solution:
- YAML manifests:
```yaml
egress:
- to:
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: kube-system
    podSelector:
      matchLabels:
        k8s-app: kube-dns
  ports:
  - protocol: UDP
    port: 53
  - protocol: TCP
    port: 53
```
- kubectl commands:
  - `kubectl exec -it <pod> -- nslookup kubernetes.default`

Edge Cases & Tradeoffs:
- NodeLocal DNSCache runs as DaemonSet with different labels
- CNI might require policy for kube-dns Service IP
- Some apps use TCP-only DNS
- Split-horizon domains require extra egress
- Policies are namespace-scoped; missing for new namespaces
- FQDN policies not supported in all CNIs
- DNS over TLS/HTTPS uses different ports
- CoreDNS scaling issues can look like policy failures
- Large policies can slow CNI enforcement
- Egress to external resolvers may be required
- Debug pods may need elevated privileges
- Policies may not apply to hostNetwork pods

Red Flags (Bad Answers):
- "Just disable NetworkPolicies"
- "Allow all egress to fix DNS"
- "DNS uses port 80"
--------------------------------------------------
Q46. Admission Webhook Outage Blocks All Pods
Difficulty: Very Hard

What the interviewer is testing:
- Admission webhook dependencies
- FailurePolicy implications
- Timeout handling
- Recovery plan during outage
- High availability for webhooks
- Impact on cluster-wide operations
- Safe bypass strategies
- Auditing and observability
- Distinguishing webhook vs API server issues
- Mutating vs validating failure modes
- Feature gate considerations
- Communication during incident

Question:
- A validating webhook is down and new pods can't be created. How do you recover quickly and safely?

Answer:
- Explanation: If failurePolicy is Fail, API server rejects requests when webhook is unreachable. Patch webhook to failurePolicy: Ignore or remove it temporarily, then restore after fixing. Ensure HA for webhook service.
- Why this matters in production: Admission outages can halt all deployments.

Solution:
- kubectl commands:
  - `kubectl patch validatingwebhookconfiguration <name> --type=json -p='[{"op":"replace","path":"/webhooks/0/failurePolicy","value":"Ignore"}]'`
- YAML manifests:
```yaml
failurePolicy: Ignore
timeoutSeconds: 2
```

Edge Cases & Tradeoffs:
- Ignoring validation can allow unsafe objects
- Patching webhooks requires appropriate RBAC
- API server cache may take time to update
- Multiple webhooks can still block requests
- Mutating webhooks might be required for security defaults
- Webhook service DNS issues can mimic outage
- mTLS cert expiration causes failures
- NamespaceSelector can limit blast radius
- SideEffects affect dry-run and apply
- Retry storms can overload API server
- Logging may be missing for failed webhook calls
- Permanent ignore weakens compliance

Red Flags (Bad Answers):
- "Restart API server to fix"
- "Webhooks can't block creates"
- "Disable all admission permanently"
--------------------------------------------------
Q47. Node Pressure Evictions and Disk/Memory Thresholds
Difficulty: Very Hard

What the interviewer is testing:
- Eviction thresholds configuration
- Disk pressure and inode exhaustion
- Memory pressure behavior
- Eviction ordering
- Impact on critical workloads
- Monitoring node pressure signals
- Tuning kubelet eviction settings
- Handling emptyDir usage
- Image garbage collection
- Graceful degradation strategies
- PDB impact on involuntary evictions
- Recovery steps

Question:
- You see frequent evictions due to disk pressure, even though pods seem small. Explain causes and fixes.

Answer:
- Explanation: Disk pressure can be from container logs, image layers, emptyDir, or inode exhaustion. Tune eviction thresholds, manage log rotation, and size node disks appropriately.
- Why this matters in production: Evictions cause cascading failures and reduce capacity.

Solution:
- Config snippet:
```yaml
evictionHard:
  nodefs.available: "10%"
  imagefs.available: "15%"
```
- kubectl commands:
  - `kubectl describe node <node> | findstr -i Pressure`

Edge Cases & Tradeoffs:
- EmptyDir counts against node disk
- Container logs can grow unbounded
- Image garbage collection may lag
- Inode exhaustion can trigger disk pressure
- Separate imagefs vs nodefs changes eviction behavior
- Evictions may ignore PDB in pressure situations
- Disk pressure can mark node NotReady
- HostPath usage can mask disk usage
- NodeLocal DNSCache can use disk
- Larger images increase pull time and disk use
- DaemonSets may be evicted too
- Eviction thresholds too high cause premature evictions

Red Flags (Bad Answers):
- "Disk pressure only from PVCs"
- "Evictions respect PDBs always"
- "Increase eviction thresholds to stop evictions"
--------------------------------------------------
Q48. Service Mesh vs East-West Traffic
Difficulty: Very Hard

What the interviewer is testing:
- North-south vs east-west traffic distinction
- When to use service mesh
- Sidecar overhead and cost
- mTLS implications
- Traffic policy and retries
- Failure modes (policy misconfig)
- Observability benefits vs overhead
- Impact on startup time
- Resource requests for proxies
- Mesh and NetworkPolicy interaction
- Gateway integration
- Gradual adoption strategies

Question:
- Your org is considering a service mesh to secure east-west traffic. When is it appropriate, and what are the tradeoffs?

Answer:
- Explanation: A mesh provides mTLS, traffic policies, and observability for service-to-service traffic. It adds latency, resource overhead, and operational complexity. Use if you need uniform security and traffic control.
- Why this matters in production: Mesh adoption can improve security but also introduce new failure modes.

Solution:
- Config snippet:
```yaml
# Example sidecar injection label
metadata:
  labels:
    istio-injection: enabled
```
- kubectl commands:
  - `kubectl get pods -l istio.io/rev`

Edge Cases & Tradeoffs:
- Sidecar adds CPU/memory overhead
- Startup time increases with init containers
- Misconfigured retries can amplify load
- mTLS can break non-mesh services
- Debugging becomes more complex
- Traffic policies can cause cascading failures
- Proxy crashes can break connectivity
- Mesh upgrades need careful coordination
- NetworkPolicy may need updates for proxy ports
- Multi-cluster meshes add complexity
- Observability data volume can be large
- Legacy protocols may not be fully supported

Red Flags (Bad Answers):
- "Mesh is always better for every cluster"
- "Mesh has no performance overhead"
- "mTLS works without config changes"
--------------------------------------------------
Q49. DR and Multi-Region Strategy
Difficulty: Very Hard

What the interviewer is testing:
- Backup/restore planning
- Multi-region architecture options
- Active-active vs active-passive
- Data consistency challenges
- DNS failover patterns
- RPO/RTO tradeoffs
- Dependency mapping
- Stateful workload recovery pitfalls
- etcd backup locality
- Storage replication limitations
- Testing DR plans
- Operational runbooks

Question:
- Design a DR strategy for a Kubernetes platform running stateful services. Include RPO/RTO tradeoffs and operational steps.

Answer:
- Explanation: Use regular etcd backups, application-level backups, and replicated storage where possible. Decide between active-passive (simpler) and active-active (complex). Test failover with runbooks.
- Why this matters in production: Without tested DR, outages become catastrophic.

Solution:
- Config snippet:
```yaml
# Example: schedule backups via CronJob to remote storage
```
- kubectl commands:
  - `kubectl get pv,pvc -A`

Edge Cases & Tradeoffs:
- etcd backups alone don't restore external storage
- Storage replication may not be consistent
- DNS failover can be slow due to TTLs
- Active-active requires conflict resolution
- Network partitions can cause split-brain
- Backups must include CRDs and resources
- Secrets and certs must be restored securely
- Time sync across regions is critical
- DR tests can be disruptive and need staging
- Restore order matters for controllers and CRDs
- Cloud provider dependencies differ by region
- Cost of hot standby can be significant

Red Flags (Bad Answers):
- "DR is just restoring etcd"
- "Active-active is always better"
- "No need to test DR"
--------------------------------------------------
Q50. Large-Cluster Best Practices and Object Churn
Difficulty: Very Hard

What the interviewer is testing:
- Control plane scaling limits
- Object churn impact (events, pods)
- Namespace and label discipline
- Controller behavior under load
- API server watch/list pressure
- etcd size management
- Resource fragmentation strategies
- Multi-tenant isolation
- Rate limiting controllers
- Use of sharding for workloads
- Observability at scale
- Operational guardrails

Question:
- You're scaling to 10k nodes. What practices prevent control-plane overload and keep operations stable?

Answer:
- Explanation: Reduce object churn, optimize controllers, enforce quotas, and keep labels consistent. Use EndpointSlices, limit event spam, and monitor API server QPS and etcd size.
- Why this matters in production: At scale, small inefficiencies become outages.

Solution:
- Config snippet:
```yaml
# Example: limit event TTL or reduce event spam via controllers
```
- kubectl commands:
  - `kubectl get --raw /metrics | findstr apiserver`
  - `kubectl get events --all-namespaces`

Edge Cases & Tradeoffs:
- Too many namespaces increase watch overhead
- High churn workloads cause API server load spikes
- Event spam fills etcd and slows control plane
- Excessive labels increase memory and watch payload
- Large EndpointSlices still cause kube-proxy churn
- Controllers with short resync periods overload API
- Overly strict constraints slow scheduling
- Fragmentation leads to poor bin packing
- Autoscaler thrash can destabilize nodes
- CRD misuse can balloon etcd size
- Audit logging at high verbosity is expensive
- Observability pipelines must scale with cluster size

Red Flags (Bad Answers):
- "Scale issues are only about node count"
- "Just increase API server resources"
- "Labels don't affect scale"
