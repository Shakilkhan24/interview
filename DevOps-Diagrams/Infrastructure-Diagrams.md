# Infrastructure as Code Diagrams

## 35. Terraform Workflow

```mermaid
graph LR
    A[Write .tf Files] --> B[terraform init]
    B --> C[terraform plan]
    C --> D[terraform apply]
    D --> E[Infrastructure]
    E --> F[terraform destroy]
```

## 36. Terraform State Management

```mermaid
graph TB
    A[Terraform Code] --> B[State File]
    B --> C[Local State]
    B --> D[Remote State]
    D --> E[S3/Consul/etc]
    B --> F[State Locking]
```

## 37. Infrastructure Provisioning Flow

```mermaid
graph TB
    A[IaC Code] --> B[Version Control]
    B --> C[CI/CD Pipeline]
    C --> D[Plan Stage]
    D --> E[Review]
    E --> F[Apply Stage]
    F --> G[Cloud Provider]
    G --> H[Resources Created]
```

## 38. Ansible Playbook Execution

```mermaid
graph TB
    A[Ansible Control Node] --> B[Inventory]
    A --> C[Playbook]
    C --> D[Tasks]
    D --> E[Target Hosts]
    E --> F[SSH Connection]
    F --> G[Execute Tasks]
```

## 39. CloudFormation Stack

```mermaid
graph TB
    A[Template] --> B[CloudFormation]
    B --> C[Stack Creation]
    C --> D[Resources]
    D --> E[EC2]
    D --> F[RDS]
    D --> G[VPC]
    D --> H[S3]
```

## 40. Pulumi Architecture

```mermaid
graph TB
    A[Pulumi Code] --> B[Language SDK]
    B --> C[Pulumi Engine]
    C --> D[Cloud Provider API]
    D --> E[Infrastructure]
```

## 41. Infrastructure Drift Detection

```mermaid
graph TB
    A[Desired State] --> B[Actual State]
    B --> C[Compare]
    C --> D{Drift Detected?}
    D -->|Yes| E[Alert/Remediate]
    D -->|No| F[In Sync]
```

