# Project 01: Production-Ready Kubernetes App
Difficulty: Hard
Time: 10-14 hours

## Requirements
- Deployment with readiness/liveness probes.
- PDB, resource limits, and HPA.
- Safe rollout and rollback plan.

## Architecture
- Deployment, Service, HPA, PDB
- Optional: Ingress with TLS

## Implementation Steps
1) Build baseline manifests with probes and resources.
2) Add PDB and HPA.
3) Implement canary or blue/green rollout.
4) Create rollback and verification steps.

## Acceptance Tests
- Rollout completes with no downtime.
- Rollback restores previous version.

## Stretch Goals
- Add network policies.
- Add GitOps synchronization.