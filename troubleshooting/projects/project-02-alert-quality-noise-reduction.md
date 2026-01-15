# Project 02: Alert Quality and Noise Reduction
Difficulty: Hard
Time: 6-10 hours

## Requirements
- Reduce noisy alerts by 50 percent without losing coverage.
- Introduce at least 3 SLO-based alerts.

## Architecture
- Alert inventory spreadsheet
- Alert tuning plan

## Implementation Steps
1) Export current alerts and classify by type and severity.
2) Identify low-signal alerts and consolidate.
3) Add SLO-based alerts for critical services.
4) Implement routing and dedupe rules.

## Acceptance Tests
- Alert count reduced by at least 50 percent.
- SLO alerts fire correctly on simulated failures.

## Stretch Goals
- Add auto-remediation for low-risk alerts.
- Add weekly alert quality review.