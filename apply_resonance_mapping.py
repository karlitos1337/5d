#!/usr/bin/env python3
"""
Apply Resonance→IMP Mapping (optional, non-invasive)

Ziel: Aus einem strukturierten Mapping (falls vorhanden) und den externen
Lösungen (`solutions_external.json`) einen Vorschlags-Output erzeugen,
der `5d_solutions.json` nicht überschreibt, sondern ergänzend
`5d_solutions_adjusted.json` schreibt.

Erwartete Mapping-Quelle:
- In `mapping_resonance_imp.md` kann ein JSON-Codeblock enthalten sein, z. B.:

```json
{
  "scales": {"A": 1.0, "IM": 1.0, "R": 1.0, "SP": 1.0, "Au": 1.0},
  "adjustments": [
    {"project": "Bäckerei", "delta": {"A": +0.05, "IM": +0.10}},
    {"project": "Garten",   "delta": {"R": +0.08}}
  ],
  "cap": {"min": 0.0, "max": 1.0}
}
```

Wenn kein gültiger JSON-Block gefunden wird, arbeitet das Skript als No‑Op
und schreibt eine minimale Struktur.

Hinweis: Dieses Skript ist bewusst konservativ und ändert keine Kern-Schemas.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent
MAP_MD = ROOT / "mapping_resonance_imp.md"
EXT_JSON = ROOT / "solutions_external.json"
OUT_JSON = ROOT / "5d_solutions_adjusted.json"


def load_json_if_exists(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def extract_mapping_from_md(md_path: Path) -> Dict[str, Any]:
    if not md_path.exists():
        return {}
    try:
        text = md_path.read_text(encoding="utf-8")
        # Suche nach erstem JSON-Codeblock
        m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text)
        if not m:
            return {}
        data = json.loads(m.group(1))
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        return {}


def clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))


def apply_mapping(base: Dict[str, Any], external: Dict[str, Any], mapping: Dict[str, Any]) -> Dict[str, Any]:
    # Ausgangsstruktur: kopiere Basis und lege 'adjusted' ergänzend an
    out: Dict[str, Any] = {
        "base_solutions": base,
        "external": external,
        "adjusted": {
            "notes": "Non-invasive Vorschläge aus mapping_resonance_imp.md",
            "projects": {}
        }
    }

    adjustments = mapping.get("adjustments") or []
    scales = mapping.get("scales") or {}
    cap = mapping.get("cap") or {"min": 0.0, "max": 1.0}
    cmin, cmax = float(cap.get("min", 0.0)), float(cap.get("max", 1.0))

    # Versuche Projektliste aus base zu lesen (nicht vorgeschrieben, daher tolerant)
    base_projects = []
    try:
        base_projects = base.get("solutions", {}).get("Projekte", []) or []
    except Exception:
        base_projects = []

    # Baue Map für schnelle Suche
    adj_by_name: Dict[str, Dict[str, float]] = {}
    for item in adjustments:
        name = str(item.get("project", "")).strip()
        delta = item.get("delta") or {}
        if name:
            adj_by_name[name] = {k: float(v) for k, v in delta.items() if isinstance(v, (int, float))}

    # Vorschläge generieren
    for pj in base_projects:
        pj_name = str(pj)
        deltas = adj_by_name.get(pj_name, {})
        if not deltas:
            continue
        # Skalen anwenden (multiplikative Gewichtung der deltas)
        scaled = {k: float(deltas[k]) * float(scales.get(k, 1.0)) for k in deltas}
        # Cappen
        scaled = {k: clamp(v, -1.0, +1.0) for k, v in scaled.items()}
        out["adjusted"]["projects"][pj_name] = {
            "delta": scaled,
            "cap": {"min": cmin, "max": cmax}
        }

    return out


def main() -> None:
    base = load_json_if_exists(ROOT / "5d_solutions.json", default={})
    external = load_json_if_exists(EXT_JSON, default={})
    mapping = extract_mapping_from_md(MAP_MD)

    if not mapping:
        # No‑Op: schreibe minimale Datei, um Konsumenten nicht zu stören
        out = {
            "base_solutions": base,
            "external": external,
            "adjusted": {
                "notes": "Kein Mapping gefunden – dies ist ein Platzhalter.",
                "projects": {}
            }
        }
        OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print("[apply_resonance_mapping] Kein Mapping gefunden. Platzhalter geschrieben.")
        return

    out = apply_mapping(base, external, mapping)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[apply_resonance_mapping] Vorschläge geschrieben → {OUT_JSON}")


if __name__ == "__main__":
    main()
