package kubernetes.admission

# Deny if container runs as root
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("Container '%v' must run as non-root user", [container.name])
}

# Require resource limits
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.memory
    msg := sprintf("Container '%v' must have memory limits", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits.cpu
    msg := sprintf("Container '%v' must have CPU limits", [container.name])
}

# Require security context
deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg := "Pod must specify runAsNonRoot in security context"
}

# Deny privileged containers
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("Container '%v' must not run in privileged mode", [container.name])
}

# Require read-only root filesystem
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.readOnlyRootFilesystem
    msg := sprintf("Container '%v' must use read-only root filesystem", [container.name])
}

# PCI DSS Compliance: Require SSL/TLS for LoadBalancer services
deny[msg] {
    input.request.kind.kind == "Service"
    input.request.object.spec.type == "LoadBalancer"
    not input.request.object.metadata.annotations["service.beta.kubernetes.io/aws-load-balancer-ssl-cert"]
    msg := "PCI DSS: Load balancers must use SSL/TLS certificates"
}

# HIPAA Compliance: Require encryption at rest
deny[msg] {
    input.request.kind.kind == "PersistentVolumeClaim"
    not input.request.object.metadata.annotations["volume.beta.kubernetes.io/storage-class"]
    msg := "HIPAA: Storage must be encrypted at rest"
}

