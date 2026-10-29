#!/bin/bash
# Worker Mistral Workflows — Les Éditions du Discernement (auto-hébergé iMac).
# Charge les clés depuis .env puis lance le worker. Les clés ne sont jamais affichées.

cd "$(dirname "$0")" || exit 1

set -a
# shellcheck disable=SC1091
source ./.env
set +a

export PYTHONPATH=src
export DEPLOYMENT_NAME="editions-workflows-imac"
exec .venv/bin/python src/entrypoints/worker.py >> worker.log 2>&1
