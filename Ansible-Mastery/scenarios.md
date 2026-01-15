# Ansible Real Scenarios (Mid to Senior)

## Scenario 1: Playbook Hangs on Gathering Facts
- Symptoms/logs:
```text
TASK [Gathering Facts] ******************************************************
```
- Constraints: production change window 30 minutes; cannot reboot.
- Investigation plan: check SSH connectivity; run `ansible -m ping`; inspect `ansible.cfg` timeout; verify Python availability on target.
- Final fix + prevention: install Python or set `ansible_python_interpreter`; add preflight task to verify interpreter.
- Postmortem notes: detection time, root cause, action item to add preflight.

## Scenario 2: Service Restarted on Every Run
- Symptoms/logs:
```text
changed: [web1]
changed: [web2]
```
- Constraints: avoid restarts during peak traffic.
- Investigation plan: check template rendering; compare managed file with diff; check handler notifications.
- Final fix + prevention: fix template to avoid non-deterministic content; enable `--diff` in CI; add idempotence test.
- Postmortem notes: customer impact, change control, validation gap.

## Scenario 3: Vault Decryption Fails in CI
- Symptoms/logs:
```text
ERROR! Decryption failed (no vault secrets were found)
```
- Constraints: CI has no interactive input.
- Investigation plan: verify vault password file path; check CI secret mounting; ensure correct vault ID.
- Final fix + prevention: use `--vault-id` with secret store; add CI sanity check.
- Postmortem notes: pipeline failure time, missing documentation.

## Scenario 4: Rolling Update Caused Partial Outage
- Symptoms/logs:
```text
503 from load balancer during deploy
```
- Constraints: must deploy within 20 minutes; can only take 1 node at a time.
- Investigation plan: confirm `serial` setting; validate drain script; check health checks.
- Final fix + prevention: set `serial: 1`; add LB drain and post-check; enforce `max_fail_percentage: 0`.
- Postmortem notes: update rollout policy, add canary step.

## Scenario 5: Dynamic Inventory Returns Empty
- Symptoms/logs:
```text
Skipping, empty host list
```
- Constraints: AWS access via assumed role.
- Investigation plan: test inventory script; check AWS creds/region; review IAM permissions.
- Final fix + prevention: fix AWS env vars; add inventory health check in CI.
- Postmortem notes: IAM change review process.

## Scenario 6: WinRM Connection Errors
- Symptoms/logs:
```text
UNREACHABLE! => "ssl: CERTIFICATE_VERIFY_FAILED"
```
- Constraints: Windows fleet, no SSH.
- Investigation plan: verify WinRM listener; cert validity; set `ansible_winrm_server_cert_validation=ignore` for test.
- Final fix + prevention: deploy proper certs; document WinRM config baseline.
- Postmortem notes: standardize Windows bootstrap.

## Scenario 7: Package Install Fails on One Host
- Symptoms/logs:
```text
E: Could not get lock /var/lib/dpkg/lock
```
- Constraints: cannot interrupt running apt process.
- Investigation plan: check running apt process; wait or kill carefully; add retries.
- Final fix + prevention: add `retries` with `until`; schedule maintenance windows.
- Postmortem notes: avoid parallel apt operations.

## Scenario 8: Playbook Slow on Large Fleet
- Symptoms/logs:
```text
Playbook runtime > 2 hours
```
- Constraints: change window 1 hour.
- Investigation plan: check `gather_facts`, forks, and task count; profile with `-vvv`.
- Final fix + prevention: disable facts where not needed; increase forks; reduce `shell` usage.
- Postmortem notes: performance baseline documentation.

## Scenario 9: Handler Not Triggering
- Symptoms/logs:
```text
TASK [template] ok
```
- Constraints: config must be applied with restart.
- Investigation plan: verify file change; confirm handler name; check `notify`.
- Final fix + prevention: fix `notify` name; use `checksum` to validate template change.
- Postmortem notes: add unit test for handler trigger.

## Scenario 10: Secrets Leaked in Logs
- Symptoms/logs:
```text
TASK [debug] => {"password": "plain-text"}
```
- Constraints: logs already shipped to SIEM.
- Investigation plan: identify debug usage; remove sensitive output; check `no_log` usage.
- Final fix + prevention: use `no_log: true`; sanitize logs; rotate secrets.
- Postmortem notes: incident severity, compliance notification.