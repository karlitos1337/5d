r"""
5D-Kompetenz-Metrik
===================
Mathematische Definitionen für die Berechnung von 5D-Scores.

Basierend auf der System-Genesis-Formel.
"""

import math
import numpy as np

def sigmoid(x):
    r"""Standard-Sigmoid $\sigma(x)=1/(1+e^{-x})$."""
    return 1 / (1 + math.exp(-x))

def softmax(x):
    """Berechnet die Softmax-Funktion."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def min_max_normalize(x, min_val, max_val):
    """Normalisiert x auf [0, 1] basierend auf min_val und max_val."""
    if x < min_val:
        return 0.0
    if x > max_val:
        return 1.0
    if max_val == min_val:
        return 0.0
    return (x - min_val) / (max_val - min_val)

def dot(a, b):
    """Berechnet das Skalarprodukt von a und b."""
    return sum(i * j for i, j in zip(a, b))

def weighted_mean(values, weights):
    """Berechnet das gewichtete arithmetische Mittel."""
    if sum(weights) == 0:
        return 0.0
    return dot(values, weights) / sum(weights)

def calculate_imp_score(autonomy, motivation, resilience, participation, authenticity):
    """
    Berechnet den IMP-Score (Individual Maturity Potential).

    IMP = (A + M + R + P + Au) / 5
    """
    return np.mean([autonomy, motivation, resilience, participation, authenticity])
