# Nexus AI Observability v2
Clean lab: GitHub -> Native TeamCity -> GHCR -> Octopus Cloud -> k3d -> Helm.

Only TeamCity is installed natively. The application runs as three containers.

Start locally:
```bash
docker compose up --build
```
Open `http://localhost:8000`.
Follow `SETUP.md`.
