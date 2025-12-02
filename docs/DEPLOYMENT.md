# GitHub Pages Deployment Guide – 5D Intelligence Map

**Version:** 1.0  
**Last Updated:** December 2, 2025

Diese Anleitung beschreibt die Aktivierung und Konfiguration von GitHub Pages für die 5D-Map.

## 📋 Übersicht

Die 5D-Map wird automatisch über GitHub Actions deployed. Der Workflow ist bereits konfiguriert (`.github/workflows/deploy-5d-map.yml`), benötigt aber manuelle Aktivierung in den Repository-Settings.

## 🚀 Schritt-für-Schritt Anleitung

### 1. GitHub Pages aktivieren

1. **Repository öffnen:** https://github.com/karlitos1337/5d
2. **Settings aufrufen:** Klick auf "Settings" (oben rechts)
3. **Pages-Sektion finden:** Scroll zu "Pages" (linke Sidebar unter "Code and automation")
4. **Source konfigurieren:**
   - **Source:** `GitHub Actions` (wichtig: NICHT "Deploy from a branch")
   - Kein Branch-Dropdown sichtbar, wenn "GitHub Actions" aktiv ist

**Screenshot-Referenz:**
```
┌─────────────────────────────────┐
│ GitHub Pages                     │
├─────────────────────────────────┤
│ Build and deployment             │
│                                  │
│ Source: [GitHub Actions ▼]      │
│                                  │
│ ✓ Your site is live at          │
│   https://karlitos1337.github.io/5d/ │
└─────────────────────────────────┘
```

### 2. Workflow triggern

Nach Aktivierung wird der Workflow automatisch bei jedem Push ausgelöst. Für manuelles Deployment:

```bash
# Option A: Push zu main
git push origin main

# Option B: Manueller Trigger (GitHub UI)
# Actions → Deploy 5D-Map → Run workflow
```

### 3. Deployment verifizieren

1. **Actions Tab:** https://github.com/karlitos1337/5d/actions
2. **Workflow-Run finden:** "Deploy 5D-Map to GitHub Pages"
3. **Status prüfen:**
   - ✅ Grüner Haken: Deployment erfolgreich
   - ❌ Roter X: Fehler (siehe Logs)
4. **Live-URL testen:** https://karlitos1337.github.io/5d/

**Expected Logs:**
```
Run Deploy to GitHub Pages
  Deploying to GitHub Pages...
  ✓ Assets uploaded successfully
  ✓ Deployment complete
  URL: https://karlitos1337.github.io/5d/
```

### 4. Custom Domain (Optional)

Für eigene Domain (z.B., `5d-map.reflexionsfabrik.de`):

1. **DNS-Records erstellen:**
   ```
   Type: CNAME
   Name: 5d-map
   Value: karlitos1337.github.io
   ```

2. **GitHub Pages konfigurieren:**
   - Settings → Pages → Custom domain
   - Eingabe: `5d-map.reflexionsfabrik.de`
   - ✅ "Enforce HTTPS" aktivieren

3. **CNAME-Datei erstellen:**
   ```bash
   echo "5d-map.reflexionsfabrik.de" > web/5d-map/CNAME
   git add web/5d-map/CNAME
   git commit -m "chore: add custom domain for GitHub Pages"
   git push
   ```

## 🔧 Workflow-Konfiguration

**Datei:** `.github/workflows/deploy-5d-map.yml`

```yaml
name: Deploy 5D-Map to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'web/5d-map/**'
      - '.github/workflows/deploy-5d-map.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './web/5d-map'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Key Features:**
- **Trigger:** Push zu `main` (nur bei Änderungen in `web/5d-map/`)
- **Manual Trigger:** `workflow_dispatch` erlaubt manuelles Deployment
- **Permissions:** Minimal notwendige Rechte (contents: read, pages: write)
- **Concurrency:** Verhindert parallele Deployments

## 🔒 Sicherheit & Performance

### Content Security Policy (CSP)

GitHub Pages unterstützt **keine** custom HTTP headers. CSP muss via `<meta>` tag implementiert werden:

**Zu `web/5d-map/index.html` hinzufügen:**

```html
<head>
  <!-- Existing meta tags -->
  
  <!-- Content Security Policy -->
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;
    style-src 'self' 'unsafe-inline' https://unpkg.com;
    img-src 'self' data: https://*.tile.openstreetmap.org https://*.wikimedia.org;
    connect-src 'self' https://ourworldindata.org https://api.worldbank.org https://api.github.com;
    font-src 'self' data:;
    frame-src 'none';
    base-uri 'self';
    form-action 'self';
  ">
</head>
```

**Begründung:**
- `script-src`: Leaflet, Chart.js von CDN
- `style-src`: Leaflet CSS
- `img-src`: OpenStreetMap tiles, Wikimedia images
- `connect-src`: OWID, World Bank, GitHub APIs
- `frame-src 'none'`: Kein iframe embedding (Clickjacking-Schutz)

### HTTPS Enforcement

GitHub Pages erzwingt automatisch HTTPS für `*.github.io` Domains. Für Custom Domains:

1. **"Enforce HTTPS" aktivieren** (Settings → Pages)
2. **DNS-Propagierung abwarten** (24-48h)
3. **Let's Encrypt Zertifikat** wird automatisch erstellt

### Caching-Strategie

**Service Worker** (bereits implementiert in `sw.js`):
- **Static Assets:** Cache-first (CSS, JS, Icons)
- **API Responses:** Network-first mit Cache-Fallback
- **CDN Resources:** Stale-while-revalidate

**GitHub Pages Cache-Control:**
- HTML: `max-age=600` (10 Minuten)
- Assets: `max-age=31536000` (1 Jahr, mit hash in filename)

## 🧪 Testing vor Deployment

### Lokaler Test

```bash
# Starte lokalen Server
cd web/5d-map
python3 -m http.server 5500

# Öffne: http://localhost:5500
```

### Service Worker Test

```javascript
// Browser DevTools Console
navigator.serviceWorker.getRegistrations().then(registrations => {
  console.log('Active Service Workers:', registrations.length);
  registrations.forEach(reg => console.log('Scope:', reg.scope));
});

// Cache-Inhalte prüfen
caches.keys().then(keys => {
  console.log('Cache Keys:', keys);
  keys.forEach(key => {
    caches.open(key).then(cache => {
      cache.keys().then(requests => {
        console.log(`${key}: ${requests.length} cached items`);
      });
    });
  });
});
```

### Lighthouse Audit

```bash
# Chrome DevTools: Lighthouse Tab
# Oder via CLI:
npm install -g lighthouse
lighthouse https://karlitos1337.github.io/5d/ --view
```

**Erwartete Scores:**
- **Performance:** 90+
- **Accessibility:** 95+
- **Best Practices:** 100
- **SEO:** 90+
- **PWA:** 100 (nach Installation)

## 🐛 Troubleshooting

### Problem: "404 There isn't a GitHub Pages site here"

**Ursachen:**
1. GitHub Pages nicht aktiviert (siehe Schritt 1)
2. Workflow noch nicht gelaufen
3. Deployment fehlgeschlagen

**Lösung:**
```bash
# 1. Actions prüfen
https://github.com/karlitos1337/5d/actions

# 2. Workflow manuell triggern
# GitHub UI: Actions → Deploy 5D-Map → Run workflow

# 3. Logs prüfen (Fehlerdetails)
```

### Problem: "Mixed Content" Warnings

**Ursache:** HTTP-Ressourcen auf HTTPS-Seite

**Lösung:** Alle Ressourcen via HTTPS laden:
```javascript
// ❌ Bad
const url = 'http://example.com/api';

// ✅ Good
const url = 'https://example.com/api';
```

### Problem: Service Worker nicht registriert

**Ursache:** HTTPS erforderlich (außer localhost)

**Lösung:** Deployment auf GitHub Pages abwarten (automatisch HTTPS)

### Problem: API-Requests blockiert (CORS)

**Ursache:** CORS-Header fehlen auf externer API

**Lösung:** Proxy verwenden (bereits in `owid_proxy.py`):
```bash
# Starte CORS Proxy
cd web/5d-map
python3 owid_proxy.py 5510

# Im Frontend
const url = 'http://localhost:5510/proxy?url=' + encodeURIComponent(originalUrl);
```

**Produktions-Alternative:** Cloudflare Workers oder Vercel Serverless Functions

### Problem: Icons werden nicht angezeigt

**Ursache:** Pfade relativ zu GitHub Pages root

**Lösung:** Relative Pfade in `manifest.json`:
```json
{
  "icons": [
    {"src": "./icons/icon-192x192.png", "sizes": "192x192"}
  ]
}
```

### Problem: Alte Version wird geladen

**Ursache:** Browser-Cache oder Service Worker

**Lösung:**
```javascript
// 1. Hard Refresh im Browser
// Ctrl+Shift+R (Windows/Linux)
// Cmd+Shift+R (macOS)

// 2. Service Worker Cache leeren
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(reg => reg.unregister());
});
caches.keys().then(keys => keys.forEach(key => caches.delete(key)));

// 3. Seite neu laden
window.location.reload(true);
```

## 📊 Monitoring

### GitHub Actions Status Badge

In `README.md` einfügen:

```markdown
[![Deploy 5D-Map](https://github.com/karlitos1337/5d/actions/workflows/deploy-5d-map.yml/badge.svg)](https://github.com/karlitos1337/5d/actions/workflows/deploy-5d-map.yml)
```

### Uptime Monitoring

**UptimeRobot** (kostenlos, 50 Monitors):

1. Account erstellen: https://uptimerobot.com
2. Monitor hinzufügen:
   - **Type:** HTTP(s)
   - **URL:** https://karlitos1337.github.io/5d/
   - **Interval:** 5 Minuten
3. Alert via Email/Slack/Webhook

### Analytics (Optional)

**Plausible Analytics** (privacy-friendly, GDPR-compliant):

```html
<!-- In web/5d-map/index.html -->
<script defer data-domain="karlitos1337.github.io" src="https://plausible.io/js/script.js"></script>
```

**Self-hosted Alternative:** Matomo (Open Source)

## 🔄 Update-Workflow

### Reguläre Updates

```bash
# 1. Änderungen in web/5d-map/ machen
vim web/5d-map/index.html

# 2. Lokal testen
cd web/5d-map && python3 -m http.server 5500

# 3. Commit + Push
git add web/5d-map/
git commit -m "feat(map): add new feature"
git push origin main

# 4. Deployment automatisch (GitHub Actions)
# 5. Verifizieren: https://karlitos1337.github.io/5d/
```

### Breaking Changes

Bei strukturellen Änderungen (z.B., Ordner-Umbenennung):

```bash
# 1. Workflow-Pfad anpassen
vim .github/workflows/deploy-5d-map.yml

# Change:
# path: './web/5d-map'
# To:
# path: './web/new-path'

# 2. Commit + Push
git add .github/workflows/deploy-5d-map.yml
git commit -m "chore: update deployment path"
git push
```

### Rollback

Bei fehlerhaftem Deployment:

```bash
# 1. Zu letztem funktionierenden Commit zurück
git revert HEAD
git push origin main

# 2. Oder: Spezifischen Commit wiederherstellen
git log --oneline  # Finde funktionierenden Commit
git revert <commit-hash>
git push origin main
```

## 📞 Support

- **GitHub Issues:** https://github.com/karlitos1337/5d/issues
- **GitHub Pages Docs:** https://docs.github.com/pages
- **Actions Docs:** https://docs.github.com/actions

---

**Maintainer:** 5D Intelligence Team  
**Last Reviewed:** December 2, 2025
