"""Resonanz-Mapping

Projektionen zwischen 5D-Dimensionen oder auf niedrigere Dimensionen.
Stubs mit klaren Interfaces zur späteren Ausarbeitung.
"""

from collections.abc import Mapping


def project_5d_to_3d(dim_scores: Mapping[str, float]) -> dict[str, float]:
    """Projiziert 5D-Scores (0–1) grob auf drei Achsen.

    Beispielachsen: "Mind" (Neuro+Psych), "Society" (Philo+Econ), "Tech" (Tech).
    """
    mind = (
        dim_scores.get("neurobiology", 0.0) + dim_scores.get("psychology", 0.0)
    ) / 2.0
    society = (
        dim_scores.get("philosophy", 0.0) + dim_scores.get("economics", 0.0)
    ) / 2.0
    tech = dim_scores.get("technology", 0.0)
    return {"mind": mind, "society": society, "tech": tech}
