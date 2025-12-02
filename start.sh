#!/usr/bin/env bash
set -euo pipefail

# Startskript für die häufigsten Dev‑Workflows:
# 1) Führt die Python‑Pipeline aus (Extractor, Research, GitHub)
# 2) Startet das Streamlit‑Dashboard (im Hintergrund)
# 3) Serviert die statische Web‑Karte unter web/5d-map (Port 5500, im Hintergrund)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "[start.sh] Running full pipeline (this may take a while)..."
python3 "$ROOT_DIR/5d_extractor.py"
python3 "$ROOT_DIR/5d_research_scraper.py"
python3 "$ROOT_DIR/5d_github_api.py"

echo "[start.sh] Starting Streamlit dashboard (background)..."
nohup streamlit run "$ROOT_DIR/5d_dashboard.py" --server.headless true > "$LOG_DIR/streamlit.log" 2>&1 &
STREAMLIT_PID=$!
sleep 1

if [ -d "$ROOT_DIR/web/5d-map" ]; then
  echo "[start.sh] Serving static map at http://localhost:5500 (background)..."
  (cd "$ROOT_DIR/web/5d-map" && nohup python3 -m http.server 5500 > "$LOG_DIR/web_map.log" 2>&1 &)
else
  echo "[start.sh] Warning: web/5d-map not found; skipping static server"
fi

echo ""
echo "[start.sh] Done."
echo "  - Streamlit: http://localhost:8501 (PID: $STREAMLIT_PID)"
echo "  - Map: http://localhost:5500"
echo "  - Logs: $LOG_DIR/streamlit.log, $LOG_DIR/web_map.log"
echo ""
echo "Tip: make executable: chmod +x start.sh && ./start.sh"
