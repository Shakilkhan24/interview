# 04 - Cluster Operations

## Broker configuration categories
- Storage: log dirs, retention, segment sizes
- Replication: ISR, leader election
- Network: listeners, security protocols
- Performance: threads, socket buffers, fetch/produce limits

## KRaft basics
- Controllers store metadata inside Kafka.
- Use an odd number of controllers (3 or 5).
- Separate controller and broker roles for larger clusters.

## Scaling brokers
1. Add new broker with matching configs.
2. Reassign partitions to spread load.
3. Verify replicas are in sync.

### Partition reassignment
```bash
# Generate reassignment plan
kafka-reassign-partitions --bootstrap-server localhost:9092 --generate --topics-to-move-json-file topics.json --broker-list 1,2,3

# Execute plan
kafka-reassign-partitions --bootstrap-server localhost:9092 --execute --reassignment-json-file reassignment.json

# Verify
kafka-reassign-partitions --bootstrap-server localhost:9092 --verify --reassignment-json-file reassignment.json
```

## Rolling upgrade (high level)
1. Check cluster health and ISR.
2. Upgrade brokers one at a time.
3. Prefer `unclean.leader.election.enable=false`.
4. Verify leader balance after upgrade.

## Disk management
- Monitor disk usage per log dir.
- Use multiple log dirs for larger brokers.
- Avoid low disk thresholds (performance degrades).

## Runbook checks
- Under-replicated partitions count
- Offline partitions count
- Controller health
- Disk usage per broker
- Consumer lag

Next: `05-python-producers-consumers/README.md`
