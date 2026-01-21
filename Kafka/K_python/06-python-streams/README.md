# 06 - Stream Processing with Python

Kafka's native stream processing library is Kafka Streams (Java). In Python, the common pattern is a consume-transform-produce loop, or using a framework like Faust (if your org uses it). This module focuses on a reliable Python pattern.

## Stateless transform example
```python
from confluent_kafka import Consumer, Producer
import json

consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "enricher",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
producer_conf = {
    "bootstrap.servers": "localhost:9092",
    "enable.idempotence": True,
    "acks": "all",
}

c = Consumer(consumer_conf)
p = Producer(producer_conf)

c.subscribe(["raw-events"])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue

        event = json.loads(msg.value())
        event["enriched"] = True

        p.produce("enriched-events", key=msg.key(), value=json.dumps(event))
        p.flush(5)
        c.commit(msg)
finally:
    c.close()
```

## Exactly-once (conceptual)
- Python can use Kafka transactions via `confluent-kafka`.
- EOS requires broker support and careful configuration.
- For complex stateful processing, consider Kafka Streams, ksqlDB, or Flink.

## Windowing and state
- Use a local state store only if it is safe to rebuild.
- For critical state, store in an external DB or use Kafka Streams.

## DevOps notes
- Measure processing time and consumer lag.
- Keep processing idempotent where possible.
- Use separate topics for retries and dead-letter.

Next: `07-schema-management/README.md`
