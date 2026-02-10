#!/usr/bin/env bash
set -euo pipefail

RUN_ID=${1:-"$(date -u +%Y%m%dT%H%M%SZ)_queue_glm-4.6v"}
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$BASE_DIR/logs/runs/$RUN_ID"
mkdir -p "$LOG_DIR"

{
  echo "[launch] run_id=$RUN_ID"
  echo "[launch] start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "[launch] base_dir=$BASE_DIR"
  echo "[launch] python=$BASE_DIR/.venv-46v/bin/python"
  "$BASE_DIR/.venv-46v/bin/python" -V
  if [[ -z "${ZAI_API_KEY:-}" ]]; then
    echo "[launch] ZAI_API_KEY=missing"
  else
    echo "[launch] ZAI_API_KEY=set"
  fi
  echo "[launch] cmd=.venv-46v/bin/python -u eval-46v-queue.py --jobs jobs/queue.json"
} >> "$LOG_DIR/runner.log" 2>&1

cd "$BASE_DIR"
exec "$BASE_DIR/.venv-46v/bin/python" -u eval-46v-queue.py --jobs jobs/queue.json >> "$LOG_DIR/runner.log" 2>&1
