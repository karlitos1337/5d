"""5D-Scoring und Aggregation

Implementiert Basisfunktionen für Skalen, Normierung (1–99) und Aggregation.
"""

from collections.abc import Mapping, Sequence


def likert_to_0_1(value: int, scale: Sequence[int] = (1, 2, 3, 4, 5)) -> float:
    """Mappt Likert (Standard 1–5) auf [0,1]."""
    if value not in scale:
        raise ValueError("value not in likert scale")
    mn, mx = min(scale), max(scale)
    return (value - mn) / (mx - mn)


def normalize_to_1_99(x: float) -> int:
    """Mappt [0,1] auf eine integer Skala 1–99.

    Werte werden auf Grenzen geclamped.
    """
    if x <= 0:
        return 1
    if x >= 1:
        return 99
    return max(1, min(99, int(round(1 + x * 98))))


def weighted_aggregate(scores: Mapping[str, float], weights: Mapping[str, float]) -> float:
    """Aggregiert benannte Scores mit passenden Gewichten (Scores in [0,1])."""
    keys = set(scores.keys()) & set(weights.keys())
    if not keys:
        return 0.0
    sw = sum(weights[k] for k in keys)
    if sw == 0:
        return 0.0
    return sum(scores[k] * weights[k] for k in keys) / sw
