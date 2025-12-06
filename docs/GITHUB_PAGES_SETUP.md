# GitHub Pages Deployment Setup

## 🚀 Automatisches Deployment

Die 5D-Map wird automatisch bei jedem Push nach `main` auf GitHub Pages deployed:

### Workflow: `.github/workflows/deploy-map.yml`
- **Trigger**: Push nach `main` in `web/5d-map/**`
- **Deployment**: `web/5d-map/` → GitHub Pages
- **URL**: https://karlitos1337.github.io/5d/ (nach Aktivierung)

---

## ⚙️ GitHub Pages Aktivierung

### Schritt 1: Repository Settings
1. Gehe zu: https://github.com/karlitos1337/5d/settings/pages
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` → Folder: `/(root)` oder `/docs`
4. **Alternative**: GitHub Actions (empfohlen für CI/CD)

### Schritt 2: Workflow Permissions
1. Gehe zu: https://github.com/karlitos1337/5d/settings/actions
2. **Workflow permissions**: `Read and write permissions`
3. ✅ Aktiviere: `Allow GitHub Actions to create and approve pull requests`

---

## 📁 Deployment Strategien

### Option A: `docs/` Folder (Aktuell)
```yaml
# .github/workflows/deploy-map.yml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: './docs/5d-map'
```

**Vorteile:**
- Dokumentation und Map zusammen
- Keine Branch-Verwaltung nötig
- CI/CD über GitHub Actions

**Setup:**
```bash
# Sync web/ → docs/ vor jedem Deployment
cp -r web/5d-map/* docs/5d-map/
git add docs/5d-map/
git commit -m "Update map for GitHub Pages"
git push
```

### Option B: `gh-pages` Branch (Alternative)
```yaml
- name: Deploy to gh-pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./web/5d-map
```

**Vorteile:**
- Saubere Trennung von Source und Deployed Content
- Automatisches Branch Management

---

## 🔄 CI/CD Pipeline

### Aktueller Flow:
```
main Branch Push
    ↓
GitHub Actions Workflow Trigger (.github/workflows/deploy-map.yml)
    ↓
Checkout Code (actions/checkout@v4)
    ↓
Setup Pages (actions/configure-pages@v4)
    ↓
Upload Artifact (actions/upload-pages-artifact@v3)
    ↓
Deploy to Pages (actions/deploy-pages@v4)
    ↓
Live: https://karlitos1337.github.io/5d/
```

### Map Update Workflow:
```bash
# 1. Ändere web/5d-map/
vim web/5d-map/data/baseline.json

# 2. Sync nach docs/ (optional, wenn docs/ als Source)
cp -r web/5d-map/* docs/5d-map/

# 3. Commit & Push
git add web/5d-map/ docs/5d-map/
git commit -m "Update 5D Map: neue IMP-Daten Deutschland"
git push

# 4. GitHub Actions deployed automatisch
# Workflow Run: https://github.com/karlitos1337/5d/actions
```

---

## 🧪 Lokaler Test vor Deployment

### HTTP Server (Python)
```bash
cd web/5d-map
python3 -m http.server 5500
# → http://localhost:5500
```

### Makefile Target
```bash
make serve-map
# → http://localhost:5500
```

### Playwright Tests (CI)
```bash
cd web/5d-map
npm install
npm test
# Tests: tests/map.spec.js
```

---

## 📊 Dashboard Deployment (Streamlit)

Die Streamlit App (`5d_dashboard.py`) kann **nicht** auf GitHub Pages deployed werden (Python Server benötigt).

### Optionen:
1. **Streamlit Community Cloud** (empfohlen)
   - URL: https://share.streamlit.io/
   - Deploy: `streamlit run 5d_dashboard.py`
   - Repository: https://github.com/karlitos1337/5d
   - Branch: `main`
   - Python: 3.12

2. **Heroku** (Python-fähig)
   ```bash
   heroku create 5d-dashboard
   git push heroku main
   ```

3. **Railway.app** (moderne Alternative)
   - Auto-detect `requirements.txt`
   - Deploy from GitHub

---

## 🔗 URLs (nach Aktivierung)

| Resource | URL | Status |
|----------|-----|--------|
| 5D-Map (Static) | https://karlitos1337.github.io/5d/ | ⏳ Pending |
| Dashboard (Streamlit) | TBD (Streamlit Cloud) | ⏳ Pending |
| Repository | https://github.com/karlitos1337/5d | ✅ Live |
| Workflows | https://github.com/karlitos1337/5d/actions | ✅ Live |

---

## ✅ Checkliste

- [x] `.github/workflows/deploy-map.yml` erstellt
- [x] `docs/5d-map/` mit `web/5d-map/` synchronisiert
- [ ] GitHub Pages aktiviert (Settings → Pages)
- [ ] Workflow Permissions gesetzt (Actions → Settings)
- [ ] Erster erfolgreicher Workflow Run
- [ ] Map erreichbar unter https://karlitos1337.github.io/5d/
- [ ] Streamlit Dashboard auf Streamlit Cloud deployed

---

## 🐛 Troubleshooting

### Problem: 404 auf GitHub Pages
**Lösung:** Prüfe `index.html` im Root von `docs/5d-map/`
```bash
ls -la docs/5d-map/index.html
```

### Problem: Workflow Failed
**Lösung:** Prüfe Permissions
```bash
# https://github.com/karlitos1337/5d/settings/actions
# → "Read and write permissions" aktivieren
```

### Problem: Assets nicht geladen (CSS/JS)
**Lösung:** Prüfe relative Pfade in `index.html`
```html
<!-- ✅ Correct -->
<link rel="stylesheet" href="styles.css">

<!-- ❌ Wrong -->
<link rel="stylesheet" href="/styles.css">
```

---

## 📚 Referenzen

- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Leaflet + GitHub Pages Tutorial](https://leafletjs.com/examples/quick-start/)
