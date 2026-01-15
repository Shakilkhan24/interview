# Troubleshooting Question Bank (Mid to Senior)

## Easy
- Q1: What is your first step when paged for an outage? Answer outline: confirm impact, scope, and recent changes.
- Q2: What is the difference between symptoms and root cause? Answer outline: symptoms are effects, root cause is underlying issue.
- Q3: Name three basic Linux triage commands. Answer outline: uptime, free, df, top, journalctl.
- Q4: What is a rollback and when do you use it? Answer outline: revert to known good when risk or time is high.
- Q5: Why are health checks important? Answer outline: validate service state, catch regressions.
- Q6: How do you check if a port is listening? Answer outline: ss, netstat, lsof.
- Q7: What is a feature flag? Answer outline: toggle behavior without redeploy.
- Q8: What is the purpose of a postmortem? Answer outline: learning and prevention, not blame.
- Q9: How do you confirm which version is running? Answer outline: release metadata, labels, image tag.
- Q10: What is the difference between 4xx and 5xx? Answer outline: client vs server errors.

## Medium
- Q11: How do you isolate whether an issue is app, infra, or network? Answer outline: checks across layers; compare metrics and logs.
- Q12: How do you handle a flaky alert? Answer outline: validate signal, tune thresholds, add context.
- Q13: What is your approach to a memory leak? Answer outline: confirm growth, capture heap, restart as mitigation.
- Q14: Explain how you would debug DNS issues. Answer outline: check resolver, dig/nslookup, TTL, cache.
- Q15: How do you decide between scaling vs rollback? Answer outline: impact, risk, time, evidence.
- Q16: What is a canary in troubleshooting? Answer outline: test fix on small subset.
- Q17: How do you detect saturation? Answer outline: CPU, memory, disk IO, queue depth.
- Q18: How do you validate a fix? Answer outline: metrics return to baseline, logs normalize.
- Q19: How do you handle partial failures in distributed systems? Answer outline: isolate dependency, failover, degrade gracefully.
- Q20: What is a runbook and why is it useful? Answer outline: repeatable steps, reduces errors.
- Q21: How do you investigate a sudden spike in latency? Answer outline: check upstream dependencies, DB, network, slow queries.
- Q22: What is the role of SLOs in incident response? Answer outline: define impact and guide decisions.

## Hard
- Q23: How do you debug cascading failures across microservices? Answer outline: dependency map, circuit breakers, isolate root trigger.
- Q24: Describe a safe mitigation under time pressure. Answer outline: reversible change, minimal blast radius.
- Q25: How do you perform a live migration to reduce downtime? Answer outline: blue/green, traffic shift, health checks.
- Q26: How do you troubleshoot intermittent packet loss? Answer outline: measure at each hop, interface errors, congestion.
- Q27: How do you identify a bad deploy vs a traffic spike? Answer outline: compare to deploy timeline and metrics baselines.
- Q28: How do you balance incident response with data integrity? Answer outline: prioritize correctness, avoid destructive actions.
- Q29: How do you recover from a full disk on a critical node? Answer outline: identify large files, clear safely, prevent recurrence.
- Q30: How do you use tracing to find a bottleneck? Answer outline: latency breakdown by span.
- Q31: How do you debug a Kubernetes CrashLoopBackOff? Answer outline: check logs, describe, readiness, exit codes.
- Q32: How do you troubleshoot a CI pipeline that fails only in prod? Answer outline: environment diff, secrets, network, permissions.
- Q33: How do you verify a dependency outage? Answer outline: synthetic checks, vendor status, error correlation.
- Q34: What is your strategy for incident communication? Answer outline: regular updates, clear impact, ETA, owner.
- Q35: How do you prevent repeat incidents? Answer outline: fix root cause, add tests, monitoring, and documentation.
- Q36: How do you validate that a rollback did not introduce data drift? Answer outline: compare schema, data checks, audit logs.