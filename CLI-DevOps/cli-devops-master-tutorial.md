# Master-Level CLI for DevOps - Complete Tutorial
## Command Line Interface Mastery for DevOps Engineers

---

## Table of Contents

1. [Introduction to CLI in DevOps](#1-introduction-to-cli-in-devops)
2. [Shell Fundamentals](#2-shell-fundamentals)
3. [Essential Linux/Unix Commands](#3-essential-linuxunix-commands)
4. [Text Processing and Manipulation](#4-text-processing-and-manipulation)
5. [Process and System Management](#5-process-and-system-management)
6. [Network Operations](#6-network-operations)
7. [File System Operations](#7-file-system-operations)
8. [Package Management](#8-package-management)
9. [Docker CLI Mastery](#9-docker-cli-mastery)
10. [Kubernetes CLI (kubectl)](#10-kubernetes-cli-kubectl)
11. [Cloud CLI Tools](#11-cloud-cli-tools)
12. [Infrastructure as Code CLI](#12-infrastructure-as-code-cli)
13. [CI/CD CLI Tools](#13-cicd-cli-tools)
14. [Monitoring and Logging CLI](#14-monitoring-and-logging-cli)
15. [Security CLI Tools](#15-security-cli-tools)
16. [Advanced Shell Scripting](#16-advanced-shell-scripting)
17. [Performance Optimization](#17-performance-optimization)
18. [Troubleshooting and Debugging](#18-troubleshooting-and-debugging)
19. [Automation and Workflows](#19-automation-and-workflows)
20. [Best Practices and Tips](#20-best-practices-and-tips)

---

## 1. Introduction to CLI in DevOps

### Why CLI is Essential in DevOps

The Command Line Interface (CLI) is the backbone of DevOps operations:

- **Automation**: Scriptable and repeatable operations
- **Speed**: Faster than GUI for experienced users
- **Remote Access**: Essential for server management
- **CI/CD Integration**: All pipelines run via CLI
- **Resource Efficiency**: Lower overhead than GUI tools
- **Universal**: Works across all platforms and environments

### CLI Tools Ecosystem

```
┌─────────────────────────────────────────┐
│         DevOps CLI Ecosystem            │
├─────────────────────────────────────────┤
│  • Shell: bash, zsh, fish, PowerShell  │
│  • Containers: docker, podman, crictl   │
│  • Orchestration: kubectl, helm, k9s   │
│  • Cloud: aws, az, gcloud, terraform   │
│  • CI/CD: git, jenkins-cli, gh, glab   │
│  • Monitoring: prometheus, grafana-cli │
│  • Security: vault, trivy, snyk        │
│  • Networking: curl, wget, nmap, tcpdump│
└─────────────────────────────────────────┘
```

### Prerequisites

- Basic understanding of Linux/Unix systems
- Familiarity with terminal usage
- Understanding of DevOps concepts
- Access to Linux/Unix environment or WSL

---

## 2. Shell Fundamentals

### Shell Types and Selection

**Bash (Bourne Again Shell)**
```bash
# Check bash version
bash --version

# Default shell location
which bash
# /bin/bash or /usr/bin/bash

# Switch to bash
bash
```

**Zsh (Z Shell)**
```bash
# Check if zsh is installed
which zsh

# Install zsh (Ubuntu/Debian)
sudo apt-get install zsh

# Switch to zsh
zsh
```

**PowerShell (Cross-platform)**
```powershell
# Check PowerShell version
$PSVersionTable

# Install PowerShell Core (Linux)
# Ubuntu/Debian
wget -q https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y powershell
```

### Shell Configuration Files

```bash
# Bash configuration files (loaded in order)
~/.bash_profile    # Login shells (macOS)
~/.bashrc          # Interactive non-login shells
~/.bash_login      # Login shells (if .bash_profile doesn't exist)
~/.profile         # Fallback for all shells

# Zsh configuration
~/.zshrc           # Main configuration file
~/.zprofile        # Login shells

# Check current shell
echo $SHELL

# List available shells
cat /etc/shells
```

### Environment Variables

```bash
# View all environment variables
env
printenv

# View specific variable
echo $HOME
echo $PATH
echo $USER

# Set environment variable
export MY_VAR="value"
export PATH=$PATH:/custom/path

# Persistent environment variables
# Add to ~/.bashrc or ~/.zshrc
echo 'export MY_VAR="value"' >> ~/.bashrc
source ~/.bashrc

# Common DevOps environment variables
export AWS_REGION="us-east-1"
export KUBECONFIG="$HOME/.kube/config"
export DOCKER_HOST="unix:///var/run/docker.sock"
export TERRAFORM_LOG=DEBUG
```

### Command History and Aliases

```bash
# View command history
history
history | grep "docker"
history | tail -20

# Search history interactively
# Press Ctrl+R and type search term

# Configure history size
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups

# Create aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'
alias k='kubectl'
alias d='docker'
alias tf='terraform'

# View all aliases
alias

# Persistent aliases (add to ~/.bashrc)
cat >> ~/.bashrc << EOF
alias ll='ls -alF'
alias k='kubectl'
EOF
```

### Input/Output Redirection

```bash
# Output redirection
command > file          # Overwrite file
command >> file         # Append to file
command 2> file         # Redirect stderr
command > file 2>&1     # Redirect both stdout and stderr
command &> file         # Redirect both (bash 4+)

# Input redirection
command < file
command << EOF
multi-line
input
EOF

# Pipes
command1 | command2
command1 | command2 | command3

# Examples
docker ps | grep running
kubectl get pods | awk '{print $1}'
cat log.txt | grep ERROR | wc -l
```

### Command Substitution

```bash
# Backticks (older syntax)
echo "Today is `date`"

# $() syntax (preferred)
echo "Today is $(date)"
echo "Current user: $(whoami)"
echo "Files: $(ls -la)"

# Nested substitution
echo "Date: $(date +%Y-%m-%d)"
echo "Pods: $(kubectl get pods -o jsonpath='{.items[*].metadata.name}')"
```

---

## 3. Essential Linux/Unix Commands

### File and Directory Operations

```bash
# List files
ls                    # Basic listing
ls -l                 # Long format
ls -la                # All files including hidden
ls -lh                # Human-readable sizes
ls -lt                # Sorted by time
ls -ltr               # Reverse time sort
ls -R                 # Recursive
ls -d */              # Only directories

# Change directory
cd /path/to/dir
cd ~                  # Home directory
cd -                  # Previous directory
cd ..                 # Parent directory

# Create directories
mkdir dirname
mkdir -p path/to/dir  # Create parent directories
mkdir -m 755 dirname  # With specific permissions

# Remove files/directories
rm file.txt
rm -f file.txt        # Force (no prompt)
rm -r directory       # Recursive
rm -rf directory      # Force recursive
rm -i file.txt        # Interactive (prompt)

# Copy files
cp source dest
cp -r source dest     # Recursive
cp -p source dest     # Preserve attributes
cp -a source dest     # Archive mode (preserve all)

# Move/rename files
mv source dest
mv file.txt newname.txt

# Find files
find /path -name "*.txt"
find . -type f -name "*.log"
find . -type d -name "node_modules"
find . -size +100M    # Files larger than 100MB
find . -mtime -7      # Modified in last 7 days
find . -user username
find . -perm 644
find . -exec ls -l {} \;  # Execute command on results

# Locate files (faster, uses database)
locate filename
updatedb              # Update locate database
```

### File Viewing and Editing

```bash
# View file contents
cat file.txt          # Entire file
less file.txt         # Paginated view
more file.txt         # Paginated view (older)
head file.txt         # First 10 lines
head -n 20 file.txt   # First 20 lines
tail file.txt         # Last 10 lines
tail -n 20 file.txt   # Last 20 lines
tail -f file.txt      # Follow (watch for changes)

# View multiple files
cat file1.txt file2.txt
head -n 5 *.log

# Search within files
grep "pattern" file.txt
grep -r "pattern" /path  # Recursive
grep -i "pattern" file.txt  # Case insensitive
grep -v "pattern" file.txt  # Invert match
grep -n "pattern" file.txt  # Show line numbers
grep -c "pattern" file.txt  # Count matches
grep -A 3 "pattern" file.txt  # After context
grep -B 3 "pattern" file.txt  # Before context
grep -C 3 "pattern" file.txt  # Both contexts

# Advanced file operations
wc file.txt           # Word count (lines, words, chars)
wc -l file.txt        # Line count only
sort file.txt         # Sort lines
sort -r file.txt     # Reverse sort
sort -n file.txt      # Numeric sort
uniq file.txt         # Remove duplicates
uniq -c file.txt      # Count occurrences
cut -d: -f1 file.txt  # Cut fields (delimiter :, field 1)
```

### File Permissions and Ownership

```bash
# View permissions
ls -l file.txt
# Output: -rw-r--r-- 1 user group 1234 date file.txt
#         drwxr-xr-x 2 user group 4096 date dirname

# Permission format: rwxrwxrwx
# Owner | Group | Others
# r=read, w=write, x=execute

# Change permissions (numeric)
chmod 755 file.txt    # rwxr-xr-x
chmod 644 file.txt    # rw-r--r--
chmod 600 file.txt    # rw-------
chmod +x script.sh    # Add execute permission
chmod -x script.sh    # Remove execute permission

# Change permissions (symbolic)
chmod u+x file.txt    # User execute
chmod g+w file.txt    # Group write
chmod o-r file.txt    # Others remove read
chmod a+x file.txt    # All execute

# Change ownership
chown user:group file.txt
chown -R user:group directory/  # Recursive
sudo chown root:root file.txt

# Change group
chgrp groupname file.txt
chgrp -R groupname directory/
```

### System Information

```bash
# System information
uname -a              # All system info
uname -s              # Kernel name
uname -r              # Kernel release
uname -m              # Machine architecture

# Hostname
hostname
hostnamectl           # Systemd hostname control

# Uptime and load
uptime
w                     # Who is logged in and load

# CPU information
lscpu
cat /proc/cpuinfo
nproc                 # Number of processors

# Memory information
free -h               # Human-readable
free -m               # Megabytes
cat /proc/meminfo

# Disk usage
df -h                 # Human-readable
df -i                 # Inode usage
du -h                 # Directory usage
du -sh *              # Summary of each item
du -h --max-depth=1   # One level deep

# Process information
ps aux                # All processes
ps aux | grep process
top                   # Interactive process viewer
htop                  # Enhanced top (if installed)
```

---

## 4. Text Processing and Manipulation

### grep - Pattern Matching

```bash
# Basic usage
grep "pattern" file.txt

# Common options
grep -i "pattern" file.txt        # Case insensitive
grep -v "pattern" file.txt        # Invert match
grep -n "pattern" file.txt        # Line numbers
grep -c "pattern" file.txt        # Count matches
grep -l "pattern" *.txt           # List matching files
grep -L "pattern" *.txt           # List non-matching files
grep -r "pattern" /path           # Recursive
grep -R "pattern" /path           # Recursive (follow symlinks)
grep -w "pattern" file.txt        # Whole word
grep -x "pattern" file.txt        # Exact line match

# Context lines
grep -A 5 "pattern" file.txt     # 5 lines after
grep -B 5 "pattern" file.txt     # 5 lines before
grep -C 5 "pattern" file.txt     # 5 lines before and after

# Multiple patterns
grep -e "pattern1" -e "pattern2" file.txt
grep -E "pattern1|pattern2" file.txt  # Extended regex

# Regular expressions
grep "^pattern" file.txt          # Starts with
grep "pattern$" file.txt          # Ends with
grep "p.ttern" file.txt           # Any character
grep "p.*tern" file.txt           # Zero or more
grep "p\+tern" file.txt           # One or more (extended)
grep -E "p+tern" file.txt         # One or more (extended)
grep "[0-9]" file.txt             # Digits
grep "[a-zA-Z]" file.txt          # Letters

# Practical DevOps examples
grep -r "ERROR" /var/log
grep -i "failed" /var/log/syslog
grep -E "^(ERROR|WARN)" app.log
kubectl get pods | grep -v Running
docker ps | grep -E "Exited|Dead"
```

### sed - Stream Editor

```bash
# Basic substitution
sed 's/old/new/' file.txt         # Replace first occurrence per line
sed 's/old/new/g' file.txt        # Replace all occurrences
sed 's/old/new/2' file.txt        # Replace 2nd occurrence

# In-place editing
sed -i 's/old/new/g' file.txt     # Linux
sed -i '' 's/old/new/g' file.txt  # macOS

# Delete lines
sed '5d' file.txt                 # Delete line 5
sed '1,10d' file.txt              # Delete lines 1-10
sed '/pattern/d' file.txt         # Delete matching lines

# Print specific lines
sed -n '5p' file.txt              # Print line 5
sed -n '10,20p' file.txt          # Print lines 10-20
sed -n '/pattern/p' file.txt      # Print matching lines

# Multiple commands
sed -e 's/old1/new1/' -e 's/old2/new2/' file.txt
sed 's/old1/new1/; s/old2/new2/' file.txt

# Advanced examples
sed 's/^/# /' file.txt            # Comment out lines
sed 's/# //' file.txt             # Uncomment
sed 's/^[[:space:]]*//' file.txt  # Remove leading spaces
sed 's/[[:space:]]*$//' file.txt  # Remove trailing spaces

# Practical DevOps examples
sed -i 's/localhost/production-host/' config.yml
sed '/^#/d' config.txt            # Remove comment lines
sed 's/127.0.0.1/0.0.0.0/g' nginx.conf
kubectl get pods -o yaml | sed 's/namespace: default/namespace: production/'
```

### awk - Pattern Processing

```bash
# Basic usage
awk '{print}' file.txt            # Print all lines
awk '{print $1}' file.txt         # Print first field
awk '{print $1, $3}' file.txt     # Print first and third fields
awk '{print $NF}' file.txt        # Print last field

# Field separator
awk -F: '{print $1}' /etc/passwd  # Custom delimiter
awk -F'[ :]' '{print $1}' file.txt  # Multiple delimiters

# Pattern matching
awk '/pattern/ {print}' file.txt
awk '/pattern1/ || /pattern2/ {print}' file.txt
awk '$1 == "value" {print}' file.txt
awk '$3 > 100 {print}' file.txt

# Built-in variables
awk '{print NR, $0}' file.txt     # NR = record number
awk '{print NF, $0}' file.txt     # NF = number of fields
awk 'END {print NR}' file.txt     # Total lines
awk '{sum+=$1} END {print sum}' file.txt  # Sum column

# Advanced examples
awk '{if ($3 > 100) print $1, $3}' file.txt
awk '{for(i=1;i<=NF;i++) print $i}' file.txt
awk 'BEGIN {FS=":"} {print $1}' /etc/passwd

# Practical DevOps examples
# Parse kubectl output
kubectl get pods | awk '$3 != "Running" {print $1, $3}'
kubectl get pods | awk 'NR>1 {print $1}'

# Parse docker stats
docker stats --no-stream | awk 'NR>1 {print $2, $3}'

# Parse log files
awk '/ERROR/ {count++} END {print "Errors:", count}' app.log
awk '$4 >= "[2024-01-01" && $4 <= "[2024-01-31" {print}' access.log

# Parse CSV
awk -F',' '{print $1, $3}' data.csv
```

### cut - Field Extraction

```bash
# Basic usage
cut -d: -f1 /etc/passwd           # Delimiter :, field 1
cut -d',' -f1,3 file.csv          # Multiple fields
cut -c1-10 file.txt               # Characters 1-10
cut -c1,5,10 file.txt             # Specific characters

# Common options
cut -d' ' -f1-3 file.txt          # Fields 1-3
cut -d'\t' -f2 file.txt           # Tab delimiter
cut --complement -d: -f1 file.txt # All fields except 1

# Practical examples
echo "user:pass:uid:gid" | cut -d: -f1,3
kubectl get pods -o wide | cut -d' ' -f1,7
```

### sort and uniq

```bash
# Sort
sort file.txt                     # Alphabetical
sort -n file.txt                  # Numeric
sort -r file.txt                  # Reverse
sort -u file.txt                  # Unique
sort -k2 file.txt                 # Sort by 2nd field
sort -t: -k3 -n /etc/passwd       # Sort by 3rd field (numeric)

# Uniq
uniq file.txt                     # Remove consecutive duplicates
uniq -c file.txt                 # Count occurrences
uniq -d file.txt                 # Only duplicates
uniq -u file.txt                 # Only unique

# Combined usage
sort file.txt | uniq
sort file.txt | uniq -c | sort -rn  # Count and sort by frequency
```

### tr - Character Translation

```bash
# Translate characters
echo "hello" | tr 'a-z' 'A-Z'     # Uppercase
echo "HELLO" | tr 'A-Z' 'a-z'     # Lowercase
echo "hello" | tr '[:lower:]' '[:upper:]'

# Delete characters
echo "hello123" | tr -d '0-9'     # Remove digits
echo "hello world" | tr -d ' '    # Remove spaces

# Squeeze characters
echo "hello    world" | tr -s ' ' # Squeeze spaces
```

### paste and join

```bash
# Paste - merge lines
paste file1.txt file2.txt        # Side by side
paste -d: file1.txt file2.txt    # Custom delimiter

# Join - join files on common field
join file1.txt file2.txt         # Join on first field
join -1 2 -2 1 file1.txt file2.txt  # Join on different fields
```

---

## 5. Process and System Management

### Process Management

```bash
# View processes
ps                              # Current shell processes
ps aux                          # All processes (BSD style)
ps -ef                          # All processes (Unix style)
ps aux | grep process_name
ps -p PID                       # Specific process

# Process tree
pstree
pstree -p                       # With PIDs
pstree -u                       # With users

# Real-time process monitoring
top                             # Interactive
htop                            # Enhanced (if installed)
top -p PID                      # Specific process
top -u username                 # Specific user

# Process details
ps -o pid,ppid,cmd,etime,user process_name
ps auxf                         # Forest view

# Kill processes
kill PID                        # Terminate (SIGTERM)
kill -9 PID                     # Force kill (SIGKILL)
kill -15 PID                    # Graceful termination
killall process_name            # Kill all by name
pkill process_name              # Kill by pattern
kill -l                         # List signals

# Process priority
nice -n 10 command              # Lower priority (higher nice)
renice 10 PID                   # Change priority
nice -n -10 command             # Higher priority (lower nice)

# Background and foreground
command &                       # Run in background
jobs                            # List background jobs
fg %1                           # Bring job 1 to foreground
bg %1                           # Resume job 1 in background
nohup command &                 # Run immune to hangups
```

### System Monitoring

```bash
# CPU monitoring
top
htop
mpstat                          # CPU statistics
mpstat 1 5                     # Every 1 second, 5 times
vmstat                          # Virtual memory stats
vmstat 1 5                     # Every 1 second, 5 times

# Memory monitoring
free -h                         # Human-readable
free -m                         # Megabytes
free -s 5                       # Update every 5 seconds
cat /proc/meminfo
vmstat -s                       # Memory summary

# Disk I/O monitoring
iostat                          # I/O statistics
iostat -x 1 5                   # Extended, every 1s, 5 times
iotop                           # Top for I/O (if installed)
df -h                           # Disk space
du -sh *                        # Directory sizes

# Network monitoring
iftop                           # Network traffic (if installed)
nethogs                         # Per-process network (if installed)
ss -tuln                        # Socket statistics
netstat -tuln                   # Network connections
```

### System Services (systemd)

```bash
# Service management
systemctl status service_name
systemctl start service_name
systemctl stop service_name
systemctl restart service_name
systemctl reload service_name
systemctl enable service_name   # Enable on boot
systemctl disable service_name
systemctl is-active service_name
systemctl is-enabled service_name

# List services
systemctl list-units            # All units
systemctl list-units --type=service
systemctl list-units --state=running
systemctl list-unit-files

# Service logs
journalctl -u service_name      # Service logs
journalctl -u service_name -f   # Follow logs
journalctl -u service_name --since "1 hour ago"
journalctl -u service_name --since today
journalctl -xe                  # Recent logs with errors

# System information
systemctl status
systemctl list-jobs
systemctl show service_name
```

### Cron and Scheduled Tasks

```bash
# View crontab
crontab -l                      # Current user
crontab -l -u username          # Specific user
sudo crontab -l                 # Root

# Edit crontab
crontab -e
crontab -e -u username

# Crontab format
# * * * * * command
# │ │ │ │ │
# │ │ │ │ └─── day of week (0-7, Sunday = 0 or 7)
# │ │ │ └───── month (1-12)
# │ │ └─────── day of month (1-31)
# │ └───────── hour (0-23)
# └─────────── minute (0-59)

# Examples
0 * * * * /path/to/script.sh           # Every hour
0 0 * * * /path/to/script.sh           # Daily at midnight
0 0 * * 0 /path/to/script.sh            # Weekly on Sunday
0 0 1 * * /path/to/script.sh            # Monthly on 1st
*/5 * * * * /path/to/script.sh         # Every 5 minutes
0 2 * * * /path/to/backup.sh            # Daily at 2 AM

# System-wide crontab
sudo vim /etc/crontab
sudo vim /etc/cron.d/custom

# Cron directories
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

---

## 6. Network Operations

### Network Configuration

```bash
# Interface information
ip addr show
ip a                            # Short form
ifconfig                        # Traditional (may need net-tools)
ip link show

# Network interfaces
ip link set eth0 up
ip link set eth0 down
ip link set eth0 mtu 1500

# IP addresses
ip addr add 192.168.1.100/24 dev eth0
ip addr del 192.168.1.100/24 dev eth0
ip addr flush dev eth0

# Routing
ip route show
ip route add default via 192.168.1.1
ip route del default
ip route add 192.168.2.0/24 via 192.168.1.1

# Network statistics
ss -tuln                        # Socket statistics
ss -tulnp                        # With process info
netstat -tuln                   # Traditional
netstat -tulnp
```

### Network Testing and Diagnostics

```bash
# Ping
ping hostname
ping -c 4 hostname              # 4 packets
ping -i 2 hostname              # Interval 2 seconds
ping6 hostname                  # IPv6

# Traceroute
traceroute hostname
traceroute -n hostname          # No DNS lookup
mtr hostname                    # My traceroute (if installed)

# DNS lookup
nslookup domain.com
dig domain.com
dig @8.8.8.8 domain.com         # Specific DNS server
dig domain.com MX                # MX records
dig domain.com A                 # A records
host domain.com

# Port scanning
nc -zv hostname 80              # Test port
nc -zv hostname 22 80 443       # Multiple ports
nmap hostname                    # Network mapper (if installed)
nmap -p 80,443 hostname
nmap -p 1-1000 hostname

# HTTP/HTTPS testing
curl http://example.com
curl -I http://example.com      # Headers only
curl -v http://example.com      # Verbose
curl -L http://example.com      # Follow redirects
curl -O http://example.com/file # Download
curl -X POST -d "data" http://example.com/api

wget http://example.com/file
wget -r http://example.com      # Recursive
wget -c http://example.com/file # Continue partial download
```

### Network Monitoring

```bash
# Real-time network monitoring
iftop                           # Interface top (if installed)
nethogs                         # Per-process network (if installed)
vnstat                          # Network statistics (if installed)

# Packet capture
tcpdump                         # Packet analyzer
tcpdump -i eth0
tcpdump -i eth0 port 80
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 -w capture.pcap # Save to file
tcpdump -r capture.pcap         # Read from file

# Network connections
ss -tuln                        # All connections
ss -tulnp                        # With processes
lsof -i                         # List open files (network)
lsof -i :80                     # Port 80
lsof -i tcp:443                 # TCP port 443
```

### Firewall Management

```bash
# UFW (Uncomplicated Firewall)
sudo ufw status
sudo ufw enable
sudo ufw disable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow from 192.168.1.0/24
sudo ufw delete allow 22/tcp
sudo ufw reset

# firewalld (RHEL/CentOS)
sudo firewall-cmd --list-all
sudo firewall-cmd --add-port=80/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports

# iptables (traditional)
sudo iptables -L                # List rules
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables-save > /etc/iptables/rules.v4
```

---

## 7. File System Operations

### Disk Management

```bash
# Disk usage
df -h                           # Human-readable
df -i                           # Inode usage
df -T                           # File system types
du -h                           # Directory usage
du -sh *                        # Summary per item
du -h --max-depth=1             # One level
du -h --max-depth=2             # Two levels

# Find large files
find / -type f -size +100M      # Files > 100MB
find / -type f -size +1G        # Files > 1GB
find / -type f -exec ls -lh {} \; | awk '{print $5, $9}' | sort -h

# Disk operations
lsblk                           # List block devices
fdisk -l                        # Partition table
blkid                           # Block device IDs
mount                           # Mounted file systems
umount /mnt                     # Unmount
mount /dev/sda1 /mnt            # Mount device
```

### File System Types and Operations

```bash
# Check file system type
df -T
file -s /dev/sda1
blkid

# Create file systems
sudo mkfs.ext4 /dev/sda1
sudo mkfs.xfs /dev/sda1
sudo mkfs.btrfs /dev/sda1

# Check and repair
sudo fsck /dev/sda1
sudo fsck.ext4 /dev/sda1
sudo e2fsck -f /dev/sda1        # Force check

# Resize file systems
sudo resize2fs /dev/sda1        # ext2/3/4
sudo xfs_growfs /mount/point    # XFS
```

### Archive and Compression

```bash
# tar (tape archive)
tar -cf archive.tar files/      # Create
tar -xf archive.tar             # Extract
tar -czf archive.tar.gz files/  # Compress with gzip
tar -xzf archive.tar.gz         # Extract gzip
tar -cjf archive.tar.bz2 files/ # Compress with bzip2
tar -xjf archive.tar.bz2        # Extract bzip2
tar -czf archive.tar.gz --exclude='*.log' files/
tar -tvf archive.tar            # List contents
tar -xzf archive.tar.gz -C /destination

# gzip
gzip file.txt                   # Compress (creates file.txt.gz)
gunzip file.txt.gz              # Decompress
gzip -d file.txt.gz
zcat file.txt.gz                # View without extracting

# zip/unzip
zip archive.zip file1 file2
zip -r archive.zip directory/
unzip archive.zip
unzip -l archive.zip            # List contents
unzip -d /destination archive.zip

# Other compression
bzip2 file.txt                  # Compress
bunzip2 file.txt.bz2            # Decompress
xz file.txt                     # Compress
unxz file.txt.xz                # Decompress
```

### File Searching

```bash
# find - comprehensive search
find /path -name "*.txt"
find . -type f -name "*.log"
find . -type d -name "node_modules"
find . -size +100M
find . -size -1k
find . -mtime -7                # Modified last 7 days
find . -mtime +30                # Modified more than 30 days ago
find . -atime -1                # Accessed today
find . -user username
find . -group groupname
find . -perm 644
find . -perm -u+x               # User executable
find . -empty                    # Empty files/dirs

# find with actions
find . -name "*.log" -delete
find . -name "*.tmp" -exec rm {} \;
find . -name "*.txt" -exec ls -lh {} \;
find . -name "*.log" -exec grep -l "ERROR" {} \;

# locate (faster, uses database)
locate filename
locate "*.log"
updatedb                        # Update database
```

---

## 8. Package Management

### APT (Debian/Ubuntu)

```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade
sudo apt full-upgrade

# Install packages
sudo apt install package_name
sudo apt install package1 package2

# Remove packages
sudo apt remove package_name
sudo apt purge package_name     # Remove with config
sudo apt autoremove             # Remove unused

# Search packages
apt search keyword
apt-cache search keyword

# Package information
apt show package_name
apt-cache show package_name
dpkg -l                         # List installed
dpkg -l | grep package_name

# Package files
dpkg -L package_name            # List files
dpkg -S /path/to/file           # Which package owns file

# Repositories
cat /etc/apt/sources.list
sudo apt-add-repository "deb ..."
sudo apt-add-repository --remove "deb ..."
```

### YUM/DNF (RHEL/CentOS/Fedora)

```bash
# Update packages
sudo yum update
sudo dnf update                 # DNF (newer)

# Install packages
sudo yum install package_name
sudo dnf install package_name

# Remove packages
sudo yum remove package_name
sudo dnf remove package_name

# Search packages
yum search keyword
dnf search keyword

# Package information
yum info package_name
dnf info package_name
rpm -qa                         # List installed
rpm -qa | grep package_name
rpm -qi package_name            # Package info
rpm -ql package_name            # List files

# Repositories
yum repolist
dnf repolist
cat /etc/yum.repos.d/*.repo
```

### Snap

```bash
# Install
sudo snap install package_name

# Remove
sudo snap remove package_name

# List installed
snap list

# Update
sudo snap refresh
sudo snap refresh package_name

# Search
snap search keyword

# Information
snap info package_name
```

---

## 9. Docker CLI Mastery

### Docker Basics

```bash
# Docker version and info
docker --version
docker version
docker info

# Container lifecycle
docker run image_name
docker run -d image_name        # Detached mode
docker run -it image_name       # Interactive TTY
docker run --name mycontainer image_name
docker start container_name
docker stop container_name
docker restart container_name
docker pause container_name
docker unpause container_name
docker kill container_name      # Force stop
docker rm container_name        # Remove
docker rm -f container_name     # Force remove

# List containers
docker ps                        # Running
docker ps -a                     # All
docker ps -l                     # Latest
docker ps -q                     # IDs only
docker ps --filter "status=exited"
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

### Docker Run Options

```bash
# Port mapping
docker run -p 8080:80 image_name
docker run -p 127.0.0.1:8080:80 image_name
docker run -P image_name        # Publish all ports

# Volume mounting
docker run -v /host/path:/container/path image_name
docker run -v volume_name:/container/path image_name
docker run --mount type=bind,source=/host,target=/container image_name

# Environment variables
docker run -e VAR=value image_name
docker run -e VAR1=val1 -e VAR2=val2 image_name
docker run --env-file .env image_name

# Resource limits
docker run --memory="512m" image_name
docker run --cpus="1.5" image_name
docker run --memory="1g" --cpus="2" image_name

# Network
docker run --network network_name image_name
docker run --network host image_name
docker run --network none image_name

# Other useful options
docker run --rm image_name      # Auto-remove on exit
docker run --restart=always image_name
docker run --restart=unless-stopped image_name
docker run --user 1000:1000 image_name
docker run --read-only image_name
docker run --tmpfs /tmp image_name
```

### Docker Images

```bash
# List images
docker images
docker images -a                # All (including intermediate)
docker images --filter "dangling=true"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Pull images
docker pull image_name
docker pull image_name:tag
docker pull registry/image_name:tag

# Build images
docker build .
docker build -t image_name:tag .
docker build -f Dockerfile.custom .
docker build --no-cache .
docker build --build-arg VAR=value .

# Remove images
docker rmi image_name
docker rmi image_id
docker rmi -f image_name        # Force
docker image prune              # Remove dangling
docker image prune -a           # Remove unused

# Image operations
docker tag old_name:tag new_name:tag
docker push image_name:tag
docker save image_name > image.tar
docker load < image.tar
docker import file.tar image_name:tag
docker history image_name
docker inspect image_name
```

### Docker Logs and Exec

```bash
# View logs
docker logs container_name
docker logs -f container_name   # Follow
docker logs --tail 100 container_name
docker logs --since 10m container_name
docker logs --until 10m container_name
docker logs -t container_name   # Timestamps

# Execute commands
docker exec container_name command
docker exec -it container_name /bin/bash
docker exec -u root container_name command
docker exec -w /path container_name command

# Copy files
docker cp container_name:/path /host/path
docker cp /host/path container_name:/path
```

### Docker Networks

```bash
# List networks
docker network ls

# Create network
docker network create network_name
docker network create --driver bridge network_name
docker network create --subnet 172.20.0.0/16 network_name

# Inspect network
docker network inspect network_name

# Connect/disconnect
docker network connect network_name container_name
docker network disconnect network_name container_name

# Remove network
docker network rm network_name
docker network prune           # Remove unused
```

### Docker Volumes

```bash
# List volumes
docker volume ls

# Create volume
docker volume create volume_name

# Inspect volume
docker volume inspect volume_name

# Remove volume
docker volume rm volume_name
docker volume prune            # Remove unused
```

### Docker Compose

```bash
# Basic commands
docker-compose up
docker-compose up -d            # Detached
docker-compose down
docker-compose stop
docker-compose start
docker-compose restart
docker-compose ps
docker-compose logs
docker-compose logs -f service_name

# Build and run
docker-compose build
docker-compose up --build
docker-compose build --no-cache

# Scale services
docker-compose up --scale service_name=3

# Execute commands
docker-compose exec service_name command
docker-compose exec service_name /bin/bash

# Configuration
docker-compose config           # Validate config
docker-compose pull             # Pull images
```

### Docker Advanced

```bash
# System information
docker system df                # Disk usage
docker system events            # Real-time events
docker system info
docker system prune             # Clean up

# Container stats
docker stats
docker stats container_name
docker stats --no-stream
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Container inspection
docker inspect container_name
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_name
docker inspect --format='{{json .Config}}' container_name | jq

# Health checks
docker ps --filter "health=healthy"
docker ps --filter "health=unhealthy"

# Docker context (multi-host)
docker context ls
docker context use context_name
docker context create remote --docker "host=ssh://user@host"
```

---

## 10. Kubernetes CLI (kubectl)

### kubectl Basics

```bash
# Version and configuration
kubectl version
kubectl version --client
kubectl cluster-info
kubectl config view
kubectl config current-context
kubectl config get-contexts
kubectl config use-context context_name
kubectl config set-context context_name --namespace=namespace

# Get resources
kubectl get pods
kubectl get pods -A             # All namespaces
kubectl get pods -n namespace
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json
kubectl get pods --watch        # Watch changes
kubectl get all                 # All resources
kubectl get nodes
kubectl get namespaces
kubectl get services
kubectl get deployments
kubectl get replicasets
kubectl get configmaps
kubectl get secrets
```

### Resource Management

```bash
# Create resources
kubectl create deployment nginx --image=nginx
kubectl create namespace mynamespace
kubectl create service clusterip myservice --tcp=80:8080
kubectl create configmap myconfig --from-file=config.properties
kubectl create secret generic mysecret --from-literal=key=value
kubectl apply -f manifest.yaml
kubectl create -f manifest.yaml

# Delete resources
kubectl delete pod pod_name
kubectl delete pod pod_name -n namespace
kubectl delete deployment deployment_name
kubectl delete -f manifest.yaml
kubectl delete all --all -n namespace

# Edit resources
kubectl edit pod pod_name
kubectl edit deployment deployment_name
kubectl edit -f manifest.yaml

# Scale resources
kubectl scale deployment deployment_name --replicas=3
kubectl scale --replicas=5 deployment/deployment_name
```

### Pod Operations

```bash
# Describe pod
kubectl describe pod pod_name
kubectl describe pod pod_name -n namespace

# Pod logs
kubectl logs pod_name
kubectl logs pod_name -n namespace
kubectl logs pod_name -c container_name  # Multi-container
kubectl logs -f pod_name                  # Follow
kubectl logs --tail=100 pod_name
kubectl logs --since=10m pod_name
kubectl logs --previous pod_name          # Previous instance

# Execute commands
kubectl exec pod_name -- command
kubectl exec -it pod_name -- /bin/bash
kubectl exec pod_name -c container_name -- command

# Copy files
kubectl cp pod_name:/path /local/path
kubectl cp /local/path pod_name:/path
kubectl cp pod_name:/path /local/path -c container_name

# Port forwarding
kubectl port-forward pod_name 8080:80
kubectl port-forward service/service_name 8080:80
kubectl port-forward deployment/deployment_name 8080:80
```

### Advanced kubectl

```bash
# Output formatting
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
kubectl get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'

# Field selectors
kubectl get pods --field-selector status.phase=Running
kubectl get pods --field-selector metadata.namespace=default

# Label selectors
kubectl get pods -l app=nginx
kubectl get pods -l 'app in (nginx,apache)'
kubectl get pods -l '!app'
kubectl label pod pod_name key=value
kubectl label pod pod_name key-  # Remove label

# Annotations
kubectl annotate pod pod_name key=value
kubectl annotate pod pod_name key-  # Remove

# Rollout management
kubectl rollout status deployment/deployment_name
kubectl rollout history deployment/deployment_name
kubectl rollout undo deployment/deployment_name
kubectl rollout undo deployment/deployment_name --to-revision=2
kubectl rollout pause deployment/deployment_name
kubectl rollout resume deployment/deployment_name

# Debugging
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -n namespace --sort-by='.lastTimestamp'
kubectl top nodes
kubectl top pods
kubectl top pods -n namespace
kubectl top pod pod_name --containers
```

### kubectl Plugins and Tools

```bash
# Install kubectl plugins
kubectl krew install plugin_name
kubectl krew list
kubectl krew upgrade

# Useful plugins
kubectl krew install ctx        # Context switching
kubectl krew install ns         # Namespace switching
kubectl krew install access-matrix
kubectl krew install df-pv      # Disk usage

# k9s (terminal UI)
# Install: https://k9scli.io/
k9s                            # Launch k9s

# kubectx and kubens
kubectx                        # List contexts
kubectx context_name          # Switch context
kubens                         # List namespaces
kubens namespace_name         # Switch namespace
```

### YAML Generation

```bash
# Generate YAML
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml
kubectl create service clusterip mysvc --tcp=80:8080 --dry-run=client -o yaml
kubectl run nginx --image=nginx --dry-run=client -o yaml

# Export existing resources
kubectl get deployment deployment_name -o yaml > deployment.yaml
kubectl get pod pod_name -o yaml > pod.yaml
kubectl get all -o yaml > all-resources.yaml
```

---

## 11. Cloud CLI Tools

### AWS CLI (aws)

```bash
# Installation
# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configuration
aws configure
aws configure list
aws configure set region us-east-1
aws configure set output json

# Profiles
aws configure --profile profile_name
export AWS_PROFILE=profile_name
aws s3 ls --profile profile_name

# EC2
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
aws ec2 describe-images --owners amazon
aws ec2 create-key-pair --key-name mykey --query 'KeyMaterial' --output text > mykey.pem

# S3
aws s3 ls
aws s3 ls s3://bucket-name
aws s3 ls s3://bucket-name/path/
aws s3 cp file.txt s3://bucket-name/
aws s3 cp s3://bucket-name/file.txt ./
aws s3 sync ./local-folder s3://bucket-name/folder/
aws s3 sync s3://bucket-name/folder/ ./local-folder
aws s3 rm s3://bucket-name/file.txt
aws s3 mb s3://bucket-name
aws s3 rb s3://bucket-name
aws s3api list-objects --bucket bucket-name
aws s3api get-object-acl --bucket bucket-name --key file.txt

# IAM
aws iam list-users
aws iam list-groups
aws iam list-roles
aws iam get-user --user-name username
aws iam create-user --user-name newuser
aws iam attach-user-policy --user-name username --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam list-attached-user-policies --user-name username

# Lambda
aws lambda list-functions
aws lambda get-function --function-name myfunction
aws lambda invoke --function-name myfunction output.json
aws lambda create-function --function-name myfunction --runtime python3.9 --role arn:aws:iam::account:role/lambda-role --handler index.handler --zip-file fileb://function.zip

# CloudFormation
aws cloudformation list-stacks
aws cloudformation describe-stacks
aws cloudformation describe-stack-resources --stack-name mystack
aws cloudformation create-stack --stack-name mystack --template-body file://template.yaml
aws cloudformation update-stack --stack-name mystack --template-body file://template.yaml
aws cloudformation delete-stack --stack-name mystack

# EKS
aws eks list-clusters
aws eks describe-cluster --name cluster-name
aws eks update-kubeconfig --name cluster-name --region region-name

# CloudWatch
aws cloudwatch list-metrics
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-1234567890abcdef0 --start-time 2024-01-01T00:00:00Z --end-time 2024-01-02T00:00:00Z --period 3600 --statistics Average

# Secrets Manager
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id secret-name
aws secretsmanager create-secret --name secret-name --secret-string "secret-value"
```

### Azure CLI (az)

```bash
# Installation
# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
az login --tenant tenant-id
az account list
az account set --subscription subscription-id

# Resource Groups
az group list
az group create --name myResourceGroup --location eastus
az group delete --name myResourceGroup

# Virtual Machines
az vm list
az vm show --name vm-name --resource-group myResourceGroup
az vm start --name vm-name --resource-group myResourceGroup
az vm stop --name vm-name --resource-group myResourceGroup
az vm deallocate --name vm-name --resource-group myResourceGroup
az vm create --resource-group myResourceGroup --name vm-name --image UbuntuLTS --admin-username azureuser --generate-ssh-keys

# Storage
az storage account list
az storage account create --name storageaccount --resource-group myResourceGroup --location eastus --sku Standard_LRS
az storage container list --account-name storageaccount
az storage blob upload --account-name storageaccount --container-name container --name blob-name --file local-file.txt

# AKS (Kubernetes)
az aks list
az aks get-credentials --resource-group myResourceGroup --name cluster-name
az aks create --resource-group myResourceGroup --name cluster-name --node-count 3 --generate-ssh-keys

# App Service
az webapp list
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name app-name --runtime "PYTHON|3.9"
az webapp deployment source config-zip --resource-group myResourceGroup --name app-name --src app.zip
```

### Google Cloud CLI (gcloud)

```bash
# Installation
# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Configuration
gcloud config list
gcloud config set project PROJECT_ID
gcloud config set compute/zone us-central1-a
gcloud auth login
gcloud auth application-default login

# Compute Engine
gcloud compute instances list
gcloud compute instances create instance-name --zone=us-central1-a --machine-type=n1-standard-1 --image=ubuntu-2004-focal-v20240101
gcloud compute instances start instance-name --zone=us-central1-a
gcloud compute instances stop instance-name --zone=us-central1-a
gcloud compute instances delete instance-name --zone=us-central1-a

# GKE (Kubernetes)
gcloud container clusters list
gcloud container clusters get-credentials cluster-name --zone=us-central1-a
gcloud container clusters create cluster-name --num-nodes=3 --zone=us-central1-a

# Cloud Storage
gsutil ls
gsutil cp file.txt gs://bucket-name/
gsutil cp gs://bucket-name/file.txt ./
gsutil rsync -r ./local-folder gs://bucket-name/folder/
gsutil rm gs://bucket-name/file.txt
gsutil mb gs://bucket-name
gsutil rb gs://bucket-name

# Cloud Functions
gcloud functions list
gcloud functions deploy function-name --runtime python39 --trigger-http --allow-unauthenticated
gcloud functions delete function-name
```

---

## 12. Infrastructure as Code CLI

### Terraform CLI

```bash
# Installation
# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Basic commands
terraform init                   # Initialize
terraform plan                   # Preview changes
terraform apply                  # Apply changes
terraform apply -auto-approve    # Auto-approve
terraform destroy                # Destroy infrastructure
terraform destroy -target=resource.type.name  # Target specific resource

# State management
terraform state list             # List resources
terraform state show resource.type.name
terraform state mv old new       # Move resource
terraform state rm resource.type.name
terraform state pull > state.json
terraform state push state.json

# Workspaces
terraform workspace list
terraform workspace new dev
terraform workspace select dev
terraform workspace delete dev

# Outputs
terraform output
terraform output variable_name
terraform output -json

# Format and validate
terraform fmt                    # Format files
terraform fmt -check             # Check formatting
terraform validate               # Validate configuration

# Import existing resources
terraform import resource.type.name resource_id

# Debugging
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform.log
terraform plan -var-file=vars.tfvars
```

### Ansible CLI

```bash
# Installation
pip install ansible
# or
sudo apt install ansible

# Ad-hoc commands
ansible all -m ping
ansible all -a "uptime"
ansible webservers -m yum -a "name=httpd state=present"
ansible all -m copy -a "src=/path/to/file dest=/remote/path"

# Playbooks
ansible-playbook playbook.yml
ansible-playbook playbook.yml --check        # Dry run
ansible-playbook playbook.yml --limit hosts
ansible-playbook playbook.yml -v             # Verbose
ansible-playbook playbook.yml -vvv           # More verbose
ansible-playbook playbook.yml --tags tag_name
ansible-playbook playbook.yml --skip-tags tag_name

# Inventory
ansible-inventory --list
ansible-inventory --graph
ansible-inventory --host hostname

# Vault
ansible-vault create file.yml
ansible-vault edit file.yml
ansible-vault encrypt file.yml
ansible-vault decrypt file.yml
ansible-vault view file.yml
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file vault-pass.txt

# Galaxy
ansible-galaxy collection install collection_name
ansible-galaxy role install role_name
ansible-galaxy init role_name
```

### Pulumi CLI

```bash
# Installation
curl -fsSL https://get.pulumi.com | sh

# Basic commands
pulumi login
pulumi new                    # New project
pulumi stack init dev         # Create stack
pulumi stack select dev       # Select stack
pulumi preview                # Preview changes
pulumi up                     # Deploy
pulumi destroy                # Destroy
pulumi stack ls               # List stacks

# Configuration
pulumi config set key value
pulumi config get key
pulumi config
pulumi config set --secret key value  # Secret

# State
pulumi stack output
pulumi stack export
pulumi stack import
```

---

## 13. CI/CD CLI Tools

### Git CLI

```bash
# Configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --list
git config --global core.editor vim

# Repository operations
git init
git clone https://github.com/user/repo.git
git clone --branch branch_name https://github.com/user/repo.git
git remote add origin https://github.com/user/repo.git
git remote -v
git remote remove origin

# Basic operations
git status
git add file.txt
git add .
git add -A
git commit -m "Commit message"
git commit -am "Commit message"  # Add and commit
git log
git log --oneline
git log --graph --oneline --all
git show commit_hash

# Branching
git branch
git branch branch_name
git checkout branch_name
git checkout -b branch_name     # Create and switch
git switch branch_name          # Newer syntax
git switch -c branch_name        # Create and switch
git merge branch_name
git branch -d branch_name       # Delete
git branch -D branch_name       # Force delete

# Remote operations
git fetch origin
git pull origin branch_name
git push origin branch_name
git push -u origin branch_name  # Set upstream
git push --all origin
git push --tags

# Stashing
git stash
git stash save "message"
git stash list
git stash apply
git stash pop
git stash drop
git stash clear

# Undoing changes
git reset --soft HEAD~1         # Undo commit, keep changes
git reset --mixed HEAD~1        # Undo commit and staging
git reset --hard HEAD~1         # Undo commit and changes
git revert commit_hash          # Create revert commit
git checkout -- file.txt        # Discard changes
git restore file.txt            # Newer syntax

# Advanced
git rebase branch_name
git rebase -i HEAD~3            # Interactive rebase
git cherry-pick commit_hash
git tag v1.0.0
git tag -a v1.0.0 -m "Release"
git push origin v1.0.0
```

### GitHub CLI (gh)

```bash
# Installation
# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authentication
gh auth login
gh auth status
gh auth logout

# Repositories
gh repo clone owner/repo
gh repo create repo-name
gh repo view owner/repo
gh repo list
gh repo fork owner/repo

# Issues
gh issue list
gh issue create
gh issue view number
gh issue close number
gh issue comment number --body "comment"

# Pull Requests
gh pr list
gh pr create
gh pr view number
gh pr checkout number
gh pr merge number
gh pr close number
gh pr diff number

# Releases
gh release list
gh release create v1.0.0
gh release view v1.0.0
gh release download v1.0.0

# Workflows
gh workflow list
gh workflow run workflow_name
gh run list
gh run view run_id
gh run watch run_id
```

### GitLab CLI (glab)

```bash
# Installation
# Linux
curl -s https://gitlab.com/gitlab-org/cli/-/releases/permalink/latest/downloads/glab_Linux_x86_64.tar.gz | tar -xz
sudo mv bin/glab /usr/local/bin/

# Authentication
glab auth login
glab auth status

# Repositories
glab repo clone owner/repo
glab repo create repo-name
glab repo view

# Issues
glab issue list
glab issue create
glab issue view number
glab issue close number

# Merge Requests
glab mr list
glab mr create
glab mr view number
glab mr checkout number
glab mr merge number

# CI/CD
glab ci list
glab ci view
glab ci trace job_id
glab pipeline list
glab pipeline view pipeline_id
```

### Jenkins CLI

```bash
# Download jenkins-cli.jar
wget http://jenkins-server:8080/jnlpJars/jenkins-cli.jar

# Basic usage
java -jar jenkins-cli.jar -s http://jenkins-server:8080 -auth username:token command

# Common commands
java -jar jenkins-cli.jar -s http://jenkins-server:8080 list-jobs
java -jar jenkins-cli.jar -s http://jenkins-server:8080 get-job job-name
java -jar jenkins-cli.jar -s http://jenkins-server:8080 create-job job-name < config.xml
java -jar jenkins-cli.jar -s http://jenkins-server:8080 build job-name
java -jar jenkins-cli.jar -s http://jenkins-server:8080 console job-name build-number
java -jar jenkins-cli.jar -s http://jenkins-server:8080 install-plugin plugin-name
java -jar jenkins-cli.jar -s http://jenkins-server:8080 list-plugins
```

---

## 14. Monitoring and Logging CLI

### Prometheus CLI

```bash
# Prometheus server
prometheus --config.file=prometheus.yml
promtool check config prometheus.yml
promtool test rules test.yml

# Querying
curl 'http://localhost:9090/api/v1/query?query=up'
curl 'http://localhost:9090/api/v1/query_range?query=up&start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z&step=15m'

# Alertmanager
alertmanager --config.file=alertmanager.yml
amtool check-config alertmanager.yml
amtool alert query
amtool silence add alertname=HighCPU
amtool silence query
```

### Grafana CLI

```bash
# Installation
# Linux
wget https://dl.grafana.com/oss/release/grafana_9.0.0_amd64.deb
sudo dpkg -i grafana_9.0.0_amd64.deb

# Service management
sudo systemctl start grafana-server
sudo systemctl status grafana-server

# Admin operations
grafana-cli admin reset-admin-password newpassword
grafana-cli plugins install plugin-name
grafana-cli plugins ls
grafana-cli plugins update-all
```

### Log Management

```bash
# journalctl (systemd logs)
journalctl                          # All logs
journalctl -u service_name          # Service logs
journalctl -f                       # Follow
journalctl --since "1 hour ago"
journalctl --since today
journalctl --since "2024-01-01 00:00:00"
journalctl -p err                   # Error level and above
journalctl -k                       # Kernel messages
journalctl -b                       # Current boot
journalctl -b -1                    # Previous boot

# Log rotation
logrotate -d /etc/logrotate.conf    # Dry run
logrotate -f /etc/logrotate.conf    # Force rotation
logrotate -v /etc/logrotate.conf    # Verbose

# Centralized logging (if using)
# rsyslog
sudo systemctl status rsyslog
sudo tail -f /var/log/syslog

# ELK Stack (if installed)
# Elasticsearch
curl http://localhost:9200
curl http://localhost:9200/_cat/indices

# Logstash
logstash -f config.conf
logstash -t -f config.conf          # Test config
```

---

## 15. Security CLI Tools

### HashiCorp Vault CLI

```bash
# Installation
# Download from https://www.vaultproject.io/downloads

# Server
vault server -dev
vault server -config=vault.hcl

# Client operations
export VAULT_ADDR='http://127.0.0.1:8200'
vault status
vault auth -method=userpass username=user
vault login -method=userpass username=user

# Secrets
vault kv put secret/mysecret key=value
vault kv get secret/mysecret
vault kv list secret/
vault kv delete secret/mysecret

# Policies
vault policy list
vault policy read policy_name
vault policy write policy_name policy.hcl

# Tokens
vault token create
vault token list
vault token revoke token_id
```

### Trivy (Security Scanner)

```bash
# Installation
# Linux
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Image scanning
trivy image image_name
trivy image --severity HIGH,CRITICAL image_name
trivy image --format json image_name
trivy image --exit-code 1 image_name  # Exit on vulnerabilities

# File system scanning
trivy fs /path/to/directory
trivy fs --severity HIGH,CRITICAL /path

# Repository scanning
trivy repo https://github.com/user/repo
trivy repo --severity HIGH,CRITICAL .

# Kubernetes scanning
trivy k8s cluster
trivy k8s cluster --severity HIGH,CRITICAL
```

### Snyk CLI

```bash
# Installation
npm install -g snyk

# Authentication
snyk auth

# Test projects
snyk test
snyk test --severity-threshold=high
snyk test --json

# Monitor projects
snyk monitor

# Container scanning
snyk container test image_name
snyk container monitor image_name

# Infrastructure as Code
snyk iac test
snyk iac test terraform/
```

### OpenSSL

```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate certificate signing request
openssl req -new -key private.key -out request.csr

# Generate self-signed certificate
openssl req -x509 -new -nodes -key private.key -days 365 -out certificate.crt

# View certificate
openssl x509 -in certificate.crt -text -noout

# Check certificate expiration
openssl x509 -in certificate.crt -noout -enddate

# Test SSL connection
openssl s_client -connect hostname:443
openssl s_client -connect hostname:443 -showcerts

# Hash files
openssl md5 file.txt
openssl sha256 file.txt
```

---

## 16. Advanced Shell Scripting

### Script Basics

```bash
#!/bin/bash
# Shebang line - specifies interpreter

# Script with variables
NAME="DevOps Engineer"
echo "Hello, $NAME"
echo "Hello, ${NAME}"

# Command line arguments
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"

# Exit codes
exit 0    # Success
exit 1    # General error
exit 2    # Misuse of shell command
```

### Variables and Arrays

```bash
# Variables
VAR="value"
readonly VAR="value"    # Read-only
unset VAR               # Unset variable

# Arrays
ARRAY=("value1" "value2" "value3")
echo ${ARRAY[0]}
echo ${ARRAY[@]}        # All elements
echo ${#ARRAY[@]}       # Length

# Associative arrays (bash 4+)
declare -A ASSOC_ARRAY
ASSOC_ARRAY["key1"]="value1"
ASSOC_ARRAY["key2"]="value2"
echo ${ASSOC_ARRAY["key1"]}
```

### Control Structures

```bash
# If-else
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi

# Conditions
[ -f file ]              # File exists
[ -d dir ]               # Directory exists
[ -r file ]              # Readable
[ -w file ]              # Writable
[ -x file ]              # Executable
[ -z string ]            # String is empty
[ -n string ]            # String is not empty
[ str1 == str2 ]         # Strings equal
[ str1 != str2 ]         # Strings not equal
[ num1 -eq num2 ]        # Numbers equal
[ num1 -ne num2 ]        # Numbers not equal
[ num1 -lt num2 ]        # Less than
[ num1 -gt num2 ]        # Greater than

# For loop
for i in 1 2 3; do
    echo $i
done

for file in *.txt; do
    echo $file
done

for ((i=1; i<=10; i++)); do
    echo $i
done

# While loop
while [ condition ]; do
    commands
done

# Until loop
until [ condition ]; do
    commands
done

# Case statement
case $variable in
    pattern1)
        commands
        ;;
    pattern2)
        commands
        ;;
    *)
        commands
        ;;
esac
```

### Functions

```bash
# Function definition
function_name() {
    local var="local variable"
    echo "Function body"
    return 0
}

# Function with parameters
greet() {
    echo "Hello, $1"
}

greet "World"

# Function returning value
get_value() {
    echo "return value"
}

RESULT=$(get_value)
echo $RESULT
```

### Error Handling

```bash
# Exit on error
set -e

# Exit on undefined variable
set -u

# Print commands
set -x

# Pipefail
set -o pipefail

# Combined
set -euo pipefail

# Trap errors
trap 'echo "Error occurred"; exit 1' ERR

# Trap exit
trap 'cleanup_function' EXIT

# Ignore errors
command || true
command || echo "Command failed"
```

### Advanced Scripting Examples

```bash
#!/bin/bash
# Example: Docker container health check script

set -euo pipefail

CONTAINER_NAME="${1:-}"
HEALTH_CHECK_URL="${2:-http://localhost:8080/health}"
MAX_RETRIES=30
RETRY_INTERVAL=5

if [ -z "$CONTAINER_NAME" ]; then
    echo "Usage: $0 <container_name> [health_check_url]"
    exit 1
fi

check_health() {
    docker exec "$CONTAINER_NAME" curl -sf "$HEALTH_CHECK_URL" > /dev/null
}

echo "Waiting for $CONTAINER_NAME to be healthy..."
for i in $(seq 1 $MAX_RETRIES); do
    if check_health; then
        echo "Container is healthy!"
        exit 0
    fi
    echo "Attempt $i/$MAX_RETRIES failed, retrying in ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

echo "Health check failed after $MAX_RETRIES attempts"
exit 1
```

```bash
#!/bin/bash
# Example: Kubernetes deployment script

set -euo pipefail

NAMESPACE="${1:-default}"
DEPLOYMENT="${2:-}"
REPLICAS="${3:-3}"

if [ -z "$DEPLOYMENT" ]; then
    echo "Usage: $0 <namespace> <deployment> [replicas]"
    exit 1
fi

echo "Deploying $DEPLOYMENT to namespace $NAMESPACE..."

# Scale deployment
kubectl scale deployment "$DEPLOYMENT" --replicas="$REPLICAS" -n "$NAMESPACE"

# Wait for rollout
kubectl rollout status deployment/"$DEPLOYMENT" -n "$NAMESPACE" --timeout=5m

# Verify pods
PODS=$(kubectl get pods -n "$NAMESPACE" -l app="$DEPLOYMENT" -o jsonpath='{.items[*].metadata.name}')
for pod in $PODS; do
    echo "Checking pod: $pod"
    kubectl wait --for=condition=Ready pod/"$pod" -n "$NAMESPACE" --timeout=60s
done

echo "Deployment completed successfully!"
```

---

## 17. Performance Optimization

### Command Performance

```bash
# Time commands
time command
/usr/bin/time -v command         # Detailed timing

# Parallel execution
parallel command ::: arg1 arg2 arg3
parallel -j 4 command ::: args   # 4 jobs

# Background processing
command1 & command2 & command3 &
wait                              # Wait for all

# Process substitution
diff <(command1) <(command2)
```

### Resource Optimization

```bash
# Limit CPU
nice -n 10 command                # Lower priority
taskset -c 0,1 command            # Specific CPUs

# Limit memory
ulimit -v 1048576                 # Virtual memory (KB)
systemd-run --property=MemoryLimit=1G command

# I/O priority
ionice -c 2 -n 4 command          # Idle I/O class, nice 4
```

### Caching and Optimization

```bash
# Command caching (if using)
# Install: sudo apt install command-not-found
# Uses cache for faster command lookup

# SSH connection caching
# Add to ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m
```

---

## 18. Troubleshooting and Debugging

### Debugging Techniques

```bash
# Verbose mode
bash -x script.sh                 # Print commands
bash -v script.sh                 # Print input
bash -xv script.sh                # Both

# Debug specific section
set -x
# code to debug
set +x

# Check syntax
bash -n script.sh                 # Syntax check only

# Trace function calls
declare -ft function_name
set -T                            # Trace functions

# Debug with trap
trap 'echo "Line $LINENO: $BASH_COMMAND"' DEBUG
```

### System Debugging

```bash
# System information
uname -a
cat /etc/os-release
lscpu
free -h
df -h

# Process debugging
strace -p PID                     # System calls
ltrace -p PID                     # Library calls
lsof -p PID                       # Open files

# Network debugging
tcpdump -i eth0
wireshark                         # GUI (if installed)
ss -tulnp
netstat -tulnp

# Kernel debugging
dmesg                             # Kernel messages
dmesg | tail -50
journalctl -k                     # Kernel logs
```

---

## 19. Automation and Workflows

### Cron Jobs

```bash
# Edit crontab
crontab -e

# Examples
0 * * * * /path/to/script.sh                    # Hourly
0 0 * * * /path/to/backup.sh                    # Daily
0 0 * * 0 /path/to/weekly-task.sh               # Weekly
*/5 * * * * /path/to/frequent-task.sh           # Every 5 minutes
0 2 1 * * /path/to/monthly-task.sh              # Monthly

# System-wide cron
sudo vim /etc/crontab
sudo vim /etc/cron.d/custom

# Cron directories
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

### Systemd Timers

```bash
# Create timer unit
sudo vim /etc/systemd/system/backup.timer

[Unit]
Description=Backup Timer

[Timer]
OnCalendar=daily
OnBootSec=10min

[Install]
WantedBy=timers.target

# Create service unit
sudo vim /etc/systemd/system/backup.service

[Unit]
Description=Backup Service

[Service]
ExecStart=/path/to/backup.sh

# Enable and start
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
sudo systemctl list-timers
```

### Workflow Automation

```bash
#!/bin/bash
# Example: Automated deployment workflow

set -euo pipefail

deploy() {
    local environment=$1
    local version=$2
    
    echo "Deploying version $version to $environment..."
    
    # Build
    docker build -t app:$version .
    
    # Test
    docker run --rm app:$version npm test
    
    # Tag
    docker tag app:$version registry.example.com/app:$version
    
    # Push
    docker push registry.example.com/app:$version
    
    # Deploy
    kubectl set image deployment/app app=registry.example.com/app:$version -n $environment
    
    # Verify
    kubectl rollout status deployment/app -n $environment --timeout=5m
    
    echo "Deployment completed!"
}

# Usage
deploy "production" "v1.2.3"
```

---

## 20. Best Practices and Tips

### Best Practices

1. **Always use shebang**
   ```bash
   #!/bin/bash
   ```

2. **Set error handling**
   ```bash
   set -euo pipefail
   ```

3. **Use meaningful variable names**
   ```bash
   CONTAINER_NAME="myapp"
   MAX_RETRIES=30
   ```

4. **Quote variables**
   ```bash
   echo "$variable"  # Correct
   echo $variable    # Can break with spaces
   ```

5. **Use functions for reusable code**
   ```bash
   log_info() {
       echo "[INFO] $*"
   }
   ```

6. **Check command existence**
   ```bash
   if ! command -v docker &> /dev/null; then
       echo "Docker is not installed"
       exit 1
   fi
   ```

7. **Use local variables in functions**
   ```bash
   function_name() {
       local var="value"
   }
   ```

8. **Validate input**
   ```bash
   if [ -z "$1" ]; then
       echo "Usage: $0 <argument>"
       exit 1
   fi
   ```

9. **Use arrays for multiple values**
   ```bash
   SERVERS=("server1" "server2" "server3")
   for server in "${SERVERS[@]}"; do
       echo $server
   done
   ```

10. **Document your scripts**
    ```bash
    #!/bin/bash
    #
    # Script: deploy.sh
    # Description: Deploys application to Kubernetes
    # Usage: ./deploy.sh <environment> <version>
    # Author: DevOps Team
    # Date: 2024-01-01
    ```

### Useful Tips

```bash
# Quick directory navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Quick edits
alias edit='vim'
alias e='vim'

# Quick searches
alias h='history | grep'
alias f='find . -name'

# Quick system info
alias ports='netstat -tulanp'
alias meminfo='free -m -l -t'
alias psmem='ps auxf | sort -nr -k 4'
alias psmem10='ps auxf | sort -nr -k 4 | head -10'
alias pscpu='ps auxf | sort -nr -k 3'
alias pscpu10='ps auxf | sort -nr -k 3 | head -10'

# Quick Docker
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias dex='docker exec -it'
alias dlog='docker logs -f'

# Quick Kubernetes
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
alias kl='kubectl logs -f'

# Command history search
# Add to ~/.bashrc or ~/.zshrc
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
```

### Productivity Shortcuts

```bash
# Command line editing
Ctrl+A          # Move to beginning of line
Ctrl+E          # Move to end of line
Ctrl+U          # Delete to beginning of line
Ctrl+K          # Delete to end of line
Ctrl+W          # Delete word before cursor
Ctrl+Y          # Paste deleted text
Ctrl+R          # Search history
Ctrl+L          # Clear screen

# Job control
Ctrl+Z          # Suspend process
fg              # Resume in foreground
bg              # Resume in background
Ctrl+C          # Terminate process
Ctrl+D          # Exit shell

# Tab completion
Tab             # Complete command/file
Tab Tab         # Show all completions
```

---

## Conclusion

This master-level CLI tutorial covers essential command-line tools and techniques for DevOps engineers. Mastery of CLI is fundamental to efficient DevOps operations, enabling automation, troubleshooting, and infrastructure management.

### Key Takeaways

1. **Shell Mastery**: Understanding bash/zsh fundamentals is crucial
2. **Text Processing**: grep, sed, awk are powerful tools
3. **Container Tools**: Docker and Kubernetes CLI are essential
4. **Cloud CLIs**: AWS, Azure, GCP CLIs for cloud operations
5. **Automation**: Scripting enables repeatable operations
6. **Troubleshooting**: CLI tools are best for debugging
7. **Best Practices**: Follow conventions for maintainable scripts

### Next Steps

1. Practice daily with CLI tools
2. Build automation scripts for common tasks
3. Contribute to open-source projects using CLI
4. Explore advanced features of each tool
5. Stay updated with new CLI tools and features

### Resources

- **Bash Guide**: https://www.gnu.org/software/bash/manual/
- **Docker Docs**: https://docs.docker.com/
- **Kubernetes Docs**: https://kubernetes.io/docs/
- **AWS CLI Docs**: https://aws.amazon.com/cli/
- **Terraform Docs**: https://www.terraform.io/docs/

---

*Last Updated: 2024*
*Master-Level CLI for DevOps - Complete Tutorial*

