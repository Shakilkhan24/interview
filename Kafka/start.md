নিচে **Kafka-এর একদম end-to-end, প্রো-লেভেল টিউটোরিয়াল (Bangla)** দিলাম—এটা “ইন্টারঅ্যাকটিভ” রাখার জন্য আমি প্রতিটি সেকশনের শেষে **চেকপয়েন্ট টাস্ক + কুইজ + ছোট ল্যাব** দিয়েছি, যাতে তুমি নিজে হাতে করে শিখতে পারো। (তুমি চাইলে পরে বললেই আমি এটাকে “একটা Repo-র README স্টাইল”েও সাজিয়ে দেবো।)

---

## 0) Kafka আসলে কী এবং কেন লাগে?

Kafka হলো **distributed event streaming platform**। সহজ ভাষায়:

* তোমার সিস্টেমে যা কিছু ঘটে (order created, payment done, user clicked, logs, metrics…) এগুলো **event/message**।
* Kafka এসব event কে **durable + ordered + scalable** ভাবে store করে এবং বহু সার্ভিসকে **real-time** এ deliver করে।

### কোথায় ব্যবহার হয়?

* Microservices event-driven communication
* Log aggregation / metrics pipeline
* CDC (database change data capture)
* Real-time analytics (Flink/Spark/ksqlDB)
* Notification, fraud detection, recommendation pipelines

✅ **Kafka-এর মূল শক্তি**: throughput বেশি, scale সহজ, replay করা যায়, consumer group দিয়ে parallel processing।

**চেকপয়েন্ট টাস্ক:**
তোমার নিজের একটা বাস্তব উদাহরণ লেখো: “RUET portal এ কেউ login করলে event যাবে…”—এই ধরনের ৩টা event আইডিয়া লিখো।

---

## 1) Kafka Core Concepts (সবচেয়ে জরুরি বেসিক)

### 1.1 Topic

Kafka-তে message যায় **Topic** এ।
Topic কে ভাবতে পারো “stream/channel”।

### 1.2 Partition

একটা Topic-এর ভেতরে অনেক **partition** থাকতে পারে।

* partition হলো **parallelism + ordering boundary**
* **একটা partition-এর মধ্যে order guarantee থাকে** (যেমন offset 0,1,2…)

### 1.3 Offset

Partition-এর ভেতরে message-এর সিরিয়াল নম্বর = **offset**।
Consumer offset track করে বলে সে কোথায় পর্যন্ত পড়েছে।

### 1.4 Producer / Consumer

* Producer: message publish করে
* Consumer: message পড়ে

### 1.5 Consumer Group

একই group-এর ভেতরে multiple consumer থাকলে:

* partitions ভাগ হয়ে যায়
* একই message **group-এর মধ্যে একবারই process হয়** (প্রতি partition per consumer)

### 1.6 Broker / Cluster

Kafka server = broker। একাধিক broker মিলে cluster।

### 1.7 Replication

partition-এর replica থাকে (fault tolerance)

* leader replica: read/write হয়
* follower replica: copy রাখে

**কুইজ (দ্রুত):**

1. ordering কোথায় guarantee?
2. consumer group কেন দরকার?
3. offset কে track করে?

---

## 2) Kafka Architecture (Modern Kafka: KRaft)

আগে Kafka metadata রাখত **ZooKeeper** এ। এখন আধুনিক Kafka-তে থাকে **KRaft (Kafka Raft)**—Kafka নিজেই metadata manage করে।

**High-level flow**
Producer → broker leader partition → replicate to followers → ack → consumer reads

---

## 3) Hands-on Lab: Docker দিয়ে Kafka চালানো (KRaft mode)

### 3.1 docker-compose.yml

একটা ফোল্ডার বানাও `kafka-lab/` এবং ভেতরে `docker-compose.yml`:

```yaml
services:
  kafka:
    image: apache/kafka:3.8.0
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
```

Run:

```bash
docker compose up -d
docker ps
```

### 3.2 Topic বানানো / দেখা

```bash
docker exec -it kafka bash

# topic create
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic orders --partitions 3 --replication-factor 1

# list topics
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# describe
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic orders
```

### 3.3 Producer/Consumer টেস্ট

**Producer:**

```bash
/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
```

এখন কয়েকটা লাইন লিখো:

```
order-1 created
order-2 created
```

**Consumer:**
নতুন টার্মিনাল:

```bash
docker exec -it kafka bash
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic orders --from-beginning
```

✅ **চেকপয়েন্ট:** তুমি কি consumer-এ message দেখছো?
না দেখলে বলো—আমি ডিবাগিং স্টেপ দেবো (advertised listeners, ports ইত্যাদি)।

---

## 4) Partitioning & Keying (সঠিক ডিজাইন)

### Key না দিলে কী হয়?

Producer সাধারণত partitions এ round-robin করে।

### Key দিলে কী হয়?

একই key → **সবসময় একই partition** (default partitioner), ফলে **per-key ordering** পাওয়া যায়।

**উদাহরণ**: `user_id` key দিলে একই user-এর সব event order এ থাকবে।

**Design rule of thumb**

* Ordering দরকার? → key ব্যবহার করো
* High throughput? → partitions বাড়াও (কিন্তু consumer parallelism ও লাগবে)

**কুইজ:**
“order_id key দিলে কী সুবিধা?”

---

## 5) Delivery Semantics: at-most-once / at-least-once / exactly-once

### at-most-once

দ্রুত, কিন্তু message হারাতে পারে (rarely used)

### at-least-once (সবচেয়ে common)

message duplicate হতে পারে → consumer must be idempotent

### exactly-once (EOS)

Kafka transactions + idempotent producer + properly configured consumer
এটা বেশি complex কিন্তু financial/critical pipelines এ দরকার।

**ইন্টারভিউ টিপ:**
“Exactly-once মানে end-to-end exactly once, শুধু Kafka broker-level না—consumer side state/store ও matter করে।”

---

## 6) Producer Tuning (Performance + Safety)

Producer-এর গুরুত্বপূর্ণ config:

* `acks=all` (durability বেশি)
* `enable.idempotence=true` (duplicate reduce)
* `retries` + `delivery.timeout.ms`
* `linger.ms` (batching)
* `batch.size`
* `compression.type` (lz4/zstd)

**Rule**

* throughput চাইলে: batching + compression + linger একটু বাড়াও
* durability চাইলে: `acks=all` + min.insync.replicas ঠিক করো

---

## 7) Consumer Deep Dive (Offsets, Rebalance, Commit)

### Offset commit

* auto commit: সহজ, কিন্তু crash হলে duplicate/miss হতে পারে
* manual commit: control বেশি

**Golden pattern (at-least-once)**

1. poll
2. process
3. commit

### Rebalance problem

Consumer group এ consumer যোগ/বাদ হলে partition assignment বদলায় → rebalance।
Heavy rebalance মানে throughput drop।

**Mitigation**

* cooperative-sticky assignor
* session/poll timeout ঠিক করা
* long processing হলে pause/resume বা separate worker pool

---

## 8) Message Schema & Evolution (Pro-level)

Text/JSON দিয়ে শুরু করা যায়, কিন্তু production এ:

* Avro / Protobuf + Schema Registry (Confluent বা Apicurio)
* schema evolution rules: backward/forward compatibility

**কেন দরকার?**
Microservices এ producer/consumer আলাদা করে deploy হয়—schema break হলে outage।

---

## 9) Kafka Connect (No-code-ish Integration)

Kafka Connect দিয়ে:

* DB → Kafka (source connector)
* Kafka → Elasticsearch/S3/DB (sink connector)

Use-case:
Postgres CDC → Kafka → analytics / search

---

## 10) Streams Processing

### Kafka Streams

Java library—stateful stream processing (windowing, joins, aggregations)

### Alternatives

* Flink
* Spark Structured Streaming
* ksqlDB (SQL-like)

---

## 11) Security (Production must-have)

* TLS encryption (in-transit)
* SASL auth (SCRAM/OAuth/Kerberos)
* ACL authorization
* Network policies (K8s)
* Secrets management (Vault/KMS)

---

## 12) Observability & Operations

### Key metrics to watch

* Consumer lag (সবচেয়ে গুরুত্বপূর্ণ)
* Under-replicated partitions
* ISR shrink
* Request latency
* Disk usage (log retention impact)

### Retention

* time-based: `retention.ms`
* size-based: `retention.bytes`
* compaction (special): `cleanup.policy=compact` (latest value per key)

**Use-case:** user profile updates → compacted topic.

---

## 13) Troubleshooting Playbook (বাস্তব সমস্যা)

### Symptom: Consumer lag বাড়ছে

Check:

1. consumer processing slow?
2. partitions কম? → parallelism বাড়াও
3. rebalance storm?
4. broker throttling / IO bottleneck?

### Symptom: Duplicate messages

* at-least-once expected
* idempotent processing / dedupe by key + offset store

### Symptom: “Not leader for partition”

* leader election/replica sync issues
* broker health, ISR, network

---

## 14) Mini Project (Interactive Capstone)

### Project: “Order Pipeline”

**Goal**:
`orders` topic এ order events যাবে → `billing` service consume করবে → success/fail event `payments` topic এ publish করবে → `notifications` consume করবে।

**Tasks**

1. `orders` (3 partitions) topic বানাও
2. `payments` (3 partitions) topic বানাও
3. producer দিয়ে order events publish করো (key=order_id)
4. consumer group দিয়ে parallel consume টেস্ট করো
5. lag observe করো (simple CLI বা tool)

---

## 15) Optional: Python দিয়ে Producer/Consumer (তোমার জন্য useful)

Install:

```bash
pip install confluent-kafka
```

**Producer (producer.py)**

```python
from confluent_kafka import Producer
import json, time

p = Producer({"bootstrap.servers": "localhost:9092"})

def delivery_report(err, msg):
    if err is not None:
        print("Delivery failed:", err)
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")

for i in range(1, 6):
    event = {"order_id": f"o-{i}", "status": "created", "ts": int(time.time())}
    key = event["order_id"]
    p.produce("orders", key=key, value=json.dumps(event), callback=delivery_report)
    p.poll(0)

p.flush()
```

**Consumer (consumer.py)**

```python
from confluent_kafka import Consumer

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "billing-svc",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True
})

c.subscribe(["orders"])
try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue
        print("Got:", msg.key().decode() if msg.key() else None, msg.value().decode())
finally:
    c.close()
```

Run:

```bash
python producer.py
python consumer.py
```

---

# এখন তোমার “ইন্টারঅ্যাকটিভ” শেখার প্ল্যান (৭ দিন)

**Day 1:** Concepts + CLI lab (topic, partitions, producer/consumer)
**Day 2:** Keying + consumer groups + rebalance basics
**Day 3:** Offsets/commit + delivery semantics
**Day 4:** Producer/consumer tuning + lag debugging
**Day 5:** Schema + registry concept + evolution rules
**Day 6:** Connect + CDC overview
**Day 7:** Mini project + troubleshooting drills

---

## তোমার জন্য ৫টা দ্রুত প্রশ্ন (উত্তর দিলে আমি পরের লেভেলে আপগ্রেড করে দেবো)

1. `orders` topic এ 6 partitions হলে consumer group এ 4 consumer দিলে কী হবে?
2. Ordering দরকার “per user” — key কী দেবে?
3. At-least-once এ duplicate এড়াতে consumer-এ কী strategy নেবে?
4. Compacted topic কোথায় useful?
5. Consumer lag বাড়লে প্রথম ৩টা check কী?

তুমি এগুলোর উত্তর দাও—আমি এরপর **Kubernetes-এ Kafka deployment (Strimzi) + production hardening** সহ advanced অংশটা Bangla-তে করে দেবো।
