# 03 - Topics, Partitions, Replication

## Topic design
- Model events, not requests.
- Prefer stable topic names that represent a domain.
- Keep schemas backward compatible.

## Partitioning strategy
- More partitions = more parallelism, higher overhead.
- Partition key controls ordering. Use keys that match consumer logic.
- Avoid hotspots (skewed keys).

## Replication and ISR
- Replication factor (RF) controls durability.
- `min.insync.replicas` defines how many replicas must acknowledge a write.
- Use `acks=all` on producers for strong durability.

## Retention and compaction
- `delete`: remove old data by time/size.
- `compact`: keep the latest value per key.
- Combine with `compact,delete` for hybrid behavior.

## CLI examples
```bash
# Create a topic with RF=3
kafka-topics --create --topic payments --bootstrap-server localhost:9092 --partitions 6 --replication-factor 3

# Describe a topic
kafka-topics --describe --topic payments --bootstrap-server localhost:9092

# Add partitions (cannot reduce)
kafka-topics --alter --topic payments --bootstrap-server localhost:9092 --partitions 12

# Change retention
kafka-configs --alter --entity-type topics --entity-name payments \
  --add-config retention.ms=86400000 --bootstrap-server localhost:9092
```

## Best practices
- RF=3 for production.
- `min.insync.replicas=2` with `acks=all`.
- Keep partitions per broker under operational limits (monitor disk and CPU).
- Avoid frequently changing partition counts for keyed topics.

## Exercises
1. Choose a partition key for an orders topic and justify it.
2. Explain why increasing partitions can break ordering guarantees.

Next: `04-cluster-ops/README.md`
