# Troubleshooting Cheatsheet

## Triage Commands
- `uptime` `top` `htop`
- `free -m` `vmstat 1 5`
- `df -h` `du -sh *`
- `journalctl -xe`

## Network
- `ss -tulpn`
- `curl -sS -D - https://service/healthz`
- `dig example.com`
- `traceroute example.com`

## Kubernetes
- `kubectl get pods -A`
- `kubectl describe pod <pod>`
- `kubectl logs <pod> --previous`
- `kubectl top nodes`

## Decision Rules
- High impact + unknown cause -> rollback or mitigate first.
- Single host issue -> isolate before changing fleet.
- Always verify with metrics and logs.