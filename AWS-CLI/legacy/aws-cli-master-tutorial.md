# AWS CLI Master Tutorial
## Complete Guide to AWS Command Line Interface

---

## Table of Contents

1. [AWS CLI Installation & Configuration](#1-aws-cli-installation--configuration)
2. [EC2 (Elastic Compute Cloud)](#2-ec2-elastic-compute-cloud)
3. [S3 (Simple Storage Service)](#3-s3-simple-storage-service)
4. [IAM (Identity and Access Management)](#4-iam-identity-and-access-management)
5. [VPC (Virtual Private Cloud)](#5-vpc-virtual-private-cloud)
6. [RDS (Relational Database Service)](#6-rds-relational-database-service)
7. [Lambda](#7-lambda)
8. [CloudFormation](#8-cloudformation)
9. [CloudWatch](#9-cloudwatch)
10. [SNS (Simple Notification Service)](#10-sns-simple-notification-service)
11. [SQS (Simple Queue Service)](#11-sqs-simple-queue-service)
12. [EKS (Elastic Kubernetes Service)](#12-eks-elastic-kubernetes-service)
13. [ECS (Elastic Container Service)](#13-ecs-elastic-container-service)
14. [Route 53](#14-route-53)
15. [ELB (Elastic Load Balancer)](#15-elb-elastic-load-balancer)
16. [Auto Scaling](#16-auto-scaling)
17. [Secrets Manager](#17-secrets-manager)
18. [Systems Manager (SSM)](#18-systems-manager-ssm)
19. [EBS (Elastic Block Store)](#19-ebs-elastic-block-store)
20. [Best Practices & Tips](#20-best-practices--tips)

---

## 1. AWS CLI Installation & Configuration

### 1.1 Installation

**Linux:**
```bash
# Download and install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

**macOS:**
```bash
# Using Homebrew
brew install awscli

# Or download installer
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

**Windows:**
```powershell
# Download MSI installer from
# https://awscli.amazonaws.com/AWSCLIV2.msi
# Run installer

# Or using Chocolatey
choco install awscli
```

### 1.2 Configuration

```bash
# Configure AWS CLI
aws configure

# You'll be prompted for:
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name: us-east-1
# Default output format: json

# View current configuration
aws configure list

# View credentials
cat ~/.aws/credentials

# View config
cat ~/.aws/config

# Set profile
aws configure --profile myprofile

# Use profile
aws s3 ls --profile myprofile

# Set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_DEFAULT_REGION=us-east-1
```

### 1.3 Basic Commands

```bash
# Check AWS CLI version
aws --version

# Get caller identity
aws sts get-caller-identity

# List all regions
aws ec2 describe-regions --query 'Regions[].RegionName' --output text

# Set default region
aws configure set region us-west-2

# Set default output format
aws configure set output json
aws configure set output table
aws configure set output text
```

---

## 2. EC2 (Elastic Compute Cloud)

### 2.1 Instance Management

```bash
# List all instances
aws ec2 describe-instances

# List instances (formatted)
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress]' \
  --output table

# List running instances only
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,PublicIpAddress]' \
  --output table

# Get instance details
aws ec2 describe-instances --instance-ids i-1234567890abcdef0

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --count 1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'

# Start instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Stop instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Reboot instance
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0

# Terminate instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

### 2.2 AMIs (Amazon Machine Images)

```bash
# List AMIs
aws ec2 describe-images --owners self

# List public AMIs
aws ec2 describe-images \
  --filters "Name=name,Values=amzn2-ami-hvm-*" \
  --query 'Images[*].[ImageId,Name,CreationDate]' \
  --output table

# Create AMI from instance
aws ec2 create-image \
  --instance-id i-1234567890abcdef0 \
  --name "my-server-backup-$(date +%Y%m%d)" \
  --description "Backup of my server"

# Copy AMI to another region
aws ec2 copy-image \
  --source-region us-east-1 \
  --source-image-id ami-12345678 \
  --region us-west-2 \
  --name "copied-ami"

# Deregister AMI
aws ec2 deregister-image --image-id ami-12345678
```

### 2.3 Security Groups

```bash
# List security groups
aws ec2 describe-security-groups

# Create security group
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group" \
  --vpc-id vpc-12345678

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Add outbound rule
aws ec2 authorize-security-group-egress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Remove rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Delete security group
aws ec2 delete-security-group --group-id sg-12345678
```

### 2.4 Key Pairs

```bash
# List key pairs
aws ec2 describe-key-pairs

# Create key pair
aws ec2 create-key-pair \
  --key-name my-key-pair \
  --query 'KeyMaterial' \
  --output text > my-key-pair.pem

# Delete key pair
aws ec2 delete-key-pair --key-name my-key-pair
```

### 2.5 Snapshots & Volumes

```bash
# List snapshots
aws ec2 describe-snapshots --owner-ids self

# Create snapshot
aws ec2 create-snapshot \
  --volume-id vol-12345678 \
  --description "My snapshot"

# Copy snapshot
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id snap-12345678 \
  --region us-west-2 \
  --description "Copied snapshot"

# List volumes
aws ec2 describe-volumes

# Create volume
aws ec2 create-volume \
  --size 100 \
  --volume-type gp3 \
  --availability-zone us-east-1a

# Attach volume
aws ec2 attach-volume \
  --volume-id vol-12345678 \
  --instance-id i-1234567890abcdef0 \
  --device /dev/sdf

# Detach volume
aws ec2 detach-volume --volume-id vol-12345678
```

---

## 3. S3 (Simple Storage Service)

### 3.1 Bucket Operations

```bash
# List buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-bucket-name

# Create bucket in specific region
aws s3 mb s3://my-bucket-name --region us-west-2

# Delete bucket (must be empty)
aws s3 rb s3://my-bucket-name

# Delete bucket and contents
aws s3 rb s3://my-bucket-name --force

# List bucket contents
aws s3 ls s3://my-bucket-name

# List with details
aws s3 ls s3://my-bucket-name --recursive --human-readable --summarize
```

### 3.2 File Operations

```bash
# Upload file
aws s3 cp file.txt s3://my-bucket-name/

# Upload directory
aws s3 cp /local/directory s3://my-bucket-name/ --recursive

# Download file
aws s3 cp s3://my-bucket-name/file.txt ./

# Download directory
aws s3 cp s3://my-bucket-name/ /local/directory --recursive

# Sync directory (upload only changes)
aws s3 sync /local/directory s3://my-bucket-name/

# Sync with delete (remove files not in source)
aws s3 sync /local/directory s3://my-bucket-name/ --delete

# Move file
aws s3 mv file.txt s3://my-bucket-name/file.txt

# Remove file
aws s3 rm s3://my-bucket-name/file.txt

# Remove directory
aws s3 rm s3://my-bucket-name/directory/ --recursive
```

### 3.3 Bucket Configuration

```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket-name \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-bucket-name \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Set bucket policy
aws s3api put-bucket-policy \
  --bucket my-bucket-name \
  --policy file://policy.json

# Set CORS configuration
aws s3api put-bucket-cors \
  --bucket my-bucket-name \
  --cors-configuration file://cors.json

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket-name \
  --lifecycle-configuration file://lifecycle.json

# Enable static website hosting
aws s3 website s3://my-bucket-name/ --index-document index.html
```

### 3.4 Presigned URLs

```bash
# Generate presigned URL (valid for 1 hour)
aws s3 presign s3://my-bucket-name/file.txt

# Generate presigned URL with custom expiration
aws s3 presign s3://my-bucket-name/file.txt --expires-in 3600

# Generate presigned URL for upload
aws s3 presign s3://my-bucket-name/file.txt --expires-in 3600
```

### 3.5 S3 Select

```bash
# Query CSV file
aws s3api select-object-content \
  --bucket my-bucket-name \
  --key data.csv \
  --expression "SELECT * FROM S3Object WHERE _1 = 'value'" \
  --expression-type SQL \
  --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
  --output-serialization '{"CSV": {}}' \
  output.csv
```

---

## 4. IAM (Identity and Access Management)

### 4.1 User Management

```bash
# List users
aws iam list-users

# Create user
aws iam create-user --user-name myuser

# Get user details
aws iam get-user --user-name myuser

# Create access key
aws iam create-access-key --user-name myuser

# List access keys
aws iam list-access-keys --user-name myuser

# Delete access key
aws iam delete-access-key --user-name myuser --access-key-id AKIAIOSFODNN7EXAMPLE

# Delete user
aws iam delete-user --user-name myuser
```

### 4.2 Group Management

```bash
# List groups
aws iam list-groups

# Create group
aws iam create-group --group-name mygroup

# Add user to group
aws iam add-user-to-group --user-name myuser --group-name mygroup

# Remove user from group
aws iam remove-user-from-group --user-name myuser --group-name mygroup

# List users in group
aws iam get-group --group-name mygroup

# Delete group
aws iam delete-group --group-name mygroup
```

### 4.3 Role Management

```bash
# List roles
aws iam list-roles

# Create role
aws iam create-role \
  --role-name myrole \
  --assume-role-policy-document file://trust-policy.json

# Attach policy to role
aws iam attach-role-policy \
  --role-name myrole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# List role policies
aws iam list-attached-role-policies --role-name myrole

# Delete role
aws iam delete-role --role-name myrole
```

### 4.4 Policy Management

```bash
# List policies
aws iam list-policies --scope Local

# Create policy
aws iam create-policy \
  --policy-name mypolicy \
  --policy-document file://policy.json

# Attach policy to user
aws iam attach-user-policy \
  --user-name myuser \
  --policy-arn arn:aws:iam::123456789012:policy/mypolicy

# Detach policy from user
aws iam detach-user-policy \
  --user-name myuser \
  --policy-arn arn:aws:iam::123456789012:policy/mypolicy

# Get policy version
aws iam get-policy-version \
  --policy-arn arn:aws:iam::123456789012:policy/mypolicy \
  --version-id v1
```

---

## 5. VPC (Virtual Private Cloud)

### 5.1 VPC Operations

```bash
# List VPCs
aws ec2 describe-vpcs

# Create VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVPC}]'

# Get VPC details
aws ec2 describe-vpcs --vpc-ids vpc-12345678

# Delete VPC
aws ec2 delete-vpc --vpc-id vpc-12345678
```

### 5.2 Subnets

```bash
# List subnets
aws ec2 describe-subnets

# Create subnet
aws ec2 create-subnet \
  --vpc-id vpc-12345678 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

# Modify subnet (enable auto-assign public IP)
aws ec2 modify-subnet-attribute \
  --subnet-id subnet-12345678 \
  --map-public-ip-on-launch

# Delete subnet
aws ec2 delete-subnet --subnet-id subnet-12345678
```

### 5.3 Internet Gateway

```bash
# Create internet gateway
aws ec2 create-internet-gateway

# Attach to VPC
aws ec2 attach-internet-gateway \
  --internet-gateway-id igw-12345678 \
  --vpc-id vpc-12345678

# Detach from VPC
aws ec2 detach-internet-gateway \
  --internet-gateway-id igw-12345678 \
  --vpc-id vpc-12345678

# Delete internet gateway
aws ec2 delete-internet-gateway --internet-gateway-id igw-12345678
```

### 5.4 Route Tables

```bash
# List route tables
aws ec2 describe-route-tables

# Create route table
aws ec2 create-route-table --vpc-id vpc-12345678

# Create route
aws ec2 create-route \
  --route-table-id rtb-12345678 \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-12345678

# Associate route table with subnet
aws ec2 associate-route-table \
  --subnet-id subnet-12345678 \
  --route-table-id rtb-12345678

# Delete route
aws ec2 delete-route \
  --route-table-id rtb-12345678 \
  --destination-cidr-block 0.0.0.0/0
```

### 5.5 Security Groups (VPC)

```bash
# List security groups in VPC
aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=vpc-12345678"

# Create security group in VPC
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group" \
  --vpc-id vpc-12345678
```

---

## 6. RDS (Relational Database Service)

### 6.1 Database Instances

```bash
# List DB instances
aws rds describe-db-instances

# Create DB instance
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password MyPassword123 \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-12345678 \
  --db-subnet-group-name my-db-subnet-group

# Get DB instance details
aws rds describe-db-instances --db-instance-identifier mydb

# Modify DB instance
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --allocated-storage 100 \
  --apply-immediately

# Delete DB instance
aws rds delete-db-instance \
  --db-instance-identifier mydb \
  --skip-final-snapshot
```

### 6.2 Snapshots

```bash
# Create snapshot
aws rds create-db-snapshot \
  --db-snapshot-identifier mydb-snapshot \
  --db-instance-identifier mydb

# List snapshots
aws rds describe-db-snapshots

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier mydb-restored \
  --db-snapshot-identifier mydb-snapshot

# Copy snapshot
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier mydb-snapshot \
  --target-db-snapshot-identifier mydb-snapshot-copy \
  --source-region us-east-1 \
  --region us-west-2
```

### 6.3 Parameter Groups

```bash
# Create parameter group
aws rds create-db-parameter-group \
  --db-parameter-group-name my-param-group \
  --db-parameter-group-family mysql8.0 \
  --description "My parameter group"

# Modify parameter
aws rds modify-db-parameter-group \
  --db-parameter-group-name my-param-group \
  --parameters "ParameterName=max_connections,ParameterValue=100,ApplyMethod=immediate"
```

---

## 7. Lambda

### 7.1 Function Management

```bash
# List functions
aws lambda list-functions

# Create function from zip
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler index.handler \
  --zip-file fileb://function.zip

# Create function from S3
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --handler index.handler \
  --code S3Bucket=my-bucket,S3Key=function.zip

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# Get function details
aws lambda get-function --function-name my-function

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"key":"value"}' \
  response.json

# Delete function
aws lambda delete-function --function-name my-function
```

### 7.2 Function Configuration

```bash
# Update function configuration
aws lambda update-function-configuration \
  --function-name my-function \
  --timeout 300 \
  --memory-size 512 \
  --environment Variables={KEY1=value1,KEY2=value2}

# Add environment variables
aws lambda update-function-configuration \
  --function-name my-function \
  --environment Variables={DATABASE_URL=postgres://...}

# Add layers
aws lambda update-function-configuration \
  --function-name my-function \
  --layers arn:aws:lambda:us-east-1:123456789012:layer:my-layer:1
```

### 7.3 Event Sources

```bash
# Create event source mapping (SQS)
aws lambda create-event-source-mapping \
  --function-name my-function \
  --event-source-arn arn:aws:sqs:us-east-1:123456789012:my-queue \
  --batch-size 10

# List event source mappings
aws lambda list-event-source-mappings --function-name my-function

# Delete event source mapping
aws lambda delete-event-source-mapping --uuid event-source-mapping-id
```

---

## 8. CloudFormation

### 8.1 Stack Operations

```bash
# Create stack
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=InstanceType,ParameterValue=t2.micro

# Create stack from S3
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-url https://s3.amazonaws.com/my-bucket/template.yaml

# Update stack
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml

# Describe stack
aws cloudformation describe-stacks --stack-name my-stack

# List stacks
aws cloudformation list-stacks

# Get stack events
aws cloudformation describe-stack-events --stack-name my-stack

# Delete stack
aws cloudformation delete-stack --stack-name my-stack
```

### 8.2 Stack Resources

```bash
# List stack resources
aws cloudformation describe-stack-resources --stack-name my-stack

# Get resource details
aws cloudformation describe-stack-resource \
  --stack-name my-stack \
  --logical-resource-id MyInstance
```

---

## 9. CloudWatch

### 9.1 Metrics

```bash
# List metrics
aws cloudwatch list-metrics

# List metrics for namespace
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average

# Put custom metric
aws cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name RequestCount \
  --value 100 \
  --unit Count
```

### 9.2 Alarms

```bash
# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --alarm-description "Alarm when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2

# List alarms
aws cloudwatch describe-alarms

# Delete alarm
aws cloudwatch delete-alarms --alarm-names high-cpu
```

### 9.3 Logs

```bash
# List log groups
aws logs describe-log-groups

# Create log group
aws logs create-log-group --log-group-name /aws/lambda/my-function

# Put log events
aws logs put-log-events \
  --log-group-name /aws/lambda/my-function \
  --log-stream-name stream1 \
  --log-events timestamp=1234567890000,message="Log message"

# Get log events
aws logs get-log-events \
  --log-group-name /aws/lambda/my-function \
  --log-stream-name stream1

# Export logs to S3
aws logs create-export-task \
  --log-group-name /aws/lambda/my-function \
  --from 1234567890000 \
  --to 1234567900000 \
  --destination my-bucket \
  --destination-prefix logs/
```

---

## 10. SNS (Simple Notification Service)

### 10.1 Topics

```bash
# Create topic
aws sns create-topic --name my-topic

# List topics
aws sns list-topics

# Get topic attributes
aws sns get-topic-attributes --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic

# Delete topic
aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic
```

### 10.2 Subscriptions

```bash
# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --protocol email \
  --notification-endpoint user@example.com

# Subscribe SQS
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:123456789012:my-queue

# List subscriptions
aws sns list-subscriptions

# Unsubscribe
aws sns unsubscribe --subscription-arn arn:aws:sns:...
```

### 10.3 Publishing

```bash
# Publish message
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --message "Hello from SNS"

# Publish with subject
aws sns publish \
  --topic-arn arn:aws:sns:us-east-1:123456789012:my-topic \
  --subject "Alert" \
  --message "This is an alert message"
```

---

## 11. SQS (Simple Queue Service)

### 11.1 Queue Operations

```bash
# Create queue
aws sqs create-queue --queue-name my-queue

# List queues
aws sqs list-queues

# Get queue URL
aws sqs get-queue-url --queue-name my-queue

# Get queue attributes
aws sqs get-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --attribute-names All

# Set queue attributes
aws sqs set-queue-attributes \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --attributes VisibilityTimeout=60

# Delete queue
aws sqs delete-queue \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue
```

### 11.2 Message Operations

```bash
# Send message
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --message-body "Hello from SQS"

# Send message with attributes
aws sqs send-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --message-body "Message with attributes" \
  --message-attributes '{"Priority":{"StringValue":"High","DataType":"String"}}'

# Receive messages
aws sqs receive-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue

# Delete message
aws sqs delete-message \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue \
  --receipt-handle "AQEBzWwaftRI0KuVm4tP..."

# Purge queue
aws sqs purge-queue \
  --queue-url https://sqs.us-east-1.amazonaws.com/123456789012/my-queue
```

---

## 12. EKS (Elastic Kubernetes Service)

### 12.1 Cluster Management

```bash
# List clusters
aws eks list-clusters

# Describe cluster
aws eks describe-cluster --name my-cluster

# Create cluster
aws eks create-cluster \
  --name my-cluster \
  --role-arn arn:aws:iam::123456789012:role/eks-service-role \
  --resources-vpc-config subnetIds=subnet-123,subnet-456,securityGroupIds=sg-123

# Update cluster
aws eks update-cluster-version \
  --name my-cluster \
  --kubernetes-version 1.28

# Delete cluster
aws eks delete-cluster --name my-cluster
```

### 12.2 Node Groups

```bash
# List node groups
aws eks list-nodegroups --cluster-name my-cluster

# Create node group
aws eks create-nodegroup \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup \
  --node-role arn:aws:iam::123456789012:role/NodeInstanceRole \
  --subnets subnet-123 subnet-456 \
  --instance-types t3.medium \
  --scaling-config minSize=1,maxSize=3,desiredSize=2

# Describe node group
aws eks describe-nodegroup \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup

# Delete node group
aws eks delete-nodegroup \
  --cluster-name my-cluster \
  --nodegroup-name my-nodegroup
```

---

## 13. ECS (Elastic Container Service)

### 13.1 Cluster Management

```bash
# List clusters
aws ecs list-clusters

# Create cluster
aws ecs create-cluster --cluster-name my-cluster

# Describe cluster
aws ecs describe-clusters --clusters my-cluster

# Delete cluster
aws ecs delete-cluster --cluster my-cluster
```

### 13.2 Task Definitions

```bash
# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# List task definitions
aws ecs list-task-definitions

# Describe task definition
aws ecs describe-task-definition --task-definition my-task:1

# Deregister task definition
aws ecs deregister-task-definition --task-definition my-task:1
```

### 13.3 Services

```bash
# Create service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-service \
  --task-definition my-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-123],securityGroups=[sg-123]}"

# List services
aws ecs list-services --cluster my-cluster

# Update service
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --desired-count 3

# Delete service
aws ecs delete-service \
  --cluster my-cluster \
  --service my-service
```

### 13.4 Tasks

```bash
# Run task
aws ecs run-task \
  --cluster my-cluster \
  --task-definition my-task:1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-123],securityGroups=[sg-123]}"

# List tasks
aws ecs list-tasks --cluster my-cluster

# Describe task
aws ecs describe-tasks \
  --cluster my-cluster \
  --tasks task-id

# Stop task
aws ecs stop-task \
  --cluster my-cluster \
  --task task-id
```

---

## 14. Route 53

### 14.1 Hosted Zones

```bash
# List hosted zones
aws route53 list-hosted-zones

# Create hosted zone
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)

# Get hosted zone
aws route53 get-hosted-zone --id Z1234567890ABC

# Delete hosted zone
aws route53 delete-hosted-zone --id Z1234567890ABC
```

### 14.2 Records

```bash
# List resource record sets
aws route53 list-resource-record-sets --hosted-zone-id Z1234567890ABC

# Create record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch file://change-batch.json

# Example change-batch.json:
# {
#   "Changes": [{
#     "Action": "CREATE",
#     "ResourceRecordSet": {
#       "Name": "www.example.com",
#       "Type": "A",
#       "TTL": 300,
#       "ResourceRecords": [{"Value": "192.0.2.1"}]
#     }
#   }]
# }

# Delete record
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "DELETE",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "192.0.2.1"}]
      }
    }]
  }'
```

---

## 15. ELB (Elastic Load Balancer)

### 15.1 Application Load Balancer

```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name my-alb \
  --subnets subnet-123 subnet-456 \
  --security-groups sg-123

# List load balancers
aws elbv2 describe-load-balancers

# Delete load balancer
aws elbv2 delete-load-balancer \
  --load-balancer-arn arn:aws:elasticloadbalancing:...
```

### 15.2 Target Groups

```bash
# Create target group
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-12345678 \
  --health-check-path /health

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-1234567890abcdef0

# List target groups
aws elbv2 describe-target-groups

# Delete target group
aws elbv2 delete-target-group \
  --target-group-arn arn:aws:elasticloadbalancing:...
```

### 15.3 Listeners

```bash
# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...

# List listeners
aws elbv2 describe-listeners \
  --load-balancer-arn arn:aws:elasticloadbalancing:...
```

---

## 16. Auto Scaling

### 16.1 Launch Configurations

```bash
# Create launch configuration
aws autoscaling create-launch-configuration \
  --launch-configuration-name my-launch-config \
  --image-id ami-12345678 \
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-groups sg-12345678

# List launch configurations
aws autoscaling describe-launch-configurations

# Delete launch configuration
aws autoscaling delete-launch-configuration \
  --launch-configuration-name my-launch-config
```

### 16.2 Auto Scaling Groups

```bash
# Create auto scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --launch-configuration-name my-launch-config \
  --min-size 1 \
  --max-size 10 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-123,subnet-456"

# Describe auto scaling group
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names my-asg

# Update auto scaling group
aws autoscaling update-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --min-size 2 \
  --max-size 15 \
  --desired-capacity 5

# Delete auto scaling group
aws autoscaling delete-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --force-delete
```

### 16.3 Scaling Policies

```bash
# Create scaling policy
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-asg \
  --policy-name scale-up \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    }
  }'
```

---

## 17. Secrets Manager

### 17.1 Secret Operations

```bash
# Create secret
aws secretsmanager create-secret \
  --name my-secret \
  --secret-string '{"username":"admin","password":"secret123"}'

# Get secret value
aws secretsmanager get-secret-value --secret-id my-secret

# List secrets
aws secretsmanager list-secrets

# Update secret
aws secretsmanager update-secret \
  --secret-id my-secret \
  --secret-string '{"username":"admin","password":"newpassword"}'

# Rotate secret
aws secretsmanager rotate-secret \
  --secret-id my-secret \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-secret

# Delete secret
aws secretsmanager delete-secret \
  --secret-id my-secret \
  --force-delete-without-recovery
```

---

## 18. Systems Manager (SSM)

### 18.1 Parameter Store

```bash
# Put parameter
aws ssm put-parameter \
  --name /myapp/database/url \
  --value "postgres://localhost/db" \
  --type String

# Get parameter
aws ssm get-parameter \
  --name /myapp/database/url \
  --with-decryption

# List parameters
aws ssm describe-parameters

# Delete parameter
aws ssm delete-parameter --name /myapp/database/url
```

### 18.2 Run Command

```bash
# Send command to instance
aws ssm send-command \
  --instance-ids i-1234567890abcdef0 \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["echo Hello World"]'

# List commands
aws ssm list-commands

# Get command output
aws ssm get-command-invocation \
  --command-id command-id \
  --instance-id i-1234567890abcdef0
```

---

## 19. EBS (Elastic Block Store)

### 19.1 Volume Operations

```bash
# List volumes
aws ec2 describe-volumes

# Create volume
aws ec2 create-volume \
  --size 100 \
  --volume-type gp3 \
  --availability-zone us-east-1a \
  --encrypted

# Modify volume
aws ec2 modify-volume \
  --volume-id vol-12345678 \
  --size 200

# Create snapshot
aws ec2 create-snapshot \
  --volume-id vol-12345678 \
  --description "Backup snapshot"

# Restore volume from snapshot
aws ec2 create-volume \
  --snapshot-id snap-12345678 \
  --availability-zone us-east-1a
```

---

## 20. Best Practices & Tips

### 20.1 Output Formatting

```bash
# JSON (default)
aws ec2 describe-instances --output json

# Table (human-readable)
aws ec2 describe-instances --output table

# Text (script-friendly)
aws ec2 describe-instances --output text

# YAML
aws ec2 describe-instances --output yaml
```

### 20.2 Query Filtering

```bash
# Use --query for filtering
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]' \
  --output table

# Filter with --filters
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
            "Name=instance-type,Values=t2.micro"
```

### 20.3 Pagination

```bash
# Use --max-items and --page-size
aws s3 ls --max-items 10

# Use --starting-token for pagination
aws s3 ls --starting-token "token-value"
```

### 20.4 Profiles

```bash
# Use multiple profiles
aws configure --profile dev
aws configure --profile prod

# Use profile
aws s3 ls --profile dev

# Set default profile
export AWS_PROFILE=dev
```

### 20.5 Error Handling

```bash
# Check exit codes
aws s3 ls s3://non-existent-bucket
echo $?  # Will be non-zero on error

# Use --no-cli-pager for scripts
aws ec2 describe-instances --no-cli-pager
```

### 20.6 Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias aws-instances='aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,PublicIpAddress]" --output table'
alias aws-buckets='aws s3 ls'
alias aws-regions='aws ec2 describe-regions --query "Regions[].RegionName" --output text'
```

---

## Quick Reference

### Most Used Commands

```bash
# EC2
aws ec2 describe-instances
aws ec2 run-instances
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx

# S3
aws s3 ls
aws s3 cp file.txt s3://bucket/
aws s3 sync ./dir s3://bucket/

# IAM
aws iam list-users
aws iam create-user --user-name xxx
aws iam attach-user-policy --user-name xxx --policy-arn xxx

# Lambda
aws lambda list-functions
aws lambda invoke --function-name xxx

# CloudWatch
aws cloudwatch get-metric-statistics
aws cloudwatch put-metric-alarm

# EKS
aws eks list-clusters
aws eks describe-cluster --name xxx
```

---

## Conclusion

This tutorial covers the most important AWS services and their key operations. Practice these commands to become proficient with AWS CLI!

**Key Takeaways:**
- ✅ Use `--output table` for human-readable output
- ✅ Use `--query` for filtering results
- ✅ Use `--profile` for multiple AWS accounts
- ✅ Always use `--region` when working across regions
- ✅ Use `--dry-run` when available to test operations
- ✅ Combine commands with pipes for complex operations

Master AWS CLI to automate and manage your cloud infrastructure efficiently! 🚀

