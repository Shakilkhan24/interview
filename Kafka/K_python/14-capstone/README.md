# 14 - Capstone: End-to-End Pipeline

Goal: Build a small pipeline that ingests web access logs, enriches them, and stores results.

## Architecture
1. Log shipper (Python producer) reads a file and produces to `web-logs-raw`.
2. Enricher (Python consumer-producer) parses and enriches to `web-logs-enriched`.
3. Sink consumer writes enriched data to a JSONL file.

## Topics
```bash
kafka-topics --create --topic web-logs-raw --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
kafka-topics --create --topic web-logs-enriched --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

## Sample log line
```
10.0.0.1 - - [10/Oct/2024:13:55:36 +0000] "GET /api/orders/123 HTTP/1.1" 200 512
```

## Producer: shipper
```python
from confluent_kafka import Producer
import time

p = Producer({"bootstrap.servers": "localhost:9092"})

with open("access.log", "r") as f:
    for line in f:
        p.produce("web-logs-raw", value=line.strip())
        p.poll(0)
        time.sleep(0.05)

p.flush(10)
```

## Enricher: consume, parse, produce
```python
from confluent_kafka import Consumer, Producer
import json
import re

line_re = re.compile(r"(?P<ip>\S+) .* \"(?P<method>\S+) (?P<path>\S+) .*\" (?P<status>\d+)")

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "enricher",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

p = Producer({"bootstrap.servers": "localhost:9092", "enable.idempotence": True, "acks": "all"})

c.subscribe(["web-logs-raw"])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue

        line = msg.value().decode("utf-8")
        m = line_re.search(line)
        if not m:
            # send to dead-letter in real systems
            c.commit(msg)
            continue

        event = m.groupdict()
        event["service"] = "orders-api"

        p.produce("web-logs-enriched", value=json.dumps(event))
        p.flush(5)
        c.commit(msg)
finally:
    c.close()
```

## Sink: write JSONL
```python
from confluent_kafka import Consumer
import json

c = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "sink",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
})

c.subscribe(["web-logs-enriched"])

with open("enriched.jsonl", "a") as out:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        out.write(msg.value().decode("utf-8") + "\n")
        out.flush()
```

## DevOps tasks to practice
- Add `acks=all` and `min.insync.replicas`.
- Add a dead-letter topic and retry policy.
- Add monitoring for lag and throughput.
- Make scripts systemd services or Kubernetes deployments.

You now have a complete, runnable pipeline using Kafka and Python.
