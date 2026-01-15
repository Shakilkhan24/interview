# Project 01: On-Call Runbook and Toolkit
Difficulty: Hard
Time: 8-12 hours

## Requirements
- Create a runbook for top 5 incident types.
- Build a CLI toolkit with common diagnostic commands.

## Architecture
- `runbook.md` with decision flow
- `toolkit.sh` with safe read-only commands

## Implementation Steps
1) Identify top incident categories (latency, errors, capacity, deploy issues, dependency).
2) Write step-by-step investigation plans.
3) Implement read-only CLI scripts for quick checks.
4) Add validation and rollback steps.

## Acceptance Tests
- Runbook produces a consistent triage outcome.
- Toolkit runs without modifying systems.

## Stretch Goals
- Add chatops integration.
- Add incident note templates.