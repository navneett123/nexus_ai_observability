#!/usr/bin/env bash
set -euo pipefail
VERSION="${1:-}"
if [ -z "$VERSION" ]; then echo "Usage: $0 <TEAMCITY_VERSION>"; exit 1; fi
sudo apt update
sudo apt install -y openjdk-21-jdk wget tar
if ! id teamcity >/dev/null 2>&1; then sudo useradd --system --create-home --home-dir /opt/teamcity-home --shell /bin/bash teamcity; fi
cd /tmp
wget -O TeamCity.tar.gz "https://download.jetbrains.com/teamcity/TeamCity-${VERSION}.tar.gz"
sudo rm -rf /opt/TeamCity
sudo tar xfz TeamCity.tar.gz -C /opt
sudo chown -R teamcity:teamcity /opt/TeamCity /opt/teamcity-home
sudo usermod -aG docker teamcity
echo "Start with: sudo -iu teamcity /opt/TeamCity/bin/runAll.sh start"
