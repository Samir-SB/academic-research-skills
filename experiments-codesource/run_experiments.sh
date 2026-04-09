#!/usr/bin/env bash
set -u

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 configs/exp1.yaml [configs/exp2.yaml ...]"
  exit 1
fi

VENV_PATH="./.venv/bin/activate"
if [ -f "$VENV_PATH" ]; then
  # shellcheck disable=SC1091
  source "$VENV_PATH"
else
  echo "Error: virtual environment not found at $VENV_PATH"
  exit 1
fi

mkdir -p logs
PROCESS_TS="$(date +%Y%m%d_%H%M%S)"
MAIN_LOG="logs/run_experiments_${PROCESS_TS}.log"

run_sequence() {
  local configs=("$@")
  echo "=========================================="
  echo "Experiment sequence started: $(date -u +%F' '%T' UTC')"
  echo "Configs: ${configs[*]}"
  echo "=========================================="

  local cfg
  for cfg in "${configs[@]}"; do
    echo "[START] $(date -u +%F' '%T' UTC') | $cfg"
    python3 train.py --config "$cfg"
    local status=$?
    if [ "$status" -ne 0 ]; then
      echo "[FAIL]  $(date -u +%F' '%T' UTC') | $cfg | exit=$status"
      echo "Sequence aborted on first failure."
      return "$status"
    fi
    echo "[DONE]  $(date -u +%F' '%T' UTC') | $cfg"
  done

  echo "=========================================="
  echo "Experiment sequence completed successfully: $(date -u +%F' '%T' UTC')"
  echo "=========================================="
}

run_sequence "$@" >> "$MAIN_LOG" 2>&1 < /dev/null &
MAIN_PID=$!
disown "$MAIN_PID"

echo "========================================================"
echo "Experiments running in background"
echo "PID: $MAIN_PID"
echo "Main log: $MAIN_LOG"
echo "Monitor: tail -f $MAIN_LOG"
echo "========================================================"
