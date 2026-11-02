#!/usr/bin/env bash
# One-command setup: ./scripts/setup.sh
set -e

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
mkdir -p data logs

echo "Setup complete. Activate with: source venv/bin/activate"
