# Python for DevOps - Complete Tutorial
## Automation, Infrastructure, and Cloud Operations with Python

---

## Table of Contents

1. [Introduction to Python for DevOps](#1-introduction-to-python-for-devops)
2. [Python Basics for DevOps](#2-python-basics-for-devops)
3. [Working with APIs](#3-working-with-apis)
4. [AWS SDK (Boto3)](#4-aws-sdk-boto3)
5. [Infrastructure as Code with Python](#5-infrastructure-as-code-with-python)
6. [Docker Operations](#6-docker-operations)
7. [Kubernetes Operations](#7-kubernetes-operations)
8. [Configuration Management](#8-configuration-management)
9. [Monitoring and Logging](#9-monitoring-and-logging)
10. [CI/CD Automation](#10-cicd-automation)
11. [Database Operations](#11-database-operations)
12. [File and Data Processing](#12-file-and-data-processing)
13. [Network Operations](#13-network-operations)
14. [Security Automation](#14-security-automation)
15. [Error Handling and Best Practices](#15-error-handling-and-best-practices)

---

## 1. Introduction to Python for DevOps

### Why Python for DevOps?

Python is widely used in DevOps because:
- **Simple Syntax**: Easy to read and write
- **Rich Ecosystem**: Extensive libraries for automation
- **Cross-Platform**: Works on Linux, Windows, macOS
- **Cloud SDKs**: Native support for AWS, Azure, GCP
- **Integration**: Easy integration with tools and APIs
- **Rapid Development**: Quick to prototype and deploy

### Common Use Cases

- Infrastructure automation
- Cloud resource management
- CI/CD pipeline scripts
- Monitoring and alerting
- Configuration management
- Log analysis and processing
- Database operations
- Container orchestration

### Essential Libraries

```python
# Cloud Services
boto3          # AWS SDK
azure-mgmt-*   # Azure SDK
google-cloud-* # GCP SDK

# Infrastructure
ansible        # Configuration management
fabric         # Remote execution
paramiko       # SSH operations

# Containers
docker         # Docker SDK
kubernetes     # Kubernetes client

# Utilities
requests       # HTTP requests
pyyaml         # YAML parsing
jinja2         # Templating
click          # CLI creation
python-dotenv  # Environment variables
```

---

## 2. Python Basics for DevOps

### Environment Setup

**Virtual Environment:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**requirements.txt:**
```txt
boto3==1.28.0
requests==2.31.0
pyyaml==6.0.1
jinja2==3.1.2
click==8.1.7
python-dotenv==1.0.0
docker==6.1.3
kubernetes==28.1.0
```

### Essential Python Patterns

**Configuration Management:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Configuration class
class Config:
    def __init__(self):
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.db_host = os.getenv('DB_HOST')
        self.db_password = os.getenv('DB_PASSWORD')
    
    @classmethod
    def from_file(cls, config_file):
        import json
        with open(config_file) as f:
            config = json.load(f)
        instance = cls()
        instance.__dict__.update(config)
        return instance
```

**Logging:**
```python
import logging
import sys

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()
logger.info("Application started")
logger.error("An error occurred")
```

**Error Handling:**
```python
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def api_call():
    # API call that might fail
    pass
```

**Context Managers:**
```python
from contextlib import contextmanager

@contextmanager
def managed_resource(resource):
    """Context manager for resource cleanup"""
    try:
        resource.connect()
        yield resource
    finally:
        resource.disconnect()

# Usage
with managed_resource(database) as db:
    db.query("SELECT * FROM users")
```

---

## 3. Working with APIs

### REST API Client

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url, timeout=30, max_retries=3):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.timeout = timeout
    
    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def put(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.put(
            url,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.delete(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        return response.status_code

# Usage
client = APIClient("https://api.example.com")
users = client.get("users", params={"page": 1, "limit": 10})
```

### GitHub API Example

```python
import requests
from typing import List, Dict

class GitHubAPI:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_repositories(self, username: str) -> List[Dict]:
        url = f"{self.base_url}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_issue(self, owner: str, repo: str, title: str, body: str) -> Dict:
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        data = {"title": title, "body": body}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "open") -> List[Dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

# Usage
github = GitHubAPI(token="your-token")
repos = github.get_repositories("octocat")
```

### Webhook Handler

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your-secret-key"

def verify_signature(payload, signature):
    """Verify GitHub webhook signature"""
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    
    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    event = request.headers.get('X-GitHub-Event')
    data = request.json
    
    if event == 'push':
        handle_push_event(data)
    elif event == 'pull_request':
        handle_pull_request_event(data)
    elif event == 'issues':
        handle_issue_event(data)
    
    return jsonify({"status": "ok"}), 200

def handle_push_event(data):
    """Handle push event"""
    repo = data['repository']['name']
    branch = data['ref'].split('/')[-1]
    commits = data['commits']
    
    print(f"Push to {repo}/{branch}: {len(commits)} commits")
    # Trigger CI/CD pipeline
    # trigger_pipeline(repo, branch)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

---

## 4. AWS SDK (Boto3)

### Boto3 Basics

**Setup:**
```python
import boto3
from botocore.exceptions import ClientError

# Create clients
s3_client = boto3.client('s3', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')

# Create resources (higher-level API)
s3_resource = boto3.resource('s3')
ec2_resource = boto3.resource('ec2')
```

**Error Handling:**
```python
def handle_aws_error(func):
    """Decorator for AWS error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                logger.error(f"Bucket not found: {e}")
            elif error_code == 'AccessDenied':
                logger.error(f"Access denied: {e}")
            else:
                logger.error(f"AWS error: {e}")
            raise
    return wrapper
```

### S3 Operations

```python
import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, region_name='us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.s3_resource = boto3.resource('s3', region_name=region_name)
    
    def create_bucket(self, bucket_name, region=None):
        """Create S3 bucket"""
        try:
            if region:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                self.s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} created successfully")
        except ClientError as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, local_file, bucket_name, s3_key):
        """Upload file to S3"""
        try:
            self.s3_client.upload_file(
                local_file,
                bucket_name,
                s3_key,
                ExtraArgs={'ServerSideEncryption': 'AES256'}
            )
            print(f"File {local_file} uploaded to s3://{bucket_name}/{s3_key}")
        except ClientError as e:
            print(f"Error uploading file: {e}")
    
    def download_file(self, bucket_name, s3_key, local_file):
        """Download file from S3"""
        try:
            self.s3_client.download_file(bucket_name, s3_key, local_file)
            print(f"File downloaded from s3://{bucket_name}/{s3_key}")
        except ClientError as e:
            print(f"Error downloading file: {e}")
    
    def list_objects(self, bucket_name, prefix=''):
        """List objects in bucket"""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
            
            objects = []
            for page in pages:
                if 'Contents' in page:
                    objects.extend(page['Contents'])
            
            return objects
        except ClientError as e:
            print(f"Error listing objects: {e}")
            return []
    
    def delete_object(self, bucket_name, s3_key):
        """Delete object from S3"""
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
            print(f"Object s3://{bucket_name}/{s3_key} deleted")
        except ClientError as e:
            print(f"Error deleting object: {e}")
    
    def generate_presigned_url(self, bucket_name, s3_key, expiration=3600):
        """Generate presigned URL for temporary access"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
    
    def sync_directory(self, local_dir, bucket_name, s3_prefix=''):
        """Sync local directory to S3"""
        import os
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                s3_key = os.path.join(s3_prefix, relative_path).replace('\\', '/')
                self.upload_file(local_path, bucket_name, s3_key)

# Usage
s3 = S3Manager()
s3.create_bucket('my-bucket')
s3.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')
objects = s3.list_objects('my-bucket', prefix='data/')
```

### EC2 Operations

```python
import boto3
from botocore.exceptions import ClientError

class EC2Manager:
    def __init__(self, region_name='us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)
    
    def list_instances(self, filters=None):
        """List EC2 instances"""
        try:
            instances = self.ec2_resource.instances.filter(Filters=filters or [])
            return [
                {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'state': instance.state['Name'],
                    'public_ip': instance.public_ip_address,
                    'private_ip': instance.private_ip_address,
                    'tags': {tag['Key']: tag['Value'] for tag in instance.tags or []}
                }
                for instance in instances
            ]
        except ClientError as e:
            print(f"Error listing instances: {e}")
            return []
    
    def create_instance(self, image_id, instance_type, key_name, 
                       security_group_ids, user_data=None, tags=None):
        """Launch EC2 instance"""
        try:
            instances = self.ec2_resource.create_instances(
                ImageId=image_id,
                MinCount=1,
                MaxCount=1,
                InstanceType=instance_type,
                KeyName=key_name,
                SecurityGroupIds=security_group_ids,
                UserData=user_data,
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': tags or []
                }]
            )
            instance = instances[0]
            instance.wait_until_running()
            print(f"Instance {instance.id} created and running")
            return instance
        except ClientError as e:
            print(f"Error creating instance: {e}")
            return None
    
    def terminate_instance(self, instance_id):
        """Terminate EC2 instance"""
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.terminate()
            instance.wait_until_terminated()
            print(f"Instance {instance_id} terminated")
        except ClientError as e:
            print(f"Error terminating instance: {e}")
    
    def create_security_group(self, name, description, vpc_id):
        """Create security group"""
        try:
            sg = self.ec2_resource.create_security_group(
                GroupName=name,
                Description=description,
                VpcId=vpc_id
            )
            print(f"Security group {sg.id} created")
            return sg
        except ClientError as e:
            print(f"Error creating security group: {e}")
            return None
    
    def add_security_group_rule(self, group_id, protocol, port, cidr):
        """Add rule to security group"""
        try:
            self.ec2_client.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[{
                    'IpProtocol': protocol,
                    'FromPort': port,
                    'ToPort': port,
                    'IpRanges': [{'CidrIp': cidr}]
                }]
            )
            print(f"Rule added to security group {group_id}")
        except ClientError as e:
            print(f"Error adding rule: {e}")

# Usage
ec2 = EC2Manager()
instances = ec2.list_instances(filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
```

### DynamoDB Operations

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class DynamoDBManager:
    def __init__(self, region_name='us-east-1'):
        self.dynamodb_client = boto3.client('dynamodb', region_name=region_name)
        self.dynamodb_resource = boto3.resource('dynamodb', region_name=region_name)
    
    def create_table(self, table_name, partition_key, sort_key=None, 
                    read_capacity=5, write_capacity=5):
        """Create DynamoDB table"""
        try:
            key_schema = [
                {'AttributeName': partition_key, 'KeyType': 'HASH'}
            ]
            attribute_definitions = [
                {'AttributeName': partition_key, 'AttributeType': 'S'}
            ]
            
            if sort_key:
                key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})
            
            table = self.dynamodb_resource.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                BillingMode='PROVISIONED',
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_capacity,
                    'WriteCapacityUnits': write_capacity
                }
            )
            table.wait_until_exists()
            print(f"Table {table_name} created")
            return table
        except ClientError as e:
            print(f"Error creating table: {e}")
            return None
    
    def put_item(self, table_name, item):
        """Put item in table"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            table.put_item(Item=item)
            print(f"Item added to {table_name}")
        except ClientError as e:
            print(f"Error putting item: {e}")
    
    def get_item(self, table_name, key):
        """Get item from table"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            response = table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item: {e}")
            return None
    
    def query(self, table_name, partition_key_value, sort_key_condition=None):
        """Query table"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            if sort_key_condition:
                response = table.query(
                    KeyConditionExpression=Key('id').eq(partition_key_value) & 
                                         sort_key_condition
                )
            else:
                response = table.query(
                    KeyConditionExpression=Key('id').eq(partition_key_value)
                )
            return response['Items']
        except ClientError as e:
            print(f"Error querying table: {e}")
            return []
    
    def scan(self, table_name, filter_expression=None):
        """Scan table"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            if filter_expression:
                response = table.scan(FilterExpression=filter_expression)
            else:
                response = table.scan()
            return response['Items']
        except ClientError as e:
            print(f"Error scanning table: {e}")
            return []
    
    def update_item(self, table_name, key, update_expression, expression_values):
        """Update item"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            print(f"Item updated in {table_name}")
        except ClientError as e:
            print(f"Error updating item: {e}")
    
    def delete_item(self, table_name, key):
        """Delete item"""
        try:
            table = self.dynamodb_resource.Table(table_name)
            table.delete_item(Key=key)
            print(f"Item deleted from {table_name}")
        except ClientError as e:
            print(f"Error deleting item: {e}")

# Usage
dynamodb = DynamoDBManager()
table = dynamodb.create_table('users', 'user_id')
dynamodb.put_item('users', {'user_id': '123', 'name': 'John', 'email': 'john@example.com'})
user = dynamodb.get_item('users', {'user_id': '123'})
```

### Lambda Functions

```python
import boto3
import json
import zipfile
import io

class LambdaManager:
    def __init__(self, region_name='us-east-1'):
        self.lambda_client = boto3.client('lambda', region_name=region_name)
    
    def create_function(self, function_name, runtime, role_arn, handler, 
                       code_zip, description=None, timeout=3, memory=128):
        """Create Lambda function"""
        try:
            with open(code_zip, 'rb') as f:
                zip_content = f.read()
            
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler,
                Code={'ZipFile': zip_content},
                Description=description,
                Timeout=timeout,
                MemorySize=memory
            )
            print(f"Function {function_name} created")
            return response
        except ClientError as e:
            print(f"Error creating function: {e}")
            return None
    
    def invoke_function(self, function_name, payload=None):
        """Invoke Lambda function"""
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload) if payload else '{}'
            )
            result = json.loads(response['Payload'].read())
            return result
        except ClientError as e:
            print(f"Error invoking function: {e}")
            return None
    
    def update_function_code(self, function_name, code_zip):
        """Update Lambda function code"""
        try:
            with open(code_zip, 'rb') as f:
                zip_content = f.read()
            
            response = self.lambda_client.update_function_code(
                FunctionName=function_name,
                ZipFile=zip_content
            )
            print(f"Function {function_name} code updated")
            return response
        except ClientError as e:
            print(f"Error updating function code: {e}")
            return None
    
    def create_zip_package(self, source_dir, output_file):
        """Create ZIP package for Lambda"""
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            import os
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)

# Example Lambda function
def lambda_handler(event, context):
    """Example Lambda handler"""
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda',
            'event': event
        })
    }
```

---

## 5. Infrastructure as Code with Python

### Terraform Python Provider

```python
import subprocess
import json
import os

class TerraformManager:
    def __init__(self, working_dir='.'):
        self.working_dir = working_dir
    
    def init(self, backend_config=None):
        """Initialize Terraform"""
        cmd = ['terraform', 'init']
        if backend_config:
            for key, value in backend_config.items():
                cmd.extend(['-backend-config', f'{key}={value}'])
        
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        return result.returncode == 0
    
    def plan(self, var_file=None, variables=None):
        """Run terraform plan"""
        cmd = ['terraform', 'plan', '-out=tfplan']
        
        if var_file:
            cmd.extend(['-var-file', var_file])
        
        if variables:
            for key, value in variables.items():
                cmd.extend(['-var', f'{key}={value}'])
        
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        return result.stdout, result.returncode == 0
    
    def apply(self, auto_approve=True):
        """Apply Terraform changes"""
        cmd = ['terraform', 'apply']
        if auto_approve:
            cmd.append('-auto-approve')
        else:
            cmd.append('tfplan')
        
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        return result.stdout, result.returncode == 0
    
    def destroy(self, auto_approve=True):
        """Destroy infrastructure"""
        cmd = ['terraform', 'destroy']
        if auto_approve:
            cmd.append('-auto-approve')
        
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        return result.stdout, result.returncode == 0
    
    def output(self, output_name=None):
        """Get Terraform outputs"""
        cmd = ['terraform', 'output', '-json']
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            outputs = json.loads(result.stdout)
            if output_name:
                return outputs.get(output_name, {}).get('value')
            return outputs
        return None
    
    def validate(self):
        """Validate Terraform configuration"""
        cmd = ['terraform', 'validate']
        result = subprocess.run(cmd, cwd=self.working_dir, capture_output=True, text=True)
        return result.returncode == 0, result.stdout

# Usage
tf = TerraformManager(working_dir='./terraform')
tf.init()
plan_output, success = tf.plan(variables={'instance_type': 't3.micro'})
if success:
    apply_output, success = tf.apply()
    outputs = tf.output()
```

### Ansible Integration

```python
from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_ansible_playbook(playbook, inventory=None, extra_vars=None):
    """Run Ansible playbook"""
    cmd = ['ansible-playbook', playbook]
    
    if inventory:
        cmd.extend(['-i', inventory])
    
    if extra_vars:
        cmd.extend(['-e', json.dumps(extra_vars)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout

# Ansible module example
def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )
    )
    
    name = module.params['name']
    state = module.params['state']
    
    # Your logic here
    if state == 'present':
        # Create resource
        module.exit_json(changed=True, msg=f"Resource {name} created")
    else:
        # Delete resource
        module.exit_json(changed=True, msg=f"Resource {name} deleted")

if __name__ == '__main__':
    main()
```

### CloudFormation with Python

```python
import boto3
import yaml
import json

class CloudFormationManager:
    def __init__(self, region_name='us-east-1'):
        self.cf_client = boto3.client('cloudformation', region_name=region_name)
    
    def create_stack(self, stack_name, template_file, parameters=None):
        """Create CloudFormation stack"""
        with open(template_file) as f:
            if template_file.endswith('.yaml') or template_file.endswith('.yml'):
                template_body = yaml.safe_load(f)
                template_body = json.dumps(template_body)
            else:
                template_body = f.read()
        
        try:
            response = self.cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters or [],
                Capabilities=['CAPABILITY_IAM']
            )
            print(f"Stack {stack_name} creation initiated")
            return response['StackId']
        except ClientError as e:
            print(f"Error creating stack: {e}")
            return None
    
    def update_stack(self, stack_name, template_file, parameters=None):
        """Update CloudFormation stack"""
        with open(template_file) as f:
            if template_file.endswith('.yaml') or template_file.endswith('.yml'):
                template_body = yaml.safe_load(f)
                template_body = json.dumps(template_body)
            else:
                template_body = f.read()
        
        try:
            response = self.cf_client.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters or []
            )
            print(f"Stack {stack_name} update initiated")
            return response['StackId']
        except ClientError as e:
            print(f"Error updating stack: {e}")
            return None
    
    def delete_stack(self, stack_name):
        """Delete CloudFormation stack"""
        try:
            self.cf_client.delete_stack(StackName=stack_name)
            print(f"Stack {stack_name} deletion initiated")
        except ClientError as e:
            print(f"Error deleting stack: {e}")
    
    def describe_stack(self, stack_name):
        """Describe stack"""
        try:
            response = self.cf_client.describe_stacks(StackName=stack_name)
            return response['Stacks'][0] if response['Stacks'] else None
        except ClientError as e:
            print(f"Error describing stack: {e}")
            return None
    
    def get_stack_outputs(self, stack_name):
        """Get stack outputs"""
        stack = self.describe_stack(stack_name)
        if stack:
            return {output['OutputKey']: output['OutputValue'] 
                   for output in stack.get('Outputs', [])}
        return {}

# Usage
cf = CloudFormationManager()
stack_id = cf.create_stack('my-stack', 'template.yaml', [
    {'ParameterKey': 'InstanceType', 'ParameterValue': 't3.micro'}
])
outputs = cf.get_stack_outputs('my-stack')
```

---

## 6. Docker Operations

### Docker SDK

```python
import docker
from docker.errors import APIError

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
    
    def build_image(self, dockerfile_path, tag, context_path='.'):
        """Build Docker image"""
        try:
            image, logs = self.client.images.build(
                path=context_path,
                dockerfile=dockerfile_path,
                tag=tag
            )
            print(f"Image {tag} built successfully")
            return image
        except APIError as e:
            print(f"Error building image: {e}")
            return None
    
    def run_container(self, image, command=None, detach=True, 
                     ports=None, environment=None, volumes=None):
        """Run Docker container"""
        try:
            container = self.client.containers.run(
                image,
                command=command,
                detach=detach,
                ports=ports or {},
                environment=environment or {},
                volumes=volumes or {}
            )
            print(f"Container {container.id} started")
            return container
        except APIError as e:
            print(f"Error running container: {e}")
            return None
    
    def list_containers(self, all=True, filters=None):
        """List containers"""
        try:
            containers = self.client.containers.list(all=all, filters=filters or {})
            return [
                {
                    'id': c.id,
                    'name': c.name,
                    'image': c.image.tags[0] if c.image.tags else '',
                    'status': c.status,
                    'ports': c.ports
                }
                for c in containers
            ]
        except APIError as e:
            print(f"Error listing containers: {e}")
            return []
    
    def stop_container(self, container_id):
        """Stop container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            print(f"Container {container_id} stopped")
        except APIError as e:
            print(f"Error stopping container: {e}")
    
    def remove_container(self, container_id, force=False):
        """Remove container"""
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            print(f"Container {container_id} removed")
        except APIError as e:
            print(f"Error removing container: {e}")
    
    def get_container_logs(self, container_id, tail=100):
        """Get container logs"""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail)
            return logs.decode('utf-8')
        except APIError as e:
            print(f"Error getting logs: {e}")
            return None
    
    def push_image(self, image_tag, registry=None):
        """Push image to registry"""
        try:
            image = self.client.images.get(image_tag)
            if registry:
                image.tag(f"{registry}/{image_tag}")
                image_tag = f"{registry}/{image_tag}"
            
            for line in self.client.images.push(image_tag, stream=True, decode=True):
                if 'error' in line:
                    print(f"Error: {line['error']}")
                    return False
            print(f"Image {image_tag} pushed successfully")
            return True
        except APIError as e:
            print(f"Error pushing image: {e}")
            return False
    
    def pull_image(self, image_tag):
        """Pull image from registry"""
        try:
            image = self.client.images.pull(image_tag)
            print(f"Image {image_tag} pulled successfully")
            return image
        except APIError as e:
            print(f"Error pulling image: {e}")
            return None

# Usage
docker_mgr = DockerManager()
image = docker_mgr.build_image('Dockerfile', 'myapp:latest')
container = docker_mgr.run_container(
    'myapp:latest',
    ports={'8080/tcp': 8080},
    environment={'ENV': 'production'}
)
containers = docker_mgr.list_containers()
logs = docker_mgr.get_container_logs(container.id)
```

### Docker Compose Operations

```python
import yaml
import subprocess

class DockerComposeManager:
    def __init__(self, compose_file='docker-compose.yml'):
        self.compose_file = compose_file
    
    def up(self, services=None, detach=True, build=False):
        """Start services"""
        cmd = ['docker-compose', '-f', self.compose_file, 'up']
        if detach:
            cmd.append('-d')
        if build:
            cmd.append('--build')
        if services:
            cmd.extend(services)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    def down(self, volumes=False):
        """Stop services"""
        cmd = ['docker-compose', '-f', self.compose_file, 'down']
        if volumes:
            cmd.append('-v')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    
    def ps(self):
        """List running services"""
        cmd = ['docker-compose', '-f', self.compose_file, 'ps']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def logs(self, service=None, tail=100, follow=False):
        """Get service logs"""
        cmd = ['docker-compose', '-f', self.compose_file, 'logs']
        if tail:
            cmd.extend(['--tail', str(tail)])
        if follow:
            cmd.append('-f')
        if service:
            cmd.append(service)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    def scale(self, service, replicas):
        """Scale service"""
        cmd = ['docker-compose', '-f', self.compose_file, 'up', '-d', '--scale', 
               f'{service}={replicas}']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

# Usage
compose = DockerComposeManager('docker-compose.yml')
compose.up(build=True)
compose.scale('web', 3)
logs = compose.logs('web', tail=50)
compose.down()
```

---

## 7. Kubernetes Operations

### Kubernetes Python Client

```python
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class KubernetesManager:
    def __init__(self, config_file=None, context=None):
        if config_file:
            config.load_kube_config(config_file=config_file, context=context)
        else:
            try:
                config.load_incluster_config()  # Running in cluster
            except:
                config.load_kube_config()  # Running locally
        
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.batch_v1 = client.BatchV1Api()
    
    def list_pods(self, namespace='default', label_selector=None):
        """List pods"""
        try:
            pods = self.v1.list_namespaced_pod(
                namespace=namespace,
                label_selector=label_selector
            )
            return [
                {
                    'name': pod.metadata.name,
                    'namespace': pod.metadata.namespace,
                    'status': pod.status.phase,
                    'node': pod.spec.node_name,
                    'ip': pod.status.pod_ip
                }
                for pod in pods.items
            ]
        except ApiException as e:
            print(f"Error listing pods: {e}")
            return []
    
    def get_pod_logs(self, name, namespace='default', tail_lines=100):
        """Get pod logs"""
        try:
            logs = self.v1.read_namespaced_pod_log(
                name=name,
                namespace=namespace,
                tail_lines=tail_lines
            )
            return logs
        except ApiException as e:
            print(f"Error getting logs: {e}")
            return None
    
    def create_deployment(self, name, image, replicas=1, namespace='default', 
                         labels=None, env_vars=None):
        """Create deployment"""
        try:
            deployment = client.V1Deployment(
                metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                spec=client.V1DeploymentSpec(
                    replicas=replicas,
                    selector=client.V1LabelSelector(
                        match_labels=labels or {'app': name}
                    ),
                    template=client.V1PodTemplateSpec(
                        metadata=client.V1ObjectMeta(labels=labels or {'app': name}),
                        spec=client.V1PodSpec(
                            containers=[
                                client.V1Container(
                                    name=name,
                                    image=image,
                                    env=[
                                        client.V1EnvVar(name=k, value=v)
                                        for k, v in (env_vars or {}).items()
                                    ]
                                )
                            ]
                        )
                    )
                )
            )
            
            response = self.apps_v1.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            print(f"Deployment {name} created")
            return response
        except ApiException as e:
            print(f"Error creating deployment: {e}")
            return None
    
    def scale_deployment(self, name, replicas, namespace='default'):
        """Scale deployment"""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=name,
                namespace=namespace
            )
            deployment.spec.replicas = replicas
            
            self.apps_v1.patch_namespaced_deployment_scale(
                name=name,
                namespace=namespace,
                body=client.V1Scale(spec=client.V1ScaleSpec(replicas=replicas))
            )
            print(f"Deployment {name} scaled to {replicas}")
        except ApiException as e:
            print(f"Error scaling deployment: {e}")
    
    def create_service(self, name, selector, ports, namespace='default', 
                      service_type='ClusterIP'):
        """Create service"""
        try:
            service = client.V1Service(
                metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                spec=client.V1ServiceSpec(
                    selector=selector,
                    ports=[
                        client.V1ServicePort(port=port, target_port=target_port)
                        for port, target_port in ports
                    ],
                    type=service_type
                )
            )
            
            response = self.v1.create_namespaced_service(
                namespace=namespace,
                body=service
            )
            print(f"Service {name} created")
            return response
        except ApiException as e:
            print(f"Error creating service: {e}")
            return None
    
    def create_configmap(self, name, data, namespace='default'):
        """Create ConfigMap"""
        try:
            configmap = client.V1ConfigMap(
                metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                data=data
            )
            
            response = self.v1.create_namespaced_config_map(
                namespace=namespace,
                body=configmap
            )
            print(f"ConfigMap {name} created")
            return response
        except ApiException as e:
            print(f"Error creating ConfigMap: {e}")
            return None
    
    def create_secret(self, name, data, namespace='default'):
        """Create Secret"""
        try:
            import base64
            encoded_data = {
                k: base64.b64encode(v.encode()).decode()
                for k, v in data.items()
            }
            
            secret = client.V1Secret(
                metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                type='Opaque',
                data=encoded_data
            )
            
            response = self.v1.create_namespaced_secret(
                namespace=namespace,
                body=secret
            )
            print(f"Secret {name} created")
            return response
        except ApiException as e:
            print(f"Error creating secret: {e}")
            return None
    
    def delete_deployment(self, name, namespace='default'):
        """Delete deployment"""
        try:
            self.apps_v1.delete_namespaced_deployment(
                name=name,
                namespace=namespace,
                body=client.V1DeleteOptions(propagation_policy='Foreground')
            )
            print(f"Deployment {name} deleted")
        except ApiException as e:
            print(f"Error deleting deployment: {e}")

# Usage
k8s = KubernetesManager()
pods = k8s.list_pods(namespace='default')
k8s.create_deployment('myapp', 'nginx:latest', replicas=3)
k8s.scale_deployment('myapp', 5)
k8s.create_service('myapp', {'app': 'myapp'}, [(80, 80)])
```

---

## 8. Configuration Management

### YAML Processing

```python
import yaml
from pathlib import Path

class YAMLManager:
    @staticmethod
    def load(file_path):
        """Load YAML file"""
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def dump(data, file_path):
        """Dump data to YAML file"""
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def merge(*yaml_files):
        """Merge multiple YAML files"""
        merged = {}
        for file_path in yaml_files:
            data = YAMLManager.load(file_path)
            merged.update(data)
        return merged
    
    @staticmethod
    def update(file_path, updates):
        """Update YAML file with new values"""
        data = YAMLManager.load(file_path)
        
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if isinstance(value, dict) and key in base_dict:
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(data, updates)
        YAMLManager.dump(data, file_path)

# Usage
config = YAMLManager.load('config.yaml')
YAMLManager.update('config.yaml', {'database': {'host': 'new-host'}})
```

### Environment Configuration

```python
import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    username: str
    password: str
    
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 5432)),
            database=os.getenv('DB_NAME', 'mydb'),
            username=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password')
        )

class ConfigManager:
    def __init__(self, env_file='.env'):
        self.load_env(env_file)
        self.config = {
            'database': DatabaseConfig.from_env(),
            'aws': {
                'region': os.getenv('AWS_REGION', 'us-east-1'),
                'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
                'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')
            }
        }
    
    @staticmethod
    def load_env(env_file):
        """Load environment variables from file"""
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

# Usage
config = ConfigManager('.env')
db_config = config.get('database')
```

### Jinja2 Templating

```python
from jinja2 import Template, Environment, FileSystemLoader

class TemplateManager:
    def __init__(self, template_dir='templates'):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render(self, template_name, context):
        """Render template with context"""
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_string(self, template_string, context):
        """Render template from string"""
        template = Template(template_string)
        return template.render(**context)
    
    def render_to_file(self, template_name, context, output_file):
        """Render template to file"""
        content = self.render(template_name, context)
        with open(output_file, 'w') as f:
            f.write(content)

# Example template: nginx.conf.j2
# server {
#     listen {{ port }};
#     server_name {{ server_name }};
#     
#     location / {
#         proxy_pass http://{{ upstream }};
#     }
# }

# Usage
tmpl = TemplateManager('templates')
config = tmpl.render('nginx.conf.j2', {
    'port': 80,
    'server_name': 'example.com',
    'upstream': 'backend:8080'
})
tmpl.render_to_file('nginx.conf.j2', config, 'nginx.conf')
```

---

## 9. Monitoring and Logging

### CloudWatch Integration

```python
import boto3
from datetime import datetime, timedelta

class CloudWatchManager:
    def __init__(self, region_name='us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)
        self.logs = boto3.client('logs', region_name=region_name)
    
    def put_metric(self, namespace, metric_name, value, unit='Count', dimensions=None):
        """Put custom metric"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace=namespace,
                MetricData=[{
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Dimensions': dimensions or []
                }]
            )
        except ClientError as e:
            print(f"Error putting metric: {e}")
    
    def get_metric_statistics(self, namespace, metric_name, start_time, end_time,
                            period=300, statistics=['Average']):
        """Get metric statistics"""
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statistics
            )
            return response['Datapoints']
        except ClientError as e:
            print(f"Error getting metrics: {e}")
            return []
    
    def create_alarm(self, alarm_name, metric_name, namespace, threshold,
                    comparison_operator='GreaterThanThreshold', evaluation_periods=1):
        """Create CloudWatch alarm"""
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=comparison_operator,
                EvaluationPeriods=evaluation_periods,
                MetricName=metric_name,
                Namespace=namespace,
                Period=300,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True
            )
            print(f"Alarm {alarm_name} created")
        except ClientError as e:
            print(f"Error creating alarm: {e}")
    
    def put_log_events(self, log_group, log_stream, messages):
        """Put log events"""
        try:
            events = [
                {
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'message': msg
                }
                for msg in messages
            ]
            
            self.logs.put_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
                logEvents=events
            )
        except ClientError as e:
            print(f"Error putting log events: {e}")
    
    def get_log_events(self, log_group, log_stream, start_time=None, end_time=None):
        """Get log events"""
        try:
            kwargs = {
                'logGroupName': log_group,
                'logStreamName': log_stream
            }
            if start_time:
                kwargs['startTime'] = int(start_time.timestamp() * 1000)
            if end_time:
                kwargs['endTime'] = int(end_time.timestamp() * 1000)
            
            response = self.logs.get_log_events(**kwargs)
            return response['events']
        except ClientError as e:
            print(f"Error getting log events: {e}")
            return []

# Usage
cw = CloudWatchManager()
cw.put_metric('MyApp', 'RequestCount', 100)
metrics = cw.get_metric_statistics(
    'MyApp', 'RequestCount',
    datetime.now() - timedelta(hours=1),
    datetime.now()
)
cw.create_alarm('HighCPU', 'CPUUtilization', 'AWS/EC2', 80.0)
```

### Log Processing

```python
import re
from collections import Counter
from datetime import datetime

class LogProcessor:
    def __init__(self, log_file):
        self.log_file = log_file
    
    def parse_log_line(self, line, pattern):
        """Parse log line with regex pattern"""
        match = re.match(pattern, line)
        if match:
            return match.groupdict()
        return None
    
    def count_errors(self, error_pattern=r'ERROR|FATAL|CRITICAL'):
        """Count error occurrences"""
        error_count = 0
        with open(self.log_file) as f:
            for line in f:
                if re.search(error_pattern, line, re.IGNORECASE):
                    error_count += 1
        return error_count
    
    def extract_ips(self):
        """Extract IP addresses from logs"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = []
        with open(self.log_file) as f:
            for line in f:
                ips.extend(re.findall(ip_pattern, line))
        return Counter(ips)
    
    def filter_by_time_range(self, start_time, end_time, time_format='%Y-%m-%d %H:%M:%S'):
        """Filter logs by time range"""
        filtered_lines = []
        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format)
        
        with open(self.log_file) as f:
            for line in f:
                # Extract timestamp from line (adjust pattern as needed)
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if timestamp_match:
                    log_time = datetime.strptime(timestamp_match.group(1), time_format)
                    if start <= log_time <= end:
                        filtered_lines.append(line)
        
        return filtered_lines
    
    def analyze_response_times(self, pattern=r'response_time=(\d+\.?\d*)'):
        """Analyze response times"""
        response_times = []
        with open(self.log_file) as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    response_times.append(float(match.group(1)))
        
        if response_times:
            return {
                'min': min(response_times),
                'max': max(response_times),
                'avg': sum(response_times) / len(response_times),
                'p95': sorted(response_times)[int(len(response_times) * 0.95)]
            }
        return None

# Usage
processor = LogProcessor('app.log')
error_count = processor.count_errors()
ip_counts = processor.extract_ips()
response_stats = processor.analyze_response_times()
```

---

## 10. CI/CD Automation

### GitHub Actions Automation

```python
import requests
import json

class GitHubActionsManager:
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def trigger_workflow(self, workflow_id, ref='main', inputs=None):
        """Trigger GitHub Actions workflow"""
        url = f"{self.base_url}/actions/workflows/{workflow_id}/dispatches"
        data = {
            "ref": ref,
            "inputs": inputs or {}
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.status_code == 204
    
    def get_workflow_runs(self, workflow_id=None, status=None):
        """Get workflow runs"""
        if workflow_id:
            url = f"{self.base_url}/actions/workflows/{workflow_id}/runs"
        else:
            url = f"{self.base_url}/actions/runs"
        
        params = {}
        if status:
            params['status'] = status
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_workflow_run(self, run_id):
        """Get specific workflow run"""
        url = f"{self.base_url}/actions/runs/{run_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def cancel_workflow_run(self, run_id):
        """Cancel workflow run"""
        url = f"{self.base_url}/actions/runs/{run_id}/cancel"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 202

# Usage
gh = GitHubActionsManager(token, 'owner', 'repo')
gh.trigger_workflow('deploy.yml', inputs={'environment': 'production'})
runs = gh.get_workflow_runs(status='in_progress')
```

### Jenkins Automation

```python
import requests
from requests.auth import HTTPBasicAuth

class JenkinsManager:
    def __init__(self, url, username, api_token):
        self.url = url.rstrip('/')
        self.auth = HTTPBasicAuth(username, api_token)
    
    def trigger_build(self, job_name, parameters=None):
        """Trigger Jenkins build"""
        if parameters:
            url = f"{self.url}/job/{job_name}/buildWithParameters"
            response = requests.post(url, auth=self.auth, data=parameters)
        else:
            url = f"{self.url}/job/{job_name}/build"
            response = requests.post(url, auth=self.auth)
        
        response.raise_for_status()
        return response.status_code == 201
    
    def get_build_info(self, job_name, build_number):
        """Get build information"""
        url = f"{self.url}/job/{job_name}/{build_number}/api/json"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()
    
    def get_build_console(self, job_name, build_number):
        """Get build console output"""
        url = f"{self.url}/job/{job_name}/{build_number}/consoleText"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.text
    
    def get_job_info(self, job_name):
        """Get job information"""
        url = f"{self.url}/job/{job_name}/api/json"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

# Usage
jenkins = JenkinsManager('http://jenkins.example.com', 'user', 'token')
jenkins.trigger_build('my-job', {'BRANCH': 'main'})
build_info = jenkins.get_build_info('my-job', 123)
```

---

## 11. Database Operations

### Database Connection Manager

```python
import psycopg2
import pymysql
from contextlib import contextmanager
from typing import Dict, List, Any

class DatabaseManager:
    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.connection_params = kwargs
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connection"""
        if self.db_type == 'postgresql':
            conn = psycopg2.connect(**self.connection_params)
        elif self.db_type == 'mysql':
            conn = pymysql.connect(**self.connection_params)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute SQL query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return cursor.rowcount
    
    def execute_many(self, query, params_list):
        """Execute query with multiple parameter sets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def backup_table(self, table_name, output_file):
        """Backup table to CSV"""
        query = f"SELECT * FROM {table_name}"
        results = self.execute_query(query)
        
        import csv
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(results)

# Usage
db = DatabaseManager(
    'postgresql',
    host='localhost',
    database='mydb',
    user='user',
    password='password'
)
results = db.execute_query("SELECT * FROM users WHERE id = %s", (1,))
```

---

## 12. File and Data Processing

### CSV Processing

```python
import csv
from typing import List, Dict

class CSVProcessor:
    @staticmethod
    def read_csv(file_path, delimiter=',') -> List[Dict]:
        """Read CSV file to list of dictionaries"""
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            return list(reader)
    
    @staticmethod
    def write_csv(data: List[Dict], file_path, fieldnames=None):
        """Write list of dictionaries to CSV"""
        if not data:
            return
        
        fieldnames = fieldnames or data[0].keys()
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def filter_csv(input_file, output_file, filter_func):
        """Filter CSV rows based on function"""
        data = CSVProcessor.read_csv(input_file)
        filtered = [row for row in data if filter_func(row)]
        CSVProcessor.write_csv(filtered, output_file)
    
    @staticmethod
    def merge_csvs(*input_files, output_file):
        """Merge multiple CSV files"""
        all_data = []
        for file_path in input_files:
            all_data.extend(CSVProcessor.read_csv(file_path))
        CSVProcessor.write_csv(all_data, output_file)

# Usage
data = CSVProcessor.read_csv('data.csv')
CSVProcessor.write_csv(data, 'output.csv')
```

### JSON Processing

```python
import json
from typing import Any

class JSONProcessor:
    @staticmethod
    def load(file_path) -> Any:
        """Load JSON file"""
        with open(file_path) as f:
            return json.load(f)
    
    @staticmethod
    def dump(data: Any, file_path, indent=2):
        """Dump data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)
    
    @staticmethod
    def merge(*json_files, output_file):
        """Merge multiple JSON files"""
        merged = {}
        for file_path in json_files:
            data = JSONProcessor.load(file_path)
            if isinstance(data, dict):
                merged.update(data)
            else:
                merged[file_path] = data
        JSONProcessor.dump(merged, output_file)

# Usage
data = JSONProcessor.load('config.json')
JSONProcessor.dump(data, 'output.json')
```

---

## 13. Network Operations

### SSH Operations

```python
import paramiko
from typing import List, Tuple

class SSHManager:
    def __init__(self, hostname, username, key_file=None, password=None):
        self.hostname = hostname
        self.username = username
        self.key_file = key_file
        self.password = password
        self.client = None
    
    def connect(self):
        """Establish SSH connection"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if self.key_file:
            self.client.connect(
                self.hostname,
                username=self.username,
                key_filename=self.key_file
            )
        else:
            self.client.connect(
                self.hostname,
                username=self.username,
                password=self.password
            )
    
    def execute_command(self, command) -> Tuple[int, str, str]:
        """Execute command remotely"""
        if not self.client:
            self.connect()
        
        stdin, stdout, stderr = self.client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return exit_status, stdout.read().decode(), stderr.read().decode()
    
    def upload_file(self, local_path, remote_path):
        """Upload file via SFTP"""
        if not self.client:
            self.connect()
        
        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
    
    def download_file(self, remote_path, local_path):
        """Download file via SFTP"""
        if not self.client:
            self.connect()
        
        sftp = self.client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
    
    def close(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()

# Usage
ssh = SSHManager('server.example.com', 'user', key_file='~/.ssh/id_rsa')
exit_code, stdout, stderr = ssh.execute_command('ls -la')
ssh.upload_file('local.txt', '/remote/path/file.txt')
ssh.close()
```

---

## 14. Security Automation

### Secrets Management

```python
import boto3
import base64
from cryptography.fernet import Fernet

class SecretsManager:
    def __init__(self, region_name='us-east-1'):
        self.secrets_client = boto3.client('secretsmanager', region_name=region_name)
    
    def get_secret(self, secret_name):
        """Get secret from AWS Secrets Manager"""
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in response:
                import json
                return json.loads(response['SecretString'])
            else:
                return base64.b64decode(response['SecretBinary'])
        except ClientError as e:
            print(f"Error getting secret: {e}")
            return None
    
    def create_secret(self, secret_name, secret_value):
        """Create secret in AWS Secrets Manager"""
        try:
            import json
            if isinstance(secret_value, dict):
                secret_string = json.dumps(secret_value)
            else:
                secret_string = secret_value
            
            self.secrets_client.create_secret(
                Name=secret_name,
                SecretString=secret_string
            )
            print(f"Secret {secret_name} created")
        except ClientError as e:
            print(f"Error creating secret: {e}")
    
    def rotate_secret(self, secret_name):
        """Rotate secret"""
        try:
            self.secrets_client.rotate_secret(SecretId=secret_name)
            print(f"Secret {secret_name} rotation initiated")
        except ClientError as e:
            print(f"Error rotating secret: {e}")

# Usage
secrets = SecretsManager()
db_credentials = secrets.get_secret('db-credentials')
```

### Encryption/Decryption

```python
from cryptography.fernet import Fernet
import base64

class EncryptionManager:
    def __init__(self, key=None):
        if key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    def get_key(self) -> str:
        """Get encryption key"""
        return self.key.decode()

# Usage
enc = EncryptionManager()
encrypted = enc.encrypt("sensitive data")
decrypted = enc.decrypt(encrypted)
```

---

## 15. Error Handling and Best Practices

### Best Practices

**1. Use Type Hints:**
```python
from typing import List, Dict, Optional

def process_users(users: List[Dict[str, str]]) -> Optional[int]:
    """Process list of users"""
    if not users:
        return None
    return len(users)
```

**2. Use Logging:**
```python
import logging

logger = logging.getLogger(__name__)

def risky_operation():
    try:
        # Operation
        pass
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        raise
```

**3. Use Context Managers:**
```python
with open('file.txt') as f:
    content = f.read()
# File automatically closed
```

**4. Handle Exceptions Properly:**
```python
try:
    result = operation()
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    # Handle specific error
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

**5. Use Configuration Files:**
```python
# config.yaml
database:
  host: localhost
  port: 5432

# Load in code
config = YAMLManager.load('config.yaml')
```

**6. Write Tests:**
```python
import unittest

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager('postgresql', **test_config)
    
    def test_query(self):
        result = self.db.execute_query("SELECT 1")
        self.assertEqual(result[0][0], 1)

if __name__ == '__main__':
    unittest.main()
```

**7. Use Virtual Environments:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**8. Document Code:**
```python
def process_data(data: List[Dict], filter_func: callable) -> List[Dict]:
    """
    Process data with filter function.
    
    Args:
        data: List of dictionaries to process
        filter_func: Function to filter data
    
    Returns:
        Filtered list of dictionaries
    
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    return [item for item in data if filter_func(item)]
```

---

## Summary

This comprehensive Python for DevOps tutorial covers:

- **Python Basics**: Environment setup, patterns, error handling
- **API Integration**: REST clients, webhooks, GitHub API
- **AWS SDK**: S3, EC2, DynamoDB, Lambda operations
- **Infrastructure**: Terraform, Ansible, CloudFormation
- **Containers**: Docker SDK, Docker Compose
- **Kubernetes**: Python client operations
- **Configuration**: YAML, environment variables, templating
- **Monitoring**: CloudWatch integration, log processing
- **CI/CD**: GitHub Actions, Jenkins automation
- **Database**: Connection management, operations
- **File Processing**: CSV, JSON operations
- **Network**: SSH operations
- **Security**: Secrets management, encryption
- **Best Practices**: Error handling, testing, documentation

Key takeaways:
- Use Python for automation and infrastructure management
- Leverage AWS SDKs for cloud operations
- Implement proper error handling and logging
- Use configuration management for flexibility
- Write tests for reliability
- Follow best practices for maintainability

Each section includes:
- Code examples
- Real-world use cases
- Best practices
- Error handling
- Production-ready patterns

Use this guide to automate DevOps tasks and manage infrastructure with Python.

