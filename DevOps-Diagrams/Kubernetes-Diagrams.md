# Kubernetes Architecture Diagrams

## 13. Kubernetes Cluster Architecture

```mermaid
graph TB
    subgraph "Control Plane"
        A[API Server]
        B[etcd]
        C[Scheduler]
        D[Controller Manager]
    end
    subgraph "Worker Nodes"
        E[Kubelet]
        F[Kube-proxy]
        G[Container Runtime]
        H[Pods]
    end
    A --> B
    A --> C
    A --> D
    A --> E
    E --> F
    E --> G
    G --> H
```

## 14. Pod Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Running: Container Started
    Running --> Succeeded: All Containers Exit 0
    Running --> Failed: Container Exits Non-Zero
    Running --> Unknown: Node Communication Lost
    Succeeded --> [*]
    Failed --> [*]
    Unknown --> [*]
```

## 15. Kubernetes Service Types

```mermaid
graph TB
    A[Pod] --> B[ClusterIP]
    A --> C[NodePort]
    A --> D[LoadBalancer]
    A --> E[ExternalName]
    B --> F[Internal Access]
    C --> G[Port on Node]
    D --> H[Cloud LB]
    E --> I[External Service]
```

## 16. Deployment Strategy - Rolling Update

```mermaid
graph LR
    A[Old Pods] --> B[New Pod 1]
    B --> C[New Pod 2]
    C --> D[New Pod 3]
    D --> E[All New Pods]
    E --> F[Remove Old Pods]
```

## 17. Kubernetes Ingress Flow

```mermaid
graph TB
    A[User] --> B[Internet]
    B --> C[Ingress Controller]
    C --> D[Ingress Resource]
    D --> E[Service]
    E --> F[Pods]
```

## 18. ConfigMap and Secret Usage

```mermaid
graph TB
    A[ConfigMap] --> B[Pod]
    C[Secret] --> B
    D[Volume Mount] --> B
    B --> E[Container]
    E --> F[Application]
```

## 19. Horizontal Pod Autoscaler

```mermaid
graph TB
    A[Metrics Server] --> B[HPA Controller]
    B --> C{CPU/Memory > Threshold?}
    C -->|Yes| D[Scale Up]
    C -->|No| E{Below Threshold?}
    E -->|Yes| F[Scale Down]
    E -->|No| G[Maintain]
    D --> H[More Pods]
    F --> I[Fewer Pods]
```

## 20. Kubernetes Namespace Isolation

```mermaid
graph TB
    subgraph "Namespace: Production"
        A[Prod Pods]
        B[Prod Services]
        C[Prod Secrets]
    end
    subgraph "Namespace: Staging"
        D[Staging Pods]
        E[Staging Services]
        F[Staging Secrets]
    end
    subgraph "Namespace: Development"
        G[Dev Pods]
        H[Dev Services]
        I[Dev Secrets]
    end
```

## 21. StatefulSet Architecture

```mermaid
graph TB
    A[StatefulSet] --> B[Pod-0]
    A --> C[Pod-1]
    A --> D[Pod-2]
    B --> E[PV-0]
    C --> F[PV-1]
    D --> G[PV-2]
    B --> H[Headless Service]
    C --> H
    D --> H
```

## 22. DaemonSet Architecture

```mermaid
graph TB
    A[DaemonSet] --> B[Node 1]
    A --> C[Node 2]
    A --> D[Node 3]
    B --> E[Log Collector Pod]
    C --> F[Log Collector Pod]
    D --> G[Log Collector Pod]
```

## 23. Kubernetes Networking Model

```mermaid
graph TB
    A[Pod 1] --> B[Pod Network]
    C[Pod 2] --> B
    D[Pod 3] --> B
    B --> E[Service Network]
    E --> F[Cluster Network]
    F --> G[External Network]
```

## 24. Persistent Volume Lifecycle

```mermaid
graph LR
    A[PV Created] --> B[Available]
    B --> C[Bound to PVC]
    C --> D[In Use]
    D --> E[Released]
    E --> F[Failed/Deleted]
```

## 25. Kubernetes RBAC Flow

```mermaid
graph TB
    A[User/ServiceAccount] --> B[Authentication]
    B --> C[Authorization]
    C --> D{Role/RoleBinding?}
    D -->|Yes| E[Allow Access]
    D -->|No| F[Deny Access]
```

## 26. Helm Chart Architecture

```mermaid
graph TB
    A[Helm Chart] --> B[Values.yaml]
    A --> C[Templates]
    C --> D[Deployment]
    C --> E[Service]
    C --> F[ConfigMap]
    B --> G[Helm Install]
    G --> H[Kubernetes Resources]
```

