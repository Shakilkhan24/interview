# 30 Advanced Kubernetes Interview Questions & Solutions
## Medium to Senior Level

---

## 1. Explain Pod Disruption Budgets (PDB) and implement one for a critical application

**Question:** You have a critical application running with 10 replicas. How would you ensure that at least 7 pods are always available during voluntary disruptions (node drains, cluster upgrades)?

**Solution:**

Pod Disruption Budgets ensure availability during voluntary disruptions. Here's the implementation:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: critical-app-pdb
  namespace: production
spec:
  minAvailable: 7
  selector:
    matchLabels:
      app: critical-app
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-app
  namespace: production
spec:
  replicas: 10
  selector:
    matchLabels:
      app: critical-app
  template:
    metadata:
      labels:
        app: critical-app
    spec:
      containers:
      - name: app
        image: nginx:1.21
```

**Key Points:**
- `minAvailable: 7` ensures at least 7 pods are running
- Alternative: use `maxUnavailable: 3` (equivalent)
- PDB only affects voluntary disruptions (not node failures)
- Works with Deployments, StatefulSets, ReplicaSets

**Verification:**
```bash
kubectl get pdb critical-app-pdb -n production
kubectl describe pdb critical-app-pdb -n production
```

---

## 2. Implement Network Policies to restrict traffic between namespaces

**Question:** Create a NetworkPolicy that allows pods in namespace `frontend` to communicate only with pods in namespace `backend` on port 8080, and deny all other traffic.

**Solution:**

```yaml
# NetworkPolicy for frontend namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: frontend
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: backend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: backend
    ports:
    - protocol: TCP
      port: 8080
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53  # DNS
---
# Label the backend namespace
apiVersion: v1
kind: Namespace
metadata:
  name: backend
  labels:
    name: backend
```

**Key Points:**
- Network policies are namespace-scoped
- Default deny-all if no policy matches
- Must explicitly allow DNS (port 53 UDP)
- Requires CNI plugin with NetworkPolicy support (Calico, Cilium, etc.)

**Verification:**
```bash
kubectl get networkpolicy -n frontend
kubectl label namespace backend name=backend
kubectl run test-pod --image=busybox -n frontend --rm -it -- sh
# Inside pod: wget -O- backend-service.backend.svc.cluster.local:8080
```

---

## 3. Configure Resource Quotas and Limit Ranges

**Question:** Set up a namespace with:
- Maximum 4 CPUs and 8Gi memory total
- Each pod can request max 2 CPUs and 4Gi memory
- Each container defaults to 100m CPU and 128Mi memory if not specified

**Solution:**

```yaml
# ResourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "4"
    limits.memory: 8Gi
    pods: "10"
---
# LimitRange
apiVersion: v1
kind: LimitRange
metadata:
  name: compute-limits
  namespace: dev
spec:
  limits:
  - max:
      cpu: "2"
      memory: 4Gi
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Pod
  - default:
      cpu: "100m"
      memory: "128Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

**Key Points:**
- ResourceQuota enforces namespace-level limits
- LimitRange sets defaults and constraints per pod/container
- Requests are used for scheduling decisions
- Limits prevent resource exhaustion

**Verification:**
```bash
kubectl describe quota compute-quota -n dev
kubectl describe limitrange compute-limits -n dev
kubectl get pods -n dev -o jsonpath='{.items[*].spec.containers[*].resources}'
```

---

## 4. Implement Advanced Pod Scheduling with Affinity/Anti-Affinity

**Question:** Schedule pods so that:
- Pods with label `app=web` prefer nodes with label `node-type=web`
- Pods with label `app=web` must not be on the same node as pods with `app=database`
- Ensure pods are spread across zones

**Solution:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      affinity:
        # Node affinity - prefer web nodes
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: node-type
                operator: In
                values:
                - web
        # Pod anti-affinity - avoid database pods
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - database
            topologyKey: kubernetes.io/hostname
        # Pod affinity - spread across zones
        podAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web
              topologyKey: topology.kubernetes.io/zone
      containers:
      - name: web
        image: nginx:1.21
```

**Key Points:**
- `requiredDuringScheduling` = hard requirement (must)
- `preferredDuringScheduling` = soft requirement (should)
- `topologyKey` defines the domain (hostname, zone, region)
- Anti-affinity prevents co-location, affinity encourages it

**Verification:**
```bash
kubectl get pods -o wide
kubectl describe node <node-name> | grep Labels
kubectl get nodes --show-labels
```

---

## 5. Create a Custom Resource Definition (CRD) and Controller

**Question:** Create a CRD for `DatabaseBackup` that schedules database backups, and a simple controller that creates a Job when a DatabaseBackup is created.

**Solution:**

```yaml
# CRD Definition
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databasebackups.stable.example.com
spec:
  group: stable.example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              database:
                type: string
              schedule:
                type: string
              retention:
                type: integer
          status:
            type: object
            properties:
              lastBackup:
                type: string
              status:
                type: string
  scope: Namespaced
  names:
    plural: databasebackups
    singular: databasebackup
    kind: DatabaseBackup
    shortNames:
    - dbb
---
# Example DatabaseBackup resource
apiVersion: stable.example.com/v1
kind: DatabaseBackup
metadata:
  name: mysql-backup
  namespace: production
spec:
  database: mysql-prod
  schedule: "0 2 * * *"  # Cron format
  retention: 7
status:
  lastBackup: "2024-01-15T02:00:00Z"
  status: "Success"
```

**Simple Controller (Python example):**

```python
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import yaml

config.load_incluster_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()
custom_api = client.CustomObjectsApi()

def create_backup_job(backup_name, database):
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {
            "name": f"backup-{backup_name}",
            "namespace": "production"
        },
        "spec": {
            "template": {
                "spec": {
                    "containers": [{
                        "name": "backup",
                        "image": "backup-tool:latest",
                        "command": ["/bin/sh", "-c", f"backup {database}"]
                    }],
                    "restartPolicy": "Never"
                }
            }
        }
    }
    batch_v1.create_namespaced_job("production", job_manifest)

def watch_backups():
    w = watch.Watch()
    for event in w.stream(custom_api.list_namespaced_custom_object,
                         "stable.example.com", "v1", "production", "databasebackups"):
        obj = event['object']
        if event['type'] == 'ADDED':
            create_backup_job(obj['metadata']['name'], 
                            obj['spec']['database'])

if __name__ == "__main__":
    watch_backups()
```

**Key Points:**
- CRDs extend Kubernetes API
- Controllers watch CRDs and reconcile desired state
- Use Operator SDK or Kubebuilder for production controllers
- CRDs enable domain-specific abstractions

**Verification:**
```bash
kubectl get crd databasebackups.stable.example.com
kubectl get databasebackups
kubectl describe databasebackup mysql-backup
```

---

## 6. Implement Taints and Tolerations for Dedicated Nodes

**Question:** Configure a node to only accept pods with a specific toleration, and create a deployment that can run on that node.

**Solution:**

```bash
# Taint the node
kubectl taint nodes node-1 dedicated=gpu:NoSchedule

# Or using YAML
kubectl patch node node-1 -p '{"spec":{"taints":[{"effect":"NoSchedule","key":"dedicated","value":"gpu"}]}}'
```

```yaml
# Deployment with toleration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-workload
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpu-workload
  template:
    metadata:
      labels:
        app: gpu-workload
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
      containers:
      - name: gpu-app
        image: nvidia/cuda:11.0-base
        resources:
          limits:
            nvidia.com/gpu: 1
```

**Key Points:**
- Taint effects: `NoSchedule`, `PreferNoSchedule`, `NoExecute`
- Tolerations allow pods to be scheduled on tainted nodes
- Use with node affinity for precise control
- Common use cases: GPU nodes, dedicated workloads, maintenance

**Verification:**
```bash
kubectl describe node node-1 | grep Taints
kubectl get pods -o wide
kubectl get pods -o jsonpath='{.items[*].spec.tolerations}'
```

---

## 7. Configure Security Contexts and Pod Security Standards

**Question:** Create a pod that runs as non-root user (UID 1000), drops all capabilities except NET_BIND_SERVICE, and runs in read-only root filesystem.

**Solution:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 3000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: nginx:1.21
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: var-cache
      mountPath: /var/cache/nginx
  volumes:
  - name: tmp
    emptyDir: {}
  - name: var-cache
    emptyDir: {}
```

**Pod Security Standards (PSP replacement):**

```yaml
# Pod Security Policy via Namespace labels
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Key Points:**
- Security contexts enforce least privilege
- Read-only root filesystem prevents tampering
- Capabilities limit what containers can do
- Pod Security Standards replace deprecated PSP

**Verification:**
```bash
kubectl get pod secure-pod -o jsonpath='{.spec.securityContext}'
kubectl exec secure-pod -- id
kubectl exec secure-pod -- touch /test  # Should fail
```

---

## 8. Implement StatefulSet with Headless Service and Persistent Volumes

**Question:** Create a StatefulSet for a database with:
- 3 replicas with stable network identities
- Each pod gets its own PVC
- Ordered deployment and scaling

**Solution:**

```yaml
# Headless Service
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  clusterIP: None  # Headless
  selector:
    app: mysql
  ports:
  - port: 3306
    name: mysql
---
# StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql
  replicas: 3
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 20Gi
```

**Key Points:**
- StatefulSets provide stable network identities (mysql-0, mysql-1, mysql-2)
- Headless service enables direct pod access
- Each pod gets its own PVC from the template
- Ordered: create/delete sequentially (0, 1, 2)

**Verification:**
```bash
kubectl get statefulset mysql
kubectl get pods -l app=mysql
kubectl get pvc
kubectl run -it --rm debug --image=mysql:8.0 -- mysql -h mysql-1.mysql -u root -p
```

---

## 9. Configure RBAC with Service Accounts

**Question:** Create a ServiceAccount that can only list and get pods in a specific namespace, and use it in a deployment.

**Solution:**

```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-reader
  namespace: monitoring
---
# Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: monitoring
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: monitoring
subjects:
- kind: ServiceAccount
  name: pod-reader
  namespace: monitoring
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
---
# Deployment using the ServiceAccount
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-agent
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      serviceAccountName: pod-reader
      containers:
      - name: agent
        image: monitoring-agent:latest
```

**ClusterRole example (cross-namespace):**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-pod-reader-binding
subjects:
- kind: ServiceAccount
  name: pod-reader
  namespace: monitoring
roleRef:
  kind: ClusterRole
  name: cluster-pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Key Points:**
- Role = namespace-scoped, ClusterRole = cluster-scoped
- ServiceAccounts provide identity to pods
- RBAC follows principle of least privilege
- Verbs: get, list, create, update, patch, delete, watch

**Verification:**
```bash
kubectl auth can-i get pods --as=system:serviceaccount:monitoring:pod-reader -n monitoring
kubectl get sa pod-reader -n monitoring -o yaml
kubectl describe rolebinding pod-reader-binding -n monitoring
```

---

## 10. Implement Canary Deployment Strategy

**Question:** Implement a canary deployment that gradually shifts traffic from version 1 to version 2 of an application.

**Solution:**

```yaml
# Service
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
---
# Stable Deployment (v1)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v1
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: app
        image: myapp:v1
---
# Canary Deployment (v2)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      version: v2
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
      - name: app
        image: myapp:v2
```

**Using Istio VirtualService (advanced):**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-vs
spec:
  hosts:
  - app-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: app-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: app-service
        subset: v1
      weight: 90
    - destination:
        host: app-service
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: app-dr
spec:
  host: app-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

**Key Points:**
- Canary = gradual rollout with traffic splitting
- Monitor metrics before increasing canary percentage
- Easy rollback by scaling canary to 0
- Service mesh enables advanced traffic management

**Verification:**
```bash
kubectl get deployments
kubectl get pods -l app=myapp
kubectl scale deployment app-v2 --replicas=3  # Increase canary
```

---

## 11. Configure Horizontal Pod Autoscaler (HPA) with Custom Metrics

**Question:** Set up HPA that scales based on CPU and custom metrics (requests per second).

**Solution:**

```yaml
# HPA with CPU and custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

**Deployment with resource requests:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: app
        image: nginx:1.21
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

**Key Points:**
- HPA requires metrics-server for CPU/memory
- Custom metrics need Prometheus adapter or custom metrics API
- Behavior controls scaling speed and stabilization
- Always set resource requests for HPA to work

**Verification:**
```bash
kubectl get hpa app-hpa
kubectl describe hpa app-hpa
kubectl top pods
# Generate load: kubectl run -i --tty load-generator --rm --image=busybox -- sh
```

---

## 12. Implement Vertical Pod Autoscaler (VPA)

**Question:** Configure VPA to automatically adjust CPU and memory requests/limits based on historical usage.

**Solution:**

```yaml
# VPA
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  updatePolicy:
    updateMode: "Auto"  # Auto, Off, Initial, Recreate
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
```

**Key Points:**
- VPA recommends or automatically adjusts resources
- Update modes:
  - `Auto`: Updates pods automatically (may cause restarts)
  - `Recreate`: Recreates pods with new resources
  - `Initial`: Only sets resources at pod creation
  - `Off`: Only provides recommendations
- Requires VPA admission controller

**Verification:**
```bash
kubectl get vpa app-vpa
kubectl describe vpa app-vpa
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].resources}'
```

---

## 13. Configure Init Containers and Sidecar Pattern

**Question:** Create a pod with an init container that waits for a database to be ready, and a sidecar container that handles logging.

**Solution:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-init-sidecar
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.35
    command:
    - sh
    - -c
    - |
      until nc -z database-service 5432; do
        echo "Waiting for database..."
        sleep 2
      done
      echo "Database is ready!"
  containers:
  - name: app
    image: nginx:1.21
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/app
  - name: log-sidecar
    image: fluent/fluent-bit:latest
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/app
      readOnly: true
    - name: fluent-bit-config
      mountPath: /fluent-bit/etc/
  volumes:
  - name: shared-logs
    emptyDir: {}
  - name: fluent-bit-config
    configMap:
      name: fluent-bit-config
---
# Fluent Bit ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [INPUT]
        Name tail
        Path /var/log/app/*.log
        Multiline On
        Parser_Firstline multiline
    
    [OUTPUT]
        Name stdout
        Match *
```

**Key Points:**
- Init containers run sequentially before app containers
- Sidecars share volumes with main container
- Common sidecar use cases: logging, monitoring, proxies
- Init containers useful for setup, migrations, dependencies

**Verification:**
```bash
kubectl get pod app-with-init-sidecar
kubectl logs app-with-init-sidecar -c wait-for-db
kubectl logs app-with-init-sidecar -c app
kubectl logs app-with-init-sidecar -c log-sidecar
```

---

## 14. Implement ConfigMap and Secret Management

**Question:** Create a ConfigMap for application config and a Secret for credentials, then use them in a deployment with automatic reloading.

**Solution:**

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    logging.level=INFO
    feature.flag.enabled=true
  config.yaml: |
    database:
      host: db.example.com
      timeout: 30s
---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  username: admin
  password: super-secret-password
  api-key: abc123xyz
data:
  # Base64 encoded (echo -n 'value' | base64)
  token: c2VjcmV0LXRva2Vu
---
# Deployment using ConfigMap and Secret
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: username
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: password
        envFrom:
        - secretRef:
            name: app-secrets
        volumeMounts:
        - name: config
          mountPath: /etc/app/config
          readOnly: true
        - name: secrets
          mountPath: /etc/app/secrets
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: app-config
      - name: secrets
        secret:
          secretName: app-secrets
          defaultMode: 0400
```

**Reloader for automatic updates (using Reloader operator):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    reloader.stakater.com/auto: "true"
spec:
  # ... deployment spec
```

**Key Points:**
- ConfigMaps for non-sensitive config
- Secrets for sensitive data (base64 encoded, not encrypted)
- Use external secret operators for production (Sealed Secrets, Vault)
- Reloader can restart pods when ConfigMap/Secret changes

**Verification:**
```bash
kubectl get configmap app-config -o yaml
kubectl get secret app-secrets -o yaml
kubectl exec app-xxx -- env | grep DB_
kubectl exec app-xxx -- cat /etc/app/config/app.properties
```

---

## 15. Implement Multi-Container Pod Communication

**Question:** Create a pod with multiple containers that communicate via shared volumes and localhost.

**Solution:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: web-server
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
    - name: nginx-config
      mountPath: /etc/nginx/conf.d
  - name: content-generator
    image: busybox:1.35
    command: ['sh', '-c']
    args:
    - |
      while true; do
        echo "<h1>Generated at $(date)</h1>" > /shared/index.html
        sleep 10
      done
    volumeMounts:
    - name: shared-data
      mountPath: /shared
  - name: config-watcher
    image: busybox:1.35
    command: ['sh', '-c']
    args:
    - |
      while true; do
        cat > /config/app.conf <<EOF
        server {
            listen 80;
            location / {
                root /usr/share/nginx/html;
            }
        }
        EOF
        sleep 30
      done
    volumeMounts:
    - name: nginx-config
      mountPath: /config
  volumes:
  - name: shared-data
    emptyDir: {}
  - name: nginx-config
    emptyDir: {}
```

**Key Points:**
- Containers in same pod share network namespace (localhost)
- Shared volumes enable file-based communication
- All containers must be ready for pod to be ready
- Useful for: logging sidecars, proxies, content generators

**Verification:**
```bash
kubectl get pod multi-container-pod
kubectl exec multi-container-pod -c web-server -- curl localhost
kubectl exec multi-container-pod -c content-generator -- ls -la /shared
kubectl logs multi-container-pod -c web-server
kubectl logs multi-container-pod -c content-generator
```

---

## 16. Configure Pod Lifecycle Hooks (PreStop and PostStart)

**Question:** Implement graceful shutdown using PreStop hook and health check initialization with PostStart hook.

**Solution:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-hooks
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: nginx:1.21
        ports:
        - containerPort: 80
        lifecycle:
          postStart:
            exec:
              command:
              - /bin/sh
              - -c
              - |
                echo "Application started" > /tmp/started
                # Initialize health check file
                touch /tmp/healthy
          preStop:
            exec:
              command:
              - /bin/sh
              - -c
              - |
                # Graceful shutdown
                echo "Shutting down gracefully..."
                # Remove from load balancer
                rm /tmp/healthy
                # Wait for connections to drain
                sleep 15
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        terminationGracePeriodSeconds: 30
```

**Key Points:**
- `postStart`: Runs after container starts (not guaranteed to complete before main process)
- `preStop`: Runs before container termination (critical for graceful shutdown)
- `terminationGracePeriodSeconds`: Time to wait before force kill
- Use preStop to drain connections, save state, cleanup

**Verification:**
```bash
kubectl get pods -l app=myapp
kubectl delete pod <pod-name>  # Watch graceful shutdown
kubectl logs <pod-name> | grep -i shutdown
```

---

## 17. Implement Custom Admission Controllers

**Question:** Create a ValidatingAdmissionWebhook that rejects deployments without resource limits.

**Solution:**

**Webhook Server (Python example):**

```python
from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    admission_review = request.json
    uid = admission_review['request']['uid']
    obj = admission_review['request']['object']
    
    # Check if it's a Deployment
    if obj.get('kind') == 'Deployment':
        containers = obj.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
        
        violations = []
        for container in containers:
            resources = container.get('resources', {})
            limits = resources.get('limits', {})
            
            if not limits.get('cpu') or not limits.get('memory'):
                violations.append(
                    f"Container '{container['name']}' missing resource limits"
                )
        
        if violations:
            return jsonify({
                'apiVersion': 'admission.k8s.io/v1',
                'kind': 'AdmissionReview',
                'response': {
                    'uid': uid,
                    'allowed': False,
                    'status': {
                        'code': 403,
                        'message': '; '.join(violations)
                    }
                }
            })
    
    return jsonify({
        'apiVersion': 'admission.k8s.io/v1',
        'kind': 'AdmissionReview',
        'response': {
            'uid': uid,
            'allowed': True
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
```

**ValidatingWebhookConfiguration:**

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionWebhook
metadata:
  name: resource-limits-validator
webhooks:
- name: resourcelimits.example.com
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: "/validate"
  rules:
  - apiGroups: ["apps"]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["deployments"]
  admissionReviewVersions: ["v1"]
  sideEffects: None
  failurePolicy: Fail
```

**Key Points:**
- Admission webhooks intercept API requests
- ValidatingWebhook: validates and can reject
- MutatingWebhook: modifies objects before validation
- Requires TLS certificate and service

**Verification:**
```bash
# Try creating deployment without limits (should fail)
kubectl apply -f deployment-without-limits.yaml
# Should see rejection message
```

---

## 18. Implement Cluster Autoscaling

**Question:** Configure cluster autoscaling to automatically add/remove nodes based on pod scheduling requirements.

**Solution:**

**Cluster Autoscaler Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.27.0
        name: cluster-autoscaler
        resources:
          limits:
            cpu: 100m
            memory: 300Mi
          requests:
            cpu: 100m
            memory: 300Mi
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
        - --balance-similar-node-groups
        - --scale-down-enabled=true
        - --scale-down-delay-after-add=10m
        - --scale-down-unneeded-time=10m
        - --scale-down-utilization-threshold=0.5
        env:
        - name: AWS_REGION
          value: us-west-2
```

**Node Selector and Taints for Autoscaling Groups:**

```yaml
apiVersion: v1
kind: Node
metadata:
  labels:
    node.kubernetes.io/instance-type: spot
    k8s.io/cluster-autoscaler/enabled: "true"
    k8s.io/cluster-autoscaler/my-cluster: "true"
  annotations:
    cluster-autoscaler.kubernetes.io/scale-down-disabled: "false"
```

**Key Points:**
- Cluster Autoscaler adds nodes when pods can't be scheduled
- Removes nodes when underutilized (after scale-down-delay)
- Works with cloud provider ASGs/node pools
- Respects PDBs and node taints

**Verification:**
```bash
kubectl get nodes
kubectl logs -n kube-system deployment/cluster-autoscaler
# Create unschedulable pods to trigger scale-up
```

---

## 19. Implement Service Mesh with mTLS

**Question:** Configure Istio service mesh with mutual TLS between services.

**Solution:**

**Install Istio:**

```bash
istioctl install --set values.global.mtls.enabled=true
```

**PeerAuthentication (mTLS):**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT  # STRICT, PERMISSIVE, DISABLE
---
# Namespace-level mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
---
# Service-level mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: api-service
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  mtls:
    mode: STRICT
```

**AuthorizationPolicy:**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-policy
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend-sa"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

**Key Points:**
- mTLS encrypts service-to-service communication
- PeerAuthentication enforces mTLS
- AuthorizationPolicy controls access based on identity
- STRICT mode requires mTLS, PERMISSIVE allows both

**Verification:**
```bash
istioctl authn tls-check frontend-service.production.svc.cluster.local
kubectl get peerauthentication
kubectl get authorizationpolicy
```

---

## 20. Configure Pod Priority and Preemption

**Question:** Set up pod priorities so critical workloads can preempt lower-priority pods when resources are scarce.

**Solution:**

```yaml
# PriorityClass
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority class for critical workloads"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100
globalDefault: false
description: "Low priority class for batch jobs"
---
# High Priority Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-app
spec:
  replicas: 5
  selector:
    matchLabels:
      app: critical
  template:
    metadata:
      labels:
        app: critical
    spec:
      priorityClassName: high-priority
      containers:
      - name: app
        image: nginx:1.21
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
---
# Low Priority Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-job
spec:
  replicas: 10
  selector:
    matchLabels:
      app: batch
  template:
    metadata:
      labels:
        app: batch
    spec:
      priorityClassName: low-priority
      containers:
      - name: job
        image: busybox:1.35
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
```

**Key Points:**
- Higher value = higher priority
- Preemption evicts lower-priority pods when high-priority can't be scheduled
- System pods (kube-system) have high priority
- Preemption respects PDBs

**Verification:**
```bash
kubectl get priorityclass
kubectl get pods --sort-by=.spec.priority
kubectl describe pod <pod-name> | grep Priority
```

---

## 21. Implement Custom Scheduler

**Question:** Create a custom scheduler that prioritizes pods with specific annotations.

**Solution:**

**Custom Scheduler (Python example):**

```python
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

config.load_incluster_config()
v1 = client.CoreV1Api()

def nodes_available():
    nodes = v1.list_node()
    return [node.metadata.name for node in nodes.items 
            if node.spec.unschedulable is None]

def score_node(pod, node_name):
    score = 50  # Base score
    
    # Check pod annotations
    annotations = pod.metadata.annotations or {}
    preferred_node = annotations.get('scheduler.example.com/preferred-node')
    
    if preferred_node == node_name:
        score += 50
    
    # Check node labels
    node = v1.read_node(node_name)
    labels = node.metadata.labels or {}
    
    pod_zone = annotations.get('scheduler.example.com/zone')
    node_zone = labels.get('topology.kubernetes.io/zone')
    
    if pod_zone == node_zone:
        score += 30
    
    return score

def schedule_pod(pod_name, namespace):
    pod = v1.read_namespaced_pod(pod_name, namespace)
    
    if pod.spec.scheduler_name != 'my-custom-scheduler':
        return None
    
    nodes = nodes_available()
    if not nodes:
        return None
    
    # Score nodes
    node_scores = {}
    for node in nodes:
        node_scores[node] = score_node(pod, node)
    
    # Select highest scoring node
    best_node = max(node_scores, key=node_scores.get)
    
    # Bind pod to node
    binding = client.V1Binding(
        target=client.V1ObjectReference(
            api_version="v1",
            kind="Node",
            name=best_node
        )
    )
    
    try:
        v1.create_namespaced_pod_binding(
            name=pod_name,
            namespace=namespace,
            body=binding
        )
        print(f"Scheduled {pod_name} to {best_node}")
        return best_node
    except ApiException as e:
        print(f"Error binding pod: {e}")
        return None

def watch_pods():
    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event['object']
        if (pod.spec.scheduler_name == 'my-custom-scheduler' and
            pod.spec.node_name is None and
            pod.status.phase == 'Pending'):
            schedule_pod(pod.metadata.name, pod.metadata.namespace)

if __name__ == "__main__":
    watch_pods()
```

**Pod using custom scheduler:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: scheduled-pod
  annotations:
    scheduler.example.com/preferred-node: node-1
    scheduler.example.com/zone: us-west-2a
spec:
  schedulerName: my-custom-scheduler
  containers:
  - name: app
    image: nginx:1.21
```

**Key Points:**
- Custom schedulers watch for unscheduled pods
- Use `schedulerName` to specify custom scheduler
- Scheduler binds pods to nodes via Binding API
- Can implement complex scheduling logic

**Verification:**
```bash
kubectl get pods -o wide
kubectl describe pod scheduled-pod | grep "Scheduled By"
```

---

## 22. Configure Pod Security Admission (PSA)

**Question:** Enforce pod security standards at namespace level using Pod Security Admission.

**Solution:**

```yaml
# Namespace with restricted policy
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
# Namespace with baseline policy (warnings only)
apiVersion: v1
kind: Namespace
metadata:
  name: dev-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
# Exempt user/service account
apiVersion: v1
kind: Namespace
metadata:
  name: exempt-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
  annotations:
    pod-security.kubernetes.io/exempt: "user=admin,serviceaccount=system:serviceaccount:kube-system:admin"
```

**AdmissionConfiguration (cluster-level):**

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1
    kind: PodSecurityConfiguration
    defaults:
      enforce: "restricted"
      enforce-version: "latest"
      audit: "restricted"
      audit-version: "latest"
      warn: "restricted"
      warn-version: "latest"
    exemptions:
      usernames: []
      runtimeClasses: []
      namespaces: ["kube-system", "kube-public"]
```

**Key Points:**
- Three levels: `privileged`, `baseline`, `restricted`
- Three modes: `enforce` (reject), `audit` (log), `warn` (warning)
- Replaces deprecated PodSecurityPolicy
- Can exempt specific users/namespaces

**Verification:**
```bash
kubectl label namespace test-ns pod-security.kubernetes.io/enforce=restricted
# Try creating pod without security context (should fail)
kubectl apply -f insecure-pod.yaml
```

---

## 23. Implement Multi-Cluster Federation

**Question:** Set up multi-cluster service discovery and failover using Kubernetes Federation or Service Mesh.

**Solution:**

**Using KubeFed (Federated Resources):**

```yaml
# FederatedDeployment
apiVersion: types.kubefed.io/v1beta1
kind: FederatedDeployment
metadata:
  name: app
  namespace: default
spec:
  placement:
    clusters:
    - name: cluster1
    - name: cluster2
  template:
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: myapp
      template:
        metadata:
          labels:
            app: myapp
        spec:
          containers:
          - name: app
            image: nginx:1.21
  overrides:
  - clusterName: cluster1
    clusterOverrides:
    - path: "/spec/replicas"
      value: 5
```

**Using Istio Multi-Cluster:**

```yaml
# ServiceEntry for remote cluster
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: remote-service
spec:
  hosts:
  - remote-service.remote-cluster.svc.cluster.local
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: DNS
  location: MESH_INTERNAL
---
# DestinationRule with failover
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: app-dr
spec:
  host: app-service
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
    loadBalancer:
      localityLbSetting:
        enabled: true
        failover:
        - from: region1
          to: region2
```

**Key Points:**
- Multi-cluster enables disaster recovery, geo-distribution
- KubeFed manages resources across clusters
- Service mesh provides transparent cross-cluster communication
- Requires network connectivity and trust between clusters

**Verification:**
```bash
kubectl get federateddeployment
kubectl get pods --all-namespaces -o wide
```

---

## 24. Configure Advanced Probes with Custom Logic

**Question:** Implement custom health checks using exec probes with complex logic.

**Solution:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-custom-probes
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        # Startup probe - allows slow-starting containers
        startupProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - |
              # Check if application process is running
              pgrep -f "java.*myapp" > /dev/null && \
              # Check if port is listening
              netstat -tuln | grep -q ":8080.*LISTEN" && \
              # Check if health endpoint responds
              curl -f http://localhost:8080/health || exit 1
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 30  # 2.5 minutes total
        # Liveness probe - detects deadlocks
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - |
              # Check if process is responsive
              timeout 2 curl -f http://localhost:8080/health || exit 1
              # Check if thread dump endpoint works (detects deadlocks)
              timeout 2 curl -f http://localhost:8080/threads || exit 1
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        # Readiness probe - checks if ready to serve traffic
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
            httpHeaders:
            - name: X-Custom-Header
              value: HealthCheck
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3
```

**Key Points:**
- Startup probe: allows slow-starting containers
- Liveness probe: restarts container if unhealthy
- Readiness probe: removes from service endpoints if not ready
- Custom exec probes enable complex health check logic

**Verification:**
```bash
kubectl get pods -l app=myapp
kubectl describe pod <pod-name> | grep -A 10 "Liveness\|Readiness\|Startup"
kubectl logs <pod-name> | grep -i health
```

---

## 25. Implement Advanced Storage with CSI Drivers

**Question:** Configure dynamic provisioning with storage classes and volume snapshots.

**Solution:**

```yaml
# StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain
---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
---
# VolumeSnapshotClass
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-snapshot-class
driver: ebs.csi.aws.com
deletionPolicy: Retain
parameters:
  tagSpecification_1: "Snapshot=true"
---
# VolumeSnapshot
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: app-data-snapshot
spec:
  volumeSnapshotClassName: csi-snapshot-class
  source:
    persistentVolumeClaimName: app-data
---
# Restore from Snapshot
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data-restored
spec:
  dataSource:
    name: app-data-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
  - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
```

**Key Points:**
- CSI drivers enable vendor-agnostic storage
- `WaitForFirstConsumer` delays binding until pod scheduling
- Volume snapshots enable backup/restore
- `allowVolumeExpansion` enables online resizing

**Verification:**
```bash
kubectl get storageclass
kubectl get pvc
kubectl get volumesnapshot
kubectl describe pvc app-data
```

---

## 26. Configure Advanced Networking with CNI Plugins

**Question:** Set up network policies and IP address management using Calico CNI.

**Solution:**

**Calico Installation:**

```yaml
# Calico IP Pool
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: default-ipv4-ippool
spec:
  cidr: 192.168.0.0/16
  blockSize: 26
  ipipMode: Always
  natOutgoing: true
---
# NetworkPolicy (Kubernetes native)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-backend
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 8080
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
---
# Calico GlobalNetworkPolicy
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: default-deny-all
spec:
  selector: all()
  types:
  - Ingress
  - Egress
  egress:
  - action: Allow
    protocol: UDP
    destination:
      ports:
      - 53  # DNS
---
# Calico NetworkPolicy (advanced)
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: advanced-policy
  namespace: production
spec:
  selector: app == "api"
  ingress:
  - action: Allow
    source:
      selector: app == "frontend"
      namespaceSelector: name == "production"
    destination:
      ports:
      - 8080
  egress:
  - action: Allow
    destination:
      selector: app == "database"
      namespaceSelector: name == "production"
    protocol: TCP
    destination:
      ports:
      - 5432
```

**Key Points:**
- CNI plugins provide networking implementation
- Calico supports both Kubernetes and Calico network policies
- IP pools manage IP address allocation
- Network policies enforce micro-segmentation

**Verification:**
```bash
calicoctl get ippool
calicoctl get networkpolicy
kubectl get networkpolicy
```

---

## 27. Implement Advanced Monitoring with Prometheus and Grafana

**Question:** Set up comprehensive monitoring with custom metrics, alerts, and dashboards.

**Solution:**

**Prometheus ServiceMonitor:**

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    scheme: https
    tlsConfig:
      insecureSkipVerify: true
---
# Service exposing metrics
apiVersion: v1
kind: Service
metadata:
  name: app-service
  labels:
    app: myapp
spec:
  ports:
  - name: metrics
    port: 9090
    targetPort: 9090
  selector:
    app: myapp
---
# PrometheusRule for alerts
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-alerts
  namespace: monitoring
spec:
  groups:
  - name: app.rules
    interval: 30s
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value }} errors/sec"
    - alert: PodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Pod is crash looping"
```

**Grafana Dashboard ConfigMap:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard
  namespace: monitoring
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Application Metrics",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [{
              "expr": "rate(http_requests_total[5m])"
            }]
          }
        ]
      }
    }
```

**Key Points:**
- ServiceMonitor tells Prometheus what to scrape
- PrometheusRule defines alerting rules
- Grafana visualizes metrics
- Use Prometheus Operator for easier management

**Verification:**
```bash
kubectl get servicemonitor
kubectl get prometheusrule
# Access Prometheus: kubectl port-forward svc/prometheus 9090:9090
# Access Grafana: kubectl port-forward svc/grafana 3000:3000
```

---

## 28. Implement GitOps with ArgoCD/Flux

**Question:** Set up GitOps workflow where Kubernetes manifests are managed in Git and automatically synced.

**Solution:**

**ArgoCD Application:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests
    targetRevision: main
    path: production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
---
# App of Apps pattern
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests
    targetRevision: main
    path: argocd/apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**Flux GitRepository and Kustomization:**

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: app-repo
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/k8s-manifests
  ref:
    branch: main
  secretRef:
    name: git-credentials
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: production-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./production
  prune: true
  sourceRef:
    kind: GitRepository
    name: app-repo
  validation: client
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: app
    namespace: production
```

**Key Points:**
- GitOps: Git as source of truth
- ArgoCD: Pull-based, UI for visualization
- Flux: Push-based, more Git-native
- Both support automated sync and drift detection

**Verification:**
```bash
kubectl get applications -n argocd
argocd app get production-app
kubectl get kustomization -n flux-system
flux get kustomizations
```

---

## 29. Implement Advanced Troubleshooting Scenarios

**Question:** Diagnose and fix a pod that's in CrashLoopBackOff state with limited information.

**Solution:**

**Troubleshooting Steps:**

```bash
# 1. Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# 2. Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Previous container instance

# 3. Check events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector involvedObject.name=<pod-name>

# 4. Check resource constraints
kubectl top pod <pod-name>
kubectl describe node <node-name>

# 5. Check configuration
kubectl get pod <pod-name> -o yaml
kubectl get configmap,secret -n <namespace>

# 6. Exec into pod (if running)
kubectl exec -it <pod-name> -- sh

# 7. Check network connectivity
kubectl run debug --image=nicolaka/netshoot --rm -it -- sh
# Inside debug pod:
# nslookup <service-name>
# curl <service-endpoint>

# 8. Check DNS
kubectl get svc kube-dns -n kube-system
kubectl logs -n kube-system -l k8s-app=kube-dns

# 9. Check node resources
kubectl describe node | grep -A 5 "Allocated resources"

# 10. Check admission webhooks
kubectl get validatingwebhookconfiguration
kubectl get mutatingwebhookconfiguration
```

**Common Issues and Fixes:**

```yaml
# Issue: ImagePullBackOff
# Fix: Check image name, registry credentials
apiVersion: v1
kind: Secret
metadata:
  name: registry-secret
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded>
---
# Issue: CrashLoopBackOff - Missing config
# Fix: Add missing ConfigMap/Secret
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.properties: |
    key=value
---
# Issue: OOMKilled
# Fix: Increase memory limits or fix memory leak
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        resources:
          limits:
            memory: 1Gi  # Increase if needed
          requests:
            memory: 512Mi
```

**Key Points:**
- Always check logs first (`kubectl logs`)
- Use `describe` for detailed pod/node information
- Check events for recent changes
- Verify resource constraints and quotas
- Use debug pods for network troubleshooting

---

## 30. Implement Advanced Security: Pod Security, Image Scanning, and Runtime Protection

**Question:** Implement comprehensive security: enforce pod security standards, scan container images, and protect runtime.

**Solution:**

**Pod Security Standards:**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Image Policy with OPA Gatekeeper:**

```yaml
# ConstraintTemplate
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimages
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImages
      validation:
        openAPIV3Schema:
          type: object
          properties:
            exemptImages:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimages
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not startswith(container.image, "myregistry.com/")
          not container.image in input.parameters.exemptImages
          msg := sprintf("Image '%v' not from allowed registry", [container.image])
        }
---
# Constraint
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredImages
metadata:
  name: must-be-from-registry
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    exemptImages:
      - "k8s.gcr.io/*"
      - "gcr.io/*"
```

**Falco Runtime Security:**

```yaml
# FalcoRules for detecting suspicious activity
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-rules
data:
  custom-rules.yaml: |
    - rule: Write below binary dir
      desc: Detect writes to binary directories
      condition: >
        bin_dir and evt.dir = < and open_write
        and not package_mgmt_procs
        and not exe_running_docker_save
        and not python_running_get_pip
        and not python_running_msf
        and not user_known_write_below_binary_dir_activities
      output: >
        File below a known binary directory opened for writing
        (user=%user.name command=%proc.cmdline file=%fd.name parent=%proc.pname
        container_id=%container.id image=%container.image.repository)
      priority: ERROR
      tags: [filesystem, mitre_persistence]
```

**Trivy Image Scanning:**

```yaml
# ScanJob
apiVersion: batch/v1
kind: Job
metadata:
  name: image-scan
spec:
  template:
    spec:
      containers:
      - name: trivy
        image: aquasec/trivy:latest
        command:
        - trivy
        - image
        - --exit-code
        - "1"
        - --severity
        - HIGH,CRITICAL
        - myapp:latest
      restartPolicy: Never
```

**Key Points:**
- Pod Security Standards enforce security at namespace level
- OPA Gatekeeper enforces policies via admission control
- Falco detects runtime threats and anomalies
- Image scanning prevents vulnerable images from running
- Defense in depth: multiple security layers

**Verification:**
```bash
kubectl get constrainttemplate
kubectl get k8srequiredimages
kubectl logs -n falco-system -l app=falco
trivy image myapp:latest
```

---

## Summary

These 30 questions cover:
- **Scheduling**: Affinity, Taints/Tolerations, Custom Schedulers
- **Networking**: Network Policies, Service Mesh, Multi-cluster
- **Storage**: StatefulSets, PVCs, Snapshots, CSI
- **Security**: RBAC, Pod Security, Admission Controllers, Runtime Protection
- **Autoscaling**: HPA, VPA, Cluster Autoscaler
- **Deployment**: Canary, Blue-Green, GitOps
- **Observability**: Monitoring, Logging, Tracing
- **Advanced**: CRDs, Operators, Troubleshooting

Each solution includes practical YAML manifests, commands, and explanations suitable for medium to senior-level interviews.

