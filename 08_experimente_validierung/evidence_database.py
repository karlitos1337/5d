"""
Evidence Database: Strukturierte Speicherung validierter Hypothesen
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Evidence:
    """Represents a validated scientific claim.

    Attributes:
        hypothesis: Testable claim in IF-THEN format
        effect_size: Cohen's d or equivalent
        p_value: Statistical significance
        n_samples: Sample size
        date_validated: ISO 8601 timestamp
        replications: List of replication studies
        doi: Digital Object Identifier (if published)
        data_path: Path to raw data (CSV)
    """

    hypothesis: str
    effect_size: float
    p_value: float
    n_samples: int
    date_validated: str
    replications: list[str] = field(default_factory=list)
    doi: str | None = None
    data_path: str | None = None

    def is_valid(self) -> bool:
        """Check if evidence meets acceptance criteria."""
        return self.effect_size > 0.5 and self.p_value < 0.05 and self.n_samples >= 20 and len(self.replications) >= 1


class EvidenceDatabase:
    """Manages validated hypotheses with JSON persistence."""

    def __init__(self, db_path: Path = Path("evidence_db.json")):
        self.db_path = db_path
        self.evidences: list[Evidence] = []
        self.load()

    def add(self, evidence: Evidence) -> None:
        """Add evidence if valid, raise ValueError otherwise."""
        if not evidence.is_valid():
            raise ValueError(
                f"Evidence does not meet criteria: "
                f"d={evidence.effect_size}, p={evidence.p_value}, "
                f"n={evidence.n_samples}, replications={len(evidence.replications)}"
            )
        self.evidences.append(evidence)
        self.save()

    def save(self) -> None:
        """Persist to JSON."""
        data = [vars(e) for e in self.evidences]
        self.db_path.write_text(json.dumps(data, indent=2))

    def load(self) -> None:
        """Load from JSON if exists."""
        if self.db_path.exists():
            data = json.loads(self.db_path.read_text())
            self.evidences = [Evidence(**item) for item in data]

    def get_valid_count(self) -> int:
        """Count evidences meeting all criteria."""
        return sum(e.is_valid() for e in self.evidences)


# Example Usage
if __name__ == "__main__":
    db = EvidenceDatabase()

    # Add validated hypothesis
    evidence = Evidence(
        hypothesis="IF autonomy ↑ THEN Shannon-entropy ↑ BECAUSE intrinsic exploration",
        effect_size=0.72,
        p_value=0.003,
        n_samples=45,
        date_validated=datetime.now().isoformat(),
        replications=["study_2024_02"],
        data_path="data/autonomy_entropy_2024.csv",
    )

    try:
        db.add(evidence)
        print(f"✅ Evidence added. Valid count: {db.get_valid_count()}")
    except ValueError as e:
        print(f"❌ {e}")
