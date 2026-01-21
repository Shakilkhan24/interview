# 00 - Overview

## What Kafka is
Kafka is a distributed commit log used to move and store event data at high throughput. Producers write events to topics, and consumers read those events independently. Kafka keeps data for a configurable time, so consumers can rewind or replay.

## Common use cases
- Event-driven microservices
- Log aggregation and analytics pipelines
- CDC (change data capture)
- Real-time monitoring and alerting
- Data integration between systems

## Where Kafka fits in a DevOps role
- Provide reliable messaging between services
- Operate clusters safely (upgrades, scaling, security)
- Monitor health and performance
- Ensure data durability and recovery
- Support schema governance and compatibility

## Core workflow
1. A producer sends records to a topic.
2. The broker appends records to partition logs.
3. Consumers read records using offsets.
4. Kafka retains records based on time or size.

## Key concepts in one page
- Topic: named stream of records
- Partition: ordered, append-only log within a topic
- Offset: position in a partition
- Consumer group: set of consumers sharing a workload
- Replication: copies of partitions across brokers
- ISR: in-sync replicas that are fully caught up

## When not to use Kafka
- Very low volume, simple point-to-point tasks
- Strict, real-time request-response workflows
- Workloads that require full SQL query on data at rest

## Learning goals
By the end of this tutorial, you should be able to:
- Deploy and operate Kafka clusters
- Create and manage topics safely
- Build Python producers and consumers
- Secure and monitor Kafka
- Respond to incidents with runbooks

Next: `01-foundations/README.md`
