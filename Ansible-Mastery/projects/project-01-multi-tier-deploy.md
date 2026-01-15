# Project 01: Multi-Tier Deploy with Rolling Updates
Difficulty: Hard
Time: 6-8 hours

## Requirements
- Deploy a web tier and a db tier using roles.
- Rolling update with `serial` and health checks.
- Secrets managed with Vault.

## Architecture
- Inventory with `web` and `db` groups
- Roles: `web`, `db`, `common`

## Implementation Steps
1) Build role structure and defaults.
2) Add templates and handlers.
3) Add rolling update controls.
4) Add CI check mode run.

## Acceptance Tests
- First run converges to desired state.
- Second run shows no changes.
- Rolling update affects only one node at a time.

## Stretch Goals
- Add dynamic inventory for cloud provider.
- Add Molecule tests for roles.