# Lab 04: ArgoCD GitOps Sync
Difficulty: Medium
Time: 60 minutes

## Objective
- Create an ArgoCD app and sync from Git.

## Prerequisites
- Kubernetes cluster and ArgoCD installed

## Steps
1) Create app from Git repo.
2) Enable auto-sync and prune.
3) Trigger a Git change.

```bash
argocd app create demo \
  --repo https://github.com/example/repo \
  --path k8s \
  --dest-namespace demo \
  --dest-server https://kubernetes.default.svc
```

## Validation
- ArgoCD shows Synced and Healthy.

## Cleanup
- Delete the ArgoCD app and namespace.