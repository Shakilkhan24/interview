# 13 - Disaster Recovery and Backup

## Philosophy
Kafka is not a database backup. DR is usually implemented by cross-cluster replication and IaC for cluster rebuild.

## Options
- MirrorMaker 2: open source replication between clusters
- Cluster Linking (Confluent): managed, low-latency replication
- Tiered storage (if supported) for long-term retention

## MirrorMaker 2 overview
- Runs as Kafka Connect on both clusters
- Replicates topics, consumer groups, and offsets
- Supports active-passive or active-active patterns

## Operational steps
1. Provision a second cluster in another region.
2. Replicate critical topics with MM2.
3. Validate replication lag and data integrity.
4. Test failover with clients pointed at DR.

## Backup of configuration
- Store broker configs in Git.
- Store topic configs and ACLs as code.
- Export metadata regularly.

## DR drills
- Simulate region outage.
- Measure RPO and RTO.
- Verify consumer catch-up behavior.

Next: `14-capstone/README.md`
