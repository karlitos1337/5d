"""
Evolution Simulation - Multi-Crisis Version
============================================

Tests hypothesis: Over MULTIPLE crises, diverse populations survive better than controlled ones.

Previous result (single crisis): Controlled 99%, Free 61%
Expected result (multi-crisis): Free > Controlled (diversity advantage emerges!)

Hypothesis:
- Single crisis: Controlled population optimized for THAT crisis → survives better
- Multiple crises: Diverse population has VARIANTS for EACH crisis → cumulative advantage

Based on:
- Darwin (1859): Natural Selection favors adaptability
- Wright (1932): Shifting Balance Theory
- Gould & Eldredge (1977): Punctuated Equilibrium
"""

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


class Population:
    def __init__(self, size, diversity_mode="free"):
        """
        Initialize population.

        diversity_mode:
        - 'free': Random traits (high diversity)
        - 'controlled': Similar traits (low diversity)
        """
        self.size = size
        self.diversity_mode = diversity_mode

        if diversity_mode == "free":
            # High diversity: traits uniformly distributed [0, 1]
            self.traits = np.random.uniform(0, 1, size)
        else:
            # Low diversity: traits clustered around 0.5
            self.traits = np.random.normal(0.5, 0.1, size)
            self.traits = np.clip(self.traits, 0, 1)  # Keep in [0, 1]

        self.alive = np.ones(size, dtype=bool)
        self.crisis_history = []

    def apply_crisis(self, crisis_type, severity=0.5):
        """
        Apply crisis to population.

        Crisis types:
        - 'low': Survival if trait < 0.5 (favors low traits)
        - 'high': Survival if trait > 0.5 (favors high traits)
        - 'mid': Survival if 0.3 < trait < 0.7 (favors moderate traits)
        - 'extreme': Survival if trait < 0.2 OR trait > 0.8 (favors extremes)

        severity: How harsh the crisis (0 = no deaths, 1 = strict cutoff)
        """
        for i in range(self.size):
            if not self.alive[i]:
                continue

            trait = self.traits[i]

            # Determine survival probability based on crisis type
            if crisis_type == "low":
                # Favors low traits
                fitness = 1 - trait  # trait=0 → fitness=1, trait=1 → fitness=0
            elif crisis_type == "high":
                # Favors high traits
                fitness = trait  # trait=1 → fitness=1, trait=0 → fitness=0
            elif crisis_type == "mid":
                # Favors moderate traits
                distance_from_center = abs(trait - 0.5)
                fitness = 1 - distance_from_center * 2  # trait=0.5 → fitness=1
            elif crisis_type == "extreme":
                # Favors extremes (low OR high)
                distance_from_extremes = min(trait, 1 - trait) * 2
                fitness = 1 - distance_from_extremes  # trait=0 or 1 → fitness=1
            else:
                raise ValueError(f"Unknown crisis type: {crisis_type}")

            # Apply severity
            survival_prob = fitness ** (1 / severity) if severity > 0 else 1

            # Probabilistic survival
            if np.random.random() > survival_prob:
                self.alive[i] = False

        # Record crisis
        survivors = self.alive.sum()
        self.crisis_history.append(
            {
                "type": crisis_type,
                "severity": severity,
                "survivors": survivors,
                "survival_rate": survivors / self.size,
            }
        )

        return survivors

    def get_diversity(self):
        """Calculate Shannon entropy of trait distribution."""
        if self.alive.sum() == 0:
            return 0

        # Bin traits into 10 categories
        alive_traits = self.traits[self.alive]
        hist, _ = np.histogram(alive_traits, bins=10, range=(0, 1))

        # Shannon entropy
        hist = hist / hist.sum()
        hist = hist[hist > 0]  # Remove zeros
        entropy = -np.sum(hist * np.log2(hist))

        return entropy

    def get_stats(self):
        """Get current statistics."""
        alive_traits = self.traits[self.alive]

        return {
            "survivors": self.alive.sum(),
            "survival_rate": self.alive.sum() / self.size,
            "diversity": self.get_diversity(),
            "mean_trait": alive_traits.mean() if len(alive_traits) > 0 else 0,
            "std_trait": alive_traits.std() if len(alive_traits) > 0 else 0,
        }


def run_multi_crisis_experiment(pop_size=1000, num_crises=10, crisis_types=None, severity=0.5):
    """
    Run evolution simulation with multiple crises.

    Args:
        pop_size: Size of each population
        num_crises: Number of crises to apply
        crisis_types: List of crisis types (or None for random)
        severity: Crisis severity (0-1)

    Returns:
        dict: Results for both populations
    """

    # Initialize populations
    pop_free = Population(pop_size, diversity_mode="free")
    pop_controlled = Population(pop_size, diversity_mode="controlled")

    # Random crisis types if not specified
    if crisis_types is None:
        crisis_types = np.random.choice(["low", "high", "mid", "extreme"], num_crises)

    print(f"\n{'='*60}")
    print("🧬 EVOLUTION MULTI-CRISIS EXPERIMENT")
    print(f"{'='*60}")
    print(f"Population Size: {pop_size}")
    print(f"Number of Crises: {num_crises}")
    print(f"Crisis Severity: {severity}")
    print(f"Crisis Sequence: {crisis_types}")
    print(f"{'='*60}\n")

    # Track results
    results = {
        "free": {"initial": pop_free.get_stats(), "crises": []},
        "controlled": {"initial": pop_controlled.get_stats(), "crises": []},
    }

    # Apply crises
    for i, crisis_type in enumerate(crisis_types):
        print(f"Crisis {i+1}/{num_crises}: {crisis_type.upper()}")

        # Apply to both populations
        survivors_free = pop_free.apply_crisis(crisis_type, severity)
        survivors_controlled = pop_controlled.apply_crisis(crisis_type, severity)

        # Get stats
        stats_free = pop_free.get_stats()
        stats_controlled = pop_controlled.get_stats()

        # Record
        results["free"]["crises"].append(stats_free)
        results["controlled"]["crises"].append(stats_controlled)

        print(
            f"  Free: {survivors_free} survivors ({stats_free['survival_rate']*100:.1f}%), diversity={stats_free['diversity']:.2f}"
        )
        print(
            f"  Controlled: {survivors_controlled} survivors ({stats_controlled['survival_rate']*100:.1f}%), diversity={stats_controlled['diversity']:.2f}"
        )
        print()

        # Check extinction
        if survivors_free == 0:
            print("💀 Free population EXTINCT!")
        if survivors_controlled == 0:
            print("💀 Controlled population EXTINCT!")

        if survivors_free == 0 or survivors_controlled == 0:
            break

    # Final results
    print(f"{'='*60}")
    print("📊 FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Free: {pop_free.alive.sum()} survivors ({pop_free.alive.sum()/pop_size*100:.1f}%)")
    print(
        f"Controlled: {pop_controlled.alive.sum()} survivors ({pop_controlled.alive.sum()/pop_size*100:.1f}%)"
    )
    print(f"{'='*60}\n")

    # Add final stats
    results["free"]["final"] = pop_free.get_stats()
    results["controlled"]["final"] = pop_controlled.get_stats()
    results["crisis_types"] = crisis_types.tolist()
    results["pop_size"] = pop_size
    results["severity"] = severity

    return results, pop_free, pop_controlled


def visualize_results(results, pop_free, pop_controlled, save_path=None):
    """Visualize multi-crisis experiment results."""

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("🧬 Evolution Multi-Crisis Experiment", fontsize=16, fontweight="bold")

    num_crises = len(results["free"]["crises"])
    crisis_range = range(1, num_crises + 1)

    # 1. Survival Rate Over Time
    ax = axes[0, 0]
    free_survival = [c["survival_rate"] * 100 for c in results["free"]["crises"]]
    controlled_survival = [c["survival_rate"] * 100 for c in results["controlled"]["crises"]]

    ax.plot(
        crisis_range,
        free_survival,
        "o-",
        label="Free (High Diversity)",
        linewidth=2,
        markersize=8,
        color="#10b981",
    )
    ax.plot(
        crisis_range,
        controlled_survival,
        "s-",
        label="Controlled (Low Diversity)",
        linewidth=2,
        markersize=8,
        color="#ef4444",
    )
    ax.set_xlabel("Crisis Number", fontsize=12)
    ax.set_ylabel("Survival Rate (%)", fontsize=12)
    ax.set_title("Survival Rate Over Multiple Crises", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Diversity Over Time
    ax = axes[0, 1]
    free_diversity = [c["diversity"] for c in results["free"]["crises"]]
    controlled_diversity = [c["diversity"] for c in results["controlled"]["crises"]]

    ax.plot(
        crisis_range, free_diversity, "o-", label="Free", linewidth=2, markersize=8, color="#10b981"
    )
    ax.plot(
        crisis_range,
        controlled_diversity,
        "s-",
        label="Controlled",
        linewidth=2,
        markersize=8,
        color="#ef4444",
    )
    ax.set_xlabel("Crisis Number", fontsize=12)
    ax.set_ylabel("Shannon Entropy", fontsize=12)
    ax.set_title("Diversity Over Multiple Crises", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Cumulative Survival
    ax = axes[0, 2]
    categories = ["Initial", f"After {num_crises} Crises"]
    free_cumulative = [100, results["free"]["final"]["survival_rate"] * 100]
    controlled_cumulative = [100, results["controlled"]["final"]["survival_rate"] * 100]

    x = np.arange(len(categories))
    width = 0.35

    ax.bar(x - width / 2, free_cumulative, width, label="Free", color="#10b981")
    ax.bar(x + width / 2, controlled_cumulative, width, label="Controlled", color="#ef4444")
    ax.set_ylabel("Survival Rate (%)", fontsize=12)
    ax.set_title("Cumulative Survival", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    # 4. Trait Distribution (Free)
    ax = axes[1, 0]
    alive_traits_free = pop_free.traits[pop_free.alive]
    ax.hist(alive_traits_free, bins=20, color="#10b981", alpha=0.7, edgecolor="black")
    ax.set_xlabel("Trait Value", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(
        f"Free Population Traits (n={len(alive_traits_free)})", fontsize=14, fontweight="bold"
    )
    ax.grid(True, alpha=0.3, axis="y")

    # 5. Trait Distribution (Controlled)
    ax = axes[1, 1]
    alive_traits_controlled = pop_controlled.traits[pop_controlled.alive]
    ax.hist(alive_traits_controlled, bins=20, color="#ef4444", alpha=0.7, edgecolor="black")
    ax.set_xlabel("Trait Value", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(
        f"Controlled Population Traits (n={len(alive_traits_controlled)})",
        fontsize=14,
        fontweight="bold",
    )
    ax.grid(True, alpha=0.3, axis="y")

    # 6. Crisis Types
    ax = axes[1, 2]
    crisis_types = results["crisis_types"]
    crisis_counts = {ct: crisis_types.count(ct) for ct in set(crisis_types)}

    colors = {"low": "#3b82f6", "high": "#f59e0b", "mid": "#8b5cf6", "extreme": "#ef4444"}
    ax.bar(
        crisis_counts.keys(),
        crisis_counts.values(),
        color=[colors[ct] for ct in crisis_counts.keys()],
        edgecolor="black",
        linewidth=1.5,
    )
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title("Crisis Type Distribution", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"📊 Visualization saved: {save_path}")

    return fig


if __name__ == "__main__":
    # Run experiment
    results, pop_free, pop_controlled = run_multi_crisis_experiment(
        pop_size=1000, num_crises=10, severity=0.5
    )

    # Visualize
    output_dir = "../08-experimente-validierung/experiments/results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save JSON
    json_path = os.path.join(output_dir, f"evolution_multi_crisis_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved: {json_path}")

    # Save plot
    png_path = os.path.join(output_dir, f"evolution_multi_crisis_{timestamp}.png")
    visualize_results(results, pop_free, pop_controlled, save_path=png_path)

    # Show plot
    plt.show()

    print("\n✅ Multi-crisis experiment complete!")
    print("📊 Hypothesis Test: Does diversity help over multiple crises?")
    print(f"   Free final survival: {results['free']['final']['survival_rate']*100:.1f}%")
    print(
        f"   Controlled final survival: {results['controlled']['final']['survival_rate']*100:.1f}%"
    )

    if results["free"]["final"]["survival_rate"] > results["controlled"]["final"]["survival_rate"]:
        print("   ✅ HYPOTHESIS CONFIRMED: Diversity wins over multiple crises!")
    else:
        print("   ❌ HYPOTHESIS REJECTED: Controlled population still wins")
