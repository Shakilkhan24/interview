# ArgoCD - Complete Guide
## GitOps Continuous Delivery for Kubernetes

---

## Table of Contents
1. [Introduction to ArgoCD](#1-introduction-to-argocd)
2. [Core Concepts](#2-core-concepts)
3. [Installation and Setup](#3-installation-and-setup)
4. [Application Management](#4-application-management)
5. [Sync Policies and Strategies](#5-sync-policies-and-strategies)
6. [Multi-Environment Management](#6-multi-environment-management)
7. [Advanced Features](#7-advanced-features)
8. [Security and RBAC](#8-security-and-rbac)
9. [Best Practices](#9-best-practices)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Introduction to ArgoCD

### What is ArgoCD?

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It automates the deployment of applications to Kubernetes clusters by syncing the desired state defined in Git repositories with the actual state in the cluster.

### Key Features

- **GitOps**: Git as the single source of truth
- **Declarative**: Define desired state in YAML
- **Automated Sync**: Continuous synchronization
- **Multi-Environment**: Manage multiple clusters
- **Rollback**: Easy rollback to previous versions
- **Web UI**: Visual interface for monitoring
- **RBAC**: Role-based access control

### ArgoCD vs Other Tools

| Feature | ArgoCD | Flux | Jenkins X | Spinnaker |
|---------|--------|------|----------|-----------|
| GitOps | ✅ Native | ✅ Native | ✅ Yes | ⚠️ Partial |
| UI | ✅ Excellent | ⚠️ Basic | ✅ Good | ✅ Good |
| Multi-cluster | ✅ Yes | ✅ Yes | ⚠️ Limited | ✅ Yes |
| Learning Curve | ✅ Easy | ✅ Easy | ⚠️ Medium | ⚠️ Steep |
| Helm Support | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Kustomize | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Limited |

### Architecture

```
┌─────────────┐
│  Git Repo   │
│ (Source of  │
│   Truth)    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   ArgoCD        │
│   Application   │
│   Controller    │
└──────┬──────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Cluster 1│   │ Cluster 2│   │ Cluster 3│
│ (Dev)    │   │ (Staging)│   │ (Prod)   │
└──────────┘   └──────────┘   └──────────┘
```

---

## 2. Core Concepts

### Application

An ArgoCD Application represents a deployed application in a Kubernetes cluster. It defines:
- Source repository (Git, Helm, Kustomize)
- Destination cluster and namespace
- Sync policy
- Health checks

### ApplicationSet

ApplicationSet automates the creation of multiple Applications based on:
- Git directories
- Cluster lists
- Matrix combinations

### Sync

The process of applying the desired state from Git to the cluster. Can be:
- **Automatic**: Continuous sync
- **Manual**: Triggered manually
- **Scheduled**: Based on cron

### Health Status

ArgoCD monitors application health:
- **Healthy**: All resources are healthy
- **Progressing**: Deployment in progress
- **Degraded**: Some resources unhealthy
- **Suspended**: Application is paused
- **Unknown**: Health status unknown
- **Missing**: Resources not found

### Sync Status

- **Synced**: Cluster matches Git state
- **OutOfSync**: Differences detected
- **Unknown**: Status unknown

---

## 3. Installation and Setup

### Installation Methods

#### Method 1: kubectl (Recommended)

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod \
  --all -n argocd --timeout=300s

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

#### Method 2: Helm

```bash
# Add ArgoCD Helm repository
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install ArgoCD
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set server.service.type=LoadBalancer
```

#### Method 3: Terraform

```hcl
# Install ArgoCD using Helm provider
resource "helm_release" "argocd" {
  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace  = "argocd"
  version    = "5.46.7"

  values = [
    file("${path.module}/values/argocd-values.yaml")
  ]

  create_namespace = true
}
```

### Initial Configuration

```bash
# Login via CLI
argocd login localhost:8080 --username admin --password <password>

# Change admin password
argocd account update-password

# Add Git repository
argocd repo add https://github.com/user/repo \
  --type git \
  --name myrepo

# Add cluster (if managing external cluster)
argocd cluster add <context-name>
```

### Accessing ArgoCD

**Web UI:**
- Default: `https://argocd-server.argocd.svc.cluster.local`
- Port-forward: `kubectl port-forward svc/argocd-server -n argocd 8080:443`
- Ingress: Configure ingress for external access

**CLI:**
```bash
# Install CLI
brew install argocd  # macOS
# Or download from: https://github.com/argoproj/argo-cd/releases

# Login
argocd login <argocd-server>
```

---

## 4. Application Management

### Basic Application

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/user/repo
    targetRevision: main
    path: k8s/base
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### Application with Helm

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-helm
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://charts.example.com
    chart: myapp
    targetRevision: 1.0.0
    helm:
      valueFiles:
      - values.yaml
      parameters:
      - name: image.tag
        value: v1.0.0
      - name: replicas
        value: "3"
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Application with Kustomize

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-kustomize
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/user/repo
    targetRevision: main
    path: k8s/overlays/production
    kustomize:
      images:
      - myapp:v1.0.0
      commonAnnotations:
        app.kubernetes.io/managed-by: argocd
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
```

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  
  source:
    repoURL: https://github.com/user/repo
    targetRevision: HEAD
    path: k8s/base
  
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
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  revisionHistoryLimit: 10
```

---

## 5. Sync Policies and Strategies

### Automated Sync

```yaml
syncPolicy:
  automated:
    prune: true        # Delete resources removed from Git
    selfHeal: true     # Automatically sync when cluster drifts
    allowEmpty: false  # Don't sync if no resources
```

### Manual Sync

```yaml
syncPolicy:
  syncOptions:
  - CreateNamespace=true
```

**Trigger manually:**
```bash
# Via CLI
argocd app sync myapp

# Via UI
# Click "Sync" button in ArgoCD UI
```

### Sync Waves

```yaml
# Use annotations to control sync order
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"  # Sync first
---
apiVersion: v1
kind: Service
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "2"  # Sync second
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "3"  # Sync last
```

### Sync Hooks

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pre-sync-hook
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:migrate
        command: ["./migrate.sh"]
      restartPolicy: Never
---
apiVersion: batch/v1
kind: Job
metadata:
  name: post-sync-hook
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: notify
        image: myapp:notify
        command: ["./notify.sh"]
      restartPolicy: Never
```

**Hook Types:**
- `PreSync`: Before sync
- `Sync`: During sync
- `PostSync`: After sync
- `SyncFail`: On sync failure

**Hook Delete Policies:**
- `BeforeHookCreation`: Delete before new hook
- `HookSucceeded`: Delete on success
- `HookFailed`: Delete on failure

### Sync Strategies

```yaml
syncPolicy:
  syncOptions:
  - ApplyOutOfSyncOnly=true      # Only apply out-of-sync resources
  - PrunePropagationPolicy=foreground  # Prune with foreground deletion
  - PruneLast=true               # Prune resources last
  - RespectIgnoreDifferences=true  # Respect ignore differences
```

---

## 6. Multi-Environment Management

### ApplicationSet for Multiple Environments

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-environments
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: dev
        url: https://dev-cluster.example.com
        namespace: development
      - cluster: staging
        url: https://staging-cluster.example.com
        namespace: staging
      - cluster: prod
        url: https://prod-cluster.example.com
        namespace: production
  
  template:
    metadata:
      name: '{{cluster}}-myapp'
    spec:
      project: default
      source:
        repoURL: https://github.com/user/repo
        targetRevision: main
        path: k8s/overlays/{{cluster}}
      destination:
        server: '{{url}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Git Directory Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-git-directories
  namespace: argocd
spec:
  generators:
  - git:
      repoURL: https://github.com/user/repo
      revision: main
      directories:
      - path: apps/*
  
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/user/repo
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
```

### Matrix Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-matrix
  namespace: argocd
spec:
  generators:
  - matrix:
      generators:
      - list:
          elements:
          - cluster: dev
            url: https://dev-cluster.example.com
          - cluster: prod
            url: https://prod-cluster.example.com
      - list:
          elements:
          - app: frontend
            namespace: frontend
          - app: backend
            namespace: backend
  
  template:
    metadata:
      name: '{{cluster}}-{{app}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/user/repo
        targetRevision: main
        path: apps/{{app}}
      destination:
        server: '{{url}}'
        namespace: '{{namespace}}'
```

### Cluster Generator

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-clusters
  namespace: argocd
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          environment: production
  
  template:
    metadata:
      name: '{{name}}-myapp'
    spec:
      project: default
      source:
        repoURL: https://github.com/user/repo
        targetRevision: main
        path: k8s/base
      destination:
        server: '{{server}}'
        namespace: production
```

---

## 7. Advanced Features

### Health Checks

**Custom Health Checks:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  # ... other config
  source:
    repoURL: https://github.com/user/repo
    path: k8s/base
    kustomize:
      commonAnnotations:
        # Custom health check
        argocd.argoproj.io/health-check-path: /health
```

**Health Check Lua Script:**

```lua
-- Custom health check for custom resource
hs = {}
if obj.status ~= nil and obj.status.health ~= nil then
  if obj.status.health == "Healthy" then
    hs.status = "Healthy"
    hs.message = "Resource is healthy"
    return hs
  end
  if obj.status.health == "Unhealthy" then
    hs.status = "Unhealthy"
    hs.message = "Resource is unhealthy"
    return hs
  end
end
hs.status = "Progressing"
hs.message = "Waiting for health status"
return hs
```

### Resource Hooks

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:migrate
        command: ["./migrate.sh"]
      restartPolicy: Never
```

### Ignore Differences

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  # ... other config
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
  - group: ""
    kind: Service
    jsonPointers:
    - /spec/clusterIP
```

### Resource Tracking

```yaml
# Track resources by label
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/instance: myapp
spec:
  # ...
```

### Projects

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: production
  namespace: argocd
spec:
  description: Production project
  
  sourceRepos:
  - 'https://github.com/user/repo'
  - 'https://charts.example.com'
  
  destinations:
  - namespace: production
    server: https://kubernetes.default.svc
  - namespace: staging
    server: https://kubernetes.default.svc
  
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  
  namespaceResourceWhitelist:
  - group: '*'
    kind: '*'
  
  roles:
  - name: admin
    policies:
    - p, proj:production:admin, applications, *, production/*, allow
    - p, proj:production:admin, repositories, get, *, allow
    groups:
    - production-admins
```

---

## 8. Security and RBAC

### RBAC Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.csv: |
    # Admin policy
    p, role:admin, applications, *, */*, allow
    p, role:admin, clusters, get, *, allow
    p, role:admin, repositories, get, *, allow
    p, role:admin, repositories, create, *, allow
    p, role:admin, repositories, update, *, allow
    p, role:admin, repositories, delete, *, allow
    
    # Developer policy
    p, role:developer, applications, get, */*, allow
    p, role:developer, applications, sync, */*, allow
    p, role:developer, applications, override, */*, allow
    
    # Read-only policy
    p, role:readonly, applications, get, */*, allow
    
    # Assign roles to groups
    g, developers, role:developer
    g, admins, role:admin
    g, viewers, role:readonly
```

### OIDC Integration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: https://argocd.example.com
  oidc.config: |
    name: Okta
    issuer: https://dev-123456.okta.com/oauth2/default
    clientId: abc123
    clientSecret: $oidc.clientSecret
    requestedScopes: ["openid", "profile", "email", "groups"]
```

### Repository Credentials

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: repo-credentials
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://github.com/user/private-repo
  password: <github-token>
  username: <github-username>
```

### Cluster Access

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: external-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: external-cluster
  server: https://external-cluster.example.com
  config: |
    {
      "bearerToken": "<token>",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "<ca-data>"
      }
    }
```

---

## 9. Best Practices

### Repository Structure

```
repo/
├── apps/
│   ├── frontend/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── backend/
│       └── ...
├── infrastructure/
│   ├── base/
│   └── overlays/
└── argocd/
    ├── applications/
    └── applicationsets/
```

### Application Organization

1. **Use Projects for Isolation**
   ```yaml
   # Separate projects per environment
   - production-project
   - staging-project
   - development-project
   ```

2. **Use ApplicationSets for Scale**
   ```yaml
   # One ApplicationSet for multiple apps
   # Instead of individual Applications
   ```

3. **Version Control Everything**
   ```bash
   # Store Application manifests in Git
   # Use GitOps for ArgoCD itself
   ```

### Sync Policies

1. **Use Automated Sync Carefully**
   ```yaml
   # Only for non-critical environments
   syncPolicy:
     automated:
       prune: true
       selfHeal: true
   ```

2. **Manual Sync for Production**
   ```yaml
   # Production should require manual approval
   syncPolicy:
     syncOptions:
     - CreateNamespace=true
   ```

3. **Use Sync Waves**
   ```yaml
   # Control deployment order
   annotations:
     argocd.argoproj.io/sync-wave: "1"
   ```

### Health Checks

1. **Implement Proper Health Checks**
   ```yaml
   # Use readiness and liveness probes
   livenessProbe:
     httpGet:
       path: /health
       port: 8080
   ```

2. **Custom Health Checks**
   ```lua
   -- For custom resources
   -- Implement health check logic
   ```

### Monitoring

1. **Enable Metrics**
   ```yaml
   # ArgoCD exposes Prometheus metrics
   # Monitor application sync status
   ```

2. **Set Up Alerts**
   ```yaml
   # Alert on:
   # - Sync failures
   # - Health degradation
   # - OutOfSync status
   ```

---

## 10. Troubleshooting

### Common Issues

#### Application Stuck in Syncing

```bash
# Check application status
argocd app get myapp

# Check sync operation
argocd app history myapp

# Force refresh
argocd app get myapp --refresh

# Check logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller
```

#### OutOfSync Resources

```bash
# Compare Git vs Cluster
argocd app diff myapp

# Check what's different
argocd app get myapp --show-params
```

#### Sync Failures

```bash
# Check sync operation details
argocd app get myapp --refresh

# View sync operation logs
argocd app logs myapp

# Retry sync
argocd app sync myapp --retry-limit 5
```

#### Health Check Failures

```bash
# Check resource health
argocd app get myapp --show-params

# Check pod status
kubectl get pods -n <namespace>

# Check events
kubectl get events -n <namespace>
```

### Debugging Commands

```bash
# List all applications
argocd app list

# Get application details
argocd app get myapp

# Get application manifests
argocd app manifests myapp

# Get application parameters
argocd app get myapp --show-params

# Compare Git vs Cluster
argocd app diff myapp

# View application events
argocd app get myapp --show-events

# Check application resources
argocd app resources myapp
```

### Logs

```bash
# Application Controller logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller

# Repo Server logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server

# API Server logs
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-server
```

---

## Summary

ArgoCD provides:

- **GitOps**: Git as single source of truth
- **Automation**: Continuous synchronization
- **Multi-Environment**: Manage multiple clusters
- **Visual Interface**: Web UI for monitoring
- **Rollback**: Easy rollback capabilities
- **Security**: RBAC and OIDC integration

Key takeaways:
- Use Git as the source of truth
- Implement proper sync policies
- Use ApplicationSets for scale
- Enable health checks
- Implement RBAC
- Monitor and alert on issues
- Use sync waves for ordering
- Implement proper repository structure

For production deployments:
- Use manual sync for production
- Implement approval workflows
- Enable monitoring and alerting
- Use health checks
- Implement proper RBAC
- Use projects for isolation
- Version control everything

