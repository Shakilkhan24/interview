## **Probes-এর Components Explained:**

---

### **১. Probe Types:**

```yaml
httpGet:    # HTTP request করে response check করে
tcpSocket:  # TCP port খুলা আছে কিনা check করে
exec:       # Container-এ command run করে exit code check করে
```

**উদাহরণ:**
```yaml
# HTTP GET request
httpGet:
  path: /health  # এই path-এ request যাবে
  port: 8080     # এই port-এ
  httpHeaders:   # Headers দিতে চাইলে
  - name: Custom-Header
    value: Hello

# TCP socket check
tcpSocket:
  port: 3306  # MySQL port check

# Command execute
exec:
  command:
  - cat
  - /tmp/healthy  # File exists কিনা check
```

---

### **২. Timing Parameters:**

```yaml
initialDelaySeconds: 30  # Container start হওয়ার পর কতক্ষণ অপেক্ষা করবে
periodSeconds: 10        # কত seconds পর পর check করবে
timeoutSeconds: 5        # কত seconds পর্যন্ত response-এর জন্য wait করবে
successThreshold: 1      # কতবার success লাগবে healthy বলা জন্য
failureThreshold: 3      # কতবার fail লাগবে unhealthy বলা জন্য
```

**Timing Diagram:**
```
Container Start
      │
      ▼
[initialDelaySeconds]  ← 30 seconds wait
      │
      ▼
First probe check
      │
      ▼
Wait [periodSeconds]   ← Every 10 seconds check
      │
      ▼
If fails, retry [failureThreshold] times (3 times)
      │
      ▼
If 3 fails → Unhealthy
```

---

### **৩. Startup Probe Specific:**
```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  failureThreshold: 30     # Maximum কতবার fail হতে দিবে
  periodSeconds: 10        # কত পর পর check করবে
  
# Calculation: 30 failures × 10 seconds = 300 seconds (5 minutes)
# মানে ৫ মিনিট পর্যন্ত শুরু হতে দিবে
```

---

### **৪. Readiness vs Liveness Difference:**

```yaml
readinessProbe:
  initialDelaySeconds: 5   # কম থাকে (কারণ দ্রুত জানা লাগবে ready কিনা)
  periodSeconds: 5         # ঘন ঘন check
  # FAIL হলে: Service থেকে remove, কিন্তু pod kill হবে না

livenessProbe:
  initialDelaySeconds: 15  # বেশি থাকে (ঝাপটা সামলানোর সময় দিতে)
  periodSeconds: 20        # কম ঘন ঘন check
  # FAIL হলে: Pod kill → restart
```

---

### **৫. Real Example Breakdown:**

```yaml
livenessProbe:
  httpGet:
    path: /healthz  # App-এর health endpoint
    port: 8080
    httpHeaders:
    - name: X-Liveness-Check
      value: "true"
  initialDelaySeconds: 15  # App-কে শুরু হতে ১৫ সেকেন্ড সময় দিলাম
  periodSeconds: 20        # প্রতি ২০ সেকেন্ড পর check
  timeoutSeconds: 3        # ৩ সেকেন্ডের মধ্যে response চাই
  successThreshold: 1      # ১ বার success হলেই healthy
  failureThreshold: 3      # ৩ বার fail হলে unhealthy
  
# মানে: 
# 1. 15s wait
# 2. Check every 20s
# 3. If fails, try 2 more times (total 3 attempts over 40 seconds)
# 4. If all 3 fail → restart pod
```

---

### **৬. Common Patterns:**

**Web Application:**
```yaml
readinessProbe:
  httpGet:
    path: /ready  # Database, cache connections check করে
    port: 8080
  initialDelaySeconds: 10

livenessProbe:
  httpGet:
    path: /live   # Basic "am I alive" check
    port: 8080
  initialDelaySeconds: 30
```

**Database:**
```yaml
readinessProbe:
  exec:
    command: ["mysql", "-h", "127.0.0.1", "-e", "SELECT 1"]
  initialDelaySeconds: 30

livenessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 60
```

---

### **৭. Critical Warning:**

```yaml
# DANGEROUS: If liveness probe is too sensitive
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 3    # খুব কম
  periodSeconds: 5          # খুব ঘন ঘন
  failureThreshold: 1       # ১ বার fail হলেই restart
  
# Problem: Temporary load increase → slow response 
# → Probe fails → Pod restart → More load → More restarts
# → CASCADING FAILURE!
```

**Best Practice:**
```yaml
livenessProbe:
  # Simple, reliable endpoint
  # Longer periods
  # Higher failure thresholds
  # Never same as readiness probe
```

---

### **৮. Test Commands:**

```bash
# Probe simulate করো:
# 1. Check pod status
kubectl describe pod <name> | grep -A 20 "Probes"

# 2. Check probe endpoints manually
kubectl exec <pod> -- wget -q -O- http://localhost:8080/health

# 3. Watch probe failures
kubectl get events --field-selector involvedObject.name=<pod-name>

# 4. Check service endpoints (readiness probe effect)
kubectl describe svc <service-name>
# দেখবে ready podগুলাই শুধু এন্ডপয়েন্ট হিসেবে আছে




## **Custom Commands in Probes (exec probes)**

### **১. Basic exec probe:**
```yaml
livenessProbe:
  exec:
    command:
    - sh
    - -c
    - ps aux | grep nginx | grep -v grep  # nginx process running check
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

### **২. File-based health checks:**
```yaml
readinessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy  # File exists and readable
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

### **৩. Application-specific checks:**
```yaml
# MySQL Database
livenessProbe:
  exec:
    command:
    - mysqladmin
    - ping
    - -h
    - localhost
  initialDelaySeconds: 60
  periodSeconds: 30

# Redis
readinessProbe:
  exec:
    command:
    - redis-cli
    - ping
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

### **৪. Script-based probes:**
```yaml
livenessProbe:
  exec:
    command:
    - /bin/bash
    - -c
    - |
      #!/bin/bash
      # Check multiple conditions
      if [ -f /var/run/nginx.pid ]; then
        if kill -0 $(cat /var/run/nginx.pid) 2>/dev/null; then
          exit 0
        fi
      fi
      exit 1
  initialDelaySeconds: 40
  periodSeconds: 30
```

---

### **৫. Port listening check:**
```yaml
readinessProbe:
  exec:
    command:
    - ss
    - -tln
    - | grep -q ":80 "  # Check if port 80 is listening
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

### **৬. Custom metrics/status check:**
```yaml
livenessProbe:
  exec:
    command:
    - python3
    - -c
    - |
      import psutil
      import sys
      
      # Check CPU usage of our process
      for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'myapp':
          if proc.cpu_percent(interval=1) > 90:  # >90% CPU
            sys.exit(1)
      sys.exit(0)
  periodSeconds: 30
```

---

### **৭. Combined health check:**
```yaml
startupProbe:
  exec:
    command:
    - /app/health-check.sh  # External script
  failureThreshold: 30
  periodSeconds: 10

# health-check.sh content:
#!/bin/bash
# Check 1: Process running
pgrep myapp > /dev/null || exit 1
# Check 2: Port open
nc -z localhost 8080 || exit 1
# Check 3: Can write to disk
touch /tmp/healthcheck.test && rm /tmp/healthcheck.test || exit 1
# All good
exit 0
```

---

### **৮. Resource-based checks:**
```yaml
readinessProbe:
  exec:
    command:
    - sh
    - -c
    - |
      # Check disk space > 10%
      df / | awk 'NR==2 {if ($4 < 10) exit 1; exit 0}'
  periodSeconds: 20
```

---

### **৯. Network connectivity check:**
```yaml
livenessProbe:
  exec:
    command:
    - curl
    - -f
    - --connect-timeout 3
    - http://localhost:8080/health
    - && nc -z localhost 3306  # Also check DB port
  initialDelaySeconds: 45
  periodSeconds: 25
```

---

### **১০. Complete Nginx Example with custom probes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-custom-probes
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        # Startup: Check if pid file exists
        startupProbe:
          exec:
            command:
            - test
            - -f
            - /var/run/nginx.pid
          failureThreshold: 30
          periodSeconds: 5
        # Readiness: Check if can serve requests
        readinessProbe:
          exec:
            command:
            - sh
            - -c
            - |
              # Check if nginx responds with 200
              if curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q 200; then
                # Check if error log has recent critical errors
                if tail -5 /var/log/nginx/error.log | grep -q "emerg\|crit"; then
                  exit 1
                fi
                exit 0
              else
                exit 1
              fi
          initialDelaySeconds: 10
          periodSeconds: 5
        # Liveness: Check if master process exists
        livenessProbe:
          exec:
            command:
            - sh
            - -c
            - |
              # Check nginx master process
              if [ -f /var/run/nginx.pid ]; then
                if kill -0 $(cat /var/run/nginx.pid) 2>/dev/null; then
                  # Check worker processes
                  if [ $(ps -ef | grep nginx | grep -v grep | wc -l) -ge 3 ]; then
                    exit 0
                  fi
                fi
              fi
              exit 1
          initialDelaySeconds: 40
          periodSeconds: 30
          failureThreshold: 3
```

---

### **Test custom probes:**
```bash
# 1. Deploy the pod
kubectl apply -f deployment.yaml

# 2. Check probe status
kubectl describe pod <pod-name> | grep -A 30 "Probes"

# 3. Test the exec command manually
kubectl exec <pod-name> -- sh -c "ps aux | grep nginx"

# 4. Simulate probe failure
# For file-based: delete the pid file
kubectl exec <pod-name> -- rm -f /var/run/nginx.pid

# For process-based: kill nginx
kubectl exec <pod-name> -- nginx -s stop

# 5. Watch pod restart
kubectl get pods -w
```

---

### **Important Notes:**
1. **exec commands run inside the container**
2. **Exit code matters:**
   - `0` = Success/Healthy
   - `Non-zero` = Failure/Unhealthy
3. **Keep commands lightweight** - they run frequently
4. **Security:** Don't expose secrets in commands
5. **Debug:** Test commands manually before deploying:
```bash
# Test command locally first
docker exec <container> sh -c "your_probe_command"
```