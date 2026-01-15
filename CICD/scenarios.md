# CI/CD Real Scenarios (Mid to Senior)

## Scenario 1: Prod Deploy Succeeds but Traffic Errors Spike
- Symptoms/logs:
```text
5xx rate increased after deploy, health checks still passing
```
- Constraints: 10 minutes to stabilize, no full rollback if data migration is in progress.
- Investigation plan: compare release vs previous artifact; check feature flags; review recent config changes.
- Final fix + prevention: disable feature flag; add canary metrics gate before full rollout.
- Postmortem notes: missing SLO gate, improve staged verification.

## Scenario 2: GitHub Actions Runner Compromised
- Symptoms/logs:
```text
Unexpected outbound traffic from runner VM
```
- Constraints: cannot pause releases longer than 1 hour.
- Investigation plan: isolate runner, rotate secrets, review workflow permissions.
- Final fix + prevention: move to ephemeral runners; restrict permissions; add OIDC auth.
- Postmortem notes: credential exposure risk and rotation plan.

## Scenario 3: Jenkins Pipeline Hangs on Integration Tests
- Symptoms/logs:
```text
stage 'Integration Tests' running > 2 hours
```
- Constraints: deployment window closing.
- Investigation plan: check test logs; verify external deps; rerun with timeout.
- Final fix + prevention: add timeouts and retries; isolate flaky tests.
- Postmortem notes: test stability and dependencies.

## Scenario 4: ArgoCD Shows OutOfSync After Merge
- Symptoms/logs:
```text
Application OutOfSync, resource drift detected
```
- Constraints: no manual kubectl changes allowed in prod.
- Investigation plan: compare live vs git; check drift source (manual changes, controller).
- Final fix + prevention: revert manual changes; enable auto-sync with prune.
- Postmortem notes: enforce change policy.

## Scenario 5: Deployment Rolled Back but DB Migration Applied
- Symptoms/logs:
```text
App reverted but schema is forward-only
```
- Constraints: cannot restore from snapshot due to time.
- Investigation plan: verify migration status; check backward compatibility.
- Final fix + prevention: use backward-compatible migrations; implement expand/contract.
- Postmortem notes: migration gate requirements.

## Scenario 6: Pipeline Secrets Leaked in Logs
- Symptoms/logs:
```text
echo $API_KEY printed in build log
```
- Constraints: logs already shipped to SIEM.
- Investigation plan: remove echo, rotate keys, audit workflow.
- Final fix + prevention: mask secrets; add lint for unsafe commands.
- Postmortem notes: secret handling policy.

## Scenario 7: Canary Rollout Stuck at 10 Percent
- Symptoms/logs:
```text
canary metrics never reach pass threshold
```
- Constraints: business needs deploy within 1 hour.
- Investigation plan: validate metrics query and baseline; check sampling.
- Final fix + prevention: fix metric query; add preflight SLO check.
- Postmortem notes: monitoring correctness.

## Scenario 8: Artifact Missing in Registry
- Symptoms/logs:
```text
image tag not found
```
- Constraints: release must go out.
- Investigation plan: check build logs; verify tag logic; check retention policy.
- Final fix + prevention: fix tagging; enforce retention; add artifact presence check.
- Postmortem notes: registry policy update.

## Scenario 9: AWS CodeBuild Fails Due to IAM
- Symptoms/logs:
```text
AccessDenied for s3:GetObject
```
- Constraints: no direct access to prod bucket.
- Investigation plan: review CodeBuild role; check resource policy.
- Final fix + prevention: least-privilege IAM update; add role validation step.
- Postmortem notes: IAM change review.

## Scenario 10: Multi-Env Promotion Promotes Wrong Artifact
- Symptoms/logs:
```text
staging artifact differs from prod
```
- Constraints: can only fix via pipeline.
- Investigation plan: compare commit SHA and artifact digest.
- Final fix + prevention: promote by digest, not tag; lock build metadata.
- Postmortem notes: artifact immutability policy.

## Scenario 11: Parallel Jobs Exhaust Runners
- Symptoms/logs:
```text
No runners available, jobs queued
```
- Constraints: SLA on build time.
- Investigation plan: check runner pool size; look for stuck jobs.
- Final fix + prevention: autoscale runners; add job timeouts.
- Postmortem notes: capacity planning.

## Scenario 12: Deployed Config Drift from Git
- Symptoms/logs:
```text
Config mismatch between Git and runtime
```
- Constraints: must restore desired state quickly.
- Investigation plan: check ArgoCD diff; verify manual changes.
- Final fix + prevention: enforce GitOps, disable manual edits.
- Postmortem notes: change control compliance.