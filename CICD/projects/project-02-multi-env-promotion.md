# Project 02: Multi-Environment Promotion Pipeline
Difficulty: Hard
Time: 6-10 hours

## Requirements
- Promote dev -> staging -> prod using the same artifact.
- Approvals and audit trail for prod.

## Architecture
- Promotion workflow with protected environments.

## Implementation Steps
1) Build artifact in dev and tag by digest.
2) Promote digest to staging with tests.
3) Promote digest to prod with approval.

## Acceptance Tests
- Audit report includes commit, build ID, artifact digest.
- Promotions are blocked without approval.

## Stretch Goals
- Add automated change ticket creation.