# 02 - Local Setup (Docker)

This module uses a single-broker Kafka setup with KRaft for quick local testing.

## Prerequisites
- Docker + Docker Compose
- `kcat` (optional but recommended)

## docker-compose.yml (single broker, KRaft)
```yaml
version: '3.8'
services:
  kafka:
    image: confluentinc/cp-kafka:7.6.1
    hostname: kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_LOG_DIRS: /var/lib/kafka/data
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
    volumes:
      - kafka-data:/var/lib/kafka/data
volumes:
  kafka-data:
```

Start the broker:
```bash
docker compose up -d
```

## Create a topic
```bash
docker exec -it kafka kafka-topics --create --topic orders --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

## Produce and consume with CLI
```bash
# Produce
printf "order-1\norder-2\n" | docker exec -i kafka kafka-console-producer --topic orders --bootstrap-server localhost:9092

# Consume
 docker exec -it kafka kafka-console-consumer --topic orders --from-beginning --bootstrap-server localhost:9092
```

## Optional: kcat
```bash
# Produce
kcat -b localhost:9092 -t orders -P

# Consume
kcat -b localhost:9092 -t orders -C -o beginning
```

## Cleanup
```bash
docker compose down -v
```

Next: `03-topics-partitions/README.md`
