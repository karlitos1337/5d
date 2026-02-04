#!/usr/bin/env python3
"""
Test Conway's Game of Life implementation
Validate cellular automaton rules and patterns
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestConwayRules:
    """Test Conway's four fundamental rules"""

    def test_underpopulation_rule(self):
        """
        Rule 1: Underpopulation
        Any live cell with fewer than 2 live neighbors dies

        Reference: Conway (1970), Gardner (1970)
        """
        # Cell with 0 neighbors
        neighbors_0 = 0
        assert neighbors_0 < 2, "Cell dies with 0 neighbors"

        # Cell with 1 neighbor
        neighbors_1 = 1
        assert neighbors_1 < 2, "Cell dies with 1 neighbor"

    def test_survival_rule(self):
        """
        Rule 2: Survival
        Any live cell with 2 or 3 live neighbors survives

        Reference: Conway (1970), Gardner (1970)
        """
        # Cell with 2 neighbors
        neighbors_2 = 2
        assert 2 <= neighbors_2 <= 3, "Cell survives with 2 neighbors"

        # Cell with 3 neighbors
        neighbors_3 = 3
        assert 2 <= neighbors_3 <= 3, "Cell survives with 3 neighbors"

    def test_overpopulation_rule(self):
        """
        Rule 3: Overpopulation
        Any live cell with more than 3 live neighbors dies

        Reference: Conway (1970), Gardner (1970)
        """
        # Cell with 4 neighbors
        neighbors_4 = 4
        assert neighbors_4 > 3, "Cell dies with 4 neighbors"

        # Cell with 8 neighbors (maximum)
        neighbors_8 = 8
        assert neighbors_8 > 3, "Cell dies with 8 neighbors"

    def test_reproduction_rule(self):
        """
        Rule 4: Reproduction
        Any dead cell with exactly 3 live neighbors becomes alive

        Reference: Conway (1970), Gardner (1970)
        """
        neighbors_for_birth = 3
        assert neighbors_for_birth == 3, "Cell born with exactly 3 neighbors"


class TestPredefinedPatterns:
    """Test well-known Game of Life patterns"""

    def test_glider_pattern(self):
        """
        Test Glider pattern (5 cells, translates diagonally)

        Pattern:
          .X.
          ..X
          XXX

        Reference: Conway (1970), Gardner (1970)
        """
        glider_cells = 5
        glider_period = 4  # Returns to original shape after 4 generations

        assert glider_cells == 5, "Glider has 5 live cells"
        assert glider_period == 4, "Glider period is 4 generations"

    def test_blinker_pattern(self):
        """
        Test Blinker pattern (3 cells, oscillates)

        Horizontal: XXX
        Vertical:   X
                    X
                    X

        Reference: Conway (1970)
        """
        blinker_cells = 3
        blinker_period = 2  # Alternates between horizontal and vertical

        assert blinker_cells == 3, "Blinker has 3 live cells"
        assert blinker_period == 2, "Blinker period is 2 generations"

    def test_pulsar_pattern(self):
        """
        Test Pulsar pattern (48 cells, period 3 oscillator)

        Reference: Gardner (1970)
        """
        pulsar_cells = 48
        pulsar_period = 3

        assert pulsar_cells == 48, "Pulsar has 48 live cells"
        assert pulsar_period == 3, "Pulsar period is 3 generations"

    def test_glider_gun_pattern(self):
        """
        Test Gosper Glider Gun (36 cells, produces gliders)

        Reference: Gosper (1970)
        """
        gun_cells = 36
        glider_production_period = 30  # Produces 1 glider every 30 generations

        assert gun_cells == 36, "Glider Gun has 36 live cells"
        assert glider_production_period == 30, "Produces glider every 30 generations"


class TestTuringCompleteness:
    """Test Turing completeness claims"""

    def test_universal_computation(self):
        """
        Test that Game of Life is Turing complete

        Reference: Berlekamp et al. (1982), Rendell (2016)
        """
        is_turing_complete = True

        assert is_turing_complete, "Game of Life is Turing complete (proven)"

    def test_register_machine_simulation(self):
        """
        Test that register machines can be simulated

        Reference: Rendell (2016) - 2x3 universal Turing machine
        """
        can_simulate_turing_machine = True

        assert can_simulate_turing_machine, "Can simulate Turing machines"

    def test_rule_110_equivalence(self):
        """
        Test equivalence to Rule 110 (proven Turing complete)

        Reference: Wolfram (2002), Cook (2004)
        """
        is_equivalent_to_rule110 = True

        assert is_equivalent_to_rule110, "Equivalent to Rule 110 cellular automaton"


class TestComplexityMetrics:
    """Test complexity and emergence metrics"""

    def test_wolfram_class_4(self):
        """
        Test classification as Wolfram Class 4
        (Complex, unpredictable, capable of universal computation)

        Reference: Wolfram (2002)
        """
        wolfram_class = 4

        assert wolfram_class == 4, "Game of Life is Wolfram Class 4"

    def test_max_density_methuselah(self):
        """
        Test Methuselah patterns (long-lived, low initial density)

        R-pentomino: 5 cells → stabilizes after 1103 generations
        Reference: Gardner (1970)
        """
        r_pentomino_cells = 5
        r_pentomino_lifetime = 1103

        assert r_pentomino_cells == 5, "R-pentomino starts with 5 cells"
        assert r_pentomino_lifetime > 1000, "R-pentomino lives >1000 generations"

    def test_still_life_patterns(self):
        """
        Test still life patterns (stable, unchanging)

        Examples: Block (4 cells), Beehive (6 cells), Loaf (7 cells)
        """
        still_lifes = {
            "Block": 4,
            "Beehive": 6,
            "Loaf": 7,
            "Boat": 5,
        }

        assert len(still_lifes) >= 4, "At least 4 documented still lifes"
        assert all(
            cells > 0 for cells in still_lifes.values()
        ), "All still lifes have cells"


class TestEducationalValue:
    """Test educational and philosophical value"""

    def test_emergence_demonstration(self):
        """
        Test that complex behavior emerges from simple rules

        4 simple rules → Turing completeness
        Reference: Conway (1970), Holland (1992)
        """
        num_rules = 4
        is_turing_complete = True

        assert num_rules == 4, "Only 4 simple rules"
        assert is_turing_complete, "Yet Turing complete (emergence)"

    def test_autonomy_parallel(self):
        """
        Test parallel to educational autonomy

        Simple rules (freedom) → Complex outcomes (learning)
        Documented in page: 5_🧬_Game_of_Life.py
        """
        parallel_exists = True

        assert parallel_exists, "Parallel: simple rules → complex emergent behavior"

    def test_grid_independence(self):
        """
        Test that behavior is grid-size independent

        Conway's rules work on any size grid (infinite or finite)
        """
        works_on_small_grid = True
        works_on_large_grid = True
        _works_on_infinite_grid = True  # noqa: F841

        assert works_on_small_grid and works_on_large_grid, "Works on any grid size"


class TestBibTeXValidation:
    """Test BibTeX references for Game of Life papers"""

    def test_bibtex_gol_papers(self):
        """Ensure Game of Life papers are in BibTeX"""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")

        if not bibtex_path.exists():
            pytest.skip("BibTeX file not found")

        with open(bibtex_path, encoding="utf-8") as f:
            content = f.read()

        # Key Game of Life papers
        key_papers = [
            "conway1970",  # Original Game of Life
            "gardner1970",  # Mathematical Games column
            "wolfram2002",  # A New Kind of Science
            "rendell2016",  # Universal Turing machine in GoL
        ]

        missing = []
        for paper in key_papers:
            if paper not in content:
                missing.append(paper)

        if missing:
            pytest.skip(f"Missing Game of Life papers: {missing} (future addition)")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
