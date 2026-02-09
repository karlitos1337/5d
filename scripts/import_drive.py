#!/usr/bin/env python3
"""
Import Google Drive folder contents into the repository as a data source.

Usage:
  python scripts/import_drive.py --folder "https://drive.google.com/drive/folders/<ID>" [--out drive_import]  # noqa: E501

Requires:
  pip install gdown

Mapping rules (best‑effort, non‑destructive):
  - 03_philosophie_epistemologie/*.md  → 03_philosophie_epistemologie/
  - 06_synthesen_kompilationen/*.md    → 06_synthesen_kompilationen/
  - web/5d-map/data/*.json             → web/5d-map/data/
  - 07_daten_analysen/*.bib            → 07_daten_analysen/
  - Other files                        → drive_import/ (keine Überschreibung)

This script is safe-by-default: it will not overwrite existing files unless --force is provided.
"""

import argparse
import shutil
import sys
from pathlib import Path


def ensure_gdown():
    try:
        import gdown  # noqa: F401

        return True
    except Exception:
        print("gdown not installed. Install via: pip install gdown", file=sys.stderr)
        return False


def download_folder(url: str, out_dir: Path) -> Path:
    import gdown

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Drive folder → {out_dir}")
    gdown.download_folder(url=url, output=str(out_dir), quiet=False, use_cookies=False)
    return out_dir


def safe_copy(src: Path, dst: Path, force: bool = False):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not force:
        print(f"Skip (exists): {dst}")
        return
    print(f"Copy: {src} → {dst}")
    shutil.copy2(src, dst)


def apply_mapping(root: Path, force: bool = False):
    # Walk all files and map by simple heuristics
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        rel_str = str(rel)

        # Philosophy
        if "03_philosophie_epistemologie" in rel_str and p.suffix.lower() == ".md":
            dst = Path("03_philosophie_epistemologie") / p.name
            safe_copy(p, dst, force)
            continue

        # Syntheses
        if "06_synthesen_kompilationen" in rel_str and p.suffix.lower() == ".md":
            dst = Path("06_synthesen_kompilationen") / p.name
            safe_copy(p, dst, force)
            continue

        # Web map data
        if (
            "web" in rel.parts or "5d-map" in rel.parts or "map" in rel.parts
        ) and p.suffix.lower() == ".json":
            dst = Path("web/5d-map/data") / p.name
            safe_copy(p, dst, force)
            continue

        # BibTeX sources
        if p.suffix.lower() == ".bib" and (
            "07_daten_analysen" in rel_str or "bib" in p.name.lower()
        ):
            dst = Path("07_daten_analysen") / p.name
            safe_copy(p, dst, force)
            continue

        # Default: keep under drive_import mirror
        mirror = Path("drive_import") / rel
        mirror.parent.mkdir(parents=True, exist_ok=True)
        if not mirror.exists() or force:
            print(f"Mirror: {p} → {mirror}")
            shutil.copy2(p, mirror)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True, help="Google Drive folder URL")
    ap.add_argument("--out", default="drive_import", help="Local download directory")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    if not ensure_gdown():
        sys.exit(1)

    out_dir = download_folder(args.folder, Path(args.out))
    apply_mapping(out_dir, force=args.force)
    print("Done. Review changes and run validators:")
    print("  pytest tests/ -k 'metadata|world_map_data' -v")


if __name__ == "__main__":
    main()
