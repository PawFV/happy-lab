#!/usr/bin/env bash
set -euo pipefail

PI_HOST="${PI_HOST:-happy-core}"
REMOTE_DIR="/home/darkin/happy"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "==> Generating AI vulnerabilities (if API keys are set) ..."
if [ -n "${OPENAI_API_KEY:-}" ] || [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  python3 "$PROJECT_ROOT/infra/scripts/ai_vuln_generator.py" "$PROJECT_ROOT/labs/vulnbank/routes/main.py" || true
  python3 "$PROJECT_ROOT/infra/scripts/ai_vuln_generator.py" "$PROJECT_ROOT/labs/vulnbank/routes/auth.py" || true
  python3 "$PROJECT_ROOT/infra/scripts/ai_vuln_generator.py" "$PROJECT_ROOT/labs/vulnshop/routes/api.js" || true
else
  echo "  Skipping: OPENAI_API_KEY and ANTHROPIC_API_KEY not found."
fi

echo "==> Syncing project to ${PI_HOST}:${REMOTE_DIR} ..."
rsync -avz --delete \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude 'node_modules/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '*.db' \
  --exclude 'uploads/' \
  --exclude '.env' \
  "$PROJECT_ROOT/" "${PI_HOST}:${REMOTE_DIR}/"

echo "==> Building and starting containers on ${PI_HOST} ..."
ssh "$PI_HOST" "cd ${REMOTE_DIR} && docker compose up --build -d"

echo "==> Checking container status ..."
ssh "$PI_HOST" "cd ${REMOTE_DIR} && docker compose ps"

PI_IP=$(ssh "$PI_HOST" 'hostname -I' | awk '{print $1}')
echo ""
echo "Deploy complete."
echo "  VulnBank  → http://${PI_IP}:5000"
echo "  VulnShop  → http://${PI_IP}:3001"
