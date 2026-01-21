# 05 - Python Producers and Consumers

## Python client options
- `confluent-kafka` (recommended): high performance, backed by librdkafka
- `kafka-python`: pure Python, easier to install, lower throughput

## Install
```bash
pip install confluent-kafka
```

## Producer example (idempotent, strong durability)
```python
from confluent_kafka import Producer
import json
import time

conf = {
    "bootstrap.servers": "localhost:9092",
    "enable.idempotence": True,
    "acks": "all",
    "retries": 5,
    "linger.ms": 10,
    "batch.size": 32768,
}

p = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()}[{msg.partition()}]@{msg.offset()}")

for i in range(10):
    value = {"order_id": i, "status": "created"}
    p.produce(
        "orders",
        key=str(i),
        value=json.dumps(value),
        on_delivery=delivery_report,
    )
    p.poll(0)

p.flush(10)
```

## Consumer example (manual commit)
```python
from confluent_kafka import Consumer
import json

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "orders-service",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}

c = Consumer(conf)
c.subscribe(["orders"])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        data = json.loads(msg.value())
        print("got", data)

        # Commit after successful processing
        c.commit(msg)
finally:
    c.close()
```

## Key operational patterns
- Use idempotent producers for retries without duplicates.
- Prefer manual commit for at-least-once processing.
- Use a dead-letter topic for poison messages.
- Implement graceful shutdown and flush.

## Troubleshooting tips
- If consumers lag, check processing time and partitions.
- If producers time out, check broker load and `buffer.memory`.

Next: `06-python-streams/README.md`
