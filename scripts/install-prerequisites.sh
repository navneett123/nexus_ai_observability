#!/usr/bin/env bash
set -euo pipefail
sudo apt update
sudo apt install -y docker.io git curl unzip python3-venv ca-certificates
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
if ! command -v kubectl >/dev/null; then curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"; chmod +x kubectl; sudo mv kubectl /usr/local/bin/; fi
if ! command -v helm >/dev/null; then curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash; fi
if ! command -v k3d >/dev/null; then curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash; fi
echo "Log out and back in before using Docker without sudo."
