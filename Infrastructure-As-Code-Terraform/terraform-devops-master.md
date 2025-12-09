# Infrastructure as Code with Terraform - Master Guide
## Complete Terraform Tutorial for DevOps Engineers

---

## Table of Contents

1. [Infrastructure as Code Fundamentals](#1-infrastructure-as-code-fundamentals)
2. [Terraform Installation & Setup](#2-terraform-installation--setup)
3. [Terraform Basics](#3-terraform-basics)
4. [Terraform Configuration Language (HCL)](#4-terraform-configuration-language-hcl)
5. [Providers & Resources](#5-providers--resources)
6. [Variables & Outputs](#6-variables--outputs)
7. [State Management](#7-state-management)
8. [Modules](#8-modules)
9. [Workspaces](#9-workspaces)
10. [Remote Backends](#10-remote-backends)
11. [AWS with Terraform](#11-aws-with-terraform)
12. [Multi-Cloud & Provider Configuration](#12-multi-cloud--provider-configuration)
13. [Advanced Terraform Patterns](#13-advanced-terraform-patterns)
14. [Terraform Cloud & Enterprise](#14-terraform-cloud--enterprise)
15. [Best Practices & Troubleshooting](#15-best-practices--troubleshooting)

---

## 1. Infrastructure as Code Fundamentals

### 1.1 What is Infrastructure as Code?

**IaC Benefits:**

- **Version Control**: Infrastructure changes tracked in Git
- **Reproducibility**: Same infrastructure every time
- **Automation**: Reduce manual errors
- **Collaboration**: Team members can review and contribute
- **Documentation**: Code is self-documenting
- **Disaster Recovery**: Infrastructure can be recreated quickly

**IaC Tools Comparison:**

| Tool | Language | State Management | Cloud Support |
|------|----------|------------------|---------------|
| Terraform | HCL/JSON | State file | All major clouds |
| Ansible | YAML | None (agentless) | All major clouds |
| CloudFormation | YAML/JSON | Managed by AWS | AWS only |
| Pulumi | Python/TypeScript/Go | State file | All major clouds |
| CDK | Python/TypeScript/Java | CloudFormation | AWS, Azure, GCP |

### 1.2 Terraform Overview

**How Terraform Works:**

```
┌─────────────────┐
│  Terraform Code │  (HCL files)
│  (main.tf)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   terraform     │
│     plan        │  (What will change?)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  terraform      │
│    apply        │  (Apply changes)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  State File     │  (Current infrastructure state)
│  (terraform.tfstate) │
└─────────────────┘
```

**Terraform Workflow:**

1. **Write** - Define infrastructure in HCL
2. **Initialize** - `terraform init` (download providers)
3. **Plan** - `terraform plan` (preview changes)
4. **Apply** - `terraform apply` (create/update infrastructure)
5. **Destroy** - `terraform destroy` (remove infrastructure)

---

## 2. Terraform Installation & Setup

### 2.1 Installation

**Linux (Manual):**

```bash
# Download Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip

# Unzip
unzip terraform_1.6.0_linux_amd64.zip

# Move to PATH
sudo mv terraform /usr/local/bin/

# Verify
terraform version
```

**Linux (Package Manager):**

```bash
# Ubuntu/Debian
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# RHEL/CentOS
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install terraform
```

**macOS:**

```bash
# Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Or manual download
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_darwin_amd64.zip
unzip terraform_1.6.0_darwin_amd64.zip
sudo mv terraform /usr/local/bin/
```

**Windows:**

```powershell
# Chocolatey
choco install terraform

# Or download from:
# https://releases.hashicorp.com/terraform/
```

### 2.2 IDE Setup

**VS Code Extensions:**

```bash
# Install HashiCorp Terraform extension
code --install-extension hashicorp.terraform

# Install Terraform autocomplete
terraform -install-autocomplete
```

**Configuration:**

```bash
# Create .terraformrc in home directory
cat > ~/.terraformrc << EOF
plugin_cache_dir = "$HOME/.terraform.d/plugin-cache"
EOF
```

---

## 3. Terraform Basics

### 3.1 First Terraform Configuration

**Simple Example:**

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "HelloWorld"
  }
}
```

**Basic Commands:**

```bash
# Initialize Terraform
terraform init

# Format code
terraform fmt

# Validate configuration
terraform validate

# Plan (preview changes)
terraform plan

# Apply (create infrastructure)
terraform apply

# Apply with auto-approve
terraform apply -auto-approve

# Show current state
terraform show

# Destroy infrastructure
terraform destroy
```

### 3.2 Directory Structure

```
project/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── terraform.tfvars     # Variable values
├── terraform.tfstate    # State file (gitignored)
├── terraform.tfstate.backup
├── .terraform/          # Provider plugins (gitignored)
└── .terraform.lock.hcl  # Dependency lock file
```

### 3.3 Terraform State

**State File Purpose:**

- Maps real-world resources to configuration
- Tracks resource metadata
- Stores resource dependencies
- Enables Terraform to update/delete resources

**State Commands:**

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.web

# Move resource (rename in state)
terraform state mv aws_instance.web aws_instance.webserver

# Remove resource from state (doesn't delete resource)
terraform state rm aws_instance.web

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

---

## 4. Terraform Configuration Language (HCL)

### 4.1 HCL Syntax

**Blocks:**

```hcl
# Resource block
resource "resource_type" "resource_name" {
  # Configuration
}

# Data source block
data "data_source_type" "data_name" {
  # Query parameters
}

# Variable block
variable "variable_name" {
  # Variable definition
}

# Output block
output "output_name" {
  # Output definition
}
```

**Arguments:**

```hcl
# Simple key-value
instance_type = "t3.micro"

# String interpolation
name = "server-${var.environment}"

# Multi-line string
user_data = <<-EOF
  #!/bin/bash
  echo "Hello World"
EOF

# Lists
security_groups = ["sg-123", "sg-456"]

# Maps
tags = {
  Name        = "MyServer"
  Environment = "Production"
}
```

**Comments:**

```hcl
# Single-line comment

/*
  Multi-line
  comment
*/

# Inline comment
instance_type = "t3.micro" # Small instance
```

### 4.2 Expressions

**Interpolation:**

```hcl
# Variables
name = "server-${var.environment}"

# Resource attributes
subnet_id = aws_subnet.main.id

# Functions
name = upper("hello")  # "HELLO"

# Conditionals
instance_count = var.environment == "prod" ? 3 : 1
```

**Functions:**

```hcl
# String functions
name = join("-", ["app", "web", "prod"])        # "app-web-prod"
name = split("-", "app-web-prod")                # ["app", "web", "prod"]
name = upper("hello")                            # "HELLO"
name = lower("HELLO")                            # "hello"
name = replace("hello", "l", "L")                # "heLLo"

# Numeric functions
count = max(1, 2, 3)                             # 3
count = min(1, 2, 3)                             # 1
count = abs(-5)                                  # 5

# Collection functions
items = concat(list1, list2)                     # Combine lists
value = contains(list, "item")                   # true/false
value = length(list)                             # Count items
value = element(list, 0)                         # Get element

# File functions
content = file("${path.module}/script.sh")
content = fileexists("${path.module}/file.txt")
content = templatefile("${path.module}/template.tpl", {name = "value"})
```

**Conditionals:**

```hcl
# Ternary operator
instance_count = var.environment == "prod" ? 3 : 1

# Conditional value
enable_feature = var.environment == "prod" ? true : false

# If-else logic
resource "aws_instance" "web" {
  count = var.create_instance ? 1 : 0
  # ...
}
```

---

## 5. Providers & Resources

### 5.1 Providers

**Provider Configuration:**

```hcl
# AWS Provider
provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "~/.aws/credentials"
  profile                 = "default"
  
  default_tags {
    tags = {
      Environment = "production"
      ManagedBy   = "Terraform"
    }
  }
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

# Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Multiple provider instances
provider "aws" {
  alias  = "us-east"
  region = "us-east-1"
}

provider "aws" {
  alias  = "us-west"
  region = "us-west-2"
}

# Use provider alias
resource "aws_instance" "web" {
  provider = aws.us-east
  # ...
}
```

**Provider Version Constraints:**

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"        # >= 5.0, < 6.0
      # version = ">= 4.0, < 6.0"
      # version = "= 5.0.0"
      # version = ">= 5.0"
    }
  }
}
```

### 5.2 Resources

**Resource Syntax:**

```hcl
resource "resource_type" "local_name" {
  # Required arguments
  argument1 = "value1"
  argument2 = "value2"
  
  # Optional arguments
  argument3 = "value3"
  
  # Nested blocks
  nested_block {
    nested_arg = "value"
  }
  
  # Meta-arguments
  count      = 3
  for_each   = var.items
  depends_on = [aws_vpc.main]
  provider   = aws.us-east
  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = [tags]
  }
}
```

**Resource Dependencies:**

```hcl
# Implicit dependency (by reference)
resource "aws_instance" "web" {
  subnet_id = aws_subnet.main.id  # Implicit dependency
}

# Explicit dependency
resource "aws_instance" "web" {
  depends_on = [aws_security_group.web]
}

# Multiple dependencies
resource "aws_instance" "web" {
  depends_on = [
    aws_vpc.main,
    aws_subnet.main,
    aws_security_group.web
  ]
}
```

**Resource Meta-Arguments:**

```hcl
# Count - Create multiple resources
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-123"
  instance_type = "t3.micro"
  tags = {
    Name = "web-${count.index}"
  }
}

# Reference counted resource
subnet_id = aws_subnet.main[0].id
# Or
subnet_id = aws_subnet.main[count.index].id

# for_each - Create resources from map/set
resource "aws_instance" "web" {
  for_each = {
    web1 = "us-east-1a"
    web2 = "us-east-1b"
  }
  ami           = "ami-123"
  instance_type = "t3.micro"
  availability_zone = each.value
  tags = {
    Name = each.key
  }
}

# Reference for_each resource
instance_id = aws_instance.web["web1"].id
```

### 5.3 Data Sources

**Data Source Syntax:**

```hcl
# Fetch existing resource
data "aws_ami" "latest_amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Use data source
resource "aws_instance" "web" {
  ami           = data.aws_ami.latest_amazon_linux.id
  instance_type = "t3.micro"
}

# Multiple data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_vpc" "default" {
  default = true
}
```

---

## 6. Variables & Outputs

### 6.1 Variables

**Variable Declaration:**

```hcl
# variables.tf

# Simple variable
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

# Variable with validation
variable "environment" {
  description = "Environment name"
  type        = string
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# List variable
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# Map variable
variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

# Object variable
variable "database" {
  description = "Database configuration"
  type = object({
    engine    = string
    version   = string
    instance_class = string
    allocated_storage = number
  })
  default = {
    engine           = "mysql"
    version          = "8.0"
    instance_class   = "db.t3.micro"
    allocated_storage = 20
  }
}

# Sensitive variable
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Variable with default from environment
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
```

**Variable Files:**

```hcl
# terraform.tfvars
instance_type = "t3.small"
environment   = "production"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

tags = {
  Environment = "production"
  Team        = "DevOps"
}

# terraform.tfvars.dev
instance_type = "t3.micro"
environment   = "development"

# terraform.tfvars.prod
instance_type = "t3.large"
environment   = "production"
```

**Using Variables:**

```bash
# Via command line
terraform apply -var="instance_type=t3.large"
terraform apply -var-file="terraform.tfvars.prod"

# Via environment variables
export TF_VAR_instance_type=t3.large
terraform apply

# Via .auto.tfvars (automatically loaded)
# instance_type.auto.tfvars
instance_type = "t3.medium"
```

**Using Variables in Configuration:**

```hcl
resource "aws_instance" "web" {
  instance_type = var.instance_type
  ami           = var.ami_id
  
  tags = merge(
    var.tags,
    {
      Name = "web-${var.environment}"
    }
  )
  
  count = var.environment == "prod" ? 3 : 1
}
```

### 6.2 Outputs

**Output Declaration:**

```hcl
# outputs.tf

# Simple output
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

# Output with condition
output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web.public_ip
  condition   = var.assign_public_ip
}

# Output from count
output "instance_ids" {
  description = "IDs of the EC2 instances"
  value       = aws_instance.web[*].id
}

# Output from for_each
output "instance_ids_map" {
  description = "Map of instance IDs"
  value = {
    for k, v in aws_instance.web : k => v.id
  }
}

# Sensitive output
output "db_password" {
  description = "Database password"
  value       = aws_db_instance.main.password
  sensitive   = true
}

# Output with dependencies
output "web_url" {
  description = "Web application URL"
  value       = "http://${aws_instance.web.public_ip}"
  depends_on  = [aws_security_group.web]
}

# Output from module
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}
```

**Using Outputs:**

```bash
# View all outputs
terraform output

# View specific output
terraform output instance_id

# Output as JSON
terraform output -json

# Output specific value (for scripts)
terraform output -raw instance_id
```

---

## 7. State Management

### 7.1 Local State

**Default Behavior:**

```bash
# State stored locally
terraform.tfstate          # Current state
terraform.tfstate.backup   # Previous state backup

# View state
terraform show
terraform state list
terraform state show aws_instance.web
```

### 7.2 State Operations

**State Manipulation:**

```bash
# List resources
terraform state list

# Show resource
terraform state show aws_instance.web

# Move resource (rename)
terraform state mv aws_instance.web aws_instance.webserver

# Remove resource from state (doesn't delete)
terraform state rm aws_instance.web

# Pull state (download from remote)
terraform state pull > state.json

# Push state (upload to remote)
terraform state push state.json
```

**State Import:**

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Import with complex ID
terraform import 'aws_instance.web[0]' i-1234567890abcdef0

# Import from file
terraform import -var-file="production.tfvars" aws_instance.web i-1234567890abcdef0
```

### 7.3 State Locking

**Why State Locking?**

- Prevents concurrent modifications
- Avoids state corruption
- Essential for team collaboration

**Remote Backends (covered in section 10) provide state locking automatically**

---

## 8. Modules

### 8.1 Module Basics

**Module Structure:**

```
modules/
└── vpc/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

**Simple Module:**

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = var.vpc_name
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.vpc_name}-public-${count.index + 1}"
    }
  )
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name tag for VPC"
  type        = string
}

variable "public_subnets" {
  description = "List of public subnet CIDRs"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}
```

**Using Modules:**

```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr      = "10.0.0.0/16"
  vpc_name      = "my-vpc"
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  
  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
  }
}

# Use module outputs
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
  # ...
}
```

### 8.2 Module Sources

**Local Modules:**

```hcl
module "vpc" {
  source = "./modules/vpc"
}

module "vpc" {
  source = "../modules/vpc"
}
```

**Git Modules:**

```hcl
# GitHub
module "vpc" {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-vpc.git"
}

# Git with branch
module "vpc" {
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-vpc.git?ref=v5.0.0"
}

# Private Git
module "vpc" {
  source = "git::ssh://git@github.com/company/modules.git//vpc"
}
```

**Terraform Registry:**

```hcl
# Public registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
}
```

**S3/HTTP:**

```hcl
# S3
module "vpc" {
  source = "s3::https://s3.amazonaws.com/bucket/modules/vpc.zip"
}

# HTTP
module "vpc" {
  source = "https://example.com/modules/vpc.zip"
}
```

### 8.3 Module Best Practices

**Module Design:**

1. **Single Responsibility** - One purpose per module
2. **Reusability** - Design for multiple use cases
3. **Documentation** - README.md with examples
4. **Versioning** - Use semantic versioning
5. **Outputs** - Expose all useful values

**Module Versioning:**

```hcl
# Pin to specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
}

# Allow patch updates
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # >= 5.0, < 6.0
}

# Allow minor updates
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0.0"  # >= 5.0.0, < 5.1.0
}
```

---

## 9. Workspaces

### 9.1 Workspace Basics

**Workspace Commands:**

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Select workspace
terraform workspace select dev

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

**Using Workspaces:**

```hcl
# Conditionally set values based on workspace
locals {
  instance_count = terraform.workspace == "prod" ? 3 : 1
  instance_type  = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
}

resource "aws_instance" "web" {
  count         = local.instance_count
  instance_type = local.instance_type
  # ...
}

# Different backends per workspace
terraform {
  backend "s3" {
    bucket = "terraform-state-${terraform.workspace}"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

**Workspace Limitations:**

- Not recommended for completely different infrastructure
- Use separate directories for different environments instead
- Good for same infrastructure with different scales/values

---

## 10. Remote Backends

### 10.1 Backend Configuration

**Local Backend (Default):**

```hcl
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
```

**S3 Backend:**

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Optional
    profile        = "default"
    role_arn       = "arn:aws:iam::123456789012:role/terraform"
  }
}
```

**Azure Backend:**

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```

**GCS Backend:**

```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state"
    prefix = "terraform/state"
  }
}
```

**Remote Backend (Terraform Cloud/Enterprise):**

```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "production"
    }
  }
}
```

### 10.2 Backend Migration

**Migrating State:**

```bash
# Update backend configuration in code
# Then run:
terraform init -migrate-state

# Or manually
terraform init -backend-config="bucket=new-bucket"
```

---

## 11. AWS with Terraform

### 11.1 VPC Configuration

```hcl
# modules/vpc/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-vpc"
    }
  )
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-igw"
    }
  )
}

# Public Subnets
resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}

# Private Subnets
resource "aws_subnet" "private" {
  count = length(var.private_subnets)

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-private-${count.index + 1}"
      Type = "private"
    }
  )
}

# Route Table for Public Subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-public-rt"
    }
  )
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

data "aws_availability_zones" "available" {
  state = "available"
}
```

### 11.2 EC2 Instances

```hcl
# Security Group
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "SSH"
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-web-sg"
    }
  )
}

# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "${var.project_name}-web-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/user-data.sh", {
    environment = var.environment
  }))

  iam_instance_profile {
    name = aws_iam_instance_profile.web.name
  }

  tag_specifications {
    resource_type = "instance"
    tags = merge(
      var.tags,
      {
        Name = "${var.project_name}-web"
      }
    )
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "${var.project_name}-web-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  min_size            = var.min_size
  max_size            = var.max_size
  desired_capacity    = var.desired_capacity

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-web"
    propagate_at_launch = true
  }
}

# Application Load Balancer
resource "aws_lb" "web" {
  name               = "${var.project_name}-web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = var.environment == "prod"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-web-alb"
    }
  )
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

### 11.3 RDS Database

```hcl
# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-db-subnet-group"
    }
  )
}

# Security Group for RDS
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "MySQL"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-rds-sg"
    }
  )
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier             = "${var.project_name}-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.db_instance_class
  allocated_storage      = var.allocated_storage
  storage_type          = "gp3"
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  skip_final_snapshot = var.environment != "prod"
  final_snapshot_identifier = var.environment == "prod" ? "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}" : null

  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery"]

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-db"
    }
  )
}

# RDS Read Replicas (for production)
resource "aws_db_instance" "read_replica" {
  count = var.environment == "prod" ? 2 : 0

  identifier           = "${var.project_name}-db-replica-${count.index + 1}"
  replicate_source_db  = aws_db_instance.main.identifier
  instance_class       = var.db_instance_class
  availability_zone    = data.aws_availability_zones.available.names[count.index]
  publicly_accessible  = false

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-db-replica-${count.index + 1}"
    }
  )
}
```

### 11.4 S3 Buckets

```hcl
# S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = "${var.project_name}-${var.environment}-storage"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-storage"
    }
  )
}

# Versioning
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = var.environment == "prod" ? "Enabled" : "Disabled"
  }
}

# Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle Policy
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "delete-old-versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
  }
}

# Public Access Block
resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

---

## 12. Multi-Cloud & Provider Configuration

### 12.1 Multiple Providers

```hcl
# AWS Provider
provider "aws" {
  region = "us-east-1"
  alias  = "us_east"
}

provider "aws" {
  region = "eu-west-1"
  alias  = "eu_west"
}

# Azure Provider
provider "azurerm" {
  features {}
  alias = "primary"
}

# Google Cloud Provider
provider "google" {
  project = var.gcp_project
  region  = "us-central1"
  alias   = "primary"
}

# Use providers
resource "aws_instance" "web" {
  provider = aws.us_east
  # ...
}

resource "azurerm_resource_group" "main" {
  provider = azurerm.primary
  # ...
}
```

### 12.2 Provider Configuration via Variables

```hcl
# Provider configuration via variables
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  
  # Or use environment variables
  # AWS_ACCESS_KEY_ID
  # AWS_SECRET_ACCESS_KEY
  # AWS_REGION
}

# Credentials file
provider "aws" {
  shared_credentials_file = "~/.aws/credentials"
  profile                 = var.aws_profile
}

# Assume role
provider "aws" {
  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/terraform-role"
  }
}
```

---

## 13. Advanced Terraform Patterns

### 13.1 Locals

```hcl
# locals.tf
locals {
  # Common tags
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CreatedAt   = timestamp()
  }

  # Resource naming
  name_prefix = "${var.project_name}-${var.environment}"

  # Conditional values
  instance_count = var.environment == "prod" ? 3 : 1
  instance_type  = var.environment == "prod" ? "t3.large" : "t3.micro"

  # Computed values
  subnet_cidrs = [
    cidrsubnet(var.vpc_cidr, 8, 1),
    cidrsubnet(var.vpc_cidr, 8, 2),
    cidrsubnet(var.vpc_cidr, 8, 3)
  ]

  # Data transformations
  subnet_map = {
    for idx, subnet in aws_subnet.public : subnet.id => subnet.availability_zone
  }
}

# Use locals
resource "aws_instance" "web" {
  count         = local.instance_count
  instance_type = local.instance_type
  tags          = local.common_tags
}
```

### 13.2 Data Sources

```hcl
# Get current AWS account
data "aws_caller_identity" "current" {}

# Get current region
data "aws_region" "current" {}

# Get AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Get VPC
data "aws_vpc" "default" {
  default = true
}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Get route53 zone
data "aws_route53_zone" "main" {
  name = "example.com"
}
```

### 13.3 Lifecycle Rules

```hcl
resource "aws_instance" "web" {
  # ...
  
  lifecycle {
    # Create new before destroying old
    create_before_destroy = true
    
    # Prevent accidental deletion
    prevent_destroy = false
    
    # Ignore changes to specific attributes
    ignore_changes = [
      tags,
      ami
    ]
    
    # Replace when these change
    replace_triggered_by = [
      aws_launch_template.web.latest_version
    ]
  }
}
```

### 13.4 For Expressions

```hcl
# List transformation
locals {
  instance_names = [for i in range(3) : "web-${i}"]
}

# Map transformation
locals {
  instance_map = {
    for idx, subnet in aws_subnet.public : subnet.id => {
      name = subnet.tags.Name
      cidr = subnet.cidr_block
    }
  }
}

# Conditional for
locals {
  prod_instances = {
    for k, v in var.instances : k => v
    if v.environment == "prod"
  }
}
```

---

## 14. Terraform Cloud & Enterprise

### 14.1 Terraform Cloud Setup

**Configuration:**

```hcl
terraform {
  cloud {
    organization = "my-org"
    
    workspaces {
      name = "production"
      # Or
      tags = ["production", "aws"]
    }
  }
}
```

**Features:**

- Remote state management
- State locking
- Remote execution
- Cost estimation
- Policy as code (Sentinel)
- Team collaboration

### 14.2 Sentinel Policies

```hcl
# Example Sentinel policy
import "tfplan"

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_instance" implies
      rc.change.after.instance_type in ["t3.micro", "t3.small", "t3.medium"]
  }
}
```

---

## 15. Best Practices & Troubleshooting

### 15.1 Best Practices

**Code Organization:**

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   └── rds/
└── shared/
    └── backend.tf
```

**State Management:**

- Use remote backends (S3, GCS, Azure)
- Enable state locking (DynamoDB for S3)
- Enable encryption
- Use separate state per environment
- Regular backups

**Variables:**

- Use descriptive variable names
- Provide defaults when possible
- Use validation rules
- Mark sensitive variables
- Document variables

**Modules:**

- Single responsibility
- Version modules
- Document inputs/outputs
- Use semantic versioning
- Test modules independently

**Security:**

- Never commit secrets
- Use secrets management (Vault, AWS Secrets Manager)
- Use least privilege IAM roles
- Enable audit logging
- Scan for sensitive data

### 15.2 Troubleshooting

**Common Issues:**

```bash
# State locked
Error: Error acquiring the state lock

# Solution: Check for running Terraform processes
# Or force unlock (use with caution)
terraform force-unlock LOCK_ID

# Provider not found
Error: Could not load plugin

# Solution: Reinitialize
terraform init -upgrade

# State mismatch
Error: Resource already exists

# Solution: Import existing resource
terraform import resource_type.name resource_id

# Validation errors
Error: Missing required argument

# Solution: Check required variables
terraform validate
```

**Debugging:**

```bash
# Enable debug logging
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log
terraform apply

# Trace execution
export TF_LOG=TRACE
terraform apply

# Check plan output
terraform plan -out=tfplan
terraform show tfplan
```

**State Issues:**

```bash
# Refresh state
terraform refresh

# List resources
terraform state list

# Show resource
terraform state show aws_instance.web

# Pull state for inspection
terraform state pull > state.json

# Validate state
terraform validate
```

### 15.3 Performance Optimization

**Parallelism:**

```bash
# Limit parallel operations
terraform apply -parallelism=10
```

**Targeted Operations:**

```bash
# Target specific resources
terraform apply -target=aws_instance.web
terraform destroy -target=aws_instance.web
```

**State Filtering:**

```bash
# Use -target to limit scope
terraform plan -target=module.vpc
```

---

## Conclusion

### Key Takeaways:

1. **Infrastructure as Code** enables version control and automation
2. **State Management** is critical for Terraform operations
3. **Modules** promote reusability and maintainability
4. **Remote Backends** enable team collaboration
5. **Best Practices** ensure scalable and maintainable infrastructure
6. **Testing** infrastructure code prevents production issues

### Essential Commands:

```bash
# Basic workflow
terraform init
terraform plan
terraform apply
terraform destroy

# State management
terraform state list
terraform state show
terraform state mv
terraform import

# Workspaces
terraform workspace list
terraform workspace select
terraform workspace new

# Utilities
terraform fmt
terraform validate
terraform output
```

---

*Infrastructure as Code with Terraform - Master Guide*
*Complete Terraform Tutorial for DevOps Engineers*
*Last Updated: 2024*

