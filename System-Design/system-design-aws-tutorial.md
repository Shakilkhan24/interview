# System Design with AWS - Comprehensive Tutorial
## Large-Scale System Architecture Patterns and AWS Service Integration

---

## Table of Contents

1. [Introduction to System Design](#1-introduction-to-system-design)
2. [Core System Design Principles](#2-core-system-design-principles)
3. [AWS Service Mapping](#3-aws-service-mapping)
4. [Design Pattern 1: URL Shortener (TinyURL)](#4-design-pattern-1-url-shortener-tinyurl)
5. [Design Pattern 2: Distributed Cache System](#5-design-pattern-2-distributed-cache-system)
6. [Design Pattern 3: Chat/Messaging System](#6-design-pattern-3-chatmessaging-system)
7. [Design Pattern 4: Video Streaming Platform](#7-design-pattern-4-video-streaming-platform)
8. [Design Pattern 5: Social Media Feed](#8-design-pattern-5-social-media-feed)
9. [Design Pattern 6: E-Commerce Platform](#9-design-pattern-6-e-commerce-platform)
10. [Design Pattern 7: Search Engine](#10-design-pattern-7-search-engine)
11. [Design Pattern 8: Notification System](#11-design-pattern-8-notification-system)
12. [Design Pattern 9: Rate Limiting System](#12-design-pattern-9-rate-limiting-system)
13. [Design Pattern 10: Distributed File Storage](#13-design-pattern-10-distributed-file-storage)
14. [Scalability Patterns](#14-scalability-patterns)
15. [Reliability and High Availability](#15-reliability-and-high-availability)
16. [Performance Optimization](#16-performance-optimization)
17. [Security Patterns](#17-security-patterns)
18. [Cost Optimization](#18-cost-optimization)
19. [Monitoring and Observability](#19-monitoring-and-observability)
20. [Best Practices and Trade-offs](#20-best-practices-and-trade-offs)

---

## 1. Introduction to System Design

### What is System Design?

System design is the process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements. It involves making architectural decisions that affect scalability, reliability, performance, and maintainability.

### Key Goals

1. **Scalability**: Handle growing amounts of work
2. **Reliability**: System works correctly even when components fail
3. **Availability**: System is operational when needed
4. **Performance**: Low latency and high throughput
5. **Maintainability**: Easy to update and extend
6. **Cost-Effective**: Optimize resource usage

### System Design Process

1. **Requirements Gathering**
   - Functional requirements
   - Non-functional requirements (scale, performance, etc.)
   - Constraints and assumptions

2. **Capacity Estimation**
   - Traffic estimates
   - Storage requirements
   - Bandwidth calculations

3. **System API Design**
   - Define interfaces
   - Request/response formats
   - Error handling

4. **Database Design**
   - Data models
   - Schema design
   - Indexing strategy

5. **High-Level Design**
   - Component identification
   - Interaction patterns
   - Technology choices

6. **Detailed Design**
   - Component deep-dive
   - Algorithms and data structures
   - Trade-offs analysis

---

## 2. Core System Design Principles

### Scalability

**Vertical Scaling (Scale Up)**
- Increase resources of existing servers
- AWS: Larger EC2 instance types
- Pros: Simple, no code changes
- Cons: Limited by hardware, single point of failure

**Horizontal Scaling (Scale Out)**
- Add more servers
- AWS: Auto Scaling Groups, ECS/EKS
- Pros: Unlimited scale, fault tolerance
- Cons: Requires stateless design, load balancing

### Load Balancing

**Application Load Balancer (ALB)**
- Layer 7 (HTTP/HTTPS)
- Path-based and host-based routing
- SSL termination
- Health checks

**Network Load Balancer (NLB)**
- Layer 4 (TCP/UDP)
- Ultra-low latency
- Static IP addresses
- High throughput

**Classic Load Balancer (CLB)**
- Legacy option
- Layer 4 and Layer 7
- Being phased out

### Caching Strategies

**Cache-Aside (Lazy Loading)**
```
Application Flow:
1. Check cache
2. If miss, read from database
3. Write to cache
4. Return data
```

**Write-Through**
```
Application Flow:
1. Write to cache
2. Write to database
3. Return success
```

**Write-Behind (Write-Back)**
```
Application Flow:
1. Write to cache
2. Return success immediately
3. Asynchronously write to database
```

**AWS Services:**
- **ElastiCache (Redis/Memcached)**: In-memory caching
- **CloudFront**: CDN and edge caching
- **DynamoDB Accelerator (DAX)**: DynamoDB caching layer

### Database Patterns

**SQL Databases (RDS)**
- ACID compliance
- Complex queries
- Relational data
- AWS: RDS (MySQL, PostgreSQL, etc.)

**NoSQL Databases**
- **DynamoDB**: Key-value, document store
- **DocumentDB**: MongoDB-compatible
- **Neptune**: Graph database
- **ElastiCache**: In-memory

**Database Replication**
- **Read Replicas**: Scale read operations
- **Multi-AZ**: High availability
- **Global Tables**: Cross-region replication

---

## 3. AWS Service Mapping

### Compute Services

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Web Servers | EC2, ECS, EKS, Lambda | Application hosting |
| API Gateway | API Gateway | REST/WebSocket APIs |
| Serverless Functions | Lambda | Event-driven processing |
| Containers | ECS, EKS, Fargate | Containerized applications |
| Batch Processing | Batch, ECS | Long-running jobs |

### Storage Services

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Object Storage | S3 | Files, media, backups |
| Block Storage | EBS | Database storage |
| File Storage | EFS | Shared file systems |
| Archive Storage | Glacier | Long-term archival |
| CDN | CloudFront | Content delivery |

### Database Services

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Relational DB | RDS | Structured data |
| NoSQL | DynamoDB | Key-value, document |
| In-Memory Cache | ElastiCache | Caching layer |
| Graph DB | Neptune | Graph relationships |
| Time-Series | Timestream | IoT, metrics |
| Document DB | DocumentDB | MongoDB workloads |

### Messaging & Queue Services

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Message Queue | SQS | Async processing |
| Pub/Sub | SNS | Event notifications |
| Streaming | Kinesis | Real-time data streams |
| Event Bus | EventBridge | Event-driven architecture |

### Networking Services

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Load Balancer | ALB, NLB, CLB | Traffic distribution |
| DNS | Route 53 | Domain management |
| VPC | VPC | Network isolation |
| CDN | CloudFront | Global content delivery |
| API Gateway | API Gateway | API management |

### Monitoring & Observability

| Component | AWS Service | Use Case |
|-----------|-------------|----------|
| Metrics | CloudWatch | System metrics |
| Logs | CloudWatch Logs | Application logs |
| Tracing | X-Ray | Distributed tracing |
| Alarms | CloudWatch Alarms | Alerting |
| Dashboards | CloudWatch Dashboards | Visualization |

---

## 4. Design Pattern 1: URL Shortener (TinyURL)

### Requirements

**Functional:**
- Shorten long URLs
- Redirect short URLs to original
- Custom short URLs (optional)
- URL expiration (optional)

**Non-Functional:**
- High availability
- Low latency (< 100ms)
- Handle 100M URLs/day
- 99.9% uptime

### Capacity Estimation

**Traffic:**
- 100M URLs/day = 1,160 URLs/second
- Read:Write ratio = 100:1
- Reads: 115,000/second
- Writes: 1,160/second

**Storage:**
- Average URL length: 100 characters
- 5 years storage: 100M * 365 * 5 = 182.5B URLs
- Storage: 182.5B * 100 bytes = 18.25 TB

**Bandwidth:**
- Write: 1,160 * 100 bytes = 116 KB/s
- Read: 115,000 * 100 bytes = 11.5 MB/s

### High-Level Design

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │  (AWS API Gateway)
│  - POST /shorten│
│  - GET /{hash}  │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│  Load    │      │  Application │   │   Cache     │
│ Balancer │─────▶│   Servers    │───▶│ (ElastiCache│
│  (ALB)   │      │  (ECS/EKS)   │   │   Redis)    │
└──────────┘      └──────┬───────┘   └─────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Database   │
                  │  (DynamoDB)  │
                  └──────────────┘
```

### AWS Architecture

**Components:**

1. **API Gateway**
   - REST API endpoints
   - Rate limiting
   - Authentication
   - Request validation

2. **Application Load Balancer (ALB)**
   - Distribute traffic
   - Health checks
   - SSL termination

3. **ECS/EKS (Application Servers)**
   - Stateless application logic
   - Auto-scaling
   - Multiple availability zones

4. **ElastiCache (Redis)**
   - Cache popular URLs
   - Reduce database load
   - Sub-millisecond latency

5. **DynamoDB**
   - Store URL mappings
   - Partition key: short URL hash
   - Global Secondary Index: original URL
   - TTL for expiration

6. **CloudFront**
   - CDN for redirects
   - Edge locations
   - Reduce latency globally

### Database Schema

**DynamoDB Table: `urls`**

```
Partition Key: hash (String)
Attributes:
  - original_url (String)
  - created_at (Number)
  - expires_at (Number, optional)
  - user_id (String, optional)
  - click_count (Number)
  - ttl (Number) - for auto-deletion
```

**Global Secondary Index: `original-url-index`**
- Partition Key: original_url
- For reverse lookup

### API Design

**Shorten URL:**
```
POST /api/v1/shorten
Request:
{
  "url": "https://example.com/very/long/url",
  "custom_hash": "optional",
  "expires_in": 3600
}

Response:
{
  "short_url": "https://short.ly/abc123",
  "expires_at": "2024-01-01T00:00:00Z"
}
```

**Redirect:**
```
GET /{hash}
Response: 301 Redirect to original URL
```

### Key Generation

**Option 1: Base62 Encoding**
- Use counter or random number
- Encode to base62 (a-z, A-Z, 0-9)
- 6 characters = 56.8 billion combinations

**Option 2: Hash-based**
- MD5/SHA256 of original URL
- Take first 6-8 characters
- Handle collisions

**AWS Implementation:**
```python
import hashlib
import base64

def generate_short_url(original_url, counter=None):
    if counter:
        # Use counter for uniqueness
        hash_value = base64.b64encode(str(counter).encode()).decode()[:6]
    else:
        # Hash-based
        hash_value = hashlib.md5(original_url.encode()).hexdigest()[:6]
    
    return hash_value
```

### Detailed Design

**Write Flow:**
```
1. Client → API Gateway → ALB → Application Server
2. Generate hash (check for collision)
3. Store in DynamoDB
4. Cache in ElastiCache
5. Return short URL
```

**Read Flow:**
```
1. Client → CloudFront → ALB → Application Server
2. Check ElastiCache (cache hit: return immediately)
3. If miss, query DynamoDB
4. Update cache
5. Return 301 redirect
```

### Scaling Considerations

**Database Sharding:**
- Partition by hash prefix
- Use consistent hashing
- DynamoDB handles sharding automatically

**Caching Strategy:**
- Cache popular URLs (80/20 rule)
- LRU eviction policy
- TTL based on popularity

**CDN Strategy:**
- Cache redirects at edge
- Reduce origin load
- Global distribution

### Trade-offs

| Aspect | Option 1 | Option 2 | Choice |
|--------|----------|----------|--------|
| Hash Generation | Counter-based | Hash-based | Hash-based (no DB dependency) |
| Database | SQL (RDS) | NoSQL (DynamoDB) | DynamoDB (better scale) |
| Cache | Redis | Memcached | Redis (persistence) |
| CDN | CloudFront | None | CloudFront (global) |

### Cost Estimation (Monthly)

- API Gateway: $3.50 per million requests = $10,440
- ALB: $0.0225 per ALB-hour = $16.20
- ECS: 10 t3.medium instances = $1,000
- ElastiCache: 3 cache.r6g.large = $450
- DynamoDB: On-demand = $500
- CloudFront: $0.085 per GB = $1,000
- **Total: ~$13,400/month**

### Monitoring

- **CloudWatch Metrics:**
  - Request count
  - Latency (p50, p95, p99)
  - Error rate
  - Cache hit ratio

- **X-Ray Tracing:**
  - End-to-end request tracing
  - Identify bottlenecks

- **Alarms:**
  - High error rate
  - High latency
  - Cache miss rate

---

## 5. Design Pattern 2: Distributed Cache System

### Requirements

**Functional:**
- Store key-value pairs
- TTL support
- Cache invalidation
- Distributed across nodes

**Non-Functional:**
- Sub-millisecond latency
- 99.99% availability
- Handle 1M requests/second
- Data consistency

### Architecture

```
┌─────────────┐
│ Application │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Cache Client   │
│  (SDK/Library)  │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│ ElastiCache│    │ ElastiCache│    │ ElastiCache│
│  Node 1   │    │  Node 2   │    │  Node 3   │
│ (Primary) │    │ (Replica) │    │ (Replica) │
└──────────┘      └──────────┘      └──────────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Database   │
                  │   (RDS)      │
                  └──────────────┘
```

### AWS Implementation

**ElastiCache for Redis:**

**Configuration:**
- **Mode**: Cluster mode enabled
- **Node Type**: cache.r6g.xlarge
- **Replication**: Multi-AZ
- **Backup**: Daily snapshots
- **Encryption**: In-transit and at-rest

**Architecture Patterns:**

1. **Cache-Aside Pattern:**
```python
def get_data(key):
    # Check cache
    value = redis_client.get(key)
    if value:
        return value
    
    # Cache miss - get from database
    value = database.get(key)
    
    # Store in cache
    redis_client.setex(key, 3600, value)  # TTL: 1 hour
    
    return value
```

2. **Write-Through Pattern:**
```python
def set_data(key, value):
    # Write to database
    database.set(key, value)
    
    # Write to cache
    redis_client.setex(key, 3600, value)
```

3. **Write-Behind Pattern:**
```python
def set_data_async(key, value):
    # Write to cache immediately
    redis_client.setex(key, 3600, value)
    
    # Queue for database write
    sqs.send_message(
        QueueUrl=write_queue_url,
        MessageBody=json.dumps({'key': key, 'value': value})
    )
```

### Cache Invalidation Strategies

**Time-Based (TTL):**
```python
redis_client.setex(key, ttl_seconds, value)
```

**Event-Based:**
```python
# Publish invalidation event
redis_client.publish('cache:invalidate', key)

# Subscribers remove from cache
def invalidate_handler(message):
    redis_client.delete(message['data'])
```

**Tag-Based:**
```python
# Store tags with keys
redis_client.sadd(f'tag:{tag}', key)
redis_client.set(key, value)

# Invalidate by tag
def invalidate_tag(tag):
    keys = redis_client.smembers(f'tag:{tag}')
    redis_client.delete(*keys)
```

### Consistency Models

**Strong Consistency:**
- Use Redis with replication
- Read from primary
- Synchronous replication

**Eventual Consistency:**
- Read from replicas
- Asynchronous replication
- Lower latency

### Scaling Strategy

**Horizontal Scaling:**
- Add more cache nodes
- Use Redis Cluster
- Automatic sharding

**Vertical Scaling:**
- Larger instance types
- More memory
- Better performance

**Multi-Region:**
- Global Datastore (Redis)
- Cross-region replication
- Active-active setup

### Monitoring

**CloudWatch Metrics:**
- CacheHits
- CacheMisses
- Evictions
- ReplicationLag
- CPUUtilization
- NetworkBytesIn/Out

**Alarms:**
- High cache miss rate
- High CPU usage
- Replication lag
- Memory usage

---

## 6. Design Pattern 3: Chat/Messaging System

### Requirements

**Functional:**
- Send/receive messages
- 1-on-1 and group chats
- Message history
- Online/offline status
- Typing indicators
- File attachments

**Non-Functional:**
- Real-time delivery (< 100ms)
- 99.9% availability
- Handle 10M users
- 1B messages/day
- Message persistence

### Capacity Estimation

**Users:**
- 10M total users
- 1M concurrent users
- 100K messages/second peak

**Storage:**
- Average message: 100 bytes
- 1B messages/day * 365 days = 365B messages
- Storage: 365B * 100 bytes = 36.5 TB/year

**Bandwidth:**
- 100K messages/sec * 100 bytes = 10 MB/s
- With overhead: ~50 MB/s

### High-Level Architecture

```
┌─────────────┐
│   Mobile    │
│   / Web     │
│   Client    │
└──────┬──────┘
       │ WebSocket/HTTP
       ▼
┌─────────────────┐
│  API Gateway    │
│  (WebSocket API)│
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│  Load    │      │  Chat        │   │  Presence  │
│ Balancer │─────▶│  Servers     │───▶│  Service   │
│  (ALB)   │      │  (ECS/EKS)   │   │ (ElastiCache│
└──────────┘      └──────┬───────┘   └─────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│ Message  │      │   Message    │   │   File      │
│ Queue    │      │   Store      │   │   Storage   │
│ (SQS)    │      │ (DynamoDB)   │   │   (S3)      │
└──────────┘      └──────────────┘   └─────────────┘
```

### AWS Architecture

**Components:**

1. **API Gateway (WebSocket)**
   - Real-time bidirectional communication
   - Connection management
   - Route messages to backend

2. **Application Servers (ECS/EKS)**
   - WebSocket connection handling
   - Message routing logic
   - Presence management

3. **ElastiCache (Redis)**
   - Active connections mapping
   - Presence information
   - Typing indicators
   - Recent message cache

4. **DynamoDB**
   - Message storage
   - User conversations
   - Message indexes

5. **S3**
   - File attachments
   - Media files
   - CDN via CloudFront

6. **SQS**
   - Async message processing
   - Notification delivery
   - Background jobs

7. **SNS**
   - Push notifications
   - Email notifications
   - SMS alerts

### Database Schema

**DynamoDB Tables:**

**1. Messages Table:**
```
Partition Key: conversation_id (String)
Sort Key: message_id (String)
Attributes:
  - sender_id (String)
  - content (String)
  - timestamp (Number)
  - message_type (String)
  - attachments (List)
  - ttl (Number)
```

**2. Conversations Table:**
```
Partition Key: user_id (String)
Sort Key: conversation_id (String)
Attributes:
  - participants (List)
  - last_message_id (String)
  - last_message_time (Number)
  - unread_count (Number)
```

**3. Users Table:**
```
Partition Key: user_id (String)
Attributes:
  - username (String)
  - status (String) - online/offline
  - last_seen (Number)
  - avatar_url (String)
```

### Message Flow

**Send Message:**
```
1. Client → API Gateway (WebSocket)
2. API Gateway → Application Server
3. Store in DynamoDB
4. Check recipient online status (Redis)
5. If online: Push via WebSocket
6. If offline: Queue in SQS for push notification
7. Update conversation metadata
8. Cache recent message (Redis)
```

**Receive Message:**
```
1. Application Server receives message
2. Lookup recipient connection (Redis)
3. Push to recipient via WebSocket
4. Update unread count
5. Send push notification (if needed)
```

### Presence Management

**Redis Structure:**
```
Key: user:{user_id}:presence
Value: {
  "status": "online",
  "last_seen": timestamp,
  "connection_id": "ws-connection-id"
}

Key: connection:{connection_id}
Value: user_id

Set: online_users
Members: user_id (for quick online count)
```

**Heartbeat:**
```python
def update_presence(user_id, connection_id):
    redis_client.setex(
        f'user:{user_id}:presence',
        60,  # 60 second TTL
        json.dumps({
            'status': 'online',
            'last_seen': time.time(),
            'connection_id': connection_id
        })
    )
    redis_client.sadd('online_users', user_id)
    redis_client.setex(f'connection:{connection_id}', 60, user_id)
```

### Scaling Considerations

**Connection Management:**
- Use API Gateway for connection handling
- Scale application servers horizontally
- Store connections in Redis cluster

**Message Routing:**
- Consistent hashing for user-to-server mapping
- Redis pub/sub for cross-server communication
- SQS for reliable message delivery

**Database Sharding:**
- Partition by conversation_id
- Use GSI for user-based queries
- Archive old messages to S3

### Real-time Features

**Typing Indicators:**
```python
def send_typing_indicator(conversation_id, user_id):
    redis_client.publish(
        f'typing:{conversation_id}',
        json.dumps({
            'user_id': user_id,
            'timestamp': time.time()
        })
    )
```

**Read Receipts:**
```python
def mark_as_read(conversation_id, user_id, message_id):
    dynamodb.update_item(
        TableName='messages',
        Key={'conversation_id': conversation_id, 'message_id': message_id},
        UpdateExpression='ADD read_by :user_id',
        ExpressionAttributeValues={':user_id': {user_id}}
    )
```

### Trade-offs

| Aspect | Option 1 | Option 2 | Choice |
|--------|----------|----------|--------|
| Protocol | WebSocket | HTTP Long Polling | WebSocket (lower latency) |
| Message Store | DynamoDB | RDS | DynamoDB (better scale) |
| Presence | Redis | DynamoDB | Redis (real-time) |
| File Storage | S3 | EBS | S3 (unlimited scale) |

### Cost Estimation (Monthly)

- API Gateway: $1.00 per million messages = $2,592
- ALB: $0.0225 per hour = $16.20
- ECS: 20 t3.large instances = $2,400
- ElastiCache: 5 cache.r6g.xlarge = $1,500
- DynamoDB: On-demand = $2,000
- S3: Storage + requests = $500
- SQS/SNS: $100
- **Total: ~$9,100/month**

---

## 7. Design Pattern 4: Video Streaming Platform

### Requirements

**Functional:**
- Upload videos
- Transcode videos
- Stream videos
- Video recommendations
- User profiles
- Comments and likes

**Non-Functional:**
- Support 4K streaming
- Low buffering (< 2%)
- Handle 100M users
- 10M videos
- Global distribution

### Capacity Estimation

**Users:**
- 100M users
- 10M daily active users
- 1M concurrent viewers

**Videos:**
- 10M videos
- Average video: 500 MB
- Total storage: 5 PB

**Bandwidth:**
- 1M concurrent * 5 Mbps = 5 Tbps
- Peak: 10 Tbps

### Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  CloudFront     │
│  (CDN)          │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  MediaPackage   │
│  (Origin)       │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│   S3     │      │  Transcoding │   │  Metadata   │
│ (Storage)│      │  (MediaConvert│   │ (DynamoDB) │
└──────────┘      └──────────────┘   └─────────────┘
```

### AWS Architecture

**Components:**

1. **S3**
   - Original video storage
   - Transcoded video storage
   - Thumbnails and metadata
   - Lifecycle policies for archival

2. **MediaConvert**
   - Video transcoding
   - Multiple quality levels
   - Adaptive bitrate streaming
   - Batch and on-demand

3. **MediaPackage**
   - Video origin server
   - HLS/DASH packaging
   - DRM support
   - Ad insertion

4. **CloudFront**
   - Global CDN
   - Video delivery
   - Low latency
   - High throughput

5. **Lambda**
   - Upload processing
   - Transcoding triggers
   - Thumbnail generation
   - Metadata extraction

6. **DynamoDB**
   - Video metadata
   - User data
   - Viewing history
   - Recommendations

7. **ElastiCache**
   - Popular videos cache
   - User session cache
   - Recommendations cache

### Upload Flow

```
1. Client → API Gateway → S3 (multipart upload)
2. S3 event → Lambda (trigger transcoding)
3. Lambda → MediaConvert (start job)
4. MediaConvert → S3 (store transcoded videos)
5. S3 event → Lambda (update metadata)
6. Lambda → DynamoDB (store video info)
7. Lambda → MediaPackage (create channel)
```

### Streaming Flow

```
1. Client requests video
2. CloudFront checks cache
3. If miss, fetch from MediaPackage
4. MediaPackage serves HLS/DASH
5. Client adapts quality based on bandwidth
6. Track viewing in DynamoDB
7. Update recommendations
```

### Transcoding Strategy

**Quality Levels:**
- 4K: 20 Mbps
- 1080p: 5 Mbps
- 720p: 2.5 Mbps
- 480p: 1 Mbps
- 360p: 0.5 Mbps

**Adaptive Bitrate:**
- HLS with multiple bitrates
- Client switches automatically
- Smooth playback experience

### Storage Strategy

**S3 Lifecycle Policies:**
```
1. Standard (0-30 days): Hot storage
2. Standard-IA (30-90 days): Infrequent access
3. Glacier (90-365 days): Archive
4. Deep Archive (365+ days): Long-term
```

**Cost Optimization:**
- Delete unused videos after 1 year
- Compress thumbnails
- Use S3 Intelligent-Tiering

### Recommendation System

**Algorithm:**
1. Collaborative filtering
2. Content-based filtering
3. Trending videos
4. User watch history

**Implementation:**
- Pre-compute recommendations (Lambda + EMR)
- Store in ElastiCache
- Update in real-time
- Use DynamoDB for history

### Monitoring

**Key Metrics:**
- Buffering ratio
- Average bitrate
- Playback start time
- Error rate
- Concurrent viewers

**CloudWatch:**
- MediaConvert job status
- CloudFront cache hit ratio
- S3 request metrics
- Lambda execution metrics

---

## 8. Design Pattern 5: Social Media Feed

### Requirements

**Functional:**
- Create posts
- View feed (timeline)
- Like/comment/share
- Follow/unfollow users
- Trending topics

**Non-Functional:**
- Feed generation < 200ms
- Handle 1B users
- 500M posts/day
- Real-time updates

### Capacity Estimation

**Users:**
- 1B total users
- 200M daily active
- 50M concurrent

**Posts:**
- 500M posts/day
- Average post: 1 KB
- Storage: 500M * 1 KB = 500 GB/day

**Feed Requests:**
- 200M users * 20 requests/day = 4B requests/day
- Peak: 50K requests/second

### Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│  Load    │      │  Feed        │   │  Timeline   │
│ Balancer │─────▶│  Service     │───▶│  Generator │
│  (ALB)   │      │  (ECS/EKS)   │   │ (Lambda)    │
└──────────┘      └──────┬───────┘   └─────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│ Posts    │      │  Followers   │   │   Feed      │
│ (DynamoDB│      │  (DynamoDB)   │   │   Cache     │
│          │      │              │   │ (ElastiCache│
└──────────┘      └──────────────┘   └─────────────┘
```

### Feed Generation Strategies

**1. Pull Model (Fan-out on Read)**
```
User requests feed:
1. Get user's follow list
2. Fetch recent posts from each followed user
3. Merge and sort by timestamp
4. Return top N posts
```

**Pros:**
- Simple implementation
- Real-time data
- Low write overhead

**Cons:**
- High read load
- Slow for users with many follows

**2. Push Model (Fan-out on Write)**
```
User creates post:
1. Store post in database
2. Get user's followers
3. Write post to each follower's feed
4. Store in feed cache
```

**Pros:**
- Fast feed retrieval
- Low read load

**Cons:**
- High write load
- Slow for users with many followers
- Storage intensive

**3. Hybrid Model (Recommended)**
```
For active users (many followers):
- Use pull model

For inactive users (few followers):
- Use push model

For celebrities (millions of followers):
- Use pull model + cache
```

### AWS Implementation

**Components:**

1. **DynamoDB Tables:**

**Posts Table:**
```
Partition Key: user_id
Sort Key: post_id
Attributes:
  - content
  - timestamp
  - likes_count
  - comments_count
```

**Followers Table:**
```
Partition Key: user_id
Sort Key: follower_id
```

**Following Table:**
```
Partition Key: user_id
Sort Key: following_id
```

**Feed Table (Push Model):**
```
Partition Key: user_id
Sort Key: timestamp (reverse)
Attributes:
  - post_id
  - author_id
  - content
```

2. **ElastiCache (Redis)**
   - Pre-computed feeds
   - Trending posts
   - User sessions

3. **Lambda (Feed Generator)**
   - Background feed generation
   - Fan-out processing
   - Cache warming

4. **SQS**
   - Async feed updates
   - Fan-out queue
   - Retry mechanism

### Feed Generation Flow

**Pull Model:**
```python
def get_feed_pull(user_id, limit=20):
    # Get following list
    following = get_following(user_id)
    
    # Fetch recent posts
    posts = []
    for followee_id in following:
        recent_posts = dynamodb.query(
            TableName='posts',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': followee_id},
            Limit=10,
            ScanIndexForward=False
        )
        posts.extend(recent_posts)
    
    # Sort by timestamp
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Return top N
    return posts[:limit]
```

**Push Model:**
```python
def create_post_push(user_id, post_content):
    # Create post
    post_id = generate_id()
    post = {
        'user_id': user_id,
        'post_id': post_id,
        'content': post_content,
        'timestamp': time.time()
    }
    dynamodb.put_item(TableName='posts', Item=post)
    
    # Get followers
    followers = get_followers(user_id)
    
    # Fan-out to followers' feeds
    for follower_id in followers:
        feed_item = {
            'user_id': follower_id,
            'timestamp': post['timestamp'],
            'post_id': post_id,
            'author_id': user_id,
            'content': post_content
        }
        dynamodb.put_item(TableName='feeds', Item=feed_item)
        
        # Invalidate cache
        redis_client.delete(f'feed:{follower_id}')
```

**Hybrid Model:**
```python
def get_feed_hybrid(user_id, limit=20):
    # Check cache first
    cached_feed = redis_client.get(f'feed:{user_id}')
    if cached_feed:
        return json.loads(cached_feed)
    
    # Check follower count
    follower_count = get_follower_count(user_id)
    
    if follower_count < 1000:
        # Use push model (pre-computed feed)
        feed = get_feed_from_table(user_id, limit)
    else:
        # Use pull model (real-time)
        feed = get_feed_pull(user_id, limit)
    
    # Cache result
    redis_client.setex(
        f'feed:{user_id}',
        300,  # 5 minutes
        json.dumps(feed)
    )
    
    return feed
```

### Real-time Updates

**WebSocket for Live Feed:**
```python
# When new post created
def notify_followers(author_id, post_id):
    followers = get_followers(author_id)
    
    for follower_id in followers:
        # Send via WebSocket if online
        if is_online(follower_id):
            websocket.send(follower_id, {
                'type': 'new_post',
                'post_id': post_id,
                'author_id': author_id
            })
        
        # Update feed cache
        redis_client.lpush(f'feed:{follower_id}', post_id)
        redis_client.ltrim(f'feed:{follower_id}', 0, 99)  # Keep last 100
```

### Trending Algorithm

**Factors:**
- Likes in last hour
- Comments in last hour
- Shares in last hour
- Time decay factor

**Implementation:**
```python
def calculate_trending_score(post, current_time):
    time_diff = current_time - post['created_at']
    time_decay = math.exp(-time_diff / 3600)  # 1 hour half-life
    
    score = (
        post['likes_count'] * 1 +
        post['comments_count'] * 2 +
        post['shares_count'] * 3
    ) * time_decay
    
    return score

# Update trending posts every 5 minutes
def update_trending():
    all_posts = get_recent_posts(hours=24)
    trending = sorted(
        all_posts,
        key=lambda p: calculate_trending_score(p, time.time()),
        reverse=True
    )[:100]
    
    redis_client.setex(
        'trending:posts',
        300,
        json.dumps(trending)
    )
```

### Scaling Considerations

**Database Sharding:**
- Partition by user_id
- Use consistent hashing
- Distribute load evenly

**Caching Strategy:**
- Cache hot feeds (active users)
- Pre-warm feeds for top users
- Use CDN for static content

**Fan-out Optimization:**
- Batch writes
- Use SQS for async processing
- Limit fan-out for celebrities

---

## 9. Design Pattern 6: E-Commerce Platform

### Requirements

**Functional:**
- Product catalog
- Shopping cart
- Order processing
- Payment processing
- Inventory management
- Recommendations
- Reviews and ratings

**Non-Functional:**
- Handle 10M products
- 1M orders/day
- 99.99% availability
- < 200ms page load
- Handle flash sales

### Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  CloudFront     │
│  (CDN)          │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│  Load    │      │  Application │   │   Cache     │
│ Balancer │─────▶│   Servers    │───▶│ (ElastiCache│
│  (ALB)   │      │  (ECS/EKS)   │   │   Redis)    │
└──────────┘      └──────┬───────┘   └─────────────┘
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│ Products │      │   Orders     │   │  Inventory  │
│(DynamoDB)│      │  (RDS)       │   │ (DynamoDB)  │
└──────────┘      └──────────────┘   └─────────────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Payment    │
                  │  (External)  │
                  └──────────────┘
```

### AWS Components

**1. Product Catalog (DynamoDB)**
```
Partition Key: product_id
Attributes:
  - name
  - description
  - price
  - category
  - images
  - rating
  - review_count
  - in_stock
```

**GSI: category-index**
- Partition Key: category
- Sort Key: rating

**2. Shopping Cart (ElastiCache)**
```
Key: cart:{user_id}
Value: {
  "items": [
    {"product_id": "123", "quantity": 2, "price": 29.99}
  ],
  "total": 59.98,
  "updated_at": timestamp
}
TTL: 7 days
```

**3. Orders (RDS PostgreSQL)**
```sql
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    items JSONB,
    total DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

**4. Inventory (DynamoDB)**
```
Partition Key: product_id
Attributes:
  - quantity
  - reserved
  - last_updated
```

**5. S3**
- Product images
- Static assets
- CDN via CloudFront

### Order Processing Flow

```
1. User adds items to cart (ElastiCache)
2. User proceeds to checkout
3. Reserve inventory (DynamoDB with conditional update)
4. Create order (RDS)
5. Process payment (External service)
6. If success:
   - Update order status
   - Deduct inventory
   - Send confirmation (SNS)
   - Clear cart
7. If failure:
   - Release inventory
   - Update order status
```

### Inventory Management

**Optimistic Locking:**
```python
def reserve_inventory(product_id, quantity):
    while True:
        item = dynamodb.get_item(
            TableName='inventory',
            Key={'product_id': product_id}
        )
        
        current_qty = item['quantity'] - item['reserved']
        
        if current_qty < quantity:
            raise InsufficientInventory()
        
        try:
            dynamodb.update_item(
                TableName='inventory',
                Key={'product_id': product_id},
                UpdateExpression='ADD reserved :qty',
                ConditionExpression='quantity - reserved >= :qty',
                ExpressionAttributeValues={':qty': quantity}
            )
            return True
        except ConditionalCheckFailedException:
            # Retry
            continue
```

### Flash Sale Handling

**Problem:** High traffic spike for limited inventory

**Solution:**
1. **Pre-warm cache:**
   - Cache product details
   - Cache inventory count
   - Use ElastiCache

2. **Queue-based ordering:**
   - Use SQS for order requests
   - Process orders sequentially
   - Prevent overselling

3. **Rate limiting:**
   - API Gateway throttling
   - Per-user limits
   - Distributed rate limiting (Redis)

4. **Database optimization:**
   - Read replicas
   - Connection pooling
   - Prepared statements

### Search Functionality

**Option 1: DynamoDB Scan (Not Recommended)**
- Slow and expensive
- Only for small catalogs

**Option 2: Elasticsearch (OpenSearch)**
- Full-text search
- Faceted search
- Autocomplete
- AWS: Amazon OpenSearch Service

**Implementation:**
```python
# Index products
def index_product(product):
    opensearch.index(
        index='products',
        id=product['product_id'],
        body=product
    )

# Search
def search_products(query, filters):
    results = opensearch.search(
        index='products',
        body={
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['name^2', 'description']
                }
            },
            'filter': filters
        }
    )
    return results
```

### Recommendations

**Collaborative Filtering:**
- User purchase history
- Similar users
- Item-based recommendations

**Implementation:**
- Pre-compute with EMR
- Store in ElastiCache
- Update daily

### Payment Processing

**Flow:**
```
1. Create payment intent
2. Process via payment gateway (Stripe, PayPal)
3. Webhook for confirmation
4. Update order status
5. Send notification
```

**AWS Services:**
- Lambda for webhook handling
- SQS for async processing
- SNS for notifications

---

## 10. Design Pattern 7: Search Engine

### Requirements

**Functional:**
- Web crawling
- Indexing
- Search queries
- Ranking
- Autocomplete
- Spell correction

**Non-Functional:**
- Index 10B web pages
- Handle 10K queries/second
- < 100ms search latency
- 99.9% availability

### Architecture

```
┌─────────────┐
│   Crawler   │
│  (EC2/ECS)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  URL Frontier  │
│  (SQS)         │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Document Store │
│  (S3)           │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Indexer       │
│  (EMR/Lambda)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Search Index   │
│  (OpenSearch)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Query Service  │
│  (ECS/EKS)      │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Client        │
└─────────────────┘
```

### AWS Components

**1. Crawler (ECS/EKS)**
- Distributed crawling
- Respect robots.txt
- Rate limiting
- URL deduplication

**2. URL Frontier (SQS)**
- Queue of URLs to crawl
- Priority queues
- Deduplication

**3. Document Store (S3)**
- Raw HTML content
- Metadata
- Lifecycle policies

**4. Indexer (EMR)**
- Parse documents
- Extract text
- Build inverted index
- Update search index

**5. OpenSearch**
- Inverted index
- Full-text search
- Ranking
- Faceted search

**6. Query Service (ECS/EKS)**
- Process queries
- Query optimization
- Result ranking
- Caching

### Crawling System

**URL Frontier:**
```python
# Priority queues
high_priority_queue = sqs.Queue('crawl-high-priority')
normal_queue = sqs.Queue('crawl-normal')
low_priority_queue = sqs.Queue('crawl-low-priority')

# Deduplication
seen_urls = set()  # Use DynamoDB in production

def add_url(url, priority='normal'):
    if url in seen_urls:
        return
    
    seen_urls.add(url)
    
    if priority == 'high':
        high_priority_queue.send_message(MessageBody=url)
    elif priority == 'normal':
        normal_queue.send_message(MessageBody=url)
    else:
        low_priority_queue.send_message(MessageBody=url)
```

**Crawler:**
```python
def crawl_url(url):
    # Fetch page
    response = requests.get(url, timeout=10)
    html = response.text
    
    # Store in S3
    s3.put_object(
        Bucket='crawled-documents',
        Key=f'{hash(url)}.html',
        Body=html
    )
    
    # Extract links
    links = extract_links(html, url)
    
    # Add to frontier
    for link in links:
        add_url(link, priority='normal')
    
    # Extract metadata
    metadata = {
        'url': url,
        'title': extract_title(html),
        'content': extract_text(html),
        'crawled_at': time.time()
    }
    
    # Send to indexer
    sqs.send_message(
        QueueUrl=indexer_queue_url,
        MessageBody=json.dumps(metadata)
    )
```

### Indexing System

**Inverted Index:**
```
Term -> [Document IDs with term]

Example:
"python" -> [doc1, doc5, doc12]
"aws" -> [doc2, doc5, doc8]
```

**Indexing Process:**
```python
def index_document(metadata):
    # Parse document
    words = tokenize(metadata['content'])
    
    # Build index entries
    index_entries = {}
    for word in words:
        if word not in index_entries:
            index_entries[word] = []
        index_entries[word].append({
            'doc_id': metadata['doc_id'],
            'tf': count_term_frequency(word, words),
            'positions': get_positions(word, words)
        })
    
    # Update OpenSearch
    for term, postings in index_entries.items():
        opensearch.update(
            index='search_index',
            id=term,
            body={
                'script': {
                    'source': 'ctx._source.postings.addAll(params.postings)',
                    'params': {'postings': postings}
                },
                'upsert': {'postings': postings}
            }
        )
```

### Search Query Processing

**Query Flow:**
```
1. Parse query
2. Check cache (ElastiCache)
3. If miss:
   - Tokenize query
   - Lookup terms in index
   - Compute relevance scores
   - Rank results
   - Cache results
4. Return top N results
```

**Ranking Algorithm (TF-IDF + PageRank):**
```python
def calculate_relevance(query_terms, document):
    score = 0
    
    for term in query_terms:
        # Term Frequency
        tf = document['tf'][term] if term in document['tf'] else 0
        
        # Inverse Document Frequency
        idf = math.log(total_docs / doc_frequency[term])
        
        # PageRank
        pagerank = document['pagerank']
        
        # Combined score
        score += tf * idf * pagerank
    
    return score
```

### Autocomplete

**Trie Data Structure:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.suggestions = []

def build_autocomplete_trie(queries):
    root = TrieNode()
    
    for query, frequency in queries:
        node = root
        for char in query:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.suggestions.append((query, frequency))
        node.is_end = True
    
    return root

def autocomplete(prefix, trie):
    node = trie
    for char in prefix:
        if char not in node.children:
            return []
        node = node.children[char]
    
    # Return top suggestions
    return sorted(
        node.suggestions,
        key=lambda x: x[1],
        reverse=True
    )[:10]
```

**AWS Implementation:**
- Store in ElastiCache (Redis)
- Update daily from query logs
- Fast prefix matching

### Spell Correction

**Edit Distance Algorithm:**
```python
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def correct_spelling(query, dictionary):
    min_distance = float('inf')
    best_match = query
    
    for word in dictionary:
        distance = levenshtein_distance(query, word)
        if distance < min_distance:
            min_distance = distance
            best_match = word
    
    return best_match if min_distance <= 2 else query
```

---

## 11. Design Pattern 8: Notification System

### Requirements

**Functional:**
- Send notifications (email, SMS, push)
- Notification preferences
- Delivery tracking
- Retry mechanism
- Batching

**Non-Functional:**
- Handle 1B notifications/day
- < 1 second delivery
- 99.9% delivery rate
- Support multiple channels

### Architecture

```
┌─────────────┐
│ Application │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Notification   │
│  API Gateway    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Notification   │
│  Service        │
│  (Lambda/ECS)   │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│   SQS    │      │  Preferences │   │   Template  │
│  (Queue) │      │  (DynamoDB)   │   │   (S3)      │
└──────┬───┘      └──────────────┘   └─────────────┘
       │
       ▼
┌─────────────────┐
│  Workers        │
│  (Lambda/ECS)   │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│   SNS    │      │   SES        │   │   SNS       │
│  (Push)  │      │  (Email)     │   │  (SMS)      │
└──────────┘      └──────────────┘   └─────────────┘
```

### AWS Components

**1. SQS**
- Notification queue
- Dead letter queue
- Priority queues
- Batching

**2. SNS**
- Push notifications (mobile)
- SMS notifications
- Topic-based routing

**3. SES**
- Email delivery
- Template management
- Bounce/complaint handling

**4. DynamoDB**
- User preferences
- Delivery tracking
- Notification history

**5. Lambda**
- Notification processing
- Template rendering
- Retry logic

### Notification Flow

```
1. Application sends notification request
2. Notification service:
   - Check user preferences
   - Load template
   - Personalize message
   - Enqueue to SQS
3. Worker processes queue:
   - Dequeue message
   - Route to appropriate channel
   - Send via SNS/SES
   - Update delivery status
4. Handle failures:
   - Retry with exponential backoff
   - Move to DLQ after max retries
```

### Multi-Channel Support

**Channel Router:**
```python
def send_notification(user_id, notification_type, data):
    # Get user preferences
    preferences = get_preferences(user_id)
    
    # Determine channels
    channels = []
    if preferences.get('email_enabled', True):
        channels.append('email')
    if preferences.get('sms_enabled', False):
        channels.append('sms')
    if preferences.get('push_enabled', True):
        channels.append('push')
    
    # Send to each channel
    for channel in channels:
        send_to_channel(user_id, channel, notification_type, data)

def send_to_channel(user_id, channel, notification_type, data):
    # Load template
    template = load_template(notification_type, channel)
    
    # Render message
    message = render_template(template, data)
    
    # Send
    if channel == 'email':
        ses.send_email(
            Destination={'ToAddresses': [get_email(user_id)]},
            Message={'Subject': message['subject'], 'Body': message['body']}
        )
    elif channel == 'sms':
        sns.publish(
            PhoneNumber=get_phone(user_id),
            Message=message['text']
        )
    elif channel == 'push':
        sns.publish(
            TargetArn=get_push_endpoint(user_id),
            Message=json.dumps(message)
        )
    
    # Track delivery
    track_delivery(user_id, channel, notification_type)
```

### Batching

**Email Batching:**
```python
def batch_emails():
    batch = []
    batch_size = 50
    
    while True:
        message = sqs.receive_message(QueueUrl=email_queue)
        if not message:
            break
        
        batch.append(message)
        
        if len(batch) >= batch_size:
            send_batch(batch)
            batch = []
    
    if batch:
        send_batch(batch)

def send_batch(messages):
    # Prepare batch
    email_data = []
    for msg in messages:
        email_data.append({
            'Destination': {'ToAddresses': [msg['email']]},
            'Message': {
                'Subject': {'Data': msg['subject']},
                'Body': {'Text': {'Data': msg['body']}}
            }
        })
    
    # Send batch
    ses.send_bulk_templated_email(
        Source='noreply@example.com',
        Template='notification-template',
        DefaultTemplateData='{}',
        Destinations=email_data
    )
```

### Retry Mechanism

**Exponential Backoff:**
```python
def send_with_retry(user_id, channel, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            send_to_channel(user_id, channel, message)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                # Move to DLQ
                send_to_dlq(user_id, channel, message, str(e))
                return False
            
            # Wait before retry
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
    
    return False
```

### Delivery Tracking

**DynamoDB Schema:**
```
Partition Key: notification_id
Attributes:
  - user_id
  - channel
  - status (pending/sent/delivered/failed)
  - sent_at
  - delivered_at
  - retry_count
```

**Tracking:**
```python
def track_delivery(notification_id, status):
    dynamodb.update_item(
        TableName='notifications',
        Key={'notification_id': notification_id},
        UpdateExpression='SET #status = :status, updated_at = :now',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': status,
            ':now': time.time()
        }
    )
```

---

## 12. Design Pattern 9: Rate Limiting System

### Requirements

**Functional:**
- Limit requests per user/IP
- Multiple rate limit algorithms
- Distributed rate limiting
- Whitelist/blacklist

**Non-Functional:**
- Handle 1M requests/second
- < 1ms overhead
- 99.99% availability

### Algorithms

**1. Token Bucket**
```
- Bucket with capacity C tokens
- Refill rate: R tokens/second
- Request consumes 1 token
- Reject if bucket empty
```

**2. Leaky Bucket**
```
- Queue with capacity C
- Process rate: R requests/second
- Reject if queue full
```

**3. Fixed Window**
```
- Count requests in time window
- Reset counter at window end
- Reject if count > limit
```

**4. Sliding Window**
```
- Track requests in sliding window
- More accurate than fixed window
- Higher memory usage
```

### AWS Implementation

**ElastiCache (Redis) for Rate Limiting:**

**Token Bucket:**
```python
def check_rate_limit_token_bucket(user_id, capacity, refill_rate):
    key = f'ratelimit:{user_id}'
    
    # Get current state
    pipe = redis.pipeline()
    pipe.get(key)
    pipe.ttl(key)
    result = pipe.execute()
    
    tokens = int(result[0]) if result[0] else capacity
    ttl = result[1] if result[1] > 0 else 60
    
    # Refill tokens
    elapsed = 60 - ttl
    tokens = min(capacity, tokens + elapsed * refill_rate)
    
    # Check limit
    if tokens < 1:
        return False, ttl
    
    # Consume token
    redis.setex(key, 60, tokens - 1)
    
    return True, 60
```

**Sliding Window:**
```python
def check_rate_limit_sliding_window(user_id, limit, window_seconds):
    key = f'ratelimit:{user_id}'
    now = time.time()
    
    # Remove old entries
    redis.zremrangebyscore(key, 0, now - window_seconds)
    
    # Count current requests
    count = redis.zcard(key)
    
    if count >= limit:
        # Get oldest request time
        oldest = redis.zrange(key, 0, 0, withscores=True)
        if oldest:
            ttl = int(oldest[0][1] + window_seconds - now)
            return False, ttl
        return False, window_seconds
    
    # Add current request
    redis.zadd(key, {str(now): now})
    redis.expire(key, window_seconds)
    
    return True, window_seconds
```

**API Gateway Rate Limiting:**
```yaml
# API Gateway usage plan
UsagePlan:
  Name: StandardPlan
  Throttle:
    BurstLimit: 100
    RateLimit: 50
  Quota:
    Limit: 10000
    Period: DAY

# API Key
ApiKey:
  Name: user-api-key
  Enabled: true
```

### Distributed Rate Limiting

**Problem:** Multiple servers need shared rate limit

**Solution:** Use Redis with Lua script for atomicity

```lua
-- Lua script for atomic rate limiting
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Remove old entries
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

-- Count current
local count = redis.call('ZCARD', key)

if count < limit then
    -- Add current request
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, window)
    return {1, window}  -- allowed, ttl
else
    -- Get oldest
    local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
    local ttl = window - (now - tonumber(oldest[2]))
    return {0, ttl}  -- denied, ttl
end
```

**Python Implementation:**
```python
def check_rate_limit_distributed(user_id, limit, window):
    script = """
    -- Lua script here
    """
    
    result = redis.eval(
        script,
        1,  # num keys
        f'ratelimit:{user_id}',
        limit,
        window,
        time.time()
    )
    
    allowed, ttl = result
    return allowed == 1, ttl
```

### Multi-Level Rate Limiting

**Hierarchical Limits:**
```
Global: 10K req/s
Per User: 100 req/s
Per IP: 50 req/s
```

**Implementation:**
```python
def check_multi_level_rate_limit(user_id, ip_address):
    # Check global limit
    global_allowed, _ = check_rate_limit('global', 10000, 1)
    if not global_allowed:
        return False, 'Global limit exceeded'
    
    # Check user limit
    user_allowed, ttl = check_rate_limit(user_id, 100, 1)
    if not user_allowed:
        return False, f'User limit exceeded, retry in {ttl}s'
    
    # Check IP limit
    ip_allowed, ttl = check_rate_limit(ip_address, 50, 1)
    if not ip_allowed:
        return False, f'IP limit exceeded, retry in {ttl}s'
    
    return True, None
```

---

## 13. Design Pattern 10: Distributed File Storage

### Requirements

**Functional:**
- Upload/download files
- File versioning
- Access control
- File sharing
- Search

**Non-Functional:**
- Store 1PB of data
- Handle 100K uploads/day
- 99.99% durability
- Global access

### Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  API Gateway    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Application    │
│  Service        │
└──────┬──────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌──────────┐      ┌──────────────┐   ┌─────────────┐
│   S3     │      │  Metadata    │   │   CDN       │
│(Storage) │      │  (DynamoDB)  │   │ (CloudFront)│
└──────────┘      └──────────────┘   └─────────────┘
```

### AWS S3 Architecture

**Bucket Structure:**
```
bucket-name/
  users/
    {user_id}/
      files/
        {file_id}/
          v1/
          v2/
          metadata.json
  shared/
    {share_id}/
```

**S3 Features:**
- **Versioning**: Keep multiple versions
- **Lifecycle Policies**: Move to cheaper storage
- **Cross-Region Replication**: Disaster recovery
- **Encryption**: At-rest and in-transit
- **Access Control**: IAM, bucket policies, ACLs

### File Upload Flow

**Multipart Upload:**
```python
def upload_large_file(file_path, user_id, file_name):
    # Initiate multipart upload
    upload_id = s3.create_multipart_upload(
        Bucket='file-storage',
        Key=f'users/{user_id}/files/{file_id}/v1',
        Metadata={'filename': file_name}
    )['UploadId']
    
    # Upload parts (5MB each)
    parts = []
    part_number = 1
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(5 * 1024 * 1024)  # 5MB
            if not chunk:
                break
            
            part = s3.upload_part(
                Bucket='file-storage',
                Key=f'users/{user_id}/files/{file_id}/v1',
                PartNumber=part_number,
                UploadId=upload_id,
                Body=chunk
            )
            parts.append({
                'ETag': part['ETag'],
                'PartNumber': part_number
            })
            part_number += 1
    
    # Complete upload
    s3.complete_multipart_upload(
        Bucket='file-storage',
        Key=f'users/{user_id}/files/{file_id}/v1',
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
    
    # Store metadata
    store_metadata(user_id, file_id, file_name, upload_id)
```

### Metadata Management

**DynamoDB Schema:**
```
Partition Key: user_id
Sort Key: file_id
Attributes:
  - filename
  - size
  - content_type
  - s3_key
  - version
  - created_at
  - updated_at
  - shared_with (List)
  - permissions
```

### File Download Flow

```
1. Client requests file
2. Check permissions (DynamoDB)
3. Generate presigned URL (S3)
4. Return URL to client
5. Client downloads directly from S3
```

**Presigned URL:**
```python
def get_download_url(user_id, file_id, expires_in=3600):
    # Check permissions
    file_metadata = get_file_metadata(user_id, file_id)
    if not has_permission(user_id, file_metadata):
        raise PermissionDenied()
    
    # Generate presigned URL
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'file-storage',
            'Key': file_metadata['s3_key']
        },
        ExpiresIn=expires_in
    )
    
    return url
```

### File Sharing

**Share Link:**
```python
def create_share_link(user_id, file_id, expires_in=None):
    # Generate share token
    share_token = generate_token()
    
    # Store share info
    dynamodb.put_item(
        TableName='shares',
        Item={
            'share_token': share_token,
            'user_id': user_id,
            'file_id': file_id,
            'created_at': time.time(),
            'expires_at': time.time() + expires_in if expires_in else None,
            'access_count': 0
        }
    )
    
    return f'https://files.example.com/share/{share_token}'

def access_shared_file(share_token):
    # Get share info
    share = dynamodb.get_item(
        TableName='shares',
        Key={'share_token': share_token}
    )
    
    if not share:
        raise NotFound()
    
    # Check expiration
    if share.get('expires_at') and share['expires_at'] < time.time():
        raise Expired()
    
    # Update access count
    dynamodb.update_item(
        TableName='shares',
        Key={'share_token': share_token},
        UpdateExpression='ADD access_count :one',
        ExpressionAttributeValues={':one': 1}
    )
    
    # Get file
    return get_file(share['user_id'], share['file_id'])
```

### Storage Optimization

**Lifecycle Policies:**
```json
{
  "Rules": [
    {
      "Id": "Move to IA",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        }
      ]
    },
    {
      "Id": "Archive old files",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "Delete very old",
      "Status": "Enabled",
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**Deduplication:**
```python
def upload_file_with_dedup(file_content, user_id, file_name):
    # Calculate hash
    file_hash = hashlib.sha256(file_content).hexdigest()
    
    # Check if file exists
    existing = dynamodb.query(
        TableName='file_hashes',
        KeyConditionExpression='file_hash = :hash',
        ExpressionAttributeValues={':hash': file_hash}
    )
    
    if existing:
        # File already exists, create reference
        existing_file_id = existing[0]['file_id']
        create_file_reference(user_id, file_name, existing_file_id)
        return existing_file_id
    
    # Upload new file
    file_id = upload_to_s3(file_content, user_id)
    
    # Store hash
    dynamodb.put_item(
        TableName='file_hashes',
        Item={
            'file_hash': file_hash,
            'file_id': file_id
        }
    )
    
    return file_id
```

---

## 14. Scalability Patterns

### Horizontal Scaling

**Auto Scaling Groups:**
```yaml
AutoScalingGroup:
  MinSize: 2
  MaxSize: 10
  DesiredCapacity: 4
  TargetTrackingScalingPolicy:
    PredefinedMetricSpecification:
      PredefinedMetricType: ASGAverageCPUUtilization
    TargetValue: 70.0
```

**ECS Auto Scaling:**
```python
# Service auto scaling
ecs.update_service(
    cluster='my-cluster',
    service='my-service',
    desiredCount=5
)

# Application auto scaling
application_autoscaling.register_scalable_target(
    ServiceNamespace='ecs',
    ResourceId='service/my-cluster/my-service',
    ScalableDimension='ecs:service:DesiredCount',
    MinCapacity=2,
    MaxCapacity=20
)
```

### Database Scaling

**Read Replicas:**
```python
# RDS read replica
rds.create_db_instance_read_replica(
    DBInstanceIdentifier='my-db-replica',
    SourceDBInstanceIdentifier='my-db',
    PubliclyAccessible=False
)

# Route reads to replica
def get_connection(read_only=False):
    if read_only:
        return get_replica_connection()
    return get_primary_connection()
```

**DynamoDB Scaling:**
- Automatic scaling
- On-demand capacity
- Global tables for multi-region

### Caching Strategy

**Multi-Level Caching:**
```
L1: Application cache (in-memory)
L2: ElastiCache (Redis)
L3: CloudFront (CDN)
L4: Database
```

**Cache Warming:**
```python
def warm_cache():
    # Pre-load popular data
    popular_items = get_popular_items()
    
    for item in popular_items:
        redis_client.setex(
            f'item:{item.id}',
            3600,
            json.dumps(item)
        )
```

### Load Distribution

**Geographic Distribution:**
- Multi-region deployment
- Route 53 geolocation routing
- CloudFront edge locations

**Content Distribution:**
- CloudFront for static content
- Regional caches
- Edge computing (Lambda@Edge)

---

## 15. Reliability and High Availability

### Multi-AZ Deployment

**RDS Multi-AZ:**
```python
rds.create_db_instance(
    DBInstanceIdentifier='my-db',
    MultiAZ=True,  # Automatic failover
    BackupRetentionPeriod=7
)
```

**Application Multi-AZ:**
- Deploy in multiple availability zones
- Use ALB with health checks
- Auto-recovery

### Disaster Recovery

**Backup Strategy:**
- Automated backups (RDS, EBS)
- Cross-region replication (S3, DynamoDB)
- Point-in-time recovery

**Recovery Time Objective (RTO):** < 1 hour
**Recovery Point Objective (RPO):** < 15 minutes

**Implementation:**
```python
# Cross-region replication
s3.put_bucket_replication(
    Bucket='my-bucket',
    ReplicationConfiguration={
        'Role': 'arn:aws:iam::account:role/replication-role',
        'Rules': [{
            'Status': 'Enabled',
            'Destination': {
                'Bucket': 'arn:aws:s3:::my-bucket-replica',
                'Region': 'us-west-2'
            }
        }]
    }
)
```

### Circuit Breaker Pattern

**Implementation:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpen()
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise
```

### Health Checks

**Application Health:**
```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database(),
        'cache': check_cache(),
        's3': check_s3()
    }
    
    if all(checks.values()):
        return {'status': 'healthy'}, 200
    else:
        return {'status': 'unhealthy', 'checks': checks}, 503
```

**ALB Health Checks:**
```yaml
HealthCheck:
  HealthyThresholdCount: 2
  UnhealthyThresholdCount: 3
  Interval: 30
  Timeout: 5
  Path: /health
  Protocol: HTTP
  Matcher:
    HttpCode: '200'
```

---

## 16. Performance Optimization

### Database Optimization

**Indexing:**
```sql
-- RDS indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_user_date ON orders(user_id, created_at);

-- DynamoDB GSIs
GlobalSecondaryIndex:
  IndexName: email-index
  KeySchema:
    - AttributeName: email
      KeyType: HASH
  Projection:
    ProjectionType: ALL
```

**Query Optimization:**
- Use prepared statements
- Limit result sets
- Use pagination
- Avoid N+1 queries

### Caching Optimization

**Cache Patterns:**
- Cache-aside
- Write-through
- Write-behind
- Refresh-ahead

**Cache Invalidation:**
- TTL-based
- Event-based
- Tag-based

### CDN Optimization

**CloudFront Configuration:**
- Cache behaviors
- Origin failover
- Compression
- HTTP/2

**Edge Computing:**
- Lambda@Edge for custom logic
- Reduce origin load
- Lower latency

### Connection Pooling

**RDS Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://...',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

---

## 17. Security Patterns

### Authentication & Authorization

**Cognito:**
- User pools for authentication
- Identity pools for AWS access
- Social login integration
- MFA support

**IAM Roles:**
- Least privilege
- Role-based access
- Temporary credentials

### Data Encryption

**At Rest:**
- S3 server-side encryption (SSE)
- RDS encryption
- EBS encryption
- DynamoDB encryption

**In Transit:**
- TLS/SSL
- API Gateway HTTPS
- CloudFront HTTPS

### Network Security

**VPC:**
- Private subnets
- Security groups
- NACLs
- VPN/Direct Connect

**WAF:**
- DDoS protection
- SQL injection prevention
- XSS protection
- Rate limiting

### Secrets Management

**Secrets Manager:**
```python
import boto3

secrets_client = boto3.client('secretsmanager')

# Store secret
secrets_client.create_secret(
    Name='db-credentials',
    SecretString=json.dumps({
        'username': 'admin',
        'password': 'secret'
    })
)

# Retrieve secret
secret = secrets_client.get_secret_value(SecretId='db-credentials')
credentials = json.loads(secret['SecretString'])
```

---

## 18. Cost Optimization

### Right-Sizing

**EC2:**
- Use appropriate instance types
- Reserved instances for predictable workloads
- Spot instances for flexible workloads

**RDS:**
- Choose right instance class
- Use read replicas instead of larger instances
- Storage autoscaling

### Storage Optimization

**S3 Storage Classes:**
- Standard: Hot data
- Standard-IA: Infrequent access
- One Zone-IA: Single AZ
- Glacier: Archive
- Intelligent-Tiering: Automatic optimization

**Lifecycle Policies:**
- Move to cheaper storage
- Delete old data
- Reduce costs by 50-80%

### Compute Optimization

**Serverless:**
- Lambda for event-driven workloads
- Pay per request
- No idle costs

**Container Optimization:**
- Fargate spot for cost savings
- Right-size container resources
- Use spot instances

### Monitoring Costs

**Cost Explorer:**
- Track spending
- Identify cost drivers
- Budget alerts

**Tags:**
- Tag resources for cost allocation
- Track by project/environment
- Optimize based on data

---

## 19. Monitoring and Observability

### CloudWatch

**Metrics:**
- Custom metrics
- Application metrics
- Infrastructure metrics

**Logs:**
- Centralized logging
- Log groups and streams
- Log insights

**Alarms:**
- Threshold-based
- Anomaly detection
- SNS notifications

### X-Ray

**Distributed Tracing:**
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()  # Patch libraries

@xray_recorder.capture('process_order')
def process_order(order_id):
    # Traced function
    pass
```

### Dashboards

**CloudWatch Dashboards:**
- Custom visualizations
- Real-time metrics
- Multiple data sources

**Grafana:**
- Advanced visualizations
- Multiple data sources
- Alerting

---

## 20. Best Practices and Trade-offs

### Design Principles

1. **Scalability First**
   - Design for horizontal scaling
   - Use managed services
   - Plan for growth

2. **Reliability**
   - Multi-AZ deployment
   - Automated backups
   - Disaster recovery

3. **Performance**
   - Caching strategy
   - CDN usage
   - Database optimization

4. **Security**
   - Defense in depth
   - Least privilege
   - Encryption everywhere

5. **Cost Optimization**
   - Right-sizing
   - Reserved instances
   - Storage optimization

### Common Trade-offs

| Aspect | Option A | Option B | When to Choose A | When to Choose B |
|--------|----------|----------|------------------|------------------|
| Database | SQL (RDS) | NoSQL (DynamoDB) | Complex queries, ACID | High scale, simple queries |
| Caching | Redis | Memcached | Persistence needed | Simple key-value |
| Compute | EC2 | Lambda | Long-running, control | Event-driven, serverless |
| Storage | EBS | S3 | Database, low latency | Files, unlimited scale |
| Messaging | SQS | SNS | Point-to-point | Pub/sub |

### Anti-Patterns to Avoid

1. **Single Point of Failure**
   - Always use multi-AZ
   - Avoid single instances

2. **Over-Engineering**
   - Start simple
   - Scale when needed

3. **Ignoring Costs**
   - Monitor spending
   - Optimize continuously

4. **Poor Error Handling**
   - Implement retries
   - Use circuit breakers

5. **No Monitoring**
   - Instrument everything
   - Set up alerts

---

## Summary

This comprehensive tutorial covered:

- **10 Complete System Designs** with AWS implementations
- **Architecture Patterns** for scalability and reliability
- **AWS Service Integration** for each component
- **Best Practices** for production systems
- **Trade-offs Analysis** for decision making
- **Cost Optimization** strategies
- **Security Patterns** for protection
- **Monitoring** for observability

Key takeaways:
- Use managed AWS services for scalability
- Design for failure (multi-AZ, backups)
- Implement caching at multiple levels
- Monitor and optimize continuously
- Balance cost and performance
- Security by design
- Start simple, scale as needed

Each system design includes:
- Requirements and capacity estimation
- High-level architecture
- AWS service mapping
- Detailed implementation
- Scaling considerations
- Cost estimates
- Monitoring strategies

Use this guide as a reference for system design interviews and real-world architecture decisions.

