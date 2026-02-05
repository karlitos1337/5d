#!/usr/bin/env python3
"""
Game of Life Coercion Experiment
=================================

Vergleicht zwei Varianten:
1. **Koerzitiv**: Erzwungenes Startmuster (Glider, fixed seed)
2. **Nicht-Koerzitiv**: Zufälliges Startmuster (random init, verschiedene Seeds)

Metriken:
- **Musterdiversität**: Shannon-Entropie der Zellzustände
- **Lebensdauer**: Anzahl Generationen bis Stabilität oder Aussterben
- **Stabilität**: Oszillationsfrequenz (Periode-2, Periode-3, chaotisch)

Hypothese: Nicht-koerzitive Variante hat höhere Diversität (H > 0.8)
           und längere Lebensdauer als koerzitive Variante.

Scientific Basis:
- Conway (1970): Game of Life rules
- Wolfram (2002): Class 4 cellular automata (edge of chaos)
- Granovetter (1973): Weak ties → diversity (analogie zu random init)

BibTeX: conway1970game, wolfram2002new, granovetter1973strength
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import entropy, ttest_ind


def game_of_life_step(grid: np.ndarray) -> np.ndarray:
    """Conway's Game of Life step (periodic boundaries)."""
    rows, cols = grid.shape
    neighbors = np.zeros((rows, cols), dtype=int)

    # Count 8 neighbors (periodic boundaries via modulo)
    for i in range(rows):
        for j in range(cols):
            total = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = (i + di) % rows, (j + dj) % cols
                    total += grid[ni, nj]
            neighbors[i, j] = total

    # Rules: Survive (2-3), Birth (exactly 3)
    new_grid = np.zeros((rows, cols), dtype=int)
    new_grid[(grid == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    new_grid[(grid == 0) & (neighbors == 3)] = 1
    return new_grid


def place_glider(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    """Place Glider at (top, left)."""
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)
    h, w = glider.shape
    grid[top : top + h, left : left + w] = glider


def shannon_entropy(grid: np.ndarray) -> float:
    """
    Calculate Shannon entropy of cell states.

    H = -Σ p_i log_2(p_i)

    H = 0: All cells same state (no diversity)
    H = 1: Maximum diversity (50% alive, 50% dead)
    """
    flat = grid.flatten()
    total = len(flat)
    if total == 0:
        return 0.0

    counts = Counter(flat)
    probs = [count / total for count in counts.values()]

    # Use scipy.stats.entropy with base 2
    return entropy(probs, base=2)


def detect_stability(history: list[np.ndarray], window: int = 10) -> tuple[int, str]:
    """
    Detect stability type from grid history.

    Returns:
        (generation, stability_type)
        - "extinct": All cells dead
        - "still_life": No change
        - "period_2": Oscillator period 2
        - "period_3": Oscillator period 3
        - "chaotic": No pattern detected
    """
    if len(history) < window:
        return -1, "chaotic"

    last = history[-1]

    # Extinct?
    if np.sum(last) == 0:
        return len(history) - 1, "extinct"

    # Check for still life (no change)
    if np.array_equal(last, history[-2]):
        return len(history) - 1, "still_life"

    # Check for period-2 oscillator
    if len(history) >= 2 and np.array_equal(last, history[-3]):
        return len(history) - 1, "period_2"

    # Check for period-3 oscillator
    if len(history) >= 3 and np.array_equal(last, history[-4]):
        return len(history) - 1, "period_3"

    return -1, "chaotic"


def simulate_coercive(size: int, steps: int, pattern: str = "glider") -> dict:
    """
    Coercive variant: Fixed seed pattern (Glider).

    Returns metrics: diversity, longevity, stability_type, entropy_history
    """
    grid = np.zeros((size, size), dtype=int)

    if pattern == "glider":
        place_glider(grid, top=1, left=1)
    else:
        raise ValueError(f"Unknown pattern: {pattern}")

    history = [grid.copy()]
    entropy_history = [shannon_entropy(grid)]

    for _ in range(steps):
        grid = game_of_life_step(grid)
        history.append(grid.copy())
        entropy_history.append(shannon_entropy(grid))

        # Early stop if stable
        gen, stability = detect_stability(history)
        if gen >= 0:
            break

    # Final stability check
    gen, stability = detect_stability(history)
    if gen < 0:
        gen = len(history) - 1
        stability = "chaotic"

    return {
        "type": "coercive",
        "pattern": pattern,
        "diversity": np.mean(entropy_history),  # Mean Shannon entropy
        "longevity": gen,  # Generations until stable
        "stability_type": stability,
        "entropy_history": entropy_history,
        "final_entropy": entropy_history[-1],
    }


def simulate_non_coercive(size: int, steps: int, density: float = 0.3, seed: int | None = None) -> dict:
    """
    Non-coercive variant: Random initialization.

    Args:
        density: Probability of alive cell (0.3 = 30% alive)
        seed: Random seed for reproducibility

    Returns metrics: diversity, longevity, stability_type, entropy_history
    """
    if seed is not None:
        np.random.seed(seed)

    grid = (np.random.rand(size, size) < density).astype(int)

    history = [grid.copy()]
    entropy_history = [shannon_entropy(grid)]

    for _ in range(steps):
        grid = game_of_life_step(grid)
        history.append(grid.copy())
        entropy_history.append(shannon_entropy(grid))

        # Early stop if stable
        gen, stability = detect_stability(history)
        if gen >= 0:
            break

    # Final stability check
    gen, stability = detect_stability(history)
    if gen < 0:
        gen = len(history) - 1
        stability = "chaotic"

    return {
        "type": "non_coercive",
        "seed": seed,
        "density": density,
        "diversity": np.mean(entropy_history),  # Mean Shannon entropy
        "longevity": gen,  # Generations until stable
        "stability_type": stability,
        "entropy_history": entropy_history,
        "final_entropy": entropy_history[-1],
    }


def run_experiment(
    n_trials: int = 100,
    size: int = 20,
    steps: int = 200,
    density: float = 0.3,
    output: str = "gol_experiment_results.json",
) -> dict:
    """
    Run full experiment: n_trials coercive + n_trials non-coercive.

    Returns:
        {
            "coercive": [results],
            "non_coercive": [results],
            "statistics": {
                "diversity": {
                    "coercive_mean": float,
                    "non_coercive_mean": float,
                    "t_statistic": float,
                    "p_value": float
                },
                "longevity": {...},
                "hypothesis": "rejected" | "supported"
            }
        }
    """
    print("🧪 Starting Game of Life Coercion Experiment")
    print(f"   Trials: {n_trials} coercive + {n_trials} non-coercive")
    print(f"   Grid size: {size}x{size}, Max steps: {steps}\n")

    # Coercive trials (all same Glider)
    print("📍 Running coercive trials (fixed Glider pattern)...")
    coercive_results = []
    for i in range(n_trials):
        result = simulate_coercive(size, steps, pattern="glider")
        coercive_results.append(result)
        if (i + 1) % 10 == 0:
            print(f"   Completed {i + 1}/{n_trials} coercive trials")

    # Non-coercive trials (random init, different seeds)
    print("\n🎲 Running non-coercive trials (random initialization)...")
    non_coercive_results = []
    for i in range(n_trials):
        result = simulate_non_coercive(size, steps, density=density, seed=i)
        non_coercive_results.append(result)
        if (i + 1) % 10 == 0:
            print(f"   Completed {i + 1}/{n_trials} non-coercive trials")

    # Statistical analysis
    print("\n📊 Computing statistics...")

    coercive_diversity = [r["diversity"] for r in coercive_results]
    non_coercive_diversity = [r["diversity"] for r in non_coercive_results]

    coercive_longevity = [r["longevity"] for r in coercive_results]
    non_coercive_longevity = [r["longevity"] for r in non_coercive_results]

    # t-tests
    diversity_t, diversity_p = ttest_ind(non_coercive_diversity, coercive_diversity)
    longevity_t, longevity_p = ttest_ind(non_coercive_longevity, coercive_longevity)

    # Hypothesis: non-coercive has higher diversity AND longer longevity
    hypothesis = (
        "supported"
        if (
            diversity_p < 0.05
            and np.mean(non_coercive_diversity) > np.mean(coercive_diversity)
            and longevity_p < 0.05
            and np.mean(non_coercive_longevity) > np.mean(coercive_longevity)
        )
        else "rejected"
    )

    statistics = {
        "diversity": {
            "coercive_mean": float(np.mean(coercive_diversity)),
            "coercive_std": float(np.std(coercive_diversity)),
            "non_coercive_mean": float(np.mean(non_coercive_diversity)),
            "non_coercive_std": float(np.std(non_coercive_diversity)),
            "t_statistic": float(diversity_t),
            "p_value": float(diversity_p),
            "significant": bool(diversity_p < 0.05),
        },
        "longevity": {
            "coercive_mean": float(np.mean(coercive_longevity)),
            "coercive_std": float(np.std(coercive_longevity)),
            "non_coercive_mean": float(np.mean(non_coercive_longevity)),
            "non_coercive_std": float(np.std(non_coercive_longevity)),
            "t_statistic": float(longevity_t),
            "p_value": float(longevity_p),
            "significant": bool(longevity_p < 0.05),
        },
        "hypothesis": hypothesis,
    }

    results = {
        "experiment": "game_of_life_coercion",
        "parameters": {"n_trials": n_trials, "size": size, "steps": steps, "density": density},
        "coercive": coercive_results,
        "non_coercive": non_coercive_results,
        "statistics": statistics,
    }

    # Save results
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {output}")
    print("\n📈 STATISTICAL SUMMARY:")
    print("   Diversity (Shannon Entropy):")
    print(
        f"     Coercive:     {statistics['diversity']['coercive_mean']:.4f} ± {statistics['diversity']['coercive_std']:.4f}"
    )
    print(
        f"     Non-Coercive: {statistics['diversity']['non_coercive_mean']:.4f} ± {statistics['diversity']['non_coercive_std']:.4f}"
    )
    print(f"     t = {statistics['diversity']['t_statistic']:.4f}, p = {statistics['diversity']['p_value']:.4e}")
    print(f"     Significant: {statistics['diversity']['significant']}")
    print("\n   Longevity (Generations):")
    print(
        f"     Coercive:     {statistics['longevity']['coercive_mean']:.2f} ± {statistics['longevity']['coercive_std']:.2f}"
    )
    print(
        f"     Non-Coercive: {statistics['longevity']['non_coercive_mean']:.2f} ± {statistics['longevity']['non_coercive_std']:.2f}"
    )
    print(f"     t = {statistics['longevity']['t_statistic']:.4f}, p = {statistics['longevity']['p_value']:.4e}")
    print(f"     Significant: {statistics['longevity']['significant']}")
    print(f"\n   Hypothesis: {statistics['hypothesis'].upper()}")
    print("   Expected: non-coercive > coercive (diversity H > 0.8, longer longevity)")

    return results


def main():
    parser = argparse.ArgumentParser(description="Game of Life Coercion Experiment")
    parser.add_argument("--trials", type=int, default=100, help="Number of trials per variant")
    parser.add_argument("--size", type=int, default=20, help="Grid size NxN")
    parser.add_argument("--steps", type=int, default=200, help="Max generations per trial")
    parser.add_argument("--density", type=float, default=0.3, help="Initial density for non-coercive (0-1)")
    parser.add_argument("--output", type=str, default="gol_experiment_results.json", help="Output JSON file")
    args = parser.parse_args()

    results = run_experiment(
        n_trials=args.trials,
        size=args.size,
        steps=args.steps,
        density=args.density,
        output=args.output,
    )

    print("\n" + "=" * 60)
    print("🎉 Experiment complete!")
    print(f"   Results: {args.output}")
    print(f"   Hypothesis: {results['statistics']['hypothesis'].upper()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
