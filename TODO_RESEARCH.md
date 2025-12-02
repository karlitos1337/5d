# TODO – 5D-Forschungsplanung

**Status:** Draft (2025-12-02)  
**Scope:** Wissenschaftliche Grundlagen, empirische Testbarkeit, theoretische Kohärenz

---

## 0. Meta / Organisation

- [ ] **Repository-Struktur für Forschung klären**
  - Anbindung an bestehende Ordner:
    - `02_neurobiologie_psychologie/` – Neurowissenschaftliche Grundlagen
    - `03_philosophie_epistemologie/` – Philosophie des Geistes, Phänomenologie
    - `04_oekonomie_governance/` – Verhaltensökonomie, Governance-Modelle
    - `06_synthesen_kompilationen/` – Meta-Analysen, Vergleichsstudien
    - `07_daten_analysen/` – Datensätze, empirische Validierung
  - Neue Struktur: `research/` Namespace vs. Integration in 0x-Ordner

- [x] **Zentrales Literatur-File definieren** ✅
  - Location: `07_daten_analysen/LITERATUR_INDEX.md` (DONE)
  - Verweise auf:
    - `5d-relevant-sources.bib` (64 entries, BibTeX) ✅
    - `SOURCES.md` (allgemeine Quellen) ✅
    - `RAUM_QUELLEN_INDEX.md` (räumliche Datenquellen) ✅
    - `WISSENS_INDEX.md` (Wissensmanagement) ✅
  - Kategorisierung: Neuro, Öko, Sozial, Philosophie, Governance ✅

- [ ] **Dokumentationsstandard erweitern**
  - In `docs/README.md` ergänzen:
    - **Zitierstil:** APA 7th Edition (konsistent mit BibTeX)
    - **Evidenzlabel:** 
      - ✅ **Fakt** (peer-reviewed, repliziert)
      - ⚠️ **Hypothese** (plausibel, testbar, nicht validiert)
      - 🔮 **Spekulation** (explorativ, spekulativ, offene Frage)
    - **Begriffs-Glossar:** Zentrale Definitionen (5D, Zwanglosigkeit, IMP, Autopoiesis)

- [ ] **Research Namespace evaluieren**
  - Option A: Separater `research/` Ordner (papers, drafts, experiments)
  - Option B: Alles über 0x-Ordner (bessere Integration)
  - Entscheidung dokumentieren in `docs/ARCHITECTURE.md`

---

## 1. Klärung des 5D-Begriffs

**Problem:** "5D" ist überladen (AIR-5D, Policy-5D, Bildungs-5D, New-Age-5D-Bewusstsein etc.)

- [ ] **Präzise Definition in `VISION.md`**
  - 5D-Intelligence Framework = **spatio-temporales Netzwerkmodell**
  - Dimensionen: x, y, z (Raum) + t (Zeit) + **Netzwerkzustand** (Topologie, Konnektivität)
  - Constraint: **Zwanglosigkeit** als fundamentales Organisationsprinzip
  - Unterscheidung zu klassischen 5D-Modellen (5. Dimension ≠ Kaluza-Klein, String Theory)

- [ ] **Mapping externer 5D-Modelle**
  - Datei: `06_synthesen_kompilationen/5d_landschaft.md`
  - Modelle dokumentieren:
    - **AIR-5D** (Accountability, Impartiality, Responsiveness + 2 weitere)
    - **Policy-5D** (Policy-Evaluationsframework)
    - **Bildungs-5D** (Islamisches Bildungsmodell: Körper, Geist, Seele, Sozial, Spirituell)
    - **5D-Bewusstsein** (New Age: Lichtkörper, Dimensionsaufstieg)
    - **Touristische 5D-Resilienz** (Tourismus-Impact-Framework)
  - Begründung: Warum diese NICHT das eigene Framework sind

- [ ] **Vergleichstabelle erstellen**
  - Location: `README.md` / `VISION.md`
  - Spalten:
    - Modell-Name
    - Domäne (Neuro, Sozial, Spirituell, Policy, etc.)
    - Ziel (Beschreibung, Präskription, Metaphysik)
    - Empirische Basis (peer-reviewed, anekdotisch, keine)
    - Verhältnis zu Zwang/Zwanglosigkeit (explizit, implizit, irrelevant)
    - Bezug zu 5d-Framework (kompatibel, orthogonal, inkompatibel)

- [ ] **Arbeitsdefinition formulieren**
  - 1–2 präzise Absätze:
    - **Zwanglosigkeit:** Selbstorganisation ohne externe Steuerung/Koercion
    - **Intrinsische Motivation:** Autonomie, Kompetenz, Verbundenheit (Deci & Ryan 1985)
    - **Nicht-koerzitive Selbstorganisation:** Emergente Ordnung ohne Top-Down-Kontrolle
  - Integration in Wiki (`5d_dashboard.py` Page 0) + `VISION.md`

---

## 2. Neurowissenschaftliche Spur

**Ziel:** Neurobiologische Grundlagen für nicht-koerzitive Selbstorganisation

- [ ] **Literatur kuratieren in `02_neurobiologie_psychologie/`**
  - Themen:
    - Selbstorganisation neuronaler Netzwerke (Edelman, Tononi IIT)
    - Network Sampling (Hippocampus, DMN, salience network)
    - DMN (Default Mode Network) & Frontoparietal Network (task-positive)
    - Polyvagal Theory (Porges 2011) – autonomic regulation
    - Flow & Neural Signatures (Csíkszentmihályi, fMRI studies)
  - BibTeX-Einträge ergänzen (aktuell 59 → Ziel 80+)

- [ ] **Netzwerk-Topologie analysieren**
  - Skripte in `07_daten_analysen/`:
    - `analyze_network_topology.py` (Betti-Zahlen, H₁/H₂, persistent homology)
    - `cluster_coefficients.py` (Watts-Strogatz, small-world metrics)
    - `betweenness_centrality.py` (Granovetter weak ties, hubs)
  - Beispielgraphen: Connectome datasets (C. elegans, Drosophila, Human Connectome Project)

- [ ] **Minimales Netzwerkmodell implementieren**
  - Datei: `simulations/neural_inhibition_model.py`
  - Modell: Graph mit adaptiver Inhibition μ (μ_low = non-coercive, μ_high = coercive)
  - Metriken:
    - Vielfalt (Shannon-Entropie der Aktivierungsmuster)
    - Stabilität (Lyapunov-Exponenten)
    - Evolvabilität (Reaktion auf Störungen)
  - Hypothese: μ_low → robustere Vielfalt als μ_high

- [ ] **Verbindung zu IMP/Resonanz-Mapping**
  - Integration mit `apply_resonance_mapping.py` und `mapping_resonance_imp.md`
  - Test: Nicht-koerzitive Update-Regeln → höhere IMP-Scores?
  - Visualisierung in `5d_dashboard.py` (Page 1: IMP Analysis)

- [ ] **Lücken-Memo erstellen**
  - Datei: `02_neurobiologie_psychologie/GAPS_NEUROBIOLOGIE.md`
  - Fragen:
    - Wo sind nur Analogien (Graph ≠ Gehirn)?
    - Wo wäre echte neurobiologische Datenanbindung nötig (EEG, fMRI, MEG)?
    - Welche Experimente könnten Hypothesen validieren?

---

## 3. Philosophie des Geistes / Bewusstsein

**Ziel:** Phänomenologische Grundlagen ohne metaphysische Esoterik

- [ ] **Phänomenologie ausarbeiten**
  - Datei: `03_philosophie_epistemologie/5d_phaenomenologie.md`
  - Autoren:
    - Husserl (Intentionalität, epoché)
    - Merleau-Ponty (embodiment, leibliche Wahrnehmung)
    - Varela (enaktive Kognition, autopoiesis)
    - Thompson (Mind in Life, neurophenomenology)
  - Fokus: Zwanglosigkeit und Intentionalität ohne externe Steuerung

- [ ] **5D-Bewusstseinszustand definieren**
  - Kriterien:
    - Nicht metaphysisch (kein Lichtkörper, keine Dimensionsaufstieg)
    - Operationalisierbar (Selbstbericht, Neurofeedback, Verhaltensmetriken)
    - Verbindung zu Flow, Open Awareness, Non-Dual States
  - Abgrenzung zu New-Age-Narrativen (explizit in `VISION.md`)

- [ ] **UI-Flows für nicht-koerzitive Interaktion**
  - In `bewusstsein_evolution.html` und `autopoietic_streamlit.py`:
    - Affordanzen statt Druck (Gibson ecological psychology)
    - Keine Dark Patterns (Forced Actions, Nagging, Confirmshaming)
    - User Agency Preservation (klare Feedback-Loops, Autonomie-Respekt)
  - Design Principles dokumentieren in `docs/UX_PRINCIPLES.md`

- [ ] **Offene theoretische Fragen dokumentieren**
  - Datei: `03_philosophie_epistemologie/OPEN_QUESTIONS.md`
  - Fragen:
    - Wo endet aktuelle Philosophie des Geistes?
    - Wo beginnt Spekulation im Projekt?
    - Welche Brücken zur Neurowissenschaft sind tragfähig?
    - Wie lässt sich subjektive Erfahrung mit objektiven Metriken verbinden (hard problem)?

---

## 4. Verhaltensökonomie / Motivation

**Ziel:** Ökonomische Modelle mit Zwang als Störgröße

- [ ] **Literatur zusammentragen in `04_oekonomie_governance/`**
  - Themen:
    - Selbstbestimmungstheorie (SDT: Deci & Ryan 1985, 2000)
    - Bounded Rationality (Simon, Kahneman & Tversky)
    - Soziale Normen (Ostrom 1990, Axelrod 1984)
    - Nicht-koerzive Modelle (Nudge-Kritik, Libertarian Paternalism)
    - Commons Governance (Ostrom's 8 Principles)

- [ ] **Survey-Modul entwerfen**
  - In `surveys/dimension_5_agency_economics.py`:
    - Wahrgenommene Autonomie (PANAS, autonomy subscale)
    - Agency (locus of control, self-efficacy)
    - Einkommensverlauf (longitudinal income trajectory)
    - Kohäsion (social capital, trust, reciprocity)
    - Ressourcenzugang (housing, education, healthcare)

- [ ] **Auswertungslogik implementieren**
  - Scripts in `analysis/`:
    - `calculate_agency_score.py` (Agency = autonomy × competence × relatedness)
    - `cohesion_metrics.py` (social network density, trust indices)
    - `income_gradients.py` (Gini, income mobility, generational wealth)
  - Visualisierung in `5d_dashboard.py` (neue Page oder Integration in Page 2: Projects)

- [ ] **IYPT-Interventionsstudien analysieren**
  - International Youth Panel Transitions (falls relevant)
  - Memo: `04_oekonomie_governance/INTERVENTIONS_CRITIQUE.md`
  - Frage: Wie reproduzieren „positive" Interventionen langfristig koerzitive Muster?
  - Beispiele: Conditional Cash Transfers, Nudges, Gamification

- [ ] **Hypothesen für ökonomisches Modell formulieren**
  - Zwang als explizite Störgröße (Friction Coefficient)
  - Modell: Utility Function U = f(Autonomy, Resources) - λ × Coercion
  - Parameter λ = Coercion Sensitivity (individuell, kontextabhängig)
  - Test: Simulationen in `simulations/economic_agency_model.py`

---

## 5. Gaia, Autopoiesis, Sympoiesis

**Ziel:** Ökologische Selbstorganisation ohne Top-Down-Kontrolle

- [ ] **Vergleichsdokument erstellen**
  - Datei: `06_synthesen_kompilationen/gaia_autopoiesis_sympoiesis_5d.md`
  - Modelle:
    - **Gaia** (Lovelock & Margulis) – Erde als selbstregulierendes System
    - **Autopoiesis** (Maturana & Varela 1980) – geschlossene Selbstproduktion
    - **Sympoiesis** (Haraway) – offene Ko-Produktion, dezentral
  - Kriterienkatalog:
    - Geschlossenheit vs. Offenheit
    - Selbstproduktion vs. Ko-Produktion
    - Zentrale Steuerung vs. dezentrale Emergenz
    - Verhältnis zu Zwanglosigkeit

- [ ] **Autopoietisch vs. Sympoietisch definieren**
  - **Autopoietisch:** Geschlossen, selbstproduzierend (Zelle, Organismus)
  - **Sympoietisch:** Offen, ko-produziert, dezentral (Ökosystem, soziales System)
  - 5D-Framework: Sympoietisch (Netzwerk, keine zentrale Kontrolle)

- [ ] **Simulation bauen**
  - Erweitern: `autopoietic_streamlit.py` → `sympoietic_streamlit.py`
  - Features:
    - Ressourcenzonen (N regions, resource flow)
    - Feedback-Schleifen (positive/negative, local/global)
    - Schalter: "Top-Down-Kontrolle" (an/aus)
  - Metriken:
    - Vielfalt (Shannon-Entropie der Ressourcenverteilung)
    - Stabilität (Zeitreihen-Varianz)
    - Resilienz (Erholung nach Störung)
  - Hypothese: Sympoietisch (ohne Top-Down) → höhere Resilienz

- [ ] **Gaia auf 5D-Struktur mappen**
  - Gaia als sympoietisches Netzwerk:
    - Knoten: Mikroben, Pflanzen, Tiere, Geosphäre, Atmosphäre
    - Kanten: Stoffflüsse (C, N, P, H₂O), Energieflüsse (Solar, chemisch)
    - Dynamik: Feedback-Loops ohne zentrale Steuerung
  - Visualisierung: `web/5d-map` (globale Ökosystem-Netzwerke)

---

## 6. Ökosysteme und Evolution

**Ziel:** Nicht-koerzitive Evolvabilität als langlebiges Systemprinzip

- [ ] **Literatur zu Selbstorganisation konsolidieren**
  - In `07_daten_analysen/ecology_self_organization.md`:
    - Trockengebiete (Musterbildung, Vegetation Patches)
    - Wasserverteilung (Runoff-Infiltration Feedback)
    - Lévy-Flüge (optimal foraging, scale-free search)
    - Frontinstabilitäten (Turing patterns, reaction-diffusion)
  - Quellen: Rietkerk, Kéfi, Scheffer (tipping points, regime shifts)

- [ ] **Hypermutabilität modellieren**
  - Datei: `simulations/hypermutability_pflu.py`
  - Modell: Lokale Hypermutabilität vs. normale Mutation
  - Parameter:
    - μ_normal (baseline mutation rate)
    - μ_hyper (stress-induced hypermutation)
    - Selection pressure (environmental harshness)
  - Metriken:
    - Evolvabilität (adaptive capacity, genetic diversity)
    - Diversität (Shannon-Entropie, Simpson Index)
    - Überleben (population size, extinction risk)
  - Hypothese: Hypermutabilität → höhere Evolvabilität unter Stress

- [ ] **Nicht-koerzitive Evolvabilität formulieren**
  - Prinzip: Langlebige Systeme = flexible Anpassung ohne externe Steuerung
  - Kopplung an `src/universal_system_genesis_5d`:
    - Evolvabilität als 6. Dimension? (5D + E)
    - Integration in IMP-Formel: IMP_E = IMP × Evolvability
  - Dokumentation in `models/evolvability.py`

- [ ] **Empirische Datensätze identifizieren**
  - Öffentlich verfügbare Daten:
    - Vegetation Patterns (Remote Sensing, NASA, MODIS)
    - Microbial Diversity (Earth Microbiome Project)
    - Evolutionary Rates (Genome databases, NCBI)
  - Plausibilitätscheck in `07_daten_analysen/`:
    - `validate_vegetation_patterns.py` (Spatial autocorrelation, power laws)
    - `microbial_diversity_analysis.py` (Alpha/Beta diversity, network analysis)

---

## 7. Soziale Systeme, Governance, Urbanität

**Ziel:** Community-led Governance als nicht-koerzives Organisationsprinzip

- [ ] **Fallstudien sammeln in `04_oekonomie_governance/`**
  - Themen:
    - Community-led Governance (Ostrom commons, participatory budgeting)
    - Urbane Resilienz (Rotterdam, Copenhagen climate adaptation)
    - Gewaltprävention (Medellín, Ceará violence reduction)
    - Partizipative Stadtgestaltung (Curitiba BRT, tactical urbanism)
  - Datei: `04_oekonomie_governance/CASE_STUDIES.md`

- [ ] **Governance-Metriken definieren**
  - In `analysis/governance_metrics.py`:
    - Soziale Kohäsion (trust, civic engagement, social capital)
    - Einkommensentwicklung (income mobility, generational wealth)
    - Resilienz-Indizes (adaptive capacity, recovery speed)
    - Ökologische Dienstleistungen (green space, biodiversity, air quality)
  - WGI-Anbindung: World Governance Indicators (Voice & Accountability)

- [ ] **Dashboard-Integration**
  - In `web/5d-map` und `5d_dashboard.py`:
    - Indikatoren für nicht-koerzitive Governance:
      - Community-led (% participatory budgeting, local autonomy)
      - Adaptive Feedbacks (policy iteration speed, citizen input)
      - Ressourcenautonomie (local production, energy independence)
    - Farbcodierung: Grün (high autonomy) → Rot (high coercion)

- [ ] **FEMA-Kritik-Memo**
  - Datei: `04_oekonomie_governance/FEMA_CRITIQUE.md`
  - Problem: Aggregierte Scores als Intelligenzmaß unzureichend
  - Argumente:
    - Simpson's Paradox (Aggregation hides subgroup patterns)
    - Campbell's Law (metrics become targets → gaming)
    - Context-insensitivity (one-size-fits-all)
  - Alternative: Multi-dimensional profiles statt Single Score

- [ ] **5D-Governance-Mapping**
  - Datei: `04_oekonomie_governance/5D_GOVERNANCE_MAP.md`
  - Tabelle: Welche 5D-Komponenten in realen Fallstudien?
    - Medellín: SP (soziale Kohäsion), R (Resilienz nach Gewalt)
    - Curitiba: IM (intrinsische Motivation für ÖPNV), A (Autonomie der Stadtplanung)
    - Ostrom Commons: Au (Authentizität der Regeln), SP (Community-Partizipation)
  - Links im Knowledge Graph (`WISSENS_INDEX.md`)

---

## 8. Informations- und Kausalmodelle

**Ziel:** Kausalität ohne versteckte Zwangsmechanismen

- [ ] **Research Scraper erweitern**
  - In `5d_research_scraper.py`:
    - Tag-System für Kausalmodelle:
      - `causal_model` (yes/no)
      - `coercion_type` (none, nudge, mandate, incentive)
      - `persuasion_mechanism` (information, social proof, defaults)
    - Strukturierte Speicherung in `5d_research_data.json`:
      ```json
      {
        "paper_id": "arxiv_1234",
        "tags": ["causal_model", "non_coercive"],
        "persuasion": {
          "mechanism": "information",
          "autonomy_preserved": true
        }
      }
      ```

- [ ] **Kausalgraph-Bibliothek anlegen**
  - In `analysis/causal_graphs.py`:
    - NetworkX-basierte Wrapper für DAGs (Directed Acyclic Graphs)
    - Do-Kalkül (Pearl): P(Y | do(X)) vs. P(Y | X)
    - Interventions-API: `simulate_intervention(graph, node, value)`
  - Beispiel: Bildungsinterventionen (ohne Coercion)

- [ ] **Prototypische Kausal-Graphen modellieren**
  - Datei: `analysis/social_interaction_graphs.py`
  - Graphen:
    - **Non-Coercive Persuasion:** Information → Belief Update → Behavior (no hidden nudges)
    - **Coercive Nudge:** Default → Behavior (bypassing deliberation)
  - Metriken:
    - Autonomy Score = P(deliberation | intervention)
    - Transparency Score = Shannon Entropy of causal paths
  - Visualisierung in `5d_dashboard.py` (neue Page oder Integration)

- [ ] **Nudge-Vergleich dokumentieren**
  - Datei: `04_oekonomie_governance/NUDGES_VS_5D.md`
  - Vergleichskriterien:
    - **Dauerhaftigkeit** (behavior change persistence)
    - **Autonomie** (preserved vs. compromised)
    - **Kontextsensitivität** (adaptive vs. one-size-fits-all)
    - **Transparenz** (disclosed vs. hidden)
  - Beispiele: Opt-out organ donation (nudge) vs. informed consent (5D)

---

## 9. Abgrenzung zu „5D"-Mythologien & anderen 5D-Frameworks

**Ziel:** Klare Differenzierung, keine Verwechslung mit Esoterik

- [ ] **5D-Landschaft dokumentieren**
  - Datei: `06_synthesen_kompilationen/5d_landschaft.md`
  - Modelle:
    - **Islamisches 5D-Bildungsmodell** (Körper, Geist, Seele, Sozial, Spirituell)
    - **Policy-5D** (Policy-Evaluationsframework, 5 Kriterien)
    - **AIR-5D** (Accountability, Impartiality, Responsiveness, Democracy, Rule of Law)
    - **Touristische 5D-Resilienz** (Destination Resilience, 5 Faktoren)
    - **New-Age-5D-Bewusstsein** (Lichtkörper, Dimensionsaufstieg, Esoterik)

- [ ] **Kriterienkatalog entwickeln**
  - Kriterien:
    - **Domäne** (Bildung, Policy, Tourismus, Spiritualität, Neurobiologie, etc.)
    - **Ziel** (Beschreibung, Evaluation, Transformation, Erleuchtung, etc.)
    - **Empirie** (peer-reviewed, anekdotisch, keine, metaphysisch)
    - **Zwangsgrad** (explizit thematisiert, implizit, irrelevant, fördernd)
    - **Relation zu 5d-Framework** (kompatibel, orthogonal, inkompatibel, metaphysisch)

- [ ] **Vergleichstabelle erstellen**
  - In `README.md` und `VISION.md`:
    - Markdown-Tabelle mit allen 5D-Modellen
    - Spalten: Name, Domäne, Ziel, Empirie, Zwangsgrad, Relation
    - Farbcodierung: ✅ (kompatibel), ⚠️ (orthogonal), ❌ (inkompatibel)

- [ ] **Warnung in Doku platzieren**
  - In `README.md` (Einleitung):
    > ⚠️ **Terminologie-Warnung:** „5D" ist in vielen Kontexten überladen.
    > Unser 5D-Intelligenzframework ist **nicht**:
    > - New-Age-5D-Bewusstsein (Lichtkörper, Dimensionsaufstieg)
    > - 5. physikalische Dimension (Kaluza-Klein, String Theory)
    > - Islamisches 5D-Bildungsmodell (Körper/Geist/Seele/Sozial/Spirituell)
    > 
    > Definition siehe [VISION.md](VISION.md).

---

## 10. Empirische Testbarkeit & Minimal-Experimente

**Ziel:** Wissenschaftliche Validierung, keine Spekulation ohne Test

- [ ] **Kernbehauptungen auflisten**
  - Datei: `docs/CLAIMS_EVIDENCE_MATRIX.md`
  - Format:
    ```markdown
    | Behauptung | Evidenz-Level | Domain | Datenquelle | Status |
    |------------|---------------|--------|-------------|--------|
    | Nicht-koerzitive Systeme sind resilienter | Hypothese | Öko | Vegetation Patterns | Testbar |
    | IMP korreliert mit Life Satisfaction | Hypothese | Sozial | Survey Data | In Arbeit |
    | Flow-Zustände sind nicht-koerzitiv | Fakt | Neuro | fMRI Studies | Validiert |
    ```
  - Evidenz-Level: Fakt ✅, Hypothese ⚠️, Spekulation 🔮

- [ ] **Domains/Datenquellen identifizieren**
  - Für jede Behauptung:
    - **Neuro:** EEG, fMRI, MEG (Flow, DMN, Polyvagal)
    - **Öko:** Remote Sensing, Biodiversity Databases, Vegetation Patterns
    - **Sozial:** Surveys, Longitudinal Studies, Governance Indicators
    - **Governance:** WGI, Participatory Budgeting Data, Case Studies
    - **Urban:** Census Data, GIS, Urban Planning Records

- [ ] **Minimalexperiment 1: Game of Life**
  - Erweitern: `python game_of_life.py`
  - Varianten:
    - **Koerzitiv:** Erzwungene Muster (seed patterns, boundary conditions)
    - **Nicht-koerzitiv:** Random initialization, keine Constraints
  - Metriken:
    - Musterdiversität (unique patterns, entropy)
    - Lebensdauer (generations until stable/extinction)
    - Entropie (Shannon-Entropie der Zellzustände)
  - Hypothese: Nicht-koerzitiv → höhere Diversität langfristig

- [ ] **Minimalexperiment 2: Governance-Panel**
  - In `5d_dashboard.py` (neue Page oder Integration):
    - Reale Governance-Indikatoren (WGI: Voice & Accountability)
    - Outcome-Proxies (HDI, Life Satisfaction, Resilience Indices)
    - Scatterplot: WGI Voice vs. HDI (Korrelation r ≈ 0.7)
    - Hypothese: Höhere Autonomie → bessere Outcomes

- [ ] **Roadmap dokumentieren**
  - In `NEXT_STEPS.md`:
    - **Q1 2026:** Minimalexperimente 1+2 implementieren
    - **Q2 2026:** Survey-Daten sammeln (n > 100)
    - **Q3 2026:** Neurobiologische Daten (EEG, n > 30)
    - **Q4 2026:** Erste Publikation (preprint, peer-review)

---

## 11. Integration ins 5d-Repo

**Ziel:** Forschung in bestehende Strukturen einbetten

- [ ] **README.md und VISION.md erweitern**
  - Neue Sektion: „Forschungsstand & offene Fragen"
  - Verweise auf:
    - `TODO_RESEARCH.md` (diese Datei)
    - `docs/CLAIMS_EVIDENCE_MATRIX.md` (Evidenzmatrix)
    - `ETHIK_MANIFEST.md` (Forschungsethik)
    - `02_neurobiologie_psychologie/`, `03_philosophie_epistemologie/`, etc.

- [ ] **TODO-Listen konsolidieren**
  - Dateien: `TODO.md`, `TODO_MULTIPAGE.md`, `TODO_RESEARCH.md`
  - Dopplungen auflösen:
    - `TODO.md` → Infrastruktur, Deployment, CI/CD
    - `TODO_MULTIPAGE.md` → Dashboard-Features, UI/UX
    - `TODO_RESEARCH.md` → Wissenschaftliche Grundlagen, Experimente
  - Cross-Links zwischen Dateien

- [ ] **Dashboard-Links zu Forschung**
  - In `5d_dashboard.py`, `bewusstsein_evolution.html`, `web/5d-map`:
    - Tooltips/Expandables mit Evidenzlabels:
      - ✅ **Fakt:** Link zu peer-reviewed Paper
      - ⚠️ **Hypothese:** Link zu Experiment-Plan
      - 🔮 **Spekulation:** Explizite Warnung, Link zu offenen Fragen
    - Beispiel: IMP-Score Tooltip → „Basierend auf Deci & Ryan 1985 ✅"

- [ ] **GitHub-Issue-Templates anlegen**
  - `.github/ISSUE_TEMPLATE/`:
    - `research_neuro.md` (Neurobiologie-Fragen)
    - `research_eco.md` (Ökologie-Fragen)
    - `theory.md` (Theoretische Fragen)
    - `ethics.md` (Ethik-Fragen)
  - Operationalisierung dieser TODO-Liste über Issues

---

## 12. Reflexion & Ethik

**Ziel:** Transparenz, Bias-Bewusstsein, Abbruchkriterien

- [ ] **ETHIK_MANIFEST.md anlegen**
  - Location: Root oder `docs/`
  - Inhalte:
    - **Bias-Log:** Wo dominiert persönliche Intuition?
    - **Abbruch-/Umbaukriterien:** Wann ist das Framework falsifiziert?
    - **Forschungs-Ethos:** „Mit mir selbst schlafen können"
      - Transparenz über Unsicherheiten
      - Keine Überverkauf von Hypothesen als Fakten
      - Offenheit für Kritik und Falsifikation

- [x] **Evidenzmatrix transparent machen** ✅
  - In `docs/CLAIMS_EVIDENCE_MATRIX.md`:
    - Spalte: „Evidenz-Stärke" (stark, mittel, schwach, keine)
    - Spalte: „Persönliche Intuition" (hoch, mittel, niedrig)
    - Warnung: Wo Intuition > Evidenz → explizit als Spekulation kennzeichnen
  - **Status:** 40 Behauptungen dokumentiert (45% Fakt, 40% Hypothese, 15% Spekulation)

- [ ] **Repo-Selbst-Tracking**
  - Nutzen: `5d_github_api.py` + `5d_github_data.json`
  - Metriken:
    - Evolution von Struktur (Ordner, Dateien, LOC)
    - Issues & Pull Requests (Anteil Forschung vs. Engineering)
    - Doku-Qualität (Anteil Fakten vs. Hypothesen vs. Spekulationen)
  - Fallstudie: Repo als Beispiel für transparente Forschung

- [ ] **Regelmäßige Reflexions-Checkpoints**
  - Frequenz: Alle 3 Monate
  - Aufgaben:
    - Review dieser TODO-Liste (Fortschritt, neue Fragen)
    - Ethik-Sektion aktualisieren (Bias-Log, Evidenzmatrix)
    - Abbruchkriterien prüfen (Wurde etwas falsifiziert?)
  - Dokumentation in `docs/REFLEXION_LOG.md`

---

## Priorisierung & Roadmap

### Phase 1 (Q1 2026) – Grundlagen
- [ ] 0. Meta: Repository-Struktur, Literatur-Index, Dokumentationsstandard
- [ ] 1. 5D-Begriff: Präzise Definition, Abgrenzung, Vergleichstabelle
- [ ] 10. Testbarkeit: Kernbehauptungen, Evidenzmatrix, Minimalexperimente

### Phase 2 (Q2 2026) – Empirische Validierung
- [ ] 2. Neuro: Literatur, Netzwerk-Topologie, Inhibitionsmodell
- [ ] 4. Öko: Survey-Modul, Auswertungslogik, Agency-Score
- [ ] 7. Governance: Fallstudien, Metriken, Dashboard-Integration

### Phase 3 (Q3 2026) – Theoretische Vertiefung
- [ ] 3. Philosophie: Phänomenologie, Bewusstseinszustand, UI-Flows
- [ ] 5. Gaia: Vergleichsdokument, Simulation, Gaia-Mapping
- [ ] 8. Kausalmodelle: Scraper-Erweiterung, Kausalgraph-Bibliothek

### Phase 4 (Q4 2026) – Integration & Reflexion
- [ ] 6. Ökosysteme: Hypermutabilität, Evolvabilität, Datensätze
- [ ] 9. Abgrenzung: 5D-Landschaft, Kriterienkatalog, Warnung
- [ ] 11. Integration: README, TODO-Konsolidierung, Issue-Templates
- [ ] 12. Reflexion: Ethik-Manifest, Evidenzmatrix, Checkpoints

---

**Status:** Draft (2025-12-02)  
**Nächster Schritt:** Priorisierung mit Team/Community diskutieren  
**Kontakt:** Siehe `CONTRIBUTING.md` für Beiträge zu dieser Roadmap
