# Networking in DevOps - Master Guide
## Linux Networking, Theory, and Practical Implementation

---

## Table of Contents

1. [Networking Fundamentals & OSI Model](#1-networking-fundamentals--osi-model)
2. [Linux Network Configuration](#2-linux-network-configuration)
3. [TCP/IP Protocol Suite](#3-tcpip-protocol-suite)
4. [Network Interfaces & Routing](#4-network-interfaces--routing)
5. [DNS & Service Discovery](#5-dns--service-discovery)
6. [Load Balancing & High Availability](#6-load-balancing--high-availability)
7. [Container Networking](#7-container-networking)
8. [Kubernetes Networking](#8-kubernetes-networking)
9. [Network Security & Firewalls](#9-network-security--firewalls)
10. [VPN & Tunneling](#10-vpn--tunneling)
11. [Network Monitoring & Troubleshooting](#11-network-monitoring--troubleshooting)
12. [Performance Tuning](#12-performance-tuning)
13. [Cloud Networking](#13-cloud-networking)
14. [Network Automation](#14-network-automation)
15. [Best Practices & Troubleshooting](#15-best-practices--troubleshooting)

---

## 1. Networking Fundamentals & OSI Model

### 1.1 OSI Model Layers

```
┌─────────────────────────────────────────┐
│ Layer 7: Application  (HTTP, DNS, SSH)  │
├─────────────────────────────────────────┤
│ Layer 6: Presentation (SSL/TLS, Encoding)│
├─────────────────────────────────────────┤
│ Layer 5: Session     (RPC, NetBIOS)     │
├─────────────────────────────────────────┤
│ Layer 4: Transport   (TCP, UDP)         │
├─────────────────────────────────────────┤
│ Layer 3: Network     (IP, ICMP, Routing)│
├─────────────────────────────────────────┤
│ Layer 2: Data Link   (Ethernet, MAC)    │
├─────────────────────────────────────────┤
│ Layer 1: Physical    (Cables, Signals) │
└─────────────────────────────────────────┘
```

### 1.2 TCP/IP Model (Simplified)

```
┌─────────────────────────────┐
│ Application Layer           │  (HTTP, HTTPS, SSH, DNS, FTP)
├─────────────────────────────┤
│ Transport Layer             │  (TCP, UDP)
├─────────────────────────────┤
│ Internet Layer              │  (IP, ICMP, ARP)
├─────────────────────────────┤
│ Network Interface Layer     │  (Ethernet, Wi-Fi)
└─────────────────────────────┘
```

### 1.3 Key Networking Concepts

**Packet vs Frame:**
- **Frame**: Layer 2 (Data Link) - Contains MAC addresses
- **Packet**: Layer 3 (Network) - Contains IP addresses
- **Segment**: Layer 4 (Transport) - TCP/UDP data

**Encapsulation Process:**
```
Application Data
    ↓
TCP Header + Data (Segment)
    ↓
IP Header + Segment (Packet)
    ↓
Ethernet Header + Packet (Frame)
    ↓
Physical Transmission
```

---

## 2. Linux Network Configuration

### 2.1 Network Interface Management

**View Network Interfaces:**

```bash
# Modern method (ip command)
ip addr show
ip a                    # Short form
ip link show            # Link layer info

# Traditional method
ifconfig                # May need: sudo apt install net-tools
ifconfig -a             # All interfaces including down

# Detailed information
ip -s link show         # Statistics
ethtool eth0            # Ethernet interface details
```

**Interface Configuration:**

```bash
# Bring interface up/down
ip link set eth0 up
ip link set eth0 down

# Set MTU (Maximum Transmission Unit)
ip link set eth0 mtu 1500

# View interface statistics
ip -s link show eth0
cat /proc/net/dev       # All interfaces statistics
```

### 2.2 IP Address Configuration

**Static IP Configuration:**

```bash
# Add IP address
ip addr add 192.168.1.100/24 dev eth0
ip addr add 192.168.1.100/24 dev eth0 label eth0:0  # Alias

# Remove IP address
ip addr del 192.168.1.100/24 dev eth0

# Flush all addresses on interface
ip addr flush dev eth0

# Show IP addresses
ip addr show eth0
ip -4 addr show         # IPv4 only
ip -6 addr show         # IPv6 only
```

**DHCP Configuration:**

```bash
# Request DHCP lease
dhclient eth0
dhclient -r eth0        # Release lease
dhclient -v eth0        # Verbose

# Systemd networkd
systemctl status systemd-networkd
```

**Persistent Configuration (NetworkManager):**

```bash
# View connections
nmcli connection show
nmcli device status

# Add connection
nmcli connection add \
    type ethernet \
    con-name eth0-static \
    ifname eth0 \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8 8.8.4.4" \
    ipv4.method manual

# Activate connection
nmcli connection up eth0-static

# Modify connection
nmcli connection modify eth0-static ipv4.addresses "192.168.1.101/24"
```

**Persistent Configuration (netplan - Ubuntu):**

```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

# Apply configuration
sudo netplan apply
sudo netplan try    # Test with rollback
```

**Persistent Configuration (ifcfg - RHEL/CentOS):**

```bash
# /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE=Ethernet
BOOTPROTO=static
NAME=eth0
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4

# Restart network
systemctl restart network
```

### 2.3 Routing Configuration

**View Routing Table:**

```bash
# Modern method
ip route show
ip route                    # Short form
ip -4 route show            # IPv4 only
ip -6 route show            # IPv6 only

# Traditional method
route -n                    # Numeric addresses
netstat -rn                 # Routing table
```

**Add/Remove Routes:**

```bash
# Add default route
ip route add default via 192.168.1.1
ip route add default via 192.168.1.1 dev eth0

# Add specific route
ip route add 192.168.2.0/24 via 192.168.1.1
ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0

# Remove route
ip route del 192.168.2.0/24
ip route del default

# Add route with metric
ip route add default via 192.168.1.1 metric 100

# View route for specific destination
ip route get 8.8.8.8
```

**Persistent Routes:**

```bash
# /etc/sysconfig/network-scripts/route-eth0 (RHEL/CentOS)
192.168.2.0/24 via 192.168.1.1
10.0.0.0/8 via 192.168.1.1

# Or use ip route in startup script
# /etc/rc.local or systemd service
```

### 2.4 Network Namespaces

**Create and Manage Namespaces:**

```bash
# Create namespace
ip netns add netns1
ip netns add netns2

# List namespaces
ip netns list

# Execute command in namespace
ip netns exec netns1 ip addr show
ip netns exec netns1 ping 8.8.8.8

# Create veth pair (virtual ethernet)
ip link add veth0 type veth peer name veth1

# Move interface to namespace
ip link set veth1 netns netns1

# Configure IP in namespace
ip netns exec netns1 ip addr add 10.0.1.1/24 dev veth1
ip netns exec netns1 ip link set veth1 up

# Configure IP on host
ip addr add 10.0.1.2/24 dev veth0
ip link set veth0 up

# Delete namespace
ip netns delete netns1
```

**Use Case: Container Isolation**

```bash
# Docker uses network namespaces for container isolation
# Each container gets its own namespace
docker run -d --name container1 nginx
docker exec container1 ip addr show
```

---

## 3. TCP/IP Protocol Suite

### 3.1 IP Addressing

**IPv4 Address Classes:**

```
Class A: 1.0.0.0 to 126.255.255.255    (8-bit network, 24-bit host)
Class B: 128.0.0.0 to 191.255.255.255  (16-bit network, 16-bit host)
Class C: 192.0.0.0 to 223.255.255.255  (24-bit network, 8-bit host)
Class D: 224.0.0.0 to 239.255.255.255  (Multicast)
Class E: 240.0.0.0 to 255.255.255.255  (Reserved)
```

**CIDR Notation:**

```bash
# Calculate network information
ipcalc 192.168.1.100/24
# Network:   192.168.1.0
# Netmask:   255.255.255.0
# Broadcast: 192.168.1.255
# Hosts:     254

# Common CIDR blocks:
# /24 = 255.255.255.0   (256 addresses, 254 hosts)
# /16 = 255.255.0.0     (65,536 addresses)
# /8  = 255.0.0.0       (16,777,216 addresses)
```

**Private IP Ranges (RFC 1918):**

```bash
10.0.0.0/8          # 10.0.0.0 to 10.255.255.255
172.16.0.0/12       # 172.16.0.0 to 172.31.255.255
192.168.0.0/16      # 192.168.0.0 to 192.168.255.255
```

**IPv6 Basics:**

```bash
# IPv6 address format
2001:0db8:85a3:0000:0000:8a2e:0370:7334
2001:0db8:85a3::8a2e:0370:7334  # Compressed

# Add IPv6 address
ip -6 addr add 2001:db8::1/64 dev eth0

# View IPv6 routes
ip -6 route show
```

### 3.2 TCP (Transmission Control Protocol)

**TCP Characteristics:**

- **Connection-oriented**: 3-way handshake
- **Reliable**: Acknowledgments, retransmission
- **Flow control**: Sliding window
- **Congestion control**: Slow start, congestion avoidance

**TCP 3-Way Handshake:**

```
Client                          Server
  |                               |
  |-------- SYN (seq=x) ---------->|
  |<------ SYN-ACK (seq=y, ack=x+1)|
  |-------- ACK (ack=y+1) ------->|
  |                               |
```

**TCP States:**

```bash
# View TCP connections and states
ss -tuln                    # TCP/UDP listening
ss -tan                     # All TCP connections
ss -tan state established   # Established connections
ss -tan state time-wait     # TIME-WAIT connections

# Common TCP states:
# LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED
# FIN-WAIT-1, FIN-WAIT-2, CLOSE-WAIT, CLOSING
# LAST-ACK, TIME-WAIT, CLOSED
```

**TCP Tuning:**

```bash
# View TCP parameters
sysctl net.ipv4.tcp_*

# TCP window scaling
sysctl net.ipv4.tcp_window_scaling

# TCP congestion control
sysctl net.ipv4.tcp_congestion_control
# Options: cubic, reno, bbr, etc.

# TCP keepalive
sysctl net.ipv4.tcp_keepalive_time      # Default: 7200 seconds
sysctl net.ipv4.tcp_keepalive_probes   # Default: 9
sysctl net.ipv4.tcp_keepalive_intvl    # Default: 75 seconds

# Optimize TCP for high-performance
cat >> /etc/sysctl.conf << EOF
# TCP optimizations
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_max_tw_buckets = 2000000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fastopen = 3
net.core.somaxconn = 1024
EOF

sysctl -p
```

### 3.3 UDP (User Datagram Protocol)

**UDP Characteristics:**

- **Connectionless**: No handshake
- **Unreliable**: No acknowledgments
- **Low overhead**: Minimal header
- **Fast**: No flow/congestion control

**UDP Use Cases:**

- DNS queries
- DHCP
- Streaming media
- Real-time applications
- SNMP

**View UDP Connections:**

```bash
ss -uln                    # UDP listening
ss -uan                    # All UDP connections
```

### 3.4 ICMP (Internet Control Message Protocol)

**ICMP Types:**

```bash
# Ping (ICMP Echo Request/Reply)
ping 8.8.8.8
ping -c 4 8.8.8.8          # 4 packets
ping -i 2 8.8.8.8          # 2 second interval

# Traceroute (ICMP Time Exceeded)
traceroute 8.8.8.8
traceroute -n 8.8.8.8     # No DNS lookup

# mtr (My Traceroute)
mtr 8.8.8.8                # Continuous traceroute
```

**ICMP Configuration:**

```bash
# Disable ICMP echo replies (security)
sysctl net.ipv4.icmp_echo_ignore_all=1

# Allow ICMP redirects
sysctl net.ipv4.conf.all.accept_redirects=1
```

---

## 4. Network Interfaces & Routing

### 4.1 Interface Bonding (Link Aggregation)

**Create Bond Interface:**

```bash
# Load bonding module
modprobe bonding

# Create bond interface
ip link add bond0 type bond mode 802.3ad
ip link set bond0 up

# Add slaves
ip link set eth0 master bond0
ip link set eth1 master bond0

# Configure bond IP
ip addr add 192.168.1.100/24 dev bond0

# View bond status
cat /proc/net/bonding/bond0
```

**Bonding Modes:**

```bash
# Mode 0: balance-rr (Round-robin)
# Mode 1: active-backup (Active-backup)
# Mode 2: balance-xor (XOR policy)
# Mode 3: broadcast (Broadcast)
# Mode 4: 802.3ad (LACP - Link Aggregation Control Protocol)
# Mode 5: balance-tlb (Adaptive transmit load balancing)
# Mode 6: balance-alb (Adaptive load balancing)

# Configure mode
ip link set bond0 type bond mode 802.3ad
```

### 4.2 VLAN (Virtual LAN)

**VLAN Configuration:**

```bash
# Load 8021q module
modprobe 8021q

# Create VLAN interface
ip link add link eth0 name eth0.100 type vlan id 100
ip link set eth0.100 up

# Configure VLAN IP
ip addr add 192.168.100.1/24 dev eth0.100

# View VLAN
ip -d link show eth0.100

# Remove VLAN
ip link del eth0.100
```

**Persistent VLAN (netplan):**

```yaml
# /etc/netplan/01-vlan.yaml
network:
  version: 2
  renderer: networkd
  vlans:
    eth0.100:
      id: 100
      link: eth0
      addresses:
        - 192.168.100.1/24
```

### 4.3 Advanced Routing

**Policy-Based Routing:**

```bash
# Create custom routing table
echo "200 custom" >> /etc/iproute2/rt_tables

# Add route to custom table
ip route add 10.0.0.0/8 via 192.168.1.1 table custom

# Add rule to use custom table
ip rule add from 192.168.1.100 table custom
ip rule add fwmark 1 table custom

# View rules
ip rule show
```

**Source-Based Routing:**

```bash
# Route traffic from specific source
ip rule add from 192.168.1.0/24 table 100
ip route add default via 192.168.1.1 table 100
```

**Multipath Routing:**

```bash
# Multiple gateways with load balancing
ip route add default \
    nexthop via 192.168.1.1 dev eth0 weight 1 \
    nexthop via 192.168.2.1 dev eth1 weight 1
```

---

## 5. DNS & Service Discovery

### 5.1 DNS Configuration

**Local DNS Configuration:**

```bash
# /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver 1.1.1.1
search example.com

# Test DNS resolution
nslookup google.com
dig google.com
dig @8.8.8.8 google.com    # Specific DNS server
dig google.com MX          # MX records
dig google.com A           # A records
dig google.com AAAA        # IPv6 records

# Reverse DNS lookup
dig -x 8.8.8.8
```

**DNS Tools:**

```bash
# host command
host google.com
host 8.8.8.8

# getent (uses /etc/nsswitch.conf)
getent hosts google.com

# Test DNS resolution speed
time dig google.com
```

**Local DNS with systemd-resolved:**

```bash
# View DNS configuration
systemd-resolve --status

# Flush DNS cache
systemd-resolve --flush-caches

# Test resolution
systemd-resolve google.com
```

### 5.2 Local DNS Server (dnsmasq)**

```bash
# Install dnsmasq
sudo apt install dnsmasq

# Configuration: /etc/dnsmasq.conf
listen-address=127.0.0.1,192.168.1.1
server=8.8.8.8
server=8.8.4.4
cache-size=1000

# Local hostname resolution
address=/example.local/192.168.1.100

# Restart service
systemctl restart dnsmasq
systemctl status dnsmasq
```

### 5.3 Service Discovery

**mDNS (Multicast DNS):**

```bash
# Install avahi-daemon
sudo apt install avahi-daemon

# Hostname resolution
hostname.local  # Resolves to local IP
```

**Consul Service Discovery:**

```bash
# Install Consul
wget https://releases.hashicorp.com/consul/1.16.0/consul_1.16.0_linux_amd64.zip
unzip consul_1.16.0_linux_amd64.zip
sudo mv consul /usr/local/bin/

# Start Consul agent
consul agent -dev -client=0.0.0.0

# Register service
consul services register -name=web -address=192.168.1.100 -port=80

# Discover services
consul catalog services
consul catalog nodes
```

**etcd Service Discovery:**

```bash
# Install etcd
sudo apt install etcd

# Start etcd
systemctl start etcd

# Register service
etcdctl put /services/web/192.168.1.100 '{"port":80}'

# Discover services
etcdctl get /services/web/192.168.1.100 --prefix
```

---

## 6. Load Balancing & High Availability

### 6.1 Linux Virtual Server (LVS/IPVS)

**IPVS Configuration:**

```bash
# Load IPVS modules
modprobe ip_vs
modprobe ip_vs_rr          # Round-robin
modprobe ip_vs_wrr         # Weighted round-robin
modprobe ip_vs_sh          # Source hashing

# Install ipvsadm
sudo apt install ipvsadm

# Create virtual server
ipvsadm -A -t 192.168.1.100:80 -s rr

# Add real servers
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.10:80 -g
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.11:80 -g
ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.12:80 -g

# View virtual servers
ipvsadm -ln

# View statistics
ipvsadm -ln --stats
```

**IPVS Scheduling Algorithms:**

```bash
# Round-robin (rr)
ipvsadm -A -t 192.168.1.100:80 -s rr

# Weighted round-robin (wrr)
ipvsadm -A -t 192.168.1.100:80 -s wrr

# Least connections (lc)
ipvsadm -A -t 192.168.1.100:80 -s lc

# Weighted least connections (wlc)
ipvsadm -A -t 192.168.1.100:80 -s wlc

# Source hashing (sh)
ipvsadm -A -t 192.168.1.100:80 -s sh

# Destination hashing (dh)
ipvsadm -A -t 192.168.1.100:80 -s dh
```

### 6.2 HAProxy

**HAProxy Configuration:**

```bash
# Install HAProxy
sudo apt install haproxy

# Configuration: /etc/haproxy/haproxy.cfg
global
    log /dev/log local0
    maxconn 4096
    user haproxy
    group haproxy

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http-in
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
    server web3 192.168.1.12:80 check

# Test configuration
haproxy -f /etc/haproxy/haproxy.cfg -c

# Start HAProxy
systemctl start haproxy
systemctl status haproxy

# View statistics
# Enable stats in config:
listen stats
    bind *:8404
    stats enable
    stats uri /stats
```

### 6.3 Nginx Load Balancing

**Nginx Configuration:**

```nginx
# /etc/nginx/nginx.conf
upstream backend {
    least_conn;                    # Least connections algorithm
    server 192.168.1.10:80 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:80 weight=2 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:80 weight=1 max_fails=3 fail_timeout=30s;
    server 192.168.1.13:80 backup;  # Backup server
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Nginx Load Balancing Methods:**

```nginx
# Round-robin (default)
upstream backend {
    server 192.168.1.10:80;
    server 192.168.1.11:80;
}

# Least connections
upstream backend {
    least_conn;
    server 192.168.1.10:80;
    server 192.168.1.11:80;
}

# IP hash (session persistence)
upstream backend {
    ip_hash;
    server 192.168.1.10:80;
    server 192.168.1.11:80;
}

# Weighted
upstream backend {
    server 192.168.1.10:80 weight=3;
    server 192.168.1.11:80 weight=1;
}
```

### 6.4 Keepalived (VRRP for HA)**

```bash
# Install keepalived
sudo apt install keepalived

# Configuration: /etc/keepalived/keepalived.conf
vrrp_script chk_haproxy {
    script "/usr/bin/killall -0 haproxy"
    interval 2
    weight -2
    fall 3
    rise 2
}

vrrp_instance VI_1 {
    state MASTER                    # or BACKUP
    interface eth0
    virtual_router_id 51
    priority 100                    # Higher priority = master
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass password123
    }
    virtual_ipaddress {
        192.168.1.100/24
    }
    track_script {
        chk_haproxy
    }
}

# Start keepalived
systemctl start keepalived
systemctl status keepalived

# View VRRP status
ip addr show eth0
```

---

## 7. Container Networking

### 7.1 Docker Networking

**Docker Network Types:**

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create network
docker network create mynetwork
docker network create --driver bridge mybridge
docker network create --subnet=172.20.0.0/16 mynetwork

# Connect container to network
docker network connect mynetwork container1

# Disconnect container
docker network disconnect mynetwork container1

# Remove network
docker network rm mynetwork
```

**Docker Network Drivers:**

```bash
# Bridge (default)
docker network create --driver bridge mybridge

# Host (uses host network)
docker network create --driver host myhost

# Overlay (for Swarm)
docker network create --driver overlay myoverlay

# Macvlan (direct access to physical network)
docker network create -d macvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o parent=eth0 \
    mymacvlan

# None (no networking)
docker run --network none nginx
```

**Docker Compose Networking:**

```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend
  app:
    image: node:18
    networks:
      - frontend
      - backend
  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Isolated from external
```

### 7.2 Container Network Namespaces

**View Container Network:**

```bash
# Get container PID
docker inspect --format '{{.State.Pid}}' container1

# Enter container network namespace
nsenter -t <PID> -n ip addr show
nsenter -t <PID> -n ip route show

# View veth pairs
ip link show type veth
```

**Custom Bridge Network:**

```bash
# Create bridge
ip link add br0 type bridge
ip link set br0 up
ip addr add 172.20.0.1/16 dev br0

# Create veth pair
ip link add veth0 type veth peer name veth1

# Connect to bridge
ip link set veth0 master br0
ip link set veth0 up

# Move to container namespace
ip link set veth1 netns <container_pid>
ip netns exec <container_pid> ip addr add 172.20.0.2/16 dev veth1
ip netns exec <container_pid> ip link set veth1 up
ip netns exec <container_pid> ip route add default via 172.20.0.1
```

---

## 8. Kubernetes Networking

### 8.1 Kubernetes Network Model

**Pod Networking:**

```bash
# View pod network
kubectl get pods -o wide
kubectl describe pod <pod-name>

# View pod IP
kubectl get pod <pod-name> -o jsonpath='{.status.podIP}'

# Exec into pod and check network
kubectl exec -it <pod-name> -- ip addr show
kubectl exec -it <pod-name> -- ip route show
```

**Service Networking:**

```yaml
# ClusterIP (default)
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP

# NodePort
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080

# LoadBalancer
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
```

**Ingress:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

### 8.2 CNI (Container Network Interface)

**CNI Plugins:**

- **Flannel**: Overlay network using VXLAN
- **Calico**: BGP-based networking
- **Weave**: Overlay network
- **Cilium**: eBPF-based networking

**Calico Configuration:**

```bash
# Install Calico
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# View Calico nodes
calicoctl get nodes

# View IP pools
calicoctl get ippools

# Network policies
kubectl get networkpolicies
```

**Network Policies:**

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

---

## 9. Network Security & Firewalls

### 9.1 iptables

**Basic iptables Commands:**

```bash
# View rules
iptables -L -n -v
iptables -L INPUT -n -v
iptables -L OUTPUT -n -v
iptables -L FORWARD -n -v

# View with line numbers
iptables -L -n --line-numbers

# View rules in table format
iptables -t nat -L -n -v
iptables -t mangle -L -n -v
iptables -t raw -L -n -v
```

**Basic Firewall Rules:**

```bash
# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow from specific IP
iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT

# Drop invalid packets
iptables -A INPUT -m state --state INVALID -j DROP

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "DROPPED: "
iptables -A INPUT -j DROP
```

**NAT (Network Address Translation):**

```bash
# Enable IP forwarding
sysctl net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# SNAT (Source NAT) - Masquerade
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT (Destination NAT) - Port forwarding
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
iptables -t nat -A POSTROUTING -p tcp -d 192.168.1.10 --dport 8080 -j SNAT --to-source 192.168.1.1
```

**Save and Restore Rules:**

```bash
# Save rules
iptables-save > /etc/iptables/rules.v4

# Restore rules
iptables-restore < /etc/iptables/rules.v4

# Install iptables-persistent
sudo apt install iptables-persistent
# Rules automatically saved on changes
```

### 9.2 firewalld (RHEL/CentOS)

```bash
# Start firewalld
systemctl start firewalld
systemctl enable firewalld

# View status
firewall-cmd --state
firewall-cmd --list-all

# Add service
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# Add port
firewall-cmd --permanent --add-port=8080/tcp
firewall-cmd --reload

# Add rich rule
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8080" protocol="tcp" accept'
firewall-cmd --reload

# Zones
firewall-cmd --get-zones
firewall-cmd --get-active-zones
firewall-cmd --set-default-zone=public
firewall-cmd --zone=public --add-interface=eth0
```

### 9.3 UFW (Uncomplicated Firewall)

```bash
# Enable UFW
sudo ufw enable

# View status
sudo ufw status verbose

# Allow services
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8080/tcp

# Allow from specific IP
sudo ufw allow from 192.168.1.0/24
sudo ufw allow from 192.168.1.100 to any port 22

# Deny
sudo ufw deny 3306/tcp

# Delete rule
sudo ufw delete allow 8080/tcp

# Reset
sudo ufw reset
```

---

## 10. VPN & Tunneling

### 10.1 OpenVPN

**OpenVPN Server Setup:**

```bash
# Install OpenVPN
sudo apt install openvpn easy-rsa

# Setup CA
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
./easyrsa init-pki
./easyrsa build-ca
./easyrsa gen-req server nopass
./easyrsa sign-req server server
./easyrsa gen-dh

# Generate client certificate
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1

# Server configuration: /etc/openvpn/server.conf
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3

# Start OpenVPN
systemctl start openvpn@server
systemctl enable openvpn@server
```

### 10.2 WireGuard

**WireGuard Setup:**

```bash
# Install WireGuard
sudo apt install wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Server configuration: /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

# Start WireGuard
wg-quick up wg0
systemctl enable wg-quick@wg0
```

### 10.3 SSH Tunneling

**Local Port Forwarding:**

```bash
# Forward local port to remote
ssh -L 8080:localhost:80 user@remote-server

# Access localhost:8080 -> remote:80
```

**Remote Port Forwarding:**

```bash
# Forward remote port to local
ssh -R 8080:localhost:80 user@remote-server

# Access remote:8080 -> local:80
```

**Dynamic Port Forwarding (SOCKS Proxy):**

```bash
# Create SOCKS proxy
ssh -D 1080 user@remote-server

# Use with applications
export http_proxy=socks5://localhost:1080
```

**SSH Tunnel with Key:**

```bash
# Create tunnel
ssh -i ~/.ssh/id_rsa -L 3306:db-server:3306 user@jump-host

# Persistent tunnel (autossh)
autossh -M 20000 -L 3306:db-server:3306 user@jump-host
```

---

## 11. Network Monitoring & Troubleshooting

### 11.1 Network Monitoring Tools

**tcpdump:**

```bash
# Capture all traffic
sudo tcpdump -i eth0

# Capture specific host
sudo tcpdump -i eth0 host 192.168.1.100

# Capture specific port
sudo tcpdump -i eth0 port 80

# Capture HTTP traffic
sudo tcpdump -i eth0 -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# Save to file
sudo tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap
```

**Wireshark/tshark:**

```bash
# Install
sudo apt install wireshark tshark

# Capture
sudo tshark -i eth0

# Filter
tshark -i eth0 -f "host 192.168.1.100"
tshark -i eth0 -f "tcp port 80"

# Read pcap
tshark -r capture.pcap
```

**iftop:**

```bash
# Install
sudo apt install iftop

# Monitor interface
sudo iftop -i eth0

# Show ports
sudo iftop -i eth0 -P
```

**nethogs:**

```bash
# Install
sudo apt install nethogs

# Monitor per-process network
sudo nethogs eth0
```

**vnstat:**

```bash
# Install
sudo apt install vnstat

# View statistics
vnstat
vnstat -d    # Daily
vnstat -m    # Monthly
vnstat -h    # Hourly
```

### 11.2 Network Troubleshooting

**Connectivity Tests:**

```bash
# Ping test
ping -c 4 8.8.8.8
ping6 -c 4 2001:4860:4860::8888

# Traceroute
traceroute 8.8.8.8
traceroute -n 8.8.8.8    # No DNS

# mtr (continuous)
mtr 8.8.8.8

# Test specific port
nc -zv 192.168.1.100 80
telnet 192.168.1.100 80
```

**DNS Troubleshooting:**

```bash
# Test DNS
nslookup google.com
dig google.com
dig @8.8.8.8 google.com

# Check DNS servers
cat /etc/resolv.conf
systemd-resolve --status

# Flush DNS cache
sudo systemd-resolve --flush-caches
```

**Routing Troubleshooting:**

```bash
# View routing table
ip route show
route -n

# Trace route
ip route get 8.8.8.8

# View ARP table
arp -a
ip neigh show

# Clear ARP cache
ip neigh flush dev eth0
```

**Connection Analysis:**

```bash
# View active connections
ss -tuln
netstat -tuln

# View connections by process
ss -tulnp
netstat -tulnp

# View established connections
ss -tan state established
netstat -tan | grep ESTABLISHED

# Count connections
ss -tan | grep ESTABLISHED | wc -l
```

**Bandwidth Testing:**

```bash
# iperf3 server
iperf3 -s

# iperf3 client
iperf3 -c server-ip
iperf3 -c server-ip -t 60    # 60 seconds
iperf3 -c server-ip -P 4     # 4 parallel streams
```

---

## 12. Performance Tuning

### 12.1 TCP Tuning

**TCP Buffer Sizes:**

```bash
# View current values
sysctl net.core.rmem_max
sysctl net.core.wmem_max
sysctl net.ipv4.tcp_rmem
sysctl net.ipv4.tcp_wmem

# Optimize for high throughput
cat >> /etc/sysctl.conf << EOF
# TCP buffer sizes
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_congestion_control = bbr
EOF

sysctl -p
```

**TCP Connection Settings:**

```bash
# Increase connection limits
sysctl net.core.somaxconn=1024
sysctl net.ipv4.tcp_max_syn_backlog=8192

# TCP fast open
sysctl net.ipv4.tcp_fastopen=3

# TCP keepalive
sysctl net.ipv4.tcp_keepalive_time=300
sysctl net.ipv4.tcp_keepalive_probes=5
sysctl net.ipv4.tcp_keepalive_intvl=15
```

### 12.2 Network Interface Tuning

**Ring Buffer Sizes:**

```bash
# View ring buffer
ethtool -g eth0

# Set ring buffer
ethtool -G eth0 rx 4096 tx 4096

# Persistent: /etc/network/interfaces
# post-up ethtool -G eth0 rx 4096 tx 4096
```

**Offloading:**

```bash
# View offload settings
ethtool -k eth0

# Enable offloading
ethtool -K eth0 tso on
ethtool -K eth0 gso on
ethtool -K eth0 lro on

# Disable if causing issues
ethtool -K eth0 tso off
```

**Interrupt Coalescing:**

```bash
# View settings
ethtool -c eth0

# Set coalescing
ethtool -C eth0 rx-usecs 100
ethtool -C eth0 tx-usecs 100
```

### 12.3 Network Queue Management

**Receive Side Scaling (RSS):**

```bash
# View RSS settings
ethtool -x eth0

# Enable RSS
ethtool -X eth0 equal 4    # 4 queues
```

**CPU Affinity:**

```bash
# Set IRQ affinity
echo 2 > /proc/irq/24/smp_affinity    # CPU 1
echo 4 > /proc/irq/25/smp_affinity    # CPU 2
```

---

## 13. Cloud Networking

### 13.1 AWS Networking

**VPC Configuration:**

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets
aws ec2 create-subnet \
    --vpc-id vpc-xxx \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway \
    --vpc-id vpc-xxx \
    --internet-gateway-id igw-xxx

# Create route table
aws ec2 create-route-table --vpc-id vpc-xxx
aws ec2 create-route \
    --route-table-id rtb-xxx \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id igw-xxx
```

**Security Groups:**

```bash
# Create security group
aws ec2 create-security-group \
    --group-name web-sg \
    --description "Web server security group" \
    --vpc-id vpc-xxx

# Add rule
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxx \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0
```

### 13.2 Azure Networking

**Virtual Network:**

```bash
# Create VNet
az network vnet create \
    --resource-group myResourceGroup \
    --name myVNet \
    --address-prefix 10.0.0.0/16 \
    --subnet-name mySubnet \
    --subnet-prefix 10.0.1.0/24

# Create network security group
az network nsg create \
    --resource-group myResourceGroup \
    --name myNSG

# Add rule
az network nsg rule create \
    --resource-group myResourceGroup \
    --nsg-name myNSG \
    --name AllowHTTP \
    --priority 100 \
    --protocol Tcp \
    --destination-port-ranges 80 \
    --access Allow
```

### 13.3 GCP Networking

**VPC Network:**

```bash
# Create VPC
gcloud compute networks create my-vpc \
    --subnet-mode custom

# Create subnet
gcloud compute networks subnets create my-subnet \
    --network my-vpc \
    --range 10.0.1.0/24 \
    --region us-central1

# Create firewall rule
gcloud compute firewall-rules create allow-http \
    --network my-vpc \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0
```

---

## 14. Network Automation

### 14.1 Ansible Network Modules

```yaml
# Ansible playbook for network configuration
- name: Configure network interfaces
  hosts: network_devices
  tasks:
    - name: Configure interface
      ios_config:
        lines:
          - ip address 192.168.1.1 255.255.255.0
        parents: interface GigabitEthernet0/1

    - name: Configure OSPF
      ios_config:
        lines:
          - network 192.168.1.0 0.0.0.255 area 0
        parents: router ospf 1
```

### 14.2 Network Scripts

**Network Configuration Script:**

```bash
#!/bin/bash
# Network configuration script

INTERFACE="eth0"
IP_ADDRESS="192.168.1.100"
NETMASK="255.255.255.0"
GATEWAY="192.168.1.1"
DNS1="8.8.8.8"
DNS2="8.8.4.4"

# Configure interface
ip addr add ${IP_ADDRESS}/${NETMASK} dev ${INTERFACE}
ip link set ${INTERFACE} up

# Configure gateway
ip route add default via ${GATEWAY}

# Configure DNS
echo "nameserver ${DNS1}" > /etc/resolv.conf
echo "nameserver ${DNS2}" >> /etc/resolv.conf
```

**Network Monitoring Script:**

```bash
#!/bin/bash
# Network monitoring script

INTERFACE="eth0"
THRESHOLD=1000  # Mbps

# Get interface statistics
RX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/rx_bytes)
TX_BYTES=$(cat /sys/class/net/${INTERFACE}/statistics/tx_bytes)

sleep 1

RX_BYTES_NEW=$(cat /sys/class/net/${INTERFACE}/statistics/rx_bytes)
TX_BYTES_NEW=$(cat /sys/class/net/${INTERFACE}/statistics/tx_bytes)

RX_RATE=$(( (RX_BYTES_NEW - RX_BYTES) * 8 / 1024 / 1024 ))
TX_RATE=$(( (TX_BYTES_NEW - TX_BYTES) * 8 / 1024 / 1024 ))

echo "RX: ${RX_RATE} Mbps, TX: ${TX_RATE} Mbps"

if [ ${RX_RATE} -gt ${THRESHOLD} ] || [ ${TX_RATE} -gt ${THRESHOLD} ]; then
    echo "ALERT: High network usage detected!"
fi
```

---

## 15. Best Practices & Troubleshooting

### 15.1 Network Best Practices

1. **Use Static IPs for Servers**
   - Avoid DHCP for production servers
   - Document IP assignments

2. **Implement Network Segmentation**
   - Separate networks for different tiers
   - Use VLANs or separate subnets

3. **Enable Network Monitoring**
   - Monitor bandwidth usage
   - Set up alerts for anomalies

4. **Use Firewalls**
   - Default deny policy
   - Allow only necessary ports

5. **Implement Redundancy**
   - Multiple network paths
   - Load balancing
   - Failover mechanisms

6. **Document Network Topology**
   - Network diagrams
   - IP address assignments
   - Routing tables

### 15.2 Common Issues & Solutions

**Issue: Cannot Connect to Server**

```bash
# Troubleshooting steps:
# 1. Check interface status
ip link show eth0

# 2. Check IP configuration
ip addr show eth0

# 3. Check routing
ip route show

# 4. Test connectivity
ping 8.8.8.8

# 5. Check firewall
iptables -L -n -v

# 6. Check DNS
nslookup google.com
```

**Issue: Slow Network Performance**

```bash
# Check bandwidth
iperf3 -c server-ip

# Check packet loss
ping -c 100 8.8.8.8

# Check latency
mtr 8.8.8.8

# Check interface errors
ethtool -S eth0 | grep error

# Check TCP retransmissions
ss -i
```

**Issue: DNS Resolution Fails**

```bash
# Check DNS configuration
cat /etc/resolv.conf

# Test DNS servers
dig @8.8.8.8 google.com

# Check DNS cache
systemd-resolve --status

# Flush DNS cache
systemd-resolve --flush-caches
```

### 15.3 Network Troubleshooting Checklist

- [ ] Interface is up and configured
- [ ] IP address is correct
- [ ] Default gateway is reachable
- [ ] DNS servers are accessible
- [ ] Firewall rules allow traffic
- [ ] Routing table is correct
- [ ] No packet loss or errors
- [ ] MTU size is appropriate
- [ ] Network interface statistics are normal
- [ ] No network loops or broadcast storms

---

## Conclusion

### Key Takeaways:

1. **Understand the OSI Model** - Helps troubleshoot at the right layer
2. **Master Linux Networking Tools** - ip, ss, iptables, etc.
3. **Know Your Protocols** - TCP, UDP, ICMP characteristics
4. **Implement Security** - Firewalls, VPNs, network policies
5. **Monitor Everything** - Use tools to track network health
6. **Automate Configuration** - Use scripts and IaC tools
7. **Document Everything** - Network diagrams and configurations

### Essential Commands Reference:

```bash
# Interface management
ip addr show
ip link set eth0 up
ip addr add 192.168.1.100/24 dev eth0

# Routing
ip route show
ip route add default via 192.168.1.1

# DNS
dig google.com
nslookup google.com

# Connectivity
ping 8.8.8.8
traceroute 8.8.8.8
nc -zv host port

# Monitoring
ss -tuln
tcpdump -i eth0
iftop -i eth0

# Firewall
iptables -L -n -v
ufw status
firewall-cmd --list-all
```

---

*Networking in DevOps - Master Guide*
*Linux Networking, Theory, and Practical Implementation*
*Last Updated: 2024*

