# DevSecOps Project Quick Start Guide

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Prerequisites

```bash
# On Jenkins agent/worker node
sudo apt-get update
sudo apt-get install -y docker.io git curl wget

# Make install script executable
chmod +x scripts/install-tools.sh
./scripts/install-tools.sh
```

### Step 2: Configure Jenkins

1. **Install Required Plugins:**
   - Jenkins → Manage Jenkins → Manage Plugins
   - Install: Docker Pipeline, GitHub Integration, HTML Publisher

2. **Add Credentials:**
   - Jenkins → Manage Jenkins → Credentials
   - Add:
     - `dockerhub-credentials` (Docker Hub username/password)
     - `github-token` (GitHub personal access token)

### Step 3: Create Pipeline Job

1. Jenkins → New Item → Pipeline
2. Name: `DevSecOps-Pipeline`
3. Pipeline → Definition: Pipeline script from SCM
4. SCM: Git
5. Repository: Your repo URL
6. Script Path: `Jenkinsfile.devsecops`

### Step 4: Run Pipeline

```bash
# Trigger build
# Or push to repository if webhook configured
```

## 📋 Minimal Test Run

To test without full setup:

```bash
# Test secret detection
gitleaks detect --source . --no-git

# Test container scan
trivy image hello-world:latest

# Test SAST
semgrep --config=auto .
```

## 🔍 Verify Installation

```bash
# Check tools
trivy --version
semgrep --version
bandit --version
snyk --version
gitleaks version
checkov --version
tfsec --version
```

## ⚡ Common Commands

```bash
# Run full pipeline locally (Jenkinsfile simulation)
docker-compose up --build

# Run security scans manually
./scripts/security-scan.sh

# Deploy manually
./scripts/deploy.sh dev
```

---

**Next Steps:**
- Read full [README.md](README.md) for detailed documentation
- Customize security thresholds in `Jenkinsfile.devsecops`
- Add your application code to `app/` directory
- Configure your deployment targets

