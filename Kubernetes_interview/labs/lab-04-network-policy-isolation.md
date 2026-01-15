# Lab 04: Network Policy Isolation
Difficulty: Hard
Time: 75 minutes

## Objective
- Isolate traffic between namespaces with NetworkPolicy.

## Prerequisites
- CNI with NetworkPolicy support

## Steps
1) Create two namespaces and sample pods.
2) Deny all ingress by default.
3) Allow only frontend -> backend on port 8080.

## Validation
- Allowed traffic works, other traffic denied.

## Cleanup
- Delete namespaces.