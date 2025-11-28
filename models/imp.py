"""
IMP calculation utilities.

Provides verified formulas for raw multiplicative IMP and an optional
weighted additive variant, with safe normalization and clear provenance.
"""

from __future__ import annotations

from typing import Dict
import numpy as np


def calculate_imp_verified(dimensions: Dict[str, float]) -> Dict[str, float | str]:
    """
    Berechnet IMP nach dokumentierter Formel.

    Parameters
    ---------
    dimensions: Dict[str, float]
        Keys expected: 'A', 'IM', 'R', 'SP', 'Au'. Values in [0,1].

    Returns
    -------
    dict
        {
            'raw_multiplicative': float,  # A × IM × R × SP × Au
            'weighted_additive': float,   # Gewichtet, falls verwendet
            'normalized': float,          # Clamp auf [0,1]
            'formula_used': str           # Beschreibung der verwendeten Formel
        }
    """
    # Sicherstellen, dass die Reihenfolge stabil ist
    keys = ['A', 'IM', 'R', 'SP', 'Au']
    vals = [float(dimensions.get(k, 0.0)) for k in keys]

    raw = float(np.prod(vals))

    # Optionale Gewichtung (dokumentieren und konsistent halten)
    weights = {'A': 1.1, 'IM': 1.05, 'R': 1.0, 'SP': 0.95, 'Au': 1.0}
    weighted_sum = sum(dimensions.get(k, 0.0) * weights[k] for k in keys)
    weighted = weighted_sum / sum(weights.values())

    # Normalisierung: Clamp auf [0,1] (kein echtes Min-Max ohne Referenzwerte)
    normalized = max(0.0, min(1.0, raw))

    formula_used = 'A × IM × R × SP × Au' if abs(raw - weighted) < 1e-12 else 'Gewichtet'

    return {
        'raw_multiplicative': raw,
        'weighted_additive': weighted,
        'normalized': normalized,
        'formula_used': formula_used,
    }
