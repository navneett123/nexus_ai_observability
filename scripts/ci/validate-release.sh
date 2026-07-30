#!/usr/bin/env bash
set -Eeuo pipefail

: "${RELEASE_VERSION:?RELEASE_VERSION is required}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE is required}"

if [[ ! "$RELEASE_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]]; then
  echo "RELEASE_VERSION must be a semantic version, got: $RELEASE_VERSION" >&2
  exit 2
fi

if [[ ! "$REGISTRY_NAMESPACE" =~ ^[a-z0-9]+([._-][a-z0-9]+)*$ ]]; then
  echo "Invalid REGISTRY_NAMESPACE: $REGISTRY_NAMESPACE" >&2
  exit 2
fi

if grep -R --line-number --fixed-strings '#{ImageTag}' helm octopus 2>/dev/null; then
  echo "Legacy Octopus ImageTag reference detected" >&2
  exit 3
fi

if grep -R --line-number --fixed-strings 'image.tag=#{Octopus.Release.Number}' helm octopus 2>/dev/null; then
  echo "Image tag must not depend on Octopus release numbering" >&2
  exit 4
fi

printf 'Release contract valid: %s/%s\n' "$REGISTRY_NAMESPACE" "$RELEASE_VERSION"
