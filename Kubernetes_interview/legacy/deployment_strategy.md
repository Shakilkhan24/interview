# Kubernetes Deployment Strategies: A Comprehensive Guide

Deployment strategies in Kubernetes control **how your application updates are rolled out** to users, balancing between speed, reliability, and risk management.

## 1. **Recreate Strategy** (Big Bang Deployment)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: Recreate  # All old pods are terminated before new ones are created
```

**How it works:**
- Terminates **all existing pods** first
- Creates **new pods** with updated version
- **Downtime occurs** during transition

**Use cases:**
- Development environments
- Non-critical applications
- When database migrations require it

## 2. **Rolling Update** (Default Strategy)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Can create 1 pod over desired count
      maxUnavailable: 0  # Minimum available pods during update
```

**How it works:**
- Gradually replaces old pods with new ones
- Zero downtime (if configured properly)
- Controlled by `maxSurge` and `maxUnavailable`

**Pros:**
- No downtime
- Easy rollback
- Built-in to Kubernetes

**Cons:**
- Version inconsistency during rollout
- Complex stateful applications may have issues

## 3. **Blue-Green Deployment**
**Concept:** Maintain two identical environments (Blue = current, Green = new)

```yaml
# Step 1: Deploy Green environment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green

# Step 2: Switch service from Blue to Green
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: green  # Change from 'blue' to 'green'
  ports:
  - port: 80
```

**Implementation Steps:**
1. Deploy new version alongside old version
2. Test new version thoroughly
3. Switch traffic using Service selector
4. Delete old deployment

**Pros:**
- Instant rollback (just switch selector back)
- Zero downtime
- Full version testing before traffic switch

**Cons:**
- Requires double resources
- Database schema changes need careful handling

## 4. **Canary Deployment**
**Concept:** Release new version to a small subset of users first

```yaml
# Main deployment (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v1
spec:
  replicas: 9
  template:
    metadata:
      labels:
        app: myapp
        version: v1

# Canary deployment (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v2-canary
spec:
  replicas: 1  # 10% of total traffic
  template:
    metadata:
      labels:
        app: myapp
        version: v2

# Service with both versions
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp  # Routes to both v1 and v2
```

**Advanced Canary with Service Mesh (Istio):**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90  # 90% to v1
    - destination:
        host: myapp
        subset: v2
      weight: 10  # 10% to v2
```

**Pros:**
- Low-risk testing with real users
- Performance monitoring before full rollout
- Gradual traffic increase

**Cons:**
- More complex to implement
- Requires traffic splitting mechanism

## 5. **A/B Testing Deployment**
Similar to Canary but based on **user attributes** (headers, cookies, geography)

```yaml
# Using Istio for A/B testing
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        user-type:
          exact: premium
    route:
    - destination:
        host: myapp
        subset: new-ui  # Premium users get new UI
  - route:
    - destination:
        host: myapp
        subset: old-ui  # Everyone else gets old UI
```

## 6. **Shadow Deployment** (Traffic Mirroring)
**Concept:** Send copy of production traffic to new version without affecting users

```yaml
# Istio mirroring configuration
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 100
    mirror:
      host: myapp
      subset: v2
    mirror_percentage:
      value: 100  # Mirror 100% of traffic
```

**Pros:**
- Test with real traffic without risk
- Performance comparison

**Cons:**
- Complex setup
- Can affect new version's performance

## Comparison Table

| Strategy | Downtime | Rollback Speed | Resource Usage | Complexity |
|----------|----------|----------------|----------------|------------|
| Recreate | Yes | Slow | Low | Low |
| Rolling Update | No | Medium | Medium | Low |
| Blue-Green | No | Fast | High | Medium |
| Canary | No | Fast | Medium | High |
| A/B Testing | No | Fast | Medium | High |
| Shadow | No | N/A | High | Very High |

## Best Practices

### 1. **Health Checks are Crucial**
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: myapp
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 2. **Resource Management**
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### 3. **Pod Disruption Budget**
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # Always keep at least 2 pods running
  selector:
    matchLabels:
      app: myapp
```

### 4. **Rollback Procedures**
```bash
# Rollback to previous version
kubectl rollout undo deployment/myapp

# Check rollout history
kubectl rollout history deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2
```

## Choosing the Right Strategy

### **Start with:**
- **Development**: Recreate (simple)
- **Staging**: Rolling Update
- **Production**: Start with Rolling, evolve to Blue-Green/Canary

### **Consider:**
1. **Application Type**: Stateless apps can use any strategy
2. **Database Changes**: May require Recreate or careful Blue-Green
3. **Team Experience**: Start simple, add complexity gradually
4. **Infrastructure**: Service Mesh needed for advanced strategies

## Quick Decision Flowchart

```
Is downtime acceptable?
├── Yes → Use **Recreate**
└── No → Need instant rollback?
         ├── Yes → Use **Blue-Green**
         └── No → Need to test with real users?
                  ├── Yes → Use **Canary** (or A/B if user segmentation needed)
                  └── No → Use **Rolling Update**
```

## Hands-On Exercise

Try this minimal Canary deployment:

```bash
# 1. Deploy v1
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
EOF

# 2. Create service
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80
EOF

# 3. Deploy canary (v2)
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
EOF

# 4. Monitor (25% traffic to v2)
kubectl get pods -l app=myapp
```

## Advanced Tools

1. **Flagger** (CNCF project): Automates canary deployments
2. **Argo Rollouts**: Progressive delivery controller
3. **Istio/Linkerd**: Service mesh for traffic splitting
4. **Spinnaker**: Multi-cloud deployment platform

Remember: **Start simple, measure everything, and evolve your strategy based on actual needs.** The best strategy depends on your specific application, team, and business requirements.