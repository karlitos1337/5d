#!/usr/bin/env python3
"""
Merge External 5D Solutions
---------------------------
Sammelt zusätzliche Muster aus eingebundenen Submodules unter ./external/ und merged sie
mit den Kernlösungen, ohne bestehende Keys zu überschreiben.

Strategie:
- Kern: liest bestehende '5d_solutions.json'
- External Scan: durchsucht rekursiv Markdown-Dateien unter:
    external/system-genesis
    external/resonance-formulas
- Extrahiert einfache Kandidaten (Projekte / ROI / Pilots + Resonanz-/Genesis-Begriffe)
- Präfixt neue Felder: ext_genesis_projects, ext_resonanz_terms, ext_resonanz_raw
- Schreibt:
    solutions_external.json (nur externe Extraktion)
    5d_solutions_merged.json (kombiniert)

Nicht-invasiv: Originaldateien bleiben unverändert.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

EXTERNAL_PATHS = [
    Path("external/system-genesis"),
    Path("external/resonance-formulas")
]

PROJECT_PATTERN = re.compile(r"(Bäckerei|Garten|Imkerei|Holz|Kräuter)", re.I)
ROI_PATTERN = re.compile(r"ROI\s*:?\s*(\d+[.,]?\d*)", re.I)
PILOT_PATTERN = re.compile(r"Pilot\s*:?\s*(\d+)", re.I)
RESONANCE_TERMS = ["Resonanz", "Schwingung", "Frequenz", "Amplitude", "Kohärenz"]
GENESIS_TERMS = ["Genesis", "Emergenz", "Autopoiesis", "Selbstorganisation", "Komplexität"]


def scan_external() -> dict:
    data = defaultdict(list)
    for base in EXTERNAL_PATHS:
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            try:
                text = md.read_text(encoding="utf-8")
            except Exception:
                continue
            # Projekte / ROI / Pilots
            for match in PROJECT_PATTERN.findall(text):
                data['ext_genesis_projects'].append(match)
            for match in ROI_PATTERN.findall(text):
                data['ext_genesis_roi'].append(match)
            for match in PILOT_PATTERN.findall(text):
                data['ext_genesis_pilots'].append(match)
            # Resonanz-/Genesis-Begriffe
            found_res = [t for t in RESONANCE_TERMS if t.lower() in text.lower()]
            found_gen = [t for t in GENESIS_TERMS if t.lower() in text.lower()]
            if found_res:
                data['ext_resonanz_terms'].extend(found_res)
                data['ext_resonanz_raw'].append({"file": str(md), "terms": found_res})
            if found_gen:
                data['ext_genesis_terms'].extend(found_gen)
                data['ext_genesis_raw'].append({"file": str(md), "terms": found_gen})
    # Deduplicate simple lists
    for k in list(data.keys()):
        if k.endswith('_projects') or k.endswith('_roi') or k.endswith('_pilots') or k.endswith('_terms'):
            data[k] = sorted(set(data[k]))
    return dict(data)


def load_core() -> dict:
    try:
        with open('5d_solutions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"solutions": {}, "plan": {}}


def merge(core: dict, external: dict) -> dict:
    merged = json.loads(json.dumps(core))  # tiefe Kopie
    merged.setdefault('external', {})
    merged['external'].update(external)  # kein Überschreiben der Top-Level Keys
    return merged


def main():
    external = scan_external()
    with open('solutions_external.json', 'w', encoding='utf-8') as f:
        json.dump(external, f, indent=2, ensure_ascii=False)
    print("💾 solutions_external.json gespeichert")

    core = load_core()
    merged = merge(core, external)
    with open('5d_solutions_merged.json', 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print("💾 5d_solutions_merged.json gespeichert")

    print("📊 Externe Felder:")
    for k, v in external.items():
        if isinstance(v, list):
            print(f"  {k}: {len(v)} Einträge")
        else:
            print(f"  {k}: Objekt")

if __name__ == '__main__':
    main()
