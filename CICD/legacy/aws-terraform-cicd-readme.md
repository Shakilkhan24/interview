# AWS CI/CD with Terraform - Complete Guide
## Infrastructure as Code and Continuous Deployment on AWS

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [AWS CI/CD Services Overview](#2-aws-cicd-services-overview)
3. [Terraform Basics for AWS](#3-terraform-basics-for-aws)
4. [Setting Up CI/CD Infrastructure](#4-setting-up-cicd-infrastructure)
5. [CodePipeline Integration](#5-codepipeline-integration)
6. [CodeBuild Configuration](#6-codebuild-configuration)
7. [CodeDeploy Strategies](#7-codedeploy-strategies)
8. [ECS Deployment with Terraform](#8-ecs-deployment-with-terraform)
9. [EKS Deployment with Terraform](#9-eks-deployment-with-terraform)
10. [Lambda Deployment](#10-lambda-deployment)
11. [Advanced Patterns](#11-advanced-patterns)
12. [Best Practices](#12-best-practices)

---

## 1. Introduction

### What is AWS CI/CD with Terraform?

Combining AWS native CI/CD services (CodePipeline, CodeBuild, CodeDeploy) with Terraform for Infrastructure as Code enables automated infrastructure provisioning and application deployment.

### Key Benefits

- **Infrastructure as Code**: Version-controlled infrastructure
- **Automated Provisioning**: Terraform manages AWS resources
- **Native AWS Integration**: Seamless integration with AWS services
- **Cost Optimization**: Pay only for what you use
- **Scalability**: Auto-scaling infrastructure

### Architecture Overview

```
┌─────────────┐
│   GitHub     │
│  / GitLab    │
└──────┬───────┘
       │ Push/PR
       ▼
┌─────────────────┐
│  CodePipeline   │
│  (Orchestrator) │
└──────┬──────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│CodeBuild │   │ Terraform│   │CodeDeploy│
│  (Build) │   │  (Provision)│  │ (Deploy) │
└────┬─────┘   └────┬──────┘   └────┬─────┘
     │              │               │
     └──────────────┴───────────────┘
                    ▼
            ┌───────────────┐
            │  AWS Services │
            │  (ECS/EKS/LB) │
            └───────────────┘
```

---

## 2. AWS CI/CD Services Overview

### AWS CodePipeline

**Purpose**: Fully managed continuous delivery service

**Features**:
- Visual workflow editor
- Integration with GitHub, GitLab, Bitbucket
- Parallel and sequential stages
- Manual approval gates
- Artifact management

**Pricing**: First pipeline free, then $1 per active pipeline/month

### AWS CodeBuild

**Purpose**: Fully managed build service

**Features**:
- Supports multiple languages
- Custom build environments
- Caching support
- Parallel builds
- Integration with VPC

**Pricing**: Pay per build minute (varies by instance type)

### AWS CodeDeploy

**Purpose**: Automated deployment service

**Features**:
- Multiple deployment strategies
- Rollback capabilities
- Health checks
- Traffic shifting
- Blue/Green deployments

**Pricing**: Free (only pay for underlying resources)

### Other AWS Services

- **ECS**: Container orchestration
- **EKS**: Kubernetes on AWS
- **Lambda**: Serverless functions
- **S3**: Artifact storage
- **CloudFormation**: Infrastructure templates
- **Systems Manager**: Parameter Store, Secrets Manager

---

## 3. Terraform Basics for AWS

### Provider Configuration

```hcl
# providers.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "cicd/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}
```

### Variables

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}

variable "github_repo" {
  description = "GitHub repository (owner/repo)"
  type        = string
}
```

### Outputs

```hcl
# outputs.tf
output "pipeline_arn" {
  description = "CodePipeline ARN"
  value       = aws_codepipeline.main.arn
}

output "pipeline_name" {
  description = "CodePipeline name"
  value       = aws_codepipeline.main.name
}

output "build_project_name" {
  description = "CodeBuild project name"
  value       = aws_codebuild_project.main.name
}
```

---

## 4. Setting Up CI/CD Infrastructure

### Complete Terraform Module

```hcl
# main.tf
# S3 Bucket for Artifacts
resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.project_name}-artifacts-${var.environment}"

  tags = {
    Name = "${var.project_name}-artifacts-${var.environment}"
  }
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# IAM Role for CodePipeline
resource "aws_iam_role" "codepipeline" {
  name = "${var.project_name}-codepipeline-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "codepipeline" {
  role = aws_iam_role.codepipeline.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject",
          "s3:GetBucketVersioning"
        ]
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "codebuild:BatchGetBuilds",
          "codebuild:StartBuild"
        ]
        Resource = aws_codebuild_project.main.arn
      },
      {
        Effect = "Allow"
        Action = [
          "codedeploy:CreateDeployment",
          "codedeploy:GetApplication",
          "codedeploy:GetApplicationRevision",
          "codedeploy:GetDeployment",
          "codedeploy:GetDeploymentConfig",
          "codedeploy:RegisterApplicationRevision"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeTasks",
          "ecs:ListTasks",
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:PassRole"
        ]
        Resource = [
          aws_iam_role.ecs_task_execution.arn,
          aws_iam_role.ecs_task.arn
        ]
      }
    ]
  })
}

# CodePipeline
resource "aws_codepipeline" "main" {
  name     = "${var.project_name}-pipeline-${var.environment}"
  role_arn = aws_iam_role.codepipeline.arn

  artifact_store {
    location = aws_s3_bucket.artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        ConnectionArn    = aws_codestarconnections_connection.github.arn
        FullRepositoryId = var.github_repo
        BranchName       = var.branch_name
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts   = ["source_output"]
      output_artifacts  = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = aws_codebuild_project.main.name
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      input_artifacts  = ["build_output"]
      version         = "1"

      configuration = {
        ClusterName = aws_ecs_cluster.main.name
        ServiceName = aws_ecs_service.main.name
        FileName    = "imagedefinitions.json"
      }
    }
  }
}

# CodeStar Connection for GitHub
resource "aws_codestarconnections_connection" "github" {
  name          = "${var.project_name}-github-${var.environment}"
  provider_type = "GitHub"
}
```

---

## 5. CodePipeline Integration

### GitHub Integration

```hcl
# GitHub connection using CodeStar
resource "aws_codestarconnections_connection" "github" {
  name          = "${var.project_name}-github"
  provider_type = "GitHub"
}

# Pipeline source stage
stage {
  name = "Source"

  action {
    name             = "GitHub_Source"
    category         = "Source"
    owner            = "AWS"
    provider         = "CodeStarSourceConnection"
    version          = "1"
    output_artifacts = ["source_output"]

    configuration = {
      ConnectionArn    = aws_codestarconnections_connection.github.arn
      FullRepositoryId = var.github_repo
      BranchName       = var.branch_name
    }
  }
}
```

### S3 Source

```hcl
stage {
  name = "Source"

  action {
    name             = "S3_Source"
    category         = "Source"
    owner            = "AWS"
    provider         = "S3"
    version          = "1"
    output_artifacts = ["source_output"]

    configuration = {
      S3Bucket    = "my-source-bucket"
      S3ObjectKey = "source.zip"
      PollForSourceChanges = "true"
    }
  }
}
```

### Manual Approval Gate

```hcl
stage {
  name = "Approval"

  action {
    name     = "ManualApproval"
    category = "Approval"
    owner    = "AWS"
    provider = "Manual"
    version  = "1"

    configuration = {
      CustomData = "Please review and approve for production deployment"
    }
  }
}
```

### Parallel Actions

```hcl
stage {
  name = "Test"

  action {
    name             = "UnitTests"
    category         = "Test"
    owner            = "AWS"
    provider         = "CodeBuild"
    input_artifacts   = ["source_output"]
    output_artifacts  = ["test_output"]
    version          = "1"

    configuration = {
      ProjectName = aws_codebuild_project.unit_tests.name
    }
  }

  action {
    name             = "IntegrationTests"
    category         = "Test"
    owner            = "AWS"
    provider         = "CodeBuild"
    input_artifacts   = ["source_output"]
    output_artifacts  = ["test_output"]
    version          = "1"

    configuration = {
      ProjectName = aws_codebuild_project.integration_tests.name
    }
  }
}
```

---

## 6. CodeBuild Configuration

### Basic CodeBuild Project

```hcl
# IAM Role for CodeBuild
resource "aws_iam_role" "codebuild" {
  name = "${var.project_name}-codebuild-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "codebuild" {
  role = aws_iam_role.codebuild.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      }
    ]
  })
}

# CodeBuild Project
resource "aws_codebuild_project" "main" {
  name          = "${var.project_name}-build-${var.environment}"
  description   = "Build project for ${var.project_name}"
  build_timeout = 60
  service_role  = aws_iam_role.codebuild.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = var.aws_region
    }

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "IMAGE_REPO_NAME"
      value = aws_ecr_repository.main.name
    }

    environment_variable {
      name  = "IMAGE_TAG"
      value = "latest"
    }

    environment_variable {
      name  = "ENVIRONMENT"
      value = var.environment
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "buildspec.yml"
  }

  cache {
    type  = "LOCAL"
    modes = ["LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/${var.project_name}"
      stream_name = var.environment
    }
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
```

### Buildspec Examples

**Node.js Buildspec:**

```yaml
# buildspec.yml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
      - echo Installing dependencies...
      - npm ci

  build:
    commands:
      - echo Build started on `date`
      - echo Running tests...
      - npm run test
      - echo Building application...
      - npm run build
      - echo Building Docker image...
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_REPO_NAME:latest

  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing Docker image...
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
      - docker push $IMAGE_REPO_NAME:latest
      - echo Writing image definitions file...
      - printf '[{"name":"%s","imageUri":"%s"}]' $IMAGE_REPO_NAME $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
```

**Python/Django Buildspec:**

```yaml
# buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt
      - pip install -r requirements-dev.txt

  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - echo Running tests...
      - python manage.py test
      - echo Running migrations check...
      - python manage.py check --deploy

  build:
    commands:
      - echo Building Docker image...
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_REPO_NAME:latest

  post_build:
    commands:
      - echo Pushing Docker image...
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
      - docker push $IMAGE_REPO_NAME:latest
      - echo Writing image definitions file...
      - printf '[{"name":"%s","imageUri":"%s"}]' $IMAGE_REPO_NAME $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG > imagedefinitions.json

artifacts:
  files:
    - imagedefinitions.json
```

**Terraform Buildspec:**

```yaml
# buildspec-terraform.yml
version: 0.2

phases:
  install:
    commands:
      - echo Installing Terraform...
      - wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
      - unzip terraform_1.6.0_linux_amd64.zip
      - mv terraform /usr/local/bin/
      - terraform version

  pre_build:
    commands:
      - echo Initializing Terraform...
      - cd infrastructure
      - terraform init -backend-config="bucket=${TERRAFORM_STATE_BUCKET}" -backend-config="key=${TERRAFORM_STATE_KEY}"

  build:
    commands:
      - echo Running Terraform plan...
      - terraform plan -out=tfplan
      - echo Applying Terraform...
      - terraform apply -auto-approve tfplan

  post_build:
    commands:
      - echo Terraform apply completed
      - echo Exporting outputs...
      - terraform output -json > terraform-outputs.json

artifacts:
  files:
    - terraform-outputs.json
```

---

## 7. CodeDeploy Strategies

### ECS Blue/Green Deployment

```hcl
# CodeDeploy Application
resource "aws_codedeploy_app" "ecs" {
  compute_platform = "ECS"
  name             = "${var.project_name}-${var.environment}"
}

# CodeDeploy Deployment Group
resource "aws_codedeploy_deployment_group" "ecs" {
  app_name              = aws_codedeploy_app.ecs.name
  deployment_group_name = "${var.project_name}-${var.environment}"
  service_role_arn      = aws_iam_role.codedeploy.arn

  ecs_service {
    cluster_name = aws_ecs_cluster.main.name
    service_name = aws_ecs_service.main.name
  }

  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout = "CONTINUE_DEPLOYMENT"
    }

    green_fleet_provisioning_option {
      action = "COPY_AUTO_SCALING_GROUP"
    }

    terminate_blue_instances_on_deployment_success {
      action = "TERMINATE"
      termination_wait_time_in_minutes = 5
    }
  }

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE"]
  }

  load_balancer_info {
    target_group_info {
      name = aws_lb_target_group.blue.name
    }
  }
}
```

### EC2/On-Premises Deployment

```hcl
resource "aws_codedeploy_app" "ec2" {
  compute_platform = "Server"
  name             = "${var.project_name}-${var.environment}"
}

resource "aws_codedeploy_deployment_group" "ec2" {
  app_name              = aws_codedeploy_app.ec2.name
  deployment_group_name = "${var.project_name}-${var.environment}"
  service_role_arn      = aws_iam_role.codedeploy.arn

  ec2_tag_filter {
    key   = "Environment"
    type  = "KEY_AND_VALUE"
    value = var.environment
  }

  deployment_style {
    deployment_option = "WITH_TRAFFIC_CONTROL"
    deployment_type   = "BLUE_GREEN"
  }

  load_balancer_info {
    elb_info {
      name = aws_elb.main.name
    }
  }

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE"]
  }
}
```

---

## 8. ECS Deployment with Terraform

### Complete ECS Setup

```hcl
# ECR Repository
resource "aws_ecr_repository" "main" {
  name                 = var.project_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  lifecycle_policy {
    policy = jsonencode({
      rules = [
        {
          rulePriority = 1
          description  = "Keep last 10 images"
          selection = {
            tagStatus   = "any"
            countType   = "imageCountMoreThan"
            countNumber = 10
          }
          action = {
            type = "expire"
          }
        }
      ]
    })
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = var.environment
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 7
}

# Task Execution Role
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-ecs-task-execution-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task Role
resource "aws_iam_role" "ecs_task" {
  name = "${var.project_name}-ecs-task-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Task Definition
resource "aws_ecs_task_definition" "main" {
  family                   = "${var.project_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities  = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = var.project_name
      image     = "${aws_ecr_repository.main.repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        }
      ]

      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.database_url.arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "main" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups   = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.main.arn
    container_name   = var.project_name
    container_port   = var.container_port
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  tags = {
    Environment = var.environment
  }
}
```

### Application Load Balancer

```hcl
# ALB
resource "aws_lb" "main" {
  name               = "${var.project_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "prod" ? true : false

  tags = {
    Environment = var.environment
  }
}

# Target Group
resource "aws_lb_target_group" "main" {
  name        = "${var.project_name}-${var.environment}"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
  }

  deregistration_delay = 30

  tags = {
    Environment = var.environment
  }
}

# Listener
resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main.arn
  }
}
```

---

## 9. EKS Deployment with Terraform

### EKS Cluster Setup

```hcl
# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  cluster_endpoint_public_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

  eks_managed_node_groups = {
    main = {
      min_size     = 1
      max_size     = 3
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }

  tags = {
    Environment = var.environment
  }
}
```

### Kubernetes Deployment via CodeBuild

```yaml
# buildspec-k8s.yml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
      - echo Building Docker image...
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $IMAGE_REPO_NAME:latest

  build:
    commands:
      - echo Pushing Docker image...
      - docker push $IMAGE_REPO_NAME:$IMAGE_TAG
      - docker push $IMAGE_REPO_NAME:latest

  post_build:
    commands:
      - echo Configuring kubectl...
      - aws eks update-kubeconfig --name ${CLUSTER_NAME} --region $AWS_DEFAULT_REGION
      - echo Updating Kubernetes deployment...
      - kubectl set image deployment/$DEPLOYMENT_NAME $CONTAINER_NAME=$IMAGE_REPO_NAME:$IMAGE_TAG -n $NAMESPACE
      - kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE
      - echo Deployment completed
```

---

## 10. Lambda Deployment

### Lambda Function with Terraform

```hcl
# Lambda Function
resource "aws_lambda_function" "main" {
  filename         = "function.zip"
  function_name    = "${var.project_name}-${var.environment}"
  role            = aws_iam_role.lambda.arn
  handler         = "index.handler"
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 256

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }

  dead_letter_config {
    target_arn = aws_sqs_queue.dlq.arn
  }

  tags = {
    Environment = var.environment
  }
}

# Lambda Alias for Blue/Green
resource "aws_lambda_alias" "main" {
  name             = "${var.project_name}-${var.environment}"
  description      = "Alias for ${var.environment}"
  function_name    = aws_lambda_function.main.function_name
  function_version = "$LATEST"
}

# CodeDeploy for Lambda
resource "aws_codedeploy_app" "lambda" {
  compute_platform = "Lambda"
  name             = "${var.project_name}-lambda-${var.environment}"
}

resource "aws_codedeploy_deployment_group" "lambda" {
  app_name              = aws_codedeploy_app.lambda.name
  deployment_group_name = "${var.project_name}-lambda-${var.environment}"
  service_role_arn      = aws_iam_role.codedeploy.arn

  deployment_config_name = "CodeDeployDefault.LambdaAllAtOnce"

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE"]
  }
}
```

### Lambda Buildspec

```yaml
# buildspec-lambda.yml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt -t .

  build:
    commands:
      - echo Building Lambda package...
      - zip -r function.zip . -x "*.git*" "*.terraform*"

  post_build:
    commands:
      - echo Uploading to S3...
      - aws s3 cp function.zip s3://${ARTIFACT_BUCKET}/lambda/${CODEBUILD_BUILD_NUMBER}/function.zip
      - echo Updating Lambda function...
      - aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --s3-bucket ${ARTIFACT_BUCKET} --s3-key lambda/${CODEBUILD_BUILD_NUMBER}/function.zip

artifacts:
  files:
    - function.zip
```

---

## 11. Advanced Patterns

### Multi-Environment Pipeline

```hcl
# Pipeline with multiple environments
resource "aws_codepipeline" "multi_env" {
  name     = "${var.project_name}-pipeline"
  role_arn = aws_iam_role.codepipeline.arn

  artifact_store {
    location = aws_s3_bucket.artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"
    # ... source action
  }

  stage {
    name = "Build"
    # ... build action
  }

  stage {
    name = "Deploy-Dev"
    action {
      name            = "DeployToDev"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      input_artifacts  = ["build_output"]
      version         = "1"
      configuration = {
        ClusterName = aws_ecs_cluster.dev.name
        ServiceName = aws_ecs_service.dev.name
        FileName    = "imagedefinitions.json"
      }
    }
  }

  stage {
    name = "Approval"
    action {
      name     = "ManualApproval"
      category = "Approval"
      owner    = "AWS"
      provider = "Manual"
      version  = "1"
    }
  }

  stage {
    name = "Deploy-Prod"
    action {
      name            = "DeployToProd"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "ECS"
      input_artifacts  = ["build_output"]
      version         = "1"
      configuration = {
        ClusterName = aws_ecs_cluster.prod.name
        ServiceName = aws_ecs_service.prod.name
        FileName    = "imagedefinitions.json"
      }
    }
  }
}
```

### Terraform in Pipeline

```hcl
# CodeBuild for Terraform
resource "aws_codebuild_project" "terraform" {
  name          = "${var.project_name}-terraform"
  service_role  = aws_iam_role.codebuild.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image       = "hashicorp/terraform:1.6"
    type        = "LINUX_CONTAINER"
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec-terraform.yml"
  }
}

# Add Terraform stage to pipeline
stage {
  name = "Infrastructure"

  action {
    name            = "TerraformApply"
    category        = "Build"
    owner           = "AWS"
    provider        = "CodeBuild"
    input_artifacts  = ["source_output"]
    output_artifacts = ["terraform_output"]
    version         = "1"

    configuration = {
      ProjectName = aws_codebuild_project.terraform.name
    }
  }
}
```

### Notifications

```hcl
# SNS Topic for notifications
resource "aws_sns_topic" "pipeline" {
  name = "${var.project_name}-pipeline-notifications"
}

# CloudWatch Event Rule
resource "aws_cloudwatch_event_rule" "pipeline" {
  name        = "${var.project_name}-pipeline-events"
  description = "Capture pipeline state changes"

  event_pattern = jsonencode({
    source      = ["aws.codepipeline"]
    detail-type = ["CodePipeline Pipeline Execution State Change"]
    detail = {
      pipeline = [aws_codepipeline.main.name]
    }
  })
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.pipeline.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.pipeline.arn
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.pipeline.arn
  protocol  = "email"
  endpoint  = var.notification_email
}
```

---

## 12. Best Practices

### Security

1. **Use IAM Roles, Not Keys**
   ```hcl
   # ✅ Good
   service_role = aws_iam_role.codebuild.arn
   
   # ❌ Bad
   environment_variable {
     name  = "AWS_ACCESS_KEY_ID"
     value = "AKIA..."
   }
   ```

2. **Encrypt Artifacts**
   ```hcl
   resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
     bucket = aws_s3_bucket.artifacts.id
     rule {
       apply_server_side_encryption_by_default {
         sse_algorithm = "AES256"
       }
     }
   }
   ```

3. **Use Secrets Manager**
   ```hcl
   environment_variable {
     name  = "DATABASE_PASSWORD"
     value = aws_secretsmanager_secret_version.db_password.arn
     type  = "SECRETS_MANAGER"
   }
   ```

### Cost Optimization

1. **Use Appropriate Instance Types**
   ```hcl
   compute_type = "BUILD_GENERAL1_SMALL"  # For small projects
   compute_type = "BUILD_GENERAL1_MEDIUM" # For medium projects
   ```

2. **Enable Caching**
   ```hcl
   cache {
     type  = "LOCAL"
     modes = ["LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
   }
   ```

3. **Set Timeouts**
   ```hcl
   build_timeout = 60  # Minutes
   ```

### Reliability

1. **Enable Auto-Rollback**
   ```hcl
   auto_rollback_configuration {
     enabled = true
     events  = ["DEPLOYMENT_FAILURE"]
   }
   ```

2. **Health Checks**
   ```hcl
   health_check {
     command     = ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
     interval    = 30
     timeout     = 5
     retries     = 3
   }
   ```

3. **Circuit Breakers**
   ```hcl
   deployment_circuit_breaker {
     enable   = true
     rollback = true
   }
   ```

### Monitoring

1. **CloudWatch Logs**
   ```hcl
   logs_config {
     cloudwatch_logs {
       group_name  = "/aws/codebuild/${var.project_name}"
       stream_name = var.environment
     }
   }
   ```

2. **CloudWatch Metrics**
   - Pipeline execution metrics
   - Build duration metrics
   - Deployment success/failure rates

3. **Alarms**
   ```hcl
   resource "aws_cloudwatch_metric_alarm" "pipeline_failures" {
     alarm_name          = "${var.project_name}-pipeline-failures"
     comparison_operator = "GreaterThanThreshold"
     evaluation_periods  = "1"
     metric_name         = "FailedExecutions"
     namespace           = "AWS/CodePipeline"
     period              = "300"
     statistic           = "Sum"
     threshold           = "1"
     alarm_description   = "This metric monitors pipeline failures"
   }
   ```

---

## Summary

AWS CI/CD with Terraform provides:

- **Infrastructure as Code**: Version-controlled infrastructure
- **Automated Pipelines**: End-to-end automation
- **Native Integration**: Seamless AWS service integration
- **Scalability**: Auto-scaling infrastructure
- **Cost-Effective**: Pay only for what you use

Key takeaways:
- Use Terraform for infrastructure provisioning
- Leverage CodePipeline for orchestration
- Use CodeBuild for building and testing
- Implement CodeDeploy for deployment strategies
- Follow security best practices
- Monitor and optimize costs
- Enable auto-rollback and health checks

For production deployments:
- Use separate environments (dev, staging, prod)
- Implement approval gates
- Enable monitoring and alerting
- Use blue/green deployments
- Implement proper IAM roles and policies
- Encrypt artifacts and secrets

