# Jenkins DevSecOps End-to-End Project
## Complete CI/CD Pipeline with Comprehensive Security Integration

This project demonstrates a complete DevSecOps implementation using Jenkins, integrating security at every stage of the CI/CD pipeline from code commit to production deployment.

---

## 🎯 Project Overview

This DevSecOps project provides:

- **Complete CI/CD Pipeline** - Full Jenkins pipeline with security integration
- **Multi-Stage Security Scanning** - SAST, DAST, Container, IaC scanning
- **Automated Security Testing** - Security test suites integrated
- **Compliance Validation** - Automated compliance checks
- **Secrets Management** - Secure secrets handling
- **Infrastructure as Code** - Terraform and Kubernetes configurations
- **Container Security** - Multi-stage Docker builds with security best practices

---

## 📁 Project Structure

```
Jenkins-DevSecOps-Project/
├── README.md                          # This file
├── Jenkinsfile.devsecops              # Main DevSecOps Jenkins pipeline
├── .pre-commit-config.yaml           # Pre-commit hooks configuration
├── .gitignore                         # Git ignore rules
├── .trivyignore                       # Trivy ignore rules (optional)
├── scripts/
│   ├── install-tools.sh              # Install all security tools
│   ├── security-scan.sh              # Security scanning wrapper script
│   └── deploy.sh                     # Deployment script
├── docker/
│   ├── Dockerfile                    # Multi-stage secure Dockerfile
│   └── docker-compose.yml            # Multi-container setup
├── terraform/                         # Infrastructure as Code (optional)
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── k8s/
│   ├── deployment.yaml               # Kubernetes deployment
│   ├── service.yaml                  # Kubernetes service
│   └── network-policy.yaml           # Network security policy
├── app/
│   ├── app.py                        # Sample Python Flask application
│   ├── requirements.txt              # Python dependencies
│   └── tests/
│       ├── test_app.py               # Unit tests
│       └── security_test.py          # Security tests
└── security-policies/
    ├── opa-policy.rego               # OPA/Rego security policies
    └── gatekeeper-policy.yaml        # Kubernetes Gatekeeper policies (optional)
```

---

## 🚀 Prerequisites

### Required Software

1. **Jenkins** (2.400+)
   - Docker Pipeline plugin
   - GitHub Integration plugin
   - Credentials Binding plugin
   - HTML Publisher plugin
   - Warnings NG plugin

2. **Docker** - Installed on Jenkins agent
3. **Kubectl** - Configured (if using Kubernetes)
4. **Git** - For repository management

### Required Jenkins Plugins

Install the following Jenkins plugins:

```bash
# Core plugins
- Docker Pipeline
- GitHub Integration
- Credentials Binding
- HTML Publisher
- Warnings NG

# Security plugins (optional but recommended)
- Trivy Plugin
- Snyk Security Scanner
- SonarQube Scanner
```

### Security Tools

The `scripts/install-tools.sh` script will install:
- Trivy (Container & filesystem scanning)
- Semgrep (SAST)
- Bandit (Python security linter)
- Snyk (Dependency scanning)
- GitLeaks (Secret detection)
- Checkov (IaC scanning)
- Tfsec (Terraform security)
- OPA (Policy engine)
- OWASP Dependency-Check
- Nuclei (DAST)

---

## ⚙️ Setup Instructions

### 1. Install Security Tools on Jenkins Agent

```bash
# Make script executable
chmod +x scripts/install-tools.sh

# Run installation
./scripts/install-tools.sh
```

### 2. Configure Jenkins Credentials

Add the following credentials in Jenkins (Manage Jenkins → Credentials):

| Credential ID | Type | Description |
|--------------|------|-------------|
| `github-token` | Secret text | GitHub personal access token |
| `dockerhub-credentials` | Username with password | Docker Hub credentials |
| `aws-credentials` | AWS credentials | AWS access key and secret |
| `vault-token` | Secret text | HashiCorp Vault token (optional) |
| `kubeconfig` | Secret file | Kubernetes configuration file |
| `snyk-token` | Secret text | Snyk API token (optional) |
| `sonar-token` | Secret text | SonarQube token (optional) |

**Adding Credentials:**

1. Go to Jenkins → Manage Jenkins → Credentials
2. Add credentials for each required service
3. Use the credential IDs exactly as shown above

### 3. Configure Jenkins Pipeline

1. **Create New Pipeline Job:**
   - Go to Jenkins → New Item
   - Select "Pipeline"
   - Enter name: `DevSecOps-Pipeline`

2. **Configure Pipeline:**
   - Pipeline definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your repository URL
   - Branch: `*/main` or `*/develop`
   - Script Path: `Jenkinsfile.devsecops`

3. **Configure Build Triggers:**
   - GitHub hook trigger for GITScm polling (if using GitHub)
   - Poll SCM: `H/5 * * * *` (every 5 minutes)

### 4. Environment Setup

Create environment files:

```bash
# .env.production
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@db:5432/dbname
API_KEY=your-secure-api-key
```

### 5. Secrets Setup

Create secrets directory:

```bash
mkdir -p docker/secrets
echo "your-db-password" > docker/secrets/db_password.txt
echo "your-api-key" > docker/secrets/api_key.txt
chmod 600 docker/secrets/*.txt
```

---

## 🔄 Pipeline Stages

The DevSecOps pipeline includes the following stages:

### 1. **Checkout**
- Clone repository
- Extract commit information

### 2. **Pre-Commit Security**
- Secret detection (GitGuardian, TruffleHog, GitLeaks)
- Code quality checks
- Pre-commit hook validation

### 3. **Build**
- Install dependencies
- Build application
- Build Docker image

### 4. **SAST - Static Application Security Testing**
- SonarQube scan (code quality & security)
- Semgrep scan (pattern-based security)
- Bandit scan (Python security linter)

### 5. **Dependency Scanning**
- Snyk dependency scan
- OWASP Dependency-Check
- License compliance check

### 6. **Container Security**
- Trivy image scan (vulnerabilities)
- Trivy filesystem scan (config issues)
- Docker Scout analysis

### 7. **Infrastructure Security**
- Checkov scan (IaC security)
- Tfsec scan (Terraform security)
- OPA policy validation

### 8. **Unit Tests**
- Run unit test suite
- Generate coverage reports
- Publish test results

### 9. **Security Tests**
- Security test suite execution
- Penetration testing (optional)

### 10. **Compliance Check**
- OPA policy evaluation
- Compliance framework validation
- Policy as code checks

### 11. **Push Image**
- Push to container registry
- Tag with version and latest

### 12. **Deploy to Dev**
- Deploy to development environment
- Wait for rollout
- Verify deployment

### 13. **DAST - Dynamic Application Security Testing**
- OWASP ZAP full scan
- Nuclei vulnerability scan
- Runtime security testing

### 14. **Approve Production Deployment**
- Manual approval gate
- Production deployment authorization

### 15. **Deploy to Production**
- Deploy to production environment
- Automatic rollback on failure
- Health check verification

### 16. **Post-Deploy Security**
- Runtime security monitoring
- Security event detection
- Continuous monitoring

---

## 🔒 Security Features

### Application Security

- **Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP, HSTS
- **Authentication**: API key authentication
- **Input Validation**: Sanitized inputs, length limits
- **Error Handling**: Secure error messages
- **Logging**: Security event logging

### Container Security

- **Multi-stage Build**: Minimal production image
- **Non-root User**: Containers run as non-root
- **Read-only Filesystem**: Immutable container filesystem
- **Resource Limits**: CPU and memory limits
- **Health Checks**: Application health monitoring

### Infrastructure Security

- **Network Policies**: Kubernetes network isolation
- **Security Contexts**: Pod and container security
- **Secrets Management**: Kubernetes secrets, Vault integration
- **RBAC**: Role-based access control
- **Encryption**: Data encryption at rest and in transit

---

## 📊 Security Reports

The pipeline generates and publishes the following security reports:

- **Semgrep Report**: Static analysis findings
- **Bandit Report**: Python security issues
- **Trivy Reports**: Container and filesystem vulnerabilities
- **OWASP Dependency-Check**: Dependency vulnerabilities
- **Checkov Reports**: Infrastructure security issues
- **ZAP Report**: Dynamic analysis results

All reports are published as HTML artifacts in Jenkins build.

---

## 🛠️ Usage

### Running the Pipeline

**Manual Trigger:**
1. Go to Jenkins → DevSecOps-Pipeline
2. Click "Build Now"

**Automatic Trigger:**
- Push to repository (if webhook configured)
- Scheduled builds (if poll SCM configured)

### Pipeline Parameters

The pipeline supports the following environment variables:

```groovy
APP_NAME              // Application name
ENV                   // Environment (dev/prod)
DOCKER_REGISTRY       // Container registry URL
```

### Running Specific Stages

To run only specific stages, modify the `Jenkinsfile.devsecops` and comment out unwanted stages, or use Jenkins "Stage View" to re-run failed stages.

---

## 🔧 Configuration

### Customizing Security Thresholds

**Fail on Critical Issues:**

```groovy
// In Jenkinsfile
trivy image --exit-code 1 --severity HIGH,CRITICAL
```

**Adjust SAST Sensitivity:**

```groovy
semgrep --config=auto --severity=ERROR
```

### Ignoring False Positives

**Trivy Ignore:**

Create `.trivyignore`:
```
CVE-2021-XXXXX  # Reason for ignoring
```

**Bandit Ignore:**

```python
# nosec
password = "hardcoded"  # Ignore this specific finding
```

---

## 📈 Monitoring & Metrics

### Security Metrics

The pipeline tracks:

- **Vulnerability Count**: By severity level
- **Scan Coverage**: Percentage of code scanned
- **Mean Time to Detect (MTTD)**: Time to find issues
- **Mean Time to Remediate (MTTR)**: Time to fix issues
- **Compliance Score**: Policy compliance percentage

### Jenkins Metrics

- Build success rate
- Average build time
- Security scan duration
- Deployment frequency

---

## 🚨 Troubleshooting

### Common Issues

**1. Tool Not Found**
```bash
# Solution: Run install script
./scripts/install-tools.sh
```

**2. Permission Denied**
```bash
# Solution: Check Jenkins agent permissions
sudo chmod +x scripts/*.sh
```

**3. Credential Errors**
```bash
# Solution: Verify credentials in Jenkins
# Manage Jenkins → Credentials → Check credential IDs
```

**4. Scan Failures**
```bash
# Solution: Check ignore files
# .trivyignore, .banditignore, etc.
```

**5. Docker Build Fails**
```bash
# Solution: Check Docker daemon is running
sudo systemctl status docker
```

**6. Kubernetes Deployment Fails**
```bash
# Solution: Verify kubectl configuration
kubectl cluster-info
kubectl get nodes
```

### Debug Mode

Enable debug logging:

```groovy
// In Jenkinsfile
sh '''
    set -x  # Enable debug
    # Your command here
'''
```

### Pipeline Logs

View detailed logs:
- Jenkins → Build → Console Output
- Check specific stage logs
- Review security scan outputs

---

## ✅ Best Practices

1. **Fail Fast**: Pipeline fails on critical security issues
2. **Approval Gates**: Manual approval for production deployments
3. **Security Reports**: All scans generate reports for review
4. **Secrets Management**: Never hardcode secrets, use Vault/secrets manager
5. **Infrastructure as Code**: All infrastructure defined in code
6. **Compliance**: Automated compliance checks in pipeline
7. **Regular Updates**: Keep security tools and dependencies updated
8. **Documentation**: Document security decisions and policies
9. **Training**: Regular security training for team
10. **Incident Response**: Have incident response plan ready

---

## 🔐 Security Policies

### OPA Policies

Located in `security-policies/opa-policy.rego`:

- Container security policies
- Resource limit requirements
- Network policy enforcement
- Compliance checks (PCI DSS, HIPAA)

### Kubernetes Policies

Located in `k8s/network-policy.yaml`:

- Network isolation
- Ingress/egress rules
- Namespace policies

---

## 📚 Additional Resources

### Documentation

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [OPA Documentation](https://www.openpolicyagent.org/docs/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)

### Security Standards

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## 🤝 Contributing

1. Follow security best practices
2. Add security tests for new features
3. Update security policies as needed
4. Review security scan results before merging
5. Update documentation for changes

---

## 📄 License

MIT License

---

## 🆘 Support

For issues or questions:
- Open an issue in the repository
- Check troubleshooting section
- Review Jenkins console logs
- Consult security tool documentation

---

## 📝 Changelog

### Version 1.0.0
- Initial DevSecOps pipeline implementation
- Complete security scanning integration
- Multi-stage Docker builds
- Kubernetes deployment configurations
- Comprehensive security testing

---

*Last Updated: 2024*
*DevSecOps End-to-End Project*
