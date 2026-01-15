# CI/CD Question Bank (Mid to Senior)

## Easy
- Q1: What is the difference between CI and CD? Answer outline: CI builds/tests; CD deploys automatically or with approvals.
- Q2: Why are immutable artifacts important? Answer outline: reproducibility, auditability, rollback safety.
- Q3: What is a pipeline stage? Answer outline: logical step grouping tasks (build/test/deploy).
- Q4: What is a deployment strategy? Answer outline: rolling, blue/green, canary, etc.
- Q5: What is a release gate? Answer outline: check or approval before promotion.
- Q6: Why should tests run before deployment? Answer outline: prevent regressions early.
- Q7: What is a rollback? Answer outline: revert to last known good artifact.
- Q8: What is GitOps? Answer outline: Git is source of truth for desired state.
- Q9: What is a self-hosted runner? Answer outline: user-managed worker for jobs.
- Q10: What is a build artifact? Answer outline: packaged output of build step.

## Medium
- Q11: How do you ensure deploys are traceable? Answer outline: link build ID, commit SHA, artifact tag.
- Q12: Explain canary vs blue/green. Answer outline: canary shifts % traffic; blue/green swaps environment.
- Q13: How do you manage secrets in CI? Answer outline: secret manager, masked vars, no plaintext.
- Q14: What is a build cache and how does it help? Answer outline: speeds builds, reduces compute.
- Q15: How do you handle flaky tests? Answer outline: quarantine, retries with limits, root cause.
- Q16: How do you structure multi-environment pipelines? Answer outline: promote artifact, approvals for prod.
- Q17: What is policy-as-code in CI/CD? Answer outline: automated checks for compliance.
- Q18: When do you use manual approvals? Answer outline: high-risk steps or prod deploys.
- Q19: How do you avoid pipeline drift across repos? Answer outline: shared templates and versioned pipelines.
- Q20: What is the purpose of deploy verification? Answer outline: health checks, smoke tests, SLO checks.
- Q21: How do you reduce pipeline time safely? Answer outline: caching, parallelism, split tests.
- Q22: How do you secure pipeline runners? Answer outline: least privilege, ephemeral runners, network isolation.

## Hard
- Q23: Design a CI/CD pipeline for a regulated environment. Answer outline: strong approvals, audit logs, signed artifacts.
- Q24: How do you implement rollback in GitOps? Answer outline: revert Git commit or pin to previous tag.
- Q25: What are supply chain risks in CI/CD? Answer outline: dependency tampering, compromised runners, untrusted actions.
- Q26: How do you handle database migrations in CI/CD? Answer outline: backwards-compatible changes, phased deploy, rollback.
- Q27: How do you gate deployments on SLOs? Answer outline: query metrics, automatic halt if error budget breached.
- Q28: How do you manage deployments across multiple regions? Answer outline: phased rollout, regional health checks.
- Q29: What is a release candidate and how do you promote it? Answer outline: freeze artifact, validate, promote unchanged.
- Q30: How do you avoid hotfix chaos? Answer outline: fast-track pipeline with audit trail and post-incident review.
- Q31: How do you validate IaC changes in CI/CD? Answer outline: plan, policy checks, drift detection.
- Q32: How would you design a reusable pipeline platform? Answer outline: templates, shared runners, guardrails.
- Q33: How do you enforce least privilege for deploy jobs? Answer outline: scoped roles per env, short-lived tokens.
- Q34: Explain the risks of rebuilding in staging/prod. Answer outline: non-determinism, drift, rollback mismatch.
- Q35: How do you balance speed vs safety in CI/CD? Answer outline: risk-based gates, metrics, staged releases.
- Q36: What is progressive delivery? Answer outline: gradual rollout with automated checks and rollback.
- Q37: How do you handle multi-service deploy dependencies? Answer outline: order, compatibility matrix, contract tests.
- Q38: How do you test pipelines themselves? Answer outline: pipeline unit tests, dry runs, staging pipelines.
- Q39: What is artifact signing and why use it? Answer outline: integrity and provenance.
- Q40: How do you prevent secrets from leaking in logs? Answer outline: masking, no_log, avoid echoing env.