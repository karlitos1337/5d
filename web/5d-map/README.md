# 5D‑Weltkarte (Leaflet MVP)

Interaktive 5D‑Weltkarte mit Heatmap (Status Quo), IMP‑Choropleth, Legende und Schul‑Markern.

## Features
- Status‑Quo‑Heatmap: Live‑Daten aus OWID (Depression, %) und World Bank (Dropout, %)
- IMP‑Choropleth: Proxy‑basierter IMP (A×IM×R×SP×Au) inkl. Legende, Popups & WGI‑Normalisierung
- Marker‑Layer: Alternative Schulen aus `data/schools.json`
- Client‑Caching (LocalStorage, 1h TTL) mit Fallbacks

## Formeln (Kurz)
- Heatmap‑Intensität: `I = clamp((avg(dep%,dropout%))/100, 0, 1)`
- IMP: `IMP = A × IM × R × SP × Au` mit
  - `A = 1 − dropout/100`
  - `IM = 1 − depression/100`
  - `R = normalize(WGI RL.EST)` (Rule of Law)
  - `SP = normalize(WGI VA.EST)` (Voice & Accountability)
  - `Au = normalize(WGI GE.EST)` (Government Effectiveness)
  - `normalize(x) = clamp((x+2.5)/5, 0, 1)` für WGI in [−2.5,2.5]
  - Hinweis: WGI sind Governance‑Proxies; echte Bildungs‑/Partizipationsmetriken können später ersetzen.

## Legende
Die IMP‑Legende (unten rechts) gruppiert Intervalle:
| Bereich | Farbe | Bedeutung |
|--------|-------|-----------|
| 0–33%  | Grün  | Relativ günstige Lage |
| 33–66% | Gelb  | Mittel / Übergangszone |
| 66–100%| Rot   | Kritische Aufmerksamkeit (niedriger kombinierter Proxy‑Score) |

Farbcodierung invertiert konventionell „Rot = schlecht“ da IMP auf inversen Risikowerten (Dropout/Depression) basiert.

## Lokal starten
```bash
cd web/5d-map
python3 -m http.server 5500
# Öffnen: http://localhost:5500
```

Schnelltest:
1. "Status Quo" → Heatmap erscheint ohne Fehler in Konsole.
2. "IMP-Score" → Choropleth + Legende sichtbar, Popup zeigt WGI Rohwerte.
3. Netzwerk offline schalten → letztes Caching (<=1h) weiter nutzbar.

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
- Radar‑Chart für IMP‑Dimensionen im Popup (Chart.js Integration)
