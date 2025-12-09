# Containerization in DevOps - Master Guide
## Docker, Docker Compose, and Advanced Container Technologies

---

## Table of Contents

1. [Container Fundamentals](#1-container-fundamentals)
2. [Docker Installation & Setup](#2-docker-installation--setup)
3. [Docker Basics](#3-docker-basics)
4. [Dockerfile Mastery](#4-dockerfile-mastery)
5. [Docker Images & Registry](#5-docker-images--registry)
6. [Docker Networking](#6-docker-networking)
7. [Docker Volumes & Storage](#7-docker-volumes--storage)
8. [Docker Compose](#8-docker-compose)
9. [Multi-Stage Builds & Optimization](#9-multi-stage-builds--optimization)
10. [Container Security](#10-container-security)
11. [Docker Swarm](#11-docker-swarm)
12. [Alternative Container Runtimes](#12-alternative-container-runtimes)
13. [Container Monitoring & Logging](#13-container-monitoring--logging)
14. [CI/CD Integration](#14-cicd-integration)
15. [Best Practices & Patterns](#15-best-practices--patterns)

---

## 1. Container Fundamentals

### 1.1 What are Containers?

**Containers vs Virtual Machines:**

```
Virtual Machine Approach:
┌─────────────────────────────────────┐
│      Application A                  │
│      Bins/Libs                      │
├─────────────────────────────────────┤
│      Guest OS                       │
├─────────────────────────────────────┤
│      Hypervisor                     │
├─────────────────────────────────────┤
│      Host Operating System          │
│      Infrastructure                 │
└─────────────────────────────────────┘

Container Approach:
┌─────────────────────────────────────┐
│      Application A    Application B │
│      Bins/Libs       Bins/Libs      │
├─────────────────────────────────────┤
│      Container Engine (Docker)      │
├─────────────────────────────────────┤
│      Host Operating System          │
│      Infrastructure                 │
└─────────────────────────────────────┘
```

**Key Differences:**

| Aspect | Virtual Machines | Containers |
|--------|-----------------|------------|
| Isolation | Full OS isolation | Process isolation |
| Startup Time | Minutes | Seconds |
| Resource Overhead | High (GBs) | Low (MBs) |
| Performance | Near-native | Native |
| Portability | Medium | High |
| Density | Low | High |

### 1.2 Container Benefits

- **Consistency**: Same environment across dev, test, prod
- **Isolation**: Applications don't interfere with each other
- **Portability**: Run anywhere Docker is installed
- **Efficiency**: Better resource utilization
- **Scalability**: Easy to scale up/down
- **Microservices**: Perfect for microservices architecture

### 1.3 Container Architecture

```
┌─────────────────────────────────────────┐
│         Docker Client                   │
│  (docker CLI, Docker Compose, etc.)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         Docker Daemon                   │
│  (dockerd - Container runtime)          │
└─────┬──────────┬──────────┬─────────────┘
      │          │          │
      ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│Container│ │Container│ │Container│
│   A     │ │   B     │ │   C     │
└─────────┘ └─────────┘ └─────────┘
```

---

## 2. Docker Installation & Setup

### 2.1 Docker Installation

**Ubuntu/Debian:**

```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

**RHEL/CentOS:**

```bash
# Install prerequisites
sudo yum install -y yum-utils

# Add repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify
sudo docker run hello-world
```

**Post-Installation Setup:**

```bash
# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER
newgrp docker  # Or log out and back in

# Verify non-sudo access
docker run hello-world

# Configure Docker daemon
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "data-root": "/var/lib/docker"
}
EOF

# Restart Docker
sudo systemctl restart docker
```

### 2.2 Docker Desktop (Windows/macOS)

```bash
# Download from: https://www.docker.com/products/docker-desktop

# For Windows:
# - Requires WSL 2 backend
# - Enable Hyper-V or VirtualBox

# For macOS:
# - Requires Apple Silicon or Intel processor
# - Uses HyperKit (Intel) or Virtualization framework (Apple Silicon)
```

---

## 3. Docker Basics

### 3.1 Container Lifecycle

**Basic Container Operations:**

```bash
# Run a container
docker run ubuntu:latest
docker run -it ubuntu:latest /bin/bash  # Interactive terminal

# List running containers
docker ps
docker ps -a              # All containers (including stopped)

# Stop container
docker stop container_id

# Start stopped container
docker start container_id

# Restart container
docker restart container_id

# Remove container
docker rm container_id
docker rm -f container_id  # Force remove running container

# Remove all stopped containers
docker container prune
```

**Container Execution:**

```bash
# Run with name
docker run --name mycontainer nginx:latest

# Run in detached mode
docker run -d --name mycontainer nginx:latest

# Run with port mapping
docker run -d -p 8080:80 --name myweb nginx:latest
# Host:Container port mapping

# Run with environment variables
docker run -e MYSQL_ROOT_PASSWORD=secret mysql:latest

# Run with volume mount
docker run -v /host/path:/container/path nginx:latest

# Run with multiple options
docker run -d \
  --name myapp \
  -p 8080:80 \
  -e ENV_VAR=value \
  -v /host/data:/app/data \
  myapp:latest
```

### 3.2 Container Inspection

```bash
# Inspect container
docker inspect container_id
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_id

# View container logs
docker logs container_id
docker logs -f container_id        # Follow logs
docker logs --tail 100 container_id # Last 100 lines
docker logs --since 10m container_id # Since 10 minutes ago

# View container processes
docker top container_id

# View container statistics
docker stats
docker stats container_id

# Execute command in running container
docker exec -it container_id /bin/bash
docker exec container_id command
docker exec -u root container_id command  # As root
```

### 3.3 Container Resource Management

```bash
# Limit CPU
docker run --cpus="1.5" nginx:latest
docker run --cpus=".5" nginx:latest  # 50% of one CPU

# Limit memory
docker run -m 512m nginx:latest
docker run --memory="1g" --memory-swap="2g" nginx:latest

# Limit both
docker run --cpus="2" -m 1g nginx:latest

# Restart policy
docker run --restart=always nginx:latest
docker run --restart=unless-stopped nginx:latest
docker run --restart=on-failure:5 nginx:latest  # Max 5 restarts

# Resource constraints
docker update --cpus="2" --memory="2g" container_id
```

---

## 4. Dockerfile Mastery

### 4.1 Dockerfile Basics

**Simple Dockerfile:**

```dockerfile
# Base image
FROM ubuntu:22.04

# Metadata
LABEL maintainer="devops@example.com"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run
CMD ["python3", "app.py"]
```

### 4.2 Dockerfile Instructions

**FROM:**

```dockerfile
# Official image
FROM ubuntu:22.04

# Specific tag
FROM node:18-alpine

# Digest (most secure)
FROM node@sha256:abc123...

# Multi-stage build
FROM node:18 AS builder
FROM nginx:alpine AS production
```

**RUN:**

```dockerfile
# Single command
RUN apt-get update

# Chained commands (reduces layers)
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Shell form
RUN echo "Hello" > /tmp/file

# Exec form (preferred)
RUN ["/bin/bash", "-c", "echo Hello > /tmp/file"]
```

**COPY vs ADD:**

```dockerfile
# COPY (recommended)
COPY source.txt /dest/
COPY source.txt dest.txt
COPY app/ /app/

# ADD (has extra features)
ADD source.txt /dest/
ADD http://example.com/file.tar.gz /tmp/  # Can download URLs
ADD file.tar.gz /tmp/  # Auto-extracts archives
```

**WORKDIR:**

```dockerfile
# Sets working directory (creates if doesn't exist)
WORKDIR /app
WORKDIR /app/src
# Now in /app/src
```

**ENV vs ARG:**

```dockerfile
# ENV - Available at runtime
ENV PYTHON_VERSION=3.9
ENV PATH="/app/bin:$PATH"

# ARG - Build-time only
ARG BUILD_VERSION
ARG USER_NAME=default

# Use ARG to set ENV
ARG VERSION=latest
ENV APP_VERSION=$VERSION
```

**EXPOSE:**

```dockerfile
# Documents which ports the container listens on
EXPOSE 80
EXPOSE 443
EXPOSE 8080/tcp
EXPOSE 53/udp

# Note: EXPOSE doesn't publish ports
# Use -p flag or docker-compose ports
```

**CMD vs ENTRYPOINT:**

```dockerfile
# CMD - Default command (can be overridden)
CMD ["python3", "app.py"]
CMD python3 app.py  # Shell form

# ENTRYPOINT - Main command (always executed)
ENTRYPOINT ["python3", "app.py"]
ENTRYPOINT ["nginx", "-g", "daemon off;"]

# Combined
ENTRYPOINT ["python3"]
CMD ["app.py"]
# docker run image -> python3 app.py
# docker run image server.py -> python3 server.py
```

### 4.3 Advanced Dockerfile Patterns

**Multi-stage Build:**

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
USER nodejs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Healthcheck:**

```dockerfile
# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Or using built-in tools
HEALTHCHECK CMD pg_isready -U postgres || exit 1
```

**User Management:**

```dockerfile
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Or in Alpine
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

# Switch to user
USER appuser
```

---

## 5. Docker Images & Registry

### 5.1 Image Management

```bash
# List images
docker images
docker image ls

# Search images
docker search nginx

# Pull image
docker pull nginx:latest
docker pull nginx:1.21-alpine

# Remove image
docker rmi image_id
docker rmi nginx:latest

# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a

# Image history
docker history image_name

# Inspect image
docker inspect image_name
docker inspect --format='{{.Config.ExposedPorts}}' image_name
```

### 5.2 Building Images

```bash
# Build from Dockerfile
docker build .
docker build -t myapp:latest .
docker build -t myapp:1.0 -t myapp:latest .

# Build with build args
docker build --build-arg VERSION=1.0 -t myapp:1.0 .

# Build from specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build without cache
docker build --no-cache -t myapp:latest .

# Build with target (multi-stage)
docker build --target builder -t myapp:builder .

# Build with progress
docker build --progress=plain -t myapp:latest .
```

### 5.3 Image Tagging & Registry

```bash
# Tag image
docker tag myapp:latest myapp:1.0
docker tag myapp:latest registry.example.com/myapp:latest
docker tag myapp:latest registry.example.com/myapp:1.0

# Push to registry
docker push registry.example.com/myapp:latest

# Login to registry
docker login
docker login registry.example.com
docker login -u username -p password registry.example.com

# Logout
docker logout
docker logout registry.example.com

# Save/load image (tar file)
docker save -o myapp.tar myapp:latest
docker load -i myapp.tar

# Export/import container
docker export container_id > container.tar
docker import container.tar newimage:tag
```

### 5.4 Docker Hub & Private Registries

**Docker Hub:**

```bash
# Tag for Docker Hub
docker tag myapp:latest username/myapp:latest

# Push to Docker Hub
docker push username/myapp:latest

# Pull from Docker Hub
docker pull username/myapp:latest
```

**Private Registry (Docker Registry):**

```bash
# Run local registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for local registry
docker tag myapp:latest localhost:5000/myapp:latest

# Push to local registry
docker push localhost:5000/myapp:latest

# Pull from local registry
docker pull localhost:5000/myapp:latest

# Configure insecure registry (development only)
# /etc/docker/daemon.json
{
  "insecure-registries": ["localhost:5000"]
}
```

**Harbor Registry Setup:**

```bash
# Install Harbor
wget https://github.com/goharbor/harbor/releases/download/v2.8.0/harbor-offline-installer-v2.8.0.tgz
tar xvf harbor-offline-installer-v2.8.0.tgz
cd harbor
./install.sh

# Access Harbor UI
# https://harbor.example.com

# Login and push
docker login harbor.example.com
docker tag myapp:latest harbor.example.com/project/myapp:latest
docker push harbor.example.com/project/myapp:latest
```

---

## 6. Docker Networking

### 6.1 Network Types

**Default Networks:**

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Default networks:
# - bridge: Default network for containers
# - host: Uses host's network stack
# - none: No networking
```

**Network Drivers:**

```bash
# Bridge network (default)
docker network create mynetwork
docker network create --driver bridge mybridge

# Host network
docker run --network host nginx:latest

# None network
docker run --network none nginx:latest

# Overlay network (for Swarm)
docker network create --driver overlay myoverlay

# Macvlan network (direct access to physical network)
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  mymacvlan
```

### 6.2 Custom Networks

**Create and Use Networks:**

```bash
# Create network
docker network create mynetwork
docker network create --subnet=172.20.0.0/16 mynetwork
docker network create --gateway=172.20.0.1 --subnet=172.20.0.0/16 mynetwork

# Connect container to network
docker network connect mynetwork container_id

# Disconnect container
docker network disconnect mynetwork container_id

# Remove network
docker network rm mynetwork

# Remove unused networks
docker network prune
```

**Container-to-Container Communication:**

```bash
# Create network
docker network create app-network

# Run containers on same network
docker run -d --name web1 --network app-network nginx
docker run -d --name web2 --network app-network nginx

# Containers can communicate by name
docker exec web1 ping web2
```

**Network Aliases:**

```bash
# Create network with alias
docker network create mynetwork

# Run with alias
docker run -d --name app --network mynetwork --network-alias api nginx

# Other containers can reach via alias
docker run --network mynetwork alpine ping api
```

### 6.3 Port Mapping

```bash
# Basic port mapping
docker run -p 8080:80 nginx:latest
# Host:Container

# Bind to specific interface
docker run -p 127.0.0.1:8080:80 nginx:latest

# Random host port
docker run -P nginx:latest
# Docker assigns random port

# UDP port
docker run -p 8080:80/udp nginx:latest

# Multiple ports
docker run -p 8080:80 -p 8443:443 nginx:latest

# Port range
docker run -p 8000-8009:8000-8009 nginx:latest
```

---

## 7. Docker Volumes & Storage

### 7.1 Volume Types

**Bind Mounts:**

```bash
# Mount host directory
docker run -v /host/path:/container/path nginx:latest

# Mount with options
docker run -v /host/path:/container/path:ro nginx:latest  # Read-only
docker run -v /host/path:/container/path:rw nginx:latest  # Read-write

# Using --mount (newer syntax)
docker run --mount type=bind,source=/host/path,target=/container/path nginx:latest
```

**Named Volumes:**

```bash
# Create volume
docker volume create myvolume

# List volumes
docker volume ls

# Inspect volume
docker volume inspect myvolume

# Use volume
docker run -v myvolume:/data nginx:latest
docker run --mount source=myvolume,target=/data nginx:latest

# Remove volume
docker volume rm myvolume

# Remove unused volumes
docker volume prune
```

**tmpfs Mounts:**

```bash
# In-memory filesystem
docker run --tmpfs /tmp nginx:latest
docker run --mount type=tmpfs,destination=/tmp nginx:latest

# With options
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m nginx:latest
```

### 7.2 Volume Management

```bash
# Backup volume
docker run --rm \
  -v myvolume:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm \
  -v myvolume:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/backup.tar.gz -C /

# Copy files to/from container
docker cp container_id:/path/file.txt ./file.txt
docker cp ./file.txt container_id:/path/file.txt
```

### 7.3 Storage Drivers

```bash
# View storage driver
docker info | grep Storage

# Common storage drivers:
# - overlay2 (recommended, default on most systems)
# - aufs (older)
# - devicemapper (RHEL)
# - btrfs, zfs

# Configure storage driver
# /etc/docker/daemon.json
{
  "storage-driver": "overlay2"
}
```

---

## 8. Docker Compose

### 8.1 Docker Compose Basics

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - NGINX_HOST=example.com
    networks:
      - app-network

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
    driver: bridge
```

**Docker Compose Commands:**

```bash
# Start services
docker-compose up
docker-compose up -d              # Detached mode
docker-compose up --build         # Rebuild images

# Stop services
docker-compose stop

# Down (stop and remove)
docker-compose down
docker-compose down -v            # Remove volumes too

# View logs
docker-compose logs
docker-compose logs -f            # Follow
docker-compose logs web           # Specific service

# Execute command
docker-compose exec web /bin/bash
docker-compose exec db psql -U user -d mydb

# Scale services
docker-compose up -d --scale web=3

# List services
docker-compose ps

# View configuration
docker-compose config
```

### 8.2 Docker Compose Advanced

**Multiple Compose Files:**

```yaml
# docker-compose.yml (base)
version: '3.8'
services:
  web:
    image: nginx

# docker-compose.override.yml (development)
version: '3.8'
services:
  web:
    volumes:
      - ./src:/app
    ports:
      - "8080:80"

# docker-compose.prod.yml (production)
version: '3.8'
services:
  web:
    restart: always
    environment:
      - ENV=production
```

```bash
# Use specific file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# Use profiles
docker-compose --profile prod up
```

**Environment Variables:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: myapp
    environment:
      - VAR1=${VAR1}
      - VAR2=${VAR2:-default}
    env_file:
      - .env
      - .env.production
```

**Health Checks:**

```yaml
version: '3.8'
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  app:
    depends_on:
      web:
        condition: service_healthy
```

**Resource Limits:**

```yaml
version: '3.8'
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## 9. Multi-Stage Builds & Optimization

### 9.1 Multi-Stage Build Patterns

**Node.js Application:**

```dockerfile
# Stage 1: Dependencies
FROM node:18 AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
USER nodejs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Python Application:**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --user pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8000
CMD ["python", "app.py"]
```

**Go Application:**

```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# Stage 2: Minimal runtime
FROM scratch
COPY --from=builder /app/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

### 9.2 Image Optimization

**Layer Caching:**

```dockerfile
# ❌ BAD: Changes invalidate cache
FROM node:18
COPY . .
RUN npm install
RUN npm run build

# ✅ GOOD: Dependencies cached separately
FROM node:18
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
```

**Alpine Linux:**

```dockerfile
# Use Alpine for smaller images
FROM node:18-alpine
FROM python:3.11-alpine
FROM nginx:alpine
```

**Multi-architecture Builds:**

```bash
# Build for multiple architectures
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

**Image Slimming:**

```bash
# Use dive to analyze image layers
dive myapp:latest

# Use distroless images
FROM gcr.io/distroless/nodejs18-debian11
COPY dist /app
WORKDIR /app
CMD ["index.js"]
```

---

## 10. Container Security

### 10.1 Security Best Practices

**Non-Root User:**

```dockerfile
# Create and use non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

**Read-Only Filesystem:**

```dockerfile
# Make root filesystem read-only
# In docker run:
docker run --read-only --tmpfs /tmp nginx:latest
```

**Security Scanning:**

```bash
# Use Trivy
trivy image myapp:latest

# Use Docker Scout
docker scout cves myapp:latest

# Use Snyk
snyk test --docker myapp:latest
```

**Secrets Management:**

```bash
# Use Docker secrets (Swarm)
echo "mysecret" | docker secret create db_password -

# Use environment files
docker run --env-file .env myapp:latest

# Use external secret managers (HashiCorp Vault, AWS Secrets Manager)
```

**Image Security:**

```dockerfile
# Pin base image version
FROM node:18.17.0-alpine  # Not node:latest

# Use specific digest
FROM node@sha256:abc123...

# Keep images updated
# Regularly rebuild and scan
```

### 10.2 Runtime Security

**Capabilities:**

```bash
# Drop all capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx:latest

# List capabilities
docker run --cap-drop=ALL alpine sh -c 'capsh --print'
```

**AppArmor/SELinux:**

```bash
# Use security profiles
docker run --security-opt apparmor=docker-default nginx:latest
docker run --security-opt seccomp=default.json nginx:latest
```

**Network Security:**

```bash
# Use custom networks
docker network create --internal isolated-network

# Limit container networking
docker run --network none nginx:latest
```

---

## 11. Docker Swarm

### 11.1 Swarm Setup

**Initialize Swarm:**

```bash
# Initialize swarm
docker swarm init

# Join as worker
docker swarm join --token SWMTKN-1-xxx <manager-ip>:2377

# Join as manager
docker swarm join-token manager

# Leave swarm
docker swarm leave --force
```

**Node Management:**

```bash
# List nodes
docker node ls

# Inspect node
docker node inspect node_id

# Update node
docker node update --availability drain node_id
docker node update --role manager node_id

# Remove node
docker node rm node_id
```

### 11.2 Swarm Services

**Create Service:**

```bash
# Create service
docker service create --name web --replicas 3 nginx:latest

# Create service with options
docker service create \
  --name web \
  --replicas 3 \
  --publish 8080:80 \
  --update-delay 10s \
  --update-parallelism 1 \
  nginx:latest

# List services
docker service ls

# Inspect service
docker service inspect web

# Scale service
docker service scale web=5

# Update service
docker service update --image nginx:1.21 web
docker service update --replicas 5 web

# Remove service
docker service rm web
```

**Service Configuration:**

```yaml
# docker-stack.yml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    networks:
      - webnet

networks:
  webnet:
```

```bash
# Deploy stack
docker stack deploy -c docker-stack.yml mystack

# List stacks
docker stack ls

# List stack services
docker stack services mystack

# Remove stack
docker stack rm mystack
```

---

## 12. Alternative Container Runtimes

### 12.1 Podman

**Podman Basics:**

```bash
# Install Podman
sudo apt install podman

# Podman is daemonless and rootless
podman run hello-world
podman ps
podman images

# Most Docker commands work the same
podman build -t myapp .
podman run -d -p 8080:80 myapp

# Podman Compose
podman-compose up
```

**Podman Differences:**

```bash
# No daemon
podman run hello-world

# Rootless by default
podman run -d nginx  # Works as non-root

# Compatible with Docker commands
alias docker=podman
```

### 12.2 containerd

**containerd Basics:**

```bash
# containerd is the runtime Docker uses
ctr images pull docker.io/library/nginx:latest
ctr containers create docker.io/library/nginx:latest nginx1
ctr containers start nginx1

# Use crictl (Kubernetes runtime interface)
crictl images
crictl pods
crictl ps
```

### 12.3 Buildah & Skopeo

**Buildah:**

```bash
# Build images without Dockerfile
buildah from ubuntu:22.04
buildah run container_name apt-get update
buildah commit container_name myapp:latest

# Build from Dockerfile
buildah bud -t myapp:latest .
```

**Skopeo:**

```bash
# Copy images between registries
skopeo copy docker://nginx:latest docker://registry.example.com/nginx:latest

# Inspect images
skopeo inspect docker://nginx:latest
```

---

## 13. Container Monitoring & Logging

### 13.1 Container Monitoring

**Docker Stats:**

```bash
# Real-time stats
docker stats

# Stats for specific container
docker stats container_id

# One-time stats
docker stats --no-stream

# Format output
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

**cAdvisor:**

```bash
# Run cAdvisor
docker run -d \
  --name=cadvisor \
  -p 8080:8080 \
  -v /:/rootfs:ro \
  -v /var/run:/var/run:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker/:/var/lib/docker:ro \
  gcr.io/cadvisor/cadvisor:latest

# Access metrics at http://localhost:8080
```

### 13.2 Container Logging

**Docker Logs:**

```bash
# View logs
docker logs container_id

# Follow logs
docker logs -f container_id

# Last N lines
docker logs --tail 100 container_id

# Since timestamp
docker logs --since 2024-01-01T00:00:00 container_id

# Timestamps
docker logs -t container_id
```

**Logging Drivers:**

```bash
# Configure logging driver
docker run --log-driver json-file --log-opt max-size=10m nginx:latest

# Syslog driver
docker run --log-driver syslog nginx:latest

# GELF driver (Graylog)
docker run --log-driver gelf \
  --log-opt gelf-address=udp://graylog:12201 \
  nginx:latest
```

**Centralized Logging:**

```bash
# ELK Stack with Docker
docker-compose.yml:
version: '3.8'
services:
  elasticsearch:
    image: elasticsearch:8.0.0
  logstash:
    image: logstash:8.0.0
  kibana:
    image: kibana:8.0.0
    ports:
      - "5601:5601"
```

---

## 14. CI/CD Integration

### 14.1 GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            user/myapp:latest
            user/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 14.2 Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm myapp:${BUILD_NUMBER} npm test'
            }
        }
        
        stage('Push') {
            steps {
                sh 'docker tag myapp:${BUILD_NUMBER} registry.example.com/myapp:${BUILD_NUMBER}'
                sh 'docker push registry.example.com/myapp:${BUILD_NUMBER}'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.prod.yml up -d'
            }
        }
    }
}
```

### 14.3 GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  script:
    - docker run --rm $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA npm test

deploy:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

---

## 15. Best Practices & Patterns

### 15.1 Dockerfile Best Practices

1. **Use specific tags, not `latest`**
   ```dockerfile
   FROM node:18.17.0-alpine  # ✅
   FROM node:latest          # ❌
   ```

2. **Multi-stage builds for smaller images**
   ```dockerfile
   FROM node:18 AS builder
   # ... build ...
   FROM node:18-alpine
   COPY --from=builder /app/dist ./dist
   ```

3. **Order Dockerfile instructions**
   ```dockerfile
   # Copy dependency files first
   COPY package.json ./
   RUN npm install
   # Copy application code last
   COPY . .
   ```

4. **Use .dockerignore**
   ```
   node_modules
   .git
   .env
   *.log
   ```

5. **One process per container**
6. **Use non-root user**
7. **Minimize layers**
8. **Use health checks**

### 15.2 Container Patterns

**Sidecar Pattern:**

```yaml
version: '3.8'
services:
  app:
    image: myapp
  sidecar:
    image: logshipper
    volumes:
      - app-logs:/var/log
```

**Ambassador Pattern:**

```yaml
version: '3.8'
services:
  app:
    image: myapp
    depends_on:
      - db-proxy
  db-proxy:
    image: proxy
    # Routes to database
```

**Adapter Pattern:**

```yaml
version: '3.8'
services:
  app:
    image: myapp
  adapter:
    image: log-adapter
    # Normalizes logs from app
```

### 15.3 Troubleshooting

**Common Issues:**

```bash
# Container won't start
docker logs container_id
docker inspect container_id

# Out of disk space
docker system df
docker system prune -a

# Network issues
docker network inspect network_name
docker exec container_id ping other_container

# Permission issues
docker exec -u root container_id chown user:user /path

# Image pull failures
docker login
docker pull image:tag
```

**Debugging:**

```bash
# Execute shell in container
docker exec -it container_id /bin/bash

# Inspect container
docker inspect container_id

# View container processes
docker top container_id

# Monitor container
docker stats container_id
```

---

## Conclusion

### Key Takeaways:

1. **Containers provide isolation and portability**
2. **Multi-stage builds reduce image size**
3. **Use Docker Compose for multi-container apps**
4. **Security: non-root users, minimal images, scanning**
5. **Optimize layers for better caching**
6. **Monitor and log containers**
7. **Integrate with CI/CD pipelines**

### Essential Commands:

```bash
# Container management
docker run, docker ps, docker stop, docker rm

# Image management
docker build, docker images, docker push, docker pull

# Networking
docker network create, docker network connect

# Volumes
docker volume create, docker volume ls

# Compose
docker-compose up, docker-compose down, docker-compose logs
```

---

*Containerization in DevOps - Master Guide*
*Docker, Docker Compose, and Advanced Container Technologies*
*Last Updated: 2024*

