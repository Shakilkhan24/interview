# Lab 05: Incident Timeline and Rollback Drill
Difficulty: Hard
Time: 90 minutes

## Objective
- Practice structured incident response and rollback.

## Prerequisites
- Sample app or service with deploy history

## Steps
1) Simulate an incident by introducing a bad config.
2) Capture timeline: detection, triage, mitigation, fix.
3) Roll back to the previous artifact.

```text
Timeline:
- 12:01 Alert triggered
- 12:03 Scope confirmed
- 12:05 Mitigation started
- 12:08 Rollback complete
```

## Validation
- Service metrics return to baseline after rollback.

## Cleanup
- Revert any test config changes.