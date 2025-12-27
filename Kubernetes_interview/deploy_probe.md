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
