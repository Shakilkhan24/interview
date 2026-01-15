# Lab 05: PDB and Node Drain
Difficulty: Hard
Time: 75 minutes

## Objective
- Use PodDisruptionBudget to keep availability during drain.

## Prerequisites
- Cluster with multiple nodes

## Steps
1) Create a Deployment with 3 replicas.
2) Apply a PDB with `minAvailable: 2`.
3) Drain one node and observe pod eviction behavior.

```bash
kubectl drain <node> --ignore-daemonsets
kubectl get pdb
```

## Validation
- At least 2 pods remain available.

## Cleanup
- Uncordon the node and remove PDB.