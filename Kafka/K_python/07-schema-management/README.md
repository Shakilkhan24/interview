# 07 - Schema Management

## Why schemas matter
- Prevent breaking changes across teams
- Enable evolution with clear compatibility rules
- Improve data quality and observability

## Common formats
- Avro: compact, schema-first, strong compatibility
- Protobuf: compact, language friendly
- JSON Schema: flexible, readable

## Schema Registry concepts
- Schema is stored and versioned centrally
- Producers register schemas
- Consumers validate and deserialize

## Compatibility modes
- Backward: new consumers can read old data
- Forward: old consumers can read new data
- Full: both directions

## Example: Avro with Schema Registry (Python)
```python
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import json

schema_str = """
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "status", "type": "string"}
  ]
}
"""

sr_conf = {"url": "http://localhost:8081"}
sr_client = SchemaRegistryClient(sr_conf)
serializer = AvroSerializer(sr_client, schema_str)

p = Producer({"bootstrap.servers": "localhost:9092"})

order = {"order_id": "123", "status": "created"}
value = serializer(order, None)

p.produce("orders-avro", value=value)
p.flush(5)
```

## Operational tips
- Enforce compatibility at the registry level.
- Version topics and schemas carefully.
- Document required and optional fields.

Next: `08-security/README.md`
