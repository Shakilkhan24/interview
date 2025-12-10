# Security and DevSecOps Diagrams

## 49. DevSecOps Pipeline

```mermaid
graph TB
    A[Code] --> B[SAST]
    B --> C[Dependency Scan]
    C --> D[Container Scan]
    D --> E[Secrets Scan]
    E --> F[Build]
    F --> G[DAST]
    G --> H[Deploy]
    H --> I[Runtime Security]
```

## 50. Zero Trust Architecture

```mermaid
graph TB
    A[User/Device] --> B[Verify Identity]
    B --> C[Verify Device]
    C --> D[Verify Access]
    D --> E[Least Privilege]
    E --> F[Resource]
    F --> G[Continuous Monitoring]
```

## 51. Security Scanning Layers

```mermaid
graph TB
    A[Source Code] --> B[SAST]
    C[Dependencies] --> D[SCA]
    E[Container Image] --> F[Image Scanning]
    G[Infrastructure] --> H[IaC Scanning]
    I[Runtime] --> J[RASP]
```

## 52. Secrets Management Flow

```mermaid
graph TB
    A[Application] --> B[Secrets Manager]
    B --> C[Vault/AWS Secrets]
    C --> D[Encrypted Storage]
    D --> E[Access Control]
    E --> F[Audit Log]
```

## 53. Network Security Zones

```mermaid
graph TB
    A[Internet] --> B[DMZ]
    B --> C[Web Tier]
    C --> D[App Tier]
    D --> E[Data Tier]
    F[Firewall] --> B
    G[WAF] --> C
    H[Network ACL] --> D
```

## 54. Container Security Layers

```mermaid
graph TB
    A[Base Image] --> B[Vulnerability Scan]
    B --> C[Minimal Packages]
    C --> D[Non-Root User]
    D --> E[Read-Only FS]
    E --> F[Network Policies]
    F --> G[Runtime Protection]
```

