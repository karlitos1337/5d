# 5D-Map Benutzerhandbuch

Eine interaktive Weltkarte zur Visualisierung des 5D Intelligence Frameworks mit Live-Daten zu Bildung, mentaler Gesundheit und Governance.

## 🌍 Überblick

Die 5D-Map ist eine clientseitige Web-Anwendung, die globale Bildungs- und Gesundheitsdaten visualisiert. Sie kombiniert:

- **Depression-Daten** (WHO, OWID)
- **Dropout-Raten** (World Bank, OECD)
- **Governance-Indikatoren** (World Bank WGI)
- **Alternative Schulen** (manuell kuratiert)

## 🚀 Schnellstart

### Lokal starten

```bash
cd web/5d-map
python3 -m http.server 5500
```

Dann öffne: http://localhost:5500

### Online Version

Die Karte ist gehostet auf GitHub Pages: https://karlitos1337.github.io/5d/

## 📊 Features

### 1. Status-Quo Heatmap

**Aktivierung:** Button "Status Quo" klicken

**Was wird angezeigt:**
- Rot: Hohe Depression- und Dropout-Raten (kritisch)
- Gelb: Mittlere Werte
- Grün: Niedrige Werte (günstig)

**Berechnung:**
```
Intensität = (Depression% + Dropout%) / 200
```

**Datenquellen:**
- Depression: Our World in Data (OWID) – CSV Export
- Dropout: World Bank Education API

### 2. IMP-Score Choropleth

**Aktivierung:** Button "IMP-Score" klicken

**Was ist der IMP-Score?**

IMP = **I**ntelligence **M**ultiplicative **P**roxy

```
IMP = A × IM × R × SP × Au
```

Wobei:
- **A** (Autonomy) = 1 - (Dropout% / 100)
- **IM** (Intrinsic Motivation) = 1 - (Depression% / 100)
- **R** (Resilience) = normalize(WGI Rule of Law)
- **SP** (Social Participation) = normalize(WGI Voice & Accountability)
- **Au** (Authenticity) = normalize(WGI Government Effectiveness)

**WGI Normalisierung:**
```
normalize(x) = (x + 2.5) / 5
```
(World Governance Indicators liegen zwischen -2.5 und 2.5)

**Farblegende:**
- Dunkelgrün (0.7-1.0): Hoher IMP-Score
- Hellgrün (0.5-0.7): Mittlerer IMP-Score
- Gelb (0.3-0.5): Niedriger IMP-Score
- Rot (0-0.3): Kritischer IMP-Score

**Popup-Informationen:**
Klicke auf ein Land für Details:
- IMP-Gesamt-Score
- Einzelne Dimensionen (A, IM, R, SP, Au)
- Rohe WGI-Werte
- Depression- und Dropout-Raten

### 3. Alternative Schulen (Marker)

**Aktivierung:** Button "Schulen" klicken

**Schultypen:**
- 🟢 **Sudbury-Schulen** (demokratisch, selbstbestimmt)
- 🔵 **Waldorf-Schulen** (ganzheitlich)
- 🟡 **Folk High Schools** (Dänemark, Erwachsenenbildung)
- 🟣 **Tokkatsu-Schulen** (Japan, kooperativ)

**Popup-Informationen:**
- Name der Schule
- Gründungsjahr
- Schülerzahl
- Wichtige Outcomes (z.B. College-Rate, Zufriedenheit)
- Link zu mehr Informationen

### 4. Zeitreise-Feature

**Aktivierung:** Button "Zeitreise" klicken

**Funktion:**
- Slider zeigt verfügbare Jahre (1990-2025)
- Wähle ein Jahr, um historische Daten zu sehen
- Heatmap passt sich automatisch an

**Datenquellen:**
- Depression: OWID historische Zeitreihen
- Dropout: World Bank historische Daten

**Hinweis:**
Nicht alle Länder haben Daten für alle Jahre. Fehlende Werte werden ignoriert.

## 🔧 Technische Details

### Caching-Strategie

**LocalStorage (1h TTL):**
```javascript
const CACHE_TTL = 3600000; // 1 Stunde in ms
```

Die Karte cached:
- OWID Depression CSV
- World Bank Dropout JSON
- WGI JSON

**Vorteile:**
- Schnellere Ladezeiten
- Weniger API-Requests
- Offline-Nutzung (begrenzt)

**Cache leeren:**
```javascript
// In Browser-Konsole:
localStorage.clear();
```

### Baseline-Daten

Datei: `web/5d-map/data/baseline.json`

**Zweck:** Fallback wenn Live-APIs nicht erreichbar sind

**Abdeckung:** 30 Länder (G20 + Nordics + EU)

**Update-Workflow:**
```bash
# Neue Daten einpflegen
vim web/5d-map/data/baseline.json

# Validieren
python3 -m json.tool web/5d-map/data/baseline.json

# Committen
git add web/5d-map/data/baseline.json
git commit -m "chore: update baseline snapshot"
```

### API-Endpoints

**OWID (Depression):**
```
https://ourworldindata.org/grapher/depression-prevalence.csv
```

**World Bank (Dropout):**
```
https://api.worldbank.org/v2/country/{ISO}/indicator/SE.PRM.DROPOUT.ZS?format=json
```

**WGI (Governance):**
```
https://api.worldbank.org/v2/country/{ISO}/indicator/{INDICATOR}?format=json

Indicators:
- RL.EST (Rule of Law)
- VA.EST (Voice & Accountability)  
- GE.EST (Government Effectiveness)
```

### Proxy für CORS (Optional)

Datei: `web/5d-map/owid_proxy.py`

**Problem:** OWID CSV hat manchmal CORS-Restrictions

**Lösung:**
```bash
cd web/5d-map
python3 owid_proxy.py 5510
```

Frontend nutzt automatisch `http://localhost:5510/proxy/...`

## 🎨 Anpassungen

### Farben ändern

Datei: `web/5d-map/styles.css`

```css
/* IMP-Score Farben */
:root {
  --imp-high: #006400;   /* Dunkelgrün */
  --imp-medium: #90ee90; /* Hellgrün */
  --imp-low: #ffff00;    /* Gelb */
  --imp-critical: #ff0000; /* Rot */
}
```

### Legende anpassen

Datei: `web/5d-map/modules/layers.js`

```javascript
const legendLabels = [
  { color: '#006400', label: 'Sehr gut (0.7-1.0)' },
  { color: '#90ee90', label: 'Gut (0.5-0.7)' },
  { color: '#ffff00', label: 'Mittel (0.3-0.5)' },
  { color: '#ff0000', label: 'Kritisch (0-0.3)' }
];
```

### Neue Schulen hinzufügen

Datei: `web/5d-map/data/schools.json`

```json
{
  "name": "Neue Schule",
  "type": "sudbury",
  "lat": 52.5200,
  "lon": 13.4050,
  "founded": 2020,
  "students": 150,
  "outcomes": {
    "college_rate": 0.85,
    "satisfaction": 4.5
  },
  "url": "https://example.com"
}
```

## ❓ FAQ

### Warum sehe ich keine Daten für mein Land?

**Mögliche Gründe:**
1. Keine Daten in OWID/World Bank
2. Land-Code falsch (ISO 3166-1 alpha-3)
3. Cache ist veraltet → `localStorage.clear()`

### Wie aktuell sind die Daten?

- **Depression:** OWID 2023
- **Dropout:** World Bank 2024
- **WGI:** World Bank 2023
- **Baseline:** 2025-12-02

### Kann ich die Karte offline nutzen?

**Teilweise:**
- Mit Cache (1h): Ja
- Ohne Cache: Nur mit Baseline-Daten
- Service Worker (TODO): Vollständig offline

### Wie zitiere ich die Daten?

**Depression:**
```
Our World in Data (2023). Prevalence of Depression.
https://ourworldindata.org/mental-health
```

**Dropout:**
```
World Bank (2024). Education Statistics - Primary Dropout Rate.
https://data.worldbank.org/indicator/SE.PRM.DROPOUT.ZS
```

**WGI:**
```
World Bank (2023). Worldwide Governance Indicators.
https://info.worldbank.org/governance/wgi/
```

## 🐛 Troubleshooting

### Karte lädt nicht

1. Browser-Konsole öffnen (F12)
2. Fehler prüfen:
   - **CORS Error:** Proxy starten (`owid_proxy.py`)
   - **404 Error:** Dateipfade prüfen
   - **JSON Error:** `baseline.json` validieren

### Popup zeigt falsche Daten

```javascript
// Cache leeren
localStorage.clear();
location.reload();
```

### Button reagiert nicht

```javascript
// In Konsole prüfen:
document.querySelectorAll('button').forEach(btn => {
  console.log(btn.textContent, btn.onclick);
});
```

## 🔗 Weiterführende Links

- **Projekt-README:** `/workspaces/5d/README.md`
- **Map-Architektur:** `/workspaces/5d/web/5d-map/README.md`
- **Formeln:** `/workspaces/5d/formeln/`
- **IMP-Berechnung:** `/workspaces/5d/models/imp.py`

## 📝 Changelog

**Version 2.1 (2025-12-02)**
- ✅ 30 Länder Baseline-Daten
- ✅ Zeitreise-Feature
- ✅ IMP-Legende erweitert

**Version 2.0 (2025-12-01)**
- ✅ IMP-Score Choropleth
- ✅ WGI-Integration
- ✅ Radar-Charts in Popups

**Version 1.0 (2025-11-15)**
- ✅ Status-Quo Heatmap
- ✅ Schulen-Marker
- ✅ Caching

---

**Feedback & Support:** GitHub Issues oder [reflexionsfabrik.de](https://reflexionsfabrik.de)
