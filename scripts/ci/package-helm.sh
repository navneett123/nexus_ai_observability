#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"

CHART_DIR="${CHART_DIR:-helm/nexus-ai-observability}"
OUTPUT_DIR="${OUTPUT_DIR:-dist}"

mkdir -p "$OUTPUT_DIR"
helm lint "$CHART_DIR" \
  --set image.tag="$RELEASE_VERSION" \
  --set config.appVersion="$RELEASE_VERSION" \
  --set config.octopusRelease="$RELEASE_VERSION"

helm package "$CHART_DIR" \
  --destination "$OUTPUT_DIR" \
  --version "$RELEASE_VERSION" \
  --app-version "$RELEASE_VERSION"
