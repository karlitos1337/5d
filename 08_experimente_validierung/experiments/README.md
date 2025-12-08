# Validation Experiments

## Overview

This directory contains all validation experiments following the **Rapid Validation Protocol** defined in `../rapid_validation.md`.

---

## Experiments

### ✅ Experiment 01: Autonomy → Shannon Entropy

**File**: `01_autonomy_entropy.py`

**Hypothesis**: IF autonomy ↑ THEN Shannon-entropy ↑ BECAUSE intrinsic exploration

**Method**:
- Simulate learning tasks with varying autonomy levels (0.2 vs 0.9)
- Measure choice diversity using Shannon entropy
- N=30 per group, seed=42 for reproducibility

**Run**:
```bash
python 08-experimente-validierung/experiments/01_autonomy_entropy.py
```

**Expected Outcome**:
- Cohen's d > 0.5
- p < 0.05
- Higher autonomy → higher entropy

---

## Adding New Experiments

1. Create `0X_hypothesis_name.py`
2. Follow template from `01_autonomy_entropy.py`
3. Use `ExperimentResult` dataclass
4. Save raw data to `../data/`
5. Save result to `../results/`
6. Document here

---

## Validation Criteria

All experiments must meet:

- ✅ Effect size (Cohen's d) > 0.5
- ✅ Statistical significance (p < 0.05)
- ✅ Sample size N ≥ 20
- ✅ Reproducible (seed documented)
- ✅ Raw data saved

See `../rapid_validation.md` for full protocol.
