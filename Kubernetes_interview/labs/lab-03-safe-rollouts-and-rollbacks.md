# Lab 03: Safe Rollouts and Rollbacks
Difficulty: Medium
Time: 60 minutes

## Objective
- Perform a rolling update and rollback safely.

## Prerequisites
- Deployment with multiple replicas

## Steps
1) Update the image tag.
2) Watch rollout status.
3) Roll back to the previous version.

```bash
kubectl set image deploy/myapp app=myapp:v2
kubectl rollout status deploy/myapp
kubectl rollout undo deploy/myapp
```

## Validation
- Rollout completes and rollback restores v1.

## Cleanup
- None.