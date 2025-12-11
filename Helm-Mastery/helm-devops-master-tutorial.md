# Helm Master Tutorial - Complete DevOps Guide
## Kubernetes Package Manager: From Basics to Production

---

## Table of Contents

### Part I: Helm Fundamentals & CLI
1. [Helm Fundamentals](#1-helm-fundamentals)
2. [Installation & Setup](#2-installation--setup)
3. [Helm CLI Commands](#3-helm-cli-commands)
4. [Understanding Charts](#4-understanding-charts)
5. [Chart Structure & Templates](#5-chart-structure--templates)
6. [Values & Configuration](#6-values--configuration)
7. [Releases & Release Management](#7-releases--release-management)
8. [Repositories](#8-repositories)

### Part II: Advanced Helm Features
9. [Template Functions & Pipelines](#9-template-functions--pipelines)
10. [Hooks & Lifecycle Management](#10-hooks--lifecycle-management)
11. [Dependencies & Subcharts](#11-dependencies--subcharts)
12. [Chart Testing & Validation](#12-chart-testing--validation)
13. [Helm Plugins](#13-helm-plugins)
14. [Helm 3 vs Helm 2](#14-helm-3-vs-helm-2)

### Part III: DevOps Integration
15. [Helm with CI/CD Pipelines](#15-helm-with-cicd-pipelines)
16. [Helm with GitOps (ArgoCD)](#16-helm-with-gitops-argocd)
17. [Helm with Terraform](#17-helm-with-terraform)
18. [Helm with Monitoring & Observability](#18-helm-with-monitoring--observability)
19. [Helm Security Best Practices](#19-helm-security-best-practices)
20. [Helm in Multi-Environment Deployments](#20-helm-in-multi-environment-deployments)
21. [Helm Chart Development Workflow](#21-helm-chart-development-workflow)
22. [Troubleshooting & Best Practices](#22-troubleshooting--best-practices)

---

## Part I: Helm Fundamentals & CLI

### 1. Helm Fundamentals

#### 1.1 What is Helm?

**Helm** is the **package manager for Kubernetes** - think of it like:
- **apt/yum** for Linux packages
- **npm** for Node.js packages
- **pip** for Python packages
- But for Kubernetes applications

**Key Concepts:**

- **Chart**: A Helm package containing all Kubernetes resources needed to run an application
- **Release**: An instance of a chart running in a Kubernetes cluster
- **Repository**: A collection of charts (like a package repository)
- **Template**: Kubernetes manifest files with placeholders for values

#### 1.2 Why Use Helm?

**Without Helm:**
```bash
# Deploying an application requires:
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f ingress.yaml

# For each environment, you need different files
# No easy way to version or rollback
# Hard to share configurations
```

**With Helm:**
```bash
# Single command for all environments
helm install myapp ./my-chart --set environment=production
helm install myapp ./my-chart --set environment=staging

# Easy upgrades and rollbacks
helm upgrade myapp ./my-chart
helm rollback myapp 1
```

**Benefits:**
- ✅ **Simplified Deployment**: One command to deploy complex applications
- ✅ **Configuration Management**: Easy customization via values
- ✅ **Versioning**: Track application versions
- ✅ **Rollback**: Easy rollback to previous versions
- ✅ **Sharing**: Share charts via repositories
- ✅ **Dependencies**: Manage application dependencies
- ✅ **Reusability**: Create reusable chart templates

#### 1.3 How Helm Works

```
┌─────────────────┐
│  Helm Chart     │  (Template files + values)
│  (myapp/)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  helm install   │  (Render templates)
│  helm upgrade   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Kubernetes     │  (Deployed resources)
│  Resources      │
└─────────────────┘
```

**Helm Architecture:**

```
┌─────────────────────────────────────┐
│         Helm Client                 │
│  (helm CLI on your machine)         │
└──────────────┬──────────────────────┘
               │
               │ kubectl API
               │
┌──────────────▼──────────────────────┐
│    Kubernetes API Server            │
│                                      │
│  ┌──────────────────────────────┐  │
│  │   Helm Releases (Secrets)     │  │
│  │   (Helm 3 stores in cluster) │  │
│  └──────────────────────────────┘  │
│                                      │
│  ┌──────────────────────────────┐  │
│  │   Application Resources      │  │
│  │   (Deployments, Services)   │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

#### 1.4 Helm 3 vs Helm 2

**Key Differences:**

| Feature | Helm 2 | Helm 3 |
|---------|--------|--------|
| **Tiller** | Required (server-side) | Removed |
| **Release Storage** | ConfigMaps/Secrets | Secrets only |
| **Security** | RBAC issues | Better security |
| **Chart Dependencies** | requirements.yaml | Chart.yaml dependencies |
| **Library Charts** | No | Yes |
| **OCI Support** | No | Yes |

**Helm 3 is the current version** (Helm 2 is deprecated)

---

### 2. Installation & Setup

#### 2.1 Installing Helm

**Linux/macOS (Script):**
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Linux (Manual):**
```bash
# Download latest version
wget https://get.helm.sh/helm-v3.13.0-linux-amd64.tar.gz

# Extract
tar -zxvf helm-v3.13.0-linux-amd64.tar.gz

# Move to PATH
sudo mv linux-amd64/helm /usr/local/bin/helm

# Verify
helm version
```

**macOS (Homebrew):**
```bash
brew install helm
```

**Windows (Chocolatey):**
```bash
choco install kubernetes-helm
```

**Windows (Scoop):**
```bash
scoop install helm
```

#### 2.2 Verify Installation

```bash
# Check version
helm version

# Output:
# version.BuildInfo{Version:"v3.13.0", GitCommit:"...", GoVersion:"go1.21.0"}
```

#### 2.3 Initial Setup

```bash
# Add stable repository (if needed)
helm repo add stable https://charts.helm.sh/stable

# Update repository
helm repo update

# List repositories
helm repo list

# Search for charts
helm search repo stable
```

#### 2.4 Kubernetes Cluster Access

```bash
# Helm uses kubectl configuration
# Make sure kubectl is configured

# Check cluster access
kubectl cluster-info

# Check current context
kubectl config current-context

# List contexts
kubectl config get-contexts

# Switch context
kubectl config use-context my-cluster
```

---

### 3. Helm CLI Commands

#### 3.1 Repository Commands

```bash
# Add a repository
helm repo add <name> <url>
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# List repositories
helm repo list

# Update repositories
helm repo update

# Remove repository
helm repo remove <name>

# Search in repositories
helm search repo <keyword>
helm search repo nginx
helm search repo mysql

# Search with version
helm search repo nginx --versions
```

#### 3.2 Chart Commands

```bash
# Create a new chart
helm create <chart-name>
helm create myapp

# Package a chart
helm package <chart-path>
helm package ./myapp

# Show chart information
helm show chart <chart>
helm show chart stable/nginx

# Show chart values
helm show values <chart>
helm show values stable/nginx

# Show all chart files
helm show all <chart>

# Lint a chart
helm lint <chart-path>
helm lint ./myapp

# Template a chart (dry-run)
helm template <release-name> <chart> [flags]
helm template myapp ./myapp
helm template myapp ./myapp --set image.tag=v2.0.0

# Get manifest (what would be installed)
helm get manifest <release-name>
```

#### 3.3 Install Commands

```bash
# Install a chart
helm install <release-name> <chart> [flags]
helm install myapp stable/nginx

# Install with values file
helm install myapp ./myapp -f values.yaml

# Install with custom values
helm install myapp ./myapp --set key=value
helm install myapp ./myapp --set image.tag=v2.0.0,replicaCount=3

# Install with multiple value files
helm install myapp ./myapp -f values.yaml -f production.yaml

# Install in specific namespace
helm install myapp ./myapp --namespace production --create-namespace

# Install with dry-run (simulate)
helm install myapp ./myapp --dry-run --debug

# Install with atomic (rollback on failure)
helm install myapp ./myapp --atomic

# Install and wait for deployment
helm install myapp ./myapp --wait --timeout 5m
```

#### 3.4 Upgrade Commands

```bash
# Upgrade a release
helm upgrade <release-name> <chart> [flags]
helm upgrade myapp ./myapp

# Upgrade with values
helm upgrade myapp ./myapp -f values.yaml

# Upgrade with set
helm upgrade myapp ./myapp --set image.tag=v2.0.0

# Upgrade and wait
helm upgrade myapp ./myapp --wait

# Upgrade with atomic (rollback on failure)
helm upgrade myapp ./myapp --atomic

# Upgrade with history limit
helm upgrade myapp ./myapp --history-max 10

# Upgrade with force (recreate resources)
helm upgrade myapp ./myapp --force
```

#### 3.5 Rollback Commands

```bash
# List release history
helm history <release-name>
helm history myapp

# Rollback to previous version
helm rollback <release-name>
helm rollback myapp

# Rollback to specific revision
helm rollback <release-name> <revision>
helm rollback myapp 3

# Rollback with wait
helm rollback myapp --wait
```

#### 3.6 List & Status Commands

```bash
# List all releases
helm list
helm ls

# List in all namespaces
helm list --all-namespaces
helm list -A

# List with output format
helm list -o json
helm list -o yaml
helm list -o table

# Get release status
helm status <release-name>
helm status myapp

# Get release values
helm get values <release-name>
helm get values myapp

# Get all release information
helm get all <release-name>
```

#### 3.7 Uninstall Commands

```bash
# Uninstall a release
helm uninstall <release-name>
helm uninstall myapp

# Uninstall and keep history
helm uninstall myapp --keep-history

# Uninstall with wait
helm uninstall myapp --wait
```

#### 3.8 Dependency Commands

```bash
# Update chart dependencies
helm dependency update <chart-path>
helm dependency update ./myapp

# Build dependencies
helm dependency build <chart-path>

# List dependencies
helm dependency list <chart-path>
```

#### 3.9 Test Commands

```bash
# Run chart tests
helm test <release-name>
helm test myapp

# Test with cleanup
helm test myapp --cleanup
```

#### 3.10 Plugin Commands

```bash
# List plugins
helm plugin list

# Install plugin
helm plugin install <plugin-url>
helm plugin install https://github.com/databus23/helm-diff

# Update plugin
helm plugin update <plugin-name>

# Uninstall plugin
helm plugin uninstall <plugin-name>
```

---

### 4. Understanding Charts

#### 4.1 What is a Chart?

A **Chart** is a collection of files that describe a related set of Kubernetes resources. It's like a package that contains:
- Kubernetes manifests (templates)
- Default configuration values
- Metadata about the chart
- Dependencies on other charts

#### 4.2 Chart Structure

```
myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── _helpers.tpl    # Helper templates
├── charts/             # Chart dependencies (downloaded)
├── crds/               # Custom Resource Definitions
└── README.md           # Chart documentation
```

#### 4.3 Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for My Application
type: application
version: 1.0.0
appVersion: "2.0.0"
keywords:
  - web
  - application
home: https://github.com/myorg/myapp
sources:
  - https://github.com/myorg/myapp
maintainers:
  - name: John Doe
    email: john@example.com
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

**Key Fields:**
- `apiVersion`: Chart API version (v2 for Helm 3)
- `name`: Chart name
- `version`: Chart version (SemVer)
- `appVersion`: Application version
- `type`: `application` or `library`
- `dependencies`: Chart dependencies

#### 4.4 Creating Your First Chart

```bash
# Create a new chart
helm create myapp

# This creates:
# myapp/
# ├── Chart.yaml
# ├── values.yaml
# ├── .helmignore
# ├── templates/
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── ingress.yaml
# │   ├── hpa.yaml
# │   ├── serviceaccount.yaml
# │   ├── _helpers.tpl
# │   └── tests/
# │       └── test-connection.yaml
# └── charts/
```

#### 4.5 Chart Types

**Application Chart:**
```yaml
type: application
```
- Deploys an application
- Can be installed
- Most common type

**Library Chart:**
```yaml
type: library
```
- Provides reusable templates
- Cannot be installed
- Used by other charts
- Example: Common templates, utilities

---

### 5. Chart Structure & Templates

#### 5.1 Template Files

Templates are Kubernetes manifest files with Go template syntax. Helm renders them with values to create actual Kubernetes resources.

**Example Template (deployment.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.port }}
        env:
        {{- range .Values.env }}
        - name: {{ .name }}
          value: {{ .value | quote }}
        {{- end }}
```

#### 5.2 Template Syntax

**Variables:**
```yaml
# Access values
{{ .Values.replicaCount }}

# Access chart metadata
{{ .Chart.Name }}
{{ .Chart.Version }}

# Access release information
{{ .Release.Name }}
{{ .Release.Namespace }}

# Access template context
{{ . }}
```

**Functions:**
```yaml
# Default value
{{ .Values.image.tag | default "latest" }}

# Quote string
{{ .Values.name | quote }}

# Upper/Lower case
{{ .Values.name | upper }}
{{ .Values.name | lower }}

# Indentation
{{- include "mychart.labels" . | nindent 4 }}

# Conditional
{{- if .Values.enabled }}
# content
{{- end }}

# Range (loops)
{{- range .Values.items }}
- {{ . }}
{{- end }}
```

**Control Structures:**
```yaml
# If/Else
{{- if .Values.enabled }}
enabled: true
{{- else }}
enabled: false
{{- end }}

# With (scope)
{{- with .Values.image }}
image: {{ .repository }}:{{ .tag }}
{{- end }}

# Range
{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value }}
{{- end }}
```

#### 5.3 Helper Templates (_helpers.tpl)

Helper templates are reusable template snippets:

```yaml
{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Chart name and version
*/}}
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Full name
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```

**Using Helpers:**
```yaml
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
```

#### 5.4 Common Template Files

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "myapp.selectorLabels" . | nindent 4 }}
```

**configmap.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "myapp.fullname" . }}-config
data:
  config.yaml: |
    {{- .Values.config | toYaml | nindent 4 }}
```

**ingress.yaml:**
```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "myapp.fullname" . }}
  annotations:
    {{- toYaml .Values.ingress.annotations | nindent 4 }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  rules:
  {{- range .Values.ingress.hosts }}
  - host: {{ .host | quote }}
    http:
      paths:
      {{- range .paths }}
      - path: {{ .path }}
        pathType: {{ .pathType }}
        backend:
          service:
            name: {{ include "myapp.fullname" $ }}
            port:
              number: {{ $.Values.service.port }}
      {{- end }}
  {{- end }}
{{- end }}
```

---

### 6. Values & Configuration

#### 6.1 Values File Structure

**values.yaml:**
```yaml
# Default values
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources: {}
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

env: []
  # - name: DATABASE_URL
  #   value: "postgresql://..."
```

#### 6.2 Using Values in Templates

```yaml
# Access nested values
{{ .Values.image.repository }}
{{ .Values.image.tag }}

# With default
{{ .Values.replicaCount | default 1 }}

# Conditional
{{- if .Values.ingress.enabled }}
# ingress resources
{{- end }}
```

#### 6.3 Overriding Values

**Command Line:**
```bash
# Single value
helm install myapp ./myapp --set replicaCount=3

# Multiple values
helm install myapp ./myapp --set replicaCount=3,image.tag=v2.0.0

# Nested values
helm install myapp ./myapp --set image.repository=myregistry/myapp

# Array values
helm install myapp ./myapp --set env[0].name=DB_HOST,env[0].value=localhost

# File values
helm install myapp ./myapp -f values.yaml

# Multiple files (later files override earlier)
helm install myapp ./myapp -f values.yaml -f production.yaml
```

**Values File (production.yaml):**
```yaml
replicaCount: 5

image:
  repository: myregistry/myapp
  tag: "v2.0.0"

ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

#### 6.4 Environment-Specific Values

**Structure:**
```
myapp/
├── Chart.yaml
├── values.yaml          # Default values
├── values-dev.yaml      # Development overrides
├── values-staging.yaml  # Staging overrides
├── values-prod.yaml     # Production overrides
└── templates/
```

**Usage:**
```bash
# Development
helm install myapp ./myapp -f values.yaml -f values-dev.yaml

# Staging
helm install myapp ./myapp -f values.yaml -f values-staging.yaml

# Production
helm install myapp ./myapp -f values.yaml -f values-prod.yaml
```

#### 6.5 Value Validation

**Using required:**
```yaml
# In template
image: "{{ required "image.repository is required" .Values.image.repository }}:{{ .Values.image.tag }}"
```

**Using fail:**
```yaml
{{- if not .Values.database.host }}
{{- fail "database.host is required" }}
{{- end }}
```

---

### 7. Releases & Release Management

#### 7.1 What is a Release?

A **Release** is an instance of a chart deployed to a Kubernetes cluster. Each time you install a chart, it creates a new release.

**Release Components:**
- **Name**: Unique identifier for the release
- **Namespace**: Kubernetes namespace where resources are deployed
- **Revision**: Version number of the release
- **Status**: Current state (deployed, failed, pending, etc.)
- **Chart**: Chart used for the release
- **Values**: Configuration values used

#### 7.2 Release Lifecycle

```
Install → Deployed → Upgrade → Deployed → Rollback → Deployed → Uninstall
```

#### 7.3 Managing Releases

**List Releases:**
```bash
# Current namespace
helm list

# All namespaces
helm list --all-namespaces

# Output format
helm list -o json
helm list -o yaml
```

**Get Release Information:**
```bash
# Status
helm status myapp

# Values used
helm get values myapp

# Manifest (all resources)
helm get manifest myapp

# Notes (chart notes)
helm get notes myapp

# All information
helm get all myapp
```

**Release History:**
```bash
# View history
helm history myapp

# Output:
# REVISION  UPDATED                  STATUS      CHART         APP VERSION DESCRIPTION
# 1         Mon Jan 15 10:00:00 2024 deployed    myapp-1.0.0   2.0.0       Install complete
# 2         Mon Jan 15 11:00:00 2024 deployed    myapp-1.1.0   2.1.0       Upgrade complete
# 3         Mon Jan 15 12:00:00 2024 superseded  myapp-1.1.0   2.1.0       Upgrade complete
```

#### 7.4 Release Storage (Helm 3)

Helm 3 stores release information in Kubernetes Secrets:

```bash
# View release secret
kubectl get secret -n <namespace> sh.helm.release.v1.<release-name>.v<revision>

# Example
kubectl get secret -n default sh.helm.release.v1.myapp.v1
```

**Release Secret Structure:**
- Contains release metadata
- Contains rendered templates
- Contains values used
- Encrypted (base64 encoded)

#### 7.5 Release Statuses

- **deployed**: Successfully deployed
- **failed**: Deployment failed
- **pending-install**: Installation in progress
- **pending-upgrade**: Upgrade in progress
- **pending-rollback**: Rollback in progress
- **superseded**: Replaced by newer revision
- **uninstalling**: Uninstallation in progress
- **uninstalled**: Successfully uninstalled

---

### 8. Repositories

#### 8.1 What is a Repository?

A **Repository** is a collection of Helm charts, similar to:
- Docker registry (for images)
- npm registry (for packages)
- Maven repository (for Java artifacts)

#### 8.2 Public Repositories

**Popular Repositories:**

```bash
# Bitnami (most popular)
helm repo add bitnami https://charts.bitnami.com/bitnami

# Prometheus Community
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Jetstack (cert-manager)
helm repo add jetstack https://charts.jetstack.io

# Grafana
helm repo add grafana https://grafana.github.io/helm-charts

# Elastic
helm repo add elastic https://helm.elastic.co

# HashiCorp
helm repo add hashicorp https://helm.releases.hashicorp.com
```

#### 8.3 Managing Repositories

```bash
# Add repository
helm repo add <name> <url>
helm repo add myrepo https://charts.example.com

# List repositories
helm repo list

# Update repositories
helm repo update

# Remove repository
helm repo remove <name>

# Search in repositories
helm search repo <keyword>
helm search repo nginx
helm search repo mysql --versions
```

#### 8.4 Creating Your Own Repository

**Option 1: GitHub Pages**

```bash
# Package charts
helm package ./myapp
helm package ./otherapp

# Create index
helm repo index . --url https://myorg.github.io/helm-charts/

# Push to GitHub
git add .
git commit -m "Add charts"
git push

# Add repository
helm repo add mycharts https://myorg.github.io/helm-charts/
```

**Option 2: ChartMuseum**

```bash
# Install ChartMuseum
helm repo add chartmuseum https://chartmuseum.github.io/charts
helm install chartmuseum chartmuseum/chartmuseum

# Upload chart
curl --data-binary "@myapp-1.0.0.tgz" http://chartmuseum:8080/api/charts

# Add repository
helm repo add chartmuseum http://chartmuseum:8080
```

**Option 3: OCI Registry**

```bash
# Login to OCI registry
helm registry login myregistry.io

# Push chart
helm push myapp-1.0.0.tgz oci://myregistry.io/charts

# Install from OCI
helm install myapp oci://myregistry.io/charts/myapp --version 1.0.0
```

#### 8.5 Repository Index

The `index.yaml` file contains metadata about all charts:

```yaml
apiVersion: v1
entries:
  myapp:
  - apiVersion: v2
    appVersion: "2.0.0"
    created: "2024-01-15T10:00:00Z"
    description: My Application
    digest: abc123...
    name: myapp
    type: application
    urls:
    - myapp-1.0.0.tgz
    version: 1.0.0
  - apiVersion: v2
    appVersion: "2.1.0"
    created: "2024-01-16T10:00:00Z"
    description: My Application
    digest: def456...
    name: myapp
    type: application
    urls:
    - myapp-1.1.0.tgz
    version: 1.1.0
generated: "2024-01-16T10:00:00Z"
```

---

## Part II: Advanced Helm Features

### 9. Template Functions & Pipelines

#### 9.1 String Functions

```yaml
# Quote
{{ .Values.name | quote }}

# Upper/Lower
{{ .Values.name | upper }}
{{ .Values.name | lower }}

# Title
{{ .Values.name | title }}

# Trim
{{ .Values.name | trim }}
{{ .Values.name | trimPrefix "app-" }}
{{ .Values.name | trimSuffix "-app" }}

# Replace
{{ .Values.name | replace "-" "_" }}

# Truncate
{{ .Values.name | trunc 10 }}

# Contains
{{- if contains "prod" .Values.environment }}
# production config
{{- end }}

# HasPrefix/HasSuffix
{{- if hasPrefix "app-" .Values.name }}
# name starts with app-
{{- end }}
```

#### 9.2 Math Functions

```yaml
# Add
{{ add .Values.replicas 1 }}

# Subtract
{{ sub .Values.replicas 1 }}

# Multiply
{{ mul .Values.replicas 2 }}

# Divide
{{ div .Values.total 2 }}

# Modulo
{{ mod .Values.number 2 }}

# Max/Min
{{ max .Values.replicas 3 }}
{{ min .Values.replicas 5 }}
```

#### 9.3 List Functions

```yaml
# First/Last
{{ first .Values.items }}
{{ last .Values.items }}

# Has/HasAny
{{- if has .Values.list "item" }}
# list contains item
{{- end }}

# Index
{{ index .Values.list 0 }}

# Uniq
{{ .Values.items | uniq }}

# Sort
{{ .Values.items | sortAlpha }}
```

#### 9.4 Date Functions

```yaml
# Now
{{ now }}

# Date format
{{ now | date "2006-01-02" }}

# Unix timestamp
{{ now | unixEpoch }}
```

#### 9.5 Type Conversion

```yaml
# To string
{{ .Values.number | toString }}

# To int
{{ .Values.string | int }}

# To float
{{ .Values.string | float64 }}

# To bool
{{ .Values.string | bool }}
```

#### 9.6 Pipeline Functions

```yaml
# Chaining functions
{{ .Values.name | upper | quote | trunc 10 }}

# Default in pipeline
{{ .Values.image.tag | default "latest" | quote }}

# Conditional pipeline
{{- if .Values.enabled }}
{{ .Values.name | upper }}
{{- end }}
```

#### 9.7 Advanced Functions

```yaml
# ToYaml/FromYaml
{{ .Values.config | toYaml | nindent 4 }}
{{ .Values.yamlString | fromYaml }}

# ToJson/FromJson
{{ .Values.data | toJson }}
{{ .Values.jsonString | fromJson }}

# B64Encode/B64Decode
{{ .Values.secret | b64enc }}
{{ .Values.encoded | b64dec }}

# Indent
{{ .Values.content | indent 2 }}
{{ .Values.content | nindent 4 }}

# Include (helper templates)
{{- include "myapp.labels" . | nindent 4 }}
```

---

### 10. Hooks & Lifecycle Management

#### 10.1 What are Hooks?

**Hooks** are Kubernetes jobs that run at specific points in a release lifecycle. They allow you to:
- Run database migrations before deployment
- Send notifications
- Backup data before upgrade
- Cleanup resources after uninstall

#### 10.2 Hook Types

| Hook | Execution Time |
|------|----------------|
| `pre-install` | Before templates are rendered |
| `post-install` | After all resources are loaded |
| `pre-delete` | Before deletion of release |
| `post-delete` | After deletion of release |
| `pre-upgrade` | Before upgrade is rendered |
| `post-upgrade` | After upgrade is complete |
| `pre-rollback` | Before rollback is rendered |
| `post-rollback` | After rollback is complete |
| `test` | Test suite execution |

#### 10.3 Hook Annotations

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-migration"
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: migration
        image: myapp:migrate
        command: ["/bin/sh", "-c", "python manage.py migrate"]
      restartPolicy: Never
```

**Hook Annotations:**
- `helm.sh/hook`: Hook type
- `helm.sh/hook-weight`: Execution order (lower first)
- `helm.sh/hook-delete-policy`: When to delete hook
  - `before-hook-creation`: Delete before creating new
  - `hook-succeeded`: Delete on success
  - `hook-failed`: Delete on failure

#### 10.4 Pre-Install Hook Example

```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-pre-install"
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: pre-install
        image: busybox
        command: ['sh', '-c', 'echo "Pre-install hook running"']
      restartPolicy: Never
```

#### 10.5 Post-Install Hook Example

```yaml
# templates/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-post-install"
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
spec:
  template:
    spec:
      containers:
      - name: notification
        image: curlimages/curl
        command: ['sh', '-c', 'curl -X POST https://hooks.slack.com/...']
      restartPolicy: Never
```

#### 10.6 Pre-Upgrade Hook (Database Migration)

```yaml
# templates/pre-upgrade-migration.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ .Release.Name }}-migration-{{ .Release.Revision }}"
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: migration
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        command: ["/bin/sh", "-c", "python manage.py migrate"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ .Release.Name }}-db
              key: url
      restartPolicy: Never
  backoffLimit: 3
```

#### 10.7 Test Hooks

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: test
    image: curlimages/curl
    command: ['sh', '-c', 'curl http://{{ .Release.Name }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

**Run Tests:**
```bash
helm test myapp
```

---

### 11. Dependencies & Subcharts

#### 11.1 Chart Dependencies

Charts can depend on other charts. Dependencies are defined in `Chart.yaml`:

```yaml
apiVersion: v2
name: myapp
version: 1.0.0
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
    tags:
      - cache
```

#### 11.2 Managing Dependencies

```bash
# Update dependencies
helm dependency update ./myapp

# Build dependencies
helm dependency build ./myapp

# List dependencies
helm dependency list ./myapp
```

**After update, dependencies are downloaded to `charts/` directory:**
```
myapp/
├── Chart.yaml
├── charts/
│   ├── postgresql-12.0.0.tgz
│   └── redis-17.0.0.tgz
└── ...
```

#### 11.3 Dependency Values

Override subchart values in parent `values.yaml`:

```yaml
# values.yaml
postgresql:
  enabled: true
  auth:
    postgresPassword: "mypassword"
    database: "myapp"
  persistence:
    enabled: true
    size: 10Gi

redis:
  enabled: true
  auth:
    enabled: true
    password: "redispassword"
```

#### 11.4 Dependency Conditions

```yaml
dependencies:
  - name: postgresql
    condition: postgresql.enabled
  - name: redis
    condition: redis.enabled
    tags:
      - cache
```

**Enable/Disable:**
```yaml
# values.yaml
postgresql:
  enabled: true
redis:
  enabled: false
tags:
  cache: false  # Disables redis
```

#### 11.5 Local Dependencies

```yaml
dependencies:
  - name: common
    version: "1.0.0"
    repository: "file://../common"
```

#### 11.6 OCI Dependencies

```yaml
dependencies:
  - name: myapp
    version: "1.0.0"
    repository: "oci://myregistry.io/charts"
```

---

### 12. Chart Testing & Validation

#### 12.1 Linting Charts

```bash
# Lint chart
helm lint ./myapp

# Lint with strict mode
helm lint ./myapp --strict

# Lint with values
helm lint ./myapp -f values.yaml
```

**Common Issues:**
- Missing required fields
- Invalid YAML
- Template syntax errors
- Missing values

#### 12.2 Template Testing

```bash
# Dry-run (render templates)
helm template myapp ./myapp

# With values
helm template myapp ./myapp -f values.yaml

# With debug
helm template myapp ./myapp --debug

# Validate with Kubernetes API
helm template myapp ./myapp | kubectl apply --dry-run=client -f -
```

#### 12.3 Chart Tests

**Test Pod Example:**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: test
    image: curlimages/curl
    command: ['sh', '-c', 'curl -f http://{{ .Release.Name }}:{{ .Values.service.port }}/health']
  restartPolicy: Never
```

**Run Tests:**
```bash
# Install release first
helm install myapp ./myapp

# Run tests
helm test myapp

# With cleanup
helm test myapp --cleanup
```

#### 12.4 CI/CD Testing

**GitHub Actions Example:**
```yaml
name: Helm Lint and Test
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    - name: Lint Chart
      run: helm lint ./myapp
    - name: Template Test
      run: helm template myapp ./myapp --debug
    - name: Install Test
      run: |
        helm install myapp ./myapp --dry-run --debug
```

---

### 13. Helm Plugins

#### 13.1 Popular Plugins

**helm-diff:**
```bash
# Install
helm plugin install https://github.com/databus23/helm-diff

# Show diff before upgrade
helm diff upgrade myapp ./myapp
```

**helm-secrets:**
```bash
# Install
helm plugin install https://github.com/jkroepke/helm-secrets

# Encrypt values
helm secrets encrypt values.yaml

# Install with decryption
helm secrets install myapp ./myapp -f values.yaml
```

**helm-unittest:**
```bash
# Install
helm plugin install https://github.com/helm-unittest/helm-unittest

# Run unit tests
helm unittest ./myapp
```

**helm-git:**
```bash
# Install
helm plugin install https://github.com/aslafy-z/helm-git

# Install from Git
helm install myapp git+https://github.com/myorg/charts@myapp
```

#### 13.2 Managing Plugins

```bash
# List plugins
helm plugin list

# Update plugin
helm plugin update <plugin-name>

# Uninstall plugin
helm plugin uninstall <plugin-name>
```

---

### 14. Helm 3 vs Helm 2

#### 14.1 Key Differences

| Feature | Helm 2 | Helm 3 |
|---------|--------|--------|
| **Architecture** | Client + Tiller | Client only |
| **Release Storage** | ConfigMaps/Secrets | Secrets only |
| **Security** | Tiller RBAC issues | No Tiller needed |
| **Chart API** | v1 | v2 |
| **Dependencies** | requirements.yaml | Chart.yaml |
| **Library Charts** | No | Yes |
| **OCI Support** | No | Yes |

#### 14.2 Migration from Helm 2

```bash
# Export Helm 2 releases
helm2 list > releases.txt

# For each release, migrate:
helm2 get values <release> > values.yaml
helm3 install <release> <chart> -f values.yaml
```

**Note:** Helm 2 is deprecated. Always use Helm 3.

---

## Part III: DevOps Integration

### 15. Helm with CI/CD Pipelines

#### 15.1 GitHub Actions

**Basic Workflow:**
```yaml
name: Deploy with Helm
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Helm
      uses: azure/setup-helm@v3
      with:
        version: '3.13.0'
    
    - name: Configure kubectl
      uses: azure/setup-kubectl@v3
    
    - name: Install/Upgrade
      run: |
        helm upgrade --install myapp ./charts/myapp \
          --namespace production \
          --create-namespace \
          --set image.tag=${{ github.sha }}
```

**Advanced Workflow with Testing:**
```yaml
name: Helm CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    
    - name: Lint Chart
      run: helm lint ./charts/myapp
    
    - name: Template Test
      run: helm template myapp ./charts/myapp --debug

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    - uses: azure/setup-kubectl@v3
    
    - name: Create Kind Cluster
      uses: helm/kind-action@v1.5.0
    
    - name: Install Chart
      run: |
        helm install myapp ./charts/myapp \
          --namespace test \
          --create-namespace
    
    - name: Run Tests
      run: helm test myapp --namespace test

  deploy-dev:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/develop'
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    - uses: azure/setup-kubectl@v3
    
    - name: Deploy to Dev
      run: |
        helm upgrade --install myapp ./charts/myapp \
          --namespace dev \
          --create-namespace \
          -f ./charts/myapp/values-dev.yaml \
          --set image.tag=${{ github.sha }}

  deploy-prod:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    - uses: azure/setup-kubectl@v3
    
    - name: Deploy to Production
      run: |
        helm upgrade --install myapp ./charts/myapp \
          --namespace production \
          --create-namespace \
          -f ./charts/myapp/values-prod.yaml \
          --set image.tag=${{ github.sha }} \
          --atomic \
          --wait
```

#### 15.2 GitLab CI/CD

```yaml
stages:
  - lint
  - test
  - deploy

variables:
  HELM_VERSION: "3.13.0"

lint:
  stage: lint
  image: alpine/helm:${HELM_VERSION}
  script:
    - helm lint ./charts/myapp
    - helm template myapp ./charts/myapp --debug

test:
  stage: test
  image: alpine/helm:${HELM_VERSION}
  script:
    - helm install myapp ./charts/myapp --dry-run --debug

deploy-dev:
  stage: deploy
  image: alpine/helm:${HELM_VERSION}
  environment:
    name: development
  script:
    - helm upgrade --install myapp ./charts/myapp \
        --namespace dev \
        --create-namespace \
        -f ./charts/myapp/values-dev.yaml \
        --set image.tag=${CI_COMMIT_SHA}
  only:
    - develop

deploy-prod:
  stage: deploy
  image: alpine/helm:${HELM_VERSION}
  environment:
    name: production
  script:
    - helm upgrade --install myapp ./charts/myapp \
        --namespace production \
        --create-namespace \
        -f ./charts/myapp/values-prod.yaml \
        --set image.tag=${CI_COMMIT_TAG} \
        --atomic \
        --wait
  only:
    - tags
```

#### 15.3 Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        HELM_VERSION = '3.13.0'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Lint') {
            steps {
                sh """
                    helm lint ./charts/myapp
                    helm template myapp ./charts/myapp --debug
                """
            }
        }
        
        stage('Deploy Dev') {
            when {
                branch 'develop'
            }
            steps {
                sh """
                    helm upgrade --install myapp ./charts/myapp \
                        --namespace dev \
                        --create-namespace \
                        -f ./charts/myapp/values-dev.yaml \
                        --set image.tag=${env.GIT_COMMIT}
                """
            }
        }
        
        stage('Deploy Prod') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    helm upgrade --install myapp ./charts/myapp \
                        --namespace production \
                        --create-namespace \
                        -f ./charts/myapp/values-prod.yaml \
                        --set image.tag=${env.GIT_COMMIT} \
                        --atomic \
                        --wait
                """
            }
        }
    }
    
    post {
        failure {
            sh 'helm rollback myapp --namespace ${env.ENVIRONMENT}'
        }
    }
}
```

#### 15.4 ArgoCD Integration

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
    repoURL: https://github.com/myorg/charts
    targetRevision: main
    path: charts/myapp
    helm:
      valueFiles:
      - values.yaml
      - values-prod.yaml
      values: |
        image:
          tag: v2.0.0
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

---

### 16. Helm with GitOps (ArgoCD)

#### 16.1 ArgoCD Helm Application

**Application Structure:**
```
charts/
├── myapp/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
└── README.md
```

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
    repoURL: https://github.com/myorg/charts-repo
    targetRevision: main
    path: charts/myapp
    helm:
      valueFiles:
      - values.yaml
      - values-prod.yaml
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
```

#### 16.2 Helm Values in Git

**values-prod.yaml:**
```yaml
replicaCount: 5

image:
  repository: myregistry/myapp
  tag: "v2.0.0"

ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

#### 16.3 ArgoCD Helm Parameters

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  source:
    helm:
      parameters:
      - name: image.tag
        value: v2.0.0
      - name: replicaCount
        value: "5"
```

---

### 17. Helm with Terraform

#### 17.1 Terraform Helm Provider

```hcl
terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "helm_release" "myapp" {
  name       = "myapp"
  repository = "https://charts.example.com"
  chart      = "myapp"
  version    = "1.0.0"
  namespace  = "production"
  
  values = [
    file("${path.module}/values.yaml")
  ]
  
  set {
    name  = "image.tag"
    value = "v2.0.0"
  }
  
  set {
    name  = "replicaCount"
    value = "5"
  }
}
```

#### 17.2 Terraform with Local Charts

```hcl
resource "helm_release" "myapp" {
  name       = "myapp"
  chart      = "./charts/myapp"
  namespace  = "production"
  
  values = [
    file("${path.module}/values-prod.yaml")
  ]
  
  depends_on = [
    kubernetes_namespace.production
  ]
}
```

#### 17.3 Terraform Helm with Variables

```hcl
variable "environment" {
  description = "Environment name"
  type        = string
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
}

resource "helm_release" "myapp" {
  name       = "myapp"
  chart      = "./charts/myapp"
  namespace  = var.environment
  
  values = [
    file("${path.module}/values-${var.environment}.yaml")
  ]
  
  set {
    name  = "image.tag"
    value = var.image_tag
  }
}
```

---

### 18. Helm with Monitoring & Observability

#### 18.1 Prometheus Integration

**Install Prometheus with Helm:**
```bash
# Add repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

**Add ServiceMonitor to Your Chart:**
```yaml
# templates/servicemonitor.yaml
{{- if .Values.monitoring.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
{{- end }}
```

**Values:**
```yaml
monitoring:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 30s
    scrapeTimeout: 10s
```

#### 18.2 Grafana Dashboard

**Install Grafana:**
```bash
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set adminPassword=admin
```

**Add Grafana Dashboard ConfigMap:**
```yaml
# templates/grafana-dashboard.yaml
{{- if .Values.grafana.dashboard.enabled }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "myapp.fullname" . }}-dashboard
  labels:
    grafana_dashboard: "1"
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "MyApp Dashboard",
        "panels": [...]
      }
    }
{{- end }}
```

#### 18.3 Logging with ELK

**Install Elasticsearch:**
```bash
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch
```

**Add Logging Sidecar:**
```yaml
# In deployment template
{{- if .Values.logging.enabled }}
- name: log-sidecar
  image: fluent/fluent-bit:latest
  volumeMounts:
  - name: varlog
    mountPath: /var/log
{{- end }}
```

---

### 19. Helm Security Best Practices

#### 19.1 Secrets Management

**Using Kubernetes Secrets:**
```yaml
# templates/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "myapp.fullname" . }}-secrets
type: Opaque
data:
  password: {{ .Values.secrets.password | b64enc | quote }}
```

**Using External Secrets Operator:**
```yaml
# templates/externalsecret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "myapp.fullname" . }}-secrets
spec:
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: {{ include "myapp.fullname" . }}-secrets
  data:
  - secretKey: password
    remoteRef:
      key: myapp/database/password
```

#### 19.2 Image Security

**Use Specific Tags:**
```yaml
# values.yaml
image:
  repository: myregistry/myapp
  tag: "v2.0.0"  # Not "latest"
  pullPolicy: IfNotPresent
```

**Image Pull Secrets:**
```yaml
# templates/deployment.yaml
spec:
  imagePullSecrets:
  - name: {{ include "myapp.fullname" . }}-registry-secret
```

#### 19.3 RBAC Best Practices

**Minimal ServiceAccount:**
```yaml
# templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
automountServiceAccountToken: false
```

**Role with Minimal Permissions:**
```yaml
# templates/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ include "myapp.fullname" . }}
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
```

#### 19.4 Network Policies

```yaml
# templates/networkpolicy.yaml
{{- if .Values.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "myapp.fullname" . }}
spec:
  podSelector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: allowed-namespace
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
{{- end }}
```

#### 19.5 Pod Security Standards

```yaml
# values.yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
```

#### 19.6 Chart Security Scanning

```bash
# Use chart-testing
ct lint --charts ./myapp

# Use checkov for security
checkov -d ./myapp

# Use kube-score
kube-score score ./myapp/templates/*.yaml
```

---

### 20. Helm in Multi-Environment Deployments

#### 20.1 Environment-Specific Values

**Structure:**
```
charts/
├── myapp/
│   ├── Chart.yaml
│   ├── values.yaml          # Base values
│   ├── values-dev.yaml      # Dev overrides
│   ├── values-staging.yaml  # Staging overrides
│   ├── values-prod.yaml     # Production overrides
│   └── templates/
```

**Base values.yaml:**
```yaml
replicaCount: 1

image:
  repository: myregistry/myapp
  tag: "latest"

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**values-prod.yaml:**
```yaml
replicaCount: 5

image:
  tag: "v2.0.0"

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10

ingress:
  enabled: true
  hosts:
    - host: myapp.example.com
```

#### 20.2 Deployment Script

```bash
#!/bin/bash
# deploy.sh

ENVIRONMENT=$1
IMAGE_TAG=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$IMAGE_TAG" ]; then
  echo "Usage: ./deploy.sh <environment> <image-tag>"
  exit 1
fi

helm upgrade --install myapp ./charts/myapp \
  --namespace $ENVIRONMENT \
  --create-namespace \
  -f ./charts/myapp/values.yaml \
  -f ./charts/myapp/values-$ENVIRONMENT.yaml \
  --set image.tag=$IMAGE_TAG \
  --atomic \
  --wait \
  --timeout 5m
```

**Usage:**
```bash
./deploy.sh dev v2.0.0-dev
./deploy.sh staging v2.0.0-rc1
./deploy.sh prod v2.0.0
```

#### 20.3 Environment-Specific Namespaces

```bash
# Development
helm install myapp ./charts/myapp \
  --namespace dev \
  --create-namespace \
  -f values-dev.yaml

# Staging
helm install myapp ./charts/myapp \
  --namespace staging \
  --create-namespace \
  -f values-staging.yaml

# Production
helm install myapp ./charts/myapp \
  --namespace production \
  --create-namespace \
  -f values-prod.yaml
```

---

### 21. Helm Chart Development Workflow

#### 21.1 Development Workflow

```
1. Create/Modify Chart
   ↓
2. Lint Chart
   ↓
3. Template Test (dry-run)
   ↓
4. Install in Dev Cluster
   ↓
5. Test Application
   ↓
6. Package Chart
   ↓
7. Push to Repository
   ↓
8. Deploy to Production
```

#### 21.2 Chart Versioning

**Semantic Versioning:**
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

**Chart.yaml:**
```yaml
version: 1.2.3  # Chart version
appVersion: "2.0.0"  # Application version
```

**Versioning Strategy:**
```bash
# Initial release
version: 1.0.0

# Bug fix
version: 1.0.1

# New feature
version: 1.1.0

# Breaking change
version: 2.0.0
```

#### 21.3 Chart Testing Workflow

```bash
# 1. Lint
helm lint ./myapp

# 2. Template (dry-run)
helm template myapp ./myapp --debug

# 3. Install in test cluster
helm install myapp ./myapp --namespace test

# 4. Run tests
helm test myapp

# 5. Upgrade test
helm upgrade myapp ./myapp --set image.tag=v2.0.0

# 6. Rollback test
helm rollback myapp 1

# 7. Uninstall
helm uninstall myapp
```

#### 21.4 CI/CD for Charts

**GitHub Actions:**
```yaml
name: Chart CI
on:
  push:
    paths:
    - 'charts/**'
    
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: azure/setup-helm@v3
    
    - name: Lint
      run: helm lint ./charts/myapp
    
    - name: Package
      run: helm package ./charts/myapp
    
    - name: Test Install
      run: |
        helm install myapp ./charts/myapp --dry-run --debug
```

---

### 22. Troubleshooting & Best Practices

#### 22.1 Common Issues

**Issue: Template Rendering Errors**
```bash
# Debug template
helm template myapp ./myapp --debug

# Check specific template
helm template myapp ./myapp --show-only templates/deployment.yaml
```

**Issue: Values Not Applied**
```bash
# Check values
helm get values myapp

# Verify with template
helm template myapp ./myapp --set key=value --debug
```

**Issue: Release Stuck**
```bash
# Check release status
helm status myapp

# Check pods
kubectl get pods -n <namespace>

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

**Issue: Rollback Failed**
```bash
# Check history
helm history myapp

# Manual rollback
helm rollback myapp <revision>

# Force rollback
helm rollback myapp <revision> --force
```

#### 22.2 Debugging Tips

```bash
# Verbose output
helm install myapp ./myapp --debug --dry-run

# Check rendered templates
helm template myapp ./myapp > rendered.yaml

# Validate with kubectl
helm template myapp ./myapp | kubectl apply --dry-run=client -f -

# Check release secrets
kubectl get secret -n <namespace> | grep helm

# Decode release secret
kubectl get secret sh.helm.release.v1.myapp.v1 -n <namespace> -o jsonpath='{.data.release}' | base64 -d | base64 -d | gzip -d
```

#### 22.3 Best Practices

**1. Use Semantic Versioning**
```yaml
version: 1.2.3  # MAJOR.MINOR.PATCH
```

**2. Document Values**
```yaml
# values.yaml
# Number of replicas
replicaCount: 1

# Image configuration
image:
  # Repository URL
  repository: nginx
  # Image tag
  tag: "1.21"
```

**3. Use Helper Templates**
```yaml
# _helpers.tpl
{{- define "myapp.labels" -}}
# Reusable labels
{{- end }}
```

**4. Validate Required Values**
```yaml
{{- if not .Values.image.repository }}
{{- fail "image.repository is required" }}
{{- end }}
```

**5. Use Conditions for Optional Features**
```yaml
{{- if .Values.ingress.enabled }}
# Ingress resources
{{- end }}
```

**6. Test Before Deploying**
```bash
helm lint ./myapp
helm template myapp ./myapp --debug
helm install myapp ./myapp --dry-run
```

**7. Use Atomic Upgrades**
```bash
helm upgrade myapp ./myapp --atomic
```

**8. Set Resource Limits**
```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

**9. Use Secrets for Sensitive Data**
```yaml
# Don't put secrets in values.yaml
# Use Kubernetes Secrets or External Secrets
```

**10. Version Control Charts**
```bash
# Keep charts in Git
git add charts/
git commit -m "Update chart to v1.2.0"
git tag chart-v1.2.0
```

#### 22.4 Performance Optimization

**1. Use .helmignore**
```
.helmignore
.git
*.swp
.env
```

**2. Minimize Template Complexity**
```yaml
# Good: Simple template
{{ .Values.name }}

# Bad: Complex nested logic
{{- if .Values.config.enabled }}{{ .Values.config.name }}{{ else }}{{ .Values.default.name }}{{ end }}
```

**3. Cache Dependencies**
```bash
# Update dependencies only when needed
helm dependency update ./myapp
```

---

## Quick Reference

### Essential Commands

```bash
# Install
helm install <release> <chart>

# Upgrade
helm upgrade <release> <chart>

# List
helm list

# Status
helm status <release>

# Rollback
helm rollback <release>

# Uninstall
helm uninstall <release>

# Template
helm template <release> <chart>

# Lint
helm lint <chart>
```

### Common Patterns

```yaml
# Default value
{{ .Values.replicaCount | default 1 }}

# Conditional
{{- if .Values.enabled }}
# content
{{- end }}

# Include helper
{{- include "myapp.labels" . | nindent 4 }}

# Range
{{- range .Values.items }}
- {{ . }}
{{- end }}
```

---

## Conclusion

Helm is an essential tool for DevOps engineers working with Kubernetes. It simplifies:
- Application deployment
- Configuration management
- Version control
- Multi-environment deployments
- CI/CD integration

**Key Takeaways:**
- ✅ Use Helm 3 (Helm 2 is deprecated)
- ✅ Follow semantic versioning
- ✅ Test charts before deploying
- ✅ Use values files for configuration
- ✅ Integrate with CI/CD pipelines
- ✅ Follow security best practices
- ✅ Document your charts

Master Helm to become more efficient in managing Kubernetes applications! 🚀

