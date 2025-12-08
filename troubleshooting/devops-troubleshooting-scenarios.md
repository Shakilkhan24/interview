# 30 DevOps Troubleshooting Scenarios & Solutions
## Real-World Problems and Step-by-Step Solutions

---

## Table of Contents
1. [Kubernetes Issues](#1-kubernetes-issues)
2. [Docker/Container Issues](#2-dockercontainer-issues)
3. [CI/CD Pipeline Problems](#3-cicd-pipeline-problems)
4. [Infrastructure Issues](#4-infrastructure-issues)
5. [Network Problems](#5-network-problems)
6. [Application Deployment Issues](#6-application-deployment-issues)
7. [Performance Problems](#7-performance-problems)
8. [Security Issues](#8-security-issues)
9. [Database Connectivity](#9-database-connectivity)
10. [Monitoring and Logging](#10-monitoring-and-logging)

---

## 1. Kubernetes Issues

### Scenario 1: Pod Stuck in Pending State

**Problem:**
Pod remains in `Pending` state and cannot be scheduled to any node.

**Symptoms:**
```bash
$ kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
myapp-xxx              0/1     Pending   0          5m

$ kubectl describe pod myapp-xxx
Events:
  Warning  FailedScheduling  pod has unbound immediate PersistentVolumeClaims
```

**Troubleshooting Steps:**

1. **Check pod events:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

2. **Check node resources:**
   ```bash
   kubectl top nodes
   kubectl describe node <node-name>
   ```

3. **Check PVC status:**
   ```bash
   kubectl get pvc
   kubectl describe pvc <pvc-name>
   ```

4. **Check node taints:**
   ```bash
   kubectl describe node <node-name> | grep Taints
   ```

5. **Check resource quotas:**
   ```bash
   kubectl describe quota -n <namespace>
   ```

**Common Causes & Solutions:**

**Cause 1: Insufficient Resources**
```bash
# Check node capacity
kubectl describe node | grep -A 5 "Allocated resources"

# Solution: Add more nodes or reduce resource requests
kubectl scale deployment <deployment> --replicas=0
# Or increase cluster capacity
```

**Cause 2: Node Selector/Affinity Mismatch**
```bash
# Check pod node selector
kubectl get pod <pod-name> -o yaml | grep nodeSelector

# Check node labels
kubectl get nodes --show-labels

# Solution: Add required labels to nodes or remove node selector
kubectl label nodes <node-name> <key>=<value>
```

**Cause 3: PVC Not Bound**
```bash
# Check storage class
kubectl get storageclass

# Check PVC
kubectl get pvc
kubectl describe pvc <pvc-name>

# Solution: Create storage class or fix PVC configuration
kubectl apply -f storageclass.yaml
```

**Cause 4: Node Taints**
```bash
# Check taints
kubectl describe node | grep Taints

# Solution: Add toleration to pod or remove taint
kubectl taint nodes <node-name> <taint-key>-
```

**Prevention:**
- Set appropriate resource requests/limits
- Use node affinity carefully
- Ensure storage classes are configured
- Monitor cluster capacity

---

### Scenario 2: Pod CrashLoopBackOff

**Problem:**
Pod continuously crashes and restarts, showing `CrashLoopBackOff` status.

**Symptoms:**
```bash
$ kubectl get pods
NAME                    READY   STATUS             RESTARTS   AGE
myapp-xxx              0/1     CrashLoopBackOff   5          2m

$ kubectl logs myapp-xxx
Error: Cannot connect to database
```

**Troubleshooting Steps:**

1. **Check pod logs:**
   ```bash
   kubectl logs <pod-name> -n <namespace>
   kubectl logs <pod-name> -n <namespace> --previous  # Previous container
   ```

2. **Check pod events:**
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   ```

3. **Check container exit code:**
   ```bash
   kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
   ```

4. **Check resource limits:**
   ```bash
   kubectl describe pod <pod-name> | grep -A 5 "Limits"
   ```

5. **Check configuration:**
   ```bash
   kubectl get pod <pod-name> -o yaml | grep -A 10 "env:"
   ```

**Common Causes & Solutions:**

**Cause 1: Application Error**
```bash
# Check logs
kubectl logs <pod-name> --previous

# Solution: Fix application code or configuration
# Check environment variables
kubectl exec <pod-name> -- env
```

**Cause 2: Missing Dependencies**
```bash
# Check if service dependencies are available
kubectl get svc
kubectl get endpoints

# Solution: Ensure dependent services are running
kubectl get deployment <dependency-service>
```

**Cause 3: OOMKilled (Out of Memory)**
```bash
# Check if pod was OOMKilled
kubectl describe pod <pod-name> | grep -i "oom"

# Solution: Increase memory limits
kubectl set resources deployment <deployment> --limits=memory=512Mi
```

**Cause 4: Wrong Image or Tag**
```bash
# Check image being used
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].image}'

# Solution: Update to correct image
kubectl set image deployment/<deployment> <container>=<correct-image>:<tag>
```

**Cause 5: Readiness Probe Failure**
```bash
# Check probe configuration
kubectl get pod <pod-name> -o yaml | grep -A 10 "readinessProbe"

# Solution: Fix probe endpoint or adjust probe timing
```

**Prevention:**
- Test images before deployment
- Set appropriate resource limits
- Implement proper health checks
- Use init containers for dependencies
- Monitor application logs

---

### Scenario 3: Service Not Accessible

**Problem:**
Service is created but cannot be accessed from within or outside the cluster.

**Symptoms:**
```bash
$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
myapp-svc    ClusterIP   10.96.1.2       <none>        80/TCP    5m

$ curl http://myapp-svc:80
curl: (7) Failed to connect to myapp-svc port 80: Connection refused
```

**Troubleshooting Steps:**

1. **Check service endpoints:**
   ```bash
   kubectl get endpoints <service-name>
   kubectl describe svc <service-name>
   ```

2. **Check pod labels:**
   ```bash
   kubectl get pods --show-labels
   kubectl get svc <service-name> -o yaml | grep selector
   ```

3. **Check pod readiness:**
   ```bash
   kubectl get pods
   kubectl describe pod <pod-name> | grep -A 5 "Readiness"
   ```

4. **Test connectivity:**
   ```bash
   # From within cluster
   kubectl run test-pod --image=busybox --rm -it -- sh
   # Inside pod: wget -O- http://<service-name>:<port>
   ```

5. **Check network policies:**
   ```bash
   kubectl get networkpolicies
   kubectl describe networkpolicy <policy-name>
   ```

**Common Causes & Solutions:**

**Cause 1: No Endpoints (Label Mismatch)**
```bash
# Check service selector matches pod labels
kubectl get svc <service-name> -o jsonpath='{.spec.selector}'
kubectl get pods --show-labels

# Solution: Fix label mismatch
kubectl label pod <pod-name> <key>=<value>
# Or update service selector
kubectl edit svc <service-name>
```

**Cause 2: Pods Not Ready**
```bash
# Check pod status
kubectl get pods

# Solution: Fix readiness probe or pod issues
kubectl describe pod <pod-name>
```

**Cause 3: Wrong Port**
```bash
# Check service port matches container port
kubectl get svc <service-name> -o yaml | grep -A 5 "ports"
kubectl get pod <pod-name> -o yaml | grep -A 5 "containerPort"

# Solution: Update service port
kubectl patch svc <service-name> -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

**Cause 4: Network Policy Blocking**
```bash
# Check network policies
kubectl get networkpolicies -A

# Solution: Update network policy to allow traffic
kubectl edit networkpolicy <policy-name>
```

**Cause 5: Service Type Issue**
```bash
# For external access, use LoadBalancer or NodePort
kubectl patch svc <service-name> -p '{"spec":{"type":"LoadBalancer"}}'
```

**Prevention:**
- Ensure label selectors match
- Test service connectivity
- Use proper service types
- Configure network policies correctly
- Monitor service endpoints

---

### Scenario 4: ImagePullBackOff Error

**Problem:**
Pod cannot start because it cannot pull the container image.

**Symptoms:**
```bash
$ kubectl get pods
NAME                    READY   STATUS         RESTARTS   AGE
myapp-xxx              0/1     ImagePullBackOff   0       2m

$ kubectl describe pod myapp-xxx
Events:
  Warning  Failed      Error: ImagePullBackOff
  Warning  Failed      Failed to pull image "myregistry/myapp:v1.0"
```

**Troubleshooting Steps:**

1. **Check image name and tag:**
   ```bash
   kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].image}'
   ```

2. **Check image pull secrets:**
   ```bash
   kubectl get pod <pod-name> -o yaml | grep -A 5 "imagePullSecrets"
   kubectl get secrets | grep docker
   ```

3. **Test image pull manually:**
   ```bash
   docker pull <image-name>:<tag>
   ```

4. **Check registry credentials:**
   ```bash
   kubectl get secret <registry-secret> -o yaml
   ```

5. **Check network connectivity:**
   ```bash
   kubectl run test --image=busybox --rm -it -- ping <registry-host>
   ```

**Common Causes & Solutions:**

**Cause 1: Image Doesn't Exist**
```bash
# Verify image exists in registry
docker pull <image>:<tag>

# Solution: Build and push image
docker build -t <image>:<tag> .
docker push <image>:<tag>
```

**Cause 2: Wrong Image Name/Tag**
```bash
# Check deployment image
kubectl get deployment <deployment> -o jsonpath='{.spec.template.spec.containers[0].image}'

# Solution: Update to correct image
kubectl set image deployment/<deployment> <container>=<correct-image>:<tag>
```

**Cause 3: Missing Image Pull Secret**
```bash
# Check if secret exists
kubectl get secrets

# Create image pull secret
kubectl create secret docker-registry <secret-name> \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<password> \
  --docker-email=<email>

# Add to deployment
kubectl patch deployment <deployment> -p '{"spec":{"template":{"spec":{"imagePullSecrets":[{"name":"<secret-name>"}]}}}}'
```

**Cause 4: Private Registry Authentication**
```bash
# For ECR (AWS)
aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin <registry>

# Create secret from existing docker config
kubectl create secret generic <secret-name> \
  --from-file=.dockerconfigjson=<path-to-docker-config> \
  --type=kubernetes.io/dockerconfigjson
```

**Cause 5: Network Issues**
```bash
# Check if registry is reachable
kubectl run test --image=busybox --rm -it -- wget -O- <registry-url>

# Solution: Configure proxy or fix network policies
```

**Prevention:**
- Use image tags instead of latest
- Pre-pull images to nodes
- Configure image pull secrets correctly
- Test image accessibility before deployment
- Use image pull policies appropriately

---

## 2. Docker/Container Issues

### Scenario 5: Container Won't Start

**Problem:**
Docker container exits immediately after starting.

**Symptoms:**
```bash
$ docker run myapp:latest
$ docker ps -a
CONTAINER ID   IMAGE          STATUS
abc123        myapp:latest   Exited (1) 2 seconds ago

$ docker logs abc123
Error: Cannot find configuration file
```

**Troubleshooting Steps:**

1. **Check container logs:**
   ```bash
   docker logs <container-id>
   docker logs <container-id> --tail 50
   ```

2. **Check exit code:**
   ```bash
   docker inspect <container-id> | grep -A 5 "State"
   ```

3. **Run interactively:**
   ```bash
   docker run -it <image> /bin/sh
   ```

4. **Check entrypoint:**
   ```bash
   docker inspect <image> | grep -A 5 "Entrypoint"
   ```

5. **Check environment variables:**
   ```bash
   docker inspect <container-id> | grep -A 10 "Env"
   ```

**Common Causes & Solutions:**

**Cause 1: Missing Configuration**
```bash
# Check if config file exists in container
docker run -it <image> ls -la /app/config

# Solution: Mount config file or set environment variables
docker run -v /host/config:/app/config <image>
# Or
docker run -e CONFIG_PATH=/app/config <image>
```

**Cause 2: Wrong Entrypoint**
```bash
# Check Dockerfile entrypoint
docker inspect <image> | grep Entrypoint

# Solution: Override entrypoint
docker run --entrypoint /bin/sh <image>
```

**Cause 3: Port Already in Use**
```bash
# Check port usage
docker ps | grep <port>
netstat -tuln | grep <port>

# Solution: Use different port
docker run -p 8080:8080 <image>
```

**Cause 4: Permission Issues**
```bash
# Check file permissions
docker run <image> ls -la /app

# Solution: Fix permissions or run as different user
docker run -u root <image>
```

**Prevention:**
- Test containers locally before deployment
- Use proper entrypoints
- Handle missing configuration gracefully
- Check logs for errors
- Use health checks

---

### Scenario 6: Container Running Out of Memory

**Problem:**
Container is being killed due to OOM (Out of Memory) errors.

**Symptoms:**
```bash
$ docker stats
CONTAINER   MEM USAGE / LIMIT   MEM %
abc123      512Mi / 512Mi       100%

$ dmesg | grep -i oom
Out of memory: Killed process 1234
```

**Troubleshooting Steps:**

1. **Check memory usage:**
   ```bash
   docker stats <container-id>
   docker stats --no-stream
   ```

2. **Check container limits:**
   ```bash
   docker inspect <container-id> | grep -A 5 "Memory"
   ```

3. **Check system memory:**
   ```bash
   free -h
   docker system df
   ```

4. **Check for memory leaks:**
   ```bash
   docker exec <container-id> ps aux
   ```

**Common Causes & Solutions:**

**Cause 1: Memory Limit Too Low**
```bash
# Check current limit
docker inspect <container-id> | grep Memory

# Solution: Increase memory limit
docker update --memory=1g <container-id>
# Or in docker-compose
services:
  app:
    mem_limit: 1g
```

**Cause 2: Memory Leak in Application**
```bash
# Monitor memory over time
watch -n 1 'docker stats --no-stream'

# Solution: Fix application memory leak
# Use memory profilers
# Set appropriate garbage collection
```

**Cause 3: Too Many Containers**
```bash
# Check running containers
docker ps

# Solution: Remove unused containers
docker container prune
docker system prune -a
```

**Prevention:**
- Set appropriate memory limits
- Monitor memory usage
- Fix memory leaks
- Use resource quotas
- Implement memory monitoring

---

## 3. CI/CD Pipeline Problems

### Scenario 7: Pipeline Fails at Build Stage

**Problem:**
CI/CD pipeline fails during the build stage with unclear error messages.

**Symptoms:**
```bash
Build failed: Exit code 1
Error: npm install failed
```

**Troubleshooting Steps:**

1. **Check build logs:**
   ```bash
   # Jenkins
   View build logs in Jenkins UI
   
   # GitHub Actions
   Check Actions tab for detailed logs
   
   # GitLab CI
   Check pipeline logs
   ```

2. **Reproduce locally:**
   ```bash
   # Run same commands locally
   npm install
   npm run build
   ```

3. **Check dependencies:**
   ```bash
   # Verify package.json
   cat package.json
   
   # Check lock file
   ls -la package-lock.json
   ```

4. **Check build environment:**
   ```bash
   # Verify Node version
   node --version
   npm --version
   ```

5. **Check network/proxy:**
   ```bash
   # Test registry access
   npm ping
   ```

**Common Causes & Solutions:**

**Cause 1: Dependency Issues**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Solution: Update dependencies or fix version conflicts
npm audit fix
npm update
```

**Cause 2: Wrong Node Version**
```bash
# Check required Node version
cat .nvmrc
cat package.json | grep engines

# Solution: Use correct Node version
nvm use <version>
# Or in CI
- uses: actions/setup-node@v3
  with:
    node-version: '18'
```

**Cause 3: Missing Environment Variables**
```bash
# Check required env vars
cat .env.example

# Solution: Set environment variables in CI
# Jenkins: Environment variables
# GitHub Actions: secrets or env
env:
  NODE_ENV: production
```

**Cause 4: Network/Registry Issues**
```bash
# Test registry access
npm config get registry
npm ping

# Solution: Configure proxy or use different registry
npm config set registry <registry-url>
npm config set proxy <proxy-url>
```

**Prevention:**
- Lock dependency versions
- Use consistent build environments
- Test builds locally first
- Set up proper caching
- Monitor build times

---

### Scenario 8: Deployment Fails Silently

**Problem:**
Pipeline shows success but application is not actually deployed.

**Symptoms:**
```bash
Pipeline: SUCCESS
But application is not accessible
```

**Troubleshooting Steps:**

1. **Check deployment status:**
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl rollout status deployment/<name>
   ```

2. **Check deployment events:**
   ```bash
   kubectl describe deployment <name>
   kubectl get events --sort-by='.lastTimestamp'
   ```

3. **Verify image was pushed:**
   ```bash
   docker images | grep <image>
   # Or check registry
   aws ecr describe-images --repository-name <repo>
   ```

4. **Check service configuration:**
   ```bash
   kubectl get svc
   kubectl describe svc <name>
   ```

5. **Test connectivity:**
   ```bash
   curl http://<service-url>
   kubectl port-forward svc/<name> 8080:80
   ```

**Common Causes & Solutions:**

**Cause 1: Image Not Updated**
```bash
# Check if new image was built
docker images | grep <image>

# Solution: Ensure image tag changes
# Use commit SHA or build number
IMAGE_TAG=${GIT_COMMIT:0:7}
docker build -t <image>:${IMAGE_TAG} .
```

**Cause 2: Deployment Not Triggered**
```bash
# Check if deployment was updated
kubectl get deployment <name> -o yaml | grep image

# Solution: Force deployment update
kubectl rollout restart deployment/<name>
```

**Cause 3: Wrong Namespace**
```bash
# Check current namespace
kubectl config view | grep namespace

# Solution: Deploy to correct namespace
kubectl apply -f deployment.yaml -n <namespace>
```

**Cause 4: Health Check Failing**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Solution: Fix health check endpoint
# Or adjust probe timing
```

**Prevention:**
- Verify deployments after pipeline
- Use proper image tagging
- Implement health checks
- Monitor deployment status
- Test in staging first

---

## 4. Infrastructure Issues

### Scenario 9: Terraform Apply Fails

**Problem:**
Terraform apply fails with resource creation errors.

**Symptoms:**
```bash
$ terraform apply
Error: Error creating resource: AlreadyExistsException
```

**Troubleshooting Steps:**

1. **Check Terraform state:**
   ```bash
   terraform state list
   terraform show
   ```

2. **Check for state drift:**
   ```bash
   terraform plan
   terraform refresh
   ```

3. **Check resource existence:**
   ```bash
   # AWS
   aws ec2 describe-instances --filters "Name=tag:Name,Values=<name>"
   
   # Check manually in cloud console
   ```

4. **Check IAM permissions:**
   ```bash
   aws sts get-caller-identity
   # Verify required permissions
   ```

5. **Check Terraform logs:**
   ```bash
   export TF_LOG=DEBUG
   terraform apply
   ```

**Common Causes & Solutions:**

**Cause 1: Resource Already Exists**
```bash
# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0

# Or remove from state if not needed
terraform state rm aws_instance.example
```

**Cause 2: State File Out of Sync**
```bash
# Refresh state
terraform refresh

# Or manually fix state
terraform state mv <old-address> <new-address>
```

**Cause 3: Insufficient Permissions**
```bash
# Check IAM policy
aws iam get-user-policy --user-name <user> --policy-name <policy>

# Solution: Add required permissions
# Or use role with proper permissions
```

**Cause 4: Resource Limits**
```bash
# Check service quotas
aws service-quotas get-service-quota --service-code ec2 --quota-code L-0263D0A3

# Solution: Request quota increase
```

**Prevention:**
- Use remote state backend
- Lock state files
- Review plans before apply
- Use workspaces for environments
- Implement proper IAM policies

---

### Scenario 10: AWS Service Quota Exceeded

**Problem:**
Cannot create new resources due to service quota limits.

**Symptoms:**
```bash
Error: LimitExceededException
You have reached the limit of 20 instances
```

**Troubleshooting Steps:**

1. **Check current usage:**
   ```bash
   aws service-quotas get-aws-default-service-quota \
     --service-code ec2 \
     --quota-code L-0263D0A3
   ```

2. **List all quotas:**
   ```bash
   aws service-quotas list-service-quotas --service-code ec2
   ```

3. **Check resource usage:**
   ```bash
   aws ec2 describe-instances --query 'length(Reservations[*].Instances[*])'
   ```

4. **Identify unused resources:**
   ```bash
   aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped"
   ```

**Common Causes & Solutions:**

**Cause 1: Too Many Running Instances**
```bash
# List all instances
aws ec2 describe-instances

# Solution: Terminate unused instances
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Or request quota increase
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-0263D0A3 \
  --desired-value 50
```

**Cause 2: VPC Limits**
```bash
# Check VPC count
aws ec2 describe-vpcs --query 'length(Vpcs)'

# Solution: Delete unused VPCs or request increase
```

**Prevention:**
- Monitor quota usage
- Clean up unused resources
- Request quota increases proactively
- Use resource tagging for tracking
- Implement resource lifecycle policies

---

## 5. Network Problems

### Scenario 11: Cannot Connect to Service

**Problem:**
Application cannot connect to external service or database.

**Symptoms:**
```bash
Error: Connection refused
Error: Timeout connecting to database
```

**Troubleshooting Steps:**

1. **Test connectivity:**
   ```bash
   # From pod
   kubectl exec -it <pod> -- nc -zv <host> <port>
   kubectl exec -it <pod> -- telnet <host> <port>
   ```

2. **Check DNS resolution:**
   ```bash
   kubectl exec -it <pod> -- nslookup <hostname>
   kubectl exec -it <pod> -- dig <hostname>
   ```

3. **Check network policies:**
   ```bash
   kubectl get networkpolicies
   kubectl describe networkpolicy <policy>
   ```

4. **Check service endpoints:**
   ```bash
   kubectl get endpoints
   kubectl get svc
   ```

5. **Check firewall rules:**
   ```bash
   # AWS Security Groups
   aws ec2 describe-security-groups
   
   # Check ingress/egress rules
   ```

**Common Causes & Solutions:**

**Cause 1: Network Policy Blocking**
```bash
# Check network policies
kubectl get networkpolicies -A

# Solution: Update network policy
kubectl edit networkpolicy <policy>
# Add egress rule for required traffic
```

**Cause 2: DNS Resolution Failure**
```bash
# Check CoreDNS
kubectl get pods -n kube-system | grep coredns
kubectl logs -n kube-system <coredns-pod>

# Solution: Fix DNS configuration
# Or use IP address instead of hostname
```

**Cause 3: Security Group Rules**
```bash
# Check security group
aws ec2 describe-security-groups --group-ids <sg-id>

# Solution: Add required ingress/egress rules
aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port <port> \
  --cidr <cidr>
```

**Cause 4: Wrong Port or Host**
```bash
# Verify connection details
echo $DATABASE_HOST
echo $DATABASE_PORT

# Solution: Fix environment variables
kubectl set env deployment/<name> DATABASE_HOST=<correct-host>
```

**Prevention:**
- Test connectivity before deployment
- Document network requirements
- Use service discovery
- Configure network policies correctly
- Monitor network connectivity

---

### Scenario 12: Slow Network Performance

**Problem:**
Network connections are slow or timing out.

**Symptoms:**
```bash
High latency
Connection timeouts
Slow data transfer
```

**Troubleshooting Steps:**

1. **Measure latency:**
   ```bash
   kubectl exec -it <pod> -- ping <host>
   kubectl exec -it <pod> -- traceroute <host>
   ```

2. **Check bandwidth:**
   ```bash
   # Use iperf
   kubectl run iperf-server --image=networkstatic/iperf3 -- --server
   kubectl run iperf-client --image=networkstatic/iperf3 -- --client <server-ip>
   ```

3. **Check network policies:**
   ```bash
   kubectl get networkpolicies -A
   ```

4. **Check node network:**
   ```bash
   # On node
   ifconfig
   netstat -i
   ```

5. **Check for packet loss:**
   ```bash
   kubectl exec -it <pod> -- ping -c 100 <host>
   ```

**Common Causes & Solutions:**

**Cause 1: Network Policy Overhead**
```bash
# Simplify network policies
# Use label selectors efficiently
```

**Cause 2: MTU Issues**
```bash
# Check MTU
ip link show

# Solution: Adjust MTU if needed
ip link set mtu 1400 dev eth0
```

**Cause 3: Resource Constraints**
```bash
# Check node resources
kubectl top nodes

# Solution: Add more nodes or increase resources
```

**Prevention:**
- Monitor network metrics
- Optimize network policies
- Use appropriate instance types
- Implement network monitoring
- Test performance regularly

---

## 6. Application Deployment Issues

### Scenario 13: Rolling Update Stuck

**Problem:**
Deployment rolling update is stuck and not progressing.

**Symptoms:**
```bash
$ kubectl get deployment
NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE
myapp     3         3         1            2

# Stuck for extended period
```

**Troubleshooting Steps:**

1. **Check deployment status:**
   ```bash
   kubectl rollout status deployment/<name>
   kubectl describe deployment <name>
   ```

2. **Check pod status:**
   ```bash
   kubectl get pods -l app=<name>
   kubectl describe pod <pod-name>
   ```

3. **Check events:**
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

4. **Check resource availability:**
   ```bash
   kubectl top nodes
   kubectl describe node <node>
   ```

5. **Check image pull:**
   ```bash
   kubectl describe pod <new-pod> | grep -i image
   ```

**Common Causes & Solutions:**

**Cause 1: New Pods Not Starting**
```bash
# Check why new pods aren't starting
kubectl get pods
kubectl describe pod <new-pod>

# Solution: Fix image, resources, or configuration
```

**Cause 2: Old Pods Not Terminating**
```bash
# Check pod termination
kubectl get pods
kubectl describe pod <old-pod>

# Solution: Force delete if needed (carefully)
kubectl delete pod <old-pod> --grace-period=0 --force
```

**Cause 3: Resource Constraints**
```bash
# Check available resources
kubectl describe node | grep -A 5 "Allocated resources"

# Solution: Increase resources or scale down
```

**Cause 4: Readiness Probe Failing**
```bash
# Check probe status
kubectl describe pod <pod> | grep -A 10 "Readiness"

# Solution: Fix probe or adjust timing
```

**Prevention:**
- Set appropriate resource limits
- Test deployments in staging
- Monitor rollout progress
- Use proper health checks
- Implement deployment strategies

---

### Scenario 14: Blue-Green Deployment Failure

**Problem:**
Blue-green deployment fails to switch traffic to new version.

**Symptoms:**
```bash
New version deployed but traffic still going to old version
```

**Troubleshooting Steps:**

1. **Check both deployments:**
   ```bash
   kubectl get deployments
   kubectl get pods -l version=blue
   kubectl get pods -l version=green
   ```

2. **Check service selector:**
   ```bash
   kubectl get svc <name> -o yaml | grep selector
   ```

3. **Check ingress configuration:**
   ```bash
   kubectl get ingress
   kubectl describe ingress <name>
   ```

4. **Test both versions:**
   ```bash
   kubectl port-forward deployment/<blue> 8080:80
   kubectl port-forward deployment/<green> 8081:80
   ```

**Common Causes & Solutions:**

**Cause 1: Service Selector Not Updated**
```bash
# Check current selector
kubectl get svc <name> -o jsonpath='{.spec.selector}'

# Solution: Update selector
kubectl patch svc <name> -p '{"spec":{"selector":{"version":"green"}}}'
```

**Cause 2: Ingress Not Updated**
```bash
# Check ingress backend
kubectl get ingress <name> -o yaml

# Solution: Update ingress to point to green service
```

**Cause 3: New Version Unhealthy**
```bash
# Check green deployment health
kubectl get pods -l version=green
kubectl describe pod <green-pod>

# Solution: Fix health issues before switching
```

**Prevention:**
- Automate traffic switching
- Test new version before switch
- Implement canary deployments
- Monitor both versions
- Have rollback plan ready

---

## 7. Performance Problems

### Scenario 15: High CPU Usage

**Problem:**
Application or cluster showing high CPU usage.

**Symptoms:**
```bash
$ kubectl top pods
NAME                    CPU(cores)   MEMORY(bytes)
myapp-xxx              2000m        512Mi

# CPU at 200% (2 cores fully utilized)
```

**Troubleshooting Steps:**

1. **Identify high CPU pods:**
   ```bash
   kubectl top pods --sort-by=cpu
   kubectl top nodes
   ```

2. **Check pod resource limits:**
   ```bash
   kubectl describe pod <pod> | grep -A 5 "Limits"
   ```

3. **Check application metrics:**
   ```bash
   # If Prometheus available
   # Check CPU usage over time
   ```

4. **Check for CPU throttling:**
   ```bash
   kubectl describe pod <pod> | grep -i throttle
   ```

5. **Profile application:**
   ```bash
   # Use profiling tools
   kubectl exec -it <pod> -- <profiling-command>
   ```

**Common Causes & Solutions:**

**Cause 1: Infinite Loop or High Processing**
```bash
# Check application logs
kubectl logs <pod> --tail 100

# Solution: Fix application code
# Add rate limiting
# Optimize algorithms
```

**Cause 2: Too Many Requests**
```bash
# Check request rate
# Monitor ingress metrics

# Solution: Scale horizontally
kubectl scale deployment <name> --replicas=5

# Or implement rate limiting
```

**Cause 3: CPU Limit Too Low**
```bash
# Check limits
kubectl describe pod <pod> | grep cpu

# Solution: Increase CPU limit
kubectl set resources deployment <name> --limits=cpu=2000m
```

**Cause 4: Resource Contention**
```bash
# Check node CPU usage
kubectl top nodes

# Solution: Add more nodes or move pods
```

**Prevention:**
- Set appropriate CPU limits
- Monitor CPU usage
- Optimize application code
- Scale horizontally
- Use resource quotas

---

### Scenario 16: Memory Leak

**Problem:**
Application memory usage continuously increases over time.

**Symptoms:**
```bash
$ kubectl top pods
NAME                    CPU(cores)   MEMORY(bytes)
myapp-xxx              500m         2048Mi/512Mi

# Memory exceeds limit, pod gets OOMKilled
```

**Troubleshooting Steps:**

1. **Monitor memory over time:**
   ```bash
   watch -n 5 'kubectl top pods'
   ```

2. **Check for OOMKills:**
   ```bash
   kubectl describe pod <pod> | grep -i oom
   dmesg | grep -i oom
   ```

3. **Check application memory:**
   ```bash
   kubectl exec -it <pod> -- ps aux
   ```

4. **Check memory limits:**
   ```bash
   kubectl describe pod <pod> | grep -A 5 "Limits"
   ```

5. **Use memory profiler:**
   ```bash
   # Application-specific profiling tools
   ```

**Common Causes & Solutions:**

**Cause 1: Memory Leak in Code**
```bash
# Use memory profilers
# Go: pprof
# Java: jmap, VisualVM
# Python: memory_profiler

# Solution: Fix memory leaks
# Free unused objects
# Close connections properly
```

**Cause 2: Cache Growing Unbounded**
```bash
# Check cache size
# Monitor cache metrics

# Solution: Implement cache eviction
# Set maximum cache size
# Use TTL for cache entries
```

**Cause 3: Too Many Goroutines/Threads**
```bash
# Check thread/goroutine count
kubectl exec -it <pod> -- ps -eLf | wc -l

# Solution: Limit concurrency
# Use worker pools
# Implement proper cleanup
```

**Prevention:**
- Set memory limits
- Monitor memory usage
- Use memory profilers
- Implement proper cleanup
- Test under load

---

## 8. Security Issues

### Scenario 17: Unauthorized Access

**Problem:**
Unauthorized users can access resources or services.

**Symptoms:**
```bash
Access granted without proper authentication
RBAC not working as expected
```

**Troubleshooting Steps:**

1. **Check RBAC configuration:**
   ```bash
   kubectl get roles
   kubectl get rolebindings
   kubectl get clusterroles
   kubectl get clusterrolebindings
   ```

2. **Check user permissions:**
   ```bash
   kubectl auth can-i get pods --as=<user>
   kubectl auth can-i create deployments --as=<user>
   ```

3. **Check service account:**
   ```bash
   kubectl get serviceaccounts
   kubectl describe serviceaccount <name>
   ```

4. **Check network policies:**
   ```bash
   kubectl get networkpolicies
   ```

5. **Review audit logs:**
   ```bash
   # Check Kubernetes audit logs
   # Or cloud provider logs
   ```

**Common Causes & Solutions:**

**Cause 1: Overly Permissive RBAC**
```bash
# Check role permissions
kubectl get role <name> -o yaml

# Solution: Follow principle of least privilege
# Remove unnecessary permissions
kubectl edit role <name>
```

**Cause 2: Default Service Account**
```bash
# Check if using default SA
kubectl get pod <pod> -o jsonpath='{.spec.serviceAccountName}'

# Solution: Use dedicated service account
kubectl create serviceaccount <name>
kubectl set serviceaccount deployment <name> <serviceaccount>
```

**Cause 3: Missing Network Policies**
```bash
# Check network policies
kubectl get networkpolicies -A

# Solution: Implement network policies
kubectl apply -f network-policy.yaml
```

**Prevention:**
- Implement RBAC properly
- Use least privilege
- Regular security audits
- Enable audit logging
- Use network policies

---

### Scenario 18: Exposed Secrets

**Problem:**
Secrets are exposed in logs, environment variables, or code.

**Symptoms:**
```bash
Secrets visible in pod logs
Secrets in environment variables
Secrets committed to Git
```

**Troubleshooting Steps:**

1. **Check pod environment:**
   ```bash
   kubectl exec <pod> -- env | grep -i secret
   kubectl get pod <pod> -o yaml | grep -A 10 "env:"
   ```

2. **Check logs:**
   ```bash
   kubectl logs <pod> | grep -i password
   ```

3. **Check Git history:**
   ```bash
   git log --all --full-history -- <file-with-secrets>
   ```

4. **Check secret mounts:**
   ```bash
   kubectl describe pod <pod> | grep -A 5 "Mounts"
   ```

**Common Causes & Solutions:**

**Cause 1: Secrets in Environment Variables**
```bash
# Check env vars
kubectl get pod <pod> -o yaml | grep -A 5 "env:"

# Solution: Use secret mounts instead
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secrets
    secret:
      secretName: my-secret
```

**Cause 2: Secrets in Logs**
```bash
# Check application code
# Don't log sensitive data

# Solution: Sanitize logs
# Use log masking
# Don't print secrets
```

**Cause 3: Secrets in Git**
```bash
# Check Git history
git log --all --full-history -- <file>

# Solution: Rotate exposed secrets
# Use git-secrets or similar tools
# Move to secret management system
```

**Prevention:**
- Use secret management systems
- Never commit secrets
- Use secret mounts
- Sanitize logs
- Regular secret rotation

---

## 9. Database Connectivity

### Scenario 19: Cannot Connect to Database

**Problem:**
Application cannot connect to database.

**Symptoms:**
```bash
Error: Connection refused
Error: Timeout connecting to database
Error: Authentication failed
```

**Troubleshooting Steps:**

1. **Test connectivity:**
   ```bash
   # From application pod
   kubectl exec -it <pod> -- nc -zv <db-host> <db-port>
   ```

2. **Check database service:**
   ```bash
   kubectl get svc | grep database
   kubectl get endpoints | grep database
   ```

3. **Check credentials:**
   ```bash
   kubectl get secret <db-secret>
   kubectl get secret <db-secret> -o jsonpath='{.data.password}' | base64 -d
   ```

4. **Check network policies:**
   ```bash
   kubectl get networkpolicies
   ```

5. **Check database logs:**
   ```bash
   # Access database pod/logs
   kubectl logs <db-pod>
   ```

**Common Causes & Solutions:**

**Cause 1: Wrong Connection String**
```bash
# Check environment variables
kubectl exec <pod> -- env | grep DB

# Solution: Fix connection string
kubectl set env deployment/<name> DATABASE_URL=<correct-url>
```

**Cause 2: Network Policy Blocking**
```bash
# Check network policies
kubectl get networkpolicies

# Solution: Allow database traffic
kubectl edit networkpolicy <policy>
```

**Cause 3: Database Not Ready**
```bash
# Check database pod
kubectl get pods | grep database
kubectl describe pod <db-pod>

# Solution: Wait for database to be ready
# Or fix database issues
```

**Cause 4: Authentication Failure**
```bash
# Verify credentials
kubectl get secret <db-secret> -o yaml

# Solution: Update credentials
kubectl create secret generic <db-secret> \
  --from-literal=username=<user> \
  --from-literal=password=<pass> \
  --dry-run=client -o yaml | kubectl apply -f -
```

**Prevention:**
- Test connectivity before deployment
- Use connection pooling
- Implement retry logic
- Monitor database health
- Use proper secret management

---

### Scenario 20: Database Connection Pool Exhausted

**Problem:**
Application runs out of database connections.

**Symptoms:**
```bash
Error: Too many connections
Error: Connection pool exhausted
```

**Troubleshooting Steps:**

1. **Check active connections:**
   ```bash
   # MySQL
   mysql> SHOW PROCESSLIST;
   mysql> SHOW STATUS LIKE 'Threads_connected';
   
   # PostgreSQL
   SELECT count(*) FROM pg_stat_activity;
   ```

2. **Check connection pool settings:**
   ```bash
   # In application configuration
   # Check max_connections, pool_size
   ```

3. **Check for connection leaks:**
   ```bash
   # Monitor connections over time
   # Check if connections are closed properly
   ```

**Common Causes & Solutions:**

**Cause 1: Connection Leaks**
```bash
# Check application code
# Ensure connections are closed

# Solution: Use connection pooling
# Implement proper cleanup
# Use try-with-resources (Java)
# Use context managers (Python)
```

**Cause 2: Pool Size Too Small**
```bash
# Check pool configuration
# max_connections, pool_size

# Solution: Increase pool size
# Or increase database max_connections
```

**Cause 3: Long-Running Queries**
```bash
# Check for slow queries
# MySQL: SHOW PROCESSLIST;
# PostgreSQL: pg_stat_activity

# Solution: Optimize queries
# Add query timeouts
# Kill long-running queries
```

**Prevention:**
- Use connection pooling
- Monitor connection usage
- Set appropriate timeouts
- Optimize queries
- Implement connection limits

---

## 10. Monitoring and Logging

### Scenario 21: Missing Logs

**Problem:**
Application logs are not appearing in log aggregation system.

**Symptoms:**
```bash
No logs in CloudWatch/ELK/Splunk
Logs not being collected
```

**Troubleshooting Steps:**

1. **Check pod logs:**
   ```bash
   kubectl logs <pod>
   kubectl logs <pod> --previous
   ```

2. **Check log collector:**
   ```bash
   # Fluentd/Fluent Bit
   kubectl get pods -n logging
   kubectl logs <log-collector-pod>
   ```

3. **Check log configuration:**
   ```bash
   kubectl get configmap <log-config>
   kubectl describe pod <pod> | grep -A 5 "Mounts"
   ```

4. **Check log volume:**
   ```bash
   # Check if log volume is mounted
   kubectl describe pod <pod>
   ```

5. **Test log output:**
   ```bash
   kubectl exec <pod> -- echo "test log" > /proc/1/fd/1
   ```

**Common Causes & Solutions:**

**Cause 1: Log Collector Not Running**
```bash
# Check log collector pods
kubectl get pods -n logging

# Solution: Restart log collector
kubectl rollout restart deployment/<log-collector>
```

**Cause 2: Wrong Log Path**
```bash
# Check configured log path
kubectl get configmap <log-config> -o yaml

# Solution: Fix log path configuration
kubectl edit configmap <log-config>
```

**Cause 3: Log Volume Not Mounted**
```bash
# Check volume mounts
kubectl describe pod <pod> | grep -A 5 "Mounts"

# Solution: Add log volume mount
```

**Cause 4: Application Not Writing to stdout**
```bash
# Check application logging configuration
# Applications should log to stdout/stderr

# Solution: Configure application to log to stdout
```

**Prevention:**
- Log to stdout/stderr
- Test log collection
- Monitor log collector
- Use structured logging
- Set up log retention

---

### Scenario 22: Metrics Not Appearing

**Problem:**
Application metrics are not showing up in monitoring system.

**Symptoms:**
```bash
No metrics in Prometheus/Grafana
Metrics endpoint not accessible
```

**Troubleshooting Steps:**

1. **Check metrics endpoint:**
   ```bash
   kubectl port-forward <pod> 8080:8080
   curl http://localhost:8080/metrics
   ```

2. **Check ServiceMonitor:**
   ```bash
   kubectl get servicemonitor
   kubectl describe servicemonitor <name>
   ```

3. **Check Prometheus targets:**
   ```bash
   # Access Prometheus UI
   # Check Targets page
   ```

4. **Check service annotations:**
   ```bash
   kubectl get svc <name> -o yaml | grep -A 5 "annotations"
   ```

5. **Check network policies:**
   ```bash
   kubectl get networkpolicies
   ```

**Common Causes & Solutions:**

**Cause 1: Metrics Endpoint Not Exposed**
```bash
# Check if metrics endpoint exists
kubectl exec <pod> -- curl http://localhost:8080/metrics

# Solution: Expose metrics endpoint
# Add metrics path to application
```

**Cause 2: ServiceMonitor Not Configured**
```bash
# Check ServiceMonitor
kubectl get servicemonitor

# Solution: Create ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    path: /metrics
```

**Cause 3: Wrong Service Annotations**
```bash
# Check service annotations
kubectl get svc <name> -o yaml

# Solution: Add proper annotations
kubectl annotate svc <name> prometheus.io/scrape=true
kubectl annotate svc <name> prometheus.io/port=8080
kubectl annotate svc <name> prometheus.io/path=/metrics
```

**Prevention:**
- Expose metrics endpoint
- Configure ServiceMonitor
- Test metrics collection
- Use standard metrics format
- Monitor Prometheus targets

---

## Additional Scenarios (23-30)

### Scenario 23: DNS Resolution Failures

**Problem:**
Pods cannot resolve DNS names.

**Solution:**
```bash
# Check CoreDNS
kubectl get pods -n kube-system | grep coredns
kubectl logs -n kube-system <coredns-pod>

# Check DNS config
kubectl get configmap coredns -n kube-system -o yaml

# Test DNS
kubectl run test --image=busybox --rm -it -- nslookup kubernetes.default
```

---

### Scenario 24: Persistent Volume Not Mounting

**Problem:**
PVC created but pod cannot mount the volume.

**Solution:**
```bash
# Check PVC status
kubectl get pvc
kubectl describe pvc <name>

# Check PV
kubectl get pv
kubectl describe pv <name>

# Check storage class
kubectl get storageclass

# Check pod events
kubectl describe pod <pod> | grep -i volume
```

---

### Scenario 25: ConfigMap/Secret Not Updating

**Problem:**
Changes to ConfigMap/Secret not reflected in pods.

**Solution:**
```bash
# Check ConfigMap
kubectl get configmap <name> -o yaml

# Restart pods to pick up changes
kubectl rollout restart deployment/<name>

# Or use hash in deployment to trigger update
# Add annotation with configmap hash
```

---

### Scenario 26: Ingress Not Routing Traffic

**Problem:**
Ingress created but traffic not reaching services.

**Solution:**
```bash
# Check ingress
kubectl get ingress
kubectl describe ingress <name>

# Check ingress controller
kubectl get pods -n ingress-nginx

# Check service
kubectl get svc
kubectl describe svc <name>

# Test ingress
curl -H "Host: <hostname>" http://<ingress-ip>
```

---

### Scenario 27: Horizontal Pod Autoscaler Not Working

**Problem:**
HPA not scaling pods based on metrics.

**Solution:**
```bash
# Check HPA
kubectl get hpa
kubectl describe hpa <name>

# Check metrics server
kubectl get pods -n kube-system | grep metrics-server

# Check resource requests
kubectl get deployment <name> -o yaml | grep -A 5 "resources"

# Test metrics
kubectl top pods
```

---

### Scenario 28: Job Not Completing

**Problem:**
Kubernetes Job stuck in running state.

**Solution:**
```bash
# Check job status
kubectl get jobs
kubectl describe job <name>

# Check pod logs
kubectl logs <job-pod>

# Check activeDeadlineSeconds
kubectl get job <name> -o yaml | grep activeDeadlineSeconds

# Delete and recreate if needed
kubectl delete job <name>
```

---

### Scenario 29: StatefulSet Pods Not Starting in Order

**Problem:**
StatefulSet pods not starting sequentially.

**Solution:**
```bash
# Check StatefulSet
kubectl get statefulset
kubectl describe statefulset <name>

# Check pod management policy
kubectl get statefulset <name> -o yaml | grep podManagementPolicy

# Check PVC
kubectl get pvc
kubectl describe pvc <pvc-name>

# Ensure OrderedReady policy (default)
```

---

### Scenario 30: Canary Deployment Traffic Split Not Working

**Problem:**
Canary deployment not splitting traffic correctly.

**Solution:**
```bash
# Check VirtualService (Istio)
kubectl get virtualservice
kubectl describe virtualservice <name>

# Check DestinationRule
kubectl get destinationrule
kubectl describe destinationrule <name>

# Check service labels
kubectl get svc --show-labels

# Verify traffic split
# Use monitoring to check request distribution
```

---

## General Troubleshooting Methodology

### Step-by-Step Approach

1. **Gather Information**
   - Check logs
   - Review events
   - Examine configurations
   - Check resource status

2. **Reproduce the Issue**
   - Test locally if possible
   - Check if issue is consistent
   - Identify trigger conditions

3. **Isolate the Problem**
   - Narrow down to specific component
   - Check dependencies
   - Verify network connectivity

4. **Identify Root Cause**
   - Review error messages
   - Check recent changes
   - Compare with working state

5. **Implement Solution**
   - Apply fix
   - Test thoroughly
   - Monitor for recurrence

6. **Document and Prevent**
   - Document solution
   - Update runbooks
   - Implement monitoring
   - Add preventive measures

### Useful Commands Reference

```bash
# Kubernetes
kubectl get all -A
kubectl describe <resource> <name>
kubectl logs <pod> --previous
kubectl exec -it <pod> -- <command>
kubectl top nodes
kubectl top pods
kubectl get events --sort-by='.lastTimestamp'

# Docker
docker ps -a
docker logs <container>
docker inspect <container>
docker stats
docker system df

# Network
kubectl run test --image=busybox --rm -it -- <command>
nc -zv <host> <port>
nslookup <hostname>
dig <hostname>

# Debugging
kubectl debug <pod> -it --image=busybox
kubectl run debug --image=nicolaka/netshoot --rm -it -- <command>
```

---

## Summary

These 30 troubleshooting scenarios cover:

- **Kubernetes**: Pods, services, deployments, networking
- **Docker**: Container issues, resource constraints
- **CI/CD**: Pipeline failures, deployment issues
- **Infrastructure**: Terraform, AWS quotas
- **Network**: Connectivity, performance
- **Application**: Deployment, performance
- **Security**: Access control, secrets
- **Database**: Connectivity, connection pools
- **Monitoring**: Logs, metrics

Key principles:
- **Systematic approach**: Follow structured troubleshooting steps
- **Gather information**: Logs, events, configurations
- **Isolate problems**: Narrow down to specific components
- **Test solutions**: Verify fixes work
- **Prevent recurrence**: Document and monitor

Each scenario includes:
- Problem description
- Symptoms
- Step-by-step troubleshooting
- Common causes and solutions
- Prevention tips

Use this guide as a reference for DevOps troubleshooting interviews and real-world problem-solving.

