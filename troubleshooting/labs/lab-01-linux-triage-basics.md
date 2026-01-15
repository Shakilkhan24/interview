# Lab 01: Linux Triage Basics
Difficulty: Easy
Time: 45 minutes

## Objective
- Capture CPU, memory, disk, and process state quickly.

## Prerequisites
- Linux host or VM

## Steps
1) Run `uptime`, `free -m`, `df -h`.
2) Identify top CPU and memory processes.
3) Check system logs for recent errors.

```bash
uptime
free -m
df -h
ps aux --sort=-%cpu | head
journalctl -xe
```

## Validation
- You can name the top CPU process and free disk space.

## Cleanup
- None.