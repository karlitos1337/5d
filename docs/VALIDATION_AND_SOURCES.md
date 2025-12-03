# Datenvalidierung & Quellen

Kurzüberblick über Validierungsflüsse, Datenquellen und Pflege.

## CI‑Validierung
- Workflow: `.github/workflows/validate-5d-metadata.yml`
- Prüft: JSON‑Artefakte, Schlüssel‑Konsistenz, Schema‑Konformität
- Lokal:
  ```bash
  make test-map-ci
  # oder:
  pytest -k "metadata or world_map_data" -v --disable-warnings
  ```

## Weltkarte – zusätzliche Layer
- **Validierungsring**: ✔️ Ring um Länder mit verifizierten Daten (`validatedISO3`)
- **Quellen‑Layer**: Marker mit Quellenanzahl/Kategorien (`sourcesByISO3`)

## Datenschemata (Map)
```json
{
  "validatedISO3": ["DEU", "DNK", "JPN"],
  "sourcesByISO3": {
    "DEU": { "count": 12, "categories": ["WHO", "WorldBank", "WGI"] },
    "DNK": { "count": 9, "categories": ["OECD", "WHO"] }
  }
}
```

## Pflege‑Checkliste
- Ergänze BibTeX in `07_daten_analysen/5d-relevant-sources.bib`
- Halte Map‑Daten aktuell: `web/5d-map/data/*.json`
- Prüfe Tests: `make test-map-ci`

## Google Drive als Datenquelle
- Importskript: `scripts/import_drive.py`
- Schnellstart:
  ```bash
  python scripts/import_drive.py --folder "https://drive.google.com/drive/folders/1Kzwry6SfWY_HWx9L5zh52jAR-qdeP1QT?usp=sharing"
  ```
- Automatisch via `start.sh`, wenn `DRIVE_FOLDER` gesetzt ist.
