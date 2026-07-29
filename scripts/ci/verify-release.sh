#!/usr/bin/env bash
set -euo pipefail

scripts/ci/validate-release.sh
scripts/ci/test.sh
scripts/ci/build-images.sh
scripts/ci/smoke-test.sh
scripts/ci/package-helm.sh
