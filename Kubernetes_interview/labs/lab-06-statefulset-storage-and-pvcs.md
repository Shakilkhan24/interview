# Lab 06: StatefulSet Storage and PVCs
Difficulty: Hard
Time: 90 minutes

## Objective
- Deploy a StatefulSet with persistent storage.

## Prerequisites
- Storage class available in the cluster

## Steps
1) Create a StatefulSet with volumeClaimTemplates.
2) Verify each pod gets its own PVC.
3) Delete a pod and verify PVC persistence.

```bash
kubectl get pvc
kubectl delete pod <stateful-pod>
```

## Validation
- PVCs remain after pod deletion.

## Cleanup
- Delete StatefulSet and PVCs.