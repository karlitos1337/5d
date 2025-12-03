# 5D Projekt TODO-Liste

**Last Updated:** 2025-12-03, 03:31 CET  
**Bewertung:** 84% (B) → Ziel: 91% (A-) in 1-2 Tagen

---

## 🎯 PRIORITÄT 1: WISSENSCHAFTLICHE DOKUMENTATION

**Ziel:** Score 84% (B) → 91% (A-) in 1-2 Tagen

### ✅ Fertiggestellt (2025-12-03, 03:31 CET)
- [x] **VISION.md** (Zentrale Definition, Abgrenzung 7 5D-Modelle)
- [x] **docs/FAQ.md** (15 häufige Fragen mit wissenschaftlichen Antworten)
- [x] **docs/DATENQUELLEN.md** (Transparenz externe Quellen + Google Drive)
- [x] **LITERATUR_INDEX.md** (91 BibTeX-Einträge)
- [x] **GitHub Issue-Templates** (7 Templates: Research, Theory, Ethics, Bug, Feature)
- [x] **ETHIK_MANIFEST.md** (13 Biases, 15+ Abbruchkriterien, Q1-Q4 2026 Checkpoints)
- [x] **CLAIMS_EVIDENCE_MATRIX.md** (40 Behauptungen, 45% Fakt, 40% Hypothese, 15% Spekulation)
- [x] **REFLEXION_LOG.md** (Template für quartalsweise Reflexion)

### 🔴 HÖCHSTE PRIORITÄT (noch offen)
- [ ] **docs/BEWERTUNGSMATRIX_5D.md** erstellen (Wissenschaftliches Scoring-System)
  - Adaptiert von Nuclear NFU Policy Memo Rubric (Tech & National Security, 2025)
  - Kategorien: Framework Position, Analysis, Writing Quality, Sources, Formatting
  - Detaillierte Scoring-Tabellen mit Verbesserungsvorschlägen
  - **Datei:** `docs/BEWERTUNGSMATRIX_5D.md`

- [ ] **docs/UI_INFO_BOXEN.html** erstellen (Evidenzlabels im UI)
  - Tooltips mit wissenschaftlichen Erklärungen (IMP-Faktor, 5D-Modell, Perkolationstheorie)
  - Evidenzlabels (✅⚠️🔮) in Dashboard, 5d-map, bewusstsein_evolution.html
  - "Unsere Forschung"-Badge mit Originalitätsgrad
  - **Datei:** `docs/UI_INFO_BOXEN.html`

### 🟡 Q1 2026 (nächste 3 Monate)
- [ ] **06_synthesen_kompilationen/5d_landschaft.md** (+1 Punkt)
  - 7 alternative 5D-Modelle dokumentieren (AIR-5D, Policy-5D, New Age, etc.)
  - Vergleichskriterien, Tabelle, Begründung

- [ ] **Minimalexperiment 1: Game of Life** (+2 Punkte → 30/35 Analysis)
  - Varianten: koerzitiv (forced seed) vs. nicht-koerzitiv (random init)
  - Metriken: Musterdiversität, Lebensdauer, Entropie

- [ ] **Minimalexperiment 2: Governance-Panel** visualisieren
  - Scatterplot WGI Voice vs. HDI in Dashboard (neue Page oder Page 3)

- [ ] **Minimalexperiment 3: IMP-Calculator** auswerten
  - Auswertungslogik: `analysis/calculate_agency_score.py`
  - Survey-Datensammlung (n > 50)

**Nach 1-4: Score = 91% (A-)** 🎯

---

## 📊 BEWERTUNG (adaptiert von Nuclear NFU Policy Memo Rubric)

**Siehe:** `docs/BEWERTUNGSMATRIX_5D.md` (vollständige Matrix, TODO)

| Kategorie | Punkte | Max | % | Ziel |
|-----------|--------|-----|---|------|
| **Framework Position** | 18/20 | 90% | 18/20 (90%) | ✅ VISION.md fertig |
| **Analysis** | 28/35 | 80% | 30/35 (86%) | FAQ + DATENQUELLEN fertig, Experimente TODO |
| **Writing Quality** | 18/20 | 90% | 18/20 (90%) | ✅ Fertig |
| **Sources** | 15/15 | 100% | 15/15 (100%) | ✅ Fertig |
| **Formatting** | 10/10 | 100% | 10/10 (100%) | ✅ Fertig |
| **GESAMT** | **89/100** | **89%** | **91/100 (91%)** | **A- erreicht nach Experimenten!** |

**Score-Formel:**  
```
Gesamt = (FP × 0.20) + (A × 0.35) + (WQ × 0.20) + (S × 0.15) + (F × 0.10)
```

**Update 2025-12-03:**
- Framework Position: 15 → 18 (+3 Punkte durch VISION.md)
- Analysis: 26 → 28 (+2 Punkte durch FAQ + DATENQUELLEN)
- **Neuer Score: 89% (B+) → Ziel: 91% (A-) nach Experimenten**

---

## Aktuelle Aufgaben (Original, weiterhin gültig)

### Pipeline & Core
- [x] Extractor: Robustheit bei fehlenden Dateien verbessern
- [x] Research Scraper: Rate-Limiting für arXiv optimieren
- [x] GitHub API: Token-Refresh-Logik implementieren

### Dashboard & UI
- [x] Dashboard: Caching-Strategie für große JSON-Dateien
- [x] Weltkarte: Radar-Charts in IMP-Popups (Chart.js)
- [x] Zeitreise-Feature: Baseline-Daten erweitern
- [x] Mobile Optimierung (responsive Grid für Buttons)
- [x] Loading-Overlay mit Spinner
- [x] Button-Tooltips und Accessibility

### Tests & CI
- [x] Pre-Commit Hook einrichten
- [x] Flake8 Linting integrieren
- [x] JSON Validation hinzufügen
- [x] Frontend Unit Tests (Vitest)
- [x] E2E Tests (Playwright)
- [x] Web Vitals Performance Monitoring
- [x] Discord Bot Tests erweitern
- [x] Integration Tests für Pipeline-Schritte
- [x] GitHub Actions für Auto-Deploy

### Deployment
- [x] GitHub Pages Setup für Weltkarte (Workflow ready)
- [ ] GitHub Pages aktivieren (manual step - siehe docs/DEPLOYMENT.md + docs/REMAINING_TASKS.md)
- [x] Service Worker für Offline-Modus
- [x] CSP Headers für Sicherheit
- [x] Cross-Browser Testing (Playwright: Chrome, Firefox, Safari, Mobile)

### Dokumentation
- [x] Copilot Instructions aktualisieren
- [x] User Guide für Weltkarte (docs/USER_GUIDE.md)
- [x] Contributing Guidelines (CONTRIBUTING.md)
- [x] API-Dokumentation für externe Systeme
- [x] Forschungs-Roadmap (TODO_RESEARCH.md)

---

## 📊 Gesamtfortschritt

**Infrastruktur:** 13/15 (87%)  
**Wissenschaft:** 89/100 (89%) → Ziel: 91/100 (91%, A-)  
**Kombiniert:** 90% → Ziel: 93% (A)

---

## Siehe auch

- **TODO_MULTIPAGE.md** – Dashboard-Features, UI/UX, wissenschaftliche Validierung (10/10 Pages fertig, 100%)
- **TODO_RESEARCH.md** – Wissenschaftliche Grundlagen, empirische Testbarkeit, theoretische Kohärenz (85+ Tasks)
- **docs/REMAINING_TASKS.md** – Verbleibende manuelle Schritte (GitHub Pages)
- **docs/BEWERTUNGSMATRIX_5D.md** – Wissenschaftliches Scoring-System (TODO)
- **VISION.md** – Zentrale Definition, Abgrenzung 7 5D-Modelle (✅ Fertig)
- **docs/FAQ.md** – 15 häufige Fragen (✅ Fertig)
- **docs/DATENQUELLEN.md** – Transparenz externe Quellen (✅ Fertig)
- **docs/CLAIMS_EVIDENCE_MATRIX.md** – 40 Behauptungen, Evidenzlabels (✅ Fertig)

---

**Letzte Aktualisierung:** 2025-12-03, 03:31 CET  
**Maintainer:** Siehe [CONTRIBUTING.md](CONTRIBUTING.md)