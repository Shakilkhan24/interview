# 08 - Security

## Security layers
- Network encryption: TLS
- Authentication: SASL (PLAIN, SCRAM, OAUTHBEARER)
- Authorization: ACLs
- Audit: broker logs and access events

## Listener strategy
- Internal listener for inter-broker traffic
- External listener for clients
- Use separate ports and security protocols

## TLS example (broker config snippet)
```
listeners=INTERNAL://0.0.0.0:9092,EXTERNAL://0.0.0.0:9093
advertised.listeners=INTERNAL://kafka-1:9092,EXTERNAL://broker.example.com:9093
listener.security.protocol.map=INTERNAL:SSL,EXTERNAL:SASL_SSL
inter.broker.listener.name=INTERNAL

ssl.keystore.location=/etc/kafka/keystore.jks
ssl.keystore.password=changeit
ssl.key.password=changeit
ssl.truststore.location=/etc/kafka/truststore.jks
ssl.truststore.password=changeit
```

## SASL/SCRAM example (client)
```python
from confluent_kafka import Producer

conf = {
    "bootstrap.servers": "broker.example.com:9093",
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "SCRAM-SHA-512",
    "sasl.username": "app-user",
    "sasl.password": "secret",
}

p = Producer(conf)
```

## ACLs (conceptual)
- Producers: `WRITE` on topics
- Consumers: `READ` on topics + `READ` on group
- Admins: `CREATE`, `ALTER`, `DESCRIBE`

## DevOps checklists
- Rotate certs regularly.
- Avoid shared credentials between services.
- Separate human and service accounts.

Next: `09-monitoring-metrics/README.md`
