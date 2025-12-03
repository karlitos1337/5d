---
name: 🏛️ Governance Research
about: Propose or discuss governance/economics research (Ostrom, institutions, non-coercion)
title: "[GOV] "
labels: research, governance, economics
assignees: ''
---

## 🏛️ Research Question

**Brief Description:**
<!-- What governance/economics question are you investigating? -->

**Focus Area:**
<!-- Check all that apply -->
- [ ] Commons Governance (Ostrom)
- [ ] Institutional Economics (Acemoglu, North)
- [ ] Non-Coercive Systems
- [ ] Cooperative vs. Coercive Structures
- [ ] Democracy & Voice
- [ ] Other: ___________

---

## 📖 Literature Review

**Key References:**
<!-- List 3-5 studies on governance, institutions, or commons -->

1. [Author Year] - Title (e.g., Ostrom 1990, Acemoglu & Robinson 2012)
   - BibTeX: `key_if_exists`
   - Key Finding: _____ (e.g., "8 principles for stable commons")
   - **Evidenz:** ✅ Fakt / ⚠️ Hypothese / 🔮 Spekulation

2. [Author Year] - Title
   - BibTeX: `key_if_exists`
   - Key Finding: _____
   - **Evidenz:** ✅ Fakt / ⚠️ Hypothese / 🔮 Spekulation

3. ...

**Gaps in Current Literature:**
<!-- What's missing? Quantitative metrics for "non-coercion"? Causal mechanisms? -->

---

## 🧪 Proposed Methodology

**Study Design:**
<!-- Case study? Comparative analysis? Panel data regression? Agent-based model? -->

**Sample:**
<!-- How many countries? Communities? Organizations? -->

**Data Sources:**
<!-- World Bank WGI? OECD? Field data? Surveys? -->

**Operationalization:**
<!-- How do you measure "coercion" vs. "non-coercion"? Voice & Accountability? -->

---

## 📊 Expected Outcomes

**Hypothesis:**
<!-- e.g., "Non-coercive governance (Voice > 0.75) correlates with higher IMP-Proxy (r > 0.60)" -->

**Success Criteria:**
<!-- e.g., "Regression β significant (p < 0.05), n > 30 countries" -->

**Abort Criteria:**
<!-- e.g., "If r < 0.30 → rethink non-coercion concept" -->

---

## 🔗 Integration with 5D Framework

**Impact on IMP-Proxy Formula:**
<!-- Does this research validate (1-Depression) × (1-Dropout) × Governance? -->

**Dashboard Integration:**
<!-- Add to pages/7_🌍_World_Map.py? Update IMP-Proxy formula? -->

**Test Coverage:**
<!-- Add tests to tests/test_world_map_data.py or tests/test_governance.py? -->

---

## 📋 Checklist

**Before Starting:**
- [ ] Read [ETHIK_MANIFEST.md](../../ETHIK_MANIFEST.md) (Ideological Biases: Anti-Coercion)
- [ ] Read [CLAIMS_EVIDENCE_MATRIX.md](../../docs/CLAIMS_EVIDENCE_MATRIX.md) (section 3: Governance)
- [ ] Check existing data sources:
  - World Bank WGI (Voice & Accountability, Governance Effectiveness)
  - OECD Better Life Index
  - UNDP HDI
  - Freedom House
- [ ] Define "coercion" vs. "structure" (avoid conflation)

**During Research:**
- [ ] Document biases (Anti-Coercion bias, Libertarian impulse)
- [ ] Consider cultural context (Western vs. non-Western governance models)
- [ ] Collect data for Global South (not just OECD countries)
- [ ] Version control (Git commits for analysis scripts)

**After Research:**
- [ ] Add BibTeX entries to `07_daten_analysen/5d-relevant-sources.bib`
- [ ] Update `docs/CLAIMS_EVIDENCE_MATRIX.md` (section 3: Ökonomie & Governance)
- [ ] Add tests (e.g., `tests/test_governance.py`)
- [ ] Update `pages/6_🤝_Non_Coercion.py` or `pages/7_🌍_World_Map.py` (if applicable)
- [ ] Write summary in issue comment

---

## 📖 See Also

- **[TODO_RESEARCH.md](../../TODO_RESEARCH.md)** – Section 4 (Ökonomie), Section 8 (Governance-Modelle)
- **[tests/test_non_coercion.py](../../tests/test_non_coercion.py)** – Ostrom principles, Nash equilibrium
- **[tests/test_world_map_data.py](../../tests/test_world_map_data.py)** – IMP-Proxy validation
- **[pages/6_🤝_Non_Coercion.py](../../pages/6_🤝_Non_Coercion.py)** – Non-coercion dashboard page
- **Ostrom (1990):** 8 principles for commons governance (800+ case studies)
- **Acemoglu & Robinson (2012):** Inclusive vs. extractive institutions
