# Setup
1. Run `./scripts/install-prerequisites.sh`, log out/in.
2. Find the current TeamCity version on the official download page and run `./scripts/install-teamcity-native.sh <VERSION>`.
3. Start TeamCity with `sudo -iu teamcity /opt/TeamCity/bin/runAll.sh start`.
4. Open `http://localhost:8111`, complete setup, authorize bundled agent, confirm Command Line runner.
5. Verify `sudo -u teamcity docker version`.
6. Test app: `docker compose up --build -d`, then open `http://localhost:8000`.
7. Create fresh GitHub repo `nexus-ai-observability-v2` and push branch `main`.
8. Create TeamCity Build Configuration from the repo.
9. Add parameters:
   - `env.RELEASE_VERSION = 2.0.%build.counter%`
   - `env.REGISTRY_NAMESPACE = ghcr.io/<GITHUB_USER>`
10. Add GHCR registry connection using a PAT with `read:packages` and `write:packages`.
11. Add Command Line steps:
   - `./scripts/ci/test.sh`
   - `./scripts/ci/smoke-test.sh`
   - `./scripts/ci/build-images.sh`
   - `./scripts/ci/push-images.sh`
12. Create k3d with `./scripts/create-k3d.sh`.
13. In Octopus create Space `Platform Labs`, Project `Nexus AI Observability v2`, environments Development and Production, lifecycle Development -> Production approval, target role `nexus-ai`.
14. Install Octopus Kubernetes Agent and assign both environments.
15. Add Octopus variables:
   - `Image.Registry = ghcr.io/<GITHUB_USER>`
   - Development namespace `nexus-ai-dev`, replicas 1/1/1
   - Production namespace `nexus-ai-prod`, replicas 3/2/3
16. Add Helm step with chart path `helm/nexus-ai-observability` and overrides:
```yaml
image:
  registry: #{Image.Registry}
  tag: #{Octopus.Release.Number}
replicas:
  dashboard: #{Dashboard.Replicas}
  modelService: #{Model.Replicas}
  metricsService: #{Metrics.Replicas}
config:
  environmentName: #{Octopus.Environment.Name}
  appVersion: #{Octopus.Release.Number}
  octopusRelease: #{Octopus.Release.Number}
  kubernetesNamespace: #{Kubernetes.Namespace}
```
17. Install Octopus TeamCity plugin, create release `%env.RELEASE_VERSION%`, deploy Development only.
18. Verify:
```bash
kubectl get pods -n nexus-ai-dev
kubectl port-forward service/dashboard 8000:80 -n nexus-ai-dev
```
