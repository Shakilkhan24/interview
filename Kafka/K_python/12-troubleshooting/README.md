# 12 - Troubleshooting

## Incident checklist
- Confirm cluster health (URP, offline partitions).
- Check broker logs for errors.
- Verify disk space and network latency.
- Check consumer lag and rebalance events.

## Common issues and actions

### Under-replicated partitions (URP)
- Check which brokers are out of sync.
- Verify broker health and disk IO.
- If a broker is down, restore it or reassign.

### Offline partitions
- Ensure leader broker is running.
- Avoid unclean leader election unless data loss is acceptable.

### High producer latency
- Check broker CPU and disk.
- Increase `linger.ms` and `batch.size` if CPU bound.
- Validate network MTU and TLS overhead.

### Consumer lag growing
- Increase consumer instances or partitions.
- Optimize processing time.
- Confirm `max.poll.interval.ms` is not exceeded.

### Rebalance storms
- Stabilize consumer group (session and heartbeat settings).
- Avoid long processing without `poll`.

## CLI commands
```bash
# Cluster metadata
kafka-topics --describe --bootstrap-server localhost:9092

# Consumer group lag
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group orders-service
```

## Post-incident review
- Document root cause and metrics timeline.
- Add or refine alerts.
- Create a rollback or mitigation plan.

Next: `13-dr-backup/README.md`
