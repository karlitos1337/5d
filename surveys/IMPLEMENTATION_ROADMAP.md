# 5D-Intelligence Survey Framework - Implementierungs-Roadmap

## 🎯 Projektübersicht

**Ziel**: Entwicklung eines wissenschaftlich validierten, anonymen Erhebungsinstruments zur Erfassung multidimensionaler Intelligenz.

**Status**: ✅ **Spezifikation vollständig** | 🚧 **Implementierung Phase 1 gestartet**

---

## ✅ Abgeschlossen

### Phase 0: Konzeption & Design (100%)
- [x] 5D-Framework definiert (Neurobiologie, Psychologie, Philosophie, Ökonomie, Technologie)
- [x] Wissenschaftliche Grundlagen recherchiert
- [x] Ethik-Richtlinien erstellt (DSGVO-konform)
- [x] Anonymisierungs-Konzept entwickelt

### Phase 1A: Fragebogen-Entwicklung (100%)
- [x] Eingangsfragen (demografisch, anonym) - 9 Fragen
- [x] Dimension 1: Neurobiologie - 12 Fragen (Flow, Attention, Neuroplastizität, etc.)
- [x] Dimension 2: Psychologie - 10 Fragen (SDT, Growth Mindset, Selbstwirksamkeit)
- [x] Dimension 3: Philosophie - 10 Fragen (Kritisches Denken, Epistemic Pluralism)
- [x] Dimension 4: Ökonomie - 10 Fragen (Partizipation, Commons, Degrowth)
- [x] Dimension 5: Technologie - 10 Fragen (Open Source, Digital Autonomy, AI Ethics)
- [x] **Gesamt: 61 Fragen** (9 Eingang + 52 Dimensionen)
- [x] Alle Fragen mit wissenschaftlichen Quellen belegt (BibTeX)

### Phase 1B: Backend-Infrastruktur (100%)
- [x] Score-Berechnungs-Algorithmen (`analysis/calculate_5d_scores.py`)
- [x] Clustering-Implementierung (`analysis/cluster_responses.py`)
  - [x] K-Means (5 Cluster)
  - [x] DBSCAN (Density-based)
  - [x] PCA (Dimensionsreduktion)
- [x] Visualisierungs-Templates (`analysis/visualize_results.py`)
  - [x] Radar-Charts (5D-Profile)
  - [x] Heatmaps (Korrelationen)
  - [x] Scatter-Plots (Cluster)
- [x] Anonymisierungs-Layer (`storage/anonymize.py`)
  - [x] SHA256-basierte ID-Generierung
  - [x] Prohibited-Fields-Prüfung
  - [x] DSGVO-konforme Datenverarbeitung
- [x] GitHub OAuth Integration (`auth/github_oauth.py`)
  - [x] Nur Zugangskontrolle, keine Daten-Persistierung
- [x] Validierungs-Framework (`surveys/validator.py`)
- [x] Test-Suite (`tests/`)
  - [x] Anonymisierungs-Tests
  - [x] Validierungs-Tests

### Phase 1C: Dokumentation (100%)
- [x] Copilot-Instruktionen (`.github/copilot-instructions.md`)
- [x] BibTeX-Quellensammlung (`surveys/bibtex_sources.bib`)
- [x] README-Dateien für alle Module
- [x] Diese Roadmap

---

## 🚧 In Arbeit

### Phase 2: Web-Interface (Priorität 1)

**Ziel**: Benutzerfreundliches, responsives Survey-Interface

#### 2.1 Frontend-Entwicklung
- [ ] React + Vite Setup
  - [ ] `web/survey-app/package.json`
  - [ ] Tailwind CSS Konfiguration
  - [ ] TypeScript-Konfiguration
- [ ] Komponenten-Entwicklung
  - [ ] `LoginPage.tsx` (GitHub OAuth Button)
  - [ ] `ConsentPage.tsx` (DSGVO-Einwilligung)
  - [ ] `EntranceQuestions.tsx`
  - [ ] `DimensionQuestionnaire.tsx` (wiederverwendbar für alle 5D)
  - [ ] `ProgressBar.tsx`
  - [ ] `ResultsPage.tsx` (Radar-Chart, Download)
- [ ] State Management
  - [ ] React Context oder Zustand
  - [ ] LocalStorage für Draft-Speicherung
- [ ] Formular-Validierung
  - [ ] Echtzeit-Validierung
  - [ ] Fehler-Feedback

**Geschätzte Dauer**: 3-4 Wochen

#### 2.2 Backend-API
- [ ] FastAPI Setup
  - [ ] `api/main.py`
  - [ ] OAuth-Endpoints (`/auth/login`, `/auth/callback`)
  - [ ] Survey-Endpoints (`/survey/submit`, `/survey/results`)
- [ ] Datenbank
  - [ ] SQLite für Entwicklung
  - [ ] PostgreSQL für Produktion
  - [ ] Alembic Migrations
- [ ] Session-Management
  - [ ] Redis für Sessions
  - [ ] JWT-Tokens (anonym)

**Geschätzte Dauer**: 2-3 Wochen

#### 2.3 Integration & Testing
- [ ] End-to-End Tests (Playwright)
- [ ] API-Tests (pytest)
- [ ] Performance-Tests (Locust)
- [ ] Accessibility-Tests (axe-core)

**Geschätzte Dauer**: 1-2 Wochen

---

## 📅 Geplant

### Phase 3: Wissenschaftliche Validierung (Priorität 2)

**Ziel**: Sicherstellung akademischer Standards

#### 3.1 Reliabilitäts-Analyse
- [ ] Cronbach's Alpha pro Dimension
- [ ] Test-Retest-Reliabilität (50 Teilnehmer, 2 Wochen Abstand)
- [ ] Split-Half-Reliabilität

**Methode**: `analysis/reliability_analysis.py`

#### 3.2 Validitäts-Prüfung
- [ ] Konstruktvalidität (Faktorenanalyse)
- [ ] Konvergente Validität (Korrelation mit etablierten Skalen)
- [ ] Diskriminante Validität (Unterschiedlichkeit der Dimensionen)

**Methode**: Kooperation mit Universität/Forschungsinstitut

#### 3.3 Pilotphase
- [ ] 50-100 Teilnehmer rekrutieren
- [ ] Qualitatives Feedback sammeln
- [ ] Fragebogen-Optimierung basierend auf Feedback
- [ ] Statistische Analyse der Pilot-Daten

**Geschätzte Dauer**: 2-3 Monate

---

### Phase 4: Produktionsreife (Priorität 2)

#### 4.1 Deployment
- [ ] GitHub Pages für Frontend (statisch)
- [ ] Railway/Render für Backend-API
- [ ] PostgreSQL-Datenbank (Supabase/Railway)
- [ ] Redis-Instance (Upstash)
- [ ] CDN-Setup (Cloudflare)

#### 4.2 Monitoring & Analytics
- [ ] Sentry (Error Tracking)
- [ ] Plausible Analytics (Privacy-focused, DSGVO-konform)
- [ ] Health-Check-Endpoints
- [ ] Performance-Monitoring

#### 4.3 CI/CD
- [ ] GitHub Actions
  - [ ] Automated Tests
  - [ ] Deployment-Pipeline
  - [ ] Security-Scans (Dependabot, CodeQL)
- [ ] Staging-Environment
- [ ] Automated Backups

**Geschätzte Dauer**: 2 Wochen

---

### Phase 5: Erweiterungen (Priorität 3)

#### 5.1 Mehrsprachigkeit
- [ ] Englische Übersetzung aller Fragen
- [ ] i18n-Framework (react-i18next)
- [ ] Sprachauswahl im Frontend

#### 5.2 Longitudinale Erhebung (Optional Opt-In)
- [ ] Wiederholungs-Möglichkeit mit Vergleich
- [ ] Zeitverlaufs-Visualisierung
- [ ] Entwicklungs-Tracking

**Hinweis**: Erfordert pseudonyme Verknüpfung (User entscheidet explizit)

#### 5.3 Erweiterte Visualisierungen
- [ ] 3D-Scatter-Plots (Plotly)
- [ ] Interaktive Dashboards (Streamlit)
- [ ] PDF-Export der Ergebnisse
- [ ] Vergleich mit aggregierten Daten

**Geschätzte Dauer**: 4-6 Wochen

---

## 👥 Team & Kompetenzen

### Benötigte Rollen
- **Frontend-Entwickler** (React, TypeScript, Tailwind)
- **Backend-Entwickler** (Python, FastAPI, PostgreSQL)
- **Data Scientist** (Statistik, Validierung, Clustering)
- **UX-Designer** (Survey-Design, Accessibility)
- **Wissenschaftlicher Berater** (Psychologie/Neurowissenschaft)

### Offene Beiträge willkommen!
Siehe `CONTRIBUTING.md` für Richtlinien.

---

## 📊 Erfolgskriterien

### Quantitativ
- ☑️ **61 wissenschaftlich validierte Fragen** implementiert
- 🔲 **Cronbach's Alpha > 0.7** pro Dimension
- 🔲 **500+ Teilnehmer** in Pilotphase
- 🔲 **< 15 Minuten** durchschnittliche Bearbeitungszeit
- 🔲 **> 80% Completion-Rate**

### Qualitativ
- ☑️ **100% DSGVO-Konformität**
- ☑️ **Vollständige Anonymität** garantiert
- 🔲 **Positive User-Feedback** (> 4.0/5.0)
- 🔲 **Wissenschaftliche Publikation** möglich
- 🔲 **Open-Science-Standards** erfüllt

---

## 📅 Zeitplan

| Phase | Start | Ende | Status |
|-------|-------|------|--------|
| Phase 0: Konzeption | 2025-11-01 | 2025-11-30 | ✅ Abgeschlossen |
| Phase 1: Fragebogen & Backend | 2025-12-01 | 2025-12-15 | ✅ Abgeschlossen |
| Phase 2: Web-Interface | 2025-12-15 | 2026-01-31 | 🚧 Gestartet |
| Phase 3: Validierung | 2026-02-01 | 2026-04-30 | 📅 Geplant |
| Phase 4: Produktion | 2026-05-01 | 2026-05-31 | 📅 Geplant |
| Phase 5: Erweiterungen | 2026-06-01 | ongoing | 📅 Geplant |

---

## 🔗 Ressourcen

### Dokumentation
- [Copilot Instructions](../.github/copilot-instructions.md)
- [BibTeX Sources](./bibtex_sources.bib)
- [Analysis README](../analysis/README.md)

### Wissenschaftliche Grundlagen
- Self-Determination Theory (Deci & Ryan, 2000)
- Flow Theory (Csikszentmihalyi, 1990)
- Domain-Driven Design (Evans, 2003)
- Participatory Economics (Albert & Hahnel, 1991)
- Open Source Philosophy (Raymond, 1999)

### Technische Referenzen
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Plotly Python](https://plotly.com/python/)
- [scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [React Survey Library](https://github.com/surveyjs/survey-library)

---

## ❓ FAQ

### Warum GitHub OAuth?
**A**: Um Bots und Mehrfach-Teilnahmen zu verhindern, ohne personenbezogene Daten zu speichern.

### Wie wird Anonymität garantiert?
**A**: GitHub-Daten werden NUR zur Login-Verifikation verwendet, dann sofort verworfen. Antworten erhalten SHA256-Hash-IDs ohne Rückverfolgbarkeit.

### Kann ich meine Daten löschen?
**A**: Da Daten anonym sind, gibt es keine Verknüpfung zu Ihnen. Sie können aber via GitHub Issue Ihre Session-Token-basierte Löschung beantragen.

### Wie lange dauert die Teilnahme?
**A**: Ca. 10-15 Minuten für alle 61 Fragen.

### Bekomme ich meine Ergebnisse?
**A**: Ja! Direkt nach Abschluss als interaktives Radar-Chart + Download (JSON/PDF).

---

## 📝 Changelog

### v1.0.0 (2025-12-02)
- ✅ Vollständiger Fragebogen (61 Fragen)
- ✅ Backend-Algorithmen implementiert
- ✅ Anonymisierungs-Layer fertig
- ✅ Test-Suite erstellt
- ✅ Dokumentation vollständig

---

**Status**: Bereit für Phase 2 (Web-Interface)  
**Nächster Meilenstein**: React-App Launch (2026-01-31)  
**Kontakt**: GitHub Issues & Discussions
