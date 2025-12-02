# TODO: Multi-Page Dashboard Vervollständigung mit wissenschaftlichen Quellen

## 🎯 Ziel
Jedes Thema wird zu einer eigenen Page mit:
- ✅ Vollständige wissenschaftliche Quellenangaben (BibTeX + Links)
- ✅ Alle Formeln mit Begründung und Quelle
- ✅ Eigene Apps/Tests/Simulationen eingebaut
- ✅ Mini-Weltkarte mit Werten pro Land/Region
- ✅ Farbcodierte Legende mit %-Auswirkungen
- ✅ Interaktive Karten (klickbar → Detail-Ansicht)

---

## 📊 Phase 1: Dashboard Pages (Struktur)

### 0. Wiki/Home - Hauptseite (PRIORITY 1) ✅
- [x] Page erstellen: `5d_dashboard.py` (neu: als Wiki/Guide)
- [x] Installation für Anfänger (ohne Vorkenntnisse)
  - [x] GitHub Codespaces (empfohlen)
  - [x] Lokal (Windows/macOS/Linux)
  - [x] Docker (fortgeschritten)
- [x] Alle Befehle erklärt (freundlich, ohne Abwertung)
  - [x] 10 wichtigste Befehle mit expandable Details
  - [x] Begriffe-Glossar (Terminal, Python, Git, JSON, etc.)
- [x] Navigation zu allen anderen Pages
  - [x] Sidebar mit page_link() zu fertigen Seiten
  - [x] Übersicht aller 8 Seiten mit Beschreibung
- [x] Schnellstart-Guide (3 Schritte)
  - [x] Code öffnen → Dashboard starten → Erkunden
  - [x] 5D Framework erklärt (Formel, Dimensionen)
- [x] Troubleshooting-Sektion
  - [x] 6 FAQs (häufigste Probleme)
  - [x] 10-Punkte Checkliste
  - [x] Links zu Community/Docs
- [x] Links zu allen Ressourcen (Docs, BibTeX, GitHub)
  - [x] Dokumentation (User Guide, API, Contributing, Deployment)
  - [x] Code & Daten (GitHub, BibTeX, Manifest, Formeln)
  - [x] Externe Ressourcen (OWID, World Bank, WHO, arXiv, PubMed)
- [ ] Video-Tutorials (optional, später)

### 1. IMP Analysis (✅ DONE)
- [x] Scientific validation with BibTeX
- [x] Peer-reviewed sources linked
- [x] Formula explanation with references
- [ ] Mini-Weltkarte: IMP-Scores pro Land
- [ ] Legende: Farbcodes für IMP-Bereiche
- [ ] Eigene Apps: `models/imp.py` Visualisierung

### 2. Projects / Solutions
- [x] Page erstellen: `pages/2_🚀_Projects.py`
- [x] Formeln: ROI-Berechnung (Quelle: Heckman 2006, NPV-Methode)
- [x] Quellen: Alternative Bildung (Sudbury, Waldorf, Folk High Schools) mit BibTeX
- [x] ROI-Calculator interaktiv (Heckman-Methode)
- [ ] Mini-Karte: Standorte alternativer Schulen (Folium, Phase 3)
- [ ] Eigene Apps: Projekt-Simulator erweitern
- [ ] Tests: `tests/test_projects.py` mit wissenschaftlicher Validierung

### 3. Research / Papers
- [ ] Page erstellen: `pages/3_📚_Research.py`
- [ ] Quellen: arXiv, PubMed, WHO, World Bank
- [ ] Formeln: Relevanz-Score (eigene Gewichtung dokumentieren)
- [ ] Mini-Karte: Herkunftsländer der Papers
- [ ] Eigene Apps: Paper-Explorer mit Filter
- [ ] Tests: `tests/test_research_sources.py`

### 4. GitHub / Open Source
- [ ] Page erstellen: `pages/4_💻_GitHub.py`
- [ ] Quellen: GitHub API, Open Source Lizenzen
- [ ] Formeln: Activity-Score (Stars × Updates × Contributors)
- [ ] Mini-Karte: Entwickler-Community Verteilung
- [ ] Eigene Apps: Repo-Analyzer
- [ ] Tests: `tests/test_github_metrics.py`

### 5. Game of Life (Conway)
- [ ] Page erstellen: `pages/5_🧬_Game_of_Life.py`
- [ ] Quellen: Conway 1970, Wolfram 2002 (Cellular Automata)
- [ ] Formeln: Survival-Regeln (2-3 neighbors)
- [ ] Mini-Karte: Nicht anwendbar (abstrakte Simulation)
- [ ] Eigene Apps: `gol_streamlit.py` integrieren
- [ ] Tests: `tests/test_game_of_life.py` mit Pattern-Validierung

### 6. Non-Coercion / Zwanglosigkeit
- [ ] Page erstellen: `pages/6_🤝_Non_Coercion.py`
- [ ] Quellen: Ostrom 1990 (Commons), eigene Modellierung
- [ ] Formeln: Cooperation-Payoff vs. Coercion-Penalty
- [ ] Mini-Karte: Länder mit kooperativen Systemen
- [ ] Eigene Apps: `zwi_streamlit.py` integrieren
- [ ] Tests: `tests/test_non_coercion.py` mit Nash-Equilibrium

### 7. World Map / Geodaten
- [ ] Page erstellen: `pages/7_🌍_World_Map.py`
- [ ] Quellen: OWID, World Bank, WHO, WGI
- [ ] Formeln: IMP-Proxy = f(Depression, Dropout, Governance)
- [ ] Hauptkarte: Interaktiv mit Leaflet.js (embed oder iframe)
- [ ] Legende: Depression (rot), Dropout (orange), IMP (grün)
- [ ] Eigene Apps: `web/5d-map/` einbinden
- [ ] Tests: `tests/test_world_map_data.py`

### 8. Projections / Zukunft
- [ ] Page erstellen: `pages/8_📈_Projections.py`
- [ ] Quellen: IPCC-Modelle, eigene Extrapolation
- [ ] Formeln: Logistische Adoption-Kurve
- [ ] Mini-Karte: Projektionen nach Region
- [ ] Eigene Apps: Szenario-Rechner
- [ ] Tests: `tests/test_projections.py`

---

## 📖 Phase 2: Wissenschaftliche Quellen vervollständigen

### BibTeX-Einträge ergänzen
- [ ] Alle Dimensionen (A, IM, R, SP, Au) mit je 3-5 Quellen
- [ ] ROI-Studien: Heckman 2006, Perry Preschool
- [ ] Alternative Bildung: Greenberg 1992, Summerhill Neill 1960
- [ ] Governance: Ostrom 1990, Acemoglu & Robinson 2012
- [ ] Mental Health: WHO Reports, IHME GBD 2019
- [ ] Eigene Analysen: Transparent als "Own Research" markieren

### Quellenformat (Standard)
```bibtex
@article{author_year_keyword,
  title = {Full Title},
  author = {Last, First and Other, Author},
  year = {YYYY},
  journal = {Journal Name},
  volume = {XX},
  pages = {YY--ZZ},
  doi = {10.xxxx/xxxxx},
  url = {https://doi.org/...},
  note = {Brief context: Why relevant for 5D}
}
```

---

## 🗺️ Phase 3: Mini-Karten Integration

### Technische Umsetzung
- [ ] **Option A:** Folium-Maps in Streamlit (statisch, schnell)
- [ ] **Option B:** Plotly Choropleth (interaktiv, medium)
- [ ] **Option C:** Leaflet.js iframe (voll interaktiv, aufwändig)

### Datenquellen pro Karte
1. **IMP-Karte:** `web/5d-map/data/baseline.json` (30 Länder)
2. **Projects:** `5d_solutions.json` → Koordinaten extrahieren
3. **Research:** Papers → Autoren-Länder via Affiliations
4. **GitHub:** Repos → Contributors-Standorte (GitHub API)
5. **World Map:** Vollständige Leaflet-Integration

### Legende-Standard
```
Farbskala:
🟢 Hoch (>0.70):    Optimal
🟡 Mittel (0.40-0.70): Verbesserungspotenzial
🔴 Niedrig (<0.40):  Kritisch

Größe: Proportional zu Datenmenge (z.B. Paper-Count)
Klick: Öffnet Detail-Modal mit Quellen
```

---

## 🧪 Phase 4: Eigene Apps & Tests einbauen

### Apps integrieren (per Page)
1. **IMP Analysis:** `models/imp.py` → Live-Rechner
2. **Projects:** Projekt-ROI-Simulator
3. **Research:** Paper-Filter + Keyword-Graph
4. **GitHub:** Repo-Trends + Activity-Chart
5. **Game of Life:** `gol_streamlit.py` embed (iframe oder direkt)
6. **Non-Coercion:** `zwi_streamlit.py` embed
7. **World Map:** `web/5d-map/` embed via iframe
8. **Autopoietic:** `autopoietic_streamlit.py` (neue Page?)

### Tests mit wissenschaftlicher Basis
- [ ] `tests/test_imp_scientific.py` ✅ (11 tests, done)
- [ ] `tests/test_dimensions_sources.py` (jede Dimension validieren)
- [ ] `tests/test_formulas_accuracy.py` (Formeln gegen Literatur)
- [ ] `tests/test_data_quality.py` (Quellenintegrität)
- [ ] `tests/test_maps_rendering.py` (Karten-Daten korrekt?)

---

## 📝 Phase 5: Haupttext + Formeln + Quellen

### Template pro Page (Standardstruktur)

```python
# Header
st.title("📊 Thema XYZ")
st.markdown("### Wissenschaftliche Grundlage")

# Haupttext (200-400 Wörter)
st.markdown(\"\"\"
[Erklärung des Themas mit wissenschaftlichem Kontext]
\"\"\")

# Formeln
st.header("🔬 Formeln & Berechnungen")
with st.expander("Formel 1: [Name]"):
    st.latex(r"IMP = A \\times IM \\times R \\times SP \\times Au")
    st.markdown("**Quelle:** Deci & Ryan (1985) - @cite{deci1985intrinsic}")
    st.markdown("**Begründung:** Multiplikativ weil...")
    
# Mini-Karte
st.header("🗺️ Geografische Verteilung")
# [Folium/Plotly Map hier]

# Eigene Apps
st.header("🧪 Interaktive Tools")
# [App embed hier]

# Quellen (Footer)
st.divider()
st.header("📚 Wissenschaftliche Quellen")
st.markdown(\"\"\"
1. **Deci, E. L., & Ryan, R. M. (1985).** *Intrinsic Motivation and Self-Determination*. 
   Springer. [DOI: 10.1007/978-1-4899-2271-7](https://doi.org/10.1007/978-1-4899-2271-7)
   
2. **Csíkszentmihályi, M. (1990).** *Flow: The Psychology of Optimal Experience*. 
   Harper & Row. [Amazon](https://amazon.com/...)
   
[...weitere Quellen...]

**Eigene Analysen:**
- IMP-Berechnung: Basiert auf obigen Theorien, eigene Gewichtung
- Datenintegration: OWID, World Bank, WHO (öffentlich verfügbar)
\"\"\")
```

---

## 🎨 Phase 6: Design & UX

### Farbcodes (konsistent über alle Pages)
- **IMP-Scores:** Grün (#00ff00) bis Rot (#ff0000)
- **Peer-Reviewed:** Grün Badge ✅
- **Own Research:** Orange Badge ⚠️
- **Missing Data:** Grau Badge ⚪

### Interaktivität
- [ ] Alle Karten klickbar (→ Detail-Modal)
- [ ] Slider für dynamische Formeln
- [ ] Download-Buttons für Daten (CSV, JSON)
- [ ] Copy-Button für BibTeX-Einträge

---

## 📊 Phase 7: Daten einpflegen

### Priorität 1 (Basis-Daten vorhanden)
- [x] IMP-Scores: `baseline.json` (30 Länder) ✅
- [ ] Projects: `5d_solutions.json` → Koordinaten hinzufügen
- [ ] Research: `5d_research_data.json` → Länder-Mapping
- [ ] GitHub: `5d_github_data.json` → Geo-Locations

### Priorität 2 (Neue Daten sammeln)
- [ ] Depression-Raten: OWID → CSV → JSON
- [ ] Dropout-Raten: World Bank EdStats → JSON
- [ ] Governance: WGI → JSON (Voice & Accountability)
- [ ] Folk High Schools: Manuell recherchieren (Dänemark, Norwegen)

### Priorität 3 (Erweiterte Daten)
- [ ] Tokkatsu-Schulen: Japan (recherchieren)
- [ ] Sudbury-Schulen: USA, Europa (Website scrapen?)
- [ ] Waldorf-Schulen: Waldorf Foundation API?

---

## 🧪 Phase 8: Testing & Validierung

### Test-Coverage Ziele
- [ ] IMP-Berechnungen: 100% (✅ done)
- [ ] Datenquellen: 90% (Quellenintegrität)
- [ ] Formeln: 95% (gegen Literatur validiert)
- [ ] UI-Rendering: 80% (Karten korrekt?)

### Continuous Integration
- [ ] Pre-Commit Hook: Tests laufen vor jedem Commit
- [ ] GitHub Actions: Tests bei jedem Push
- [ ] Coverage Report: Automatisch generieren

---

## 📅 Zeitplan (Schätzung)

### Sprint 1 (Tag 1-2): Struktur
- [x] Phase 1: Pages 1-4 erstellen (Grundstruktur)
- [ ] Phase 2: BibTeX vervollständigen (50 Einträge)

### Sprint 2 (Tag 3-4): Karten
- [ ] Phase 3: Mini-Karten (Folium) für alle Pages
- [ ] Phase 4: Apps einbinden (iframes/direkt)

### Sprint 3 (Tag 5-6): Content
- [ ] Phase 5: Haupttexte + Formeln + Quellen
- [ ] Phase 6: Design polieren

### Sprint 4 (Tag 7): Testing
- [ ] Phase 7: Daten einpflegen
- [ ] Phase 8: Tests erweitern, CI/CD

---

## 🚀 Nächste Schritte (Sofort)

1. **Pages 2-4 erstellen** (Projects, Research, GitHub)
2. **BibTeX erweitern** (20 neue Einträge)
3. **Folium-Karten** (Proof-of-Concept für IMP-Page)
4. **Tests erweitern** (Dimensionen-Quellen validieren)

---

**Erstellt:** 2. Dezember 2025  
**Status:** In Bearbeitung  
**Ziel:** Production-ready multi-page dashboard mit vollständiger wissenschaftlicher Dokumentation
