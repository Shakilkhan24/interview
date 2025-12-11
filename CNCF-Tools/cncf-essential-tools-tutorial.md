# CNCF Essential Tools for DevOps Engineers
## Practical Guide to Kubernetes Addons & Cloud Native Tools

---

## Table of Contents

1. [CNCF Landscape Overview](#1-cncf-landscape-overview)
2. [Monitoring & Observability](#2-monitoring--observability)
   - Prometheus & Prometheus Operator
   - Grafana
   - Jaeger (Tracing)
3. [GitOps Tools](#3-gitops-tools)
   - ArgoCD
   - Flux
4. [Service Mesh](#4-service-mesh)
   - Istio
   - Linkerd
5. [Security Tools](#5-security-tools)
   - Falco (Runtime Security)
   - OPA Gatekeeper (Policy)
6. [Networking](#6-networking)
   - Cilium
7. [Storage](#7-storage)
   - Rook/Ceph
8. [CI/CD](#8-cicd)
   - Tekton
9. [Other Essential Tools](#9-other-essential-tools)
   - cert-manager
   - External Secrets Operator
   - Velero (Backup)

---

## 1. CNCF Landscape Overview

### 1.1 What is CNCF?

**Cloud Native Computing Foundation (CNCF)** hosts critical components of the global technology infrastructure.

**CNCF Projects Categories:**
- **Orchestration**: Kubernetes
- **Observability**: Prometheus, Grafana, Jaeger
- **Service Mesh**: Istio, Linkerd
- **Security**: Falco, OPA
- **Storage**: Rook, Longhorn
- **CI/CD**: Tekton, Argo
- **Networking**: Cilium, Calico

### 1.2 Essential Tools for DevOps

**Must-Know Tools:**
1. **Prometheus** - Metrics collection
2. **Grafana** - Visualization
3. **ArgoCD** - GitOps
4. **Istio/Linkerd** - Service mesh
5. **Falco** - Security monitoring
6. **OPA** - Policy enforcement
7. **cert-manager** - Certificate management
8. **Velero** - Backup/restore

---

## 2. Monitoring & Observability

### 2.1 Prometheus & Prometheus Operator

#### What is Prometheus?

**Prometheus** is a monitoring and alerting toolkit designed for reliability and scalability.

**Key Features:**
- Time-series database
- Pull-based metrics collection
- PromQL query language
- Alerting rules
- Service discovery

#### Installation with Prometheus Operator

**Using Helm:**
```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack (includes Prometheus, Grafana, Alertmanager)
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

**Verify Installation:**
```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring

# Access Prometheus UI
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open http://localhost:9090
```

#### ServiceMonitor (Scraping Metrics)

**Create ServiceMonitor to scrape application metrics:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

**Service with metrics port:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  ports:
  - name: http
    port: 8080
  - name: metrics
    port: 9090
  selector:
    app: myapp
```

#### PrometheusRule (Alerting)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  namespace: monitoring
spec:
  groups:
  - name: myapp.rules
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

#### Common PromQL Queries

```promql
# CPU usage
rate(container_cpu_usage_seconds_total[5m])

# Memory usage
container_memory_usage_bytes

# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Pod restarts
rate(kube_pod_container_status_restarts_total[15m])
```

---

### 2.2 Grafana

#### What is Grafana?

**Grafana** is an open-source analytics and visualization platform.

**Key Features:**
- Beautiful dashboards
- Multiple data sources (Prometheus, Loki, etc.)
- Alerting
- Template variables

#### Installation

**Already included in kube-prometheus-stack, or install separately:**
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana \
  --namespace monitoring \
  --create-namespace \
  --set adminPassword=admin
```

**Access Grafana:**
```bash
# Get admin password
kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 -d

# Port forward
kubectl port-forward -n monitoring svc/grafana 3000:80
# Open http://localhost:3000 (admin/admin-password)
```

#### Creating Dashboards

**Dashboard ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "MyApp Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [{
              "expr": "rate(http_requests_total[5m])"
            }]
          },
          {
            "title": "Error Rate",
            "type": "graph",
            "targets": [{
              "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
            }]
          }
        ]
      }
    }
```

---

### 2.3 Jaeger (Distributed Tracing)

#### What is Jaeger?

**Jaeger** is a distributed tracing system for microservices.

#### Installation

```bash
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace monitoring \
  --create-namespace
```

**Access Jaeger UI:**
```bash
kubectl port-forward -n monitoring svc/jaeger-query 16686:16686
# Open http://localhost:16686
```

#### Instrumenting Applications

**Add Jaeger client to application:**
```python
# Python example
from jaeger_client import Config

def init_tracer(service):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
        },
        service_name=service,
    )
    return config.initialize_tracer()

tracer = init_tracer('myapp')
```

---

## 3. GitOps Tools

### 3.1 ArgoCD

#### What is ArgoCD?

**ArgoCD** is a declarative GitOps continuous delivery tool for Kubernetes.

**Key Features:**
- Automatic sync from Git
- Web UI
- Multi-cluster support
- RBAC integration

#### Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Open https://localhost:8080 (admin/password)
```

#### Creating Applications

**Application Manifest:**
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
    path: apps/myapp
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

**Apply:**
```bash
kubectl apply -f application.yaml
```

#### CLI Usage

```bash
# Install ArgoCD CLI
brew install argocd  # macOS
# or download from https://github.com/argoproj/argo-cd/releases

# Login
argocd login localhost:8080

# List applications
argocd app list

# Get application status
argocd app get myapp

# Sync application
argocd app sync myapp

# Delete application
argocd app delete myapp
```

---

### 3.2 Flux

#### What is Flux?

**Flux** is a GitOps tool that automatically keeps clusters in sync with Git repositories.

#### Installation

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Install Flux in cluster
flux install --namespace=flux-system

# Verify
kubectl get pods -n flux-system
```

#### Creating GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: GitRepository
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/myorg/k8s-manifests
  ref:
    branch: main
```

#### Creating Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps/myapp
  prune: true
  sourceRef:
    kind: GitRepository
    name: myapp
  targetNamespace: production
```

**Apply:**
```bash
kubectl apply -f gitrepository.yaml
kubectl apply -f kustomization.yaml

# Check status
flux get kustomizations
```

---

## 4. Service Mesh

### 4.1 Istio

#### What is Istio?

**Istio** is a service mesh that provides traffic management, security, and observability.

**Key Features:**
- Traffic management (routing, load balancing)
- Security (mTLS, RBAC)
- Observability (metrics, logs, traces)

#### Installation

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# Install Istio
istioctl install --set profile=default

# Verify
kubectl get pods -n istio-system
```

#### Enable Istio Sidecar Injection

**Automatic injection (namespace label):**
```bash
kubectl label namespace production istio-injection=enabled
```

**Manual injection:**
```bash
istioctl kube-inject -f deployment.yaml | kubectl apply -f -
```

#### VirtualService (Traffic Routing)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: myapp
        subset: v2
      weight: 100
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10
```

#### DestinationRule

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

#### Enable mTLS

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

---

### 4.2 Linkerd

#### What is Linkerd?

**Linkerd** is a lightweight service mesh focused on simplicity and performance.

#### Installation

```bash
# Install Linkerd CLI
curl -sL https://run.linkerd.io/install | sh

# Install Linkerd
linkerd install | kubectl apply -f -

# Verify
linkerd check

# Install Viz (observability)
linkerd viz install | kubectl apply -f -
```

#### Access Dashboard

```bash
linkerd viz dashboard
```

#### Automatic Injection

```bash
# Annotate namespace
kubectl annotate namespace production linkerd.io/inject=enabled

# Or annotate deployment
kubectl annotate deployment myapp linkerd.io/inject=enabled
```

---

## 5. Security Tools

### 5.1 Falco (Runtime Security)

#### What is Falco?

**Falco** is a runtime security tool that detects anomalous activity.

#### Installation

```bash
# Install Falco using Helm
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco \
  --create-namespace
```

#### Custom Rules

```yaml
# falco-rules.yaml
- rule: Write below binary dir
  desc: Detect writes to binary directories
  condition: >
    bin_dir and evt.dir = < and open_write
  output: >
    File below a known binary directory opened for writing
    (user=%user.name command=%proc.cmdline file=%fd.name)
  priority: ERROR
  tags: [filesystem, mitre_persistence]
```

**Apply custom rules:**
```bash
kubectl create configmap falco-rules -n falco --from-file=falco-rules.yaml
```

#### Viewing Falco Events

```bash
# View Falco events
kubectl logs -n falco -l app=falco

# Or use Falco Sidekick to send to external systems
```

---

### 5.2 OPA Gatekeeper (Policy)

#### What is OPA Gatekeeper?

**OPA Gatekeeper** enforces policies on Kubernetes resources using Open Policy Agent.

#### Installation

```bash
# Install Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# Verify
kubectl get pods -n gatekeeper-system
```

#### Creating Constraints

**ConstraintTemplate:**
```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        type: object
        properties:
          labels:
            type: array
            items:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
```

**Constraint:**
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-team-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["team"]
```

**Apply:**
```bash
kubectl apply -f constrainttemplate.yaml
kubectl apply -f constraint.yaml

# Test (should fail without team label)
kubectl create deployment test --image=nginx
```

---

## 6. Networking

### 6.1 Cilium

#### What is Cilium?

**Cilium** is a networking, observability, and security solution with eBPF-based dataplane.

**Key Features:**
- eBPF-based networking
- Network policies
- Service mesh (Cilium Service Mesh)
- Observability

#### Installation

```bash
# Install Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/master/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Install Cilium
cilium install

# Verify
cilium status
cilium connectivity test
```

#### Network Policies

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
```

---

## 7. Storage

### 7.1 Rook/Ceph

#### What is Rook?

**Rook** is a cloud-native storage orchestrator that turns storage software into self-managing services.

#### Installation

```bash
# Install Rook Operator
kubectl apply -f https://raw.githubusercontent.com/rook/rook/release-1.12/deploy/examples/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/rook/rook/release-1.12/deploy/examples/common.yaml
kubectl apply -f https://raw.githubusercontent.com/rook/rook/release-1.12/deploy/examples/operator.yaml

# Create Ceph Cluster
kubectl apply -f https://raw.githubusercontent.com/rook/rook/release-1.12/deploy/examples/cluster.yaml

# Create StorageClass
kubectl apply -f https://raw.githubusercontent.com/rook/rook/release-1.12/deploy/examples/csi/cephfs/storageclass.yaml
```

#### Using Rook Storage

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
spec:
  storageClassName: rook-cephfs
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

---

## 8. CI/CD

### 8.1 Tekton

#### What is Tekton?

**Tekton** is a cloud-native CI/CD framework for Kubernetes.

#### Installation

```bash
# Install Tekton Pipelines
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# Install Tekton CLI
# macOS
brew install tektoncd-cli

# Linux
curl -LO https://github.com/tektoncd/cli/releases/download/v0.32.0/tkn_0.32.0_Linux_x86_64.tar.gz
sudo tar xvzf tkn_0.32.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn
```

#### Creating a Pipeline

**Task:**
```yaml
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: build
spec:
  steps:
  - name: build
    image: docker:latest
    script: |
      #!/bin/sh
      docker build -t myapp:$IMAGE_TAG .
      docker push myapp:$IMAGE_TAG
    env:
    - name: IMAGE_TAG
      value: "v1.0.0"
```

**Pipeline:**
```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: build-and-deploy
spec:
  params:
  - name: image-tag
  tasks:
  - name: build
    taskRef:
      name: build
    params:
    - name: IMAGE_TAG
      value: $(params.image-tag)
  - name: deploy
    taskRef:
      name: deploy
    runAfter:
    - build
```

**PipelineRun:**
```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: build-and-deploy-run
spec:
  pipelineRef:
    name: build-and-deploy
  params:
  - name: image-tag
    value: v1.0.0
```

**Apply and run:**
```bash
kubectl apply -f task.yaml
kubectl apply -f pipeline.yaml
kubectl apply -f pipelinerun.yaml

# Watch
tkn pipelinerun logs build-and-deploy-run -f
```

---

## 9. Other Essential Tools

### 9.1 cert-manager

#### What is cert-manager?

**cert-manager** automatically manages TLS certificates in Kubernetes.

#### Installation

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Verify
kubectl get pods -n cert-manager
```

#### Creating Certificates

**ClusterIssuer (Let's Encrypt):**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

**Certificate:**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
spec:
  secretName: myapp-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - myapp.example.com
```

**Use in Ingress:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

---

### 9.2 External Secrets Operator

#### What is ESO?

**External Secrets Operator** integrates external secret management systems with Kubernetes.

#### Installation

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets \
  external-secrets/external-secrets \
  -n external-secrets-system \
  --create-namespace
```

#### Creating SecretStore

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
```

#### Creating ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: myapp/database/url
  - secretKey: api-key
    remoteRef:
      key: myapp/api/key
```

---

### 9.3 Velero (Backup)

#### What is Velero?

**Velero** backs up and restores Kubernetes cluster resources and persistent volumes.

#### Installation

```bash
# Install Velero CLI
# macOS
brew install velero

# Download from https://github.com/vmware-tanzu/velero/releases

# Install Velero (example with AWS S3)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.7.0 \
  --bucket my-backup-bucket \
  --secret-file ./credentials-velero \
  --use-volume-snapshots=false
```

#### Creating Backups

```bash
# Backup entire cluster
velero backup create cluster-backup

# Backup specific namespace
velero backup create myapp-backup --include-namespaces production

# Backup with schedule
velero schedule create daily-backup --schedule="0 2 * * *" --ttl 72h0m0s

# List backups
velero backup get

# Restore
velero restore create --from-backup cluster-backup
```

---

## Quick Reference

### Installation Commands

```bash
# Prometheus Stack
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Istio
istioctl install --set profile=default

# Linkerd
linkerd install | kubectl apply -f -

# Falco
helm install falco falcosecurity/falco -n falco --create-namespace

# OPA Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# Cilium
cilium install

# cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# External Secrets
helm install external-secrets external-secrets/external-secrets -n external-secrets-system --create-namespace

# Velero
velero install --provider aws --bucket my-backup-bucket
```

### Essential Resources

- **CNCF Landscape**: https://landscape.cncf.io/
- **Prometheus**: https://prometheus.io/docs/
- **ArgoCD**: https://argo-cd.readthedocs.io/
- **Istio**: https://istio.io/latest/docs/
- **Falco**: https://falco.org/docs/
- **OPA**: https://www.openpolicyagent.org/docs/latest/

---

## Best Practices

1. **Start Simple**: Begin with Prometheus/Grafana for monitoring
2. **GitOps First**: Use ArgoCD or Flux for deployments
3. **Security Early**: Implement Falco and OPA from the start
4. **Service Mesh When Needed**: Don't add Istio/Linkerd unless you need their features
5. **Automate Certificates**: Always use cert-manager for TLS
6. **Backup Regularly**: Set up Velero for disaster recovery
7. **Monitor Everything**: Use ServiceMonitors for all applications
8. **Policy as Code**: Use OPA for policy enforcement

---

## Conclusion

These CNCF tools form the foundation of a modern Kubernetes platform:

- **Monitoring**: Prometheus + Grafana
- **GitOps**: ArgoCD or Flux
- **Security**: Falco + OPA
- **Networking**: Cilium or Calico
- **Storage**: Rook or cloud storage
- **CI/CD**: Tekton or Argo Workflows
- **Utilities**: cert-manager, ESO, Velero

Master these tools to build production-ready Kubernetes platforms! 🚀

