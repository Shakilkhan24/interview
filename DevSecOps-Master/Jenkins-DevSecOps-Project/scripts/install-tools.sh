#!/bin/bash
# Install Security Tools for DevSecOps Pipeline

set -e

echo "Installing security tools for DevSecOps pipeline..."

# Update package list
sudo apt-get update

# Install basic tools
sudo apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    python3 \
    python3-pip \
    nodejs \
    npm

# Install Trivy
if ! command -v trivy &> /dev/null; then
    echo "Installing Trivy..."
    sudo apt-get install -y wget apt-transport-https gnupg lsb-release
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
    sudo apt-get update
    sudo apt-get install -y trivy
fi

# Install Semgrep
echo "Installing Semgrep..."
pip3 install semgrep || true

# Install Bandit (Python security linter)
echo "Installing Bandit..."
pip3 install bandit || true

# Install Snyk
if ! command -v snyk &> /dev/null; then
    echo "Installing Snyk..."
    npm install -g snyk || true
fi

# Install GitLeaks
if ! command -v gitleaks &> /dev/null; then
    echo "Installing GitLeaks..."
    wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
    tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
    sudo mv gitleaks /usr/local/bin/
    rm gitleaks_8.18.0_linux_x64.tar.gz
fi

# Install Checkov
echo "Installing Checkov..."
pip3 install checkov || true

# Install Tfsec
if ! command -v tfsec &> /dev/null; then
    echo "Installing Tfsec..."
    wget https://github.com/aquasecurity/tfsec/releases/download/v1.28.4/tfsec-linux-amd64
    chmod +x tfsec-linux-amd64
    sudo mv tfsec-linux-amd64 /usr/local/bin/tfsec
fi

# Install OWASP Dependency-Check
if [ ! -f dependency-check.sh ]; then
    echo "Installing OWASP Dependency-Check..."
    wget https://github.com/jeremylong/DependencyCheck/releases/download/v8.4.0/dependency-check-8.4.0-release.zip
    unzip dependency-check-8.4.0-release.zip
    mv dependency-check dependency-check-bin
    echo '#!/bin/bash
java -jar "$(dirname "$0")/dependency-check-bin/bin/dependency-check.sh" "$@"' > dependency-check.sh
    chmod +x dependency-check.sh
fi

# Install Nuclei
if ! command -v nuclei &> /dev/null; then
    echo "Installing Nuclei..."
    go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest || {
        # Fallback: download binary
        wget https://github.com/projectdiscovery/nuclei/releases/download/v2.9.15/nuclei_2.9.15_linux_amd64.zip
        unzip nuclei_2.9.15_linux_amd64.zip
        sudo mv nuclei /usr/local/bin/
        rm nuclei_2.9.15_linux_amd64.zip
    }
fi

# Install OPA (Open Policy Agent)
if ! command -v opa &> /dev/null; then
    echo "Installing OPA..."
    curl -L -o opa https://openpolicyagent.org/downloads/v0.58.0/opa_linux_amd64
    chmod +x opa
    sudo mv opa /usr/local/bin/
fi

# Install Docker (if not present)
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Install kubectl (if not present)
if ! command -v kubectl &> /dev/null; then
    echo "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
fi

echo "Security tools installation completed!"
echo ""
echo "Installed tools:"
echo "  - Trivy: $(trivy --version | head -1 || echo 'Not found')"
echo "  - Semgrep: $(semgrep --version || echo 'Not found')"
echo "  - Bandit: $(bandit --version || echo 'Not found')"
echo "  - Snyk: $(snyk --version || echo 'Not found')"
echo "  - GitLeaks: $(gitleaks version || echo 'Not found')"
echo "  - Checkov: $(checkov --version || echo 'Not found')"
echo "  - Tfsec: $(tfsec --version || echo 'Not found')"
echo "  - OPA: $(opa version || echo 'Not found')"

