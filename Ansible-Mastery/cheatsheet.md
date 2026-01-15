# Ansible Cheatsheet

## Core Commands
- `ansible -i inventory.ini all -m ping`
- `ansible-playbook -i inventory.ini site.yml --check --diff`
- `ansible-inventory -i inventory.ini --graph`

## Common Patterns
- Use modules over `shell` for idempotence.
- Use handlers for restarts only when config changes.
- Use `serial` for controlled rollouts.

## Decision Rules
- Need configuration state -> playbook.
- Need one-off command -> ad-hoc.
- Secrets in repo -> Vault or external secret store.