# Lab 04: Kubernetes Pod Debugging
Difficulty: Medium
Time: 60 minutes

## Objective
- Diagnose a pod in CrashLoopBackOff.

## Prerequisites
- Kubernetes cluster with a failing pod

## Steps
1) Describe the pod and inspect events.
2) View current and previous logs.
3) Verify resource limits and env vars.

```bash
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
kubectl get pod <pod> -o yaml | rg "resources|env"
```

## Validation
- You can identify the failure reason and exit code.

## Cleanup
- None.