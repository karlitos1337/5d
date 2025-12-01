# 5D‑Weltkarte (Leaflet MVP)

Interaktive 5D‑Weltkarte mit Heatmap (Status Quo), IMP‑Choropleth, Legende und Schul‑Markern.

## Features
- Status‑Quo‑Heatmap: Live‑Daten aus OWID (Depression, %) und World Bank (Dropout, %)
- IMP‑Choropleth: Proxy‑basierter IMP (A×IM×R×SP×Au) inkl. Legende und Popups
- Marker‑Layer: Alternative Schulen aus `data/schools.json`
- Client‑Caching (LocalStorage, 1h TTL) mit Fallbacks

## Formeln (Kurz)
- Heatmap‑Intensität: `I = clamp((avg(dep%,dropout%))/100, 0, 1)`
- IMP: `IMP = A × IM × R × SP × Au` mit
  - `A = 1 − dropout/100`
  - `IM = 1 − depression/100`
  - `R = normalize(WGI RL.EST)`, `SP = normalize(WGI VA.EST)`, `Au = normalize(WGI GE.EST)`
  - `normalize(x) = clamp((x+2.5)/5, 0, 1)` für WGI in [−2.5,2.5]

## Lokal starten
```bash
cd web/5d-map
python3 -m http.server 5500
# Öffnen: http://localhost:5500
```

## Struktur
```
web/5d-map/
├─ index.html
├─ styles.css
├─ app.js
├─ README.md
├─ data/
│  ├─ schools.json
│  └─ countries.json
└─ modules/
   ├─ api-fetcher.js   # Datenbeschaffung (OWID/WB/WGI) + Caching
   ├─ map-renderer.js  # Leaflet Grundsetup
   ├─ layers.js        # Heatmap, IMP‑Choropleth, Legende, Marker
   └─ popups.js        # Popups (Schulen, IMP)
```

## Nächste Schritte
- Zeitreise‑Layer (Jahres‑Slider, historische Reihen)
- Weitere Proxies für R/SP/Au prüfen und dokumentieren
- Legenden/Skalen umschaltbar machen (Lin/Log, Quartile)
