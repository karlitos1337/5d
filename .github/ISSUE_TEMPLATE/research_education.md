---
name: 🎓 Education Research
about: Propose or discuss alternative education research (ROI, case studies, evaluations)
title: "[EDU] "
labels: research, education, alternative-schools
assignees: ''
---

## 🎓 Research Question

**Brief Description:**
<!-- What education question are you investigating? -->

**School Type:**
<!-- Check all that apply -->
- [ ] Sudbury School
- [ ] Summerhill
- [ ] Folk High School
- [ ] Montessori
- [ ] Waldorf/Steiner
- [ ] Democratic School
- [ ] Free School
- [ ] Other: ___________

---

## 📖 Literature Review

**Key References (ROI/Outcomes):**
<!-- List 3-5 studies on educational outcomes, ROI, or long-term impact -->

1. [Author Year] - Title (e.g., Heckman 2006, Schweinhart 2005)
   - BibTeX: `key_if_exists`
   - ROI/BCR: ___ (if applicable)
   - **Evidenz:** ✅ Fakt / ⚠️ Hypothese / 🔮 Spekulation

2. [Author Year] - Title
   - BibTeX: `key_if_exists`
   - Outcome Metric: _____ (e.g., Dropout Rate, Life Satisfaction)
   - **Evidenz:** ✅ Fakt / ⚠️ Hypothese / 🔮 Spekulation

3. ...

**Gaps in Current Literature:**
<!-- What's missing? Longitudinal data? Counterfactual analysis? -->

---

## 🧪 Proposed Methodology

**Study Design:**
<!-- Case study? Survey? RCT? Quasi-experimental? -->

**Sample:**
<!-- How many schools? How many students? Comparison group? -->

**Data Collection:**
<!-- Academic records? Surveys? Interviews? Observation? -->

**Timeframe:**
<!-- Cross-sectional? Longitudinal (5-10 years)? -->

---

## 📊 Expected Outcomes

**Hypothesis:**
<!-- e.g., "Alternative schools have 50% lower dropout rates than mainstream" -->

**Success Criteria:**
<!-- e.g., "t-Test p < 0.05, n > 30 schools" -->

**ROI Calculation (if applicable):**
<!-- Using Heckman methodology? Perry Preschool BCR 7.16 as baseline? -->

**5D Scores (if applicable):**
<!-- Expected A/IM/R/SP/Au scores? Comparison to mainstream? -->

---

## 🔗 Integration with 5D Framework

**Impact on IMP Formula:**
<!-- Do alternative schools have higher IMP scores? -->

**Dashboard Integration:**
<!-- Add to pages/2_🚀_Projects.py? New case study? -->

**Test Coverage:**
<!-- Add tests to tests/test_projects.py or tests/test_education_roi.py? -->

---

## 📋 Checklist

**Before Starting:**
- [ ] Read [ETHIK_MANIFEST.md](../../ETHIK_MANIFEST.md) (Selection Bias, Survivorship Bias)
- [ ] Read [CLAIMS_EVIDENCE_MATRIX.md](../../docs/CLAIMS_EVIDENCE_MATRIX.md) (claims 2.1-2.5)
- [ ] Check existing case studies in [manifest/01_bildung_education/](../../manifest/01_bildung_education/)
- [ ] Identify comparison group (mainstream schools with similar demographics)

**During Research:**
- [ ] Document selection process (avoid cherry-picking successful schools)
- [ ] Collect negative cases (dropouts, failures) - not just success stories
- [ ] Ethics: Informed Consent from schools, students, parents
- [ ] DSGVO: Anonymize personal data (`storage/anonymize.py`)

**After Research:**
- [ ] Add BibTeX entries to `07_daten_analysen/5d-relevant-sources.bib`
- [ ] Update `docs/CLAIMS_EVIDENCE_MATRIX.md` (section 2: Bildung)
- [ ] Add case study to `manifest/01_bildung_education/` (if applicable)
- [ ] Add tests (e.g., `tests/test_education_roi.py`)
- [ ] Update `pages/2_🚀_Projects.py` (if applicable)

---

## 📖 See Also

- **[TODO_RESEARCH.md](../../TODO_RESEARCH.md)** – Section 1 (5D-Begriff), Section 3 (Philosophie)
- **[tests/test_projects.py](../../tests/test_projects.py)** – Existing ROI tests (Perry, Abecedarian, Sudbury)
- **[manifest/01_bildung_education/](../../manifest/01_bildung_education/)** – Existing education resources
- **Heckman Methodology:** Schweinhart et al. (2005), Heckman (2006) for NPV calculation
