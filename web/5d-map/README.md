# 5D‑Weltkarte (Leaflet MVP)

Interaktive 5D‑Weltkarte mit Heatmap (Status Quo), IMP‑Choropleth, Legende und Schul‑Markern.

## Features
- Status‑Quo‑Heatmap: Live‑Daten aus OWID (Depression, %) und World Bank (Dropout, %)
- IMP‑Choropleth: Proxy‑basierter IMP (A×IM×R×SP×Au) inkl. Legende, Popups & WGI‑Normalisierung
- Marker‑Layer: Alternative Schulen aus `data/schools.json`
- Client‑Caching (LocalStorage, 1h TTL) mit Fallbacks
- Zeitreise‑Layer: Jahresauswahl für historische Heatmaps (Depression/Dropout)
 - Optional: OWID Proxy (`owid_proxy.py`) für CORS‑freie CSV‑Fetches
 - Validierung (Ringe): Länder mit externer Validierung aus `data/validation.json` (`validatedISO3`)
 - Quellen (Marker): Anzahl/Kategorien pro Land aus `data/validation.json` (`items[].iso3`)

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

## Zeitreise
- Slider zeigt verfügbare Jahre (vereinigte Menge aus Depression & Dropout Serien).
- Werte pro Jahr werden direkt aus den Originalreihen extrahiert (kein Imputing; fehlende Werte werden ignoriert).
- Intensität pro Jahr: Mittel der vorhandenen Prozentwerte (Depression, Dropout) / 100.
- Fallback: Ist für ein Land ein Wert im gewählten Jahr nicht vorhanden, wird nur der vorhandene genutzt; fehlen beide → Land entfällt.

## Baseline (Fester Ausgangswert)
Die Datei `data/baseline.json` enthält einen Snapshot (Latest-Werte) für Depression, Dropout und WGI‑Indikatoren. Beim Laden:
- Fehlende Live-Werte werden mit Baseline aufgefüllt (live Daten haben Vorrang).
- Popups kennzeichnen Werte mit dem Hinweis "Baseline aktiviert".
- Aktualisierung: Neue Baseline erzeugen und Datei ersetzen.

Update-Workflow:
```bash
git add web/5d-map/data/baseline.json
git commit -m "chore: update baseline snapshot"
```

## Lokal starten
```bash
cd web/5d-map
python3 -m http.server 5500
# Öffnen: http://localhost:5500
```

OWID Proxy (optional, anderer Port):
```bash
cd web/5d-map
python3 owid_proxy.py 5510
# Frontend nutzt automatisch zuerst http://localhost:5510/proxy/depression-prevalence.csv
```

Schnelltest:
1. "Status Quo" → Heatmap erscheint ohne Fehler in Konsole.
2. "IMP-Score" → Choropleth + Legende sichtbar, Popup zeigt WGI Rohwerte.
3. Netzwerk offline schalten → letztes Caching (<=1h) weiter nutzbar.
4. "Zeitreise" aktivieren → Slider bewegt sich; Jahr ändert Heatmap.

## Struktur
```
web/5d-map/
├─ index.html
├─ styles.css
├─ app.js
├─ README.md
├─ data/
│  ├─ schools.json
│  ├─ countries.json
│  └─ validation.json
└─ modules/
  ├─ api-fetcher.js   # Datenbeschaffung (OWID/WB/WGI/validation) + Caching
   ├─ map-renderer.js  # Leaflet Grundsetup
  ├─ layers.js        # Heatmap, IMP‑Choropleth, Legenden, Marker, Validierungsringe
   └─ popups.js        # Popups (Schulen, IMP)
```

## Nächste Schritte
- Zeitreise‑Layer (Jahres‑Slider, historische Reihen)
- Weitere Proxies für R/SP/Au prüfen und dokumentieren
- Legenden/Skalen umschaltbar machen (Lin/Log, Quartile)
- Radar‑Chart für IMP‑Dimensionen im Popup (Chart.js Integration)
