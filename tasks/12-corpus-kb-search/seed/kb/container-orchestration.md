# Container Orchestration with Kubernetes

## Overview
Kubernetes is the standard for container orchestration. It handles deployment, scaling, and management of containerized applications.

## Key Concepts
- **Pod**: Smallest deployable unit, one or more containers
- **Deployment**: Manages pod replicas and rolling updates
- **Service**: Stable network endpoint for pods
- **Ingress**: External HTTP(S) access to services

## Scaling
- Horizontal Pod Autoscaler (HPA) scales based on CPU/memory
- Vertical Pod Autoscaler (VPA) adjusts resource requests
- Cluster Autoscaler adds/removes nodes

## Configuration
Use ConfigMaps for non-sensitive configuration and Secrets for sensitive data. Mount as environment variables or volumes.

## Health Checks
- **Liveness probe**: Is the container running? (restart if not)
- **Readiness probe**: Is the container ready for traffic?
- **Startup probe**: Has the container finished initializing?

## Resource Management
Set resource requests and limits for every container. Use LimitRange and ResourceQuota to enforce namespace limits.
