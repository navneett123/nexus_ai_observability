#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

export RELEASE_VERSION REGISTRY_NAMESPACE
DASHBOARD_PORT="${DASHBOARD_PORT:-18000}"
export DASHBOARD_PORT

cleanup() {
  docker compose down -v --remove-orphans
}
trap cleanup EXIT

docker compose up -d --no-build --wait
curl -fsS "http://localhost:${DASHBOARD_PORT}/ready" >/dev/null
curl -fsS "http://localhost:${DASHBOARD_PORT}/api/models" >/dev/null
curl -fsS "http://localhost:${DASHBOARD_PORT}/api/models/supportpilot/dashboard" >/dev/null
echo "Smoke test passed for release ${RELEASE_VERSION}"
