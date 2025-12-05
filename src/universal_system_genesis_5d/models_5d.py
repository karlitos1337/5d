"""High-Level 5D-Modelle

Kombiniert Scoring und Mapping zu einfachen Pipeline-Schritten.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from .formulas_scoring import weighted_aggregate
from .mapping_resonance import project_5d_to_3d


@dataclass(frozen=True)
class FiveDProfile:
    """Repräsentiert ein normiertes 5D-Profil (Scores in [0,1])."""

    neurobiology: float
    psychology: float
    philosophy: float
    economics: float
    technology: float

    def to_dict(self) -> dict[str, float]:
        return {
            "neurobiology": self.neurobiology,
            "psychology": self.psychology,
            "philosophy": self.philosophy,
            "economics": self.economics,
            "technology": self.technology,
        }


def aggregate_5d(profile: FiveDProfile, weights: Mapping[str, float] | None = None) -> float:
    """Aggregiert 5D-Profil zu einem Gesamtwert (0–1)."""
    scores = profile.to_dict()
    if weights is None:
        weights = {k: 1.0 for k in scores.keys()}
    return weighted_aggregate(scores, weights)


def project_profile_to_3d(profile: FiveDProfile) -> dict[str, float]:
    """Bequeme Projektion eines `FiveDProfile` auf 3D-Achsen."""
    return project_5d_to_3d(profile.to_dict())
