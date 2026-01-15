# Lab 05: Pipeline Security Gates
Difficulty: Hard
Time: 75 minutes

## Objective
- Add SAST and secret scanning as a pipeline gate.

## Prerequisites
- CI pipeline in place

## Steps
1) Add a static analysis tool stage.
2) Add a secret scan step.
3) Fail the pipeline on high severity issues.

## Validation
- Pipeline fails when a known issue is introduced.

## Cleanup
- Remove test vulnerabilities from the codebase.