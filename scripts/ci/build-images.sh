#!/usr/bin/env bash
set -euo pipefail
: "${RELEASE_VERSION:?Set RELEASE_VERSION}"
: "${REGISTRY_NAMESPACE:?Set REGISTRY_NAMESPACE}"
docker build -f services/dashboard/Dockerfile -t "$REGISTRY_NAMESPACE/nexus-dashboard:$RELEASE_VERSION" .
docker build -f services/model-service/Dockerfile -t "$REGISTRY_NAMESPACE/nexus-model-service:$RELEASE_VERSION" .
docker build -f services/metrics-service/Dockerfile -t "$REGISTRY_NAMESPACE/nexus-metrics-service:$RELEASE_VERSION" .
