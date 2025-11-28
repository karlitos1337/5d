#!/usr/bin/env bash
set -euo pipefail

# PrivateGPT Integration for 5d repo
# - Ingests local folders (manifest, formeln, external resonanz-formulas)
# - Optionally starts PrivateGPT server
#
# Usage:
#   integrations/private_gpt_5d.sh ingest                # only ingest 5d content
#   integrations/private_gpt_5d.sh serve                 # start server (requires prior ingest)
#   integrations/private_gpt_5d.sh all                   # ingest then start server
#   integrations/private_gpt_5d.sh serve 5d-minimal      # start with specific profile
#
# Profile selection:
#   - Default: PGPT_PROFILES=local
#   - Override via env: export PGPT_PROFILES=5d-minimal
#   - Or pass as 2nd arg: integrations/private_gpt_5d.sh serve 5d-minimal
#
# Requirements:
#   - Python env with private-gpt-main deps installed (pip install -e private-gpt-main or python -m pip install . from repo)
#   - For local LLM: set up models according to private-gpt-main/settings-local.yaml (llamacpp or ollama)
#
# Notes:
#   - Server port defaults to 8001 (settings.yaml)
#   - Local ingestion is enabled via env vars here

ACTION=${1:-ingest}
PROFILE_ARG=${2:-}
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
PGPT_DIR="$ROOT_DIR/private-gpt-main"
# Prefer local Python 3.11 venv for PrivateGPT if available
PGPT_VENV="$ROOT_DIR/.venv-pgpt"
if [[ -x "$PGPT_VENV/bin/python" ]]; then
  PY="$PGPT_VENV/bin/python"
else
  PY="python"
fi

if [[ ! -d "$PGPT_DIR" ]]; then
  echo "PrivateGPT directory not found at: $PGPT_DIR" >&2
  exit 1
fi

export PGPT_SETTINGS_FOLDER="$PGPT_DIR"
# Keep default to "local", but allow env/arg override
export PGPT_PROFILES="${PGPT_PROFILES:-local}"  # include settings-local.yaml over default
# If a profile is passed as 2nd arg, use it
if [[ -n "$PROFILE_ARG" ]]; then
  export PGPT_PROFILES="$PROFILE_ARG"
fi
export LOCAL_INGESTION_ENABLED="true"   # enable local ingestion in settings.yaml
# Ensure PrivateGPT repo is on PYTHONPATH for module imports
export PYTHONPATH="$PGPT_DIR:${PYTHONPATH:-}"

# Warn if using unsupported Python version (>=3.12)
PY_VER=$($PY -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null || echo "unknown")
if [[ "$PY_VER" != "unknown" ]]; then
  MAJOR=${PY_VER%%.*}
  MINOR=${PY_VER#*.}
  if [[ "$MAJOR" == "3" && "$MINOR" -ge 12 ]]; then
    echo "[WARN] Python $PY_VER erkannt. PrivateGPT ist für Python 3.11 freigegeben." >&2
    echo "       Bitte richte ein Venv mit Python 3.11 ein: bash integrations/setup_pgpt_venv.sh" >&2
  fi
fi

# Optional: configure Ollama endpoint or other settings via env if needed
# export OLLAMA_API_BASE="http://localhost:11434"

INGEST() {
  echo "[PGPT] Ingesting 5d folders into PrivateGPT vector store..."
  cd "$PGPT_DIR"
  # Ignore common noise
  IGNORED=(".git" "__pycache__" ".pytest_cache" ".DS_Store")
  
  "$PY" scripts/ingest_folder.py "$ROOT_DIR/manifest" --ignored "${IGNORED[@]}" || true
  "$PY" scripts/ingest_folder.py "$ROOT_DIR/formeln" --ignored "${IGNORED[@]}" || true
  if [[ -d "$ROOT_DIR/external/resonance-formulas" ]]; then
    "$PY" scripts/ingest_folder.py "$ROOT_DIR/external/resonance-formulas" --ignored "${IGNORED[@]}" || true
  fi
  if [[ -d "$ROOT_DIR/external/system-genesis" ]]; then
    "$PY" scripts/ingest_folder.py "$ROOT_DIR/external/system-genesis" --ignored "${IGNORED[@]}" || true
  fi
  echo "[PGPT] Ingest completed."
}

SERVE() {
  echo "[PGPT] Starting PrivateGPT FastAPI server..."
  cd "$PGPT_DIR"
  "$PY" -m private_gpt
}

case "$ACTION" in
  ingest)
    INGEST
    ;;
  serve)
    SERVE
    ;;
  all)
    INGEST
    SERVE
    ;;
  *)
    echo "Unknown action: $ACTION" >&2
    exit 2
    ;;
esac
