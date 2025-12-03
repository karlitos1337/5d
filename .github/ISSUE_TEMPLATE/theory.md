---
name: 🔬 Theoretical Development
about: Propose refinements to 5D theory, IMP formula, or conceptual framework
title: "[THEORY] "
labels: theory, 5D-framework, conceptual
assignees: ''
---

## 🔬 Theoretical Question

**Brief Description:**
<!-- What theoretical issue are you addressing? -->

**Motivation:**
<!-- Why is this important? What problem does it solve? -->

---

## 📖 Current State

**Existing Framework:**
<!-- What's the current theory/formula/concept? -->

**Example:**
```
IMP = A × IM × R × SP × Au (multiplicative)
```

**Limitations:**
<!-- What's problematic? (e.g., "Multiplicative → 0 if any dimension = 0, unrealistic") -->

---

## 💡 Proposed Refinement

**New Framework:**
<!-- What's your alternative/refinement? -->

**Example:**
```
IMP = α₁×A + α₂×IM + α₃×R + α₄×SP + α₅×Au (weighted additive)
or
IMP = (A × IM × R × SP × Au)^(1/5) (geometric mean)
```

**Justification:**
<!-- Why is this better? Theoretical arguments? Empirical precedent? -->

---

## 🧪 Testability

**Falsifiable Predictions:**
<!-- What would prove/disprove your refinement? -->

**Comparison:**
<!-- How does your formula compare to current IMP? -->
- [ ] Better correlation with Life Satisfaction (r > 0.60)
- [ ] Better fit with real data (RMSE, AIC/BIC)
- [ ] More intuitive (face validity)
- [ ] Other: ___________

**Abort Criteria:**
<!-- When would you abandon your refinement? (e.g., "If r < 0.30") -->

---

## 🔗 Integration with 5D Framework

**Impact on Existing Code:**
<!-- Which files need updates? -->
- [ ] `models/imp.py` (core formula)
- [ ] `tests/test_imp_scientific.py` (validation tests)
- [ ] `pages/1_📊_IMP_Analysis.py` (dashboard)
- [ ] `docs/CLAIMS_EVIDENCE_MATRIX.md` (update claim 8.2)
- [ ] Other: ___________

**Backward Compatibility:**
<!-- Can we keep old formula as option? Gradual migration? -->

---

## 📋 Checklist

**Before Proposing:**
- [ ] Read [CLAIMS_EVIDENCE_MATRIX.md](../../docs/CLAIMS_EVIDENCE_MATRIX.md) (section 8: 5D-Framework)
- [ ] Read [5d_landschaft.md](../../06_synthesen_kompilationen/5d_landschaft.md) (7 alternative 5D models)
- [ ] Check existing formulas in `models/imp.py`
- [ ] Review scientific basis (SDT, Flow Theory, Polyvagal Theory)

**During Development:**
- [ ] Write tests FIRST (TDD: `tests/test_imp_refinement.py`)
- [ ] Compare with existing formula (correlation, RMSE)
- [ ] Document assumptions (linear? multiplicative? weighted?)
- [ ] Check mathematical stability (division by zero? overflow?)

**After Implementation:**
- [ ] Update `docs/CLAIMS_EVIDENCE_MATRIX.md` (mark old formula as deprecated, new as hypothesis)
- [ ] Update `CHANGELOG.md` (breaking change?)
- [ ] Update `models/schemas.py` (Pydantic validation)
- [ ] Update all dependent code (dashboard, analysis scripts)
- [ ] Run full test suite: `pytest tests/ -v`

---

## 📖 See Also

- **[TODO_RESEARCH.md](../../TODO_RESEARCH.md)** – Section 1 (5D-Begriff), Section 11 (Integration)
- **[models/imp.py](../../models/imp.py)** – Current IMP implementation
- **[tests/test_imp_scientific.py](../../tests/test_imp_scientific.py)** – 11 scientific validation tests
- **[5d_landschaft.md](../../06_synthesen_kompilationen/5d_landschaft.md)** – Alternative 5D models
- **Scientific References:**
  - Deci & Ryan (1985) – Self-Determination Theory
  - Csíkszentmihályi (1990) – Flow Theory
  - Porges (2011) – Polyvagal Theory
