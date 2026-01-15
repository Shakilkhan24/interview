# Project 02: Multi-Environment GitOps Pipeline
Difficulty: Hard
Time: 8-12 hours

## Requirements
- Separate dev/staging/prod namespaces or clusters.
- GitOps tool (ArgoCD or Flux) with auto-sync.
- Promotion by artifact digest.

## Architecture
- Git repo with environment overlays
- GitOps controller per cluster

## Implementation Steps
1) Create base manifests and environment overlays.
2) Configure GitOps with auto-sync.
3) Promote by updating image digest.
4) Add rollback via Git revert.

## Acceptance Tests
- Dev change promotes to staging and prod by digest.
- Rollback through Git restores previous version.

## Stretch Goals
- Add policy checks before sync.
- Add audit report generation.