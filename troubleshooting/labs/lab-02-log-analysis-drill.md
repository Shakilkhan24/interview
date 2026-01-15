# Lab 02: Log Analysis Drill
Difficulty: Medium
Time: 60 minutes

## Objective
- Extract error patterns from service logs.

## Prerequisites
- Access to a log file or journal

## Steps
1) Identify error spikes in logs.
2) Filter by time window.
3) Summarize top error messages.

```bash
journalctl -u my-service --since "30 min ago" | tail -n 200
journalctl -u my-service --since "30 min ago" | rg "ERROR|Exception" | sort | uniq -c | sort -nr | head
```

## Validation
- You can list top 3 error messages by frequency.

## Cleanup
- None.