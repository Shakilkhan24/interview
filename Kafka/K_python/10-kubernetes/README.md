# 10 - Kafka on Kubernetes (Strimzi)

Strimzi is the most common operator for running Kafka on Kubernetes.

## Key considerations
- Use dedicated nodes or node pools if possible.
- Use SSD-backed persistent volumes.
- Spread brokers across zones.
- Use PodDisruptionBudgets.

## Minimal Strimzi Kafka CR
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka
spec:
  kafka:
    version: 3.6.1
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    storage:
      type: persistent-claim
      size: 100Gi
      deleteClaim: false
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      min.insync.replicas: 2
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 20Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

## Operational tips
- Keep Kafka and ZooKeeper on separate node pools.
- Use rack awareness and topology keys.
- Tune JVM heap and page cache; avoid oversizing heap.
- Do not rely on auto topic creation in production.

Next: `11-performance-tuning/README.md`
