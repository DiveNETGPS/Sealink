#!/usr/bin/env bash
set -euo pipefail

# Minimal Raspberry Pi launcher for Sealink CLI test utility.
# Usage:
#   ./run_sealink_cli.sh --port /dev/ttyUSB0 --test ping --tx 0 --rx 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PY_SCRIPT="$REPO_ROOT/resources/uart-getRange.py"
REQ_FILE="$REPO_ROOT/resources/requirements.txt"
VENV_DIR="$SCRIPT_DIR/.venv"

if [[ ! -f "$PY_SCRIPT" ]]; then
  echo "Missing script: $PY_SCRIPT"
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$REQ_FILE" >/dev/null

python "$PY_SCRIPT" "$@"
