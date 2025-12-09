# Ansible Master Tutorial - Complete Guide
## From Beginner to Expert: Automation Made Simple

---

## Table of Contents

1. [Ansible Fundamentals](#1-ansible-fundamentals)
2. [Installation & Setup](#2-installation--setup)
3. [Ad-Hoc Commands](#3-ad-hoc-commands)
4. [Understanding Playbooks](#4-understanding-playbooks)
5. [Inventory Management](#5-inventory-management)
6. [Variables & Facts](#6-variables--facts)
7. [Templates & Jinja2](#7-templates--jinja2)
8. [Handlers & Notifications](#8-handlers--notifications)
9. [Roles & Playbook Organization](#9-roles--playbook-organization)
10. [Conditionals & Loops](#10-conditionals--loops)
11. [Error Handling & Debugging](#11-error-handling--debugging)
12. [Ansible Vault](#12-ansible-vault)
13. [Advanced Topics](#13-advanced-topics)
14. [Best Practices](#14-best-practices)
15. [Real-World Examples](#15-real-world-examples)

---

## 1. Ansible Fundamentals

### 1.1 What is Ansible?

**Ansible** is an open-source automation tool for:
- Configuration management
- Application deployment
- Task automation
- Orchestration

**Key Characteristics:**
- **Agentless**: No software to install on managed nodes
- **SSH-based**: Uses SSH for communication
- **Idempotent**: Running multiple times produces same result
- **Declarative**: Describe desired state, not steps
- **Python-based**: Built on Python

### 1.2 How Ansible Works

```
┌─────────────────┐
│  Control Node   │  (Your machine with Ansible)
│  (Ansible)      │
└────────┬────────┘
         │ SSH
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼──┐ ┌───▼──┐ ┌───▼──┐ ┌───▼──┐
│Node 1│ │Node 2│ │Node 3│ │Node 4│
└──────┘ └──────┘ └──────┘ └──────┘
  (No agent needed - just SSH access)
```

**Components:**

- **Control Node**: Machine where Ansible is installed
- **Managed Nodes**: Servers you manage
- **Inventory**: List of managed nodes
- **Modules**: Units of work (copy, install, start, etc.)
- **Playbooks**: Automation scripts (YAML format)

### 1.3 Why Ansible Over Bash Scripts?

**Bash Scripts:**
```bash
#!/bin/bash
# Install Nginx
sudo apt-get update
sudo apt-get install -y nginx
sudo systemctl start nginx

# What if nginx is already installed?
# What if apt-get fails?
# What if service is already running?
```

**Ansible Playbook:**
```yaml
- name: Install and start Nginx
  hosts: web_servers
  tasks:
    - name: Install Nginx
      apt:
        name: nginx
        state: present
      become: yes

    - name: Start Nginx service
      systemd:
        name: nginx
        state: started
        enabled: yes
      become: yes
```

**Advantages:**
- ✅ **Idempotent**: Safe to run multiple times
- ✅ **Declarative**: Describe what you want, not how
- ✅ **Error Handling**: Built-in error handling
- ✅ **Parallel Execution**: Run on multiple hosts simultaneously
- ✅ **Readable**: YAML is more readable than bash

### 1.4 Ansible vs Other Tools

| Feature | Ansible | Puppet | Chef | SaltStack |
|---------|---------|--------|------|-----------|
| Agentless | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| Language | YAML | Ruby DSL | Ruby DSL | YAML/Python |
| Learning Curve | Easy | Medium | Medium | Medium |
| Push/Pull | Push | Pull | Pull | Both |

---

## 2. Installation & Setup

### 2.1 Installing Ansible

**Ubuntu/Debian:**

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y python3-pip sshpass

# Install Ansible
sudo apt install -y ansible

# Or via pip (latest version)
sudo pip3 install ansible

# Verify installation
ansible --version
```

**RHEL/CentOS:**

```bash
# Install EPEL repository
sudo yum install -y epel-release

# Install Ansible
sudo yum install -y ansible

# Or via pip
sudo pip3 install ansible

# Verify
ansible --version
```

**macOS:**

```bash
# Using Homebrew
brew install ansible

# Verify
ansible --version
```

**Python Virtual Environment (Recommended):**

```bash
# Create virtual environment
python3 -m venv ansible-env
source ansible-env/bin/activate  # Linux/macOS
# or
ansible-env\Scripts\activate  # Windows

# Install Ansible
pip install ansible

# Verify
ansible --version
```

### 2.2 Initial Setup

**Create Ansible Directory Structure:**

```bash
mkdir -p ansible-project/{inventory,group_vars,host_vars,roles,playbooks}
cd ansible-project
```

**Directory Structure:**

```
ansible-project/
├── inventory/
│   ├── hosts.ini
│   └── production.ini
├── group_vars/
│   ├── all.yml
│   ├── web_servers.yml
│   └── db_servers.yml
├── host_vars/
│   └── web1.example.com.yml
├── roles/
│   └── common/
├── playbooks/
│   ├── site.yml
│   └── deploy.yml
├── ansible.cfg
└── requirements.yml
```

**Ansible Configuration (ansible.cfg):**

```ini
[defaults]
# Inventory file location
inventory = inventory/hosts.ini

# Remote user
remote_user = ansible

# SSH key file
private_key_file = ~/.ssh/id_rsa

# Host key checking (disable for initial setup)
host_key_checking = False

# SSH timeout
timeout = 10

# Retry files
retry_files_enabled = False

# Display skipped hosts
display_skipped_hosts = True

# Output formatting
stdout_callback = yaml

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
```

### 2.3 SSH Setup

**Generate SSH Key (if not exists):**

```bash
ssh-keygen -t rsa -b 4096 -C "ansible@example.com"
```

**Copy SSH Key to Managed Nodes:**

```bash
# Method 1: ssh-copy-id
ssh-copy-id user@remote-host

# Method 2: Manual
cat ~/.ssh/id_rsa.pub | ssh user@remote-host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Method 3: Using Ansible (for first-time setup)
ansible all -m authorized_key -a "user=ansible key='{{ lookup('file', '~/.ssh/id_rsa.pub') }}'" -k
```

**Test SSH Connection:**

```bash
# Test connectivity
ssh ansible@remote-host

# Test with Ansible
ansible all -m ping
```

---

## 3. Ad-Hoc Commands

### 3.1 Understanding Ad-Hoc Commands

**Ad-hoc commands** are one-liners that perform quick tasks without writing playbooks.

**Syntax:**
```bash
ansible <pattern> -m <module> -a "<module_arguments>"
```

**Components:**
- `<pattern>`: Host or group from inventory
- `-m <module>`: Module to use
- `-a "<arguments>"`: Module arguments

### 3.2 Basic Ad-Hoc Commands

**Ping Test:**

```bash
# Ping all hosts
ansible all -m ping

# Ping specific group
ansible web_servers -m ping

# Ping specific host
ansible web1.example.com -m ping

# Ping with custom user
ansible all -m ping -u admin
```

**Command Execution:**

```bash
# Run shell command
ansible all -m shell -a "uptime"

# Run command module (safer, no shell)
ansible all -m command -a "uptime"

# Run with sudo
ansible all -m command -a "whoami" --become

# Run as specific user
ansible all -m command -a "whoami" --become --become-user=postgres
```

**File Operations:**

```bash
# Copy file
ansible all -m copy -a "src=/local/file.txt dest=/remote/file.txt"

# Fetch file from remote
ansible all -m fetch -a "src=/remote/file.txt dest=/local/backup/"

# Create directory
ansible all -m file -a "path=/tmp/my_dir state=directory"

# Delete file
ansible all -m file -a "path=/tmp/file.txt state=absent"
```

**Package Management:**

```bash
# Install package (apt)
ansible web_servers -m apt -a "name=nginx state=present" --become

# Install package (yum)
ansible db_servers -m yum -a "name=mysql-server state=present" --become

# Update all packages
ansible all -m apt -a "upgrade=dist update_cache=yes" --become

# Remove package
ansible all -m apt -a "name=apache2 state=absent" --become
```

**Service Management:**

```bash
# Start service
ansible web_servers -m systemd -a "name=nginx state=started" --become

# Stop service
ansible web_servers -m systemd -a "name=nginx state=stopped" --become

# Restart service
ansible web_servers -m systemd -a "name=nginx state=restarted" --become

# Enable service on boot
ansible web_servers -m systemd -a "name=nginx enabled=yes state=started" --become
```

**User Management:**

```bash
# Create user
ansible all -m user -a "name=john comment='John Doe' uid=1040" --become

# Add user to group
ansible all -m user -a "name=john groups=wheel append=yes" --become

# Delete user
ansible all -m user -a "name=john state=absent remove=yes" --become

# Create user with SSH key
ansible all -m user -a "name=john" --become
ansible all -m authorized_key -a "user=john key='{{ lookup('file', '/path/to/key.pub') }}'" --become
```

### 3.3 Useful Ad-Hoc Commands for System Administration

**Gathering Information:**

```bash
# Get system facts
ansible all -m setup

# Get specific fact
ansible all -m setup -a "filter=ansible_distribution*"

# Get IP addresses
ansible all -m setup -a "filter=ansible_default_ipv4"

# Get hostname
ansible all -m setup -a "filter=ansible_hostname"
```

**Disk Space:**

```bash
# Check disk usage
ansible all -m shell -a "df -h"

# Check inode usage
ansible all -m shell -a "df -i"
```

**Process Management:**

```bash
# List processes
ansible all -m shell -a "ps aux | grep nginx"

# Kill process
ansible all -m shell -a "killall nginx" --become
```

**Network Operations:**

```bash
# Test connectivity
ansible all -m wait_for -a "host=google.com port=80"

# Check listening ports
ansible all -m shell -a "ss -tuln"
```

### 3.4 Parallel Execution

```bash
# Limit concurrent connections
ansible all -m ping --forks 5

# Serial execution (one at a time)
ansible all -m ping --serial 1

# Step-by-step execution
ansible all -m ping --step
```

---

## 4. Understanding Playbooks

### 4.1 What is a Playbook?

A **playbook** is a YAML file containing a list of plays. Each play defines tasks to be executed on hosts.

**Simple Playbook Example:**

```yaml
---
- name: Install and configure Nginx
  hosts: web_servers
  become: yes
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Start Nginx service
      systemd:
        name: nginx
        state: started
        enabled: yes

    - name: Copy index.html
      copy:
        src: files/index.html
        dest: /var/www/html/index.html
        owner: www-data
        group: www-data
        mode: '0644'
```

### 4.2 Playbook Structure

**Basic Structure:**

```yaml
---
- name: Play name
  hosts: target_hosts
  become: yes  # Use sudo
  vars:
    variable_name: value
  tasks:
    - name: Task description
      module_name:
        parameter: value
```

**Playbook Components:**

1. **name**: Description of the play
2. **hosts**: Target hosts or groups
3. **become**: Whether to use privilege escalation
4. **vars**: Variables for the play
5. **tasks**: List of tasks to execute
6. **handlers**: Tasks that run on notification
7. **pre_tasks**: Tasks before main tasks
8. **post_tasks**: Tasks after main tasks

### 4.3 Your First Playbook

**Create a simple playbook:**

```yaml
# playbooks/first-playbook.yml
---
- name: My First Ansible Playbook
  hosts: localhost
  connection: local
  tasks:
    - name: Print hello message
      debug:
        msg: "Hello from Ansible!"

    - name: Get system date
      command: date
      register: date_output

    - name: Display date
      debug:
        var: date_output.stdout
```

**Run the playbook:**

```bash
ansible-playbook playbooks/first-playbook.yml
```

### 4.4 Common Modules

**File Management:**

```yaml
- name: Copy file
  copy:
    src: files/config.conf
    dest: /etc/config.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes

- name: Create directory
  file:
    path: /var/www/app
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'

- name: Create symlink
  file:
    src: /etc/nginx/sites-available/example
    dest: /etc/nginx/sites-enabled/example
    state: link

- name: Delete file
  file:
    path: /tmp/old-file.txt
    state: absent
```

**Package Management:**

```yaml
# APT (Debian/Ubuntu)
- name: Install packages
  apt:
    name:
      - nginx
      - python3
      - git
    state: present
    update_cache: yes

# YUM (RHEL/CentOS)
- name: Install packages
  yum:
    name:
      - nginx
      - python3
      - git
    state: present

# DNF (Fedora/newer RHEL)
- name: Install packages
  dnf:
    name:
      - nginx
      - python3
    state: present
```

**Service Management:**

```yaml
- name: Start and enable service
  systemd:
    name: nginx
    state: started
    enabled: yes
    daemon_reload: yes

- name: Restart service
  systemd:
    name: nginx
    state: restarted

- name: Stop service
  systemd:
    name: nginx
    state: stopped
```

**Command Execution:**

```yaml
# Shell command (with shell features)
- name: Run shell command
  shell: |
    cd /tmp
    ls -la
    echo "Done"
  args:
    chdir: /tmp

# Command module (no shell)
- name: Run command
  command: /usr/bin/script.sh arg1 arg2

# Raw command (bypasses modules)
- name: Raw command
  raw: /bin/script.sh
```

---

## 5. Inventory Management

### 5.1 Inventory Basics

**Inventory file** defines the hosts Ansible manages.

**Simple Inventory (INI format):**

```ini
# inventory/hosts.ini
[web_servers]
web1.example.com
web2.example.com ansible_host=192.168.1.10
web3.example.com ansible_port=2222

[db_servers]
db1.example.com
db2.example.com

[all:vars]
ansible_user=ansible
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

**YAML Format:**

```yaml
# inventory/hosts.yml
all:
  children:
    web_servers:
      hosts:
        web1.example.com:
          ansible_host: 192.168.1.11
          ansible_port: 22
        web2.example.com:
          ansible_host: 192.168.1.12
      vars:
        http_port: 80

    db_servers:
      hosts:
        db1.example.com:
          ansible_host: 192.168.1.21
        db2.example.com:
          ansible_host: 192.168.1.22
      vars:
        db_port: 3306

  vars:
    ansible_user: ansible
    ansible_python_interpreter: /usr/bin/python3
```

### 5.2 Inventory Patterns

**Host Patterns:**

```bash
# All hosts
ansible all -m ping

# Specific group
ansible web_servers -m ping

# Specific host
ansible web1.example.com -m ping

# Multiple groups
ansible web_servers:db_servers -m ping

# Exclude group
ansible all:!db_servers -m ping

# Intersection
ansible web_servers:&db_servers -m ping

# Wildcard
ansible web*.example.com -m ping

# Range
ansible web[1:3].example.com -m ping
```

**Advanced Patterns:**

```bash
# First 3 hosts in group
ansible web_servers[0:2] -m ping

# Specific host in group
ansible web_servers[0] -m ping

# All hosts matching pattern
ansible "*.example.com" -m ping
```

### 5.3 Dynamic Inventory

**AWS EC2 Dynamic Inventory:**

```bash
# Install AWS plugin
pip install boto3

# Configure inventory
# inventory/ec2.ini
[ec2]
regions = us-east-1,us-west-2

# Use dynamic inventory
ansible-inventory -i inventory/ec2.ini --list
```

**Docker Dynamic Inventory:**

```yaml
# inventory/docker.yml
plugin: docker_containers
containers:
  - name: web1
    ansible_host: 172.17.0.2
    groups:
      - web_servers
```

### 5.4 Inventory Variables

**Group Variables:**

```yaml
# group_vars/web_servers.yml
http_port: 80
https_port: 443
nginx_version: "1.21.0"
deployment_user: deploy
```

**Host Variables:**

```yaml
# host_vars/web1.example.com.yml
ansible_host: 192.168.1.11
http_port: 8080
custom_config: "specific_value"
```

**All Variables:**

```yaml
# group_vars/all.yml
ansible_user: ansible
timezone: UTC
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org
```

---

## 6. Variables & Facts

### 6.1 Variable Types

**1. Playbook Variables:**

```yaml
---
- name: Using variables
  hosts: all
  vars:
    app_name: myapp
    app_version: "1.0.0"
    ports:
      - 80
      - 443
  tasks:
    - name: Display variable
      debug:
        msg: "App name is {{ app_name }}"
```

**2. Inventory Variables:**

```ini
# In inventory file
[web_servers]
web1.example.com app_port=8080
web2.example.com app_port=8081

[web_servers:vars]
http_port=80
```

**3. Registered Variables:**

```yaml
- name: Get system info
  command: uname -a
  register: system_info

- name: Display system info
  debug:
    var: system_info.stdout
```

**4. Facts (Gathered Variables):**

```yaml
- name: Display OS info
  debug:
    msg: "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"

- name: Display IP address
  debug:
    msg: "IP: {{ ansible_default_ipv4.address }}"
```

### 6.2 Using Variables

**Variable Syntax:**

```yaml
# Simple variable
{{ variable_name }}

# With default
{{ variable_name | default('default_value') }}

# Nested variable
{{ nested_variable.key.subkey }}

# List/Array access
{{ list_variable[0] }}

# Dictionary access
{{ dict_variable['key'] }}
```

**Variable Precedence:**

```
1. Command line variables (-e)
2. Play vars
3. Play vars_prompt
4. Play vars_files
5. Host facts
6. Registered vars
7. Set_facts
8. Role vars
9. Block vars
10. Task vars
11. Include vars
12. Role defaults
```

### 6.3 Facts (System Information)

**Gathering Facts:**

```yaml
---
- name: Gather facts
  hosts: all
  gather_facts: yes  # Default is yes
  
  tasks:
    - name: Display all facts
      debug:
        var: ansible_facts

    - name: Display specific facts
      debug:
        msg: |
          Hostname: {{ ansible_hostname }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          IP: {{ ansible_default_ipv4.address }}
          Memory: {{ ansible_memtotal_mb }}MB
```

**Useful Facts:**

```yaml
# Network
ansible_default_ipv4.address
ansible_default_ipv4.gateway
ansible_all_ipv4_addresses

# System
ansible_hostname
ansible_fqdn
ansible_domain

# OS
ansible_distribution
ansible_distribution_version
ansible_os_family
ansible_architecture

# Hardware
ansible_processor_vcpus
ansible_memtotal_mb
ansible_swaptotal_mb
ansible_devices

# Python
ansible_python_version
ansible_python_interpreter
```

**Custom Facts (fact.d):**

```bash
# On managed node: /etc/ansible/facts.d/custom.fact
[general]
app_name=myapp
app_version=1.0.0

# Access in playbook
{{ ansible_local.custom.general.app_name }}
```

### 6.4 Set Facts

**Setting Facts in Playbook:**

```yaml
- name: Set custom fact
  set_fact:
    deployment_timestamp: "{{ ansible_date_time.iso8601 }}"
    app_env: "{{ 'production' if inventory_hostname in groups['prod'] else 'development' }}"

- name: Use set fact
  debug:
    msg: "Deployed at {{ deployment_timestamp }}"
```

**Conditional Facts:**

```yaml
- name: Set fact based on condition
  set_fact:
    max_workers: "{{ 10 if ansible_processor_vcpus > 4 else 5 }}"
```

---

## 7. Templates & Jinja2

### 7.1 What are Templates?

**Templates** are files with variables that get substituted with actual values.

**Template File (Nginx config):**

```nginx
# templates/nginx.conf.j2
server {
    listen {{ http_port }};
    server_name {{ server_name }};

    root {{ web_root }};
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    {% if enable_ssl %}
    listen {{ https_port }} ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};
    {% endif %}
}
```

**Using Template:**

```yaml
- name: Configure Nginx
  template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/sites-available/{{ server_name }}
    owner: root
    group: root
    mode: '0644'
  notify: restart nginx
```

### 7.2 Jinja2 Basics

**Variables:**

```jinja2
{{ variable_name }}
{{ variable.key }}
{{ variable['key'] }}
```

**Filters:**

```jinja2
# String filters
{{ name | upper }}
{{ name | lower }}
{{ name | capitalize }}
{{ path | basename }}
{{ path | dirname }}

# List filters
{{ list | join(',') }}
{{ list | first }}
{{ list | last }}
{{ list | length }}

# Default values
{{ variable | default('default_value') }}
{{ variable | default('default', true) }}

# JSON
{{ data | to_json }}
{{ data | to_nice_json }}

# YAML
{{ data | to_yaml }}
{{ data | to_nice_yaml }}
```

**Conditionals:**

```jinja2
{% if condition %}
  content
{% elif other_condition %}
  content
{% else %}
  content
{% endif %}
```

**Loops:**

```jinja2
{% for item in list %}
  {{ item }}
{% endfor %}

{% for key, value in dict.items() %}
  {{ key }}: {{ value }}
{% endfor %}
```

### 7.3 Template Examples

**Nginx Configuration Template:**

```nginx
# templates/nginx-site.conf.j2
{% for server in nginx_servers %}
server {
    listen {{ server.port }};
    server_name {{ server.name }};

    {% if server.ssl %}
    listen {{ server.ssl_port }} ssl;
    ssl_certificate {{ server.ssl_cert }};
    ssl_certificate_key {{ server.ssl_key }};
    {% endif %}

    root {{ server.root }};
    index index.html;

    {% if server.proxy_pass %}
    location / {
        proxy_pass http://{{ server.proxy_pass }};
    }
    {% else %}
    location / {
        try_files $uri $uri/ =404;
    }
    {% endif %}
}
{% endfor %}
```

**Variables File:**

```yaml
# group_vars/web_servers.yml
nginx_servers:
  - name: example.com
    port: 80
    ssl: true
    ssl_port: 443
    ssl_cert: /etc/ssl/certs/example.com.crt
    ssl_key: /etc/ssl/private/example.com.key
    root: /var/www/example
    proxy_pass: ""
```

**Systemd Service Template:**

```ini
# templates/myapp.service.j2
[Unit]
Description={{ app_description }}
After=network.target

[Service]
Type=simple
User={{ app_user }}
WorkingDirectory={{ app_dir }}
ExecStart={{ app_executable }}
Restart=always
RestartSec=10

Environment="APP_ENV={{ app_env }}"
Environment="PORT={{ app_port }}"

[Install]
WantedBy=multi-user.target
```

---

## 8. Handlers & Notifications

### 8.1 What are Handlers?

**Handlers** are tasks that run only when notified by other tasks.

**Why Handlers?**
- Restart services only when configuration changes
- Avoid unnecessary service restarts
- Run tasks at the end of play

**Basic Example:**

```yaml
---
- name: Configure Nginx
  hosts: web_servers
  become: yes
  
  tasks:
    - name: Copy Nginx config
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: restart nginx

    - name: Copy site config
      template:
        src: templates/site.conf.j2
        dest: /etc/nginx/sites-available/default
      notify: restart nginx

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted
```

**Note:** Handler runs once even if notified multiple times.

### 8.2 Handler Best Practices

**Multiple Handlers:**

```yaml
tasks:
  - name: Update config
    template:
      src: config.j2
      dest: /etc/app/config.conf
    notify:
      - restart app
      - reload config

handlers:
  - name: restart app
    systemd:
      name: myapp
      state: restarted

  - name: reload config
    command: /usr/bin/appctl reload
```

**Flush Handlers:**

```yaml
tasks:
  - name: Update config
    template:
      src: config.j2
      dest: /etc/app/config.conf
    notify: restart app

  - name: Force handler execution
    meta: flush_handlers

  - name: Continue with other tasks
    command: echo "Config updated"
```

**Handler Conditions:**

```yaml
handlers:
  - name: restart app
    systemd:
      name: myapp
      state: restarted
    when: app_restart_enabled | default(true)
```

---

## 9. Roles & Playbook Organization

### 9.1 What are Roles?

**Roles** organize playbooks into reusable components.

**Role Structure:**

```
roles/
└── nginx/
    ├── defaults/
    │   └── main.yml          # Default variables
    ├── vars/
    │   └── main.yml          # Role variables
    ├── tasks/
    │   └── main.yml          # Main tasks
    ├── handlers/
    │   └── main.yml          # Handlers
    ├── templates/
    │   └── nginx.conf.j2     # Templates
    ├── files/
    │   └── index.html        # Static files
    ├── meta/
    │   └── main.yml          # Dependencies
    └── README.md             # Documentation
```

### 9.2 Creating a Role

**Create Role Structure:**

```bash
ansible-galaxy init roles/nginx
```

**Role Tasks (roles/nginx/tasks/main.yml):**

```yaml
---
- name: Install Nginx
  apt:
    name: nginx
    state: present
    update_cache: yes
  become: yes

- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx
  become: yes

- name: Start and enable Nginx
  systemd:
    name: nginx
    state: started
    enabled: yes
  become: yes
```

**Role Variables (roles/nginx/defaults/main.yml):**

```yaml
---
nginx_user: www-data
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_gzip: yes
nginx_http_port: 80
```

**Role Handlers (roles/nginx/handlers/main.yml):**

```yaml
---
- name: restart nginx
  systemd:
    name: nginx
    state: restarted
  become: yes
```

**Using the Role:**

```yaml
---
- name: Setup web servers
  hosts: web_servers
  become: yes
  roles:
    - role: nginx
      vars:
        nginx_http_port: 8080
```

### 9.3 Role Dependencies

**Define Dependencies (roles/nginx/meta/main.yml):**

```yaml
---
dependencies:
  - role: common
  - role: firewall
    vars:
      allow_port_80: yes
      allow_port_443: yes
```

### 9.4 Ansible Galaxy

**Search Roles:**

```bash
ansible-galaxy search nginx
ansible-galaxy search mysql --platforms Ubuntu
```

**Install Role:**

```bash
# Install from Galaxy
ansible-galaxy install geerlingguy.nginx

# Install from requirements
ansible-galaxy install -r requirements.yml
```

**Requirements File (requirements.yml):**

```yaml
---
# From Galaxy
- name: geerlingguy.nginx
  version: 3.1.0

- name: geerlingguy.mysql
  version: 3.3.0

# From Git
- name: custom.role
  src: https://github.com/user/ansible-role-custom.git
  version: master

# From local path
- name: local.role
  src: /path/to/local/role
```

---

## 10. Conditionals & Loops

### 10.1 Conditionals

**Basic Conditional:**

```yaml
- name: Install package on Debian
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"
  become: yes

- name: Install package on RedHat
  yum:
    name: nginx
    state: present
  when: ansible_os_family == "RedHat"
  become: yes
```

**Multiple Conditions:**

```yaml
- name: Task with multiple conditions
  command: /bin/something
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "20.04"
    - inventory_hostname in groups['web_servers']
```

**Conditional with OR:**

```yaml
- name: Task with OR condition
  command: /bin/something
  when: 
    - ansible_os_family == "Debian" or ansible_os_family == "RedHat"
```

**Conditional with Variables:**

```yaml
- name: Conditional with variable
  template:
    src: config.j2
    dest: /etc/app/config.conf
  when: app_config_enabled | default(true)
```

### 10.2 Loops

**Loop with Items:**

```yaml
- name: Install multiple packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - mysql-server
    - python3
  become: yes
```

**Loop with List Variable:**

```yaml
vars:
  packages:
    - nginx
    - mysql-server
    - python3

tasks:
  - name: Install packages
    apt:
      name: "{{ item }}"
      state: present
    loop: "{{ packages }}"
    become: yes
```

**Loop with Dictionary:**

```yaml
vars:
  users:
    - name: john
      uid: 1001
      shell: /bin/bash
    - name: jane
      uid: 1002
      shell: /bin/zsh

tasks:
  - name: Create users
    user:
      name: "{{ item.name }}"
      uid: "{{ item.uid }}"
      shell: "{{ item.shell }}"
    loop: "{{ users }}"
    become: yes
```

**Loop with Index:**

```yaml
- name: Create files with index
  copy:
    content: "File {{ item.0 }}: {{ item.1 }}"
    dest: "/tmp/file{{ item.0 }}.txt"
  loop: "{{ ['file1', 'file2', 'file3'] | enumerate }}"
  loop_control:
    label: "{{ item.1 }}"
```

**Loop Control:**

```yaml
- name: Process items
  command: "/bin/process {{ item }}"
  loop: "{{ items }}"
  loop_control:
    label: "{{ item.name | default(item) }}"
    pause: 1  # Pause 1 second between items
```

**Until Loops:**

```yaml
- name: Wait for service to be ready
  uri:
    url: http://localhost:8080/health
    status_code: 200
  register: result
  until: result.status == 200
  retries: 30
  delay: 2
```

---

## 11. Error Handling & Debugging

### 11.1 Error Handling

**Ignore Errors:**

```yaml
- name: Try command that might fail
  command: /bin/risky-command
  ignore_errors: yes
  register: result

- name: Check if failed
  debug:
    msg: "Command failed but continuing"
  when: result.failed
```

**Failed When:**

```yaml
- name: Run script
  script: /path/to/script.sh
  register: result

- name: Fail if script returns error code
  fail:
    msg: "Script failed with code {{ result.rc }}"
  when: result.rc != 0
```

**Rescue Blocks:**

```yaml
- name: Try block
  block:
    - name: Attempt risky operation
      command: /bin/risky-command
  rescue:
    - name: Handle failure
      debug:
        msg: "Operation failed, handling gracefully"
    - name: Cleanup
      file:
        path: /tmp/temp-file
        state: absent
  always:
    - name: Always run
      debug:
        msg: "This always runs"
```

### 11.2 Debugging

**Debug Module:**

```yaml
- name: Display variable
  debug:
    var: variable_name

- name: Display message
  debug:
    msg: "Current value: {{ variable_name }}"

- name: Display all variables
  debug:
    var: vars
```

**Verbose Output:**

```bash
# Run with verbose output
ansible-playbook playbook.yml -v    # Level 1
ansible-playbook playbook.yml -vv   # Level 2
ansible-playbook playbook.yml -vvv  # Level 3
ansible-playbook playbook.yml -vvvv # Level 4
```

**Check Mode (Dry Run):**

```bash
# See what would change without making changes
ansible-playbook playbook.yml --check

# Check with diff
ansible-playbook playbook.yml --check --diff
```

**Syntax Check:**

```bash
# Check playbook syntax
ansible-playbook playbook.yml --syntax-check

# Validate configuration
ansible-config dump --only-changed
```

**Step-by-Step Execution:**

```bash
# Execute one task at a time
ansible-playbook playbook.yml --step
```

### 11.3 Testing Playbooks

**Testing with Molecule (Advanced):**

```bash
# Install Molecule
pip install molecule molecule-docker

# Initialize role with Molecule
molecule init role --driver-name docker myrole
```

---

## 12. Ansible Vault

### 12.1 What is Ansible Vault?

**Ansible Vault** encrypts sensitive data (passwords, keys, etc.).

**Encrypt File:**

```bash
# Encrypt file
ansible-vault create secret.yml

# Encrypt existing file
ansible-vault encrypt secret.yml

# View encrypted file
ansible-vault view secret.yml

# Edit encrypted file
ansible-vault edit secret.yml

# Decrypt file
ansible-vault decrypt secret.yml
```

### 12.2 Using Vault

**Vault File:**

```yaml
# group_vars/production/vault.yml (encrypted)
---
db_password: "secretpassword123"
api_key: "apikey123456"
aws_access_key: "AKIAIOSFODNN7EXAMPLE"
aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Using in Playbook:**

```yaml
---
- name: Deploy application
  hosts: app_servers
  vars_files:
    - group_vars/production/vault.yml
  tasks:
    - name: Configure database
      template:
        src: db-config.j2
        dest: /etc/app/db.conf
      vars:
        db_password: "{{ db_password }}"  # From vault
```

**Running with Vault:**

```bash
# Prompt for password
ansible-playbook playbook.yml --ask-vault-pass

# Use password file
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass.txt

# Multiple vault files
ansible-playbook playbook.yml --ask-vault-pass --vault-password-file prod_vault_pass.txt
```

**Vault ID (Multiple Vaults):**

```bash
# Encrypt with vault ID
ansible-vault encrypt --vault-id dev@prompt dev-secrets.yml
ansible-vault encrypt --vault-id prod@~/.prod_vault_pass prod-secrets.yml

# Use multiple vaults
ansible-playbook playbook.yml --vault-id dev@prompt --vault-id prod@~/.prod_vault_pass
```

---

## 13. Advanced Topics

### 13.1 Async Tasks

**Long-Running Tasks:**

```yaml
- name: Long-running task
  command: /bin/long-script.sh
  async: 3600  # Maximum time in seconds
  poll: 10     # Poll every 10 seconds
  register: long_task

- name: Check task status
  async_status:
    jid: "{{ long_task.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 30
  delay: 10

- name: Fire and forget
  command: /bin/background-task.sh
  async: 3600
  poll: 0  # Don't wait
```

### 13.2 Delegation

**Task Delegation:**

```yaml
- name: Deploy to all servers
  hosts: all
  tasks:
    - name: Register in load balancer
      uri:
        url: http://lb.example.com/register/{{ inventory_hostname }}
      delegate_to: localhost

    - name: Deploy application
      copy:
        src: app.tar.gz
        dest: /opt/app/

    - name: Deregister from load balancer
      uri:
        url: http://lb.example.com/deregister/{{ inventory_hostname }}
      delegate_to: localhost
```

### 13.3 Local Actions

**Run Tasks Locally:**

```yaml
- name: Run on localhost
  command: /bin/something
  delegate_to: localhost
  connection: local

# Or use local_action
- name: Create local file
  local_action:
    module: copy
    src: /local/file.txt
    dest: /remote/file.txt
```

### 13.4 Parallel Execution

**Forks:**

```yaml
# In ansible.cfg
[defaults]
forks = 10

# Or command line
ansible-playbook playbook.yml -f 10
```

**Serial Execution:**

```yaml
---
- name: Rolling update
  hosts: web_servers
  serial: 2  # Update 2 at a time
  tasks:
    - name: Update application
      copy:
        src: app.tar.gz
        dest: /opt/app/
```

**Throttle:**

```yaml
- name: Rate-limited task
  command: /bin/api-call.sh
  throttle: 5  # Max 5 concurrent executions
```

### 13.5 Including and Importing

**Include Playbook:**

```yaml
---
# playbooks/site.yml
- include: deploy.yml
- include: configure.yml
```

**Include Tasks:**

```yaml
---
- name: Setup server
  hosts: all
  tasks:
    - include: tasks/common.yml
    - include: tasks/security.yml
      vars:
        firewall_enabled: yes
```

**Import Playbook:**

```yaml
---
# playbooks/site.yml
- import_playbook: deploy.yml
- import_playbook: configure.yml
```

**Import Tasks (Static):**

```yaml
---
- name: Setup
  hosts: all
  tasks:
    - import_tasks: tasks/common.yml
    - import_tasks: tasks/app.yml
      when: app_installed | default(false)
```

---

## 14. Best Practices

### 14.1 Playbook Best Practices

1. **Use Roles** - Organize reusable components
2. **Version Control** - Keep playbooks in Git
3. **Idempotency** - Always make playbooks idempotent
4. **Naming** - Use descriptive names
5. **Comments** - Document complex logic
6. **DRY** - Don't Repeat Yourself
7. **Testing** - Test playbooks before production

### 14.2 Variable Best Practices

1. **Defaults** - Use role defaults
2. **Naming** - Consistent naming convention
3. **Scoping** - Proper variable scoping
4. **Secrets** - Use Ansible Vault
5. **Documentation** - Document variables

### 14.3 Security Best Practices

1. **SSH Keys** - Use SSH keys, not passwords
2. **Vault** - Encrypt sensitive data
3. **Become** - Use privilege escalation carefully
4. **Validation** - Validate inputs
5. **Least Privilege** - Use minimal required permissions

### 14.4 Performance Best Practices

1. **Forks** - Adjust fork count
2. **Gather Facts** - Disable when not needed
3. **Async** - Use async for long tasks
4. **Tags** - Use tags for selective execution
5. **Caching** - Cache facts when possible

---

## 15. Real-World Examples

### 15.1 Web Server Setup

```yaml
# playbooks/webserver.yml
---
- name: Setup web server
  hosts: web_servers
  become: yes
  vars:
    nginx_user: www-data
    nginx_worker_processes: auto
    nginx_worker_connections: 1024
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install Nginx
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Nginx
      yum:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat"

    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        backup: yes
      notify: restart nginx

    - name: Copy index.html
      copy:
        src: files/index.html
        dest: /var/www/html/index.html
        owner: www-data
        group: www-data
        mode: '0644'

    - name: Start and enable Nginx
      systemd:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted
```

### 15.2 Database Setup

```yaml
# playbooks/database.yml
---
- name: Setup MySQL database
  hosts: db_servers
  become: yes
  vars:
    mysql_root_password: "{{ vault_mysql_root_password }}"
    mysql_databases:
      - name: appdb
        encoding: utf8mb4
    mysql_users:
      - name: appuser
        password: "{{ vault_db_password }}"
        priv: "appdb.*:ALL"
  
  tasks:
    - name: Install MySQL
      apt:
        name: mysql-server
        state: present
      when: ansible_os_family == "Debian"

    - name: Start MySQL
      systemd:
        name: mysql
        state: started
        enabled: yes

    - name: Create databases
      mysql_db:
        name: "{{ item.name }}"
        encoding: "{{ item.encoding }}"
        state: present
      loop: "{{ mysql_databases }}"

    - name: Create users
      mysql_user:
        name: "{{ item.name }}"
        password: "{{ item.password }}"
        priv: "{{ item.priv }}"
        state: present
      loop: "{{ mysql_users }}"
```

### 15.3 Application Deployment

```yaml
# playbooks/deploy-app.yml
---
- name: Deploy application
  hosts: app_servers
  become: yes
  vars:
    app_name: myapp
    app_version: "1.0.0"
    app_user: appuser
    app_dir: /opt/myapp
  
  tasks:
    - name: Create application user
      user:
        name: "{{ app_user }}"
        system: yes
        shell: /bin/bash

    - name: Create application directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
        mode: '0755'

    - name: Copy application files
      unarchive:
        src: "{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "{{ app_dir }}"
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
        remote_src: no

    - name: Install dependencies
      pip:
        requirements: "{{ app_dir }}/requirements.txt"
        virtualenv: "{{ app_dir }}/venv"
      become_user: "{{ app_user }}"

    - name: Create systemd service
      template:
        src: templates/myapp.service.j2
        dest: /etc/systemd/system/{{ app_name }}.service
      notify: reload systemd

    - name: Start application
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
        daemon_reload: yes

  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
```

### 15.4 Complete Infrastructure Setup

```yaml
# playbooks/site.yml
---
- name: Setup infrastructure
  hosts: all
  become: yes
  roles:
    - common
    - security
    - monitoring

- name: Setup database servers
  hosts: db_servers
  become: yes
  roles:
    - mysql
    - backup

- name: Setup web servers
  hosts: web_servers
  become: yes
  roles:
    - nginx
    - ssl
    - app

- name: Setup load balancer
  hosts: lb_servers
  become: yes
  roles:
    - haproxy
    - keepalived
```

---

## Conclusion

### Key Takeaways:

1. **Ansible is Agentless** - No software on managed nodes
2. **Idempotent** - Safe to run multiple times
3. **YAML-based** - Human-readable playbooks
4. **Modular** - Use roles for reusability
5. **Powerful** - Handles complex automation

### Essential Concepts:

- **Inventory**: Define your hosts
- **Playbooks**: Automation scripts
- **Modules**: Units of work
- **Roles**: Reusable components
- **Variables**: Configuration data
- **Templates**: Dynamic files
- **Handlers**: Conditional tasks

### Next Steps:

1. Practice with ad-hoc commands
2. Write simple playbooks
3. Create your first role
4. Explore Ansible Galaxy
5. Build complex automation

---

*Ansible Master Tutorial - Complete Guide*
*From Beginner to Expert: Automation Made Simple*
*Last Updated: 2024*

