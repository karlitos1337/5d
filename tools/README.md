# Tools & Utility Scripts

**Last Updated:** 2025-12-03  
**Purpose:** Hilfsskripte für Wartung, Migration, Debugging

---

## 📋 Scripts

### Data Processing
- **`apply_resonance_mapping.py`** - Wendet Resonanz-Mapping auf IMP-Scores an
- **`merge_external_solutions.py`** - Merged externe Lösungen (JSON)
- **`manifest_reorganize.py`** - Reorganisiert Manifest-Dateien
- **`manifest_summary.py`** - Erstellt Manifest-Zusammenfassungen

### Migration
- **`migrate_v1_to_v2.py`** - Migriert Dashboard v1 → v2

### Debugging
- **`debug_dashboard.sh`** - Diagnostik-Script für Dashboard-Probleme

---

## 🛠️ Usage

**Resonanz-Mapping anwenden:**
```bash
python tools/apply_resonance_mapping.py --input data/5d_solutions.json --output data/processed/solutions_mapped.json
```

**Externe Lösungen mergen:**
```bash
python tools/merge_external_solutions.py --external solutions_external.json --output data/5d_solutions.json
```

**Manifest reorganisieren:**
```bash
python tools/manifest_reorganize.py --manifest manifest/ --output manifest_summary.json
```

**Dashboard debuggen:**
```bash
bash tools/debug_dashboard.sh
```

---

## 📚 Siehe auch
- [MANIFEST.md](../MANIFEST.md) - Manifest-Struktur
- [TODO.md](../TODO.md) - Projektplanung
- [CHANGELOG.md](../CHANGELOG.md) - Änderungshistorie
