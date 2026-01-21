# 01 - Foundations

## Architecture basics
- Broker: Kafka server process
- Cluster: multiple brokers working together
- Controller: manages partition leadership and metadata
- Log segments: files on disk for each partition

## Partitioning and ordering
- Ordering is guaranteed within a partition, not across a topic.
- Keyed messages go to the same partition if the key is consistent.
- Partition count impacts parallelism and throughput.

## Replication and durability
- Each partition has a leader and followers.
- Producers write to the leader; followers replicate.
- ISR (in-sync replicas) is the set of replicas fully caught up.
- `min.insync.replicas` + `acks=all` = strong durability.

## Delivery semantics
- At-most-once: may lose messages but no duplicates
- At-least-once: no loss, possible duplicates
- Exactly-once: requires idempotent producer and transactional processing

## Broker storage model
- Append-only log with segment files
- Retention by time or size
- Optional compaction for key-based state

## KRaft vs ZooKeeper
- Kafka 3.x uses KRaft for metadata (no ZooKeeper)
- KRaft simplifies ops and reduces moving parts
- ZooKeeper mode is legacy and still common in older clusters

## Common configuration flags (conceptual)
- `num.partitions`: default partitions for new topics
- `log.retention.hours`: how long to keep data
- `log.cleanup.policy`: delete or compact
- `default.replication.factor`: default replication

## Exercises
1. Explain why increasing partitions can change ordering guarantees.
2. Describe how `acks=all` and `min.insync.replicas` work together.
3. Compare retention delete vs compaction.

Next: `02-local-setup/README.md`
