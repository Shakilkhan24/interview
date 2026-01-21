# 09 - Monitoring and Metrics

## Critical health signals
- Under-replicated partitions (URP)
- Offline partitions
- Controller status
- Disk usage per broker
- Request latency and error rates
- Consumer group lag

## JMX to Prometheus
Kafka exposes metrics over JMX. Use the JMX exporter agent:
```
KAFKA_OPTS="-javaagent:/opt/jmx_exporter/jmx_prometheus_javaagent.jar=7071:/opt/jmx_exporter/kafka.yml"
```

## Example Prometheus queries
- Under-replicated partitions:
```
max(kafka_server_replica_manager_under_replicated_partitions)
```
- Controller count:
```
sum(kafka_controller_kafkacontroller_activecontrollercount)
```
- Request latency:
```
rate(kafka_network_requestmetrics_totaltimems_sum[5m]) / rate(kafka_network_requestmetrics_totaltimems_count[5m])
```

## Consumer lag
- Use `kafka-consumer-groups --describe` for manual checks.
- For production, use Burrow or a Prometheus exporter.

## Alerting ideas
- URP > 0 for 5 minutes
- Offline partitions > 0
- Disk usage > 80%
- ISR shrink rate spike
- Consumer lag increasing steadily

Next: `10-kubernetes/README.md`
