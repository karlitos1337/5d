from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "simulations"
OUTDIR.mkdir(parents=True, exist_ok=True)


def write_run(kind: str, params: Dict[str, Any], metrics: Dict[str, Any]) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = {
        "art": kind,
        "parameter": params,
        "metriken": metrics,
        "timestamp": ts,
    }
    fname = OUTDIR / f"{kind}_run_{ts}.json"
    fname.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return fname
