# Lab 03: Roles and Templates
Difficulty: Medium
Time: 60 minutes

## Objective
- Create a role that manages nginx config using Jinja2 templates.

## Prerequisites
- Working playbook from Lab 02

## Steps
1) Create role structure under `roles/nginx/`.
2) Add a template `nginx.conf.j2`.
3) Add a handler to restart nginx on config change.
4) Run the playbook and verify config update.

```bash
ansible-galaxy init roles/nginx
```

## Validation
- `nginx -t` succeeds on target.
- Handler runs only when template changes.

## Cleanup
- Revert to default nginx config if needed.