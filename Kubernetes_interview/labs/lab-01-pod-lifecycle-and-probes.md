# Lab 01: Pod Lifecycle and Probes
Difficulty: Easy
Time: 45 minutes

## Objective
- Configure readiness and liveness probes correctly.

## Prerequisites
- Kubernetes cluster and kubectl

## Steps
1) Deploy a simple app with readiness and liveness probes.
2) Force a readiness failure and observe traffic removal.
3) Force a liveness failure and observe restart.

## Validation
- Readiness removes pod from Service endpoints.
- Liveness restarts the container.

## Cleanup
- Delete the deployment.