#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="${CLUSTER_NAME:-nexus-lab}"
NAMESPACES=("nexus-dev" "nexus-prod")

if k3d cluster list --no-headers 2>/dev/null | awk '{print $1}' | grep -qx "$CLUSTER_NAME"; then
  echo "k3d cluster '$CLUSTER_NAME' already exists; skipping cluster creation."
else
  k3d cluster create "$CLUSTER_NAME" --servers 1 --agents 2
fi

for namespace in "${NAMESPACES[@]}"; do
  kubectl create namespace "$namespace" \
    --dry-run=client \
    --output=yaml | kubectl apply --filename=-
done

kubectl get nodes
kubectl get namespaces nexus-dev nexus-prod
