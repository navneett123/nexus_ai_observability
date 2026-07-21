#!/usr/bin/env bash
set -euo pipefail
docker compose up --build -d
trap 'docker compose down -v' EXIT
for _ in $(seq 1 40); do
  if curl -fsS http://localhost:8000/ready >/dev/null 2>&1; then
    curl -fsS http://localhost:8000/api/models >/dev/null
    curl -fsS http://localhost:8000/api/models/supportpilot/dashboard >/dev/null
    echo "Smoke test passed"; exit 0
  fi
  sleep 3
done
docker compose logs; exit 1
