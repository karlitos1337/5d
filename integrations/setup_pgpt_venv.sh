#!/usr/bin/env bash
set -euo pipefail

# Setup a Python 3.11 virtualenv for PrivateGPT under .venv-pgpt
# Installs a minimal dependency set to run the 5d-minimal profile (mock LLM + Chroma + HF embeddings).
# Usage:
#   bash integrations/setup_pgpt_venv.sh
# After setup:
#   PGPT_PROFILES=5d-minimal bash integrations/private_gpt_5d.sh all

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENV_DIR="$ROOT_DIR/.venv-pgpt"

# Resolve Python interpreter (prefer 3.11, fallback to system python)
PY_CMD="python3.11"
if ! command -v python3.11 >/dev/null 2>&1; then
  echo "[WARN] Python 3.11 nicht gefunden. Fallback auf System-Python ($(python3 -V 2>/dev/null || echo unbekannt))" >&2
  echo "       PrivateGPT ist offiziell für Python 3.11 freigegeben. Der Fallback funktioniert meist mit dem Minimal-Profil (mock LLM + chroma)." >&2
  PY_CMD="python3"
fi

# Create venv if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Erzeuge Virtuelle Umgebung unter $VENV_DIR ($($PY_CMD -V))..."
  "$PY_CMD" -m venv "$VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# Upgrade packaging tools
"$VENV_PY" -m pip install --upgrade pip setuptools wheel

# Install minimal runtime deps
"$VENV_PIP" install \
  fastapi uvicorn injector python-multipart \
  "gradio==4.44.0" \
  chromadb \
  "llama-index-core>=0.13,<0.15" \
  llama-index-embeddings-huggingface \
  llama-index-vector-stores-chroma \
  sentence-transformers \
  einops \
  watchdog

# Install PrivateGPT repo (editable) for app entrypoint
pushd "$ROOT_DIR/private-gpt-main" >/dev/null
"$VENV_PIP" install -e . || true
popd >/dev/null

cat <<EOF

[OK] .venv-pgpt eingerichtet.

Starten (Minimal-Profil):
  PGPT_PROFILES=5d-minimal bash integrations/private_gpt_5d.sh all

Nur Ingestion:
  PGPT_PROFILES=5d-minimal bash integrations/private_gpt_5d.sh ingest

Nur Server:
  PGPT_PROFILES=5d-minimal bash integrations/private_gpt_5d.sh serve 5d-minimal

EOF
