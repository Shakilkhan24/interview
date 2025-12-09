# DevSecOps - End-to-End Master Guide
## Complete Security Integration in DevOps Pipeline

---

## Table of Contents

1. [DevSecOps Fundamentals](#1-devsecops-fundamentals)
2. [Security in CI/CD Pipeline](#2-security-in-cicd-pipeline)
3. [SAST - Static Application Security Testing](#3-sast---static-application-security-testing)
4. [DAST - Dynamic Application Security Testing](#4-dast---dynamic-application-security-testing)
5. [Dependency Management & Scanning](#5-dependency-management--scanning)
6. [Container Security](#6-container-security)
7. [Infrastructure as Code Security](#7-infrastructure-as-code-security)
8. [Secrets Management](#8-secrets-management)
9. [Compliance & Governance](#9-compliance--governance)
10. [Security Monitoring & Logging](#10-security-monitoring--logging)
11. [Vulnerability Management](#11-vulnerability-management)
12. [Security Testing Strategies](#12-security-testing-strategies)
13. [Shift-Left Security](#13-shift-left-security)
14. [Security Tools Stack](#14-security-tools-stack)
15. [Jenkins DevSecOps Implementation](#15-jenkins-devsecops-implementation)
16. [Best Practices & Patterns](#16-best-practices--patterns)

---

## 1. DevSecOps Fundamentals

### 1.1 What is DevSecOps?

**Definition:**
DevSecOps integrates security practices into the DevOps pipeline, making security a shared responsibility across development, operations, and security teams.

**Traditional vs DevSecOps:**

```
Traditional Waterfall:
┌──────────┐  ┌──────────┐  ┌──────────┐
│   Dev    │→│   Ops    │→│ Security  │
│          │  │          │  │ (Last)   │
└──────────┘  └──────────┘  └──────────┘
   Months        Months        Weeks
   
DevSecOps Approach:
┌─────────────────────────────────────┐
│   Security Integrated Everywhere    │
├─────────────────────────────────────┤
│  Dev ←→ Security ←→ Ops             │
│  (Continuous Integration)            │
└─────────────────────────────────────┘
   Minutes        Minutes        Real-time
```

### 1.2 DevSecOps Principles

1. **Shift-Left Security** - Security early in SDLC
2. **Security as Code** - Infrastructure and policies as code
3. **Automation** - Automated security checks
4. **Continuous Monitoring** - Real-time security monitoring
5. **Shared Responsibility** - Everyone owns security
6. **Fail Fast** - Catch issues early
7. **Compliance by Design** - Build compliance into pipeline

### 1.3 DevSecOps Maturity Model

```
Level 1: Basic
- Manual security reviews
- Security at the end
- No automation

Level 2: Intermediate
- Some automated scans
- Security in CI/CD
- Basic monitoring

Level 3: Advanced
- Comprehensive automation
- Shift-left practices
- Continuous monitoring

Level 4: Expert
- Full automation
- Security by design
- Advanced threat detection
```

---

## 2. Security in CI/CD Pipeline

### 2.1 Security Gates in Pipeline

**Pipeline Stages with Security:**

```
1. Pre-Commit (Developer)
   ├── Secret scanning
   ├── Pre-commit hooks
   └── Code quality checks

2. Source Code Management
   ├── Secret detection
   ├── Branch protection
   └── Code review

3. Build Stage
   ├── Dependency scanning
   ├── SAST scanning
   └── License compliance

4. Test Stage
   ├── Unit tests with security
   ├── Integration tests
   └── Security test suites

5. Package Stage
   ├── Container scanning
   ├── Artifact signing
   └── SBOM generation

6. Deploy Stage
   ├── Infrastructure scanning
   ├── Policy validation
   └── Compliance checks

7. Runtime Stage
   ├── RASP (Runtime Application Self-Protection)
   ├── Security monitoring
   └── Incident response
```

### 2.2 Security Scanning Stages

**SAST (Static Analysis):**
- Code scanning for vulnerabilities
- Run during build stage
- Fast feedback to developers

**DAST (Dynamic Analysis):**
- Runtime security testing
- Run after deployment
- Tests running application

**IAST (Interactive Analysis):**
- Hybrid approach
- Real-time vulnerability detection
- Best of SAST and DAST

**SCA (Software Composition Analysis):**
- Dependency vulnerability scanning
- Third-party library analysis
- License compliance

---

## 3. SAST - Static Application Security Testing

### 3.1 SAST Tools

**Popular SAST Tools:**

| Tool | Language Support | Type |
|------|-----------------|------|
| SonarQube | Multi-language | Commercial/OSS |
| Semgrep | Multi-language | OSS |
| Bandit | Python | OSS |
| ESLint | JavaScript | OSS |
| Brakeman | Ruby | OSS |
| SpotBugs | Java | OSS |

**SonarQube Integration:**

```yaml
# .github/workflows/security.yml
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

**Semgrep Integration:**

```bash
# Install Semgrep
pip install semgrep

# Run scan
semgrep --config=auto .

# CI integration
semgrep --json --output=semgrep-results.json .
```

**Bandit (Python):**

```bash
# Install
pip install bandit

# Scan
bandit -r ./app -f json -o bandit-report.json

# With severity levels
bandit -r ./app --severity-level high
```

### 3.2 SAST Best Practices

1. **Run Early** - In pre-commit and CI
2. **Fail on Critical** - Block on high-severity issues
3. **Custom Rules** - Add organization-specific rules
4. **Baseline** - Establish security baseline
5. **Regular Updates** - Keep rules updated
6. **Developer Training** - Educate on findings

---

## 4. DAST - Dynamic Application Security Testing

### 4.1 DAST Tools

**OWASP ZAP:**

```bash
# Docker run
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://target-app:8080

# Full scan
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t http://target-app:8080 \
  -J zap-report.json
```

**Burp Suite:**
- Commercial tool
- Comprehensive web app testing
- API security testing

**Nuclei:**

```bash
# Install
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Scan
nuclei -u http://target-app:8080 -t nuclei-templates/

# CI integration
nuclei -u http://target-app:8080 -json -o nuclei-report.json
```

### 4.2 DAST Integration

**Post-Deployment Testing:**

```groovy
// Jenkins pipeline stage
stage('DAST') {
    steps {
        sh '''
            docker run --rm -v $(pwd):/zap/wrk/:rw \
              -t owasp/zap2docker-stable zap-full-scan.py \
              -t http://${DEPLOYMENT_URL} \
              -J zap-report.json || true
        '''
        publishHTML([
            reportName: 'ZAP Security Report',
            reportDir: '.',
            reportFiles: 'zap-report.json',
            keepAll: true
        ])
    }
}
```

---

## 5. Dependency Management & Scanning

### 5.1 Dependency Scanning Tools

**Snyk:**

```bash
# Install
npm install -g snyk

# Auth
snyk auth $SNYK_TOKEN

# Test
snyk test

# Monitor
snyk monitor

# Container scan
snyk container test myapp:latest

# Fix vulnerabilities
snyk wizard
```

**OWASP Dependency-Check:**

```bash
# Run scan
dependency-check.sh --project myproject \
  --scan ./app \
  --format JSON \
  --out dependency-report.json

# CI integration
dependency-check.sh --project myproject \
  --scan ./app \
  --failOnCVSS 7
```

**Dependabot (GitHub):**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

### 5.2 SBOM Generation

**Software Bill of Materials:**

```bash
# Syft (generate SBOM)
syft packages myapp:latest -o spdx-json > sbom.json

# Grype (scan SBOM)
grype sbom:sbom.json
```

---

## 6. Container Security

### 6.1 Container Scanning

**Trivy:**

```bash
# Install
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Scan image
trivy image myapp:latest

# JSON output
trivy image --format json --output trivy-report.json myapp:latest

# CI integration (fail on critical)
trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest

# Scan filesystem
trivy fs --security-checks vuln,config /path/to/app
```

**Anchore:**

```bash
# Install
pip install anchorecli

# Scan
anchore-cli image add myapp:latest
anchore-cli image wait myapp:latest
anchore-cli image vuln myapp:latest all
```

**Docker Scout:**

```bash
# Enable Docker Scout
docker scout cves myapp:latest

# Compare images
docker scout compare myapp:latest myapp:previous
```

### 6.2 Container Security Best Practices

1. **Minimal Base Images** - Use distroless or Alpine
2. **Non-Root User** - Run as non-root
3. **Layer Scanning** - Scan each layer
4. **Image Signing** - Sign images with Cosign
5. **Policy Enforcement** - Use admission controllers
6. **Regular Updates** - Keep base images updated

---

## 7. Infrastructure as Code Security

### 7.1 IaC Security Scanning

**Checkov:**

```bash
# Install
pip install checkov

# Scan Terraform
checkov -d ./terraform

# Scan Kubernetes
checkov -f deployment.yaml

# JSON output
checkov -d ./terraform --framework terraform -o json > checkov-report.json
```

**Tfsec:**

```bash
# Install
brew install tfsec  # macOS
# or
go install github.com/aquasecurity/tfsec/cmd/tfsec@latest

# Scan
tfsec .

# JSON output
tfsec --format json --out tfsec-report.json .
```

**OPA (Open Policy Agent):**

```rego
# policy.rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg := "Pods must run as non-root user"
}
```

### 7.2 Infrastructure Security Policies

**Kubernetes Policies:**

```yaml
# Gatekeeper policy
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
```

---

## 8. Secrets Management

### 8.1 Secret Detection

**GitGuardian:**

```bash
# Install
pip install ggshield

# Scan repository
ggshield scan repo .

# Pre-commit hook
ggshield install -m local
```

**TruffleHog:**

```bash
# Install
docker run --rm -v "$PWD:/pwd" trufflesecurity/trufflehog \
  filesystem /pwd --json

# Git scan
trufflehog git file://. --json
```

**GitLeaks:**

```bash
# Install
go install github.com/gitleaks/gitleaks/v8@latest

# Scan
gitleaks detect --source . --verbose

# CI integration
gitleaks detect --source . --no-git --exit-code 1
```

### 8.2 Secrets Management Solutions

**HashiCorp Vault:**

```hcl
# Terraform provider
provider "vault" {
  address = var.vault_addr
  token   = var.vault_token
}

# Read secret
data "vault_generic_secret" "db_credentials" {
  path = "secret/database"
}

# Use in resource
resource "aws_db_instance" "main" {
  username = data.vault_generic_secret.db_credentials.data["username"]
  password = data.vault_generic_secret.db_credentials.data["password"]
}
```

**AWS Secrets Manager:**

```hcl
# Get secret
data "aws_secretsmanager_secret" "db_password" {
  name = "production/db/password"
}

data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}
```

**Kubernetes Secrets:**

```yaml
# Create secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  username: admin
  password: secret123

# Use in deployment
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: username
```

---

## 9. Compliance & Governance

### 9.1 Compliance Frameworks

**PCI DSS:**
- Payment card data protection
- Requirements in pipeline

**HIPAA:**
- Healthcare data protection
- Encryption and access controls

**SOC 2:**
- Security, availability, processing integrity
- Continuous monitoring

**GDPR:**
- Data privacy regulations
- Data handling in pipeline

### 9.2 Policy as Code

**OPA Policies:**

```rego
# PCI DSS compliance check
package pci

deny[msg] {
    input.kind == "Deployment"
    not input.spec.template.spec.securityContext.runAsNonRoot
    msg := "PCI DSS: Containers must run as non-root"
}

deny[msg] {
    input.kind == "Service"
    input.spec.type == "LoadBalancer"
    not input.metadata.annotations["service.beta.kubernetes.io/aws-load-balancer-ssl-cert"]
    msg := "PCI DSS: Load balancers must use SSL/TLS"
}
```

**Checkov Policies:**

```yaml
# .checkov.yml
framework:
  - terraform
  - cloudformation
  - kubernetes

skip-checks:
  - CKV_AWS_20  # S3 bucket encryption (example skip)

hard-fail-on: CKV_AWS_79
```

---

## 10. Security Monitoring & Logging

### 10.1 Security Information and Event Management (SIEM)

**ELK Stack for Security:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
  
  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"
```

**Falco (Runtime Security):**

```yaml
# falco-rules.yaml
- rule: Detect Shell in Container
  desc: Notice shell activity within a container
  condition: >
    spawned_process and container and
    shell_procs and proc.tty != 0 and
    container_entrypoint
  output: >
    Shell spawned in container (user=%user.name %container.info
    shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
  priority: WARNING
```

### 10.2 Security Logging

**Centralized Logging:**

```bash
# Fluentd configuration
<source>
  @type forward
  port 24224
</source>

<match **>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name security
</match>
```

---

## 11. Vulnerability Management

### 11.1 Vulnerability Lifecycle

```
1. Discovery
   ├── Automated scanning
   ├── Manual testing
   └── Threat intelligence

2. Assessment
   ├── Severity rating (CVSS)
   ├── Exploitability
   └── Business impact

3. Remediation
   ├── Patch application
   ├── Configuration changes
   └── Workarounds

4. Verification
   ├── Re-scanning
   ├── Testing
   └── Validation

5. Monitoring
   ├── Continuous scanning
   ├── Threat feeds
   └── Incident tracking
```

### 11.2 CVSS Scoring

**Common Vulnerability Scoring System:**

- **Base Score**: 0.0 - 10.0
- **Temporal Score**: Adjusts for exploitability
- **Environmental Score**: Adjusts for environment

**Severity Levels:**
- **Critical**: 9.0 - 10.0
- **High**: 7.0 - 8.9
- **Medium**: 4.0 - 6.9
- **Low**: 0.1 - 3.9
- **None**: 0.0

---

## 12. Security Testing Strategies

### 12.1 Security Test Types

**Unit Security Tests:**

```python
# test_security.py
import pytest
from app import app

def test_sql_injection_protection():
    """Test SQL injection protection"""
    response = app.test_client().get('/users?id=1 OR 1=1')
    assert response.status_code == 400

def test_xss_protection():
    """Test XSS protection"""
    response = app.test_client().post('/search', data={
        'query': '<script>alert("xss")</script>'
    })
    assert '<script>' not in response.data.decode()
```

**Integration Security Tests:**

```python
def test_authentication_required():
    """Test that authentication is required"""
    response = app.test_client().get('/admin')
    assert response.status_code == 401

def test_authorization():
    """Test proper authorization"""
    # Login as regular user
    token = login_user('user', 'password')
    response = app.test_client().get(
        '/admin',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403
```

### 12.2 Penetration Testing

**Automated Pen Testing:**

```bash
# OWASP ZAP automated scan
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t http://target-app:8080 \
  -J zap-report.json

# Nuclei templates
nuclei -u http://target-app:8080 \
  -t nuclei-templates/ \
  -severity high,critical
```

---

## 13. Shift-Left Security

### 13.1 Pre-Commit Hooks

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", ".", "-f", "json", "-o", "bandit-report.json"]

  - repo: https://github.com/aquasecurity/trivy
    rev: v0.40.0
    hooks:
      - id: trivy-fs
        args: ['--exit-code', '1', '--severity', 'HIGH,CRITICAL']
```

**Installation:**

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### 13.2 IDE Integration

**VS Code Security Extensions:**
- SonarLint
- Snyk
- Docker Security Scanning
- Kubernetes Security

---

## 14. Security Tools Stack

### 14.1 Complete Tool Stack

```
┌─────────────────────────────────────────┐
│         Security Tools Stack            │
├─────────────────────────────────────────┤
│ SAST:     SonarQube, Semgrep, Bandit   │
│ DAST:     OWASP ZAP, Burp Suite        │
│ SCA:      Snyk, OWASP Dependency-Check │
│ Container: Trivy, Anchore, Docker Scout│
│ IaC:      Checkov, Tfsec, OPA          │
│ Secrets:  GitGuardian, TruffleHog      │
│ Runtime:  Falco, Sysdig                │
│ SIEM:     ELK, Splunk, Datadog         │
│ Secrets Mgmt: Vault, AWS Secrets Manager│
└─────────────────────────────────────────┘
```

### 14.2 Tool Selection Criteria

1. **Language Support** - Supports your stack
2. **Integration** - CI/CD integration
3. **Performance** - Scan speed
4. **Accuracy** - Low false positives
5. **Cost** - License costs
6. **Community** - Active development

---

## 15. Jenkins DevSecOps Implementation

See the complete Jenkins project in `Jenkins-DevSecOps-Project/` directory.

### 15.1 Pipeline Structure

```
Jenkins DevSecOps Pipeline:
├── Checkout
├── Pre-Commit Security
├── Build
├── SAST
├── Dependency Scan
├── Container Scan
├── IaC Scan
├── Unit Tests
├── Security Tests
├── Compliance Check
├── Deploy Dev
├── DAST
├── Deploy Prod (with approval)
└── Post-Deploy Monitoring
```

---

## 16. Best Practices & Patterns

### 16.1 Security Best Practices

1. **Security by Design** - Build security in from start
2. **Least Privilege** - Minimum required permissions
3. **Defense in Depth** - Multiple security layers
4. **Automation** - Automate security checks
5. **Continuous Monitoring** - Real-time security monitoring
6. **Incident Response** - Have response plan ready
7. **Security Training** - Regular team training
8. **Regular Updates** - Keep tools and dependencies updated

### 16.2 Security Metrics

- **Mean Time to Detect (MTTD)** - How quickly issues found
- **Mean Time to Respond (MTTR)** - How quickly issues fixed
- **Vulnerability Density** - Issues per 1000 lines of code
- **Scan Coverage** - Percentage of code scanned
- **Compliance Score** - Policy compliance percentage

---

## Conclusion

### Key Takeaways:

1. **Security is Everyone's Responsibility**
2. **Automate Security Checks** - Don't rely on manual reviews
3. **Shift-Left** - Find issues early
4. **Continuous Monitoring** - Security doesn't stop at deployment
5. **Compliance by Design** - Build compliance into pipeline
6. **Tool Integration** - Use appropriate tools for each stage
7. **Regular Updates** - Keep security tools and dependencies current

---

*DevSecOps - End-to-End Master Guide*
*Complete Security Integration in DevOps Pipeline*
*Last Updated: 2024*

