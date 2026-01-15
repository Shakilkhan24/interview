# GitHub Actions CI/CD - Complete Guide
## End-to-End Concepts and Best Practices

---

## Table of Contents
1. [Introduction to GitHub Actions](#1-introduction-to-github-actions)
2. [Core Concepts](#2-core-concepts)
3. [Workflow Syntax](#3-workflow-syntax)
4. [Events and Triggers](#4-events-and-triggers)
5. [Jobs and Steps](#5-jobs-and-steps)
6. [Runners and Environments](#6-runners-and-environments)
7. [Secrets and Security](#7-secrets-and-security)
8. [Advanced Features](#8-advanced-features)
9. [Best Practices](#9-best-practices)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Introduction to GitHub Actions

### What is GitHub Actions?

GitHub Actions is a CI/CD platform built into GitHub that allows you to automate workflows directly in your repository. It enables you to build, test, and deploy code right from GitHub.

### Key Features

- **Native Integration**: Built into GitHub, no separate service needed
- **Event-Driven**: Trigger workflows on any GitHub event
- **Matrix Builds**: Test across multiple OS/versions simultaneously
- **Free for Public Repos**: Unlimited minutes for public repositories
- **Marketplace**: 10,000+ pre-built actions
- **Self-Hosted Runners**: Run workflows on your own infrastructure

### GitHub Actions vs Jenkins

| Feature | GitHub Actions | Jenkins |
|---------|---------------|---------|
| Setup | ✅ Zero setup | ⚠️ Requires installation |
| Pricing | ✅ Free for public repos | ✅ Free (self-hosted) |
| Integration | ✅ Native GitHub | ⚠️ Requires plugins |
| Learning Curve | ✅ YAML-based, simple | ⚠️ Groovy, steeper |
| Scalability | ✅ GitHub-hosted runners | ✅ Self-hosted agents |
| Marketplace | ✅ Extensive | ✅ Extensive |

---

## 2. Core Concepts

### Workflow

A workflow is an automated procedure defined in a YAML file in `.github/workflows/`. A workflow contains one or more jobs.

```
.github/
└── workflows/
    ├── ci.yml          # Continuous Integration
    ├── cd.yml          # Continuous Deployment
    └── release.yml     # Release workflow
```

### Workflow File Structure

```yaml
name: CI Workflow

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
```

### Key Components

1. **Workflow**: The entire automation process
2. **Event**: What triggers the workflow
3. **Job**: A set of steps that run on the same runner
4. **Step**: Individual task in a job
5. **Action**: Reusable unit of code
6. **Runner**: Server that executes jobs

---

## 3. Workflow Syntax

### Basic Workflow

```yaml
name: My Workflow

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run tests
        run: npm test
```

### Workflow Triggers

```yaml
on:
  # Push to branches
  push:
    branches:
      - main
      - 'releases/**'
    tags:
      - 'v*'
  
  # Pull requests
  pull_request:
    branches: [ main ]
    types: [ opened, synchronize, reopened ]
  
  # Schedule (cron)
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production
  
  # Webhook events
  repository_dispatch:
    types: [ deployment ]
  
  # Multiple events
  workflow_call:
    inputs:
      version:
        required: true
        type: string
```

### Jobs

```yaml
jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    timeout-minutes: 30
    env:
      NODE_ENV: production
    
    steps:
      - run: echo "Building..."
  
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: build  # Run after build job
    if: github.ref == 'refs/heads/main'
    
    steps:
      - run: echo "Testing..."
  
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: [build, test]  # Run after both jobs
    if: success()  # Only if previous jobs succeeded
    
    steps:
      - run: echo "Deploying..."
```

### Steps

```yaml
steps:
  # Using an action
  - name: Checkout repository
    uses: actions/checkout@v3
  
  # Using an action with inputs
  - name: Setup Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.11'
      cache: 'pip'
  
  # Run a command
  - name: Install dependencies
    run: pip install -r requirements.txt
  
  # Run with shell
  - name: Build
    shell: bash
    run: |
      echo "Building..."
      npm run build
  
  # Conditional step
  - name: Deploy
    if: github.ref == 'refs/heads/main'
    run: ./deploy.sh
  
  # Using environment variables
  - name: Build with env
    env:
      API_KEY: ${{ secrets.API_KEY }}
      VERSION: ${{ github.sha }}
    run: |
      echo "Building version $VERSION"
      npm run build -- --api-key=$API_KEY
```

---

## 4. Events and Triggers

### Push Events

```yaml
on:
  push:
    branches:
      - main
      - 'feature/**'
    paths:
      - 'src/**'
      - 'package.json'
    branches-ignore:
      - 'dependabot/**'
```

### Pull Request Events

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main
    paths:
      - '**.js'
      - '**.ts'
```

### Scheduled Events

```yaml
on:
  schedule:
    # Every day at midnight UTC
    - cron: '0 0 * * *'
    # Every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
    # Every hour
    - cron: '0 * * * *'
```

### Manual Triggers

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production
        default: 'staging'
      
      version:
        description: 'Application version'
        required: false
        type: string
        default: 'latest'
      
      force_deploy:
        description: 'Force deployment'
        required: false
        type: boolean

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          echo "Deploying to ${{ inputs.environment }}"
          echo "Version: ${{ inputs.version }}"
          if [ "${{ inputs.force_deploy }}" == "true" ]; then
            echo "Force deployment enabled"
          fi
```

### Workflow Call (Reusable Workflows)

```yaml
# .github/workflows/reusable.yml
name: Reusable Workflow

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: false
        type: string
        default: 'latest'
    secrets:
      api_key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.api_key }}
        run: |
          echo "Deploying ${{ inputs.version }} to ${{ inputs.environment }}"

# .github/workflows/main.yml
name: Main Workflow

on:
  push:
    branches: [ main ]

jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: production
      version: ${{ github.sha }}
    secrets:
      api_key: ${{ secrets.DEPLOY_API_KEY }}
```

---

## 5. Jobs and Steps

### Job Dependencies

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint
  
  test:
    runs-on: ubuntu-latest
    needs: lint  # Wait for lint to complete
    steps:
      - run: npm test
  
  build:
    runs-on: ubuntu-latest
    needs: [lint, test]  # Wait for both
    steps:
      - run: npm run build
  
  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - run: npm run deploy
```

### Matrix Strategy

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
        exclude:
          # Exclude Windows with Node 14
          - os: windows-latest
            node-version: 14
        include:
          # Add specific combination
          - os: ubuntu-latest
            node-version: 21
            experimental: true
    
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Parallel Jobs

```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:unit
  
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:integration
  
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e
  
  deploy:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests, e2e-tests]
    if: success()
    steps:
      - run: npm run deploy
```

### Job Outputs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      image: ${{ steps.build.outputs.image }}
    
    steps:
      - name: Get version
        id: version
        run: echo "version=v1.0.0" >> $GITHUB_OUTPUT
      
      - name: Build image
        id: build
        run: |
          IMAGE="myapp:${{ steps.version.outputs.version }}"
          docker build -t $IMAGE .
          echo "image=$IMAGE" >> $GITHUB_OUTPUT
  
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy
        run: |
          echo "Deploying ${{ needs.build.outputs.image }}"
          echo "Version: ${{ needs.build.outputs.version }}"
```

### Conditional Execution

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy
        if: success()
        run: ./deploy.sh
      
      - name: Notify
        if: failure()
        run: ./notify-failure.sh
```

---

## 6. Runners and Environments

### GitHub-Hosted Runners

```yaml
jobs:
  ubuntu:
    runs-on: ubuntu-latest  # Ubuntu 22.04
  
  windows:
    runs-on: windows-latest  # Windows Server 2022
  
  macos:
    runs-on: macos-latest  # macOS 12
  
  # Specific versions
  ubuntu-20:
    runs-on: ubuntu-20.04
  
  windows-2019:
    runs-on: windows-2019
```

### Self-Hosted Runners

```yaml
jobs:
  build:
    runs-on: self-hosted
    # Or with labels
    runs-on: [self-hosted, linux, docker]
    
    steps:
      - run: echo "Running on self-hosted runner"
```

**Setting up Self-Hosted Runner:**

```bash
# Download runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz \
  -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/OWNER/REPO --token TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### Environments

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    
    steps:
      - name: Deploy
        run: ./deploy.sh
```

**Environment Protection Rules:**

```yaml
# Configure in repository settings
# Settings → Environments → New environment

# Protection rules:
# - Required reviewers
# - Wait timer
# - Deployment branches
```

**Using Environment Secrets:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}  # From environment
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: ./deploy.sh
```

---

## 7. Secrets and Security

### Storing Secrets

```
Repository Settings → Secrets and variables → Actions
- New repository secret
- New repository variable (non-sensitive)
```

### Using Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          echo "Deploying with API key"
          ./deploy.sh
```

### Secret Masking

```yaml
steps:
  - name: Print secret (masked)
    run: echo "API key: ${{ secrets.API_KEY }}"
    # Output: API key: ***
```

### OIDC for Cloud Providers

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions
          aws-region: us-east-1
      
      - name: Deploy to S3
        run: aws s3 sync dist/ s3://my-bucket/
```

### Security Best Practices

1. **Never commit secrets**
   ```yaml
   # ❌ Bad
   env:
     API_KEY: "sk-1234567890"
   
   # ✅ Good
   env:
     API_KEY: ${{ secrets.API_KEY }}
   ```

2. **Use least privilege**
   ```yaml
   permissions:
     contents: read
     pull-requests: write
   ```

3. **Pin action versions**
   ```yaml
   # ❌ Bad
   - uses: actions/checkout@main
   
   # ✅ Good
   - uses: actions/checkout@v3
   ```

4. **Scan for secrets**
   ```yaml
   - name: Check for secrets
     uses: trufflesecurity/trufflehog@main
     with:
       path: ./
   ```

---

## 8. Advanced Features

### Caching

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      
      - name: Install dependencies
        run: npm ci
```

### Artifacts

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
          retention-days: 7
  
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
      
      - name: Deploy
        run: ./deploy.sh
```

### Composite Actions

```yaml
# .github/actions/setup-node/action.yml
name: 'Setup Node.js'
description: 'Setup Node.js with caching'
inputs:
  node-version:
    description: 'Node.js version'
    required: true
  cache:
    description: 'Enable npm cache'
    required: false
    default: 'true'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v3
      with:
        node-version: ${{ inputs.node-version }}
        cache: ${{ inputs.cache }}
    
    - name: Install dependencies
      shell: bash
      run: npm ci

# Usage in workflow
steps:
  - uses: ./.github/actions/setup-node
    with:
      node-version: '18'
      cache: 'true'
```

### Docker Actions

```yaml
# .github/actions/my-action/action.yml
name: 'My Docker Action'
inputs:
  version:
    required: true
    description: 'Version to use'

runs:
  using: 'docker'
  image: 'Dockerfile'

# Dockerfile
FROM node:18
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

### Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - name: Test with Postgres
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
        run: npm test
```

### Concurrency

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    concurrency:
      group: deploy-production
      cancel-in-progress: true  # Cancel previous runs
    
    steps:
      - name: Deploy
        run: ./deploy.sh
```

---

## 9. Best Practices

### Workflow Organization

```
.github/
└── workflows/
    ├── ci.yml              # Continuous Integration
    ├── cd.yml              # Continuous Deployment
    ├── release.yml         # Release workflow
    ├── security.yml        # Security scans
    └── dependency-update.yml  # Dependency updates
```

### Naming Conventions

```yaml
name: CI - Build and Test  # Descriptive names

jobs:
  build-and-test:  # Use kebab-case
    name: Build and Test Application
```

### Reusability

```yaml
# Use reusable workflows
# .github/workflows/build.yml
name: Build Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
```

### Error Handling

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        id: deploy
        continue-on-error: true
        run: ./deploy.sh
      
      - name: Rollback on failure
        if: steps.deploy.outcome == 'failure'
        run: ./rollback.sh
```

### Performance Optimization

1. **Use caching**
   ```yaml
   - uses: actions/cache@v3
     with:
       path: node_modules
       key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
   ```

2. **Parallel jobs**
   ```yaml
   jobs:
     lint:
     test:
     build:
     # All run in parallel
   ```

3. **Conditional steps**
   ```yaml
   - name: Deploy
     if: github.ref == 'refs/heads/main'
     run: ./deploy.sh
   ```

4. **Matrix optimization**
   ```yaml
   strategy:
     fail-fast: true  # Stop on first failure
     max-parallel: 4  # Limit parallel jobs
   ```

---

## 10. Troubleshooting

### Common Issues

#### Workflow Not Triggering

```yaml
# Check event syntax
on:
  push:
    branches: [ main ]  # Correct
    # branches: main    # Incorrect
```

#### Permission Denied

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Required for pushing
    steps:
      - run: git push
```

#### Secret Not Found

```yaml
# Verify secret exists in repository settings
# Settings → Secrets and variables → Actions

# Check secret name (case-sensitive)
env:
  API_KEY: ${{ secrets.API_KEY }}  # Must match exactly
```

#### Matrix Job Failing

```yaml
strategy:
  fail-fast: false  # Continue other matrix jobs on failure
  matrix:
    node: [14, 16, 18]
```

### Debugging

```yaml
steps:
  - name: Debug
    run: |
      echo "Branch: ${{ github.ref }}"
      echo "SHA: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
      env | sort
```

### Enable Debug Logging

```
Repository Settings → Secrets and variables → Actions
Add secret: ACTIONS_STEP_DEBUG = true
Add secret: ACTIONS_RUNNER_DEBUG = true
```

---

## Summary

GitHub Actions provides:

- **Native Integration**: Built into GitHub
- **Event-Driven**: Trigger on any GitHub event
- **Easy Setup**: YAML-based, no installation needed
- **Extensive Marketplace**: 10,000+ actions
- **Free for Public Repos**: Unlimited minutes
- **Self-Hosted Runners**: Full control when needed

Key takeaways:
- Use YAML for workflow definitions
- Leverage reusable workflows and actions
- Implement proper secret management
- Use matrix builds for multi-version testing
- Optimize with caching and parallel jobs
- Follow security best practices

For production use:
- Set up environment protection rules
- Use OIDC for cloud provider authentication
- Monitor workflow runs and optimize
- Implement proper error handling
- Use self-hosted runners for sensitive workloads

