#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

export RELEASE_VERSION REGISTRY_NAMESPACE
docker compose build --pull
