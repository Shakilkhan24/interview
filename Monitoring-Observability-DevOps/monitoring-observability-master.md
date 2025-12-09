# Monitoring & Observability in DevOps - Master Guide
## Complete Guide to Metrics, Logs, Traces, and Alerting

---

## Table of Contents

1. [Monitoring vs Observability Fundamentals](#1-monitoring-vs-observability-fundamentals)
2. [The Three Pillars of Observability](#2-the-three-pillars-of-observability)
3. [Metrics - Time-Series Data](#3-metrics---time-series-data)
4. [Logs - Event Data](#4-logs---event-data)
5. [Traces - Distributed Tracing](#5-traces---distributed-tracing)
6. [Prometheus & Grafana](#6-prometheus--grafana)
7. [ELK Stack (Elasticsearch, Logstash, Kibana)](#7-elk-stack-elasticsearch-logstash-kibana)
8. [Jaeger & Distributed Tracing](#8-jaeger--distributed-tracing)
9. [Cloud-Native Monitoring](#9-cloud-native-monitoring)
10. [Application Performance Monitoring (APM)](#10-application-performance-monitoring-apm)
11. [Infrastructure Monitoring](#11-infrastructure-monitoring)
12. [Alerting Strategies](#12-alerting-strategies)
13. [SLO, SLA, SLI](#13-slo-sla-sli)
14. [Real-Time Monitoring](#14-real-time-monitoring)
15. [Best Practices & Patterns](#15-best-practices--patterns)

---

## 1. Monitoring vs Observability Fundamentals

### 1.1 What is Monitoring?

**Monitoring** is the practice of collecting, analyzing, and using information to track a system's health and performance.

**Key Characteristics:**
- **Reactive**: Responds to known issues
- **Metric-based**: Focuses on predefined metrics
- **Dashboard-driven**: Visual representation of system state
- **Alert-based**: Notifications when thresholds are exceeded

### 1.2 What is Observability?

**Observability** is the ability to understand a system's internal state by examining its outputs.

**Key Characteristics:**
- **Proactive**: Discovers unknown issues
- **Exploratory**: Investigates unknown unknowns
- **Context-rich**: Provides full context for debugging
- **Three Pillars**: Metrics, Logs, Traces

### 1.3 Monitoring vs Observability

```
Traditional Monitoring:
┌─────────────────────┐
│   Known Metrics     │
│   Predefined Alerts │
│   Dashboards        │
└─────────────────────┘
         ↓
    React to Issues

Observability:
┌─────────────────────┐
│   Metrics           │
│   Logs              │
│   Traces            │
└─────────────────────┘
         ↓
    Explore & Debug
```

**Key Differences:**

| Aspect | Monitoring | Observability |
|--------|-----------|--------------|
| Approach | Reactive | Proactive |
| Focus | Known issues | Unknown issues |
| Data | Metrics | Metrics + Logs + Traces |
| Questions | "Is X broken?" | "Why is X broken?" |
| Tools | Nagios, Zabbix | Prometheus, ELK, Jaeger |

---

## 2. The Three Pillars of Observability

### 2.1 Metrics

**Definition:** Numerical measurements over time

**Characteristics:**
- **Time-series data**: Values at specific timestamps
- **Aggregated**: Summarized data points
- **Efficient**: Low storage overhead
- **Fast queries**: Quick retrieval

**Use Cases:**
- System performance (CPU, memory, disk)
- Application metrics (request rate, error rate)
- Business metrics (revenue, user count)

**Example:**
```
timestamp: 2024-01-01 10:00:00
cpu_usage: 75.5%
memory_usage: 2.5GB
request_rate: 1000 req/s
```

### 2.2 Logs

**Definition:** Discrete events with timestamps

**Characteristics:**
- **Event-based**: Individual occurrences
- **Text-based**: Human-readable format
- **Detailed**: Rich context information
- **Storage-intensive**: Can be large

**Use Cases:**
- Debugging errors
- Audit trails
- Security events
- Application behavior

**Example:**
```
2024-01-01 10:00:00 [INFO] User login successful: user_id=123
2024-01-01 10:00:01 [ERROR] Database connection failed: timeout=30s
```

### 2.3 Traces

**Definition:** Request flow through distributed systems

**Characteristics:**
- **Distributed**: Cross-service tracking
- **Hierarchical**: Parent-child relationships
- **Context propagation**: Request context
- **Performance analysis**: Latency breakdown

**Use Cases:**
- Understanding request flow
- Identifying bottlenecks
- Debugging distributed systems
- Performance optimization

**Example:**
```
Trace ID: abc123
├── Service: API Gateway (50ms)
│   ├── Service: Auth Service (20ms)
│   └── Service: User Service (30ms)
│       ├── Database Query (25ms)
│       └── Cache Lookup (5ms)
```

### 2.4 The Golden Signals

**Four Golden Signals (Google SRE):**

1. **Latency**: Time to serve a request
2. **Traffic**: Demand on the system
3. **Errors**: Rate of failed requests
4. **Saturation**: Resource utilization

**RED Method:**
- **Rate**: Requests per second
- **Errors**: Error rate
- **Duration**: Request duration

**USE Method (Infrastructure):**
- **Utilization**: Resource usage percentage
- **Saturation**: Degree of overload
- **Errors**: Error count

---

## 3. Metrics - Time-Series Data

### 3.1 Metric Types

**Counter:**
- Monotonically increasing value
- Examples: Total requests, errors count
- Operations: Increment, reset

**Gauge:**
- Value that can go up or down
- Examples: CPU usage, memory usage, queue size
- Operations: Set, increment, decrement

**Histogram:**
- Distribution of measurements
- Examples: Request duration, response size
- Operations: Observe values, calculate percentiles

**Summary:**
- Similar to histogram, but with quantiles
- Examples: Request latency percentiles
- Operations: Observe values, calculate quantiles

### 3.2 Prometheus Metrics

**Prometheus Data Model:**

```
metric_name{label1="value1",label2="value2"} value timestamp
```

**Example:**
```
http_requests_total{method="GET",status="200",endpoint="/api/users"} 1500 1609459200
http_requests_total{method="POST",status="500",endpoint="/api/users"} 5 1609459200
```

**Metric Naming:**
- Use `_total` suffix for counters
- Use `_duration_seconds` for durations
- Use `_bytes` for byte sizes
- Use `_ratio` for ratios

### 3.3 Prometheus Setup

**Installation:**

```bash
# Download Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# Start Prometheus
./prometheus --config.file=prometheus.yml
```

**Configuration (prometheus.yml):**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

rule_files:
  - '/etc/prometheus/rules/*.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'application'
    static_configs:
      - targets: ['app:8080']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### 3.4 PromQL (Prometheus Query Language)

**Basic Queries:**

```promql
# Select metric
http_requests_total

# Filter by labels
http_requests_total{status="200"}

# Multiple label filters
http_requests_total{method="GET", status="200"}

# Rate (per second)
rate(http_requests_total[5m])

# Increase over time
increase(http_requests_total[1h])

# Aggregation
sum(http_requests_total)

# Group by
sum(http_requests_total) by (status)

# Average
avg(cpu_usage)

# Percentiles
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Mathematical operations
rate(http_requests_total[5m]) * 60  # Requests per minute
```

**Advanced Queries:**

```promql
# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# CPU usage percentage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Top 10 by value
topk(10, sum(http_requests_total) by (endpoint))

# Time-based comparison
http_requests_total - http_requests_total offset 1h
```

### 3.5 Node Exporter

**Installation:**

```bash
# Download Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
cd node_exporter-1.6.1.linux-amd64

# Start Node Exporter
./node_exporter
```

**Metrics Exposed:**
- CPU metrics
- Memory metrics
- Disk I/O metrics
- Network metrics
- System load
- File system metrics

**Docker Setup:**

```yaml
version: '3.8'
services:
  node-exporter:
    image: prom/node-exporter:latest
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    ports:
      - "9100:9100"
```

---

## 4. Logs - Event Data

### 4.1 Log Levels

**Standard Log Levels:**

```
FATAL   - System is unusable
ERROR   - Error events that might still allow the app to continue
WARN    - Warning messages
INFO    - Informational messages
DEBUG   - Debug-level messages
TRACE   - Very detailed tracing information
```

### 4.2 Structured Logging

**JSON Format (Recommended):**

```json
{
  "timestamp": "2024-01-01T10:00:00Z",
  "level": "ERROR",
  "service": "user-service",
  "trace_id": "abc123",
  "message": "Database connection failed",
  "error": {
    "type": "ConnectionTimeout",
    "message": "Connection timeout after 30s"
  },
  "context": {
    "user_id": "123",
    "request_id": "req-456"
  }
}
```

**Benefits:**
- Machine-readable
- Easy to parse
- Rich context
- Queryable

### 4.3 ELK Stack Setup

**Elasticsearch:**

```bash
# Docker Compose
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data

volumes:
  es-data:
```

**Logstash Configuration:**

```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "web" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:message}" }
    }
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
  
  if [level] == "ERROR" {
    mutate {
      add_tag => [ "error", "alert" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

**Kibana Setup:**

```yaml
kibana:
  image: docker.elastic.co/kibana/kibana:8.10.0
  environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
  ports:
    - "5601:5601"
  depends_on:
    - elasticsearch
```

### 4.4 Filebeat

**Filebeat Configuration:**

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    fields:
      service: web
      environment: production
    fields_under_root: true
    multiline.pattern: '^\d{4}-\d{2}-\d{2}'
    multiline.negate: true
    multiline.match: after

output.logstash:
  hosts: ["logstash:5044"]

processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
```

### 4.5 Log Aggregation Patterns

**Centralized Logging:**

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  App 1  │  │  App 2  │  │  App 3  │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
            ┌─────▼─────┐
            │  Filebeat │
            └─────┬─────┘
                  │
            ┌─────▼─────┐
            │  Logstash │
            └─────┬─────┘
                  │
         ┌────────▼────────┐
         │  Elasticsearch  │
         └────────┬────────┘
                  │
            ┌─────▼─────┐
            │   Kibana  │
            └───────────┘
```

**Log Rotation:**

```bash
# logrotate configuration
/var/log/app/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 app app
    postrotate
        systemctl reload filebeat
    endscript
}
```

---

## 5. Traces - Distributed Tracing

### 5.1 OpenTelemetry

**OpenTelemetry Components:**

- **Tracer**: Creates spans
- **Span**: Single operation in a trace
- **Trace**: Collection of spans
- **Context**: Propagation of trace context

**Span Structure:**

```
Span {
  trace_id: "abc123"
  span_id: "def456"
  parent_span_id: "ghi789"
  name: "database_query"
  start_time: 1609459200
  end_time: 1609459201
  duration: 1s
  attributes: {
    "db.system": "postgresql",
    "db.statement": "SELECT * FROM users"
  }
  events: [...]
  status: "OK"
}
```

### 5.2 Jaeger Setup

**Jaeger Installation:**

```bash
# Docker Compose
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # HTTP collector
      - "6831:6831/udp"  # Agent
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
```

**Instrumentation Example (Python):**

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Usage
def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        
        with tracer.start_as_current_span("validate_order") as child_span:
            # Validation logic
            child_span.set_attribute("order.valid", True)
        
        with tracer.start_as_current_span("charge_payment") as child_span:
            # Payment logic
            child_span.set_attribute("payment.amount", 100.00)
```

### 5.3 Trace Context Propagation

**HTTP Headers:**

```
X-Trace-Id: abc123
X-Span-Id: def456
X-Parent-Span-Id: ghi789
```

**W3C Trace Context:**

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
tracestate: congo=t61rcWkgMzE
```

---

## 6. Prometheus & Grafana

### 6.1 Grafana Setup

**Installation:**

```bash
# Docker
docker run -d -p 3000:3000 --name=grafana grafana/grafana:latest

# Or Docker Compose
version: '3.8'
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

volumes:
  grafana-data:
```

**Prometheus Data Source:**

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

### 6.2 Grafana Dashboards

**Dashboard JSON Example:**

```json
{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "Errors"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Response Time",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

**Common Dashboard Panels:**

```promql
# Request Rate
sum(rate(http_requests_total[5m])) by (service)

# Error Rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Latency (p50, p95, p99)
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# CPU Usage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk Usage
(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes * 100
```

### 6.3 Alerting Rules

**Prometheus Alert Rules:**

```yaml
# alerts.yml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec for {{ $labels.service }}"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "p95 latency is {{ $value }}s for {{ $labels.service }}"

      - alert: HighCPUUsage
        expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}% on {{ $labels.instance }}"
```

**Alertmanager Configuration:**

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '${SLACK_WEBHOOK_URL}'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'slack-critical'
      continue: true
    - match:
        severity: warning
      receiver: 'slack-warning'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
        send_resolved: true

  - name: 'slack-warning'
    slack_configs:
      - channel: '#alerts'
        title: '⚠️ WARNING: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

---

## 7. ELK Stack (Elasticsearch, Logstash, Kibana)

### 7.1 Complete ELK Setup

**Docker Compose:**

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5044:5044"
      - "9600:9600"
    depends_on:
      - elasticsearch
    networks:
      - elk

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - elk

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.10.0
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    depends_on:
      - logstash
    networks:
      - elk

volumes:
  es-data:

networks:
  elk:
    driver: bridge
```

### 7.2 Logstash Pipeline

**Complete Pipeline:**

```ruby
# logstash/pipeline/main.conf
input {
  beats {
    port => 5044
  }
  
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
    }
  }
  
  # Parse common log formats
  if [fields][log_type] == "nginx" {
    grok {
      match => {
        "message" => "%{NGINXACCESS}"
      }
    }
  }
  
  if [fields][log_type] == "apache" {
    grok {
      match => {
        "message" => "%{COMBINEDAPACHELOG}"
      }
    }
  }
  
  # Parse application logs
  if [fields][service] {
    grok {
      match => {
        "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:log_message}"
      }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
  }
  
  # Add geoip for IP addresses
  if [clientip] {
    geoip {
      source => "clientip"
      target => "geoip"
    }
  }
  
  # Parse user agent
  if [user_agent] {
    useragent {
      source => "user_agent"
      target => "ua"
    }
  }
  
  # Tag errors
  if [level] == "ERROR" or [level] == "FATAL" {
    mutate {
      add_tag => [ "error", "alert" ]
    }
  }
  
  # Remove sensitive data
  mutate {
    remove_field => [ "password", "token", "api_key" ]
  }
}

output {
  if "error" in [tags] {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "logs-error-%{+YYYY.MM.dd}"
    }
  } else {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "logs-%{+YYYY.MM.dd}"
    }
  }
  
  # Debug output (remove in production)
  stdout {
    codec => rubydebug
  }
}
```

### 7.3 Kibana Dashboards

**Creating Dashboards:**

1. **Discover View:**
   - Search logs
   - Filter by fields
   - Time range selection

2. **Visualizations:**
   - Line charts
   - Bar charts
   - Pie charts
   - Maps

3. **Dashboard:**
   - Combine visualizations
   - Share dashboards
   - Export/import

**Kibana Query Language (KQL):**

```
# Simple search
status: 200

# Multiple conditions
status: 200 AND method: GET

# Range queries
response_time > 1000

# Field exists
user_id: *

# Wildcards
message: *error*

# Not
NOT status: 200
```

---

## 8. Jaeger & Distributed Tracing

### 8.1 Jaeger Architecture

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  App 1  │  │  App 2  │  │  App 3  │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
            ┌─────▼─────┐
            │   Agent   │
            └─────┬─────┘
                  │
            ┌─────▼─────┐
            │ Collector │
            └─────┬─────┘
                  │
         ┌────────▼────────┐
         │     Storage     │
         └────────┬────────┘
                  │
            ┌─────▼─────┐
            │   Query   │
            └─────┬─────┘
                  │
            ┌─────▼─────┐
            │    UI     │
            └───────────┘
```

### 8.2 Instrumentation Examples

**Python (Flask):**

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument Flask
FlaskInstrumentor().instrument_app(app)
```

**Node.js:**

```javascript
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');

const provider = new NodeTracerProvider();
const exporter = new JaegerExporter({
  endpoint: 'http://jaeger:14268/api/traces',
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();
```

**Java (Spring Boot):**

```java
// pom.xml
<dependency>
    <groupId>io.jaegertracing</groupId>
    <artifactId>jaeger-client</artifactId>
    <version>1.8.1</version>
</dependency>

// Application.java
@Bean
public Tracer jaegerTracer() {
    return new Configuration("my-service")
        .withSampler(new SamplerConfiguration().withType("const").withParam(1))
        .withReporter(new ReporterConfiguration()
            .withSender(new SenderConfiguration()
                .withEndpoint("http://jaeger:14268/api/traces")))
        .getTracer();
}
```

---

## 9. Cloud-Native Monitoring

### 9.1 Kubernetes Monitoring

**Prometheus Operator:**

```yaml
# prometheus-operator setup
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

**cAdvisor:**

```bash
# cAdvisor exposes container metrics
# Accessible at: http://node-ip:4194/metrics
```

**kube-state-metrics:**

```bash
# Exposes Kubernetes object metrics
# Deployment status, pod status, etc.
```

### 9.2 Cloud Provider Monitoring

**AWS CloudWatch:**

```bash
# Send custom metrics
aws cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name RequestCount \
  --value 100 \
  --timestamp $(date -u +"%Y-%m-%dT%H:%M:%S")
```

**Google Cloud Monitoring:**

```python
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/{project_id}"

series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/my_metric"
series.resource.type = "global"
point = monitoring_v3.Point()
point.value.double_value = 100.0
point.interval.end_time.seconds = int(time.time())
series.points = [point]

client.create_time_series(name=project_name, time_series=[series])
```

**Azure Monitor:**

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(
    connection_string="InstrumentationKey=xxx"
)

tracer = trace.get_tracer(__name__)
```

---

## 10. Application Performance Monitoring (APM)

### 10.1 APM Tools

**New Relic:**

```python
# Python
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

# Instrument application
@newrelic.agent.function_trace()
def my_function():
    pass
```

**Datadog APM:**

```python
# Python
from ddtrace import patch_all
patch_all()

# Automatic instrumentation
# Or manual
from ddtrace import tracer

@tracer.wrap()
def my_function():
    pass
```

**Elastic APM:**

```python
# Python
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
apm = ElasticAPM(app, service_name='my-service')
```

### 10.2 APM Metrics

**Key APM Metrics:**

- **Throughput**: Requests per second
- **Response Time**: Average, p50, p95, p99
- **Error Rate**: Percentage of failed requests
- **Apdex Score**: Application performance index
- **Database Query Time**: Slow query detection
- **External API Calls**: Third-party service latency

---

## 11. Infrastructure Monitoring

### 11.1 System Metrics

**CPU Monitoring:**

```promql
# CPU usage percentage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# CPU by core
100 - (rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100)

# Load average
node_load1
node_load5
node_load15
```

**Memory Monitoring:**

```promql
# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Memory by type
node_memory_MemTotal_bytes
node_memory_MemFree_bytes
node_memory_MemAvailable_bytes
node_memory_Buffers_bytes
node_memory_Cached_bytes
```

**Disk Monitoring:**

```promql
# Disk usage
(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes * 100

# Disk I/O
rate(node_disk_read_bytes_total[5m])
rate(node_disk_written_bytes_total[5m])
rate(node_disk_io_time_seconds_total[5m])
```

**Network Monitoring:**

```promql
# Network traffic
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])

# Network errors
rate(node_network_receive_errs_total[5m])
rate(node_network_transmit_errs_total[5m])
```

### 11.2 Container Monitoring

**Docker Metrics:**

```bash
# Docker stats
docker stats

# cAdvisor metrics
curl http://localhost:8080/metrics
```

**Kubernetes Metrics:**

```promql
# Pod CPU
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)

# Pod Memory
sum(container_memory_usage_bytes) by (pod)

# Pod Restarts
kube_pod_container_status_restarts_total
```

---

## 12. Alerting Strategies

### 12.1 Alert Design Principles

**Alert Fatigue Prevention:**

1. **Only alert on actionable items**
2. **Use appropriate severity levels**
3. **Group related alerts**
4. **Set proper thresholds**
5. **Use alert dependencies**

**Alert Severity Levels:**

- **Critical**: Immediate action required, service down
- **Warning**: Attention needed, but service functional
- **Info**: Informational, no action required

### 12.2 Alert Rules Best Practices

**Good Alert Example:**

```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate on {{ $labels.service }}"
    description: "Error rate is {{ $value }} errors/sec (threshold: 0.05)"
    runbook_url: "https://wiki.example.com/runbooks/high-error-rate"
```

**Bad Alert Example:**

```yaml
# ❌ Too sensitive
- alert: AnyError
  expr: http_requests_total{status=~"5.."} > 0

# ❌ No context
- alert: Problem
  expr: some_metric > 100
```

### 12.3 Alert Routing

**Alertmanager Routing:**

```yaml
route:
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'oncall-pagerduty'
    - match:
        severity: warning
        team: backend
      receiver: 'backend-slack'
    - match:
        severity: warning
        team: frontend
      receiver: 'frontend-slack'
```

---

## 13. SLO, SLA, SLI

### 13.1 Definitions

**SLI (Service Level Indicator):**
- Metric that measures service quality
- Example: Request success rate, latency

**SLO (Service Level Objective):**
- Target value for SLI
- Example: 99.9% uptime, p95 latency < 200ms

**SLA (Service Level Agreement):**
- Contract with consequences
- Example: 99.9% uptime or refund

### 13.2 SLO Implementation

**Error Budget:**

```
Error Budget = 100% - SLO
Example: SLO = 99.9%, Error Budget = 0.1%
```

**SLO Monitoring:**

```promql
# Availability SLO
sum(rate(http_requests_total{status=~"2.."}[5m])) / 
sum(rate(http_requests_total[5m])) >= 0.999

# Latency SLO
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) < 0.2
```

**SLO Dashboard:**

```yaml
# Grafana SLO panel
- title: "Availability SLO"
  targets:
    - expr: |
        (
          sum(rate(http_requests_total{status=~"2.."}[30d])) /
          sum(rate(http_requests_total[30d]))
        ) * 100
      legendFormat: "Availability %"
```

---

## 14. Real-Time Monitoring

### 14.1 Real-Time Dashboards

**Grafana Real-Time:**

```json
{
  "refresh": "5s",
  "time": {
    "from": "now-5m",
    "to": "now"
  }
}
```

**Kibana Real-Time:**

- Auto-refresh: 5 seconds
- Live tail: Stream logs in real-time

### 14.2 Streaming Metrics

**Prometheus Streaming:**

```promql
# Real-time query
rate(http_requests_total[1m])
```

**StatsD:**

```python
from statsd import StatsClient

statsd = StatsClient(host='statsd', port=8125)

# Increment counter
statsd.incr('requests.count')

# Gauge
statsd.gauge('users.active', 100)

# Timer
with statsd.timer('request.duration'):
    process_request()
```

---

## 15. Best Practices & Patterns

### 15.1 Monitoring Best Practices

1. **Monitor the Right Things**
   - Golden signals (latency, traffic, errors, saturation)
   - Business metrics
   - User experience metrics

2. **Set Appropriate Thresholds**
   - Based on historical data
   - Account for normal variations
   - Review and adjust regularly

3. **Use Labels/Tags Effectively**
   - Consistent naming
   - Don't over-label (cardinality)
   - Use high-cardinality labels sparingly

4. **Retention Policies**
   - Hot data: Recent (7-30 days)
   - Warm data: Older (30-90 days)
   - Cold data: Archived (90+ days)

5. **Dashboard Design**
   - Most important metrics at top
   - Group related metrics
   - Use appropriate visualizations
   - Keep dashboards focused

### 15.2 Logging Best Practices

1. **Structured Logging**
   - Use JSON format
   - Include context (trace_id, user_id)
   - Consistent field names

2. **Log Levels**
   - ERROR: Action required
   - WARN: Attention needed
   - INFO: Important events
   - DEBUG: Development only

3. **Log Rotation**
   - Rotate daily
   - Compress old logs
   - Retain for compliance period

4. **Sensitive Data**
   - Never log passwords, tokens
   - Mask PII (personally identifiable information)
   - Use log filtering

### 15.3 Tracing Best Practices

1. **Sampling**
   - 100% for errors
   - 1-10% for normal traffic
   - Adjust based on volume

2. **Span Naming**
   - Use operation names: `GET /api/users`
   - Include service name
   - Be descriptive

3. **Context Propagation**
   - Propagate trace context
   - Include in all service calls
   - Use W3C Trace Context standard

### 15.4 Alerting Best Practices

1. **Alert Rules**
   - Alert on symptoms, not causes
   - Use multi-window alerts
   - Include runbook links

2. **Alert Grouping**
   - Group related alerts
   - Use alert dependencies
   - Prevent alert storms

3. **On-Call Rotation**
   - Clear escalation paths
   - Document runbooks
   - Post-incident reviews

### 15.5 Monitoring Architecture Patterns

**Centralized Monitoring:**

```
All Services → Central Monitoring Stack
```

**Federated Monitoring:**

```
Services → Regional Monitoring → Central Aggregation
```

**Hybrid Approach:**

```
Critical Services → Central
Non-Critical → Regional
```

---

## Conclusion

### Key Takeaways:

1. **Three Pillars**: Metrics, Logs, Traces provide complete observability
2. **Golden Signals**: Monitor latency, traffic, errors, saturation
3. **Right Tools**: Choose tools that fit your stack
4. **Automation**: Automate monitoring and alerting
5. **SLOs**: Define and monitor service level objectives
6. **Continuous Improvement**: Regularly review and optimize

### Essential Tools:

- **Metrics**: Prometheus, Grafana
- **Logs**: ELK Stack, Loki
- **Traces**: Jaeger, Zipkin
- **APM**: New Relic, Datadog, Elastic APM
- **Alerting**: Alertmanager, PagerDuty

### Next Steps:

1. Set up monitoring stack
2. Instrument applications
3. Create dashboards
4. Configure alerting
5. Define SLOs
6. Establish on-call procedures

---

*Monitoring & Observability in DevOps - Master Guide*
*Complete Guide to Metrics, Logs, Traces, and Alerting*
*Last Updated: 2024*

