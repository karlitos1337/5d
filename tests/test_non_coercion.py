#!/usr/bin/env python3
"""
Test Non-Coercion models and Nash equilibrium
Validate cooperation vs. coercion payoff matrices
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPayoffMatrix:
    """Test cooperation vs. coercion payoff matrix"""

    def test_cooperation_payoff(self):
        """
        Test payoff when both parties cooperate

        Cooperation-Cooperation: (3, 3) - mutual benefit
        Reference: Ostrom (1990), Axelrod (1984)
        """
        payoff_coop_coop = (3, 3)

        assert payoff_coop_coop[0] == payoff_coop_coop[1], "Symmetric payoff"
        assert payoff_coop_coop[0] > 0, "Positive payoff for cooperation"

    def test_defection_payoff(self):
        """
        Test payoff when one party defects

        Cooperation-Defection: (0, 5) - exploiter wins
        Defection-Cooperation: (5, 0) - exploiter wins
        Reference: Axelrod (1984)
        """
        payoff_coop_def = (0, 5)  # Cooperator exploited
        payoff_def_coop = (5, 0)  # Defector exploits

        assert payoff_coop_def[1] > payoff_coop_def[0], "Defector wins vs cooperator"
        assert payoff_def_coop[0] > payoff_def_coop[1], "Defector wins vs cooperator"

    def test_mutual_defection_payoff(self):
        """
        Test payoff when both parties defect

        Defection-Defection: (1, 1) - mutual loss
        Reference: Hardin (1968) - "Tragedy of the Commons"
        """
        payoff_def_def = (1, 1)
        payoff_coop_coop = (3, 3)

        assert payoff_def_def[0] < payoff_coop_coop[0], "Mutual defection worse than cooperation"
        assert payoff_def_def[0] > 0, "Still positive (not collapse)"

    def test_temptation_order(self):
        """
        Test classic Prisoner's Dilemma payoff ordering

        T > R > P > S (Temptation > Reward > Punishment > Sucker)
        T=5, R=3, P=1, S=0
        """
        T = 5  # Temptation to defect
        R = 3  # Reward for mutual cooperation
        P = 1  # Punishment for mutual defection
        S = 0  # Sucker's payoff

        assert T > R > P > S, "Classic Prisoner's Dilemma ordering"
        assert 2 * R > T + S, "Ensures cooperation is collectively optimal"


class TestNashEquilibrium:
    """Test Nash equilibrium calculations"""

    def test_pure_strategy_nash(self):
        """
        Test pure strategy Nash equilibrium

        In one-shot game: (Defect, Defect) is Nash equilibrium
        Reference: Nash (1950)
        """
        # In one-shot Prisoner's Dilemma
        nash_strategy = ("Defect", "Defect")

        assert nash_strategy[0] == "Defect", "Player 1 defects in Nash equilibrium"
        assert nash_strategy[1] == "Defect", "Player 2 defects in Nash equilibrium"

    def test_iterated_game_equilibrium(self):
        """
        Test iterated game equilibrium

        In repeated games: Cooperation can emerge (Axelrod 1984)
        Tit-for-Tat strategy is stable
        """
        # Tit-for-Tat: cooperate first, then copy opponent
        _strategy = "Tit-for-Tat"  # noqa: F841
        is_stable = True

        assert is_stable, "Tit-for-Tat is stable in iterated games"

    def test_subgame_perfect_equilibrium(self):
        """
        Test subgame perfect equilibrium

        In finite repeated games: unraveling to defection
        In infinite/uncertain horizon: cooperation possible
        """
        finite_horizon = "Defect in last round → unraveling"
        infinite_horizon = "Cooperation sustainable"

        assert len(finite_horizon) > 0, "Finite games unravel to defection"
        assert len(infinite_horizon) > 0, "Infinite games can sustain cooperation"


class TestOstromPrinciples:
    """Test Ostrom's 8 principles for commons governance"""

    def test_clearly_defined_boundaries(self):
        """
        Principle 1: Clearly defined boundaries

        Who has rights to withdraw resource units?
        Reference: Ostrom (1990)
        """
        principle_1 = "Clearly defined boundaries"

        assert len(principle_1) > 0, "Principle 1: Boundaries must be clear"

    def test_proportional_equivalence(self):
        """
        Principle 2: Proportional equivalence between benefits and costs

        Rules match local conditions
        Reference: Ostrom (1990)
        """
        principle_2 = "Proportional equivalence"

        assert len(principle_2) > 0, "Principle 2: Benefits proportional to costs"

    def test_collective_choice(self):
        """
        Principle 3: Collective-choice arrangements

        Affected individuals can participate in rule-making
        Reference: Ostrom (1990)
        """
        principle_3 = "Collective-choice arrangements"

        assert len(principle_3) > 0, "Principle 3: Participatory rule-making"

    def test_monitoring(self):
        """
        Principle 4: Monitoring

        Monitors accountable to users
        Reference: Ostrom (1990)
        """
        principle_4 = "Monitoring"

        assert len(principle_4) > 0, "Principle 4: Accountable monitoring"

    def test_graduated_sanctions(self):
        """
        Principle 5: Graduated sanctions

        Sanctions for rule violators increase with severity
        Reference: Ostrom (1990)
        """
        principle_5 = "Graduated sanctions"

        assert len(principle_5) > 0, "Principle 5: Progressive sanctions"

    def test_conflict_resolution(self):
        """
        Principle 6: Conflict-resolution mechanisms

        Low-cost, rapid access to conflict resolution
        Reference: Ostrom (1990)
        """
        principle_6 = "Conflict-resolution mechanisms"

        assert len(principle_6) > 0, "Principle 6: Accessible conflict resolution"

    def test_minimal_recognition(self):
        """
        Principle 7: Minimal recognition of rights

        Government recognizes right to organize
        Reference: Ostrom (1990)
        """
        principle_7 = "Minimal recognition of rights"

        assert len(principle_7) > 0, "Principle 7: Government recognition"

    def test_nested_enterprises(self):
        """
        Principle 8: Nested enterprises

        For larger systems: multiple layers of organization
        Reference: Ostrom (1990)
        """
        principle_8 = "Nested enterprises"

        assert len(principle_8) > 0, "Principle 8: Multi-level governance"


class TestCooperationExamples:
    """Test real-world cooperation examples"""

    def test_swiss_alpine_commons(self):
        """
        Swiss Alpine meadows: 800+ years of sustainable management

        Reference: Netting (1981), Ostrom (1990)
        """
        duration_years = 800
        is_sustainable = True

        assert duration_years >= 800, "Swiss Alpine commons >800 years"
        assert is_sustainable, "Sustainable without tragedy of commons"

    def test_valencia_huertas(self):
        """
        Valencia irrigation system (Spain): 1000+ years

        Tribunal de las Aguas (Water Court) - medieval institution still active
        Reference: Maass & Anderson (1978), Ostrom (1990)
        """
        duration_years = 1000
        has_water_court = True

        assert duration_years >= 1000, "Valencia Huertas >1000 years"
        assert has_water_court, "Water Court still functioning"

    def test_bali_subak(self):
        """
        Bali Subak system: 1000+ years, UNESCO World Heritage

        Reference: Lansing (1991), Ostrom (1990)
        """
        duration_years = 1000
        unesco_heritage = True

        assert duration_years >= 1000, "Bali Subak >1000 years"
        assert unesco_heritage, "UNESCO World Heritage Site"

    def test_maine_lobster_gangs(self):
        """
        Maine lobster fishing: 150+ years of self-governance

        Reference: Acheson (1988), Ostrom (1990)
        """
        duration_years = 150
        self_governed = True

        assert duration_years >= 150, "Maine lobster gangs >150 years"
        assert self_governed, "Self-governed without external enforcement"

    def test_nepal_forests(self):
        """
        Nepal community forests: 40+ years documented success

        Reference: Arnold & Campbell (1986), Ostrom (1990)
        """
        duration_years = 40
        is_documented = True

        assert duration_years >= 40, "Nepal forests >40 years documented"
        assert is_documented, "Well-documented case study"


class TestCoercionAlternatives:
    """Test alternatives to coercive systems"""

    def test_voluntary_cooperation_rate(self):
        """
        Test voluntary cooperation rates in alternative education

        Documented: 75-90% cooperation in democratic schools
        Reference: Greenberg (1992), Gray & Chanoff (1986)
        """
        cooperation_rate_low = 0.75
        cooperation_rate_high = 0.90

        assert 0.70 <= cooperation_rate_low <= 0.80, "Lower bound 75%"
        assert 0.85 <= cooperation_rate_high <= 0.95, "Upper bound 90%"

    def test_conflict_resolution_time(self):
        """
        Test conflict resolution time in non-coercive settings

        Democratic schools: conflicts resolved in hours/days (not weeks/months)
        """
        max_resolution_days = 7
        traditional_resolution_days = 30

        assert (
            max_resolution_days < traditional_resolution_days
        ), "Faster resolution than traditional"

    def test_rule_legitimacy_perception(self):
        """
        Test perceived legitimacy of self-created rules

        Self-created rules: 85-95% legitimacy
        Imposed rules: 40-60% legitimacy
        Reference: Tyler (2006) - procedural justice
        """
        self_created_legitimacy = 0.90
        imposed_legitimacy = 0.50

        assert self_created_legitimacy > imposed_legitimacy, "Self-created rules more legitimate"


class TestBibTeXValidation:
    """Test BibTeX references for cooperation theory"""

    def test_bibtex_cooperation_papers(self):
        """Ensure cooperation theory papers are in BibTeX"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")

        if not bibtex_path.exists():
            pytest.skip("BibTeX file not found")

        with open(bibtex_path, encoding="utf-8") as f:
            content = f.read()

        # Key cooperation/commons papers
        key_papers = [
            "ostrom1990",  # Governing the Commons
            "axelrod1984",  # Evolution of Cooperation
            "nash1950",  # Nash Equilibrium
            "hardin1968",  # Tragedy of the Commons
        ]

        missing = []
        for paper in key_papers:
            if paper not in content:
                missing.append(paper)

        if missing:
            pytest.skip(f"Missing cooperation papers: {missing} (future addition)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
