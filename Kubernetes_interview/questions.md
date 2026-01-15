# Kubernetes Interview Question Bank (Mid to Senior)

## Easy
- Q1: What is a Kubernetes pod? Answer outline: smallest deployable unit; one or more containers with shared network/storage.
- Q2: What is the difference between a Deployment and a ReplicaSet? Answer outline: Deployment manages ReplicaSets and rollout history.
- Q3: What is a Service? Answer outline: stable virtual IP and load balancing to pods.
- Q4: What is a namespace? Answer outline: logical isolation and scoping for resources.
- Q5: What is kubelet? Answer outline: node agent that runs pods and reports status.
- Q6: How do you view logs for a pod? Answer outline: `kubectl logs <pod>` or `--previous`.
- Q7: What is the purpose of labels? Answer outline: selection and grouping of resources.
- Q8: What is a ConfigMap? Answer outline: non-secret configuration data.
- Q9: What is a Secret? Answer outline: base64-encoded sensitive data, used as env or volume.
- Q10: What is a readiness probe? Answer outline: gates traffic; not a restart trigger.

## Medium
- Q11: Explain liveness vs readiness vs startup probes. Answer outline: liveness restarts, readiness controls traffic, startup protects long init.
- Q12: What is a PodDisruptionBudget? Answer outline: limits voluntary disruptions to keep availability.
- Q13: How does the scheduler pick a node? Answer outline: filters by resources/taints/affinity, scores candidates.
- Q14: What causes Pods to be Pending? Answer outline: insufficient resources, PVC unbound, taints, selectors.
- Q15: What is a taint and toleration? Answer outline: taint repels pods; toleration allows scheduling.
- Q16: How does rolling update work? Answer outline: replaces pods gradually with maxSurge/maxUnavailable.
- Q17: How do you roll back a Deployment? Answer outline: `kubectl rollout undo` or pin image tag.
- Q18: What is a StatefulSet? Answer outline: stable identity and storage for stateful apps.
- Q19: How do you handle node drains safely? Answer outline: PDBs, readiness probes, drain one node at a time.
- Q20: What is a headless Service? Answer outline: no cluster IP; used for StatefulSet DNS.
- Q21: How do you debug ImagePullBackOff? Answer outline: check tag, registry auth, network.
- Q22: What is the purpose of resource requests and limits? Answer outline: scheduling and enforcement.

## Hard
- Q23: Design a zero-downtime deployment strategy in Kubernetes. Answer outline: rolling or canary, readiness probes, PDBs, traffic shift.
- Q24: How do you prevent noisy neighbor issues? Answer outline: requests/limits, QoS classes, node isolation.
- Q25: How do you troubleshoot intermittent 5xx in a service mesh cluster? Answer outline: check sidecar resources, mTLS, retries, upstream timeouts.
- Q26: How do you enforce policy in Kubernetes? Answer outline: admission controllers, OPA/Gatekeeper, namespace constraints.
- Q27: How do you manage secrets securely at scale? Answer outline: external secrets manager, CSI driver, rotation.
- Q28: How do you design multi-tenant clusters safely? Answer outline: namespaces, RBAC, network policies, resource quotas.
- Q29: How do you handle schema migrations with rolling updates? Answer outline: backwards-compatible changes, expand/contract.
- Q30: How do you debug a slow rollout? Answer outline: check maxUnavailable, probe failures, insufficient resources.
- Q31: How do you size HPA and VPA safely? Answer outline: metrics, min/max, avoid thrash.
- Q32: Explain how DNS works inside Kubernetes. Answer outline: CoreDNS, cluster domain, service discovery.
- Q33: What is an init container and why use it? Answer outline: setup tasks before app container.
- Q34: How do you monitor cluster health? Answer outline: node conditions, control plane metrics, etcd.
- Q35: How do you handle certificate rotation for apiserver? Answer outline: automation, controlled restarts, verify clients.
- Q36: How do you detect and fix config drift? Answer outline: GitOps tools, compare live vs repo, enforce sync.
- Q37: How do you troubleshoot PVC not binding? Answer outline: storage class, access modes, capacity.
- Q38: How do you secure the kubeconfig? Answer outline: least privilege, short-lived creds.
- Q39: How do you perform blue/green in Kubernetes? Answer outline: separate deployments, service selector switch.
- Q40: How do you handle cross-namespace traffic restrictions? Answer outline: network policies and namespace selectors.