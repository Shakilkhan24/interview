# CI/CD Cheatsheet

## Core Patterns
- Build once, deploy many.
- Promote by digest, not tag.
- Gate by tests, security, and SLOs.

## Common Commands
- `argocd app sync my-app --prune`
- `argocd app wait my-app --health`
- `gh workflow run ci.yml`

## Decision Rules
- High risk deploy -> manual approval.
- User-facing change -> add smoke tests.
- Infra change -> plan + policy checks.