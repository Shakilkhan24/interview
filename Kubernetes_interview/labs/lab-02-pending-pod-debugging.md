# Lab 02: Pending Pod Debugging
Difficulty: Medium
Time: 60 minutes

## Objective
- Diagnose why a pod is Pending.

## Prerequisites
- Cluster with resource constraints

## Steps
1) Create a pod with high resource requests.
2) Observe scheduling failure events.
3) Fix by reducing requests or freeing capacity.

```bash
kubectl describe pod <pod>
kubectl get events --sort-by=.lastTimestamp
```

## Validation
- Pod schedules successfully.

## Cleanup
- Delete the pod.