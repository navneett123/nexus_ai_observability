#!/usr/bin/env bash
set -euo pipefail
k3d cluster create nexus-lab --servers 1 --agents 2
for ns in nexus-ai-dev nexus-ai-prod; do kubectl create namespace "$ns" --dry-run=client -o yaml | kubectl apply -f -; done
kubectl get nodes
