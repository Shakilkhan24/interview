# Lab 05: Performance and Troubleshooting
Difficulty: Hard
Time: 60 minutes

## Objective
- Diagnose slow runs and reduce execution time.

## Prerequisites
- 5+ target hosts for meaningful timing

## Steps
1) Run a playbook with `-vvv` and note time spent in facts.
2) Disable `gather_facts` where not needed.
3) Increase `forks` in `ansible.cfg`.

```ini
[defaults]
forks = 20
```

## Validation
- Runtime improves by at least 30 percent.

## Cleanup
- Revert config if it causes resource pressure.