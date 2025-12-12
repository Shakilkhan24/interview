# Kustomize Master Tutorial - Kubernetes Configuration Management
## Complete Guide to Kustomize for DevOps Engineers

---

## Table of Contents

1. [Kustomize Fundamentals](#1-kustomize-fundamentals)
2. [Installation & Setup](#2-installation--setup)
3. [Basic Kustomize Operations](#3-basic-kustomize-operations)
4. [Kustomization File Structure](#4-kustomization-file-structure)
5. [Resources & Bases](#5-resources--bases)
6. [Patches & Overlays](#6-patches--overlays)
7. [ConfigMap & Secret Generation](#7-configmap--secret-generation)
8. [Image Transformations](#8-image-transformations)
9. [Name Prefixes & Suffixes](#9-name-prefixes--suffixes)
10. [Namespace Management](#10-namespace-management)
11. [Common Labels & Annotations](#11-common-labels--annotations)
12. [Replicas & Resource Management](#12-replicas--resource-management)
13. [Multi-Environment Setups](#13-multi-environment-setups)
14. [Advanced Patterns](#14-advanced-patterns)
15. [Kustomize with CI/CD](#15-kustomize-with-cicd)
16. [Kustomize vs Helm](#16-kustomize-vs-helm)
17. [Best Practices](#17-best-practices)
18. [Troubleshooting](#18-troubleshooting)

---

## 1. Kustomize Fundamentals

### 1.1 What is Kustomize?

**Kustomize** is a template-free way to customize Kubernetes YAML configurations. It's built into `kubectl` (since v1.14) and provides a declarative approach to managing Kubernetes resources.

**Key Concepts:**
- **Template-free**: No templating language, pure YAML
- **Declarative**: Describe what you want, not how to get it
- **Composable**: Build complex configurations from simple bases
- **Git-friendly**: Works well with version control

### 1.2 Why Use Kustomize?

**Benefits:**
- ✅ No templating complexity
- ✅ Native Kubernetes tool (built into kubectl)
- ✅ Easy multi-environment management
- ✅ Reusable base configurations
- ✅ GitOps friendly
- ✅ No server-side components

**Use Cases:**
- Managing multiple environments (dev, staging, prod)
- Customizing third-party applications
- Creating reusable base configurations
- Managing configuration variations

### 1.3 How Kustomize Works

```
Base Configuration
    ↓
Kustomization.yaml
    ↓
kustomize build
    ↓
Rendered YAML
    ↓
kubectl apply
```

**Workflow:**
1. Create base Kubernetes manifests
2. Create `kustomization.yaml`
3. Run `kustomize build` to generate final YAML
4. Apply with `kubectl apply -k` or `kubectl apply -f <(kustomize build .)`

---

## 2. Installation & Setup

### 2.1 Kustomize Installation

**Kustomize is built into kubectl (v1.14+):**
```bash
# Check kubectl version (should be 1.14+)
kubectl version --client

# Kustomize is available via kubectl
kubectl kustomize --help
```

**Standalone Installation:**
```bash
# Linux/macOS
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/

# macOS (Homebrew)
brew install kustomize

# Verify
kustomize version
```

**Windows:**
```powershell
# Download from releases
# https://github.com/kubernetes-sigs/kustomize/releases
# Extract and add to PATH
```

### 2.2 Verify Installation

```bash
# Check version
kustomize version

# Test kustomize
kustomize --help
```

---

## 3. Basic Kustomize Operations

### 3.1 Simple Example

**Create directory structure:**
```bash
mkdir myapp
cd myapp
```

**Create base deployment (deployment.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: nginx:latest
        ports:
        - containerPort: 80
```

**Create kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
```

**Build and preview:**
```bash
# Build and preview
kustomize build .

# Or use kubectl
kubectl kustomize .

# Apply directly
kubectl apply -k .
```

### 3.2 Common Commands

```bash
# Build kustomization
kustomize build .

# Build and save to file
kustomize build . > output.yaml

# Build with validation
kustomize build . | kubectl apply --dry-run=client -f -

# Apply kustomization
kubectl apply -k .

# Delete resources
kubectl delete -k .

# Diff changes
kubectl diff -k .
```

---

## 4. Kustomization File Structure

### 4.1 Basic kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Resources to include
resources:
- deployment.yaml
- service.yaml
- configmap.yaml

# Common metadata
namespace: production
namePrefix: prod-
nameSuffix: -v1

# Common labels
commonLabels:
  app: myapp
  environment: production

# Common annotations
commonAnnotations:
  managed-by: kustomize
  version: "1.0.0"

# Image transformations
images:
- name: nginx
  newName: myregistry/nginx
  newTag: v1.2.3

# Replicas
replicas:
- name: myapp
  count: 3

# ConfigMap/Secret generators
configMapGenerator:
- name: app-config
  files:
  - config.properties

secretGenerator:
- name: app-secret
  literals:
  - username=admin
  - password=secret123
```

### 4.2 Field Reference

| Field | Description |
|-------|-------------|
| `resources` | List of resource files or directories |
| `bases` | List of base kustomizations (deprecated, use `resources`) |
| `namespace` | Set namespace for all resources |
| `namePrefix` | Prefix to add to all resource names |
| `nameSuffix` | Suffix to add to all resource names |
| `commonLabels` | Labels to add to all resources |
| `commonAnnotations` | Annotations to add to all resources |
| `images` | Image transformations |
| `replicas` | Replica count overrides |
| `configMapGenerator` | Generate ConfigMaps |
| `secretGenerator` | Generate Secrets |
| `patchesStrategicMerge` | Strategic merge patches |
| `patchesJson6902` | JSON 6902 patches |
| `replacements` | Field replacements |

---

## 5. Resources & Bases

### 5.1 Local Resources

**Include local files:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- ingress.yaml
```

### 5.2 Remote Bases

**Include remote kustomizations:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- https://github.com/myorg/k8s-bases/app-base
- https://github.com/myorg/k8s-bases/monitoring-base
```

### 5.3 Local Bases

**Directory structure:**
```
project/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

**base/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
```

**overlays/dev/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: dev
namePrefix: dev-
replicas:
- name: myapp
  count: 1
```

**Build:**
```bash
# Build base
kustomize build base/

# Build dev overlay
kustomize build overlays/dev/

# Build prod overlay
kustomize build overlays/prod/
```

---

## 6. Patches & Overlays

### 6.1 Strategic Merge Patches

**Create patch file (patch.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

**kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

patchesStrategicMerge:
- patch.yaml
```

### 6.2 JSON 6902 Patches

**Create patch file (patch.json):**
```json
[
  {
    "op": "replace",
    "path": "/spec/replicas",
    "value": 3
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/env",
    "value": [
      {
        "name": "ENV",
        "value": "production"
      }
    ]
  }
]
```

**kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

patchesJson6902:
- target:
    group: apps
    version: v1
    kind: Deployment
    name: myapp
  path: patch.json
```

### 6.3 Inline Patches

**kustomization.yaml with inline patch:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

patches:
- patch: |-
    - op: replace
      path: /spec/replicas
      value: 3
  target:
    kind: Deployment
    name: myapp
```

### 6.4 Multiple Patches

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

patchesStrategicMerge:
- replica-patch.yaml
- resource-patch.yaml
- env-patch.yaml

patchesJson6902:
- target:
    group: apps
    version: v1
    kind: Deployment
    name: myapp
  path: json-patch.json
```

---

## 7. ConfigMap & Secret Generation

### 7.1 ConfigMap Generator

**From files:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

configMapGenerator:
- name: app-config
  files:
  - config.properties
  - app.yaml
```

**From literals:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
- name: app-config
  literals:
  - DATABASE_URL=postgres://localhost/db
  - API_KEY=secret123
  - LOG_LEVEL=info
```

**From env file:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
- name: app-config
  envs:
  - config.env
```

**With options:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

configMapGenerator:
- name: app-config
  files:
  - config.properties
  options:
    labels:
      app: myapp
    annotations:
      description: "Application configuration"
    disableNameSuffixHash: true
```

### 7.2 Secret Generator

**From files:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

secretGenerator:
- name: app-secret
  files:
  - secret.properties
```

**From literals:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

secretGenerator:
- name: app-secret
  literals:
  - username=admin
  - password=secret123
  type: Opaque
```

**From env file:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

secretGenerator:
- name: app-secret
  envs:
  - secrets.env
  type: Opaque
```

**With options:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

secretGenerator:
- name: app-secret
  literals:
  - password=secret123
  options:
    labels:
      app: myapp
    annotations:
      description: "Application secrets"
    disableNameSuffixHash: false
```

### 7.3 Using Generated Resources

**Reference in deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: nginx:latest
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
        volumeMounts:
        - name: config
          mountPath: /etc/config
      volumes:
      - name: config
        configMap:
          name: app-config
```

---

## 8. Image Transformations

### 8.1 Basic Image Transformation

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

images:
- name: nginx
  newName: myregistry/nginx
  newTag: v1.2.3
```

### 8.2 Multiple Images

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

images:
- name: nginx
  newName: myregistry/nginx
  newTag: v1.2.3
- name: redis
  newName: myregistry/redis
  newTag: 7.0
- name: postgres
  newName: myregistry/postgres
  newTag: 15-alpine
```

### 8.3 Image Digest

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

images:
- name: nginx
  newName: myregistry/nginx
  digest: sha256:abc123...
```

### 8.4 Image Name Only

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

images:
- name: nginx
  newTag: v1.2.3
```

---

## 9. Name Prefixes & Suffixes

### 9.1 Name Prefix

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

namePrefix: prod-
```

**Result:**
- `myapp` → `prod-myapp`
- `myapp-service` → `prod-myapp-service`

### 9.2 Name Suffix

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

nameSuffix: -v1
```

**Result:**
- `myapp` → `myapp-v1`
- `myapp-service` → `myapp-service-v1`

### 9.3 Combined Prefix and Suffix

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

namePrefix: prod-
nameSuffix: -v1
```

**Result:**
- `myapp` → `prod-myapp-v1`

---

## 10. Namespace Management

### 10.1 Setting Namespace

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

namespace: production
```

**All resources will have namespace set to `production`.**

### 10.2 Multi-Namespace Resources

**For resources that shouldn't have namespace (ClusterRole, etc.):**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- clusterrole.yaml

namespace: production

# ClusterRole won't get namespace
```

---

## 11. Common Labels & Annotations

### 11.1 Common Labels

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

commonLabels:
  app: myapp
  environment: production
  team: platform
  version: "1.0.0"
```

**Labels are added to all resources and selectors.**

### 11.2 Common Annotations

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

commonAnnotations:
  managed-by: kustomize
  description: "Production deployment"
  contact: "team@example.com"
```

### 11.3 Combined

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

commonLabels:
  app: myapp
  environment: production

commonAnnotations:
  managed-by: kustomize
  version: "1.0.0"
```

---

## 12. Replicas & Resource Management

### 12.1 Replica Override

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

replicas:
- name: myapp
  count: 5
```

**Original deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1  # Will be overridden to 5
```

### 12.2 Multiple Replicas

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- statefulset.yaml

replicas:
- name: myapp
  count: 3
- name: myapp-db
  count: 2
```

---

## 13. Multi-Environment Setups

### 13.1 Directory Structure

```
project/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patch.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patch.yaml
    └── prod/
        ├── kustomization.yaml
        └── patch.yaml
```

### 13.2 Base Configuration

**base/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- configmap.yaml

commonLabels:
  app: myapp
```

**base/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: nginx:latest
        ports:
        - containerPort: 80
        env:
        - name: ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: environment
```

**base/configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  environment: base
  log_level: info
```

### 13.3 Development Overlay

**overlays/dev/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: dev
namePrefix: dev-

replicas:
- name: myapp
  count: 1

images:
- name: nginx
  newTag: latest

configMapGenerator:
- name: app-config
  behavior: merge
  literals:
  - environment=development
  - log_level=debug

commonLabels:
  environment: dev
```

**overlays/dev/patch.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### 13.4 Production Overlay

**overlays/prod/kustomization.yaml:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base

namespace: production
namePrefix: prod-

replicas:
- name: myapp
  count: 5

images:
- name: nginx
  newName: myregistry/nginx
  newTag: v1.2.3

configMapGenerator:
- name: app-config
  behavior: merge
  literals:
  - environment=production
  - log_level=warn

commonLabels:
  environment: production

patchesStrategicMerge:
- patch.yaml
```

**overlays/prod/patch.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
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
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 13.5 Building Environments

```bash
# Build dev
kustomize build overlays/dev/

# Build staging
kustomize build overlays/staging/

# Build prod
kustomize build overlays/prod/

# Apply dev
kubectl apply -k overlays/dev/

# Apply prod
kubectl apply -k overlays/prod/
```

---

## 14. Advanced Patterns

### 14.1 Replacements

**Replace values across resources:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

replacements:
- source:
    kind: Service
    name: myapp
    fieldPath: spec.clusterIP
  targets:
  - select:
      kind: Deployment
      name: myapp
    fieldPaths:
    - spec.template.spec.containers.[name=myapp].env.[name=SERVICE_IP].value
```

### 14.2 Variable Substitution

**Using ConfigMap values:**
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml

configMapGenerator:
- name: app-config
  literals:
  - DATABASE_URL=postgres://localhost/db

replacements:
- source:
    kind: ConfigMap
    name: app-config
    fieldPath: data.DATABASE_URL
  targets:
  - select:
      kind: Deployment
    fieldPaths:
    - spec.template.spec.containers.[name=myapp].env.[name=DB_URL].value
```

### 14.3 Multiple Bases

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base/app
- ../../base/monitoring
- ../../base/logging

namespace: production
```

### 14.4 Conditional Resources

**Using different bases per environment:**
```yaml
# overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base/app
# No monitoring in dev

# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- ../../base/app
- ../../base/monitoring
- ../../base/logging
```

---

## 15. Kustomize with CI/CD

### 15.1 GitHub Actions

```yaml
name: Deploy with Kustomize

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup kubectl
      uses: azure/setup-kubectl@v3
      
    - name: Build kustomization
      run: |
        kustomize build overlays/prod/ > k8s-manifests.yaml
        
    - name: Validate manifests
      run: |
        kubectl apply --dry-run=client -f k8s-manifests.yaml
        
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -k overlays/prod/
      env:
        KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

### 15.2 GitLab CI/CD

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  image: bitnami/kubectl:latest
  script:
    - kustomize build overlays/prod/ > k8s-manifests.yaml
  artifacts:
    paths:
      - k8s-manifests.yaml

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -k overlays/prod/
  only:
    - main
```

### 15.3 ArgoCD Integration

**ArgoCD Application:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-manifests
    targetRevision: main
    path: overlays/prod
    kustomize: {}
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**ArgoCD automatically uses kustomize when it detects `kustomization.yaml`.**

### 15.4 Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'kustomize build overlays/prod/ > k8s-manifests.yaml'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'kubectl apply -k overlays/prod/'
            }
        }
    }
}
```

---

## 16. Kustomize vs Helm

### 16.1 Comparison

| Feature | Kustomize | Helm |
|---------|-----------|------|
| **Templating** | No | Yes (Go templates) |
| **Learning Curve** | Easy | Moderate |
| **Built-in kubectl** | Yes | No |
| **Package Management** | No | Yes (Charts) |
| **Dependencies** | No | Yes |
| **GitOps Friendly** | Excellent | Good |
| **Complexity** | Low | Medium-High |
| **Use Case** | Configuration management | Package distribution |

### 16.2 When to Use Kustomize

**Use Kustomize when:**
- ✅ You want template-free configuration
- ✅ Managing multiple environments
- ✅ Need GitOps-friendly approach
- ✅ Working with existing Kubernetes manifests
- ✅ Want simplicity

**Use Helm when:**
- ✅ Distributing applications as packages
- ✅ Need complex templating
- ✅ Managing dependencies
- ✅ Sharing charts with others

### 16.3 Using Both Together

**You can use Helm to generate base manifests and Kustomize to customize:**
```bash
# Generate base from Helm chart
helm template myapp ./chart > base/deployment.yaml

# Customize with Kustomize
kustomize build overlays/prod/
```

---

## 17. Best Practices

### 17.1 Directory Structure

```
project/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches/
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patches/
    └── prod/
        ├── kustomization.yaml
        └── patches/
```

### 17.2 Base Best Practices

- Keep bases generic and reusable
- Use minimal configuration in bases
- Document base purpose
- Version control bases separately if needed

### 17.3 Overlay Best Practices

- One overlay per environment
- Use patches for environment-specific changes
- Keep overlays minimal
- Use namePrefix/nameSuffix for isolation

### 17.4 Naming Conventions

```yaml
# Good
namePrefix: prod-
nameSuffix: -v1

# Avoid
namePrefix: production-environment-version-1-
```

### 17.5 Resource Organization

```yaml
# Group related resources
resources:
- deployments/
- services/
- configmaps/
- secrets/
```

### 17.6 Version Control

- Commit kustomization files to Git
- Tag releases
- Use GitOps workflows
- Review changes before applying

---

## 18. Troubleshooting

### 18.1 Common Issues

**Issue: Resources not found**
```bash
# Check if resources exist
kustomize build . | grep -A 5 "kind:"

# Verify paths in kustomization.yaml
cat kustomization.yaml
```

**Issue: Image not replaced**
```bash
# Check image name matches exactly
kustomize build . | grep image:

# Verify images section
cat kustomization.yaml | grep -A 3 images
```

**Issue: Namespace not applied**
```bash
# Check namespace in output
kustomize build . | grep namespace

# Verify namespace field
cat kustomization.yaml | grep namespace
```

### 18.2 Debugging Commands

```bash
# Build with verbose output
kustomize build . --load-restrictor LoadRestrictionsNone

# Validate YAML
kustomize build . | kubectl apply --dry-run=client -f -

# Compare before/after
kustomize build base/ > base.yaml
kustomize build overlays/prod/ > prod.yaml
diff base.yaml prod.yaml

# Check specific resource
kustomize build . | kubectl get -f - --dry-run=client -o yaml
```

### 18.3 Validation

```bash
# Validate kustomization file
kustomize build . --load-restrictor LoadRestrictionsNone

# Validate with kubectl
kustomize build . | kubectl apply --dry-run=client -f -

# Check for errors
kustomize build . 2>&1 | grep -i error
```

---

## Quick Reference

### Essential Commands

```bash
# Build
kustomize build .

# Build and apply
kubectl apply -k .

# Build and save
kustomize build . > output.yaml

# Validate
kustomize build . | kubectl apply --dry-run=client -f -

# Diff
kubectl diff -k .
```

### Common kustomization.yaml Structure

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

namespace: production
namePrefix: prod-

commonLabels:
  app: myapp
  environment: production

images:
- name: nginx
  newTag: v1.2.3

replicas:
- name: myapp
  count: 3

configMapGenerator:
- name: app-config
  literals:
  - key=value
```

---

## Conclusion

Kustomize is a powerful tool for managing Kubernetes configurations without templating complexity. It's perfect for:

- Multi-environment deployments
- GitOps workflows
- Configuration customization
- Reusable base configurations

**Key Takeaways:**
- ✅ Kustomize is built into kubectl
- ✅ Template-free approach
- ✅ Excellent for GitOps
- ✅ Great for multi-environment setups
- ✅ Simple and declarative

Master Kustomize to efficiently manage your Kubernetes configurations! 🚀

