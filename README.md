# Nexus AI Observability

Three FastAPI services deployed through TeamCity, Docker Hub, Octopus Deploy, Helm, and k3d.

## Release design

TeamCity owns `RELEASE_VERSION` and uses it for:

- all three Docker image tags;
- the Helm package version;
- the Helm chart `appVersion`;
- the version exposed by each service.

The chart resolves the image tag from `Chart.appVersion`. It does **not** use the Octopus release number as an image tag. This prevents an Octopus release such as `0.0.14` from trying to pull a nonexistent image when the packaged artifact is `2.1.34`.

## Local run

```bash
export RELEASE_VERSION=local
export REGISTRY_NAMESPACE=navneet78
docker compose up --build
```

Open `http://localhost:18000`.

## CI order

```text
Validate Release
Tests
Build Images
Smoke Test
Docker Login
Push Images
Package Helm
Upload Helm Package
Create Octopus Release
Deploy to Development
```

## Octopus contract

The Helm deployment step uses:

- package: `nexus-ai-observability`;
- namespace: `#{KubernetesNamespace}`;
- additional values file: `octopus/values-octopus.yaml`;
- no additional Helm parameters.

Only environment-specific values are stored in Octopus. See `octopus/DEPLOYMENT.md`.
