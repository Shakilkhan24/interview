# CI/CD Pipeline Diagrams

## 1. Basic CI/CD Pipeline Flow

```mermaid
graph LR
    A[Developer] -->|Push Code| B[Git Repository]
    B -->|Webhook| C[CI Server]
    C -->|Build| D[Build Stage]
    D -->|Test| E[Test Stage]
    E -->|Deploy| F[Staging]
    F -->|Manual Approval| G[Production]
```

## 2. Complete CI/CD Pipeline with Stages

```mermaid
graph TD
    A[Source Code] --> B[Version Control]
    B --> C[Build]
    C --> D[Unit Tests]
    D --> E[Integration Tests]
    E --> F[Code Quality]
    F --> G[Security Scan]
    G --> H[Build Artifact]
    H --> I[Deploy to Dev]
    I --> J[Smoke Tests]
    J --> K[Deploy to Staging]
    K --> L[E2E Tests]
    L --> M[Deploy to Prod]
    M --> N[Monitoring]
```

## 3. GitLab CI/CD Pipeline

```mermaid
graph TB
    A[Git Push] --> B[GitLab CI]
    B --> C[Build Stage]
    C --> D[Test Stage]
    D --> E[Deploy Stage]
    E --> F[Staging Environment]
    E --> G[Production Environment]
    F --> H[Manual Approval]
    H --> G
```

## 4. Jenkins Pipeline Stages

```mermaid
graph LR
    A[Checkout] --> B[Build]
    B --> C[Test]
    C --> D[Package]
    D --> E[Deploy Dev]
    E --> F[Deploy Staging]
    F --> G[Deploy Prod]
    G --> H[Notify]
```

## 5. GitHub Actions Workflow

```mermaid
graph TD
    A[Push/PR] --> B[Trigger Workflow]
    B --> C[Checkout Code]
    C --> D[Setup Environment]
    D --> E[Install Dependencies]
    E --> F[Run Tests]
    F --> G[Build Docker Image]
    G --> H[Push to Registry]
    H --> I[Deploy]
```

## 6. Multi-Environment Deployment Pipeline

```mermaid
graph TB
    A[Code Commit] --> B[CI Pipeline]
    B --> C{Pass Tests?}
    C -->|Yes| D[Build Image]
    C -->|No| Z[Fail]
    D --> E[Push to Registry]
    E --> F[Deploy to Dev]
    F --> G[Dev Tests]
    G --> H[Deploy to QA]
    H --> I[QA Tests]
    I --> J[Deploy to Staging]
    J --> K[Staging Tests]
    K --> L[Manual Approval]
    L --> M[Deploy to Prod]
```

## 7. Blue-Green Deployment Pipeline

```mermaid
graph LR
    A[New Version] --> B[Build]
    B --> C[Deploy Green]
    C --> D[Health Check]
    D --> E{Healthy?}
    E -->|Yes| F[Switch Traffic]
    E -->|No| G[Rollback]
    F --> H[Monitor]
    H --> I[Decommission Blue]
```

## 8. Canary Deployment Pipeline

```mermaid
graph TD
    A[New Release] --> B[Build & Test]
    B --> C[Deploy 10%]
    C --> D[Monitor Metrics]
    D --> E{Errors < Threshold?}
    E -->|Yes| F[Deploy 50%]
    E -->|No| G[Rollback]
    F --> H[Monitor]
    H --> I{Still Good?}
    I -->|Yes| J[Deploy 100%]
    I -->|No| G
```

## 9. CI/CD with Docker

```mermaid
graph TB
    A[Code Push] --> B[GitHub]
    B --> C[Jenkins]
    C --> D[Docker Build]
    D --> E[Docker Test]
    E --> F[Docker Registry]
    F --> G[Kubernetes]
    G --> H[Deploy Pods]
```

## 10. CI/CD Security Pipeline

```mermaid
graph LR
    A[Code] --> B[SAST Scan]
    B --> C[Dependency Check]
    C --> D[Container Scan]
    D --> E[Secrets Scan]
    E --> F{All Pass?}
    F -->|Yes| G[Build]
    F -->|No| H[Block]
    G --> I[Deploy]
```

## 11. ArgoCD GitOps Flow

```mermaid
graph TB
    A[Git Repository] -->|Manifests| B[ArgoCD]
    B --> C[Compare State]
    C --> D{Sync Needed?}
    D -->|Yes| E[Apply to K8s]
    D -->|No| F[Monitor]
    E --> G[Kubernetes Cluster]
    G --> H[Application Running]
```

## 12. Multi-Branch Pipeline Strategy

```mermaid
graph TD
    A[Feature Branch] --> B[Run Tests]
    B --> C[Build]
    C --> D[Deploy Preview]
    D --> E[PR Review]
    E --> F[Main Branch]
    F --> G[Full Pipeline]
    G --> H[Production]
```

