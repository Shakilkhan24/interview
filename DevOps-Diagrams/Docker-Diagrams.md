# Docker and Containerization Diagrams

## 27. Docker Architecture

```mermaid
graph TB
    A[Docker Client] --> B[Docker Daemon]
    B --> C[Containers]
    B --> D[Images]
    B --> E[Volumes]
    B --> F[Networks]
    D --> G[Registry]
```

## 28. Docker Image Layers

```mermaid
graph TB
    A[Application Layer] --> B[Runtime Layer]
    B --> C[OS Libraries]
    C --> D[Base OS Layer]
    E[Read-Write Layer] --> A
```

## 29. Docker Compose Architecture

```mermaid
graph TB
    A[docker-compose.yml] --> B[Web Service]
    A --> C[Database Service]
    A --> D[Redis Service]
    B --> E[Network]
    C --> E
    D --> E
    B --> F[Volumes]
    C --> F
```

## 30. Container Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Running: docker start
    Running --> Paused: docker pause
    Paused --> Running: docker unpause
    Running --> Stopped: docker stop
    Stopped --> Running: docker start
    Stopped --> [*]: docker rm
    Running --> [*]: docker rm -f
```

## 31. Multi-Stage Docker Build

```mermaid
graph TB
    A[Source Code] --> B[Build Stage]
    B --> C[Compiled Binary]
    C --> D[Runtime Stage]
    D --> E[Final Image]
    F[Build Tools] --> B
    G[Only Runtime] --> D
```

## 32. Docker Registry Flow

```mermaid
graph LR
    A[Developer] -->|docker push| B[Docker Registry]
    B --> C[Image Storage]
    D[CI/CD] -->|docker pull| B
    E[Production] -->|docker pull| B
```

## 33. Container Networking Modes

```mermaid
graph TB
    A[Container] --> B[Bridge Network]
    A --> C[Host Network]
    A --> D[None Network]
    A --> E[Overlay Network]
    A --> F[Macvlan Network]
```

## 34. Docker Volume Types

```mermaid
graph TB
    A[Docker Volumes] --> B[Named Volume]
    A --> C[Bind Mount]
    A --> D[Tmpfs Mount]
    B --> E[Managed by Docker]
    C --> F[Host Path]
    D --> G[Memory]
```

