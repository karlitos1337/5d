#!/usr/bin/env python3
"""
Manifest Summary Generator
- Scannt `manifest/**` und extrahiert Überschriften (#, ##) sowie erste Absätze
- Erzeugt `manifest_summary.json` (strukturierte Übersicht) und `manifest_summary.md` (lesbar)
- Bewahrt DE-Labels, keine Umbenennungen der Kern-Schemas
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent
MANIFEST_DIR = ROOT / "manifest"
OUT_JSON = ROOT / "manifest_summary.json"
OUT_MD = ROOT / "manifest_summary.md"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")


def extract_sections(text: str) -> Dict[str, Any]:
    lines = text.splitlines()
    sections: List[Dict[str, Any]] = []
    current: Dict[str, Any] | None = None
    para_acc: List[str] = []
    for ln in lines:
        m = HEADING_RE.match(ln.strip())
        if m:
            # flush previous
            if current is not None:
                current["summary"] = " ".join(p.strip() for p in para_acc if p.strip())[:800]
                sections.append(current)
            level = len(m.group(1))
            title = m.group(2).strip()
            current = {"level": level, "title": title}
            para_acc = []
        else:
            if current is not None:
                para_acc.append(ln)
    if current is not None:
        current["summary"] = " ".join(p.strip() for p in para_acc if p.strip())[:800]
        sections.append(current)
    return {"sections": sections}


def summarize_file(path: Path) -> Dict[str, Any]:
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"file": str(path), "error": "read_failed"}
    meta = extract_sections(txt)
    meta["file"] = str(path.relative_to(ROOT))
    # Thematic guess: parent folder names as categories
    parts = path.relative_to(MANIFEST_DIR).parts
    meta["category"] = parts[0] if parts else "root"
    return meta


def main() -> None:
    if not MANIFEST_DIR.exists():
        print("manifest/ nicht gefunden – keine Zusammenfassung erstellt.")
        return
    files = list(MANIFEST_DIR.rglob("*.md"))
    files.sort()
    all_data: List[Dict[str, Any]] = []
    for f in files:
        all_data.append(summarize_file(f))
    OUT_JSON.write_text(json.dumps({"items": all_data}, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown output
    out_lines: List[str] = []
    out_lines.append("# Manifest-Zusammenfassung")
    out_lines.append("")
    out_lines.append("Diese Übersicht wurde automatisch aus den Markdown-Manifests generiert.")
    out_lines.append("")
    # Group by category
    by_cat: Dict[str, List[Dict[str, Any]]] = {}
    for item in all_data:
        by_cat.setdefault(item.get("category", "root"), []).append(item)
    for cat, items in sorted(by_cat.items()):
        out_lines.append(f"## Kategorie: {cat}")
        out_lines.append("")
        for it in items:
            fname = it.get("file", "")
            out_lines.append(f"### Datei: {fname}")
            secs = it.get("sections", [])
            if secs:
                for s in secs:
                    lvl = s.get("level", 1)
                    title = s.get("title", "(ohne Titel)")
                    summary = s.get("summary", "")
                    out_lines.append(f"#### {title} (Ebene {lvl})")
                    if summary:
                        out_lines.append(summary)
                    out_lines.append("")
            else:
                out_lines.append("(Keine Überschriften gefunden)")
                out_lines.append("")
        out_lines.append("")
    OUT_MD.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"manifest_summary.json → {OUT_JSON}")
    print(f"manifest_summary.md → {OUT_MD}")


if __name__ == "__main__":
    main()
