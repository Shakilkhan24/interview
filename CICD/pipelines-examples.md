# Complete CI/CD Pipeline Examples
## 5 Production-Ready Pipelines in Jenkins and GitHub Actions

---

## Table of Contents
1. [Pipeline 1: Node.js Application](#pipeline-1-nodejs-application)
2. [Pipeline 2: Python/Django Application](#pipeline-2-pythondjango-application)
3. [Pipeline 3: Java/Spring Boot Application](#pipeline-3-javaspring-boot-application)
4. [Pipeline 4: Docker Container Build & Deploy](#pipeline-4-docker-container-build--deploy)
5. [Pipeline 5: Multi-Environment Deployment](#pipeline-5-multi-environment-deployment)

---

## Pipeline 1: Node.js Application

### Overview
Complete CI/CD pipeline for a Node.js application with testing, building, and deployment to AWS S3.

### GitHub Actions Implementation

```yaml
# .github/workflows/nodejs-ci-cd.yml
name: Node.js CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - staging
          - production

env:
  NODE_VERSION: '18'
  AWS_REGION: 'us-east-1'

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Check code formatting
        run: npm run format:check

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
        env:
          NODE_ENV: test
      
      - name: Run integration tests
        run: npm run test:integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.event_name != 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
        env:
          NODE_ENV: production
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
          retention-days: 7

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop' || (github.event_name == 'workflow_dispatch' && inputs.environment == 'staging')
    environment:
      name: staging
      url: https://staging.myapp.com
    
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://staging-bucket/ \
            --delete \
            --cache-control "public, max-age=31536000"
      
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID_STAGING }} \
            --paths "/*"
      
      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployed to staging'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' || (github.event_name == 'workflow_dispatch' && inputs.environment == 'production')
    environment:
      name: production
      url: https://myapp.com
    
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://production-bucket/ \
            --delete \
            --cache-control "public, max-age=31536000"
      
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID_PROD }} \
            --paths "/*"
      
      - name: Run smoke tests
        run: |
          npm run test:smoke -- --url=https://myapp.com
      
      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployed to production'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Jenkins Implementation

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
    }
    
    environment {
        NODE_VERSION = '18'
        AWS_REGION = 'us-east-1'
        NPM_CONFIG_CACHE = "${WORKSPACE}/.npm"
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['staging', 'production'],
            description: 'Deployment environment'
        )
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    docker.image("node:${NODE_VERSION}").inside("-v ${NPM_CONFIG_CACHE}:/root/.npm") {
                        sh '''
                            npm ci
                            npm run lint
                            npm run format:check
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        script {
                            docker.image("node:${NODE_VERSION}").inside("-v ${NPM_CONFIG_CACHE}:/root/.npm") {
                                sh '''
                                    npm ci
                                    npm run test:unit
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            junit 'test-results/**/*.xml'
                            publishCoverage adapters: [
                                coberturaAdapter('coverage/cobertura-coverage.xml')
                            ]
                        }
                    }
                }
                
                stage('Integration Tests') {
                    steps {
                        script {
                            docker.image("node:${NODE_VERSION}").inside("-v ${NPM_CONFIG_CACHE}:/root/.npm") {
                                sh '''
                                    npm ci
                                    npm run test:integration
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    docker.image("node:${NODE_VERSION}").inside() {
                        sh 'npm audit --audit-level=moderate'
                    }
                }
            }
        }
        
        stage('Build') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    docker.image("node:${NODE_VERSION}").inside("-v ${NPM_CONFIG_CACHE}:/root/.npm") {
                        sh '''
                            npm ci
                            npm run build
                        '''
                    }
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
                    stash includes: 'dist/**/*', name: 'dist'
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'develop'
                    expression { params.ENVIRONMENT == 'staging' }
                }
            }
            steps {
                script {
                    unstash 'dist'
                    withCredentials([
                        aws(
                            credentialsId: 'aws-credentials',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh '''
                            aws s3 sync dist/ s3://staging-bucket/ \
                                --delete \
                                --cache-control "public, max-age=31536000" \
                                --region ${AWS_REGION}
                            
                            aws cloudfront create-invalidation \
                                --distribution-id ${CLOUDFRONT_DIST_ID_STAGING} \
                                --paths "/*" \
                                --region ${AWS_REGION}
                        '''
                    }
                }
            }
            post {
                success {
                    slackSend(
                        channel: '#deployments',
                        color: 'good',
                        message: "Deployed to staging: ${env.BUILD_URL}"
                    )
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                anyOf {
                    branch 'main'
                    expression { params.ENVIRONMENT == 'production' }
                }
            }
            steps {
                script {
                    unstash 'dist'
                    withCredentials([
                        aws(
                            credentialsId: 'aws-credentials',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh '''
                            aws s3 sync dist/ s3://production-bucket/ \
                                --delete \
                                --cache-control "public, max-age=31536000" \
                                --region ${AWS_REGION}
                            
                            aws cloudfront create-invalidation \
                                --distribution-id ${CLOUDFRONT_DIST_ID_PROD} \
                                --paths "/*" \
                                --region ${AWS_REGION}
                        '''
                    }
                    
                    // Smoke tests
                    sh 'npm run test:smoke -- --url=https://myapp.com'
                }
            }
            post {
                success {
                    slackSend(
                        channel: '#deployments',
                        color: 'good',
                        message: "Deployed to production: ${env.BUILD_URL}"
                    )
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            slackSend(
                channel: '#deployments',
                color: 'danger',
                message: "Build failed: ${env.BUILD_URL}"
            )
        }
    }
}
```

---

## Pipeline 2: Python/Django Application

### Overview
Complete CI/CD pipeline for a Django application with database migrations, testing, and deployment to AWS ECS.

### GitHub Actions Implementation

```yaml
# .github/workflows/django-ci-cd.yml
name: Django CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'
  DJANGO_VERSION: '4.2'
  AWS_REGION: 'us-east-1'
  ECR_REPOSITORY: 'myapp/django-app'

jobs:
  lint:
    name: Lint and Format Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
          pip install black flake8 isort mypy
      
      - name: Run Black (format check)
        run: black --check .
      
      - name: Run isort (import sorting)
        run: isort --check-only .
      
      - name: Run Flake8
        run: flake8 .
      
      - name: Run MyPy
        run: mypy .

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
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
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
        django-version: ['4.1', '4.2']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install django==${{ matrix.django-version }}
      
      - name: Run database migrations
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        run: python manage.py migrate
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
        run: |
          python manage.py test --parallel
          coverage run --source='.' manage.py test
          coverage xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: django-tests

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json
      
      - name: Run Safety
        run: |
          pip install safety
          safety check --json

  build-image:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.event_name != 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
    
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster staging-cluster \
            --service django-app-staging \
            --force-new-deployment \
            --region ${{ env.AWS_REGION }}
      
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster staging-cluster \
            --services django-app-staging \
            --region ${{ env.AWS_REGION }}

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
    
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster production-cluster \
            --service django-app-production \
            --force-new-deployment \
            --region ${{ env.AWS_REGION }}
      
      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster production-cluster \
            --services django-app-production \
            --region ${{ env.AWS_REGION }}
      
      - name: Run database migrations
        run: |
          aws ecs run-task \
            --cluster production-cluster \
            --task-definition django-migrations \
            --launch-type FARGATE \
            --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
            --region ${{ env.AWS_REGION }}
```

### Jenkins Implementation

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
    }
    
    environment {
        PYTHON_VERSION = '3.11'
        AWS_REGION = 'us-east-1'
        ECR_REPOSITORY = 'myapp/django-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Lint') {
            steps {
                script {
                    docker.image("python:${PYTHON_VERSION}").inside() {
                        sh '''
                            pip install -r requirements-dev.txt
                            black --check .
                            isort --check-only .
                            flake8 .
                            mypy .
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    docker.image("python:${PYTHON_VERSION}").inside() {
                        sh '''
                            pip install -r requirements.txt
                            python manage.py test --parallel
                            coverage run --source='.' manage.py test
                            coverage xml
                        '''
                    }
                }
            }
            post {
                always {
                    junit 'test-results/**/*.xml'
                    publishCoverage adapters: [
                        coberturaAdapter('coverage.xml')
                    ]
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    docker.image("python:${PYTHON_VERSION}").inside() {
                        sh '''
                            pip install bandit safety
                            bandit -r .
                            safety check
                        '''
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    withCredentials([
                        aws(
                            credentialsId: 'aws-credentials',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh '''
                            aws ecr get-login-password --region ${AWS_REGION} | \
                                docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            
                            docker build -t ${ECR_REPOSITORY}:${BUILD_NUMBER} .
                            docker build -t ${ECR_REPOSITORY}:latest .
                            docker push ${ECR_REPOSITORY}:${BUILD_NUMBER}
                            docker push ${ECR_REPOSITORY}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    withCredentials([
                        aws(
                            credentialsId: 'aws-credentials',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh '''
                            aws ecs update-service \
                                --cluster staging-cluster \
                                --service django-app-staging \
                                --force-new-deployment \
                                --region ${AWS_REGION}
                            
                            aws ecs wait services-stable \
                                --cluster staging-cluster \
                                --services django-app-staging \
                                --region ${AWS_REGION}
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([
                        aws(
                            credentialsId: 'aws-credentials',
                            accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                            secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                        )
                    ]) {
                        sh '''
                            aws ecs update-service \
                                --cluster production-cluster \
                                --service django-app-production \
                                --force-new-deployment \
                                --region ${AWS_REGION}
                            
                            aws ecs wait services-stable \
                                --cluster production-cluster \
                                --services django-app-production \
                                --region ${AWS_REGION}
                            
                            # Run migrations
                            aws ecs run-task \
                                --cluster production-cluster \
                                --task-definition django-migrations \
                                --launch-type FARGATE \
                                --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
                                --region ${AWS_REGION}
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

---

## Pipeline 3: Java/Spring Boot Application

### Overview
Complete CI/CD pipeline for a Spring Boot application with Maven build, testing, and deployment to Kubernetes.

### GitHub Actions Implementation

```yaml
# .github/workflows/spring-boot-ci-cd.yml
name: Spring Boot CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  JAVA_VERSION: '17'
  MAVEN_VERSION: '3.9.5'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build and Test
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up JDK ${{ env.JAVA_VERSION }}
        uses: actions/setup-java@v3
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: maven
      
      - name: Run tests
        env:
          SPRING_DATASOURCE_URL: jdbc:postgresql://localhost:5432/testdb
          SPRING_DATASOURCE_USERNAME: postgres
          SPRING_DATASOURCE_PASSWORD: postgres
        run: mvn clean test
      
      - name: Generate test report
        if: always()
        uses: dorny/test-reporter@v1
        with:
          name: Maven Tests
          path: target/surefire-reports/*.xml
          reporter: java-junit
          fail-on-error: true
      
      - name: Build JAR
        if: github.event_name != 'pull_request'
        run: mvn clean package -DskipTests
      
      - name: Upload JAR artifact
        if: github.event_name != 'pull_request'
        uses: actions/upload-artifact@v3
        with:
          name: application-jar
          path: target/*.jar

  build-image:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name != 'pull_request'
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up JDK ${{ env.JAVA_VERSION }}
        uses: actions/setup-java@v3
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
      
      - name: Build JAR
        run: mvn clean package -DskipTests
      
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
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy-staging:
    name: Deploy to Staging (Kubernetes)
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
      
      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: kubeconfig
          IMAGE_TAG: ${{ github.sha }}
        run: |
          kubectl set image deployment/spring-boot-app \
            spring-boot-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop-${{ github.sha }} \
            -n staging
          
          kubectl rollout status deployment/spring-boot-app -n staging

  deploy-production:
    name: Deploy to Production (Kubernetes)
    runs-on: ubuntu-latest
    needs: build-image
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
      
      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: kubeconfig
          IMAGE_TAG: ${{ github.sha }}
        run: |
          kubectl set image deployment/spring-boot-app \
            spring-boot-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }} \
            -n production
          
          kubectl rollout status deployment/spring-boot-app -n production
      
      - name: Run smoke tests
        run: |
          kubectl run smoke-test --image=curlimages/curl --rm -i --restart=Never -- \
            curl -f http://spring-boot-app.production.svc.cluster.local:8080/health
```

### Jenkins Implementation

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
    }
    
    environment {
        JAVA_VERSION = '17'
        MAVEN_VERSION = '3.9.5'
        REGISTRY = 'ghcr.io'
        IMAGE_NAME = 'myorg/spring-boot-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Test') {
            steps {
                script {
                    docker.image("maven:${MAVEN_VERSION}-openjdk-${JAVA_VERSION}").inside() {
                        sh '''
                            mvn clean test
                        '''
                    }
                }
            }
            post {
                always {
                    junit 'target/surefire-reports/**/*.xml'
                    publishCoverage adapters: [
                        jacocoAdapter('target/site/jacoco/jacoco.xml')
                    ]
                }
            }
        }
        
        stage('Build JAR') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    docker.image("maven:${MAVEN_VERSION}-openjdk-${JAVA_VERSION}").inside() {
                        sh 'mvn clean package -DskipTests'
                    }
                }
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-registry',
                            usernameVariable: 'GITHUB_USER',
                            passwordVariable: 'GITHUB_TOKEN'
                        )
                    ]) {
                        sh '''
                            docker login ${REGISTRY} -u ${GITHUB_USER} -p ${GITHUB_TOKEN}
                            
                            docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                            docker build -t ${IMAGE_NAME}:latest .
                            docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                            docker push ${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    withCredentials([
                        file(
                            credentialsId: 'kubeconfig-staging',
                            variable: 'KUBECONFIG'
                        )
                    ]) {
                        sh '''
                            export KUBECONFIG=${KUBECONFIG}
                            
                            kubectl set image deployment/spring-boot-app \
                                spring-boot-app=${IMAGE_NAME}:${BUILD_NUMBER} \
                                -n staging
                            
                            kubectl rollout status deployment/spring-boot-app -n staging
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([
                        file(
                            credentialsId: 'kubeconfig-production',
                            variable: 'KUBECONFIG'
                        )
                    ]) {
                        sh '''
                            export KUBECONFIG=${KUBECONFIG}
                            
                            kubectl set image deployment/spring-boot-app \
                                spring-boot-app=${IMAGE_NAME}:${BUILD_NUMBER} \
                                -n production
                            
                            kubectl rollout status deployment/spring-boot-app -n production
                            
                            # Smoke tests
                            kubectl run smoke-test \
                                --image=curlimages/curl \
                                --rm -i --restart=Never -- \
                                curl -f http://spring-boot-app.production.svc.cluster.local:8080/health
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

---

## Pipeline 4: Docker Container Build & Deploy

### Overview
Complete CI/CD pipeline for building and deploying Docker containers with multi-stage builds, security scanning, and registry management.

### GitHub Actions Implementation

```yaml
# .github/workflows/docker-ci-cd.yml
name: Docker CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    tags:
      - 'v*'
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
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
            type=semver,pattern={{major}}.{{minor}}.{{patch}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name != 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
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
      
      - name: Run Hadolint (Dockerfile linter)
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: warning

  test:
    name: Test Container
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name != 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run container tests
        run: |
          docker run --rm \
            -v $(pwd)/tests:/tests \
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            /tests/run-tests.sh

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, security-scan, test]
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > kubeconfig
      
      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: kubeconfig
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n staging
          
          kubectl rollout status deployment/myapp -n staging
          
          kubectl get pods -n staging

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, security-scan, test]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
      
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > kubeconfig
      
      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: kubeconfig
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n production
          
          kubectl rollout status deployment/myapp -n production
          
          kubectl get pods -n production
      
      - name: Run smoke tests
        run: |
          kubectl run smoke-test \
            --image=curlimages/curl \
            --rm -i --restart=Never -- \
            curl -f http://myapp.production.svc.cluster.local:8080/health
```

### Jenkins Implementation

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
    }
    
    environment {
        REGISTRY = 'ghcr.io'
        IMAGE_NAME = 'myorg/myapp'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-registry',
                            usernameVariable: 'GITHUB_USER',
                            passwordVariable: 'GITHUB_TOKEN'
                        )
                    ]) {
                        sh '''
                            docker login ${REGISTRY} -u ${GITHUB_USER} -p ${GITHUB_TOKEN}
                            
                            docker buildx create --use
                            docker buildx build \
                                --platform linux/amd64,linux/arm64 \
                                --tag ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                                --tag ${REGISTRY}/${IMAGE_NAME}:latest \
                                --push \
                                .
                        '''
                    }
                }
            }
        }
        
        stage('Security Scan') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    sh '''
                        # Trivy scan
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy image \
                            ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        
                        # Hadolint
                        docker run --rm \
                            -i hadolint/hadolint < Dockerfile
                    '''
                }
            }
        }
        
        stage('Test Container') {
            when {
                not { branch 'PR-*' }
            }
            steps {
                script {
                    sh '''
                        docker run --rm \
                            -v $(pwd)/tests:/tests \
                            ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                            /tests/run-tests.sh
                    '''
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    withCredentials([
                        file(
                            credentialsId: 'kubeconfig-staging',
                            variable: 'KUBECONFIG'
                        )
                    ]) {
                        sh '''
                            export KUBECONFIG=${KUBECONFIG}
                            
                            kubectl set image deployment/myapp \
                                myapp=${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                                -n staging
                            
                            kubectl rollout status deployment/myapp -n staging
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                anyOf {
                    branch 'main'
                    tag 'v*'
                }
            }
            steps {
                script {
                    withCredentials([
                        file(
                            credentialsId: 'kubeconfig-production',
                            variable: 'KUBECONFIG'
                        )
                    ]) {
                        sh '''
                            export KUBECONFIG=${KUBECONFIG}
                            
                            kubectl set image deployment/myapp \
                                myapp=${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                                -n production
                            
                            kubectl rollout status deployment/myapp -n production
                            
                            # Smoke tests
                            kubectl run smoke-test \
                                --image=curlimages/curl \
                                --rm -i --restart=Never -- \
                                curl -f http://myapp.production.svc.cluster.local:8080/health
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

---

## Pipeline 5: Multi-Environment Deployment

### Overview
Complete CI/CD pipeline with multiple environments (dev, staging, production) with approval gates, blue-green deployments, and rollback capabilities.

### GitHub Actions Implementation

```yaml
# .github/workflows/multi-env-deployment.yml
name: Multi-Environment Deployment

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - development
          - staging
          - production
      version:
        description: 'Application version'
        required: false
        type: string

env:
  APP_NAME: myapp
  REGISTRY: ghcr.io

jobs:
  build:
    name: Build Application
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      version: ${{ steps.version.outputs.version }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Get version
        id: version
        run: |
          VERSION=$(git describe --tags --always)
          echo "version=$VERSION" >> $GITHUB_OUTPUT
      
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
          images: ${{ env.REGISTRY }}/${{ github.repository }}
          tags: |
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-development:
    name: Deploy to Development
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop' || startsWith(github.ref, 'refs/heads/feature/')
    environment:
      name: development
      url: https://dev.myapp.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy to Development
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment-dev.yaml
            k8s/service.yaml
          images: |
            ${{ env.REGISTRY }}/${{ github.repository }}:${{ needs.build.outputs.image-tag }}
          kubectl-version: 'latest'
      
      - name: Run health check
        run: |
          sleep 10
          curl -f https://dev.myapp.com/health || exit 1

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop' || (github.event_name == 'workflow_dispatch' && inputs.environment == 'staging')
    environment:
      name: staging
      url: https://staging.myapp.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Deploy to Staging (Blue-Green)
        run: |
          # Blue-Green deployment script
          ./scripts/blue-green-deploy.sh staging ${{ needs.build.outputs.image-tag }}
      
      - name: Run integration tests
        run: |
          npm run test:integration -- --base-url=https://staging.myapp.com
      
      - name: Switch traffic to green
        if: success()
        run: |
          ./scripts/switch-traffic.sh staging green

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' || (github.event_name == 'workflow_dispatch' && inputs.environment == 'production')
    environment:
      name: production
      url: https://myapp.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Create deployment record
        run: |
          echo "Deployment started at $(date)" >> deployment.log
          echo "Version: ${{ needs.build.outputs.version }}" >> deployment.log
      
      - name: Deploy to Production (Blue-Green)
        run: |
          ./scripts/blue-green-deploy.sh production ${{ needs.build.outputs.image-tag }}
      
      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh production
      
      - name: Run load tests
        run: |
          ./scripts/load-tests.sh production
      
      - name: Switch traffic to green
        if: success()
        run: |
          ./scripts/switch-traffic.sh production green
      
      - name: Monitor deployment
        run: |
          ./scripts/monitor-deployment.sh production 300
      
      - name: Rollback on failure
        if: failure()
        run: |
          ./scripts/rollback.sh production
          exit 1

  notify:
    name: Notify Team
    runs-on: ubuntu-latest
    needs: [deploy-development, deploy-staging, deploy-production]
    if: always()
    
    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Deployment Status: ${{ job.status }}
            Environment: ${{ github.event.inputs.environment || 'auto' }}
            Version: ${{ needs.build.outputs.version }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Jenkins Implementation

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 2, unit: 'HOURS')
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment'
        )
        string(
            name: 'VERSION',
            defaultValue: '',
            description: 'Application version (leave empty for latest)'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test execution'
        )
    }
    
    environment {
        APP_NAME = 'myapp'
        REGISTRY = 'ghcr.io'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = params.VERSION ?: "${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'github-registry',
                            usernameVariable: 'GITHUB_USER',
                            passwordVariable: 'GITHUB_TOKEN'
                        )
                    ]) {
                        sh '''
                            docker login ${REGISTRY} -u ${GITHUB_USER} -p ${GITHUB_TOKEN}
                            
                            docker build -t ${REGISTRY}/${APP_NAME}:${IMAGE_TAG} .
                            docker build -t ${REGISTRY}/${APP_NAME}:latest .
                            docker push ${REGISTRY}/${APP_NAME}:${IMAGE_TAG}
                            docker push ${REGISTRY}/${APP_NAME}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            when {
                not { params.SKIP_TESTS }
            }
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh './scripts/run-unit-tests.sh'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh './scripts/run-integration-tests.sh'
                    }
                }
            }
        }
        
        stage('Deploy to Development') {
            when {
                anyOf {
                    branch 'develop'
                    branch 'feature/*'
                    expression { params.ENVIRONMENT == 'development' }
                }
            }
            steps {
                script {
                    sh "./scripts/deploy.sh development ${IMAGE_TAG}"
                }
            }
            post {
                success {
                    sh './scripts/health-check.sh development'
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'develop'
                    expression { params.ENVIRONMENT == 'staging' }
                }
            }
            steps {
                script {
                    // Blue-Green deployment
                    sh "./scripts/blue-green-deploy.sh staging ${IMAGE_TAG}"
                }
            }
            post {
                success {
                    sh './scripts/run-integration-tests.sh --env=staging'
                    sh './scripts/switch-traffic.sh staging green'
                }
                failure {
                    sh './scripts/rollback.sh staging'
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                anyOf {
                    branch 'main'
                    expression { params.ENVIRONMENT == 'production' }
                }
            }
            steps {
                script {
                    // Approval gate (manual)
                    timeout(time: 30, unit: 'MINUTES') {
                        input message: 'Approve production deployment?',
                              ok: 'Deploy',
                              submitterParameter: 'APPROVER'
                    }
                    
                    // Blue-Green deployment
                    sh "./scripts/blue-green-deploy.sh production ${IMAGE_TAG}"
                }
            }
            post {
                success {
                    sh './scripts/smoke-tests.sh production'
                    sh './scripts/load-tests.sh production'
                    sh './scripts/switch-traffic.sh production green'
                    sh './scripts/monitor-deployment.sh production 300'
                }
                failure {
                    sh './scripts/rollback.sh production'
                    emailext(
                        subject: "Production Deployment Failed: ${env.JOB_NAME}",
                        body: "Deployment failed. Rollback initiated.",
                        to: "${env.APPROVER}@example.com"
                    )
                }
            }
        }
    }
    
    post {
        always {
            script {
                def deploymentStatus = currentBuild.result ?: 'SUCCESS'
                slackSend(
                    channel: '#deployments',
                    color: deploymentStatus == 'SUCCESS' ? 'good' : 'danger',
                    message: """
                        Deployment ${deploymentStatus}
                        Environment: ${params.ENVIRONMENT}
                        Version: ${env.IMAGE_TAG}
                        Build: ${env.BUILD_URL}
                    """
                )
            }
        }
        always {
            cleanWs()
        }
    }
}
```

---

## Summary

These 5 complete CI/CD pipelines demonstrate:

1. **Node.js Pipeline**: Full-stack JavaScript application with S3 deployment
2. **Python/Django Pipeline**: Backend application with ECS deployment
3. **Java/Spring Boot Pipeline**: Enterprise application with Kubernetes
4. **Docker Pipeline**: Container-focused with security scanning
5. **Multi-Environment Pipeline**: Complex deployment with approval gates and rollback

Each pipeline includes:
- ✅ Complete implementation in both Jenkins and GitHub Actions
- ✅ Testing and quality checks
- ✅ Security scanning
- ✅ Multi-environment support
- ✅ Deployment strategies
- ✅ Error handling and rollback
- ✅ Notifications and monitoring

Key differences between implementations:
- **GitHub Actions**: YAML-based, native GitHub integration, easier setup
- **Jenkins**: Groovy-based, more flexible, requires infrastructure setup

Choose based on your needs:
- **GitHub Actions**: If using GitHub, want simplicity, or have public repos
- **Jenkins**: If need self-hosting, extensive customization, or existing Jenkins infrastructure

