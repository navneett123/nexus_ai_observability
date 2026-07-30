#!/usr/bin/env bash
set -Eeuo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
CHART_DIR="${CHART_DIR:-helm/nexus-ai-observability}"
OUTPUT_DIR="${OUTPUT_DIR:-dist}"

if [[ ! "$RELEASE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]]; then
  echo "Invalid RELEASE_VERSION: $RELEASE_VERSION" >&2
  exit 2
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

for values_file in values-dev.yaml values-prod.yaml; do
  helm lint "$CHART_DIR" -f "$CHART_DIR/$values_file" \
    --set-string image.tag="$RELEASE_VERSION"
  helm template nexus-ai-observability "$CHART_DIR" \
    -f "$CHART_DIR/$values_file" \
    --set-string image.tag="$RELEASE_VERSION" >/dev/null
done

helm package "$CHART_DIR" \
  --destination "$OUTPUT_DIR" \
  --version "$RELEASE_VERSION" \
  --app-version "$RELEASE_VERSION"

package="$OUTPUT_DIR/nexus-ai-observability-$RELEASE_VERSION.tgz"
test -s "$package"
printf '%s\n' "$package"
