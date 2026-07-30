# One-time setup

## TeamCity parameters

```text
Build number format       2.1.%build.counter%
env.RELEASE_VERSION       %build.number%
env.REGISTRY_NAMESPACE    navneet78
env.DOCKER_USERNAME        <Docker Hub username>
env.DOCKER_TOKEN           <Docker Hub access token>
env.OCTOPUS_URL            <Octopus URL>
env.OCTOPUS_API_KEY        <sensitive API key>
```

## TeamCity build steps

Use this exact order:

```text
1. ./scripts/ci/validate-release.sh
2. ./scripts/ci/test.sh
3. ./scripts/ci/build-images.sh
4. ./scripts/ci/smoke-test.sh
5. docker login -u "$DOCKER_USERNAME" --password-stdin
6. ./scripts/ci/push-images.sh
7. ./scripts/ci/package-helm.sh
8. Upload dist/nexus-ai-observability-*.tgz to the Octopus built-in feed
9. Create the Octopus release using package version %env.RELEASE_VERSION%
10. Deploy the created release to Development
```

The Octopus release number may be `%env.RELEASE_VERSION%` or an Octopus-generated number. Image selection remains correct because the packaged chart `appVersion` is the image tag.

## Octopus project variables

```text
KubernetesNamespace
  Development = nexus-ai-dev
  Production  = nexus-ai-prod

IngressHost
  Development = nexus-dev.local
  Production  = nexus.local
```

Do not create these variables:

```text
ImageTag
ReleaseVersion
```

## Octopus Helm step

```text
Chart source              Chart inside a package
Chart package             nexus-ai-observability
Namespace                 #{KubernetesNamespace}
Additional values file    octopus/values-octopus.yaml
Additional parameters     <empty>
Reset values              enabled
Wait for resources        enabled
```

Enable variable substitution for `octopus/values-octopus.yaml`.

## k3d verification

```bash
kubectl get pods -n nexus-ai-dev
kubectl get events -n nexus-ai-dev --sort-by=.lastTimestamp
kubectl port-forward service/dashboard 18000:80 -n nexus-ai-dev
```

Open `http://localhost:18000`.
