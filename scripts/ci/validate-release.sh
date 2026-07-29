#!/usr/bin/env bash
set -euo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

case "$RELEASE_VERSION" in
  local|latest|"")
    echo "RELEASE_VERSION must be an immutable release identifier, not '$RELEASE_VERSION'" >&2
    exit 1
    ;;
esac

if ! [[ "$RELEASE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]]; then
  echo "RELEASE_VERSION '$RELEASE_VERSION' is not a supported semantic version" >&2
  exit 1
fi

echo "Release inputs validated: ${REGISTRY_NAMESPACE} / ${RELEASE_VERSION}"
