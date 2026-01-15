# Lab 02: Jenkins Pipeline as Code
Difficulty: Medium
Time: 60 minutes

## Objective
- Create a Jenkinsfile with build and test stages.

## Prerequisites
- Jenkins instance or local Docker Jenkins

## Steps
1) Create a `Jenkinsfile`.
2) Add stages for build and test.
3) Run the pipeline from Jenkins.

```groovy
pipeline {
  agent any
  stages {
    stage('Build') { steps { sh 'make build' } }
    stage('Test') { steps { sh 'make test' } }
  }
}
```

## Validation
- Jenkins reports a successful pipeline run.

## Cleanup
- Remove job or delete Jenkins workspace if needed.