"""Mathematische/ML-Bausteine

Reine, seiteneffektfreie Funktionen mit Type Hints. Lesbar, testbar, erweiterbar.
"""
from typing import Iterable, Sequence
import math


def sigmoid(x: float) -> float:
    """Standard-Sigmoid $\sigma(x)=1/(1+e^{-x})$.

    Args:
        x: Eingabewert
    Returns:
        Wert in [0,1]
    """
    return 1.0 / (1.0 + math.exp(-x))


def softmax(xs: Sequence[float]) -> list[float]:
    """Numerisch stabile Softmax über eine Sequenz.

    Args:
        xs: Werte
    Returns:
        Wahrscheinlichkeitsverteilung (sum=1)
    """
    if not xs:
        return []
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


def min_max_normalize(x: float, min_v: float, max_v: float) -> float:
    """Normiert x auf [0,1] basierend auf Min/Max.

    Clamped falls außerhalb des Bereichs.
    """
    if max_v == min_v:
        return 0.0
    v = (x - min_v) / (max_v - min_v)
    return max(0.0, min(1.0, v))


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    """Skalarprodukt zweier gleich langer Sequenzen."""
    if len(a) != len(b):
        raise ValueError("Vectors must have same length")
    return sum(x * y for x, y in zip(a, b))


def weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    """Gewichtetes Mittel; Gewichte müssen Länge von values haben.

    Rückgabe 0.0, wenn Summe der Gewichte == 0.
    """
    if len(values) != len(weights):
        raise ValueError("values and weights must have same length")
    sw = sum(weights)
    if sw == 0:
        return 0.0
    return sum(v * w for v, w in zip(values, weights)) / sw
