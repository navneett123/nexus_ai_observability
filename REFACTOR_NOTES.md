# Refactor notes

## Blocking issue fixed

All service images now declare the runtime identity numerically as `10001:10001`.
The Helm pod and container security contexts explicitly use the same UID/GID.
This resolves kubelet's `runAsNonRoot` rejection of the named `appuser` image user.

## Reliability improvements

- Added startup probes so liveness/readiness checks do not interfere with initial startup.
- Kept the root filesystem read-only and mounted `/tmp` as writable ephemeral storage.
- Set `HOME=/tmp` to prevent runtime writes under a read-only home directory.
- Added schema validation for the required non-root security settings.
- Added CI checks that reject named/root Docker users and missing UID 10001 Helm settings.

## Repository cleanup

- Removed embedded `.git`, `.venv`, Python caches, and compiled bytecode from the deliverable.
- Removed the obsolete hard-coded `helm/nexus-ai-observability/ingress.yml` manifest.
- Added `.helmignore`.
- Corrected Development/Production namespace documentation to `nexus-dev` and `nexus-prod`.

## Verification completed

- Python test suite: 8 passed.
- Shell scripts: syntax checked with `bash -n`.
- Python sources: compiled successfully.
- Helm CLI was not available in the execution environment, so run `helm lint` in TeamCity as already defined by `scripts/ci/package-helm.sh`.
