# Lab 01: Inventory and Ad-Hoc Basics
Difficulty: Easy
Time: 30 minutes

## Objective
- Build a static inventory and run ad-hoc commands safely.

## Prerequisites
- Ansible installed
- Two Linux hosts accessible via SSH

## Steps
1) Create `inventory.ini` with `web` and `db` groups.
2) Run `ansible -i inventory.ini all -m ping`.
3) Run an ad-hoc command to check uptime on `web` group.

```ini
[web]
web1 ansible_host=10.0.1.10

[db]
db1 ansible_host=10.0.2.10
```

## Validation
- `ping` returns `pong` for both hosts.
- `uptime` command returns output for web hosts.

## Cleanup
- None.