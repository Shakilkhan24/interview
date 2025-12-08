# Linux & Bash Scripting for DevOps Engineering Interviews
## Comprehensive Guide: Medium Basics to Advanced

---

## Table of Contents
1. [Linux Fundamentals](#1-linux-fundamentals)
2. [File System Operations](#2-file-system-operations)
3. [Process Management](#3-process-management)
4. [Text Processing & Manipulation](#4-text-processing--manipulation)
5. [System Monitoring & Performance](#5-system-monitoring--performance)
6. [Network Operations](#6-network-operations)
7. [User & Permission Management](#7-user--permission-management)
8. [Bash Scripting Basics](#8-bash-scripting-basics)
9. [Advanced Bash Scripting](#9-advanced-bash-scripting)
10. [System Administration Tasks](#10-system-administration-tasks)
11. [DevOps Automation Scenarios](#11-devops-automation-scenarios)
12. [Troubleshooting & Debugging](#12-troubleshooting--debugging)
13. [Security & Hardening](#13-security--hardening)
14. [Container & Orchestration Integration](#14-container--orchestration-integration)

---

## 1. Linux Fundamentals

### Problem 1.1: Understanding File Permissions and Ownership

**Scenario:** You need to set up a web server directory where:
- The web server (www-data) can read/write files
- Developers (dev group) can read/write
- Others can only read
- New files inherit group ownership

**Solution:**

```bash
#!/bin/bash
# Setup web directory with proper permissions

WEB_DIR="/var/www/myapp"
OWNER="www-data"
GROUP="dev"

# Create directory structure
sudo mkdir -p "$WEB_DIR"/{public,uploads,logs}
sudo chown -R "$OWNER:$GROUP" "$WEB_DIR"

# Set directory permissions (rwxrwxr-x)
sudo find "$WEB_DIR" -type d -exec chmod 775 {} \;

# Set file permissions (rw-rw-r--)
sudo find "$WEB_DIR" -type f -exec chmod 664 {} \;

# Set SGID bit so new files inherit group
sudo chmod g+s "$WEB_DIR"

# Set sticky bit on uploads (only owner can delete)
sudo chmod +t "$WEB_DIR/uploads"

# Verify
ls -ld "$WEB_DIR"
getfacl "$WEB_DIR"  # If ACLs are used
```

**Key Concepts:**
- **Octal permissions:** 755 = rwxr-xr-x, 644 = rw-r--r--
- **Special bits:** SUID (4), SGID (2), Sticky (1)
- **chmod:** Change permissions
- **chown:** Change ownership
- **umask:** Default permission mask (022 = files 644, dirs 755)

**Verification:**
```bash
stat -c "%a %U:%G %n" /var/www/myapp
getfacl /var/www/myapp
```

---

### Problem 1.2: Symbolic Links vs Hard Links

**Scenario:** Explain and demonstrate the difference between hard and symbolic links, and when to use each.

**Solution:**

```bash
#!/bin/bash
# Demonstrating hard links vs symbolic links

# Create test file
echo "Original content" > original.txt

# Create hard link
ln original.txt hardlink.txt

# Create symbolic link
ln -s original.txt symlink.txt

# Show inode numbers (hard links share same inode)
ls -li original.txt hardlink.txt symlink.txt

# Modify through hard link
echo "Modified via hard link" >> hardlink.txt
cat original.txt  # Shows modification

# Delete original
rm original.txt
cat hardlink.txt  # Still works (same inode)
cat symlink.txt   # Broken link (dangling)

# When to use:
# Hard links: Same filesystem, backup/redundancy, cannot link directories
# Symbolic links: Cross-filesystem, link directories, more flexible
```

**Key Differences:**
- **Hard link:** Same inode, works after original deleted, same filesystem only
- **Symbolic link:** Different inode, breaks if target deleted, can cross filesystems

---

### Problem 1.3: File System Hierarchy and Important Directories

**Scenario:** Identify and explain the purpose of critical Linux directories.

**Solution:**

```bash
#!/bin/bash
# Understanding Linux filesystem hierarchy

cat << 'EOF'
Critical Directories:

/ (root)
├── /bin     - Essential user binaries (ls, cp, mv)
├── /sbin    - System binaries (fdisk, ifconfig, mount)
├── /usr     - User programs and data
│   ├── /usr/bin    - User binaries
│   ├── /usr/sbin   - System admin binaries
│   └── /usr/local  - Locally installed software
├── /etc     - Configuration files
├── /var     - Variable data (logs, cache, spool)
│   ├── /var/log    - Log files
│   ├── /var/cache  - Cache files
│   └── /var/spool  - Spool files (cron, mail)
├── /tmp     - Temporary files (cleared on reboot)
├── /home    - User home directories
├── /root    - Root user home
├── /opt     - Optional/third-party software
├── /proc    - Process and kernel information (virtual)
├── /sys     - System and hardware information (virtual)
├── /dev     - Device files
├── /mnt     - Temporary mount points
├── /media   - Removable media mount points
└── /boot    - Boot loader files
EOF

# Find largest directories
du -h --max-depth=1 / 2>/dev/null | sort -hr | head -10

# Check disk usage by filesystem
df -h

# Find configuration files
find /etc -type f -name "*.conf" | head -20
```

---

## 2. File System Operations

### Problem 2.1: Find and Process Files Efficiently

**Scenario:** Find all log files older than 30 days, compress them, and move to archive directory.

**Solution:**

```bash
#!/bin/bash
# Archive old log files

LOG_DIR="/var/log/myapp"
ARCHIVE_DIR="/var/log/archive"
RETENTION_DAYS=30

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Find and archive logs older than retention period
find "$LOG_DIR" -type f -name "*.log" -mtime +$RETENTION_DAYS | while read -r logfile; do
    # Get directory structure
    rel_path="${logfile#$LOG_DIR/}"
    archive_path="$ARCHIVE_DIR/$(dirname "$rel_path")"
    mkdir -p "$archive_path"
    
    # Compress and move
    gzip -c "$logfile" > "$archive_path/$(basename "$logfile").gz"
    
    # Verify compression before deleting
    if [ -f "$archive_path/$(basename "$logfile").gz" ]; then
        rm "$logfile"
        echo "Archived: $logfile"
    else
        echo "ERROR: Failed to archive $logfile" >&2
    fi
done

# Alternative: Using find with -exec (more efficient)
find "$LOG_DIR" -type f -name "*.log" -mtime +$RETENTION_DAYS \
    -exec sh -c 'gzip -c "$1" > "$2/$(basename "$1").gz" && rm "$1"' _ {} "$ARCHIVE_DIR" \;

# Clean up empty directories
find "$LOG_DIR" -type d -empty -delete
```

**Key Commands:**
- `find`: Search for files
- `-mtime +30`: Modified more than 30 days ago
- `-exec`: Execute command on each file
- `xargs`: Pass arguments to command (alternative to -exec)

---

### Problem 2.2: Disk Space Management and Cleanup

**Scenario:** System is running out of disk space. Identify what's consuming space and clean up safely.

**Solution:**

```bash
#!/bin/bash
# Disk space analysis and cleanup

# Check overall disk usage
df -h

# Find largest files (top 20)
find / -type f -size +100M 2>/dev/null | xargs ls -lhS | head -20

# Find largest directories
du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20

# Clean package cache (Debian/Ubuntu)
sudo apt-get clean
sudo apt-get autoremove -y

# Clean package cache (RHEL/CentOS)
sudo yum clean all
sudo yum autoremove -y

# Clean Docker (if installed)
docker system prune -af --volumes

# Clean systemd journal logs (keep last 7 days)
sudo journalctl --vacuum-time=7d

# Clean temporary files
sudo find /tmp -type f -atime +7 -delete
sudo find /var/tmp -type f -atime +7 -delete

# Clean old kernels (keep current + 1)
# Ubuntu/Debian
OLD_KERNELS=$(dpkg -l | grep linux-image | awk '{print $2}' | grep -v $(uname -r) | grep -v $(uname -r | sed 's/-generic//'))
echo "$OLD_KERNELS" | xargs sudo apt-get purge -y

# Find and remove core dumps
find / -name "core.*" -type f -mtime +30 -delete 2>/dev/null

# Clean user caches
for user in /home/*; do
    if [ -d "$user/.cache" ]; then
        find "$user/.cache" -type f -atime +30 -delete
    fi
done

# Report final disk usage
echo "=== Final Disk Usage ==="
df -h
```

**Advanced: Disk usage by file type**

```bash
#!/bin/bash
# Analyze disk usage by file extension

find /var/log -type f -name "*.*" | \
    sed 's/.*\.//' | \
    sort | uniq -c | \
    sort -rn | \
    head -20 | \
    awk '{print $2, $1}'
```

---

### Problem 2.3: File Backup and Synchronization

**Scenario:** Create a robust backup script that backs up critical directories with rotation and verification.

**Solution:**

```bash
#!/bin/bash
# Comprehensive backup script with rotation

set -euo pipefail  # Exit on error, undefined vars, pipe failures

BACKUP_DIR="/backup"
SOURCE_DIRS=("/etc" "/var/www" "/home")
RETENTION_DAYS=30
BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
COMPRESSION="gzip"  # or "bzip2", "xz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Function to create backup
create_backup() {
    local source="$1"
    local dest="$BACKUP_DIR/$BACKUP_NAME"
    
    echo "Backing up $source to $dest"
    
    # Create directory structure
    mkdir -p "$dest"
    
    # Backup with tar and compression
    case $COMPRESSION in
        gzip)
            tar -czf "$dest/$(basename $source).tar.gz" -C "$(dirname $source)" "$(basename $source)"
            ;;
        bzip2)
            tar -cjf "$dest/$(basename $source).tar.bz2" -C "$(dirname $source)" "$(basename $source)"
            ;;
        xz)
            tar -cJf "$dest/$(basename $source).tar.xz" -C "$(dirname $source)" "$(basename $source)"
            ;;
    esac
    
    # Verify backup integrity
    local backup_file=""
    case $COMPRESSION in
        gzip)
            backup_file="$dest/$(basename $source).tar.gz"
            ;;
        bzip2)
            backup_file="$dest/$(basename $source).tar.bz2"
            ;;
        xz)
            backup_file="$dest/$(basename $source).tar.xz"
            ;;
    esac
    
    if [ -f "$backup_file" ]; then
        tar -tzf "$backup_file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✓ Backup verified: $source"
        else
            echo "✗ Backup verification failed: $source" >&2
            return 1
        fi
    fi
}

# Create backups
for dir in "${SOURCE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        create_backup "$dir"
    else
        echo "Warning: $dir does not exist, skipping"
    fi
done

# Create backup manifest
cat > "$BACKUP_DIR/$BACKUP_NAME/MANIFEST.txt" << EOF
Backup Date: $(date)
Hostname: $(hostname)
Source Directories: ${SOURCE_DIRS[@]}
Compression: $COMPRESSION
EOF

# Rotate old backups
find "$BACKUP_DIR" -type d -name "backup-*" -mtime +$RETENTION_DAYS -exec rm -rf {} \;

# Generate backup report
echo "=== Backup Report ==="
echo "Backup location: $BACKUP_DIR/$BACKUP_NAME"
du -sh "$BACKUP_DIR/$BACKUP_NAME"
echo "Old backups cleaned (older than $RETENTION_DAYS days)"
```

**Using rsync for incremental backups:**

```bash
#!/bin/bash
# Incremental backup with rsync

SOURCE="/var/www"
DEST="/backup/www"
RSYNC_OPTS="-avz --delete --link-dest=$DEST/latest"

# Create destination
mkdir -p "$DEST/$(date +%Y%m%d)"

# Perform backup
rsync $RSYNC_OPTS "$SOURCE/" "$DEST/$(date +%Y%m%d)/"

# Update latest symlink
ln -sfn "$DEST/$(date +%Y%m%d)" "$DEST/latest"

# Cleanup old backups (keep last 7)
ls -dt "$DEST"/[0-9]* | tail -n +8 | xargs rm -rf
```

---

## 3. Process Management

### Problem 3.1: Process Monitoring and Management

**Scenario:** Monitor a critical process, restart it if it dies, and log all events.

**Solution:**

```bash
#!/bin/bash
# Process watchdog script

PROCESS_NAME="myapp"
PIDFILE="/var/run/${PROCESS_NAME}.pid"
LOG_FILE="/var/log/${PROCESS_NAME}-watchdog.log"
MAX_RESTARTS=5
RESTART_WINDOW=300  # 5 minutes
RESTART_COUNT=0
LAST_RESTART=0

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_process() {
    if [ -f "$PIDFILE" ]; then
        local pid=$(cat "$PIDFILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Process is running
        else
            log_message "WARNING: PID file exists but process is not running"
            rm -f "$PIDFILE"
            return 1
        fi
    else
        # Check by process name
        if pgrep -f "$PROCESS_NAME" > /dev/null; then
            return 0
        else
            return 1
        fi
    fi
}

restart_process() {
    local current_time=$(date +%s)
    
    # Reset counter if outside restart window
    if [ $((current_time - LAST_RESTART)) -gt $RESTART_WINDOW ]; then
        RESTART_COUNT=0
    fi
    
    # Check restart limit
    if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
        log_message "ERROR: Max restarts ($MAX_RESTARTS) reached. Manual intervention required."
        exit 1
    fi
    
    log_message "Restarting $PROCESS_NAME (attempt $((RESTART_COUNT + 1)))"
    
    # Restart command (customize based on your service)
    systemctl restart "$PROCESS_NAME" || service "$PROCESS_NAME" restart
    
    sleep 5
    
    if check_process; then
        log_message "Successfully restarted $PROCESS_NAME"
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART=$current_time
    else
        log_message "ERROR: Failed to restart $PROCESS_NAME"
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART=$current_time
    fi
}

# Main monitoring loop
log_message "Starting watchdog for $PROCESS_NAME"

while true; do
    if ! check_process; then
        restart_process
    fi
    
    # Check process resource usage
    if [ -f "$PIDFILE" ]; then
        local pid=$(cat "$PIDFILE")
        local cpu=$(ps -p "$pid" -o %cpu --no-headers | tr -d ' ')
        local mem=$(ps -p "$pid" -o %mem --no-headers | tr -d ' ')
        
        # Alert on high resource usage
        if (( $(echo "$cpu > 90" | bc -l) )); then
            log_message "WARNING: High CPU usage: ${cpu}%"
        fi
        if (( $(echo "$mem > 90" | bc -l) )); then
            log_message "WARNING: High memory usage: ${mem}%"
        fi
    fi
    
    sleep 30
done
```

**Using systemd for process management:**

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/myapp
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

### Problem 3.2: Process Resource Monitoring

**Scenario:** Monitor system processes and identify resource-intensive processes.

**Solution:**

```bash
#!/bin/bash
# Process resource monitoring script

# Function to get top CPU processes
top_cpu_processes() {
    echo "=== Top 10 CPU Consuming Processes ==="
    ps aux --sort=-%cpu | head -11 | awk '{printf "%-8s %-6s %-6s %-50s\n", $1, $2, $3, $11}'
    echo
}

# Function to get top memory processes
top_memory_processes() {
    echo "=== Top 10 Memory Consuming Processes ==="
    ps aux --sort=-%mem | head -11 | awk '{printf "%-8s %-6s %-6s %-50s\n", $1, $2, $4, $11}'
    echo
}

# Function to monitor specific process
monitor_process() {
    local pid=$1
    local interval=${2:-5}
    
    while kill -0 "$pid" 2>/dev/null; do
        local stats=$(ps -p "$pid" -o pid,%cpu,%mem,vsz,rss,etime,cmd --no-headers)
        echo "[$(date '+%H:%M:%S')] $stats"
        sleep "$interval"
    done
    echo "Process $pid has terminated"
}

# Function to find processes by pattern
find_processes() {
    local pattern=$1
    echo "=== Processes matching '$pattern' ==="
    pgrep -af "$pattern" | while read -r line; do
        local pid=$(echo "$line" | awk '{print $1}')
        local stats=$(ps -p "$pid" -o pid,%cpu,%mem,etime,cmd --no-headers 2>/dev/null)
        echo "$stats"
    done
}

# Function to kill processes by pattern (with confirmation)
kill_processes() {
    local pattern=$1
    local signal=${2:-TERM}
    
    local pids=$(pgrep -f "$pattern")
    
    if [ -z "$pids" ]; then
        echo "No processes found matching '$pattern'"
        return
    fi
    
    echo "Found processes:"
    ps -p "$pids" -o pid,%cpu,%mem,cmd
    
    read -p "Kill these processes? (y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo "$pids" | xargs kill -$signal
        echo "Sent $signal signal to processes"
    else
        echo "Cancelled"
    fi
}

# Main menu
case "${1:-}" in
    cpu)
        top_cpu_processes
        ;;
    mem)
        top_memory_processes
        ;;
    monitor)
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 monitor <PID> [interval]"
            exit 1
        fi
        monitor_process "$2" "${3:-5}"
        ;;
    find)
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 find <pattern>"
            exit 1
        fi
        find_processes "$2"
        ;;
    kill)
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 kill <pattern> [signal]"
            exit 1
        fi
        kill_processes "$2" "${3:-TERM}"
        ;;
    *)
        top_cpu_processes
        top_memory_processes
        ;;
esac
```

---

## 4. Text Processing & Manipulation

### Problem 4.1: Advanced grep, sed, and awk Usage

**Scenario:** Parse and transform log files to extract meaningful information.

**Solution:**

```bash
#!/bin/bash
# Advanced text processing examples

LOG_FILE="/var/log/application.log"

# 1. Extract error messages with context
echo "=== Errors with 2 lines of context ==="
grep -A 2 -B 2 -i "error\|exception\|fatal" "$LOG_FILE" | head -50

# 2. Count occurrences by type
echo "=== Error type counts ==="
grep -i "error" "$LOG_FILE" | sed 's/.*\(ERROR\|WARN\|FATAL\).*/\1/' | sort | uniq -c | sort -rn

# 3. Extract IP addresses from logs
echo "=== Unique IP addresses ==="
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$LOG_FILE" | sort -u

# 4. Parse Apache/Nginx access logs with awk
echo "=== Top 10 requested URLs ==="
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

# 5. Extract timestamps and calculate time differences
echo "=== Request duration analysis ==="
awk '/duration/ {match($0, /duration=([0-9.]+)/, arr); print arr[1]}' "$LOG_FILE" | \
    awk '{sum+=$1; count++; if($1>max) max=$1; if(count==1) min=$1; if($1<min) min=$1} 
         END {printf "Avg: %.2f, Min: %.2f, Max: %.2f\n", sum/count, min, max}'

# 6. Replace text in multiple files
find /var/log -name "*.log" -type f -exec sed -i 's/old-hostname/new-hostname/g' {} \;

# 7. Extract JSON fields (if log contains JSON)
echo "=== Extract JSON fields ==="
grep -o '"user_id":"[^"]*"' "$LOG_FILE" | sed 's/"user_id":"\(.*\)"/\1/' | sort -u

# 8. Multi-line pattern matching
echo "=== Multi-line error blocks ==="
awk '/ERROR START/,/ERROR END/ {print}' "$LOG_FILE"

# 9. Advanced sed: Insert line after pattern
sed -i '/pattern/a\New line inserted' file.txt

# 10. Extract and format dates
echo "=== Date extraction and formatting ==="
grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$LOG_FILE" | sort -u
```

**Advanced awk script for log analysis:**

```bash
#!/usr/bin/awk -f
# Comprehensive log analyzer

BEGIN {
    FS=" "
    print "=== Log Analysis Report ==="
    print "Timestamp: " strftime("%Y-%m-%d %H:%M:%S")
    print ""
}

# Count by log level
/ERROR|FATAL/ { errors++ }
/WARN/ { warnings++ }
/INFO/ { info++ }
/DEBUG/ { debug++ }

# Track unique users
/user_id/ {
    match($0, /user_id=([0-9]+)/, arr)
    if (arr[1]) users[arr[1]]++
}

# Track response times
/duration=/ {
    match($0, /duration=([0-9.]+)/, arr)
    if (arr[1]) {
        duration_sum += arr[1]
        duration_count++
        if (arr[1] > max_duration) max_duration = arr[1]
    }
}

END {
    print "=== Summary ==="
    print "Errors/Fatal: " errors
    print "Warnings: " warnings
    print "Info: " info
    print "Debug: " debug
    print ""
    print "=== Performance ==="
    if (duration_count > 0) {
        print "Avg Duration: " (duration_sum / duration_count) "ms"
        print "Max Duration: " max_duration "ms"
    }
    print ""
    print "=== Unique Users ==="
    print "Total: " length(users)
}
```

---

### Problem 4.2: CSV/Data File Processing

**Scenario:** Process CSV files, calculate statistics, and generate reports.

**Solution:**

```bash
#!/bin/bash
# CSV processing script

CSV_FILE="data.csv"
OUTPUT_FILE="report.txt"

# Function to calculate column statistics
calculate_stats() {
    local col_num=$1
    local col_name=$2
    
    echo "=== $col_name Statistics ==="
    
    # Extract column, skip header, calculate stats
    awk -F',' -v col=$col_num 'NR>1 {
        sum+=$col
        count++
        values[count]=$col
        if(count==1 || $col<min) min=$col
        if(count==1 || $col>max) max=$col
    }
    END {
        if(count>0) {
            avg=sum/count
            # Calculate median
            asort(values)
            if(count%2==0) {
                median=(values[count/2]+values[count/2+1])/2
            } else {
                median=values[int(count/2)+1]
            }
            # Calculate standard deviation
            sq_diff_sum=0
            for(i=1;i<=count;i++) {
                sq_diff_sum+=(values[i]-avg)^2
            }
            stddev=sqrt(sq_diff_sum/count)
            
            printf "Count: %d\n", count
            printf "Sum: %.2f\n", sum
            printf "Average: %.2f\n", avg
            printf "Median: %.2f\n", median
            printf "Min: %.2f\n", min
            printf "Max: %.2f\n", max
            printf "Std Dev: %.2f\n", stddev
        }
    }' "$CSV_FILE"
}

# Function to filter and export
filter_csv() {
    local condition=$1
    local output=$2
    
    # Example: filter where column 3 > 100
    awk -F',' -v condition="$condition" '
    BEGIN { print "Filtering with condition: " condition }
    NR==1 { print }  # Header
    ' "$CSV_FILE" > "$output"
    
    # Apply filter (simplified - would need proper parsing)
    awk -F',' 'NR>1 && $3 > 100' "$CSV_FILE" >> "$output"
}

# Function to join CSV files
join_csv() {
    local file1=$1
    local file2=$2
    local key_col1=$3
    local key_col2=$4
    
    awk -F',' -v key1=$key_col1 -v key2=$key_col2 '
    NR==FNR {
        # Read first file into array
        key=$key1
        $key1=""
        data[key]=$0
        next
    }
    {
        # Process second file
        key=$key2
        if (key in data) {
            print $0 "," data[key]
        }
    }' "$file1" "$file2"
}

# Generate report
{
    echo "CSV Analysis Report"
    echo "Generated: $(date)"
    echo "File: $CSV_FILE"
    echo ""
    
    # Count rows and columns
    total_rows=$(wc -l < "$CSV_FILE")
    total_cols=$(head -1 "$CSV_FILE" | awk -F',' '{print NF}')
    echo "Total Rows: $((total_rows - 1))"  # Exclude header
    echo "Total Columns: $total_cols"
    echo ""
    
    # Calculate stats for numeric columns
    calculate_stats 3 "Sales"
    echo ""
    calculate_stats 4 "Profit"
    
} > "$OUTPUT_FILE"

cat "$OUTPUT_FILE"
```

---

## 5. System Monitoring & Performance

### Problem 5.1: System Resource Monitoring Script

**Scenario:** Create a comprehensive system monitoring script that tracks CPU, memory, disk, and network usage.

**Solution:**

```bash
#!/bin/bash
# Comprehensive system monitoring script

INTERVAL=${1:-5}  # Default 5 seconds
DURATION=${2:-60}  # Default 60 seconds
LOG_FILE="/tmp/system_monitor_$(date +%Y%m%d_%H%M%S).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

get_cpu_usage() {
    # Get CPU usage (average over 1 second)
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}'
}

get_memory_usage() {
    # Get memory usage percentage
    free | grep Mem | awk '{printf "%.2f", ($3/$2) * 100.0}'
}

get_disk_usage() {
    local mount_point=${1:-/}
    df -h "$mount_point" | awk 'NR==2 {print $5}' | sed 's/%//'
}

get_disk_io() {
    # Get disk I/O stats (requires iostat or reading /proc/diskstats)
    if command -v iostat &> /dev/null; then
        iostat -x 1 1 | awk '/^[a-z]/ {print $1, $10, $11}' | tail -n +2
    else
        # Parse /proc/diskstats
        cat /proc/diskstats | awk '{print $3, $4, $8}'
    fi
}

get_network_stats() {
    # Get network interface statistics
    cat /proc/net/dev | awk '
    BEGIN {
        print "Interface RX-Bytes TX-Bytes"
    }
    /:/ {
        gsub(/:/, "", $1)
        if ($1 != "lo") {
            printf "%-10s %12s %12s\n", $1, $2, $10
        }
    }'
}

get_top_processes() {
    echo "=== Top 5 CPU Processes ==="
    ps aux --sort=-%cpu | head -6 | awk '{printf "%-8s %6s %6s %s\n", $1, $2, $3"%", $11}'
    echo ""
    echo "=== Top 5 Memory Processes ==="
    ps aux --sort=-%mem | head -6 | awk '{printf "%-8s %6s %6s %s\n", $1, $2, $4"%", $11}'
}

check_thresholds() {
    local cpu=$(get_cpu_usage)
    local mem=$(get_memory_usage)
    local disk=$(get_disk_usage)
    
    # CPU threshold: 80%
    if (( $(echo "$cpu > 80" | bc -l) )); then
        echo -e "${RED}WARNING: High CPU usage: ${cpu}%${NC}"
        log_message "WARNING: High CPU usage: ${cpu}%"
    fi
    
    # Memory threshold: 85%
    if (( $(echo "$mem > 85" | bc -l) )); then
        echo -e "${RED}WARNING: High memory usage: ${mem}%${NC}"
        log_message "WARNING: High memory usage: ${mem}%"
    fi
    
    # Disk threshold: 90%
    if [ "$disk" -gt 90 ]; then
        echo -e "${RED}WARNING: High disk usage: ${disk}%${NC}"
        log_message "WARNING: High disk usage: ${disk}%"
    fi
}

# Main monitoring loop
echo "Starting system monitoring..."
echo "Interval: ${INTERVAL}s, Duration: ${DURATION}s"
echo "Log file: $LOG_FILE"
echo ""

end_time=$(($(date +%s) + DURATION))

while [ $(date +%s) -lt $end_time ]; do
    clear
    echo "=== System Monitor - $(date) ==="
    echo ""
    
    # CPU
    cpu_usage=$(get_cpu_usage)
    echo -e "CPU Usage: ${GREEN}${cpu_usage}%${NC}"
    
    # Memory
    mem_usage=$(get_memory_usage)
    echo -e "Memory Usage: ${GREEN}${mem_usage}%${NC}"
    
    # Disk
    disk_usage=$(get_disk_usage)
    echo -e "Disk Usage (/): ${GREEN}${disk_usage}%${NC}"
    
    # Load Average
    load_avg=$(uptime | awk -F'load average:' '{print $2}')
    echo "Load Average: $load_avg"
    
    echo ""
    get_top_processes
    
    echo ""
    check_thresholds
    
    sleep "$INTERVAL"
done

echo ""
echo "Monitoring completed. Log saved to: $LOG_FILE"
```

---

### Problem 5.2: Performance Tuning and Optimization

**Scenario:** Identify and resolve performance bottlenecks in a Linux system.

**Solution:**

```bash
#!/bin/bash
# Performance tuning and optimization script

echo "=== System Performance Analysis ==="

# 1. Check CPU information
echo "=== CPU Information ==="
echo "CPU Cores: $(nproc)"
echo "CPU Model: $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
echo ""

# 2. Check memory
echo "=== Memory Information ==="
free -h
echo ""
echo "Swappiness: $(cat /proc/sys/vm/swappiness)"
echo "Dirty ratio: $(cat /proc/sys/vm/dirty_ratio)"
echo ""

# 3. Check I/O wait
echo "=== I/O Statistics ==="
iostat -x 1 2 2>/dev/null || echo "iostat not available"
echo ""

# 4. Check network
echo "=== Network Statistics ==="
ss -s
echo ""

# 5. Check file descriptors
echo "=== File Descriptor Usage ==="
echo "System limit: $(cat /proc/sys/fs/file-max)"
echo "Current usage: $(cat /proc/sys/fs/file-nr | awk '{print $1}')"
for pid in $(pgrep -f "myapp"); do
    echo "PID $pid: $(ls /proc/$pid/fd 2>/dev/null | wc -l) file descriptors"
done
echo ""

# 6. Check kernel parameters
echo "=== Kernel Parameters ==="
echo "TCP keepalive: $(sysctl net.ipv4.tcp_keepalive_time)"
echo "TCP max connections: $(sysctl net.core.somaxconn)"
echo "TCP fin timeout: $(sysctl net.ipv4.tcp_fin_timeout)"
echo ""

# Performance optimization recommendations
echo "=== Optimization Recommendations ==="

# Memory optimization
if [ $(cat /proc/sys/vm/swappiness) -gt 10 ]; then
    echo "1. Consider reducing swappiness (currently: $(cat /proc/sys/vm/swappiness))"
    echo "   sudo sysctl vm.swappiness=10"
    echo "   Add to /etc/sysctl.conf: vm.swappiness=10"
fi

# Network optimization
if [ $(sysctl -n net.core.somaxconn) -lt 1024 ]; then
    echo "2. Increase max connections backlog"
    echo "   sudo sysctl -w net.core.somaxconn=4096"
fi

# File descriptor limits
echo "3. Check and increase file descriptor limits in /etc/security/limits.conf"
echo "   * soft nofile 65536"
echo "   * hard nofile 65536"

# I/O scheduler
echo "4. Check I/O scheduler (should be deadline or noop for SSDs)"
for disk in /sys/block/sd*/queue/scheduler; do
    echo "   $(dirname $disk | cut -d/ -f4): $(cat $disk | grep -o '\[.*\]')"
done

# CPU governor
echo "5. Check CPU frequency governor"
if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]; then
    echo "   Current: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)"
    echo "   For performance: echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
fi
```

---

## 6. Network Operations

### Problem 6.1: Network Troubleshooting and Analysis

**Scenario:** Diagnose network connectivity issues and analyze network traffic.

**Solution:**

```bash
#!/bin/bash
# Network troubleshooting script

TARGET_HOST=${1:-google.com}
PORT=${2:-80}

echo "=== Network Diagnostics for $TARGET_HOST ==="
echo ""

# 1. Basic connectivity
echo "1. Ping test:"
if ping -c 3 -W 2 "$TARGET_HOST" &> /dev/null; then
    echo "   ✓ Host is reachable"
    ping -c 3 "$TARGET_HOST" | tail -1
else
    echo "   ✗ Host is not reachable"
fi
echo ""

# 2. DNS resolution
echo "2. DNS resolution:"
if host "$TARGET_HOST" &> /dev/null; then
    echo "   ✓ DNS resolution successful"
    host "$TARGET_HOST" | head -1
else
    echo "   ✗ DNS resolution failed"
    echo "   Checking /etc/resolv.conf:"
    cat /etc/resolv.conf
fi
echo ""

# 3. Port connectivity
echo "3. Port $PORT connectivity:"
if command -v nc &> /dev/null; then
    if nc -zv -w 2 "$TARGET_HOST" "$PORT" &> /dev/null; then
        echo "   ✓ Port $PORT is open"
    else
        echo "   ✗ Port $PORT is closed or filtered"
    fi
else
    echo "   netcat not installed, skipping port test"
fi
echo ""

# 4. Traceroute
echo "4. Network path:"
if command -v traceroute &> /dev/null; then
    traceroute -m 15 "$TARGET_HOST" 2>/dev/null | head -10
elif command -v tracepath &> /dev/null; then
    tracepath "$TARGET_HOST" 2>/dev/null | head -10
else
    echo "   Traceroute not available"
fi
echo ""

# 5. Network interfaces
echo "5. Network interfaces:"
ip addr show | grep -E "^[0-9]+:|inet " | sed 's/^[0-9]*: /   /'
echo ""

# 6. Routing table
echo "6. Routing table:"
ip route show | head -10
echo ""

# 7. Active connections
echo "7. Active connections (top 10):"
ss -tun | head -11
echo ""

# 8. Network statistics
echo "8. Network statistics:"
ss -s
echo ""

# 9. Check listening ports
echo "9. Listening ports:"
ss -tlnp | grep LISTEN | head -10
echo ""

# 10. Firewall status
echo "10. Firewall status:"
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --state 2>/dev/null && echo "   firewalld is active"
elif command -v ufw &> /dev/null; then
    ufw status | head -5
elif [ -f /etc/iptables/rules.v4 ]; then
    echo "   iptables rules found"
    iptables -L -n | head -10
else
    echo "   No firewall detected or not configured"
fi
```

**Network traffic analysis:**

```bash
#!/bin/bash
# Network traffic capture and analysis

INTERFACE=${1:-eth0}
DURATION=${2:-60}
CAPTURE_FILE="/tmp/capture_$(date +%Y%m%d_%H%M%S).pcap"

echo "Capturing traffic on $INTERFACE for $DURATION seconds..."

# Capture traffic (requires tcpdump)
if command -v tcpdump &> /dev/null; then
    timeout "$DURATION" tcpdump -i "$INTERFACE" -w "$CAPTURE_FILE" -n
    
    echo ""
    echo "=== Traffic Analysis ==="
    
    # Top talkers
    echo "Top 10 source IPs:"
    tcpdump -r "$CAPTURE_FILE" -n 2>/dev/null | \
        awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -10
    
    echo ""
    echo "Top 10 destination IPs:"
    tcpdump -r "$CAPTURE_FILE" -n 2>/dev/null | \
        awk '{print $5}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head -10
    
    echo ""
    echo "Protocol distribution:"
    tcpdump -r "$CAPTURE_FILE" -n 2>/dev/null | \
        awk '{print $1}' | sort | uniq -c | sort -rn
    
    echo ""
    echo "Capture saved to: $CAPTURE_FILE"
    echo "Analyze with: tcpdump -r $CAPTURE_FILE"
else
    echo "tcpdump not installed"
fi
```

---

## 7. User & Permission Management

### Problem 7.1: User Account Management and Automation

**Scenario:** Create a script to manage user accounts with proper permissions, home directories, and SSH keys.

**Solution:**

```bash
#!/bin/bash
# User management script

set -euo pipefail

USERNAME=""
USER_GROUP="developers"
HOME_BASE="/home"
SSH_KEY=""
ACTION="create"  # create, delete, modify, list

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -a, --action ACTION     Action to perform (create, delete, modify, list)
    -u, --username USER      Username
    -g, --group GROUP        Primary group (default: developers)
    -k, --ssh-key KEY        SSH public key file
    -h, --help              Show this help

Examples:
    $0 -a create -u john -g developers -k ~/.ssh/id_rsa.pub
    $0 -a delete -u john
    $0 -a list
EOF
}

create_user() {
    local username=$1
    local group=$2
    local ssh_key=$3
    
    # Check if user exists
    if id "$username" &>/dev/null; then
        echo "Error: User $username already exists"
        return 1
    fi
    
    # Create group if it doesn't exist
    if ! getent group "$group" > /dev/null; then
        groupadd "$group"
        echo "Created group: $group"
    fi
    
    # Create user
    useradd -m -d "$HOME_BASE/$username" -g "$group" -s /bin/bash "$username"
    echo "Created user: $username"
    
    # Set up SSH key
    if [ -n "$ssh_key" ] && [ -f "$ssh_key" ]; then
        local ssh_dir="$HOME_BASE/$username/.ssh"
        mkdir -p "$ssh_dir"
        chmod 700 "$ssh_dir"
        cp "$ssh_key" "$ssh_dir/authorized_keys"
        chmod 600 "$ssh_dir/authorized_keys"
        chown -R "$username:$group" "$ssh_dir"
        echo "SSH key configured"
    fi
    
    # Set up sudo access (optional)
    echo "$username ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/docker" > "/etc/sudoers.d/$username"
    chmod 440 "/etc/sudoers.d/$username"
    
    # Generate random password
    local password=$(openssl rand -base64 12)
    echo "$username:$password" | chpasswd
    echo "Password set for $username"
    
    # Log creation
    logger "User $username created by $(whoami)"
    
    echo "User $username created successfully"
    echo "Home directory: $HOME_BASE/$username"
    echo "Group: $group"
}

delete_user() {
    local username=$1
    
    if ! id "$username" &>/dev/null; then
        echo "Error: User $username does not exist"
        return 1
    fi
    
    read -p "Delete home directory for $username? (y/N): " delete_home
    read -p "Are you sure you want to delete user $username? (y/N): " confirm
    
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        if [[ "$delete_home" =~ ^[Yy]$ ]]; then
            userdel -r "$username"
            echo "User $username and home directory deleted"
        else
            userdel "$username"
            echo "User $username deleted (home directory preserved)"
        fi
        
        # Remove sudo access
        rm -f "/etc/sudoers.d/$username"
        
        logger "User $username deleted by $(whoami)"
    else
        echo "Cancelled"
    fi
}

list_users() {
    echo "=== System Users ==="
    getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3, $6}' | \
        column -t -N "Username,UID,Home"
    
    echo ""
    echo "=== Groups ==="
    getent group | awk -F: '$3 >= 1000 && $3 < 65534 {print $1, $3}' | \
        column -t -N "Group,GID"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -a|--action)
            ACTION="$2"
            shift 2
            ;;
        -u|--username)
            USERNAME="$2"
            shift 2
            ;;
        -g|--group)
            USER_GROUP="$2"
            shift 2
            ;;
        -k|--ssh-key)
            SSH_KEY="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Execute action
case "$ACTION" in
    create)
        if [ -z "$USERNAME" ]; then
            echo "Error: Username required for create action"
            exit 1
        fi
        create_user "$USERNAME" "$USER_GROUP" "$SSH_KEY"
        ;;
    delete)
        if [ -z "$USERNAME" ]; then
            echo "Error: Username required for delete action"
            exit 1
        fi
        delete_user "$USERNAME"
        ;;
    list)
        list_users
        ;;
    *)
        echo "Error: Unknown action: $ACTION"
        usage
        exit 1
        ;;
esac
```

---

## 8. Bash Scripting Basics

### Problem 8.1: Robust Script Writing Practices

**Scenario:** Write a production-ready bash script with error handling, logging, and configuration.

**Solution:**

```bash
#!/bin/bash
# Production-ready script template

set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'        # Internal Field Separator

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/${SCRIPT_NAME%.sh}_$(date +%Y%m%d).log"
LOCK_FILE="/tmp/${SCRIPT_NAME}.lock"
CONFIG_FILE="${SCRIPT_DIR}/config.conf"

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Functions
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
    
    case $level in
        ERROR)
            echo -e "${RED}[ERROR]${NC} $message" >&2
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        INFO)
            echo -e "${GREEN}[INFO]${NC} $message"
            ;;
    esac
}

error_exit() {
    log ERROR "$1"
    cleanup
    exit "${2:-1}"
}

cleanup() {
    log INFO "Cleaning up..."
    rm -f "$LOCK_FILE"
}

check_lock() {
    if [ -f "$LOCK_FILE" ]; then
        local pid=$(cat "$LOCK_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            error_exit "Another instance is already running (PID: $pid)"
        else
            log WARN "Stale lock file found, removing"
            rm -f "$LOCK_FILE"
        fi
    fi
    echo $$ > "$LOCK_FILE"
}

load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        log INFO "Loading configuration from $CONFIG_FILE"
        # shellcheck source=/dev/null
        source "$CONFIG_FILE"
    else
        log WARN "Configuration file not found, using defaults"
    fi
}

validate_requirements() {
    local missing=()
    
    for cmd in "$@"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        error_exit "Missing required commands: ${missing[*]}"
    fi
}

# Signal handlers
trap cleanup EXIT
trap 'error_exit "Script interrupted"' INT TERM

# Main execution
main() {
    log INFO "Starting $SCRIPT_NAME"
    
    # Setup
    mkdir -p "$LOG_DIR"
    check_lock
    load_config
    validate_requirements "grep" "awk"
    
    # Your script logic here
    log INFO "Processing..."
    
    # Example: Process files
    if [ -d "${SOURCE_DIR:-/tmp}" ]; then
        local count=0
        while IFS= read -r -d '' file; do
            log INFO "Processing: $file"
            ((count++))
        done < <(find "${SOURCE_DIR}" -type f -print0 2>/dev/null)
        
        log INFO "Processed $count files"
    else
        log WARN "Source directory not found: ${SOURCE_DIR:-/tmp}"
    fi
    
    log INFO "Script completed successfully"
}

# Run main function
main "$@"
```

**Key Practices:**
- `set -euo pipefail`: Fail fast on errors
- Lock files: Prevent concurrent execution
- Logging: Structured logging with levels
- Error handling: Proper cleanup on exit
- Configuration: External config files
- Validation: Check requirements before execution
- Signal handling: Graceful shutdown

---

### Problem 8.2: Function Libraries and Modular Scripts

**Scenario:** Create reusable function libraries for common operations.

**Solution:**

```bash
# lib/common.sh - Common utility functions

# String operations
trim() {
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"  # Remove leading whitespace
    var="${var%"${var##*[![:space:]]}"}"  # Remove trailing whitespace
    echo -n "$var"
}

is_empty() {
    local var=$1
    [ -z "${var:-}" ]
}

is_number() {
    local var=$1
    [[ "$var" =~ ^[0-9]+$ ]]
}

# File operations
file_exists() {
    [ -f "$1" ]
}

dir_exists() {
    [ -d "$1" ]
}

backup_file() {
    local file=$1
    if [ -f "$file" ]; then
        cp "$file" "${file}.bak.$(date +%Y%m%d_%H%M%S)"
    fi
}

# System operations
is_root() {
    [ "$EUID" -eq 0 ]
}

require_root() {
    if ! is_root; then
        echo "Error: This script requires root privileges" >&2
        exit 1
    fi
}

# Network operations
is_host_reachable() {
    local host=$1
    ping -c 1 -W 2 "$host" &> /dev/null
}

is_port_open() {
    local host=$1
    local port=$2
    timeout 2 bash -c "echo >/dev/tcp/$host/$port" &>/dev/null
}

# Usage in main script:
# source "$(dirname "$0")/lib/common.sh"
# if is_host_reachable "google.com"; then
#     echo "Host is reachable"
# fi
```

---

## 9. Advanced Bash Scripting

### Problem 9.1: Parallel Processing and Job Control

**Scenario:** Process multiple files in parallel with controlled concurrency.

**Solution:**

```bash
#!/bin/bash
# Parallel processing with job control

set -euo pipefail

MAX_JOBS=4  # Maximum concurrent jobs
FILES_DIR="/data/files"
OUTPUT_DIR="/data/processed"

# Job queue
declare -a PIDS=()

# Function to process a single file
process_file() {
    local file=$1
    local output="${OUTPUT_DIR}/$(basename "$file").processed"
    
    echo "Processing: $file"
    # Simulate processing
    sleep $((RANDOM % 5 + 1))
    
    # Your processing logic here
    cp "$file" "$output"
    
    echo "Completed: $file"
    return 0
}

# Function to wait for jobs and maintain concurrency
wait_for_jobs() {
    while [ ${#PIDS[@]} -ge $MAX_JOBS ]; do
        for i in "${!PIDS[@]}"; do
            if ! kill -0 "${PIDS[$i]}" 2>/dev/null; then
                # Job completed
                wait "${PIDS[$i]}"
                unset "PIDS[$i]"
            fi
        done
        # Rebuild array (remove gaps)
        PIDS=("${PIDS[@]}")
        sleep 0.1
    done
}

# Main processing loop
main() {
    mkdir -p "$OUTPUT_DIR"
    
    # Process files
    while IFS= read -r -d '' file; do
        wait_for_jobs
        
        # Start background job
        process_file "$file" &
        PIDS+=($!)
        
    done < <(find "$FILES_DIR" -type f -print0)
    
    # Wait for all remaining jobs
    echo "Waiting for all jobs to complete..."
    for pid in "${PIDS[@]}"; do
        wait "$pid"
    done
    
    echo "All files processed"
}

# Alternative: Using GNU parallel (if available)
process_with_parallel() {
    if command -v parallel &> /dev/null; then
        find "$FILES_DIR" -type f | \
            parallel -j "$MAX_JOBS" process_file {}
    else
        echo "GNU parallel not installed, using built-in job control"
        main
    fi
}

main
```

---

### Problem 9.2: Advanced Error Handling and Retry Logic

**Scenario:** Implement robust error handling with exponential backoff retry.

**Solution:**

```bash
#!/bin/bash
# Advanced error handling with retry logic

set -euo pipefail

MAX_RETRIES=5
INITIAL_DELAY=1
MAX_DELAY=60
MULTIPLIER=2

# Retry function with exponential backoff
retry_with_backoff() {
    local cmd="$*"
    local attempt=1
    local delay=$INITIAL_DELAY
    
    while [ $attempt -le $MAX_RETRIES ]; do
        echo "Attempt $attempt/$MAX_RETRIES: $cmd"
        
        if eval "$cmd"; then
            echo "Success on attempt $attempt"
            return 0
        else
            local exit_code=$?
            echo "Failed with exit code $exit_code"
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "Waiting ${delay}s before retry..."
                sleep "$delay"
                delay=$((delay * MULTIPLIER))
                if [ $delay -gt $MAX_DELAY ]; then
                    delay=$MAX_DELAY
                fi
            fi
        fi
        
        ((attempt++))
    done
    
    echo "All $MAX_RETRIES attempts failed"
    return 1
}

# Example usage
retry_with_backoff "curl -f https://api.example.com/data" || {
    echo "Failed to fetch data after retries"
    exit 1
}

# Function with timeout
execute_with_timeout() {
    local timeout=$1
    shift
    local cmd="$*"
    
    if timeout "$timeout" bash -c "$cmd"; then
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo "Command timed out after ${timeout}s"
        else
            echo "Command failed with exit code $exit_code"
        fi
        return $exit_code
    fi
}

# Usage
execute_with_timeout 30 "long_running_command"
```

---

## 10. System Administration Tasks

### Problem 10.1: Automated System Maintenance

**Scenario:** Create a comprehensive system maintenance script.

**Solution:**

```bash
#!/bin/bash
# System maintenance script

set -euo pipefail

LOG_FILE="/var/log/maintenance.log"
REPORT_EMAIL="admin@example.com"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 1. Update system packages
update_packages() {
    log "Starting package updates..."
    
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get upgrade -y
        apt-get autoremove -y
        apt-get autoclean
    elif command -v yum &> /dev/null; then
        yum update -y
        yum autoremove -y
    elif command -v dnf &> /dev/null; then
        dnf update -y
        dnf autoremove -y
    fi
    
    log "Package updates completed"
}

# 2. Clean temporary files
clean_temp_files() {
    log "Cleaning temporary files..."
    
    find /tmp -type f -atime +7 -delete 2>/dev/null || true
    find /var/tmp -type f -atime +7 -delete 2>/dev/null || true
    
    log "Temporary files cleaned"
}

# 3. Rotate logs
rotate_logs() {
    log "Rotating logs..."
    
    # Use logrotate if available
    if [ -f /etc/logrotate.conf ]; then
        logrotate -f /etc/logrotate.conf
    fi
    
    # Clean old journal logs
    if command -v journalctl &> /dev/null; then
        journalctl --vacuum-time=30d
    fi
    
    log "Log rotation completed"
}

# 4. Check disk space
check_disk_space() {
    log "Checking disk space..."
    
    df -h | awk 'NR>1 {if ($5+0 > 90) print "WARNING: " $6 " is " $5 " full"}'
    
    log "Disk space check completed"
}

# 5. Check system health
check_system_health() {
    log "Checking system health..."
    
    # Memory
    local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    if [ "$mem_usage" -gt 90 ]; then
        log "WARNING: High memory usage: ${mem_usage}%"
    fi
    
    # Load average
    local load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
    local cores=$(nproc)
    if (( $(echo "$load > $cores * 2" | bc -l) )); then
        log "WARNING: High load average: $load"
    fi
    
    log "System health check completed"
}

# 6. Backup critical files
backup_critical_files() {
    log "Backing up critical files..."
    
    local backup_dir="/backup/$(date +%Y%m%d)"
    mkdir -p "$backup_dir"
    
    # Backup /etc
    tar -czf "$backup_dir/etc_backup.tar.gz" /etc 2>/dev/null || true
    
    # Backup database (if applicable)
    if command -v mysqldump &> /dev/null; then
        mysqldump --all-databases > "$backup_dir/mysql_backup.sql" 2>/dev/null || true
    fi
    
    log "Backup completed: $backup_dir"
}

# Main execution
main() {
    log "=== System Maintenance Started ==="
    
    update_packages
    clean_temp_files
    rotate_logs
    check_disk_space
    check_system_health
    backup_critical_files
    
    log "=== System Maintenance Completed ==="
    
    # Send report
    if command -v mail &> /dev/null; then
        mail -s "System Maintenance Report" "$REPORT_EMAIL" < "$LOG_FILE"
    fi
}

main
```

---

## 11. DevOps Automation Scenarios

### Problem 11.1: Application Deployment Script

**Scenario:** Create a deployment script with rollback capability.

**Solution:**

```bash
#!/bin/bash
# Application deployment script with rollback

set -euo pipefail

APP_NAME="myapp"
APP_DIR="/opt/$APP_NAME"
BACKUP_DIR="/opt/backups/$APP_NAME"
DEPLOY_USER="deploy"
VERSION=${1:-latest}
LOG_FILE="/var/log/${APP_NAME}-deploy.log"

# Logging function
log() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Functions
backup_current_version() {
    local backup_path="${BACKUP_DIR}/$(date +%Y%m%d_%H%M%S)"
    
    log "Creating backup at $backup_path"
    mkdir -p "$backup_path"
    
    if [ -d "$APP_DIR" ]; then
        cp -r "$APP_DIR" "$backup_path/"
        echo "$backup_path" > "${BACKUP_DIR}/.last_backup"
        log "Backup created: $backup_path"
    else
        log "No existing installation to backup"
    fi
}

deploy_new_version() {
    log "Deploying version $VERSION"
    
    # Download/Extract new version
    # This is a placeholder - adapt to your deployment method
    if [ "$VERSION" = "latest" ]; then
        # Pull from repository
        git clone https://github.com/org/repo.git "$APP_DIR.new" || true
        cd "$APP_DIR.new"
        git pull origin main
    else
        # Deploy specific version
        wget "https://releases.example.com/$APP_NAME-$VERSION.tar.gz"
        tar -xzf "$APP_NAME-$VERSION.tar.gz" -C "$APP_DIR.new"
    fi
    
    # Run pre-deployment checks
    if [ -f "$APP_DIR.new/scripts/pre-deploy.sh" ]; then
        bash "$APP_DIR.new/scripts/pre-deploy.sh"
    fi
    
    # Stop application
    systemctl stop "$APP_NAME" || service "$APP_NAME" stop || true
    
    # Swap directories
    if [ -d "$APP_DIR" ]; then
        mv "$APP_DIR" "${APP_DIR}.old"
    fi
    mv "$APP_DIR.new" "$APP_DIR"
    
    # Set permissions
    chown -R "$DEPLOY_USER:$DEPLOY_USER" "$APP_DIR"
    
    # Run database migrations (if applicable)
    if [ -f "$APP_DIR/scripts/migrate.sh" ]; then
        sudo -u "$DEPLOY_USER" bash "$APP_DIR/scripts/migrate.sh"
    fi
    
    # Start application
    systemctl start "$APP_NAME" || service "$APP_NAME" start
    
    # Health check
    sleep 5
    if health_check; then
        log "Deployment successful"
        rm -rf "${APP_DIR}.old"
        return 0
    else
        log "Health check failed, rolling back"
        rollback
        return 1
    fi
}

health_check() {
    local max_attempts=10
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8080/health &> /dev/null; then
            return 0
        fi
        sleep 2
        ((attempt++))
    done
    
    return 1
}

rollback() {
    local last_backup=$(cat "${BACKUP_DIR}/.last_backup" 2>/dev/null || echo "")
    
    if [ -z "$last_backup" ] || [ ! -d "$last_backup/$APP_NAME" ]; then
        log "ERROR: No backup found for rollback"
        exit 1
    fi
    
    log "Rolling back to: $last_backup"
    
    # Stop application
    systemctl stop "$APP_NAME" || service "$APP_NAME" stop || true
    
    # Restore backup
    rm -rf "$APP_DIR"
    cp -r "$last_backup/$APP_NAME" "$APP_DIR"
    chown -R "$DEPLOY_USER:$DEPLOY_USER" "$APP_DIR"
    
    # Start application
    systemctl start "$APP_NAME" || service "$APP_NAME" start
    
    log "Rollback completed"
}

list_backups() {
    echo "Available backups:"
    ls -lh "$BACKUP_DIR" | grep -E "^d" | awk '{print $9, $6, $7, $8}'
}

# Main
case "${2:-deploy}" in
    deploy)
        backup_current_version
        deploy_new_version
        ;;
    rollback)
        rollback
        ;;
    list-backups)
        list_backups
        ;;
    *)
        echo "Usage: $0 [VERSION] [deploy|rollback|list-backups]"
        exit 1
        ;;
esac
```

---

### Problem 11.2: Infrastructure Provisioning and Configuration

**Scenario:** Automate server provisioning and configuration.

**Solution:**

```bash
#!/bin/bash
# Server provisioning script

set -euo pipefail

HOSTNAME=${1:-$(hostname)}
ROLE=${2:-web}  # web, db, app

# Configuration based on role
configure_role() {
    case $ROLE in
        web)
            install_nginx
            configure_firewall "80 443"
            ;;
        db)
            install_mysql
            configure_firewall "3306"
            ;;
        app)
            install_runtime
            configure_firewall "8080"
            ;;
    esac
}

install_nginx() {
    if command -v apt-get &> /dev/null; then
        apt-get update
        apt-get install -y nginx
    elif command -v yum &> /dev/null; then
        yum install -y nginx
    fi
    
    systemctl enable nginx
    systemctl start nginx
}

install_mysql() {
    if command -v apt-get &> /dev/null; then
        debconf-set-selections <<< "mysql-server mysql-server/root_password password temp"
        debconf-set-selections <<< "mysql-server mysql-server/root_password_again password temp"
        apt-get install -y mysql-server
    elif command -v yum &> /dev/null; then
        yum install -y mysql-server
        systemctl enable mysqld
        systemctl start mysqld
    fi
}

configure_firewall() {
    local ports=$1
    
    if command -v ufw &> /dev/null; then
        ufw --force enable
        for port in $ports; do
            ufw allow "$port/tcp"
        done
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --permanent --add-service=ssh
        for port in $ports; do
            firewall-cmd --permanent --add-port="$port/tcp"
        done
        firewall-cmd --reload
    fi
}

# Set hostname
hostnamectl set-hostname "$HOSTNAME"

# Update system
if command -v apt-get &> /dev/null; then
    apt-get update && apt-get upgrade -y
elif command -v yum &> /dev/null; then
    yum update -y
fi

# Install common tools
if command -v apt-get &> /dev/null; then
    apt-get install -y curl wget git vim htop
elif command -v yum &> /dev/null; then
    yum install -y curl wget git vim htop
fi

# Configure role-specific services
configure_role

echo "Provisioning completed for $HOSTNAME as $ROLE server"
```

---

## 12. Troubleshooting & Debugging

### Problem 12.1: System Diagnostic Script

**Scenario:** Create a comprehensive diagnostic script for troubleshooting.

**Solution:**

```bash
#!/bin/bash
# System diagnostic script

OUTPUT_FILE="/tmp/diagnostics_$(date +%Y%m%d_%H%M%S).txt"

{
    echo "=== System Diagnostics Report ==="
    echo "Generated: $(date)"
    echo "Hostname: $(hostname)"
    echo ""
    
    echo "=== System Information ==="
    uname -a
    cat /etc/os-release
    echo ""
    
    echo "=== CPU Information ==="
    lscpu
    echo ""
    
    echo "=== Memory Information ==="
    free -h
    echo ""
    echo "Memory details:"
    cat /proc/meminfo | head -10
    echo ""
    
    echo "=== Disk Information ==="
    df -h
    echo ""
    echo "Disk I/O:"
    iostat -x 1 2 2>/dev/null || echo "iostat not available"
    echo ""
    
    echo "=== Network Information ==="
    ip addr show
    echo ""
    ip route show
    echo ""
    ss -s
    echo ""
    
    echo "=== Process Information ==="
    echo "Top 10 CPU processes:"
    ps aux --sort=-%cpu | head -11
    echo ""
    echo "Top 10 Memory processes:"
    ps aux --sort=-%mem | head -11
    echo ""
    
    echo "=== Service Status ==="
    systemctl list-units --type=service --state=failed
    echo ""
    
    echo "=== Recent Log Entries ==="
    journalctl -n 50 --no-pager
    echo ""
    
    echo "=== System Load ==="
    uptime
    echo ""
    cat /proc/loadavg
    echo ""
    
    echo "=== Open Files ==="
    lsof 2>/dev/null | wc -l
    echo ""
    
    echo "=== Kernel Messages ==="
    dmesg | tail -20
    echo ""
    
} | tee "$OUTPUT_FILE"

echo "Diagnostics saved to: $OUTPUT_FILE"
```

---

## 13. Security & Hardening

### Problem 13.1: Security Audit and Hardening Script

**Scenario:** Audit system security and apply hardening measures.

**Solution:**

```bash
#!/bin/bash
# Security audit and hardening script

set -euo pipefail

AUDIT_LOG="/var/log/security_audit.log"

log_audit() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$AUDIT_LOG"
}

# 1. Check for unnecessary services
check_services() {
    log_audit "=== Checking Services ==="
    
    systemctl list-unit-files --type=service --state=enabled | \
        grep -E "(telnet|rsh|rlogin|rexec|ftp)" && {
        log_audit "WARNING: Insecure services enabled"
    }
}

# 2. Check SSH configuration
check_ssh() {
    log_audit "=== Checking SSH Configuration ==="
    
    if [ -f /etc/ssh/sshd_config ]; then
        grep -E "^PermitRootLogin" /etc/ssh/sshd_config || \
            log_audit "WARNING: PermitRootLogin not explicitly set"
        
        grep -E "^PasswordAuthentication" /etc/ssh/sshd_config || \
            log_audit "WARNING: PasswordAuthentication not explicitly set"
    fi
}

# 3. Check file permissions
check_permissions() {
    log_audit "=== Checking File Permissions ==="
    
    # World-writable files
    find / -xdev -type f -perm -0002 2>/dev/null | while read -r file; do
        log_audit "WARNING: World-writable file: $file"
    done
    
    # SUID/SGID files
    find / -xdev \( -perm -4000 -o -perm -2000 \) -type f 2>/dev/null | \
        while read -r file; do
            log_audit "INFO: SUID/SGID file: $file"
        done
}

# 4. Check user accounts
check_users() {
    log_audit "=== Checking User Accounts ==="
    
    # Users without password
    local users_no_pass=$(awk -F: '($2 == "" ) { print $1 }' /etc/shadow)
    if [ -n "$users_no_pass" ]; then
        log_audit "WARNING: Users without password found: $users_no_pass"
    fi
    
    # UID 0 accounts (should only be root)
    local uid0_accounts=$(awk -F: '($3 == 0) { print $1 }' /etc/passwd | grep -v "^root$")
    if [ -n "$uid0_accounts" ]; then
        log_audit "WARNING: Multiple UID 0 accounts found: $uid0_accounts"
    fi
}

# 5. Apply security hardening
apply_hardening() {
    log_audit "=== Applying Security Hardening ==="
    
    # Disable root login via SSH
    if [ -f /etc/ssh/sshd_config ]; then
        sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
        systemctl restart sshd
        log_audit "Disabled root SSH login"
    fi
    
    # Set password policies
    if [ -f /etc/login.defs ]; then
        sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs
        sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 7/' /etc/login.defs
        log_audit "Updated password policies"
    fi
    
    # Enable firewall
    if command -v ufw &> /dev/null; then
        ufw --force enable
        log_audit "Firewall enabled"
    fi
}

# Run audit
check_services
check_ssh
check_permissions
check_users

# Apply hardening (uncomment to apply)
# apply_hardening

log_audit "Security audit completed"
```

---

## 14. Container & Orchestration Integration

### Problem 14.1: Docker and Kubernetes Helper Scripts

**Scenario:** Create utility scripts for Docker and Kubernetes operations.

**Solution:**

```bash
#!/bin/bash
# Docker/Kubernetes utility scripts

# Docker cleanup
docker_cleanup() {
    echo "=== Docker Cleanup ==="
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images
    docker image prune -a -f
    
    # Remove unused volumes
    docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    # System prune (everything)
    docker system prune -a -f --volumes
    
    echo "Docker cleanup completed"
}

# Kubernetes pod management
k8s_pod_shell() {
    local pod_name=$1
    local container=${2:-}
    local namespace=${3:-default}
    
    if [ -n "$container" ]; then
        kubectl exec -it "$pod_name" -c "$container" -n "$namespace" -- /bin/bash
    else
        kubectl exec -it "$pod_name" -n "$namespace" -- /bin/bash
    fi
}

# Kubernetes log aggregation
k8s_logs_all() {
    local selector=$1
    local namespace=${2:-default}
    local since=${3:-1h}
    
    kubectl logs -l "$selector" -n "$namespace" --since="$since" --all-containers=true
}

# Kubernetes resource usage
k8s_top() {
    local resource=${1:-pods}
    local namespace=${2:-}
    
    if [ -n "$namespace" ]; then
        kubectl top "$resource" -n "$namespace"
    else
        kubectl top "$resource" --all-namespaces
    fi
}

# Kubernetes port forwarding helper
k8s_port_forward() {
    local resource=$1
    local local_port=$2
    local remote_port=$3
    local namespace=${4:-default}
    
    kubectl port-forward "$resource" "$local_port:$remote_port" -n "$namespace"
}

# Main menu
case "${1:-}" in
    docker-cleanup)
        docker_cleanup
        ;;
    k8s-shell)
        k8s_pod_shell "${2:-}" "${3:-}" "${4:-default}"
        ;;
    k8s-logs)
        k8s_logs_all "${2:-}" "${3:-default}" "${4:-1h}"
        ;;
    k8s-top)
        k8s_top "${2:-pods}" "${3:-}"
        ;;
    k8s-port-forward)
        k8s_port_forward "${2:-}" "${3:-}" "${4:-}" "${5:-default}"
        ;;
    *)
        cat << EOF
Usage: $0 [COMMAND] [ARGS]

Commands:
    docker-cleanup                    Clean up Docker resources
    k8s-shell POD [CONTAINER] [NS]    Open shell in Kubernetes pod
    k8s-logs SELECTOR [NS] [SINCE]    Get logs from pods
    k8s-top [RESOURCE] [NS]           Show resource usage
    k8s-port-forward RES LPORT RPORT [NS]  Port forward to resource
EOF
        ;;
esac
```

---

## Summary

This guide covers:

1. **Linux Fundamentals**: Permissions, filesystem, process management
2. **File Operations**: Backup, cleanup, synchronization
3. **Text Processing**: grep, sed, awk, data processing
4. **System Monitoring**: Resource monitoring, performance tuning
5. **Network Operations**: Troubleshooting, traffic analysis
6. **User Management**: Account automation, permissions
7. **Bash Scripting**: Best practices, error handling, modularity
8. **Advanced Scripting**: Parallel processing, retry logic
9. **System Administration**: Maintenance, automation
10. **DevOps Automation**: Deployment, provisioning
11. **Troubleshooting**: Diagnostic scripts
12. **Security**: Auditing, hardening
13. **Container Integration**: Docker/Kubernetes utilities

Each section includes practical problems with production-ready solutions, suitable for DevOps engineering interviews from medium to advanced levels.

