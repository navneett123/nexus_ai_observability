# Octopus deployment contract

Package: `nexus-ai-observability.<release>.tgz`

Helm values files, in order:

1. `values.yaml` from the package
2. `values-dev.yaml` or `values-prod.yaml` from the package
3. `octopus/values-octopus.yaml` with Octopus variable substitution enabled

Deployment namespace:

`#{KubernetesNamespace}`

Required scoped variables:

- `KubernetesNamespace`: `nexus-dev` for Development, `nexus-prod` for Production
- `IngressHost`: `nexus-dev.local` for Development, `nexus.local` for Production

The Octopus release number is the immutable Docker image tag and application version.
