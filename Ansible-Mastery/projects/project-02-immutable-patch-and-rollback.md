# Project 02: Immutable Patch and Rollback Strategy
Difficulty: Hard
Time: 5-7 hours

## Requirements
- Use Ansible to build images (or configure base AMI) and deploy via blue/green.
- Rollback plan documented and tested.

## Architecture
- Image build phase (Packer + Ansible)
- Blue/green deploy with traffic switch

## Implementation Steps
1) Create a Packer template using Ansible provisioner.
2) Bake image and deploy to blue environment.
3) Run smoke tests and flip traffic.
4) Implement rollback by switching back.

## Acceptance Tests
- Deployment completes without configuration drift.
- Rollback completes within 10 minutes.

## Stretch Goals
- Add automated image vulnerability scan.
- Add canary deployment step.