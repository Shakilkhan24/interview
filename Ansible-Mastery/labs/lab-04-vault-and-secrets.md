# Lab 04: Vault and Secrets
Difficulty: Medium
Time: 45 minutes

## Objective
- Encrypt credentials using Ansible Vault and use them in a play.

## Prerequisites
- Vault password file or interactive access

## Steps
1) Create `group_vars/web/vault.yml` and encrypt it.
2) Reference the secret in a template or task.
3) Run the playbook with `--vault-password-file`.

```bash
ansible-vault encrypt group_vars/web/vault.yml
ansible-playbook -i inventory.ini site.yml --vault-password-file ~/.vault_pass
```

## Validation
- Playbook succeeds and uses decrypted values.

## Cleanup
- Remove temporary vault password file if needed.