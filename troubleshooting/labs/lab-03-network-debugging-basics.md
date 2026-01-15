# Lab 03: Network Debugging Basics
Difficulty: Medium
Time: 60 minutes

## Objective
- Validate connectivity and isolate network path issues.

## Prerequisites
- Two reachable hosts

## Steps
1) Check DNS resolution and TCP connectivity.
2) Identify listening services and ports.
3) Trace route to remote host.

```bash
dig example.com
ss -tulpn
curl -sS -D - https://example.com/healthz
traceroute example.com
```

## Validation
- You can confirm DNS, TCP connectivity, and service response.

## Cleanup
- None.