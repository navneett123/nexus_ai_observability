#!/usr/bin/env bash
set -Eeuo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

images=(
  "$REGISTRY_NAMESPACE/nexus-dashboard:$RELEASE_VERSION"
  "$REGISTRY_NAMESPACE/nexus-model-service:$RELEASE_VERSION"
  "$REGISTRY_NAMESPACE/nexus-metrics-service:$RELEASE_VERSION"
)

for image in "${images[@]}"; do
  docker image inspect "$image" >/dev/null
  echo "verified local image: $image"
done

package="dist/nexus-ai-observability-$RELEASE_VERSION.tgz"
test -s "$package"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
tar -xzf "$package" -C "$tmp_dir"
actual_app_version="$(awk -F': *' '$1 == "appVersion" {gsub(/\"/, "", $2); print $2}' "$tmp_dir/nexus-ai-observability/Chart.yaml")"
[[ "$actual_app_version" == "$RELEASE_VERSION" ]] || {
  echo "Chart appVersion mismatch: expected $RELEASE_VERSION, got $actual_app_version" >&2
  exit 5
}

echo "verified chart appVersion: $actual_app_version"
