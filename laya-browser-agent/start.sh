#!/usr/bin/env bash
#
# Start the local inference server.
#
#   ./start.sh                      # LAN, port 8000, Laya router mode
#   ./start.sh --port 8791          # different port
#   ./start.sh --browser            # serve the cklxx/laya-browser fine-tune
#   ./start.sh --model cklxx/laya-browser --subfolder v10s
#   ./start.sh --key secret --lan   # require a bearer token
#
# Everything is passed through to the server as environment variables, so you
# can also just export INFER_* / LAYA_* yourself and run `./start.sh`.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VENV="${VENV:-$ROOT/.venv}"
PY="$VENV/bin/python"

# ---- defaults (overridable by the flags below or a pre-set environment) -----
export INFER_HOST="${INFER_HOST:-0.0.0.0}"     # LAN-reachable by default
export INFER_PORT="${INFER_PORT:-8000}"
export LAYA_DEVICE="${LAYA_DEVICE:-}"          # empty -> auto (cuda > mps > cpu)

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

NEED_LAYA=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)       export INFER_PORT="$2"; shift 2 ;;
    --host)       export INFER_HOST="$2"; shift 2 ;;
    --key)        export INFER_API_KEY="$2"; shift 2 ;;
    --device)     export LAYA_DEVICE="$2"; shift 2 ;;
    --model)      export LAYA_MODEL="$2"; export LAYA_MODE="agent"; shift 2 ;;
    --subfolder)  export LAYA_SUBFOLDER="$2"; shift 2 ;;
    --pool)       export LAYA_POOL="$2"; shift 2 ;;
    --threads)    export LAYA_THREADS="$2"; shift 2 ;;
    --browser)    export LAYA_MODEL="${LAYA_MODEL:-cklxx/laya-browser}"
                  export LAYA_SUBFOLDER="${LAYA_SUBFOLDER:-v10s}"
                  export LAYA_MODE="agent"; shift ;;
    --local)      export INFER_HOST="127.0.0.1"; shift ;;
    --lan)        export INFER_HOST="0.0.0.0"; shift ;;
    --no-preload) export LAYA_PRELOAD="0"; shift ;;
    --recreate)   RECREATE=1; shift ;;
    -h|--help)    usage ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

# ---- virtualenv bootstrap ---------------------------------------------------
if [[ -n "${RECREATE:-}" && -d "$VENV" ]]; then
  echo "[start] removing existing venv at $VENV"
  rm -rf "$VENV"
fi

if [[ ! -x "$PY" ]]; then
  echo "[start] creating virtualenv at $VENV"
  if command -v uv >/dev/null 2>&1; then
    uv venv --python 3.12 "$VENV"
  else
    python3 -m venv "$VENV"
  fi
  NEED_LAYA=1
fi

# Install the package (editable) plus the Laya extra on first run.
if ! "$PY" -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  echo "[start] installing server dependencies"
  if command -v uv >/dev/null 2>&1; then
    uv pip install --python "$PY" -e "$ROOT"
  else
    "$PY" -m pip install -q -e "$ROOT"
  fi
  NEED_LAYA=1
fi

if ! "$PY" -c "import laya" >/dev/null 2>&1; then
  NEED_LAYA=1
fi

if [[ "$NEED_LAYA" == "1" ]]; then
  echo "[start] installing the Laya inference backend (this pulls torch; may take a while)"
  if command -v uv >/dev/null 2>&1; then
    uv pip install --python "$PY" -e "$ROOT[laya]"
  else
    "$PY" -m pip install -q -e "$ROOT[laya]"
  fi
fi

echo "[start] backend=${INFER_BACKEND:-laya} model=${LAYA_MODEL:-convaiinnovations/laya} mode=${LAYA_MODE:-router} host=${INFER_HOST}:${INFER_PORT}"
exec "$PY" -m app.server
