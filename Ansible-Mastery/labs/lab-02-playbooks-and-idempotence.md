# Lab 02: Playbooks and Idempotence
Difficulty: Medium
Time: 45 minutes

## Objective
- Write a playbook that installs and starts nginx idempotently.

## Prerequisites
- Inventory from Lab 01
- Ubuntu or Debian hosts

## Steps
1) Create `site.yml` that installs nginx and enables it.
2) Run the playbook twice with `--diff` and confirm no changes on second run.

```yaml
- name: Nginx setup
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true

    - name: Enable and start nginx
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true
```

## Validation
- First run shows `changed`.
- Second run shows `ok` with no `changed`.

## Cleanup
- Optional: remove nginx with `state: absent`.