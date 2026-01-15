# Lab 03: Artifact Immutability
Difficulty: Medium
Time: 60 minutes

## Objective
- Build once and deploy the same artifact to two environments.

## Prerequisites
- Artifact registry (ECR, GHCR, or S3)

## Steps
1) Build and tag an artifact with commit SHA.
2) Push to registry.
3) Deploy the same digest to staging and prod.

## Validation
- Same digest is used across environments.

## Cleanup
- Delete test artifacts from the registry if needed.