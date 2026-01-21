# Kafka with Python - Master Level DevOps Tutorial

This is an end-to-end, hands-on Kafka tutorial focused on DevOps engineers who want to operate Kafka confidently and build reliable Python producers and consumers.

## How to use this guide
- Follow the modules in order for a full journey from fundamentals to production operations.
- Each module has a README with concepts, commands, and exercises.
- The capstone module brings everything together with an end-to-end pipeline.

## Modules
1. `00-overview/README.md` - What Kafka is, where it fits, core workflows
2. `01-foundations/README.md` - Architecture, log model, delivery guarantees
3. `02-local-setup/README.md` - Local Kafka using Docker, tools, first run
4. `03-topics-partitions/README.md` - Topics, partitions, replication, ISR
5. `04-cluster-ops/README.md` - Broker configs, scaling, upgrades, KRaft
6. `05-python-producers-consumers/README.md` - Python clients, patterns
7. `06-python-streams/README.md` - Stream processing patterns in Python
8. `07-schema-management/README.md` - Schemas, compatibility, evolution
9. `08-security/README.md` - TLS, SASL, ACLs, multi-tenant ops
10. `09-monitoring-metrics/README.md` - JMX, exporters, alerting
11. `10-kubernetes/README.md` - Kafka on K8s with Strimzi
12. `11-performance-tuning/README.md` - Throughput, latency, sizing
13. `12-troubleshooting/README.md` - Runbooks and incident response
14. `13-dr-backup/README.md` - MirrorMaker 2, backup, recovery
15. `14-capstone/README.md` - Full pipeline project

## Prerequisites
- Linux shell basics
- Docker and Docker Compose
- Python 3.10+ and pip
- Basic networking and TLS concepts

## Tooling used in examples
- Kafka 3.x
- `kcat` for quick produce/consume testing
- Python client: `confluent-kafka`
- Prometheus + Grafana (monitoring examples)
- Strimzi (Kubernetes examples)

## Ground rules for production
- Treat configuration and security as code.
- Track changes with Git, store secrets securely.
- Use IaC for cluster provisioning when possible.

If you want this adapted to your environment (bare metal, cloud managed Kafka, or a specific CI/CD system), call it out and we will tune the runbooks.
