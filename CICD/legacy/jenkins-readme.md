# Jenkins CI/CD - Complete Guide
## End-to-End Concepts and Best Practices

---

## Table of Contents
1. [Introduction to Jenkins](#1-introduction-to-jenkins)
2. [Jenkins Architecture](#2-jenkins-architecture)
3. [Installation and Setup](#3-installation-and-setup)
4. [Core Concepts](#4-core-concepts)
5. [Pipeline Types](#5-pipeline-types)
6. [Jenkinsfile Deep Dive](#6-jenkinsfile-deep-dive)
7. [Advanced Features](#7-advanced-features)
8. [Security and Best Practices](#8-security-and-best-practices)
9. [Troubleshooting](#9-troubleshooting)
10. [Integration with Tools](#10-integration-with-tools)

---

## 1. Introduction to Jenkins

### What is Jenkins?

Jenkins is an open-source automation server that enables developers to build, test, and deploy software continuously. It's a self-contained Java-based program that can be installed on any machine with a Java Runtime Environment.

### Key Features

- **Continuous Integration (CI)**: Automatically build and test code changes
- **Continuous Delivery (CD)**: Automate deployment to various environments
- **Extensible**: 1,800+ plugins available
- **Distributed**: Master-agent architecture for scalability
- **Pipeline as Code**: Define pipelines using Groovy DSL

### Jenkins vs Alternatives

| Feature | Jenkins | GitHub Actions | GitLab CI | CircleCI |
|---------|---------|---------------|-----------|----------|
| Self-hosted | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| Free tier | ✅ Unlimited | ✅ Limited | ✅ Yes | ✅ Limited |
| Plugin ecosystem | ✅ Extensive | ⚠️ Actions | ⚠️ Limited | ⚠️ Limited |
| Learning curve | ⚠️ Steep | ✅ Easy | ✅ Easy | ✅ Easy |

---

## 2. Jenkins Architecture

### Master-Agent Architecture

```
┌─────────────┐
│   Jenkins   │
│   Master    │
│             │
│  - Schedules│
│  - Monitors │
│  - Manages  │
└──────┬──────┘
       │
       ├──────────────┬──────────────┐
       │              │              │
┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
│   Agent 1   │ │  Agent 2  │ │  Agent 3  │
│  (Linux)    │ │  (Windows)│ │  (Docker) │
│             │ │           │ │           │
│  - Executes │ │  - Executes│ │  - Executes│
│  - Reports  │ │  - Reports│ │  - Reports│
└─────────────┘ └───────────┘ └───────────┘
```

### Components

1. **Jenkins Master**
   - Schedules build jobs
   - Dispatches builds to agents
   - Monitors agent status
   - Records and presents build results
   - Can execute builds directly

2. **Jenkins Agent (Node)**
   - Executes build jobs dispatched by master
   - Can run on different OS/platforms
   - Can be dynamically provisioned
   - Reports build status back to master

3. **Workspace**
   - Directory on agent where build runs
   - Contains source code, artifacts
   - Cleaned between builds (optional)

---

## 3. Installation and Setup

### Installation Methods

#### Method 1: Standalone JAR (Recommended for Testing)

```bash
# Download Jenkins
wget https://get.jenkins.io/war-stable/latest/jenkins.war

# Run Jenkins
java -jar jenkins.war --httpPort=8080

# Access at http://localhost:8080
# Initial admin password: Check console output or ~/.jenkins/secrets/initialAdminPassword
```

#### Method 2: Docker

```bash
# Run Jenkins in Docker
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# Get initial password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

#### Method 3: Package Manager (Ubuntu/Debian)

```bash
# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install
sudo apt-get update
sudo apt-get install jenkins

# Start service
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Initial Setup

1. **Unlock Jenkins**
   - Access http://localhost:8080
   - Enter initial admin password
   - Install suggested plugins

2. **Create Admin User**
   - Set username, password, email
   - Configure Jenkins URL

3. **Configure Tools**
   - Go to Manage Jenkins → Global Tool Configuration
   - Configure JDK, Maven, Git, Docker, etc.

### Setting Up Agents

#### Static Agent (SSH)

```bash
# On agent machine, create jenkins user
sudo useradd -m -s /bin/bash jenkins
sudo mkdir -p /home/jenkins/.ssh

# On master, generate SSH key
ssh-keygen -t rsa -b 4096 -C "jenkins@master"

# Copy public key to agent
ssh-copy-id jenkins@agent-ip

# In Jenkins: Manage Jenkins → Manage Nodes → New Node
# Configure: Remote root directory, Launch method: SSH
```

#### Docker Agent (Dynamic)

```yaml
# docker-compose.yml for Docker agent
version: '3'
services:
  jenkins-agent:
    image: jenkins/inbound-agent
    environment:
      - JENKINS_URL=http://jenkins-master:8080
      - JENKINS_SECRET=agent-secret
      - JENKINS_AGENT_NAME=docker-agent
```

#### Kubernetes Agent (Cloud)

```groovy
// In Jenkins: Manage Jenkins → Configure Clouds → Kubernetes
// Configure:
// - Kubernetes URL
// - Credentials (kubeconfig)
// - Jenkins URL
// - Pod template
```

---

## 4. Core Concepts

### Jobs vs Pipelines

**Freestyle Jobs** (Legacy)
- GUI-based configuration
- Simple builds
- Limited flexibility
- Still useful for simple tasks

**Pipelines** (Modern)
- Code-based (Jenkinsfile)
- Version controlled
- Complex workflows
- Recommended for all new projects

### Pipeline Syntax

#### Declarative Pipeline (Recommended)

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'mvn clean package'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'mvn test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh './deploy.sh'
            }
        }
    }
}
```

#### Scripted Pipeline (Advanced)

```groovy
node {
    stage('Build') {
        sh 'mvn clean package'
    }
    
    stage('Test') {
        sh 'mvn test'
    }
    
    stage('Deploy') {
        sh './deploy.sh'
    }
}
```

### Key Concepts

#### Agent

```groovy
agent any                    // Run on any available agent
agent none                   // No agent (use agent in stages)
agent { label 'linux' }      // Run on agent with label
agent { docker 'node:14' }   // Run in Docker container
```

#### Stages

```groovy
stages {
    stage('Build') {
        steps {
            // Build steps
        }
    }
    
    stage('Test') {
        parallel {
            stage('Unit Tests') {
                steps { /* ... */ }
            }
            stage('Integration Tests') {
                steps { /* ... */ }
            }
        }
    }
}
```

#### Steps

```groovy
steps {
    sh 'command'              // Shell command
    echo 'message'            // Print message
    archiveArtifacts '*.jar'  // Archive files
    junit 'test-results.xml'  // Publish test results
}
```

#### Post Actions

```groovy
post {
    always {
        echo 'Always runs'
        cleanWs()  // Clean workspace
    }
    success {
        echo 'Build succeeded'
        mail to: 'team@example.com',
             subject: "Build Success: ${env.JOB_NAME}",
             body: "Build ${env.BUILD_NUMBER} succeeded"
    }
    failure {
        echo 'Build failed'
        // Send notifications
    }
    unstable {
        echo 'Build unstable'
    }
    cleanup {
        echo 'Cleanup'
    }
}
```

---

## 5. Pipeline Types

### Multibranch Pipeline

Automatically discovers and builds branches/PRs:

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
    }
    
    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
    }
}

// Configure in Jenkins:
// New Item → Multibranch Pipeline
// Branch Sources → GitHub
// Scan Multibranch Pipeline Triggers → Periodically if not otherwise run
```

### Pipeline from SCM

Store Jenkinsfile in repository:

```groovy
// In Jenkins: New Item → Pipeline
// Definition: Pipeline script from SCM
// SCM: Git
// Repository URL: https://github.com/user/repo
// Script Path: Jenkinsfile (or path/to/Jenkinsfile)
```

### Shared Libraries

Reusable pipeline code:

```groovy
// vars/buildApp.groovy
def call(Map config) {
    pipeline {
        agent any
        stages {
            stage('Build') {
                steps {
                    sh "${config.buildCommand}"
                }
            }
        }
    }
}

// Jenkinsfile
@Library('my-shared-library') _
buildApp([
    buildCommand: 'mvn clean package'
])
```

---

## 6. Jenkinsfile Deep Dive

### Environment Variables

```groovy
pipeline {
    agent any
    
    environment {
        APP_NAME = 'myapp'
        VERSION = '1.0.0'
        DOCKER_REGISTRY = 'registry.example.com'
        // Credentials
        DOCKER_CRED = credentials('docker-registry-cred')
    }
    
    stages {
        stage('Build') {
            steps {
                sh "echo Building ${APP_NAME} version ${VERSION}"
                sh "docker login -u ${DOCKER_CRED_USR} -p ${DOCKER_CRED_PSW} ${DOCKER_REGISTRY}"
            }
        }
    }
}
```

### Parameters

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Deployment environment'
        )
        string(
            name: 'VERSION',
            defaultValue: 'latest',
            description: 'Application version'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test execution'
        )
    }
    
    stages {
        stage('Deploy') {
            steps {
                sh "./deploy.sh ${params.ENVIRONMENT} ${params.VERSION}"
            }
        }
    }
}
```

### Conditional Execution

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            when {
                not { params.SKIP_TESTS }
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh 'mvn test'
            }
        }
        
        stage('Deploy to Prod') {
            when {
                branch 'main'
                expression { params.ENVIRONMENT == 'prod' }
            }
            steps {
                sh './deploy-prod.sh'
            }
        }
    }
}
```

### Error Handling

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    try {
                        sh 'mvn clean package'
                    } catch (Exception e) {
                        echo "Build failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                retry(3) {
                    sh './deploy.sh'
                }
            }
        }
    }
}
```

### Artifacts and Archives

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                    stash includes: 'target/*.jar', name: 'artifacts'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                unstash 'artifacts'
                sh './deploy.sh'
            }
        }
    }
}
```

---

## 7. Advanced Features

### Parallel Execution

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'mvn test -Dtest=UnitTest'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'mvn test -Dtest=IntegrationTest'
                    }
                }
                stage('E2E Tests') {
                    steps {
                        sh 'npm run test:e2e'
                    }
                }
            }
        }
    }
}
```

### Matrix Builds

```groovy
pipeline {
    agent none
    
    stages {
        stage('Test Matrix') {
            matrix {
                axes {
                    axis {
                        name 'NODE_VERSION'
                        values '14', '16', '18'
                    }
                    axis {
                        name 'OS'
                        values 'linux', 'windows', 'macos'
                    }
                }
                excludes {
                    exclude {
                        axis {
                            name 'OS'
                            values 'windows'
                        }
                        axis {
                            name 'NODE_VERSION'
                            values '14'
                        }
                    }
                }
                agent {
                    label "${OS}"
                }
                stages {
                    stage('Test') {
                        steps {
                            sh "node --version ${NODE_VERSION}"
                        }
                    }
                }
            }
        }
    }
}
```

### Blue Ocean

Modern UI for Jenkins pipelines:

```bash
# Install Blue Ocean plugin
# Manage Jenkins → Manage Plugins → Available
# Search: Blue Ocean → Install

# Access at: http://jenkins:8080/blue
```

Features:
- Visual pipeline editor
- Pipeline visualization
- Branch/PR discovery
- Real-time logs

### Pipeline Templates

```groovy
// templates/java-pipeline.groovy
def call(body) {
    def config = [:]
    body.resolveStrategy = Closure.DELEGATE_FIRST
    body.delegate = config
    body()
    
    pipeline {
        agent any
        stages {
            stage('Checkout') {
                steps {
                    checkout scm
                }
            }
            stage('Build') {
                steps {
                    sh config.buildCommand ?: 'mvn clean package'
                }
            }
            stage('Test') {
                steps {
                    sh config.testCommand ?: 'mvn test'
                }
            }
        }
    }
}

// Jenkinsfile
@Library('templates') _
javaPipeline {
    buildCommand = 'mvn clean package -DskipTests'
    testCommand = 'mvn test'
}
```

---

## 8. Security and Best Practices

### Credentials Management

```groovy
// Store credentials in Jenkins
// Manage Jenkins → Manage Credentials → Add Credentials

// Types:
// - Username/Password
// - SSH Username with private key
// - Secret text
// - Secret file
// - Certificate

// Use in pipeline
pipeline {
    agent any
    
    environment {
        AWS_ACCESS_KEY = credentials('aws-access-key')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('Deploy') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-registry',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                }
            }
        }
    }
}
```

### Security Best Practices

1. **Enable Security**
   ```
   Manage Jenkins → Configure Global Security
   - Enable security
   - Matrix-based or Role-based authorization
   - CSRF Protection enabled
   ```

2. **Use Credentials Plugin**
   - Never hardcode secrets
   - Use credential binding
   - Rotate credentials regularly

3. **Limit Agent Permissions**
   ```groovy
   // Use specific agents
   agent { label 'linux && docker' }
   
   // Limit workspace access
   options {
       skipDefaultCheckout true
   }
   ```

4. **Sanitize Inputs**
   ```groovy
   // Validate parameters
   parameters {
       string(name: 'VERSION', 
              pattern: '^[0-9]+\\.[0-9]+\\.[0-9]+$',
              description: 'Semantic version')
   }
   ```

5. **Use Docker for Isolation**
   ```groovy
   agent {
       docker {
           image 'maven:3.8-openjdk-11'
           args '-v /var/run/docker.sock:/var/run/docker.sock'
       }
   }
   ```

### Pipeline Best Practices

1. **Keep Jenkinsfiles Simple**
   - Move complex logic to shared libraries
   - Use functions for reusable code

2. **Version Control Everything**
   - Store Jenkinsfile in SCM
   - Use versioned shared libraries

3. **Fail Fast**
   ```groovy
   options {
       timeout(time: 1, unit: 'HOURS')
   }
   
   stages {
       stage('Lint') {
           steps {
               sh 'npm run lint'  // Fail early
           }
       }
   }
   ```

4. **Clean Workspace**
   ```groovy
   post {
       always {
           cleanWs()
       }
   }
   ```

5. **Use Declarative Pipeline**
   - More readable
   - Better error handling
   - Easier to maintain

---

## 9. Troubleshooting

### Common Issues

#### Build Fails Immediately

```groovy
// Check agent connectivity
// Manage Jenkins → Manage Nodes → Check agent status

// Check workspace permissions
ls -la $WORKSPACE

// Check disk space
df -h
```

#### Pipeline Syntax Errors

```bash
# Validate Jenkinsfile
curl -X POST -F "jenkinsfile=<Jenkinsfile" \
  http://jenkins:8080/pipeline-model-converter/validate
```

#### Agent Not Available

```groovy
// Check agent labels
// Manage Jenkins → Manage Nodes

// Use fallback
agent {
    label 'linux || docker'
}
```

#### Credentials Not Found

```groovy
// Verify credential ID
// Manage Jenkins → Manage Credentials

// Check credential scope
withCredentials([...]) {
    // Use credentials
}
```

### Debugging Tips

1. **Enable Debug Logging**
   ```
   Manage Jenkins → System Log → Add new log recorder
   Logger: org.jenkinsci.plugins.workflow
   Level: ALL
   ```

2. **Use echo for Debugging**
   ```groovy
   steps {
       echo "Current branch: ${env.BRANCH_NAME}"
       echo "Build number: ${env.BUILD_NUMBER}"
       sh 'env | sort'  // Print all environment variables
   }
   ```

3. **Check Pipeline Steps**
   ```groovy
   steps {
       script {
           def steps = currentBuild.rawBuild.getActions()
           steps.each { println it }
       }
   }
   ```

---

## 10. Integration with Tools

### Docker Integration

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build Image') {
            steps {
                script {
                    def image = docker.build("myapp:${env.BUILD_NUMBER}")
                    image.push()
                }
            }
        }
    }
}
```

### Kubernetes Integration

```groovy
pipeline {
    agent any
    
    stages {
        stage('Deploy to K8s') {
            steps {
                sh '''
                    kubectl set image deployment/myapp \
                      myapp=myapp:${BUILD_NUMBER} \
                      -n production
                '''
            }
        }
    }
}
```

### Terraform Integration

```groovy
pipeline {
    agent any
    
    stages {
        stage('Infrastructure') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                    sh 'terraform plan'
                    sh 'terraform apply -auto-approve'
                }
            }
        }
    }
}
```

### AWS Integration

```groovy
pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        AWS_CREDENTIALS = credentials('aws-credentials')
    }
    
    stages {
        stage('Deploy to S3') {
            steps {
                sh '''
                    aws s3 cp dist/ s3://my-bucket/ \
                      --recursive \
                      --region ${AWS_REGION}
                '''
            }
        }
    }
}
```

### Slack Notifications

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
    
    post {
        success {
            slackSend(
                channel: '#deployments',
                color: 'good',
                message: "Build ${env.BUILD_NUMBER} succeeded"
            )
        }
        failure {
            slackSend(
                channel: '#deployments',
                color: 'danger',
                message: "Build ${env.BUILD_NUMBER} failed"
            )
        }
    }
}
```

---

## Summary

Jenkins is a powerful CI/CD tool that provides:

- **Flexibility**: Extensive plugin ecosystem
- **Scalability**: Master-agent architecture
- **Pipeline as Code**: Version-controlled pipelines
- **Self-hosted**: Full control over infrastructure
- **Mature**: Battle-tested in production

Key takeaways:
- Use Declarative Pipelines for new projects
- Store Jenkinsfiles in SCM
- Use shared libraries for reusable code
- Implement proper security practices
- Monitor and optimize build times
- Use Docker/Kubernetes agents for isolation

For production deployments, consider:
- High availability setup
- Backup strategies
- Monitoring and alerting
- Resource management
- Security hardening

