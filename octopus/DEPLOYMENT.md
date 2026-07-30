# Octopus deployment contract

Configure the Helm step once:

- Chart package: `nexus-ai-observability`
- Namespace: `#{KubernetesNamespace}`
- Additional values file: `values-octopus.yaml`
- Structured variable replacement: enabled for `values-octopus.yaml`
- Additional Helm parameters: leave empty

Project variables:

- `KubernetesNamespace` scoped by environment
- `IngressHost` scoped by environment

Do not create `ImageTag` or `ReleaseVersion` variables. The Docker image tag is
resolved from the packaged chart's `appVersion`, stamped by TeamCity from
`RELEASE_VERSION`. Therefore Octopus release `0.0.14` can safely deploy package
`2.1.34`; Kubernetes still pulls image `2.1.34`.
