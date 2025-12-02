# Docs index

This folder contains documentation and reference materials used across the 5D project.

Files:

- `SURVEY_SPEC.md` — Full survey specification (canonical code lives in `surveys/`).
- `5d-map/` — Frontend map documentation and static assets.

How to use:

- Read `SURVEY_SPEC.md` for the questionnaire schemas and processing notes.
- Preview the interactive map locally:
```
cd web/5d-map
python3 -m http.server 5500
$BROWSER http://localhost:5500
```

If you add new docs, please update this index.
