# Master-Level DevOps Interview Questions & Solutions
## Complete End-to-End Guide with Detailed Answers

---

## Table of Contents

1. [Linux & System Administration](#1-linux--system-administration)
2. [Docker & Containerization](#2-docker--containerization)
3. [Kubernetes & Orchestration](#3-kubernetes--orchestration)
4. [CI/CD Pipelines](#4-cicd-pipelines)
5. [Infrastructure as Code](#5-infrastructure-as-code)
6. [Cloud Platforms (AWS, Azure, GCP)](#6-cloud-platforms-aws-azure-gcp)
7. [Monitoring & Observability](#7-monitoring--observability)
8. [Networking & Security](#8-networking--security)
9. [Scripting & Automation](#9-scripting--automation)
10. [Database & Data Management](#10-database--data-management)
11. [Troubleshooting & Debugging](#11-troubleshooting--debugging)
12. [Architecture & Design](#12-architecture--design)
13. [Performance Optimization](#13-performance-optimization)
14. [Disaster Recovery & Backup](#14-disaster-recovery--backup)
15. [DevOps Best Practices](#15-devops-best-practices)

---

## 1. Linux & System Administration

### Q1.1: Process Management and Resource Monitoring

**Question:** A production server is experiencing high CPU usage. You need to:
1. Identify the top 5 processes consuming CPU
2. Kill a specific process that's consuming 90% CPU
3. Set up monitoring to alert when CPU exceeds 80%
4. Create a script to automatically kill processes exceeding 85% CPU for more than 5 minutes

**Solution:**

```bash
#!/bin/bash
# Part 1: Identify top 5 CPU-consuming processes
echo "Top 5 CPU-consuming processes:"
ps aux --sort=-%cpu | head -6

# Part 2: Kill specific high CPU process
HIGH_CPU_PID=$(ps aux --sort=-%cpu | awk 'NR==2 {print $2}')
if [ ! -z "$HIGH_CPU_PID" ]; then
    echo "Killing process $HIGH_CPU_PID"
    kill -9 $HIGH_CPU_PID
fi

# Part 3: CPU monitoring script
monitor_cpu() {
    while true; do
        CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
        if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
            echo "ALERT: CPU usage is ${CPU_USAGE}%"
            # Send alert (email, Slack, etc.)
            # send_alert "High CPU: ${CPU_USAGE}%"
        fi
        sleep 60
    done
}

# Part 4: Auto-kill high CPU processes
auto_kill_high_cpu() {
    while true; do
        ps aux | awk 'NR>1 {
            cpu=$3
            pid=$2
            cmd=$11
            if (cpu > 85) {
                print pid, cpu, cmd
                system("kill -9 " pid)
                system("logger -t high-cpu-killer \"Killed PID " pid " consuming " cpu "% CPU\"")
            }
        }'
        sleep 300  # Check every 5 minutes
    done
}

# Usage
# monitor_cpu &
# auto_kill_high_cpu &
```

**Key Points:**
- Use `ps aux --sort=-%cpu` for CPU sorting
- `top -bn1` for non-interactive CPU monitoring
- Always log actions when auto-killing processes
- Consider process priority before killing

---

### Q1.2: Disk Space Management and Cleanup

**Question:** A server is running out of disk space. Create a comprehensive script that:
1. Identifies the largest files and directories
2. Cleans up old log files (older than 30 days)
3. Removes Docker unused images and containers
4. Cleans up package manager cache
5. Generates a report of freed space

**Solution:**

```bash
#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/disk-cleanup.log"
THRESHOLD=80  # Alert if disk usage > 80%
DAYS_TO_KEEP=30

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_disk_usage() {
    local usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$usage" -gt "$THRESHOLD" ]; then
        log_message "WARNING: Disk usage is ${usage}%"
        return 0
    fi
    return 1
}

find_large_files() {
    log_message "Finding largest files..."
    echo "Top 10 largest files:" | tee -a "$LOG_FILE"
    find / -type f -size +100M 2>/dev/null | xargs ls -lh 2>/dev/null | \
        awk '{print $5, $9}' | sort -hr | head -10 | tee -a "$LOG_FILE"
}

find_large_directories() {
    log_message "Finding largest directories..."
    echo "Top 10 largest directories:" | tee -a "$LOG_FILE"
    du -h --max-depth=1 / 2>/dev/null | sort -hr | head -11 | tee -a "$LOG_FILE"
}

cleanup_old_logs() {
    log_message "Cleaning up logs older than $DAYS_TO_KEEP days..."
    local freed=0
    for log_dir in /var/log /var/log/apache2 /var/log/nginx /var/log/mysql; do
        if [ -d "$log_dir" ]; then
            local size_before=$(du -sm "$log_dir" 2>/dev/null | cut -f1)
            find "$log_dir" -type f -name "*.log" -mtime +$DAYS_TO_KEEP -delete
            find "$log_dir" -type f -name "*.log.*" -mtime +$DAYS_TO_KEEP -delete
            local size_after=$(du -sm "$log_dir" 2>/dev/null | cut -f1)
            freed=$((freed + size_before - size_after))
        fi
    done
    log_message "Freed ${freed}MB from old logs"
    echo $freed
}

cleanup_docker() {
    log_message "Cleaning up Docker..."
    local freed=0
    
    # Remove stopped containers
    local containers=$(docker ps -a -q -f status=exited | wc -l)
    if [ "$containers" -gt 0 ]; then
        docker container prune -f
        log_message "Removed stopped containers"
    fi
    
    # Remove unused images
    local images=$(docker images -q -f dangling=true | wc -l)
    if [ "$images" -gt 0 ]; then
        docker image prune -a -f
        log_message "Removed unused images"
    fi
    
    # Remove unused volumes
    docker volume prune -f
    log_message "Cleaned up Docker resources"
}

cleanup_package_cache() {
    log_message "Cleaning up package cache..."
    local freed=0
    
    if command -v apt-get &> /dev/null; then
        freed=$(du -sm /var/cache/apt 2>/dev/null | cut -f1)
        apt-get clean
        apt-get autoclean
        log_message "Freed ${freed}MB from APT cache"
    elif command -v yum &> /dev/null; then
        freed=$(du -sm /var/cache/yum 2>/dev/null | cut -f1)
        yum clean all
        log_message "Freed ${freed}MB from YUM cache"
    fi
    
    echo $freed
}

generate_report() {
    local total_freed=$1
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}')
    
    cat << EOF | tee -a "$LOG_FILE"
========================================
Disk Cleanup Report
========================================
Date: $(date)
Total Space Freed: ${total_freed}MB
Current Disk Usage: ${disk_usage}
========================================
EOF
}

main() {
    log_message "Starting disk cleanup..."
    
    if ! check_disk_usage; then
        log_message "Disk usage is below threshold. Exiting."
        exit 0
    fi
    
    find_large_files
    find_large_directories
    
    local total_freed=0
    total_freed=$((total_freed + $(cleanup_old_logs)))
    cleanup_docker
    total_freed=$((total_freed + $(cleanup_package_cache)))
    
    generate_report $total_freed
    log_message "Disk cleanup completed"
}

main "$@"
```

**Key Points:**
- Always check disk usage before cleanup
- Log all actions for audit trail
- Be cautious with `find /` - may take time
- Test cleanup scripts in non-production first
- Consider disk I/O impact during cleanup

---

### Q1.3: Network Troubleshooting and Configuration

**Question:** A server cannot connect to external services. Troubleshoot and fix:
1. Check network connectivity
2. Verify DNS resolution
3. Check firewall rules
4. Test specific ports
5. Create a network diagnostic script

**Solution:**

```bash
#!/bin/bash
set -euo pipefail

diagnose_network() {
    echo "=== Network Diagnostic Report ==="
    echo "Date: $(date)"
    echo ""
    
    # 1. Check network interfaces
    echo "1. Network Interfaces:"
    ip addr show
    echo ""
    
    # 2. Check routing table
    echo "2. Routing Table:"
    ip route show
    echo ""
    
    # 3. Check default gateway
    echo "3. Default Gateway:"
    ip route | grep default || echo "No default gateway configured!"
    echo ""
    
    # 4. Test connectivity
    echo "4. Connectivity Tests:"
    echo -n "  Localhost: "
    ping -c 1 127.0.0.1 > /dev/null 2>&1 && echo "OK" || echo "FAILED"
    
    echo -n "  Gateway: "
    GATEWAY=$(ip route | grep default | awk '{print $3}')
    if [ ! -z "$GATEWAY" ]; then
        ping -c 1 $GATEWAY > /dev/null 2>&1 && echo "OK" || echo "FAILED"
    else
        echo "No gateway found"
    fi
    
    echo -n "  External (8.8.8.8): "
    ping -c 1 8.8.8.8 > /dev/null 2>&1 && echo "OK" || echo "FAILED"
    
    echo -n "  DNS (google.com): "
    ping -c 1 google.com > /dev/null 2>&1 && echo "OK" || echo "FAILED"
    echo ""
    
    # 5. DNS resolution
    echo "5. DNS Resolution:"
    echo -n "  /etc/resolv.conf: "
    cat /etc/resolv.conf
    echo ""
    
    echo -n "  nslookup google.com: "
    nslookup google.com 2>&1 | head -2
    echo ""
    
    # 6. Check listening ports
    echo "6. Listening Ports:"
    ss -tuln | head -10
    echo ""
    
    # 7. Check firewall
    echo "7. Firewall Status:"
    if command -v ufw &> /dev/null; then
        ufw status verbose
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --list-all
    elif command -v iptables &> /dev/null; then
        iptables -L -n -v | head -20
    fi
    echo ""
    
    # 8. Test specific ports
    echo "8. Port Connectivity Tests:"
    test_port() {
        local host=$1
        local port=$2
        timeout 3 bash -c "echo > /dev/tcp/$host/$port" 2>/dev/null && \
            echo "  Port $port on $host: OPEN" || \
            echo "  Port $port on $host: CLOSED/FILTERED"
    }
    
    test_port "google.com" 80
    test_port "google.com" 443
    test_port "8.8.8.8" 53
    echo ""
    
    # 9. Network statistics
    echo "9. Network Statistics:"
    ss -s
    echo ""
    
    # 10. Recommendations
    echo "10. Recommendations:"
    if ! ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        echo "  - Check default gateway configuration"
        echo "  - Verify network interface is up"
    fi
    if ! ping -c 1 google.com > /dev/null 2>&1; then
        echo "  - Check DNS configuration in /etc/resolv.conf"
        echo "  - Verify DNS server is reachable"
    fi
}

fix_network() {
    echo "Attempting to fix network issues..."
    
    # Restart network service
    if systemctl is-active --quiet NetworkManager; then
        echo "Restarting NetworkManager..."
        systemctl restart NetworkManager
    elif systemctl is-active --quiet networking; then
        echo "Restarting networking service..."
        systemctl restart networking
    fi
    
    # Flush and renew DHCP
    for interface in $(ip link show | grep -E "^[0-9]+:" | awk -F: '{print $2}' | tr -d ' '); do
        if [ "$interface" != "lo" ]; then
            echo "Renewing DHCP for $interface..."
            dhclient -r $interface 2>/dev/null || true
            dhclient $interface 2>/dev/null || true
        fi
    done
    
    # Flush DNS cache
    if command -v systemd-resolve &> /dev/null; then
        systemd-resolve --flush-caches
    fi
}

# Main execution
case "${1:-diagnose}" in
    diagnose)
        diagnose_network
        ;;
    fix)
        fix_network
        sleep 5
        diagnose_network
        ;;
    *)
        echo "Usage: $0 [diagnose|fix]"
        exit 1
        ;;
esac
```

**Key Points:**
- Check connectivity layer by layer (local → gateway → external)
- DNS issues are common - always verify /etc/resolv.conf
- Firewall rules can block even if network is fine
- Use `ss` instead of deprecated `netstat`
- Test both ICMP (ping) and TCP connectivity

---

## 2. Docker & Containerization

### Q2.1: Multi-Stage Dockerfile Optimization

**Question:** Create an optimized multi-stage Dockerfile for a Node.js application that:
1. Minimizes image size
2. Uses build cache effectively
3. Runs as non-root user
4. Includes health checks
5. Handles secrets properly

**Solution:**

```dockerfile
# Stage 1: Build stage
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./

# Install dependencies (this layer will be cached if package.json doesn't change)
RUN npm ci --only=production && \
    npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production stage
FROM node:18-alpine AS production

# Install security updates
RUN apk update && \
    apk upgrade && \
    apk add --no-cache dumb-init && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Change ownership to non-root user
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/index.js"]
```

**Docker Compose with secrets:**

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production
    secrets:
      - db_password
      - api_key
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
    restart: unless-stopped
    networks:
      - app-network

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt

networks:
  app-network:
    driver: bridge
```

**Build and run commands:**

```bash
# Build with cache
docker build --target production -t myapp:latest .

# Build without cache
docker build --no-cache --target production -t myapp:latest .

# Run with security
docker run -d \
  --name myapp \
  --user nodejs \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /var/tmp \
  -p 3000:3000 \
  myapp:latest

# Check image size
docker images myapp

# Security scan
docker scan myapp:latest
```

**Key Points:**
- Multi-stage builds reduce final image size significantly
- Copy package.json first for better layer caching
- Always use non-root user in production
- Health checks enable proper orchestration
- Use secrets management, never hardcode credentials
- Alpine Linux reduces image size but may have compatibility issues

---

### Q2.2: Docker Networking and Service Discovery

**Question:** Set up a microservices architecture with Docker where:
1. Services can communicate via service names
2. Services are isolated in separate networks
3. A reverse proxy routes external traffic
4. Services can discover each other dynamically

**Solution:**

```yaml
version: '3.8'

services:
  # Reverse Proxy (Nginx)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - frontend
    depends_on:
      - api
      - web
    restart: unless-stopped

  # API Service
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    networks:
      - frontend
      - backend
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Web Service
  web:
    build:
      context: ./web
      dockerfile: Dockerfile
    environment:
      - API_URL=http://api:8080
    networks:
      - frontend
    depends_on:
      - api
    restart: unless-stopped

  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Service Discovery (Consul - optional)
  consul:
    image: consul:latest
    command: consul agent -dev -client=0.0.0.0
    ports:
      - "8500:8500"
    networks:
      - backend
    restart: unless-stopped

networks:
  frontend:
    driver: bridge
    name: frontend-network
  backend:
    driver: bridge
    name: backend-network
    internal: false  # Set to true to isolate from external access

volumes:
  postgres_data:
  redis_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**Nginx configuration for service routing:**

```nginx
upstream api_backend {
    least_conn;
    server api:8080 max_fails=3 fail_timeout=30s;
    # Add more API instances for load balancing
    # server api2:8080 max_fails=3 fail_timeout=30s;
}

upstream web_backend {
    least_conn;
    server web:3000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name example.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # API routes
    location /api/ {
        proxy_pass http://api_backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Health check endpoint
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }

    # Web routes
    location / {
        proxy_pass http://web_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

**Service discovery script:**

```bash
#!/bin/bash
# Service discovery using Docker DNS

discover_service() {
    local service_name=$1
    local port=${2:-80}
    
    # Docker DNS resolution
    getent hosts $service_name | awk '{print $1}'
}

# Example: Discover all services
discover_all_services() {
    echo "Discovering services in Docker network..."
    
    for service in api web postgres redis; do
        echo "Service: $service"
        ip=$(discover_service $service)
        if [ ! -z "$ip" ]; then
            echo "  IP: $ip"
            # Test connectivity
            if command -v nc &> /dev/null; then
                nc -zv $ip 80 2>&1 | grep -q succeeded && echo "  Status: UP" || echo "  Status: DOWN"
            fi
        else
            echo "  Status: NOT FOUND"
        fi
        echo ""
    done
}

# Run discovery
discover_all_services
```

**Key Points:**
- Docker Compose automatically creates DNS entries for service names
- Use separate networks for security isolation
- Health checks enable automatic failover
- Reverse proxy handles external routing
- Service discovery can use Docker DNS or external tools (Consul, etcd)

---

### Q2.3: Docker Security Hardening

**Question:** Implement security best practices for Docker containers:
1. Run containers as non-root
2. Use read-only file systems
3. Scan images for vulnerabilities
4. Implement resource limits
5. Use secrets management

**Solution:**

```bash
#!/bin/bash
# Docker security hardening script

# 1. Create non-root user Dockerfile template
cat > Dockerfile.secure << 'EOF'
FROM node:18-alpine

# Create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Install only necessary packages
RUN apk add --no-cache dumb-init

WORKDIR /app

# Copy files with correct ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Use read-only root filesystem
# Note: Requires tmpfs for /tmp
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "index.js"]
EOF

# 2. Security scanning
scan_image() {
    local image=$1
    echo "Scanning image: $image"
    
    # Using Trivy
    if command -v trivy &> /dev/null; then
        trivy image --severity HIGH,CRITICAL $image
    fi
    
    # Using Docker Scout (if available)
    docker scout cves $image
    
    # Using Snyk
    if command -v snyk &> /dev/null; then
        snyk test --docker $image
    fi
}

# 3. Secure Docker Compose
cat > docker-compose.secure.yml << 'EOF'
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.secure
    image: myapp:secure
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    security_opt:
      - no-new-privileges:true
      - apparmor:docker-default
      - seccomp:/etc/docker/seccomp/default.json
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed for port < 1024
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    networks:
      - secure-network
    restart: unless-stopped

networks:
  secure-network:
    driver: bridge
    internal: false
EOF

# 4. Docker daemon security configuration
configure_docker_daemon() {
    cat > /etc/docker/daemon.json << 'EOF'
{
  "userns-remap": "default",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp/default.json",
  "apparmor-profile": "docker-default"
}
EOF
    systemctl restart docker
}

# 5. Secrets management
setup_secrets() {
    # Create secrets directory
    mkdir -p ./secrets
    chmod 700 ./secrets
    
    # Generate secure passwords
    openssl rand -base64 32 > ./secrets/db_password.txt
    openssl rand -base64 32 > ./secrets/api_key.txt
    
    chmod 600 ./secrets/*.txt
    
    # Use Docker secrets in Compose
    cat >> docker-compose.secure.yml << 'EOF'
secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
EOF
}

# 6. Runtime security checks
runtime_security_check() {
    local container=$1
    
    echo "Checking security for container: $container"
    
    # Check if running as root
    local user=$(docker exec $container id -u)
    if [ "$user" = "0" ]; then
        echo "WARNING: Container running as root!"
    else
        echo "OK: Container running as UID $user"
    fi
    
    # Check capabilities
    docker inspect $container | jq '.[0].HostConfig.CapAdd'
    docker inspect $container | jq '.[0].HostConfig.CapDrop'
    
    # Check read-only filesystem
    local readonly=$(docker inspect $container | jq '.[0].HostConfig.ReadonlyRootfs')
    if [ "$readonly" = "true" ]; then
        echo "OK: Read-only root filesystem enabled"
    else
        echo "WARNING: Root filesystem is writable"
    fi
    
    # Check resource limits
    docker stats $container --no-stream --format "CPU: {{.CPUPerc}}, Memory: {{.MemUsage}}"
}

# 7. Network security
setup_network_security() {
    # Create isolated network
    docker network create \
        --driver bridge \
        --opt com.docker.network.bridge.enable_icc=false \
        --opt com.docker.network.bridge.enable_ip_masquerade=true \
        isolated-network
}

# Main execution
main() {
    echo "Setting up Docker security..."
    setup_secrets
    configure_docker_daemon
    setup_network_security
    echo "Security setup complete!"
    echo "Run: scan_image myapp:latest"
    echo "Run: runtime_security_check container_name"
}

main "$@"
```

**Key Points:**
- Always run containers as non-root users
- Use read-only filesystems with tmpfs for writable directories
- Drop all capabilities and add only what's needed
- Implement resource limits to prevent DoS
- Use secrets management, never environment variables for sensitive data
- Regularly scan images for vulnerabilities
- Use security profiles (AppArmor, SELinux, seccomp)

---

## 3. Kubernetes & Orchestration

### Q3.1: Kubernetes Deployment Strategy

**Question:** Implement a blue-green deployment strategy in Kubernetes with:
1. Zero-downtime deployment
2. Automatic rollback on failure
3. Traffic splitting between versions
4. Health check validation
5. Canary deployment option

**Solution:**

```yaml
# Blue Deployment (Current/Stable)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
    track: stable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
        track: stable
    spec:
      containers:
      - name: app
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
# Green Deployment (New Version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    version: green
    track: canary
spec:
  replicas: 0  # Start with 0, scale up during deployment
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
        track: canary
    spec:
      containers:
      - name: app
        image: myapp:v2.0.0
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
---
# Service (Routes to active version)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue  # Switch this label to change active version
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
# Ingress for external access
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

**Deployment script with rollback:**

```bash
#!/bin/bash
set -euo pipefail

NAMESPACE="default"
BLUE_DEPLOYMENT="myapp-blue"
GREEN_DEPLOYMENT="myapp-green"
SERVICE="myapp-service"
NEW_VERSION="v2.0.0"
HEALTH_CHECK_URL="http://myapp.example.com/health"
MAX_WAIT_TIME=300  # 5 minutes

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

check_deployment_health() {
    local deployment=$1
    local namespace=$2
    
    log "Checking health of $deployment..."
    
    # Wait for deployment to be ready
    if kubectl wait --for=condition=available \
        --timeout=${MAX_WAIT_TIME}s \
        deployment/$deployment -n $namespace; then
        log "$deployment is healthy"
        return 0
    else
        log "ERROR: $deployment failed to become healthy"
        return 1
    fi
}

check_service_health() {
    local url=$1
    local max_attempts=30
    local attempt=0
    
    log "Checking service health at $url..."
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s $url > /dev/null; then
            log "Service is healthy"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 10
    done
    
    log "ERROR: Service health check failed"
    return 1
}

switch_traffic() {
    local target_version=$1  # blue or green
    
    log "Switching traffic to $target_version..."
    
    # Update service selector
    kubectl patch service $SERVICE -n $NAMESPACE -p \
        "{\"spec\":{\"selector\":{\"version\":\"$target_version\"}}}"
    
    log "Traffic switched to $target_version"
}

rollback() {
    local from_version=$1
    local to_version=$2
    
    log "ROLLBACK: Switching from $from_version to $to_version"
    
    # Scale down failing deployment
    kubectl scale deployment/$from_version -n $NAMESPACE --replicas=0
    
    # Switch traffic back
    switch_traffic $to_version
    
    log "Rollback completed"
}

blue_green_deploy() {
    log "Starting blue-green deployment..."
    
    # Determine current active version
    CURRENT_VERSION=$(kubectl get service $SERVICE -n $NAMESPACE \
        -o jsonpath='{.spec.selector.version}')
    
    if [ "$CURRENT_VERSION" = "blue" ]; then
        ACTIVE_DEPLOYMENT=$BLUE_DEPLOYMENT
        STANDBY_DEPLOYMENT=$GREEN_DEPLOYMENT
        ACTIVE_VERSION="blue"
        STANDBY_VERSION="green"
    else
        ACTIVE_DEPLOYMENT=$GREEN_DEPLOYMENT
        STANDBY_DEPLOYMENT=$BLUE_DEPLOYMENT
        ACTIVE_VERSION="green"
        STANDBY_VERSION="blue"
    fi
    
    log "Current active version: $ACTIVE_VERSION"
    log "Deploying to: $STANDBY_VERSION"
    
    # Update standby deployment with new version
    kubectl set image deployment/$STANDBY_DEPLOYMENT \
        app=myapp:$NEW_VERSION -n $NAMESPACE
    
    # Scale up standby deployment
    kubectl scale deployment/$STANDBY_DEPLOYMENT -n $NAMESPACE --replicas=3
    
    # Wait for standby to be healthy
    if ! check_deployment_health $STANDBY_DEPLOYMENT $NAMESPACE; then
        log "ERROR: Standby deployment failed"
        kubectl scale deployment/$STANDBY_DEPLOYMENT -n $NAMESPACE --replicas=0
        exit 1
    fi
    
    # Switch traffic to new version
    switch_traffic $STANDBY_VERSION
    
    # Wait and verify service health
    sleep 30
    
    if ! check_service_health $HEALTH_CHECK_URL; then
        log "ERROR: Service health check failed after traffic switch"
        rollback $STANDBY_VERSION $ACTIVE_VERSION
        exit 1
    fi
    
    # Scale down old version
    log "Scaling down old version: $ACTIVE_VERSION"
    kubectl scale deployment/$ACTIVE_DEPLOYMENT -n $NAMESPACE --replicas=0
    
    log "Blue-green deployment completed successfully!"
}

canary_deploy() {
    local canary_percentage=${1:-10}  # Default 10%
    
    log "Starting canary deployment with $canary_percentage% traffic..."
    
    # Scale up green to handle canary traffic
    local canary_replicas=$((3 * canary_percentage / 100))
    [ $canary_replicas -eq 0 ] && canary_replicas=1
    
    kubectl scale deployment/$GREEN_DEPLOYMENT -n $NAMESPACE \
        --replicas=$canary_replicas
    
    # Use Istio or service mesh for traffic splitting
    # For simplicity, using manual replica management
    
    log "Canary deployment active with $canary_percentage% traffic"
    log "Monitor metrics and promote when ready"
}

# Main execution
case "${1:-blue-green}" in
    blue-green)
        blue_green_deploy
        ;;
    canary)
        canary_deploy ${2:-10}
        ;;
    rollback)
        rollback "green" "blue"
        ;;
    *)
        echo "Usage: $0 [blue-green|canary|rollback] [percentage]"
        exit 1
        ;;
esac
```

**Key Points:**
- Blue-green allows instant rollback by switching service selector
- Health checks are critical before traffic switch
- Always verify service health after switching
- Keep old version running briefly for quick rollback
- Canary deployments allow gradual traffic migration
- Use service mesh (Istio) for advanced traffic splitting

---

### Q3.2: Kubernetes Autoscaling

**Question:** Implement comprehensive autoscaling for a Kubernetes application:
1. Horizontal Pod Autoscaler (HPA)
2. Vertical Pod Autoscaler (VPA)
3. Cluster Autoscaler configuration
4. Custom metrics-based scaling
5. Scaling policies and behaviors

**Solution:**

```yaml
# Deployment with resource requests
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
# Horizontal Pod Autoscaler (HPA)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # Custom metrics (requires metrics server)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  # External metrics (from Prometheus)
  - type: External
    external:
      metric:
        name: queue_messages
        selector:
          matchLabels:
            queue: "task-queue"
      target:
        type: AverageValue
        averageValue: "50"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 minutes
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min  # Use the most conservative policy
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max  # Use the most aggressive policy
---
# Vertical Pod Autoscaler (VPA)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # Auto, Off, Initial, Recreate
  resourcePolicy:
    containerPolicies:
    - containerName: app
      minAllowed:
        cpu: 50m
        memory: 64Mi
      maxAllowed:
        cpu: 2
        memory: 2Gi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
---
# Cluster Autoscaler (Node Group configuration)
# Note: This is typically configured at cluster level
# Example for AWS EKS:
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler-status
  namespace: kube-system
data:
  nodes.min: "3"
  nodes.max: "10"
  scale-down-delay: "10m"
  scale-down-unneeded-time: "10m"
  scale-down-utilization-threshold: "0.5"
```

**Custom metrics setup (Prometheus Adapter):**

```yaml
# Prometheus Adapter for custom metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: adapter-config
  namespace: custom-metrics
data:
  config.yaml: |
    rules:
    - seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^(.*)_total"
        as: "${1}_per_second"
      metricsQuery: 'sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)'
    - seriesQuery: 'queue_messages{namespace!="",queue!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
      name:
        matches: "queue_messages"
        as: "queue_messages"
      metricsQuery: 'sum(<<.Series>>{<<.LabelMatchers>>}) by (<<.GroupBy>>)'
```

**Autoscaling monitoring script:**

```bash
#!/bin/bash
# Monitor autoscaling behavior

NAMESPACE="default"
DEPLOYMENT="myapp"

watch_autoscaling() {
    while true; do
        clear
        echo "=== Autoscaling Status ==="
        echo "Time: $(date)"
        echo ""
        
        # HPA Status
        echo "HPA Status:"
        kubectl get hpa $DEPLOYMENT-hpa -n $NAMESPACE
        echo ""
        
        # Current Replicas
        echo "Current Replicas:"
        kubectl get deployment $DEPLOYMENT -n $NAMESPACE \
            -o jsonpath='{.status.replicas}/{.spec.replicas}'
        echo ""
        
        # Pod Status
        echo "Pod Status:"
        kubectl get pods -l app=$DEPLOYMENT -n $NAMESPACE \
            -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,CPU:.spec.containers[0].resources.requests.cpu,MEM:.spec.containers[0].resources.requests.memory
        echo ""
        
        # Resource Usage
        echo "Resource Usage:"
        kubectl top pods -l app=$DEPLOYMENT -n $NAMESPACE 2>/dev/null || echo "Metrics not available"
        echo ""
        
        sleep 5
    done
}

test_autoscaling() {
    echo "Testing autoscaling with load..."
    
    # Create load (if you have a load testing tool)
    # kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- \
    #     /bin/sh -c "while true; do wget -q -O- http://myapp-service/; done"
    
    # Or use a proper load testing tool
    echo "Generating load..."
    # Add your load generation command here
    
    watch_autoscaling
}

# Main
case "${1:-watch}" in
    watch)
        watch_autoscaling
        ;;
    test)
        test_autoscaling
        ;;
    *)
        echo "Usage: $0 [watch|test]"
        exit 1
        ;;
esac
```

**Key Points:**
- HPA scales based on CPU, memory, or custom metrics
- VPA adjusts resource requests/limits based on usage
- Cluster Autoscaler adds/removes nodes based on demand
- Use stabilization windows to prevent flapping
- Custom metrics require metrics server or Prometheus adapter
- Test autoscaling behavior under load

---

### Q3.3: Kubernetes Troubleshooting

**Question:** Create a comprehensive troubleshooting guide and script for common Kubernetes issues:
1. Pods not starting
2. Services not accessible
3. Image pull errors
4. Resource constraints
5. Network connectivity issues

**Solution:**

```bash
#!/bin/bash
# Comprehensive Kubernetes troubleshooting script

set -euo pipefail

NAMESPACE="${1:-default}"
POD_NAME="${2:-}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Check cluster connectivity
check_cluster() {
    log_info "Checking cluster connectivity..."
    
    if kubectl cluster-info &> /dev/null; then
        log_info "Cluster is accessible"
        kubectl cluster-info
    else
        log_error "Cannot connect to cluster"
        return 1
    fi
    echo ""
}

# 2. Check node status
check_nodes() {
    log_info "Checking node status..."
    
    kubectl get nodes -o wide
    
    echo ""
    log_info "Node conditions:"
    kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .status.conditions[*]}{.type}={.status}{"\n"}{end}{end}' | \
        grep -v "Ready=True" && log_warn "Some nodes have issues" || log_info "All nodes are ready"
    echo ""
}

# 3. Check pods
check_pods() {
    log_info "Checking pods in namespace: $NAMESPACE"
    
    kubectl get pods -n $NAMESPACE -o wide
    
    echo ""
    log_info "Pods with issues:"
    kubectl get pods -n $NAMESPACE -o json | \
        jq -r '.items[] | select(.status.phase != "Running" or ([.status.containerStatuses[]? | select(.ready != true)] | length > 0)) | "\(.metadata.name)\t\(.status.phase)\t\(.status.containerStatuses[0].state | keys[0])"'
    echo ""
}

# 4. Diagnose specific pod
diagnose_pod() {
    local pod=$1
    local namespace=$2
    
    log_info "Diagnosing pod: $pod in namespace: $namespace"
    echo ""
    
    # Pod details
    log_info "Pod details:"
    kubectl describe pod $pod -n $namespace
    echo ""
    
    # Pod events
    log_info "Pod events:"
    kubectl get events -n $namespace --field-selector involvedObject.name=$pod --sort-by='.lastTimestamp'
    echo ""
    
    # Container status
    log_info "Container status:"
    kubectl get pod $pod -n $namespace -o jsonpath='{range .status.containerStatuses[*]}{.name}{"\t"}{.state}{"\n"}{end}'
    echo ""
    
    # Common issues
    local phase=$(kubectl get pod $pod -n $namespace -o jsonpath='{.status.phase}')
    
    case $phase in
        Pending)
            log_warn "Pod is Pending. Common causes:"
            echo "  - Insufficient resources"
            echo "  - Image pull issues"
            echo "  - PVC not bound"
            echo "  - Node selector/affinity issues"
            ;;
        ImagePullBackOff|ErrImagePull)
            log_error "Image pull failed. Checking:"
            local image=$(kubectl get pod $pod -n $namespace -o jsonpath='{.spec.containers[0].image}')
            echo "  Image: $image"
            echo "  Check image registry access"
            echo "  Check image pull secrets"
            kubectl get pod $pod -n $namespace -o jsonpath='{.spec.imagePullSecrets[*].name}'
            ;;
        CrashLoopBackOff)
            log_error "Container is crashing. Checking logs:"
            kubectl logs $pod -n $namespace --tail=50
            echo ""
            log_info "Previous container logs:"
            kubectl logs $pod -n $namespace --previous --tail=50
            ;;
        *)
            log_info "Pod phase: $phase"
            ;;
    esac
    echo ""
}

# 5. Check services
check_services() {
    log_info "Checking services in namespace: $NAMESPACE"
    
    kubectl get svc -n $NAMESPACE -o wide
    echo ""
    
    # Check endpoints
    log_info "Service endpoints:"
    for svc in $(kubectl get svc -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
        echo "Service: $svc"
        kubectl get endpoints $svc -n $NAMESPACE
        echo ""
    done
}

# 6. Check ingress
check_ingress() {
    log_info "Checking ingress:"
    
    kubectl get ingress -n $NAMESPACE -o wide
    echo ""
    
    # Ingress details
    for ing in $(kubectl get ingress -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}'); do
        log_info "Ingress details: $ing"
        kubectl describe ingress $ing -n $NAMESPACE
        echo ""
    done
}

# 7. Check resources
check_resources() {
    log_info "Checking resource usage:"
    
    # Node resources
    log_info "Node resources:"
    kubectl top nodes 2>/dev/null || log_warn "Metrics server not available"
    echo ""
    
    # Pod resources
    log_info "Pod resources:"
    kubectl top pods -n $NAMESPACE 2>/dev/null || log_warn "Metrics server not available"
    echo ""
    
    # Resource quotas
    log_info "Resource quotas:"
    kubectl get resourcequota -n $NAMESPACE
    echo ""
    
    # Limit ranges
    log_info "Limit ranges:"
    kubectl get limitrange -n $NAMESPACE
    echo ""
}

# 8. Check network policies
check_network() {
    log_info "Checking network policies:"
    
    kubectl get networkpolicies -n $NAMESPACE
    echo ""
    
    # Test connectivity
    log_info "Testing pod connectivity..."
    # This would require a test pod
    echo "  Create a test pod to verify connectivity"
    echo "  kubectl run -it --rm debug --image=busybox --restart=Never -- sh"
    echo ""
}

# 9. Check storage
check_storage() {
    log_info "Checking storage:"
    
    # PVCs
    log_info "Persistent Volume Claims:"
    kubectl get pvc -n $NAMESPACE
    echo ""
    
    # PVs
    log_info "Persistent Volumes:"
    kubectl get pv
    echo ""
    
    # Storage classes
    log_info "Storage Classes:"
    kubectl get storageclass
    echo ""
}

# 10. Check RBAC
check_rbac() {
    log_info "Checking RBAC:"
    
    # Service accounts
    log_info "Service accounts:"
    kubectl get sa -n $NAMESPACE
    echo ""
    
    # Roles and RoleBindings
    log_info "Roles:"
    kubectl get roles -n $NAMESPACE
    echo ""
    
    log_info "RoleBindings:"
    kubectl get rolebindings -n $NAMESPACE
    echo ""
}

# 11. Comprehensive report
full_diagnostic() {
    log_info "Running full diagnostic for namespace: $NAMESPACE"
    echo "=========================================="
    
    check_cluster
    check_nodes
    check_pods
    check_services
    check_ingress
    check_resources
    check_network
    check_storage
    check_rbac
    
    log_info "Diagnostic complete"
}

# 12. Quick fixes
quick_fix() {
    local issue=$1
    
    case $issue in
        image-pull)
            log_info "Fixing image pull issues..."
            echo "1. Check image pull secrets:"
            echo "   kubectl get secrets -n $NAMESPACE | grep docker"
            echo "2. Create image pull secret:"
            echo "   kubectl create secret docker-registry regcred \\"
            echo "     --docker-server=<registry> \\"
            echo "     --docker-username=<user> \\"
            echo "     --docker-password=<pass> \\"
            echo "     -n $NAMESPACE"
            echo "3. Add to deployment:"
            echo "   kubectl patch deployment <name> -n $NAMESPACE -p '{\"spec\":{\"template\":{\"spec\":{\"imagePullSecrets\":[{\"name\":\"regcred\"}]}}}}'"
            ;;
        resources)
            log_info "Fixing resource issues..."
            echo "1. Check resource quotas:"
            echo "   kubectl describe quota -n $NAMESPACE"
            echo "2. Check node resources:"
            echo "   kubectl describe nodes"
            echo "3. Scale down other workloads or add nodes"
            ;;
        pvc)
            log_info "Fixing PVC issues..."
            echo "1. Check PVC status:"
            echo "   kubectl get pvc -n $NAMESPACE"
            echo "2. Check storage class:"
            echo "   kubectl get storageclass"
            echo "3. Check PV:"
            echo "   kubectl get pv"
            ;;
        *)
            log_error "Unknown issue: $issue"
            echo "Available fixes: image-pull, resources, pvc"
            ;;
    esac
}

# Main execution
main() {
    case "${1:-full}" in
        full)
            full_diagnostic
            ;;
        pod)
            if [ -z "$POD_NAME" ]; then
                log_error "Pod name required"
                echo "Usage: $0 pod <pod-name> [namespace]"
                exit 1
            fi
            diagnose_pod "$POD_NAME" "$NAMESPACE"
            ;;
        nodes)
            check_nodes
            ;;
        services)
            check_services
            ;;
        resources)
            check_resources
            ;;
        fix)
            quick_fix "${2:-}"
            ;;
        *)
            echo "Usage: $0 [full|pod|nodes|services|resources|fix] [args...]"
            echo ""
            echo "Commands:"
            echo "  full              - Run full diagnostic"
            echo "  pod <name>        - Diagnose specific pod"
            echo "  nodes             - Check node status"
            echo "  services          - Check services"
            echo "  resources         - Check resource usage"
            echo "  fix <issue>       - Quick fix guide"
            exit 1
            ;;
    esac
}

main "$@"
```

**Key Points:**
- Always check pod events first - they contain error messages
- Image pull errors often indicate registry/auth issues
- Pending pods usually have resource or scheduling issues
- CrashLoopBackOff requires checking container logs
- Service connectivity issues often relate to selectors or endpoints
- Use `kubectl describe` for detailed information
- Check resource quotas and limits when pods can't be scheduled

---

## 4. CI/CD Pipelines

### Q4.1: Jenkins Pipeline for Multi-Environment Deployment

**Question:** Create a Jenkins pipeline that:
1. Builds and tests application
2. Deploys to dev, staging, and production
3. Includes approval gates
4. Implements rollback capability
5. Sends notifications

**Solution:**

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        DOCKER_CREDENTIALS = 'docker-registry-cred'
        KUBECTL_CONFIG = credentials('kubeconfig')
        SLACK_WEBHOOK = credentials('slack-webhook')
        APP_NAME = 'myapp'
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${APP_NAME}:${IMAGE_TAG}")
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh '''
                            docker run --rm \
                                ${APP_NAME}:${IMAGE_TAG} \
                                npm test
                        '''
                    }
                }
                stage('Lint') {
                    steps {
                        sh '''
                            docker run --rm \
                                ${APP_NAME}:${IMAGE_TAG} \
                                npm run lint
                        '''
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh '''
                            trivy image --severity HIGH,CRITICAL \
                                ${APP_NAME}:${IMAGE_TAG} || true
                        '''
                    }
                }
            }
            post {
                failure {
                    sendNotification('Tests failed', 'danger')
                }
            }
        }
        
        stage('Push Image') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS) {
                        docker.image("${APP_NAME}:${IMAGE_TAG}").push()
                        docker.image("${APP_NAME}:${IMAGE_TAG}").push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to Dev') {
            when {
                branch 'develop'
            }
            steps {
                deployToKubernetes('dev', IMAGE_TAG)
            }
            post {
                success {
                    sendNotification('Deployed to DEV', 'good')
                }
                failure {
                    sendNotification('DEV deployment failed', 'danger')
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'release/*'
            }
            steps {
                deployToKubernetes('staging', IMAGE_TAG)
            }
            post {
                success {
                    sendNotification('Deployed to STAGING', 'good')
                }
            }
        }
        
        stage('Approve Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    def userInput = input(
                        id: 'approval',
                        message: 'Approve production deployment?',
                        parameters: [
                            choice(
                                choices: ['Approve', 'Reject'],
                                description: 'Deployment approval',
                                name: 'action'
                            )
                        ]
                    )
                    if (userInput != 'Approve') {
                        error('Production deployment rejected')
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
                beforeInput true
            }
            steps {
                script {
                    try {
                        // Save previous version for rollback
                        sh '''
                            kubectl get deployment ${APP_NAME} -n production \
                                -o jsonpath='{.spec.template.spec.containers[0].image}' \
                                > previous-version.txt || echo "" > previous-version.txt
                        '''
                        
                        deployToKubernetes('production', IMAGE_TAG)
                        
                        // Wait for rollout
                        sh '''
                            kubectl rollout status deployment/${APP_NAME} \
                                -n production --timeout=5m
                        '''
                        
                        // Verify deployment
                        sh '''
                            sleep 30
                            curl -f https://myapp.example.com/health || exit 1
                        '''
                        
                    } catch (Exception e) {
                        // Automatic rollback on failure
                        rollbackDeployment('production')
                        throw e
                    }
                }
            }
            post {
                success {
                    sendNotification('Deployed to PRODUCTION', 'good')
                }
                failure {
                    sendNotification('PRODUCTION deployment failed - Rolled back', 'danger')
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh 'docker system prune -f || true'
            
            // Archive artifacts
            archiveArtifacts artifacts: '**/*.log', allowEmptyArchive: true
        }
        success {
            sendNotification("Pipeline succeeded: ${env.BUILD_URL}", 'good')
        }
        failure {
            sendNotification("Pipeline failed: ${env.BUILD_URL}", 'danger')
        }
    }
}

// Helper functions
def deployToKubernetes(String environment, String imageTag) {
    sh """
        export KUBECONFIG=${KUBECTL_CONFIG}
        kubectl set image deployment/${APP_NAME} \
            app=${DOCKER_REGISTRY}/${APP_NAME}:${imageTag} \
            -n ${environment}
    """
}

def rollbackDeployment(String environment) {
    script {
        def previousVersion = readFile('previous-version.txt').trim()
        if (previousVersion) {
            echo "Rolling back to: ${previousVersion}"
            sh """
                export KUBECONFIG=${KUBECTL_CONFIG}
                kubectl set image deployment/${APP_NAME} \
                    app=${previousVersion} \
                    -n ${environment}
                kubectl rollout status deployment/${APP_NAME} \
                    -n ${environment} --timeout=5m
            """
            sendNotification("Rolled back ${environment} to previous version", 'warning')
        } else {
            echo "No previous version found for rollback"
        }
    }
}

def sendNotification(String message, String color) {
    script {
        def payload = """
        {
            "text": "${message}",
            "attachments": [{
                "color": "${color}",
                "fields": [{
                    "title": "Build",
                    "value": "${env.BUILD_NUMBER}",
                    "short": true
                }, {
                    "title": "Branch",
                    "value": "${env.BRANCH_NAME}",
                    "short": true
                }, {
                    "title": "Commit",
                    "value": "${env.GIT_COMMIT_SHORT}",
                    "short": true
                }]
            }]
        }
        """
        
        sh """
            curl -X POST -H 'Content-type: application/json' \
                --data '${payload}' \
                ${SLACK_WEBHOOK}
        """
    }
}
```

**Key Points:**
- Use parallel stages for faster execution
- Implement approval gates for production
- Always save previous version for rollback
- Verify deployment health before considering success
- Send notifications for all important events
- Clean up resources in post actions

---

### Q4.2: GitHub Actions CI/CD Pipeline

**Question:** Create a GitHub Actions workflow for:
1. Multi-matrix builds (multiple OS/versions)
2. Automated testing
3. Docker image building and pushing
4. Kubernetes deployment
5. Security scanning

**Solution:**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ created ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run unit tests
      run: npm test -- --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage/lcov.info
        flags: unittests
        name: codecov-umbrella

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name != 'pull_request'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name != 'pull_request'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  deploy-dev:
    name: Deploy to Dev
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: development
      url: https://dev.myapp.example.com
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      uses: azure/setup-kubectl@v2
    
    - name: Set up kubeconfig
      run: |
        echo "${{ secrets.KUBECONFIG_DEV }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/myapp \
          app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n development
        kubectl rollout status deployment/myapp -n development --timeout=5m
    
    - name: Verify deployment
      run: |
        sleep 30
        curl -f https://dev.myapp.example.com/health || exit 1

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: startsWith(github.ref, 'refs/heads/release/')
    environment:
      name: staging
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      uses: azure/setup-kubectl@v2
    
    - name: Set up kubeconfig
      run: |
        echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/myapp \
          app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n staging
        kubectl rollout status deployment/myapp -n staging --timeout=5m

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://myapp.example.com
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Save previous version
      run: |
        export KUBECONFIG=<(echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d)
        kubectl get deployment/myapp -n production \
          -o jsonpath='{.spec.template.spec.containers[0].image}' \
          > previous-version.txt || echo "" > previous-version.txt
        echo "PREVIOUS_VERSION=$(cat previous-version.txt)" >> $GITHUB_ENV
    
    - name: Configure kubectl
      uses: azure/setup-kubectl@v2
    
    - name: Set up kubeconfig
      run: |
        echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
    
    - name: Deploy to Kubernetes
      id: deploy
      run: |
        kubectl set image deployment/myapp \
          app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          -n production
        kubectl rollout status deployment/myapp -n production --timeout=5m
    
    - name: Verify deployment
      run: |
        sleep 30
        curl -f https://myapp.example.com/health || exit 1
    
    - name: Rollback on failure
      if: failure()
      run: |
        if [ ! -z "$PREVIOUS_VERSION" ]; then
          kubectl set image deployment/myapp \
            app=$PREVIOUS_VERSION \
            -n production
          kubectl rollout status deployment/myapp -n production --timeout=5m
        fi

  notify:
    name: Notify
    runs-on: ubuntu-latest
    needs: [deploy-dev, deploy-staging, deploy-production]
    if: always()
    
    steps:
    - name: Send Slack notification
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployment ${{ job.status }}'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
      if: always()
```

**Key Points:**
- Use matrix strategy for testing multiple versions
- Cache dependencies for faster builds
- Scan images for vulnerabilities before deployment
- Use GitHub environments for approval gates
- Implement automatic rollback on failure
- Send notifications for deployment status

---

## 5. Infrastructure as Code

### Q5.1: Terraform Multi-Environment Setup

**Question:** Create a Terraform configuration for:
1. Multi-environment support (dev, staging, prod)
2. Modular structure
3. State management
4. Variable validation
5. Output values

**Solution:**

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  environment = var.environment
  vpc_cidr    = var.vpc_cidr
  
  tags = local.common_tags
}

# EKS Cluster Module
module "eks" {
  source = "./modules/eks"
  
  environment     = var.environment
  cluster_name    = "${var.project_name}-${var.environment}"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  node_group_size = var.environment == "production" ? 3 : 1
  
  tags = local.common_tags
}

# RDS Module
module "rds" {
  source = "./modules/rds"
  
  environment        = var.environment
  db_instance_class  = var.environment == "production" ? "db.r5.large" : "db.t3.micro"
  allocated_storage  = var.environment == "production" ? 100 : 20
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnet_ids
  allowed_cidr_blocks = module.vpc.private_subnet_cidrs
  
  tags = local.common_tags
}

# S3 Bucket Module
module "s3" {
  source = "./modules/s3"
  
  environment = var.environment
  bucket_name = "${var.project_name}-${var.environment}-storage"
  
  versioning_enabled = var.environment == "production"
  lifecycle_rules = var.environment == "production" ? [
    {
      id      = "delete-old-versions"
      enabled = true
      noncurrent_version_expiration_days = 90
    }
  ] : []
  
  tags = local.common_tags
}
```

```hcl
# variables.tf
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
  
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid CIDR block."
  }
}

# Environment-specific variables
variable "instance_types" {
  description = "EC2 instance types by environment"
  type = map(string)
  default = {
    dev        = "t3.micro"
    staging    = "t3.small"
    production = "t3.medium"
  }
}
```

```hcl
# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = false
}

output "eks_cluster_ca_certificate" {
  description = "EKS cluster CA certificate"
  value       = module.eks.cluster_ca_certificate
  sensitive   = true
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = module.s3.bucket_name
}
```

```hcl
# modules/vpc/main.tf
variable "environment" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "tags" {
  type = map(string)
  default = {}
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-vpc"
    }
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-igw"
    }
  )
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone        = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-public-subnet-${count.index + 1}"
      Type = "public"
    }
  )
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 2)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-private-subnet-${count.index + 1}"
      Type = "private"
    }
  )
}

data "aws_availability_zones" "available" {
  state = "available"
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "private_subnet_cidrs" {
  value = aws_subnet.private[*].cidr_block
}
```

```hcl
# terraform.tfvars.example
environment = "dev"
aws_region  = "us-east-1"
project_name = "myapp"
vpc_cidr    = "10.0.0.0/16"
```

**Deployment script:**

```bash
#!/bin/bash
# deploy.sh - Terraform deployment script

set -euo pipefail

ENVIRONMENT="${1:-dev}"
ACTION="${2:-plan}"

if [ ! -f "terraform.tfvars.${ENVIRONMENT}" ]; then
    echo "Error: terraform.tfvars.${ENVIRONMENT} not found"
    exit 1
fi

# Initialize Terraform
terraform init \
    -backend-config="key=${ENVIRONMENT}/terraform.tfstate" \
    -reconfigure

# Select workspace
terraform workspace select $ENVIRONMENT || terraform workspace new $ENVIRONMENT

# Validate
terraform validate

# Format check
terraform fmt -check

case $ACTION in
    plan)
        terraform plan \
            -var-file="terraform.tfvars.${ENVIRONMENT}" \
            -out=tfplan
        ;;
    apply)
        terraform apply \
            -var-file="terraform.tfvars.${ENVIRONMENT}" \
            -auto-approve
        ;;
    destroy)
        read -p "Are you sure you want to destroy ${ENVIRONMENT}? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            terraform destroy \
                -var-file="terraform.tfvars.${ENVIRONMENT}" \
                -auto-approve
        fi
        ;;
    *)
        echo "Usage: $0 <environment> [plan|apply|destroy]"
        exit 1
        ;;
esac
```

**Key Points:**
- Use modules for reusability
- Separate state files per environment
- Use workspaces or separate state backends
- Validate variables to prevent errors
- Use remote state with locking (DynamoDB)
- Tag all resources for cost tracking
- Use sensitive outputs for secrets

---

## 6. Cloud Platforms (AWS, Azure, GCP)

### Q6.1: AWS High Availability Architecture

**Question:** Design and implement a highly available web application on AWS with:
1. Multi-AZ deployment
2. Auto-scaling groups
3. Load balancing
4. Database replication
5. Disaster recovery plan

**Solution:**

```bash
#!/bin/bash
# AWS High Availability Setup Script

# 1. Create VPC with multiple AZs
aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=HA-VPC}]'

VPC_ID=$(aws ec2 describe-vpcs \
    --filters "Name=tag:Name,Values=HA-VPC" \
    --query 'Vpcs[0].VpcId' --output text)

# 2. Create subnets in multiple AZs
for i in 0 1 2; do
    AZ=$(aws ec2 describe-availability-zones \
        --query "AvailabilityZones[$i].ZoneName" --output text)
    
    # Public subnet
    aws ec2 create-subnet \
        --vpc-id $VPC_ID \
        --cidr-block "10.0.$((i+1)).0/24" \
        --availability-zone $AZ \
        --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=Public-Subnet-$((i+1))}]"
    
    # Private subnet
    aws ec2 create-subnet \
        --vpc-id $VPC_ID \
        --cidr-block "10.0.$((i+10)).0/24" \
        --availability-zone $AZ \
        --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=Private-Subnet-$((i+1))}]"
done

# 3. Create Application Load Balancer
aws elbv2 create-load-balancer \
    --name ha-alb \
    --subnets $(aws ec2 describe-subnets \
        --filters "Name=tag:Name,Values=Public-Subnet-*" \
        --query 'Subnets[*].SubnetId' --output text | tr '\t' ' ') \
    --scheme internet-facing \
    --type application

# 4. Create Launch Template for Auto Scaling
aws ec2 create-launch-template \
    --launch-template-name ha-app-template \
    --launch-template-data '{
        "ImageId": "ami-0c55b159cbfafe1f0",
        "InstanceType": "t3.medium",
        "SecurityGroupIds": ["sg-xxxxx"],
        "UserData": "'"$(base64 -w 0 user-data.sh)"'",
        "IamInstanceProfile": {"Name": "EC2-Role"}
    }'

# 5. Create Auto Scaling Group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name ha-app-asg \
    --launch-template LaunchTemplateName=ha-app-template,Version='$Latest' \
    --min-size 2 \
    --max-size 10 \
    --desired-capacity 3 \
    --vpc-zone-identifier "$(aws ec2 describe-subnets \
        --filters 'Name=tag:Name,Values=Private-Subnet-*' \
        --query 'Subnets[*].SubnetId' --output text | tr '\t' ',')" \
    --health-check-type ELB \
    --health-check-grace-period 300 \
    --target-group-arns $(aws elbv2 describe-target-groups \
        --names ha-app-tg --query 'TargetGroups[0].TargetGroupArn' --output text)

# 6. Create RDS Multi-AZ Database
aws rds create-db-instance \
    --db-instance-identifier ha-db-primary \
    --db-instance-class db.t3.medium \
    --engine mysql \
    --engine-version 8.0 \
    --master-username admin \
    --master-user-password $(openssl rand -base64 32) \
    --allocated-storage 100 \
    --storage-type gp3 \
    --multi-az \
    --db-subnet-group-name ha-db-subnet-group \
    --vpc-security-group-ids sg-xxxxx \
    --backup-retention-period 7 \
    --enable-cloudwatch-logs-exports '["audit","error","general","slowquery"]'

# 7. Create Read Replicas
for i in 1 2; do
    aws rds create-db-instance-read-replica \
        --db-instance-identifier ha-db-replica-$i \
        --source-db-instance-identifier ha-db-primary \
        --db-instance-class db.t3.medium \
        --availability-zone $(aws ec2 describe-availability-zones \
            --query "AvailabilityZones[$i].ZoneName" --output text)
done
```

**Terraform Configuration:**

```hcl
# modules/aws-ha/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.project_name}-private-${count.index + 1}"
  }
}

resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = var.environment == "production"
  
  tags = {
    Name = "${var.project_name}-alb"
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-asg"
  vpc_zone_identifier  = aws_subnet.private[*].id
  target_group_arns    = [aws_lb_target_group.app.arn]
  health_check_type    = "ELB"
  min_size             = var.min_instances
  max_size             = var.max_instances
  desired_capacity      = var.desired_instances
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-instance"
    propagate_at_launch = true
  }
}

resource "aws_db_instance" "primary" {
  identifier             = "${var.project_name}-db-primary"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.db_instance_class
  allocated_storage      = var.allocated_storage
  storage_type          = "gp3"
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  multi_az               = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  backup_retention_period = 7
  skip_final_snapshot    = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  tags = {
    Name = "${var.project_name}-db-primary"
  }
}

resource "aws_db_instance" "replica" {
  count = var.environment == "production" ? 2 : 0
  
  identifier             = "${var.project_name}-db-replica-${count.index + 1}"
  replicate_source_db    = aws_db_instance.primary.identifier
  instance_class         = var.db_instance_class
  publicly_accessible    = false
  availability_zone      = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.project_name}-db-replica-${count.index + 1}"
  }
}
```

**Key Points:**
- Always use multiple Availability Zones for high availability
- Implement auto-scaling for dynamic capacity management
- Use Multi-AZ RDS for automatic failover
- Create read replicas for read scaling and disaster recovery
- Use Application Load Balancer for layer 7 routing
- Implement health checks at all levels
- Regular backups with point-in-time recovery

---

### Q6.2: Azure DevOps CI/CD with ARM Templates

**Question:** Create an Azure DevOps pipeline that:
1. Builds and tests application
2. Deploys infrastructure using ARM templates
3. Deploys application to Azure App Service
4. Implements blue-green deployment
5. Includes rollback capability

**Solution:**

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
      - release/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: azure-credentials
  - name: serviceConnection
    value: 'Azure-ServiceConnection'
  - name: resourceGroup
    value: 'myapp-rg'
  - name: location
    value: 'eastus'

stages:
- stage: Build
  displayName: 'Build and Test'
  jobs:
  - job: Build
    displayName: 'Build Application'
    steps:
    - task: NodeTool@0
      inputs:
        versionSpec: '18.x'
      displayName: 'Install Node.js'
    
    - script: |
        npm ci
        npm run build
        npm test
      displayName: 'Build and Test'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test-results.xml'
        failTaskOnFailedTests: true
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: 'Cobertura'
        summaryFileLocation: '**/coverage/cobertura-coverage.xml'

- stage: Infrastructure
  displayName: 'Deploy Infrastructure'
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployInfrastructure
    displayName: 'Deploy ARM Template'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureResourceManagerTemplateDeployment@3
            inputs:
              deploymentScope: 'Resource Group'
              azureResourceManagerConnection: $(serviceConnection)
              subscriptionId: '$(subscriptionId)'
              action: 'Create Or Update Resource Group'
              resourceGroupName: $(resourceGroup)
              location: $(location)
              templateLocation: 'Linked artifact'
              csmFile: 'infrastructure/main.json'
              csmParametersFile: 'infrastructure/parameters.json'
              deploymentMode: 'Incremental'

- stage: Deploy
  displayName: 'Deploy Application'
  dependsOn: Infrastructure
  condition: succeeded()
  jobs:
  - deployment: DeployApp
    displayName: 'Deploy to App Service'
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: $(serviceConnection)
              appName: 'myapp-prod'
              package: '$(System.DefaultWorkingDirectory)/dist'
              deploymentMethod: 'auto'
```

**ARM Template:**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "appName": {
      "type": "string",
      "defaultValue": "myapp"
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2021-02-01",
      "name": "[concat(parameters('appName'), '-plan')]",
      "location": "[parameters('location')]",
      "sku": {
        "name": "S1",
        "tier": "Standard"
      },
      "properties": {
        "reserved": true
      }
    },
    {
      "type": "Microsoft.Web/sites",
      "apiVersion": "2021-02-01",
      "name": "[concat(parameters('appName'), '-prod')]",
      "location": "[parameters('location')]",
      "dependsOn": [
        "[resourceId('Microsoft.Web/serverfarms', concat(parameters('appName'), '-plan'))]"
      ],
      "properties": {
        "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', concat(parameters('appName'), '-plan'))]",
        "siteConfig": {
          "linuxFxVersion": "NODE|18-lts",
          "alwaysOn": true,
          "http20Enabled": true,
          "minTlsVersion": "1.2"
        },
        "httpsOnly": true
      }
    },
    {
      "type": "Microsoft.Insights/components",
      "apiVersion": "2020-02-02",
      "name": "[concat(parameters('appName'), '-insights')]",
      "location": "[parameters('location')]",
      "kind": "web",
      "properties": {
        "Application_Type": "web"
      }
    }
  ]
}
```

**Key Points:**
- Use ARM templates for infrastructure as code
- Implement deployment slots for blue-green deployments
- Use Azure DevOps environments for approval gates
- Monitor deployments with Application Insights
- Implement rollback using deployment slots

---

## 7. Monitoring & Observability

### Q7.1: Prometheus and Grafana Setup

**Question:** Set up comprehensive monitoring with:
1. Prometheus for metrics collection
2. Grafana for visualization
3. Alertmanager for alerting
4. Custom application metrics
5. Dashboard creation

**Solution:**

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - "9090:9090"
    networks:
      - monitoring
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    ports:
      - "9093:9093"
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - monitoring
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    ports:
      - "9100:9100"
    networks:
      - monitoring
    restart: unless-stopped

volumes:
  prometheus_data:
  alertmanager_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

**Prometheus Configuration:**

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

rule_files:
  - '/etc/prometheus/rules/*.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'application'
    static_configs:
      - targets: ['app:8080']
    metrics_path: '/metrics'
```

**Alert Rules:**

```yaml
# prometheus/rules/alerts.yml
groups:
  - name: application_alerts
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

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is above 80%"

      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is above 85%"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod is crash looping"
          description: "Pod {{ $labels.pod }} is restarting frequently"
```

**Alertmanager Configuration:**

```yaml
# alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '${SLACK_WEBHOOK_URL}'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'slack-critical'
      continue: true
    - match:
        severity: warning
      receiver: 'slack-warning'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-warning'
    slack_configs:
      - channel: '#alerts'
        title: '⚠️ WARNING: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

**Grafana Dashboard JSON (Example):**

```json
{
  "dashboard": {
    "title": "Application Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "Errors"
          }
        ],
        "type": "graph"
      },
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{instance}}"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

**Key Points:**
- Use Prometheus for time-series metrics collection
- Configure alert rules with appropriate thresholds
- Use Alertmanager for alert routing and grouping
- Create Grafana dashboards for visualization
- Export custom application metrics
- Set up proper retention policies
- Test alerting rules regularly

---

## 8. Networking & Security

### Q8.1: Network Security and Firewall Configuration

**Question:** Implement network security for a multi-tier application:
1. Network segmentation
2. Firewall rules
3. WAF configuration
4. DDoS protection
5. VPN setup

**Solution:**

```bash
#!/bin/bash
# Network Security Configuration Script

# 1. Create Security Groups (AWS example)
create_security_groups() {
    VPC_ID=$1
    
    # Web tier security group
    WEB_SG=$(aws ec2 create-security-group \
        --group-name web-tier-sg \
        --description "Web tier security group" \
        --vpc-id $VPC_ID \
        --query 'GroupId' --output text)
    
    # Allow HTTP/HTTPS from internet
    aws ec2 authorize-security-group-ingress \
        --group-id $WEB_SG \
        --protocol tcp \
        --port 80 \
        --cidr 0.0.0.0/0
    
    aws ec2 authorize-security-group-ingress \
        --group-id $WEB_SG \
        --protocol tcp \
        --port 443 \
        --cidr 0.0.0.0/0
    
    # App tier security group
    APP_SG=$(aws ec2 create-security-group \
        --group-name app-tier-sg \
        --description "Application tier security group" \
        --vpc-id $VPC_ID \
        --query 'GroupId' --output text)
    
    # Allow traffic only from web tier
    aws ec2 authorize-security-group-ingress \
        --group-id $APP_SG \
        --protocol tcp \
        --port 8080 \
        --source-group $WEB_SG
    
    # Database tier security group
    DB_SG=$(aws ec2 create-security-group \
        --group-name db-tier-sg \
        --description "Database tier security group" \
        --vpc-id $VPC_ID \
        --query 'GroupId' --output text)
    
    # Allow MySQL only from app tier
    aws ec2 authorize-security-group-ingress \
        --group-id $DB_SG \
        --protocol tcp \
        --port 3306 \
        --source-group $APP_SG
}

# 2. Configure WAF Rules
configure_waf() {
    # Create WAF Web ACL
    aws wafv2 create-web-acl \
        --name production-waf \
        --scope REGIONAL \
        --default-action Allow={} \
        --rules file://waf-rules.json \
        --visibility-config \
            SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=production-waf
}

# 3. Network ACLs (Additional layer)
configure_nacls() {
    VPC_ID=$1
    
    # Get default NACL
    DEFAULT_NACL=$(aws ec2 describe-network-acls \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=default,Values=true" \
        --query 'NetworkAcls[0].NetworkAclId' --output text)
    
    # Deny all inbound by default, then allow specific
    # (NACLs are stateless, need both inbound and outbound rules)
}
```

**Terraform Security Configuration:**

```hcl
# Security Groups
resource "aws_security_group" "web" {
  name        = "web-tier-sg"
  description = "Security group for web tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-tier-sg"
    Tier = "web"
  }
}

resource "aws_security_group" "app" {
  name        = "app-tier-sg"
  description = "Security group for application tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "App port from web tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app-tier-sg"
    Tier = "app"
  }
}

resource "aws_security_group" "db" {
  name        = "db-tier-sg"
  description = "Security group for database tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL from app tier"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "db-tier-sg"
    Tier = "db"
  }
}

# WAF
resource "aws_wafv2_web_acl" "main" {
  name        = "production-waf"
  description = "WAF for production"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 2

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "KnownBadInputsRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "production-waf"
    sampled_requests_enabled   = true
  }
}

# Associate WAF with ALB
resource "aws_wafv2_web_acl_association" "main" {
  resource_arn = aws_lb.main.arn
  web_acl_arn  = aws_wafv2_web_acl.main.arn
}
```

**Key Points:**
- Implement defense in depth with multiple security layers
- Use security groups for instance-level firewall
- Use NACLs for subnet-level filtering
- Configure WAF for application-layer protection
- Implement least privilege principle
- Regularly audit and update security rules
- Monitor security events and alerts

---

## 9. Scripting & Automation

### Q9.1: Infrastructure Automation Script

**Question:** Create a comprehensive automation script that:
1. Provisions infrastructure
2. Configures applications
3. Deploys code
4. Runs health checks
5. Handles rollback

**Solution:**

```bash
#!/bin/bash
# Complete Infrastructure Automation Script

set -euo pipefail

ENVIRONMENT="${1:-dev}"
ACTION="${2:-deploy}"
ROLLBACK_VERSION="${3:-}"

# Configuration
CONFIG_FILE="config/${ENVIRONMENT}.conf"
LOG_FILE="logs/deployment-$(date +%Y%m%d-%H%M%S).log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

# Load configuration
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "Configuration file not found: $CONFIG_FILE"
        exit 1
    fi
    source "$CONFIG_FILE"
    log "Loaded configuration for $ENVIRONMENT"
}

# Provision infrastructure
provision_infrastructure() {
    log "Provisioning infrastructure..."
    
    cd infrastructure
    
    terraform init -backend-config="key=${ENVIRONMENT}/terraform.tfstate"
    terraform workspace select $ENVIRONMENT || terraform workspace new $ENVIRONMENT
    
    if [ "$ACTION" = "plan" ]; then
        terraform plan -var-file="../config/${ENVIRONMENT}.tfvars" -out=tfplan
        log "Infrastructure plan created"
    else
        terraform apply -var-file="../config/${ENVIRONMENT}.tfvars" -auto-approve
        log "Infrastructure provisioned"
    fi
    
    cd ..
}

# Build application
build_application() {
    log "Building application..."
    
    docker build -t ${APP_NAME}:${VERSION} .
    docker tag ${APP_NAME}:${VERSION} ${REGISTRY}/${APP_NAME}:${VERSION}
    docker tag ${APP_NAME}:${VERSION} ${REGISTRY}/${APP_NAME}:latest
    
    log "Application built: ${APP_NAME}:${VERSION}"
}

# Run tests
run_tests() {
    log "Running tests..."
    
    docker run --rm ${APP_NAME}:${VERSION} npm test || {
        log_error "Tests failed"
        exit 1
    }
    
    docker run --rm ${APP_NAME}:${VERSION} npm run lint || {
        log_error "Linting failed"
        exit 1
    }
    
    log "All tests passed"
}

# Push to registry
push_image() {
    log "Pushing image to registry..."
    
    docker login -u ${REGISTRY_USER} -p ${REGISTRY_PASSWORD} ${REGISTRY}
    docker push ${REGISTRY}/${APP_NAME}:${VERSION}
    docker push ${REGISTRY}/${APP_NAME}:latest
    
    log "Image pushed successfully"
}

# Deploy to Kubernetes
deploy_kubernetes() {
    log "Deploying to Kubernetes..."
    
    # Save current version
    CURRENT_VERSION=$(kubectl get deployment ${APP_NAME} -n ${NAMESPACE} \
        -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null || echo "")
    echo "$CURRENT_VERSION" > .current-version
    
    # Update deployment
    kubectl set image deployment/${APP_NAME} \
        app=${REGISTRY}/${APP_NAME}:${VERSION} \
        -n ${NAMESPACE}
    
    # Wait for rollout
    kubectl rollout status deployment/${APP_NAME} \
        -n ${NAMESPACE} --timeout=5m || {
        log_error "Deployment failed"
        rollback_deployment
        exit 1
    }
    
    log "Deployment successful"
}

# Health check
health_check() {
    log "Running health checks..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s ${HEALTH_CHECK_URL} > /dev/null; then
            log "Health check passed"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 10
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Rollback
rollback_deployment() {
    log_warn "Initiating rollback..."
    
    if [ ! -z "$ROLLBACK_VERSION" ]; then
        VERSION_TO_ROLLBACK=$ROLLBACK_VERSION
    elif [ -f .current-version ]; then
        VERSION_TO_ROLLBACK=$(cat .current-version)
    else
        log_error "No version to rollback to"
        return 1
    fi
    
    log "Rolling back to: $VERSION_TO_ROLLBACK"
    
    kubectl set image deployment/${APP_NAME} \
        app=$VERSION_TO_ROLLBACK \
        -n ${NAMESPACE}
    
    kubectl rollout status deployment/${APP_NAME} \
        -n ${NAMESPACE} --timeout=5m
    
    log "Rollback completed"
}

# Main deployment flow
main_deploy() {
    log "Starting deployment to $ENVIRONMENT"
    
    load_config
    provision_infrastructure
    build_application
    run_tests
    push_image
    deploy_kubernetes
    
    if ! health_check; then
        log_error "Health check failed, rolling back..."
        rollback_deployment
        exit 1
    fi
    
    log "Deployment completed successfully!"
}

# Main execution
case "$ACTION" in
    deploy)
        main_deploy
        ;;
    rollback)
        load_config
        rollback_deployment
        ;;
    plan)
        load_config
        provision_infrastructure
        ;;
    *)
        echo "Usage: $0 <environment> [deploy|rollback|plan] [rollback-version]"
        exit 1
        ;;
esac
```

**Key Points:**
- Always load configuration from files
- Implement proper error handling and logging
- Save current version before deployment for rollback
- Run health checks after deployment
- Automatically rollback on failure
- Use idempotent operations
- Log all actions for audit trail

---

## 10. Database & Data Management

### Q10.1: Database Backup and Recovery Strategy

**Question:** Implement a comprehensive database backup and recovery strategy:
1. Automated backups
2. Point-in-time recovery
3. Cross-region replication
4. Backup testing
5. Disaster recovery procedures

**Solution:**

```bash
#!/bin/bash
# Database Backup and Recovery Script

set -euo pipefail

DB_TYPE="${1:-mysql}"
BACKUP_TYPE="${2:-full}"  # full, incremental
RETENTION_DAYS=30
S3_BUCKET="db-backups-$(date +%Y%m%d)"
BACKUP_DIR="/backup/$(date +%Y%m%d)"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# MySQL Backup
mysql_backup() {
    local db_name=$1
    local backup_file="${BACKUP_DIR}/${db_name}-$(date +%Y%m%d-%H%M%S).sql"
    
    log "Starting MySQL backup: $db_name"
    
    mysqldump \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --master-data=2 \
        --flush-logs \
        $db_name > $backup_file
    
    # Compress
    gzip $backup_file
    backup_file="${backup_file}.gz"
    
    # Upload to S3
    aws s3 cp $backup_file s3://${S3_BUCKET}/mysql/
    
    log "Backup completed: $backup_file"
    echo $backup_file
}

# PostgreSQL Backup
postgres_backup() {
    local db_name=$1
    local backup_file="${BACKUP_DIR}/${db_name}-$(date +%Y%m%d-%H%M%S).dump"
    
    log "Starting PostgreSQL backup: $db_name"
    
    pg_dump \
        -Fc \
        -f $backup_file \
        $db_name
    
    # Upload to S3
    aws s3 cp $backup_file s3://${S3_BUCKET}/postgresql/
    
    log "Backup completed: $backup_file"
    echo $backup_file
}

# Restore from backup
restore_database() {
    local backup_file=$1
    local db_name=$2
    
    log "Restoring database $db_name from $backup_file"
    
    case $DB_TYPE in
        mysql)
            gunzip -c $backup_file | mysql $db_name
            ;;
        postgresql)
            pg_restore -d $db_name $backup_file
            ;;
    esac
    
    log "Restore completed"
}

# Test backup
test_backup() {
    local backup_file=$1
    local test_db="test_restore_$(date +%Y%m%d)"
    
    log "Testing backup: $backup_file"
    
    # Download from S3 if needed
    if [[ $backup_file == s3://* ]]; then
        local local_file="/tmp/$(basename $backup_file)"
        aws s3 cp $backup_file $local_file
        backup_file=$local_file
    fi
    
    # Create test database
    case $DB_TYPE in
        mysql)
            mysql -e "CREATE DATABASE $test_db"
            restore_database $backup_file $test_db
            # Verify
            mysql -e "USE $test_db; SHOW TABLES;" | head -5
            mysql -e "DROP DATABASE $test_db"
            ;;
        postgresql)
            createdb $test_db
            restore_database $backup_file $test_db
            # Verify
            psql -d $test_db -c "\dt" | head -5
            dropdb $test_db
            ;;
    esac
    
    log "Backup test completed successfully"
}

# Cleanup old backups
cleanup_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days"
    
    aws s3 ls s3://${S3_BUCKET}/ --recursive | \
        awk -v date=$(date -d "$RETENTION_DAYS days ago" +%Y-%m-%d) '$1 < date {print $4}' | \
        xargs -I {} aws s3 rm s3://${S3_BUCKET}/{}
    
    log "Cleanup completed"
}

# Main execution
case "${3:-backup}" in
    backup)
        mkdir -p $BACKUP_DIR
        case $DB_TYPE in
            mysql)
                mysql_backup "myapp"
                ;;
            postgresql)
                postgres_backup "myapp"
                ;;
        esac
        cleanup_backups
        ;;
    restore)
        restore_database "$4" "$5"
        ;;
    test)
        test_backup "$4"
        ;;
    *)
        echo "Usage: $0 <mysql|postgresql> <full|incremental> [backup|restore|test] [args...]"
        exit 1
        ;;
esac
```

**Key Points:**
- Use consistent backup methods (mysqldump, pg_dump)
- Store backups in multiple locations (S3, cross-region)
- Test backups regularly
- Implement retention policies
- Document recovery procedures
- Monitor backup success/failure
- Use point-in-time recovery when available

---

## 11. Troubleshooting & Debugging

### Q11.1: Comprehensive Troubleshooting Framework

**Question:** Create a systematic troubleshooting approach for:
1. Application performance issues
2. Database connectivity problems
3. Network issues
4. Container orchestration problems
5. CI/CD pipeline failures

**Solution:**

```bash
#!/bin/bash
# Comprehensive Troubleshooting Script

troubleshoot_application() {
    local app_name=$1
    
    echo "=== Application Troubleshooting: $app_name ==="
    
    # Check if application is running
    if kubectl get deployment $app_name &> /dev/null; then
        echo "✓ Deployment exists"
        kubectl get deployment $app_name
    else
        echo "✗ Deployment not found"
        return 1
    fi
    
    # Check pod status
    echo ""
    echo "Pod Status:"
    kubectl get pods -l app=$app_name
    
    # Check logs
    echo ""
    echo "Recent Logs:"
    kubectl logs -l app=$app_name --tail=50
    
    # Check resource usage
    echo ""
    echo "Resource Usage:"
    kubectl top pods -l app=$app_name 2>/dev/null || echo "Metrics not available"
    
    # Check events
    echo ""
    echo "Recent Events:"
    kubectl get events --field-selector involvedObject.name=$app_name --sort-by='.lastTimestamp' | tail -10
}

troubleshoot_database() {
    local db_host=$1
    local db_name=$2
    
    echo "=== Database Troubleshooting ==="
    
    # Test connectivity
    echo "Testing connectivity to $db_host..."
    nc -zv $db_host 3306 2>&1 || echo "✗ Cannot connect to database"
    
    # Check connection pool
    echo ""
    echo "Database Connections:"
    mysql -h $db_host -e "SHOW PROCESSLIST;" 2>/dev/null || \
    psql -h $db_host -d $db_name -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null
    
    # Check slow queries
    echo ""
    echo "Slow Queries:"
    mysql -h $db_host -e "SELECT * FROM information_schema.processlist WHERE time > 5;" 2>/dev/null || \
    psql -h $db_host -d $db_name -c "SELECT * FROM pg_stat_activity WHERE state = 'active' AND now() - query_start > interval '5 seconds';" 2>/dev/null
}

troubleshoot_network() {
    echo "=== Network Troubleshooting ==="
    
    # Check DNS
    echo "DNS Resolution:"
    nslookup google.com || echo "✗ DNS resolution failed"
    
    # Check connectivity
    echo ""
    echo "Connectivity Tests:"
    ping -c 3 8.8.8.8 || echo "✗ Cannot reach external network"
    
    # Check ports
    echo ""
    echo "Listening Ports:"
    ss -tuln | head -10
    
    # Check iptables
    echo ""
    echo "Firewall Rules:"
    iptables -L -n -v | head -20
}

# Main
case "${1:-all}" in
    app)
        troubleshoot_application "${2:-myapp}"
        ;;
    db)
        troubleshoot_database "${2:-localhost}" "${3:-myapp}"
        ;;
    network)
        troubleshoot_network
        ;;
    all)
        troubleshoot_application "myapp"
        echo ""
        troubleshoot_database "db-host" "myapp"
        echo ""
        troubleshoot_network
        ;;
    *)
        echo "Usage: $0 [app|db|network|all] [args...]"
        exit 1
        ;;
esac
```

**Key Points:**
- Follow systematic approach (check logs, events, resources)
- Use appropriate tools for each layer
- Document findings and solutions
- Create runbooks for common issues
- Monitor proactively to prevent issues

---

## 12. Architecture & Design

### Q12.1: Microservices Architecture Design

**Question:** Design a microservices architecture with:
1. Service decomposition strategy
2. API gateway implementation
3. Service discovery
4. Distributed tracing
5. Event-driven communication

**Solution:**

```yaml
# docker-compose.microservices.yml
version: '3.8'

services:
  # API Gateway
  api-gateway:
    image: kong:latest
    ports:
      - "8000:8000"
      - "8001:8001"
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
    volumes:
      - ./kong/kong.yml:/kong/declarative/kong.yml
    networks:
      - microservices

  # Service Discovery (Consul)
  consul:
    image: consul:latest
    ports:
      - "8500:8500"
    command: consul agent -dev -client=0.0.0.0
    networks:
      - microservices

  # User Service
  user-service:
    build: ./services/user-service
    environment:
      - CONSUL_HOST=consul
      - DB_HOST=user-db
    depends_on:
      - consul
      - user-db
    networks:
      - microservices

  # Order Service
  order-service:
    build: ./services/order-service
    environment:
      - CONSUL_HOST=consul
      - DB_HOST=order-db
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - consul
      - order-db
      - rabbitmq
    networks:
      - microservices

  # Payment Service
  payment-service:
    build: ./services/payment-service
    environment:
      - CONSUL_HOST=consul
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - consul
      - rabbitmq
    networks:
      - microservices

  # Message Queue
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - microservices

  # Distributed Tracing (Jaeger)
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
    networks:
      - microservices

networks:
  microservices:
    driver: bridge
```

**Key Points:**
- Decompose by business capability
- Use API gateway for routing and authentication
- Implement service discovery for dynamic services
- Use message queues for async communication
- Implement distributed tracing for debugging
- Design for failure (circuit breakers, retries)

---

## 13. Performance Optimization

### Q13.1: Application Performance Tuning

**Question:** Optimize application performance:
1. Database query optimization
2. Caching strategy
3. CDN configuration
4. Load balancing
5. Resource optimization

**Solution:**

```bash
#!/bin/bash
# Performance Optimization Script

# 1. Database Optimization
optimize_database() {
    echo "Optimizing database..."
    
    # Analyze tables
    mysql -e "ANALYZE TABLE users, orders, products;" || \
    psql -c "ANALYZE users, orders, products;"
    
    # Add indexes on frequently queried columns
    mysql -e "CREATE INDEX idx_user_email ON users(email);" || \
    psql -c "CREATE INDEX idx_user_email ON users(email);"
    
    # Optimize queries
    # Enable query cache (MySQL)
    mysql -e "SET GLOBAL query_cache_size = 67108864;"
}

# 2. Redis Caching
setup_redis_cache() {
    echo "Setting up Redis cache..."
    
    # Cache frequently accessed data
    redis-cli SET "user:123" "$(mysql -e "SELECT * FROM users WHERE id=123" -N)"
    
    # Set TTL
    redis-cli EXPIRE "user:123" 3600
}

# 3. CDN Configuration
configure_cdn() {
    echo "Configuring CDN..."
    # Use CloudFront, Cloudflare, or similar
    # Cache static assets
    # Set appropriate cache headers
}

# Key Points:
# - Profile application to find bottlenecks
# - Optimize database queries and add indexes
# - Implement caching at multiple levels
# - Use CDN for static assets
# - Optimize container resources
# - Monitor and measure improvements
```

---

## 14. Disaster Recovery & Backup

### Q14.1: Disaster Recovery Plan

**Question:** Create a comprehensive disaster recovery plan:
1. RTO and RPO definitions
2. Backup strategies
3. Failover procedures
4. Recovery testing
5. Documentation

**Solution:**

```bash
#!/bin/bash
# Disaster Recovery Script

# RTO: Recovery Time Objective (target downtime)
# RPO: Recovery Point Objective (acceptable data loss)

# Backup Strategy
backup_strategy() {
    # Full backup daily
    # Incremental backup hourly
    # Point-in-time recovery enabled
    # Cross-region replication
}

# Failover Procedure
failover() {
    echo "Initiating failover to DR site..."
    
    # 1. Promote DR database
    # 2. Update DNS
    # 3. Scale up DR infrastructure
    # 4. Verify services
    # 5. Notify team
}

# Recovery Testing
test_recovery() {
    echo "Testing disaster recovery..."
    # Monthly DR drills
    # Document results
    # Update procedures
}
```

**Key Points:**
- Define RTO and RPO for each service
- Implement automated backups
- Test recovery procedures regularly
- Document all procedures
- Maintain DR infrastructure
- Regular drills and updates

---

## 15. DevOps Best Practices

### Q15.1: DevOps Maturity Assessment

**Question:** Assess and improve DevOps practices:
1. CI/CD maturity
2. Infrastructure automation
3. Monitoring and observability
4. Security practices
5. Team collaboration

**Solution:**

```bash
#!/bin/bash
# DevOps Maturity Assessment

assess_cicd() {
    echo "=== CI/CD Assessment ==="
    # Check for:
    # - Automated builds
    # - Automated tests
    # - Automated deployments
    # - Deployment frequency
    # - Mean time to recovery
}

assess_infrastructure() {
    echo "=== Infrastructure Assessment ==="
    # Check for:
    # - Infrastructure as Code
    # - Version control
    # - Automated provisioning
    # - Configuration management
}

# Key Best Practices:
# 1. Version control everything
# 2. Automate everything possible
# 3. Monitor and measure
# 4. Implement security from start
# 5. Foster collaboration
# 6. Continuous improvement
# 7. Document everything
# 8. Test thoroughly
# 9. Fail fast and recover quickly
# 10. Learn from failures
```

**Key Points:**
- Implement Infrastructure as Code
- Automate CI/CD pipelines
- Monitor everything
- Security by design
- Document processes
- Continuous improvement
- Blameless post-mortems
- Shared responsibility

---

## Conclusion

This master-level DevOps interview questions tutorial provides comprehensive coverage of:

- **Real-world scenarios** with practical solutions
- **Complete code examples** ready to use
- **Best practices** from industry experience
- **Troubleshooting guides** for common issues
- **Architecture patterns** for scalable systems

### Key Takeaways:

1. **Automation is key** - Automate repetitive tasks
2. **Monitor everything** - Visibility is crucial
3. **Security first** - Build security into everything
4. **Fail fast** - Quick feedback loops
5. **Documentation** - Knowledge sharing is essential
6. **Continuous improvement** - Always iterate and improve

### Practice Recommendations:

1. Set up your own lab environment
2. Practice with real scenarios
3. Contribute to open-source projects
4. Stay updated with latest tools
5. Participate in DevOps communities
6. Build a portfolio of projects

---

*Master-Level DevOps Interview Questions & Solutions*
*Complete End-to-End Guide*
*Last Updated: 2024*
