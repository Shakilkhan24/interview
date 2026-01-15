# Troubleshooting Scenarios (Mid to Senior)

## Scenario 1: CPU Saturation After Deploy
- Symptoms/logs:
```text
CPU 95-100 percent, request latency 10x baseline
```
- Constraints: peak traffic, no maintenance window.
- Investigation plan: check deploy timeline, compare metrics per version, profile hot endpoints.
- Final fix + prevention: rollback or scale out, add performance regression test.
- Postmortem notes: alert improvements and perf budget.

## Scenario 2: Disk Full on Logging Node
- Symptoms/logs:
```text
No space left on device
```
- Constraints: logs are required for compliance.
- Investigation plan: identify top directories, check log rotation, verify retention policy.
- Final fix + prevention: clear old logs safely, increase disk, enforce retention.
- Postmortem notes: capacity planning.

## Scenario 3: DNS Resolution Fails in One AZ
- Symptoms/logs:
```text
temporary failure in name resolution
```
- Constraints: only one AZ affected, must restore quickly.
- Investigation plan: check resolver health, VPC DNS, node-level resolv.conf.
- Final fix + prevention: fail traffic to healthy AZ, fix resolver, add health checks.
- Postmortem notes: multi-AZ resilience.

## Scenario 4: Kubernetes CrashLoopBackOff
- Symptoms/logs:
```text
Back-off restarting failed container
```
- Constraints: can only restart one replica at a time.
- Investigation plan: inspect logs, exit code, config changes, resource limits.
- Final fix + prevention: fix config or image, add readiness checks.
- Postmortem notes: deploy validation gaps.

## Scenario 5: TLS Certificate Expired
- Symptoms/logs:
```text
x509: certificate has expired or is not yet valid
```
- Constraints: renew without downtime.
- Investigation plan: confirm cert chain, check expiration, identify responsible service.
- Final fix + prevention: renew cert, automate rotation and alerts.
- Postmortem notes: certificate tracking.

## Scenario 6: CI Pipeline Fails After Dependency Update
- Symptoms/logs:
```text
Module not found after upgrade
```
- Constraints: release blocked.
- Investigation plan: review lockfile changes, rollback dependency bump, run targeted tests.
- Final fix + prevention: pin version, add compatibility tests.
- Postmortem notes: dependency policy.

## Scenario 7: High Error Rate from One Service
- Symptoms/logs:
```text
5xx spike from service B, upstream OK
```
- Constraints: cannot redeploy all services.
- Investigation plan: check service B logs, recent config, downstream dependency health.
- Final fix + prevention: rollback service B, add circuit breaker.
- Postmortem notes: dependency health gates.

## Scenario 8: Container Image Pull BackOff
- Symptoms/logs:
```text
ImagePullBackOff
```
- Constraints: prod cluster.
- Investigation plan: verify image tag, registry auth, network access.
- Final fix + prevention: fix tag or registry credentials, add pre-deploy image check.
- Postmortem notes: registry reliability.

## Scenario 9: Slow Database Queries
- Symptoms/logs:
```text
p95 query latency 3s
```
- Constraints: cannot take DB offline.
- Investigation plan: identify slow queries, check indexes, review recent schema changes.
- Final fix + prevention: add index, optimize query, add query budget alerts.
- Postmortem notes: performance regression detection.

## Scenario 10: Alert Storm from Noisy Metrics
- Symptoms/logs:
```text
hundreds of alerts per hour
```
- Constraints: on-call overload.
- Investigation plan: evaluate alert conditions, merge duplicates, add rate limiting.
- Final fix + prevention: tune thresholds, add dedupe and routing.
- Postmortem notes: alerting hygiene policy.

## Scenario 11: Network Latency Spikes Between Services
- Symptoms/logs:
```text
intra-service latency +300ms
```
- Constraints: cannot change network topology.
- Investigation plan: trace request path, check load balancer metrics, verify congestion.
- Final fix + prevention: scale out, adjust timeouts, add retries with jitter.
- Postmortem notes: capacity and timeout standards.

## Scenario 12: Configuration Drift in Production
- Symptoms/logs:
```text
prod config differs from git
```
- Constraints: compliance requires audit trail.
- Investigation plan: compare deployed config to source of truth, find manual change.
- Final fix + prevention: restore from git, enforce GitOps, remove manual access.
- Postmortem notes: access control review.