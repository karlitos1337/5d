## 5D‑Weltkarte – Copilot‑Instruktionen (Pointer)

Diese Datei ist eine kurze Wegweiser‑Fassung. Die vollständige, vom Autor bereitgestellte Spezifikation liegt in der Projektwurzel:

- Volltext: `../../md_copilot_ki_anweisung`

Worum geht es?
- Interaktive, live‑aktualisierte Weltkarte (Leaflet.js + Leaflet.heat + Chart.js)
- Daten: World Bank, Our World in Data, OECD (SDMX), WHO GHO; plus statische Schulstandorte
- Layer: Status‑Quo‑Heatmap, Alternativschulen‑Marker, IMP‑Choropleth, Zeitreise
- Caching: localStorage (1h TTL), Fallbacks bei API‑Ausfall
- 5D‑Designsystem: Farben/Typografie/Layout aus Datei

Empfohlene Ordnerstruktur (separates Frontend‑Modul):
```
web/5d-map/
├── index.html
├── styles.css
├── app.js
├── data/{countries.json, schools.json, cache.json}
└── modules/{api-fetcher.js, map-renderer.js, layers.js, popups.js}
```

Schneller Start (lokal testen):
```
mkdir -p web/5d-map/{data,modules}
printf '<!doctype html>...' > web/5d-map/index.html   # Gerüst laut Volltext
printf '/* styles */' > web/5d-map/styles.css
printf '// app controller' > web/5d-map/app.js
python3 -m http.server -d web/5d-map 8080
# Öffnen: http://localhost:8080
```

Wichtige Guardrails (im 5D‑Repo):
- Dieses Frontend ist unabhängig von der Python‑Pipeline; keine Änderungen an Kern‑JSONs nötig
- API‑Keys werden nicht benötigt; respektiere Rate‑Limits und setze Caching ein
- Keine Backend‑Abhängigkeit hinzufügen (reines Static‑Hosting genügt)

Weiterführend:
- Lies den Volltext `../../md_copilot_ki_anweisung` für detaillierte API‑Endpunkte, Layer‑Logik, Design‑Tokens und die Checkliste.