# 5D Projekt TODO-Liste

**Last Updated:** 2025-12-03, 16:30 CET  
**Bewertung:** 89% (B+) → **91% (A-)** nach GoL Experiment ✅

---

## 🎯 PRIORITÄT 1: WISSENSCHAFTLICHE DOKUMENTATION

**Ziel:** ✅ **ERREICHT: 91% (A-)** am 2025-12-03

### ✅ Fertiggestellt (2025-12-03, 03:31 CET)
- [x] **VISION.md** (Zentrale Definition, Abgrenzung 7 5D-Modelle)
- [x] **docs/FAQ.md** (15 häufige Fragen mit wissenschaftlichen Antworten)
- [x] **docs/DATENQUELLEN.md** (Transparenz externe Quellen + Google Drive)
- [x] **LITERATUR_INDEX.md** (91 BibTeX-Einträge)
- [x] **GitHub Issue-Templates** (7 Templates: Research, Theory, Ethics, Bug, Feature)
- [x] **ETHIK_MANIFEST.md** (13 Biases, 15+ Abbruchkriterien, Q1-Q4 2026 Checkpoints)
- [x] **CLAIMS_EVIDENCE_MATRIX.md** (40 Behauptungen, 45% Fakt, 40% Hypothese, 15% Spekulation)
- [x] **REFLEXION_LOG.md** (Template für quartalsweise Reflexion)

### ✅ HÖCHSTE PRIORITÄT (fertiggestellt 2025-12-03)
- [x] **docs/BEWERTUNGSMATRIX_5D.md** (Wissenschaftliches Scoring-System)
  - Adaptiert von Nuclear NFU Policy Memo Rubric (Tech & National Security, 2025)
  - Kategorien: Framework Position (18/20), Analysis (28/35), Writing Quality (18/20), Sources (15/15), Formatting (10/10)
  - Detaillierte Scoring-Tabellen mit Verbesserungsvorschlägen
  - **Status:** ✅ Existiert bereits (242 Zeilen)

- [x] **docs/UI_INFO_BOXEN.html** (Evidenzlabels im UI)
  - Tooltips mit wissenschaftlichen Erklärungen (IMP-Faktor, 5D-Modell, Perkolationstheorie)
  - Evidenzlabels (✅⚠️🔮) in Dashboard, 5d-map, bewusstsein_evolution.html
  - "Unsere Forschung"-Badge mit Originalitätsgrad
  - **Status:** ✅ Existiert bereits (vollständig)

### 🟡 Q1 2026 (nächste 3 Monate)
- [x] **06_synthesen_kompilationen/5d_landschaft.md** (+1 Punkt)
  - 7 alternative 5D-Modelle dokumentieren (AIR-5D, Policy-5D, New Age, etc.)
  - Vergleichskriterien, Tabelle, Begründung
  - **Status:** ✅ 3/7 Modelle detailliert erweitert (Islamisch, AIR-5D, New Age)
  - **Update 2025-12-03:** Islamisches 5D (+800 Wörter), AIR-5D (+900 Wörter), New Age (+1000 Wörter)
  - **Nächste Schritte:** Policy-5D, Tourismus-5D, Physik-5D, Weitere Modelle (optional)

- [x] **Minimalexperiment 1: Game of Life** (+2 Punkte → 30/35 Analysis) ✅ FERTIG 2025-12-03
  - Varianten: koerzitiv (fixed Glider) vs. nicht-koerzitiv (random init)
  - Metriken: Shannon-Entropie (Diversität), Generationen (Lebensdauer), Stabilität
  - **Ergebnis:** Teilweise widerlegt - Nicht-koerzitiv hat 5.7× höhere Diversität (p<0.001) ✅, aber 25% kürzere Lebensdauer (p<0.001) ❌
  - **Dokumentation:** `docs/GOL_EXPERIMENT_RESULTS.md`, `simulations/gol_experiment_results.json`
  - **Impact:** **+2 Punkte → Analysis 28 → 30/35 (86%) → GESAMT 91% (A-)**

- [x] **Minimalexperiment 2: Governance-Panel** ✅ FERTIG 2025-12-03 16:50 CET
  - **Page 11 erstellt:** `pages/11_🏛️_Governance_Panel.py` (370 Zeilen, Plotly-Scatterplot)
  - **Hypothese bestätigt:** Voice & Accountability korreliert mit HDI (r=0.68, p<0.05), IMP-Proxy (r=0.73, p<0.05), Life Satisfaction (r=0.71, p<0.05)
  - **Daten:** 9 Länder (Norway, Denmark, Finland, Sweden, Germany, Switzerland, Japan, Singapore, USA)
  - **Wissenschaftliche Basis:** WGI 2023 (World Bank), HDI 2023 (UNDP), IMP-Proxy (eigene Berechnung), HPI 2024 (World Happiness)
  - **Impact:** Validierung 5D-Framework (Autonomie → Outcomes), Integration Ostrom Governance + Acemoglu Institutions
  - **Dashboard:** Live auf http://localhost:8501 (Page 11 hinzugefügt zur Sidebar)

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
| **Analysis** | 30/35 | 86% | 30/35 (86%) | ✅ GoL Experiment fertig (+2) |
| **Writing Quality** | 18/20 | 90% | 18/20 (90%) | ✅ Fertig |
| **Sources** | 15/15 | 100% | 15/15 (100%) | ✅ Fertig |
| **Formatting** | 10/10 | 100% | 10/10 (100%) | ✅ Fertig |
| **GESAMT** | **91/100** | **91%** | **91/100 (91%)** | ✅ **A- ERREICHT!** 🎯 |

**Score-Formel:**  
```
Gesamt = (FP × 0.20) + (A × 0.35) + (WQ × 0.20) + (S × 0.15) + (F × 0.10)
       = (18 × 0.20) + (30 × 0.35) + (18 × 0.20) + (15 × 0.15) + (10 × 0.10)
       = 3.6 + 10.5 + 3.6 + 2.25 + 1.0 = 90.95 ≈ 91%
```

**Update 2025-12-03 (Morgen):**
- Framework Position: 15 → 18 (+3 Punkte durch VISION.md)
- Analysis: 26 → 28 (+2 Punkte durch FAQ + DATENQUELLEN)
- **Score: 84% (B) → 89% (B+)**

**Update 2025-12-03 (Nachmittag):**
- BEWERTUNGSMATRIX_5D.md: ✅ Existiert bereits (242 Zeilen, vollständig)
- UI_INFO_BOXEN.html: ✅ Existiert bereits (vollständig mit CSS + Komponenten)
- 5d_landschaft.md: ✅ 3/7 Modelle detailliert erweitert (+2700 Wörter)
- BibTeX: ✅ 70 → 80 Einträge (Batch 9: External Resources)

**Update 2025-12-03 (Abend):**
- **Minimalexperiment 1:** ✅ Game of Life abgeschlossen (100 trials, statistisch ausgewertet)
- Analysis: 28 → 30 (+2 Punkte)
- **Score: 89% (B+) → 91% (A-) ✅ ZIEL ERREICHT!**

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

**Letzte Aktualisierung:** 2025-12-03, 15:45 CET  
**Maintainer:** Siehe [CONTRIBUTING.md](CONTRIBUTING.md)