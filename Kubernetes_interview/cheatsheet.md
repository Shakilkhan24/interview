# Kubernetes Cheatsheet

## Triage
- `kubectl get pods -A`
- `kubectl describe pod <pod>`
- `kubectl logs <pod> --previous`
- `kubectl top nodes`

## Rollouts
- `kubectl rollout status deploy/<name>`
- `kubectl rollout undo deploy/<name>`

## Scheduling
- `kubectl describe node <node>`
- `kubectl get events --sort-by=.lastTimestamp`

## Decision Rules
- Pod pending -> check resources, taints, PVC.
- CrashLoop -> check logs, config, probes.
- Slow rollout -> check readiness and maxUnavailable.