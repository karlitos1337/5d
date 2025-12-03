# 5D Projekt - Nächste Schritte

## ✅ Was bereits funktioniert (Stand: 01.12.2025)

### Backend (Python Pipeline)
- ✅ Extractor (`5d_extractor.py`) → `5d_solutions.json`
- ✅ Research Scraper (`5d_research_scraper.py`) → `5d_research_data.json`
- ✅ GitHub API (`5d_github_api.py`) → `5d_github_data.json`
- ✅ Streamlit Dashboards (5 verschiedene UIs)
- ✅ Pydantic-validierte Schemas
- ✅ IMP-Berechnung (models/imp.py)

### Frontend (5D-Weltkarte)
- ✅ 4 interaktive Layer (Status Quo, Schulen, IMP, Zeitreise)
- ✅ Live-Daten-Integration (OWID, World Bank, WGI)
- ✅ Auto-Refresh & Caching (1h TTL)
- ✅ Responsive Design
- ✅ Zeitreise-Slider (2000-2025)

### Quality & CI/CD
- ✅ Pre-Commit Hook mit Tests, Linting, JSON-Validierung
- ✅ GitHub Actions für Python Tests
- ✅ GitHub Pages Deployment Workflow
- ✅ Flake8 Konfiguration
- ✅ TODO-Liste Tracking

### Dokumentation
- ✅ Copilot Instructions (.github/copilot-instructions.md)
- ✅ Map-spezifische Anweisungen (md_copilot_ki_anweisung)
- ✅ README mit Quick Start
- ✅ TODO.md mit strukturierter Aufgabenliste

---

## 🎯 Priorität 1: GitHub Pages Aktivierung

### Schritt 1: GitHub Pages einschalten
1. Gehe zu: https://github.com/karlitos1337/5d/settings/pages
2. Under "Build and deployment":
   - Source: **GitHub Actions** (nicht "Deploy from a branch")
3. Save
4. Warte ~2 Minuten auf Deployment
5. Karte verfügbar unter: **https://karlitos1337.github.io/5d/**

### Schritt 2: Test der Live-Seite
```bash
# Workflow manuell triggern (falls nicht automatisch)
# GitHub → Actions → "Deploy 5D Map to GitHub Pages" → "Run workflow"

# Nach Deployment testen:
curl -I https://karlitos1337.github.io/5d/
# Erwartete Response: 200 OK
```

### Schritt 3: Custom Domain (optional)
Falls du eine eigene Domain hast (z.B. `5d-map.com`):
1. Erstelle `web/5d-map/CNAME` mit Inhalt: `5d-map.com`
2. Bei Domain-Provider: CNAME Record → `karlitos1337.github.io`
3. GitHub Settings → Pages → Custom domain: `5d-map.com`

---

## 🚀 Priorität 2: UX-Verbesserungen

### Task 2.1: Radar-Charts in IMP-Popups
**Datei:** `web/5d-map/modules/popups.js`

Erweitere `createIMPPopup()` mit Chart.js Radar-Chart:
- Zeigt 5 IMP-Komponenten visuell (A, IM, R, SP, Au)
- Canvas mit ID `radar-${country.code}`
- Chart nach 100ms Timeout rendern (DOM muss ready sein)

**Warum wichtig:** Nutzer verstehen IMP-Score besser mit visueller Aufschlüsselung.

### Task 2.2: Mobile Optimierung
**Datei:** `web/5d-map/styles.css`

Media Queries hinzufügen:
```css
@media (max-width: 768px) {
  .controls { grid-template-columns: 1fr 1fr; }
  #map { min-height: 60vh; }
}
```

**Warum wichtig:** ~60% der Nutzer sind auf Mobile.

### Task 2.3: Loading-Overlay
**Dateien:** `web/5d-map/app.js`, `web/5d-map/styles.css`

Zeige Spinner während API-Calls:
- Overlay mit Animation
- "Lade Daten..." Message
- Fade-out nach erfolgreichem Laden

**Warum wichtig:** Besseres Feedback bei langsamen Verbindungen.

---

## 🔧 Priorität 3: Daten-Erweiterungen

### Task 3.1: Mehr Alternative Schulen
**Datei:** `web/5d-map/data/schools.json`

**Recherche-Quellen:**
- Sudbury: https://sudbury.org.uk/schools
- Waldorf: https://www.freunde-waldorf.de/schulen-weltweit/
- Folk High: https://danishfolkhighschools.com/
- Tokkatsu: https://www.mext.go.jp/en/

**Ziel:** Mindestens 50 Schulen (aktuell ~10)

**Format:**
```json
{
  "name": "Neue Schule",
  "type": "sudbury|waldorf|folk-high|tokkatsu",
  "lat": 52.52,
  "lng": 13.40,
  "founded": 2010,
  "students": 100,
  "outcomes": {
    "college": 85,
    "satisfaction": 90
  },
  "detailsLink": "https://..."
}
```

### Task 3.2: Bessere IMP-Proxies
**Datei:** `web/5d-map/modules/api-fetcher.js`

Aktuell nutzen wir WGI-Proxies (RL.EST, VA.EST, GE.EST). Besser:
- **PISA-Daten** für Autonomie (statt 1-dropout)
- **Life Satisfaction** (OWID) für Authentizität
- **V-Dem Participatory Index** für SP

**APIs:**
- PISA: https://www.oecd.org/pisa/data/
- OWID Life Satisfaction: https://ourworldindata.org/grapher/happiness-cantril-ladder.csv
- V-Dem: https://www.v-dem.net/data/

### Task 3.3: Baseline-Daten erweitern
**Datei:** `web/5d-map/data/baseline.json`

Füge mehr historische Jahre hinzu (2000-2025):
- Depression rates
- Dropout rates
- WGI-Indices

**Quelle:** World Bank Historical Data
```bash
curl "https://api.worldbank.org/v2/country/all/indicator/SE.PRM.DROPOUT.ZS?date=2000:2025&format=json&per_page=10000" > baseline_dropout.json
```

---

## 🧪 Priorität 4: Testing & Qualität

### Task 4.1: Frontend-Tests
**Neue Datei:** `web/5d-map/tests/test-app.js`

Jest oder Vitest für JavaScript-Tests:
```javascript
describe('5D Map', () => {
  test('initializes map correctly', () => {
    const map = initMap('map', [0, 0], 2);
    expect(map).toBeDefined();
  });
  
  test('calculates IMP correctly', () => {
    const imp = calculateIMP({a: 0.8, im: 0.9, r: 0.7, sp: 0.6, au: 0.8});
    expect(imp).toBeCloseTo(0.242);
  });
});
```

### Task 4.2: E2E-Tests mit Playwright
**Neue Datei:** `web/5d-map/tests/e2e.spec.js`

```javascript
test('can toggle between layers', async ({ page }) => {
  await page.goto('http://localhost:5500');
  
  await page.click('#layer-schools');
  await expect(page.locator('.school-marker')).toBeVisible();
  
  await page.click('#layer-imp');
  await expect(page.locator('.imp-legend')).toBeVisible();
});
```

### Task 4.3: Performance Monitoring
**Datei:** `web/5d-map/index.html`

Web Vitals messen:
```html
<script type="module">
  import {onCLS, onFID, onLCP} from 'https://unpkg.com/web-vitals?module';
  
  onCLS(console.log);
  onFID(console.log);
  onLCP(console.log);
</script>
```

---

## 📚 Priorität 5: Dokumentation

### Task 5.1: User Guide
**Neue Datei:** `docs/USER_GUIDE.md`

Inhalt:
- Schnellstart
- Layer-Erklärungen (Was zeigt jeder Layer?)
- IMP-Formel erklärt (für Nicht-Mathematiker)
- FAQ (Warum fehlen Länder? Wie aktuell sind Daten?)
- Troubleshooting

### Task 5.2: Contributing Guidelines
**Neue Datei:** `CONTRIBUTING.md`

Inhalt:
- Wie füge ich Schulen hinzu? (Pull Request Template)
- Code-Style Guide
- Testing-Anforderungen
- Review-Prozess

### Task 5.3: API-Dokumentation
**Neue Datei:** `docs/API.md`

Dokumentiere alle genutzten APIs:
- Endpoints
- Rate Limits
- Beispiel-Responses
- Fehlerbehandlung
- Alternative Quellen bei Ausfall

---

## 🎨 Priorität 6: Advanced Features

### Task 6.1: Vergleichs-Modus
**Neue Datei:** `web/5d-map/modules/compare-mode.js`

Feature:
- Button "Vergleichen"
- Nutzer wählt 2 Länder
- Split-Screen mit Radar-Charts
- Tabelle mit Deltas

### Task 6.2: Export-Funktion
**Integration:** `web/5d-map/app.js`

Feature:
- Button "Als PNG exportieren"
- html2canvas für Screenshot
- Download aktueller Kartenansicht
- Optional: PDF mit Metadaten

### Task 6.3: 3D-Visualisierung
**Neue Datei:** `web/5d-map/modules/3d-renderer.js`

Feature:
- Three.js Integration
- Säulen-Darstellung von IMP-Scores
- Rotierbare Weltkugel
- Toggle 2D ↔ 3D

---

## 🔒 Priorität 7: Sicherheit & Performance

### Task 7.1: Service Worker
**Neue Datei:** `web/5d-map/service-worker.js`

Offline-Support:
- Cache Leaflet, Chart.js, eigene JS-Dateien
- Cache API-Responses (1h)
- Fallback zu Cache bei Netzwerk-Ausfall

### Task 7.2: CSP Headers
**Datei:** `web/5d-map/index.html`

Content Security Policy:
```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net;
  connect-src 'self' https://api.worldbank.org https://ourworldindata.org;
">
```

### Task 7.3: Rate Limiting
**Datei:** `web/5d-map/modules/api-fetcher.js`

Klasse `RateLimiter`:
- Max. 5 Requests/Sekunde pro API
- Queue für überschüssige Requests
- Exponential Backoff bei Errors

---

## 📊 Erfolgskriterien

### MVP (Minimum Viable Product) ✅
- [x] 4 Layer funktionieren
- [x] Live-Daten-Integration
- [x] Auto-Refresh
- [x] Responsive Design
- [x] Deployment-Ready

### V1.0 (Next Release)
- [ ] GitHub Pages live
- [ ] 50+ Schulen in Datenbank
- [ ] Radar-Charts in Popups
- [ ] Mobile optimiert
- [ ] User Guide vorhanden

### V1.5 (Zukunft)
- [ ] Vergleichs-Modus
- [ ] Export-Funktion
- [ ] Frontend-Tests (80% Coverage)
- [ ] Service Worker
- [ ] 3D-Modus (Optional)

---

## 🚨 Bekannte Issues

### Issue #1: CORS bei OWID-API
**Problem:** Direct fetch zu OWID CSV blockiert manchmal durch CORS.
**Workaround:** Lokales CSV-Fallback in `data/depression_sample.csv`.
**Lösung:** Proxy-Server oder CORS-Anywhere nutzen.

### Issue #2: WGI-Daten unvollständig
**Problem:** Nicht alle Länder haben WGI-Daten (z.B. kleine Inselstaaten).
**Workaround:** Fallback zu 0.5 (neutral).
**Lösung:** Alternative Governance-Indizes (V-Dem, Freedom House).

### Issue #3: Zeitreise-Baseline limitiert
**Problem:** Baseline nur mit Sample-Daten (10 Länder).
**Workaround:** Funktioniert für Demo.
**Lösung:** Vollständige historische Daten von World Bank laden.

---

## 💡 Ideen für später

### Community-Features
- User können Schulen vorschlagen (GitHub Issues)
- Erfahrungsberichte zu Schulen hinzufügen
- Rating-System für Outcomes

### Analytics
- Heatmap-Änderungen über Zeit (Trend-Analyse)
- Korrelation: IMP-Score vs. Depression
- Prediction: IMP 2030 basierend auf aktuellen Trends

### Gamification
- "Finde die beste Schule in deiner Nähe"
- Quiz: "Erkenne das Land am IMP-Score"
- Challenges: "Verbessere IMP um 0.1 - wie?"

---

## 📞 Support & Feedback

- **GitHub Issues:** https://github.com/karlitos1337/5d/issues
- **Discussions:** https://github.com/karlitos1337/5d/discussions
- **Email:** (optional einfügen)

---

**Letzte Aktualisierung:** 01.12.2025  
**Nächster Review:** 15.12.2025
