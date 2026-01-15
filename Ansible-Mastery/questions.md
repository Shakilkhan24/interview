# Ansible Question Bank (Mid to Senior)

## Easy
- Q1: What is Ansible and why is it considered agentless? Answer outline: control node uses SSH/WinRM; no daemon on managed nodes.
- Q2: What is idempotence in Ansible? Answer outline: repeated runs converge to same state; avoids unintended changes.
- Q3: What is an inventory file and what does it contain? Answer outline: hosts/groups/vars; static or dynamic.
- Q4: Difference between `command` and `shell` modules? Answer outline: `shell` uses shell features; `command` is safer.
- Q5: What is a playbook? Answer outline: YAML file with plays; maps hosts to tasks.
- Q6: What are handlers? Answer outline: tasks triggered by `notify`; run once at end.
- Q7: What is the purpose of `become`? Answer outline: privilege escalation to root or other user.
- Q8: How do you run a playbook on a subset of hosts? Answer outline: `--limit` flag and inventory groups.
- Q9: What is `ansible.cfg` used for? Answer outline: defaults for inventory, roles_path, forks, etc.
- Q10: What does `--check` mode do? Answer outline: dry-run to show changes without applying.
- Q11: What are `group_vars` and `host_vars`? Answer outline: variable scoping per group/host.
- Q12: What is a role? Answer outline: structured, reusable tasks and assets.

## Medium
- Q13: Explain variable precedence and how you avoid surprises. Answer outline: document sources; prefer group_vars and extra-vars; limit overrides.
- Q14: How do you implement a rolling update with Ansible? Answer outline: use `serial`, handlers, health checks, and `max_fail_percentage`.
- Q15: How do you test roles? Answer outline: use Molecule; separate defaults; lint; idempotence tests.
- Q16: When would you use `import_tasks` vs `include_tasks`? Answer outline: import is static at parse-time; include is dynamic at runtime.
- Q17: How do you manage secrets in Ansible? Answer outline: Vault; CI secrets; avoid plaintext in repo.
- Q18: How do you structure a multi-environment setup? Answer outline: inventory per env; group_vars; env-specific vaults; CI gates.
- Q19: How do you handle errors in tasks? Answer outline: `failed_when`, `ignore_errors` carefully, block/rescue/always.
- Q20: Explain `delegate_to` and a use case. Answer outline: run task on controller or another host; e.g., update LB.
- Q21: How do you speed up slow playbook runs? Answer outline: reduce facts, use `gather_facts: false`, increase forks, limit scope.
- Q22: What is a dynamic inventory and why use it? Answer outline: generated from cloud APIs; reduces drift.
- Q23: How do you implement service restarts safely? Answer outline: handlers triggered on config change; `serial`.
- Q24: How do you validate changes before rollout? Answer outline: `--check`, `--diff`, test environments, canary.

## Hard
- Q25: Design an Ansible strategy for zero-downtime deploys behind a load balancer. Answer outline: drain node, deploy, health check, reattach, serial.
- Q26: How would you debug intermittent task failures across a large fleet? Answer outline: increase verbosity, isolate host, check network/SSH, retries with `until`.
- Q27: What are idempotence pitfalls with `shell`/`command` and how do you fix them? Answer outline: use `creates`/`removes`, or modules.
- Q28: Explain how you would model immutable infrastructure with Ansible. Answer outline: bake images, use Ansible for image build, not post-deploy changes.
- Q29: How do you prevent configuration drift with Ansible? Answer outline: scheduled runs, compliance checks, CI enforcement, diff reporting.
- Q30: How do you structure roles for a large org with shared components? Answer outline: galaxy-style roles, versioning, internal registry.
- Q31: Discuss Ansible Vault in CI/CD and key management. Answer outline: separate keys; rotate; use CI secret store.
- Q32: When is Ansible not the right tool? Answer outline: heavy orchestration, event-driven workflows, complex dependency graphs.
- Q33: How do you manage Windows nodes? Answer outline: WinRM setup, `ansible_user`, `ansible_connection=winrm`, modules.
- Q34: Explain `strategy: free` tradeoffs. Answer outline: faster but harder to reason about ordering and handlers.
- Q35: How do you handle partial failures with `serial` and `max_fail_percentage`? Answer outline: control blast radius; abort if threshold exceeded.
- Q36: How would you migrate from ad-hoc scripts to Ansible at scale? Answer outline: inventory first, module parity, incremental roles, testing gates.