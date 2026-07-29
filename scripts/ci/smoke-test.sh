#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

export RELEASE_VERSION REGISTRY_NAMESPACE

cleanup() {
  docker compose down -v --remove-orphans
}
trap cleanup EXIT

docker compose up -d --no-build

for _ in $(seq 1 40); do
  if curl -fsS http://localhost:8000/ready >/dev/null 2>&1; then
    curl -fsS http://localhost:8000/api/models >/dev/null
    curl -fsS http://localhost:8000/api/models/supportpilot/dashboard >/dev/null
    echo "Smoke test passed for release ${RELEASE_VERSION}"
    exit 0
  fi
  sleep 3
done

docker compose logs
exit 1
