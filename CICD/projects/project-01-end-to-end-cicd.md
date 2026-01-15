# Project 01: End-to-End CI/CD Pipeline
Difficulty: Hard
Time: 8-12 hours

## Requirements
- CI build/test, artifact storage, deployment to staging and prod.
- Approved promotion to prod.
- Rollback strategy documented.

## Architecture
- CI: GitHub Actions or Jenkins
- Registry: ECR or GHCR
- Deploy: ArgoCD or Helm

## Implementation Steps
1) Build and tag by commit SHA.
2) Push artifact and store metadata.
3) Deploy to staging and run smoke tests.
4) Manual approval for prod.
5) Automated rollback if health check fails.

## Acceptance Tests
- Same artifact promoted across environments.
- Rollback completes within 10 minutes.

## Stretch Goals
- Add SLO gate for prod deploy.
- Add artifact signing.