"""
Quantum Superposition erklärt via MINECRAFT! ⛏️💎

KONZEPT:
Diamanten sind ÜBERALL (in Superposition), bis du hinschaust (Messung)!
Dann kollabiert die Wellenfunktion → Diamant ist an EINEM Ort.

WISSENSCHAFTLICH:
- Superposition: |ψ⟩ = α|hier⟩ + β|dort⟩ + γ|da⟩ + ...
- Messung: |ψ⟩ → |hier⟩ mit Wahrscheinlichkeit |α|²
- Schrödinger's Cat analog: Diamant ist "lebendig UND tot" bis Beobachtung

FÜR KINDER (8-14):
"Diamanten verstecken sich in JEDEM Block! Aber sobald du einen Block aufbrichst,
entscheiden sie sich BLITZSCHNELL wo sie sein wollen. Manchmal da, manchmal nicht!"

Usage:
    python superposition_minecraft.py

Author: 5D Intelligence Framework
Date: 2025-12-03
"""

import json
from datetime import datetime

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


class MinecraftWorld:
    """Minecraft world with quantum diamonds"""

    def __init__(self, size=10):
        self.size = size
        self.blocks = np.zeros((size, size))  # 0 = stone, 1 = diamond
        self.superposition_state = np.ones((size, size))  # All blocks in superposition
        self.measured = np.zeros((size, size), dtype=bool)
        self.diamond_probability = 0.1  # 10% chance per block

    def measure_block(self, x, y):
        """Measure (break) a block → wave function collapse!"""
        if self.measured[x, y]:
            return self.blocks[x, y]

        # QUANTUM COLLAPSE!
        probability = self.superposition_state[x, y] * self.diamond_probability
        has_diamond = np.random.random() < probability

        self.blocks[x, y] = 1 if has_diamond else 0
        self.measured[x, y] = True
        self.superposition_state[x, y] = 0  # No longer in superposition

        return self.blocks[x, y]

    def get_superposition_map(self):
        """Get heatmap of superposition (before measurement)"""
        superposition_map = self.superposition_state.copy()
        superposition_map[self.measured] = 0  # Measured blocks = no superposition
        return superposition_map

    def reset(self):
        """Reset world (new game)"""
        self.__init__(size=self.size)


class QuantumMinecraftVisualizer:
    """Interactive visualization"""

    def __init__(self, world_size=10):
        self.world = MinecraftWorld(size=world_size)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self.setup_plot()

    def setup_plot(self):
        """Setup matplotlib figure"""
        self.fig.suptitle(
            "Quantum Superposition via MINECRAFT! ⛏️💎", fontsize=16, fontweight="bold"
        )

        # Left: Superposition state (BEFORE measurement)
        self.ax1.set_title(
            "BEFORE Breaking Block\n(Superposition: Diamanten ÜBERALL!)", fontsize=12
        )
        self.ax1.set_xlabel("X")
        self.ax1.set_ylabel("Y")
        self.ax1.set_xticks(range(self.world.size))
        self.ax1.set_yticks(range(self.world.size))
        self.ax1.grid(True, alpha=0.3)

        # Right: Collapsed state (AFTER measurement)
        self.ax2.set_title(
            "AFTER Breaking Block\n(Collapsed: Diamant HIER oder NICHT!)", fontsize=12
        )
        self.ax2.set_xlabel("X")
        self.ax2.set_ylabel("Y")
        self.ax2.set_xticks(range(self.world.size))
        self.ax2.set_yticks(range(self.world.size))
        self.ax2.grid(True, alpha=0.3)

    def visualize_step(self, x, y):
        """Visualize one measurement step"""
        self.ax1.clear()
        self.ax2.clear()
        self.setup_plot()

        # LEFT: Superposition heatmap
        superposition_map = self.world.get_superposition_map()
        _im1 = self.ax1.imshow(
            superposition_map,
            cmap="YlOrRd",
            vmin=0,
            vmax=1,
            origin="upper",  # noqa: F841
        )

        # Add text annotations
        for i in range(self.world.size):
            for j in range(self.world.size):
                if not self.world.measured[i, j]:
                    text = "💎?"
                    color = "white"
                else:
                    text = "❌"
                    color = "gray"
                self.ax1.text(
                    j,
                    i,
                    text,
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=color,
                    fontweight="bold",
                )

        # Highlight current block
        rect1 = patches.Rectangle(
            (y - 0.5, x - 0.5), 1, 1, linewidth=3, edgecolor="cyan", facecolor="none"
        )
        self.ax1.add_patch(rect1)

        # Measure block!
        result = self.world.measure_block(x, y)

        # RIGHT: Collapsed state
        collapsed_map = np.zeros_like(self.world.blocks)
        collapsed_map[self.world.measured] = self.world.blocks[self.world.measured]

        _im2 = self.ax2.imshow(
            collapsed_map,
            cmap="Blues",
            vmin=0,
            vmax=1,
            origin="upper",  # noqa: F841
        )

        # Add result annotations
        for i in range(self.world.size):
            for j in range(self.world.size):
                if self.world.measured[i, j]:
                    if self.world.blocks[i, j] == 1:
                        text = "💎"
                        color = "cyan"
                    else:
                        text = "🪨"
                        color = "gray"
                    self.ax2.text(
                        j, i, text, ha="center", va="center", fontsize=14, fontweight="bold"
                    )

        # Highlight measured block
        if result == 1:
            result_text = "DIAMANT! 💎"
            result_color = "green"
        else:
            result_text = "Nur Stein 🪨"
            result_color = "red"

        rect2 = patches.Rectangle(
            (y - 0.5, x - 0.5), 1, 1, linewidth=3, edgecolor=result_color, facecolor="none"
        )
        self.ax2.add_patch(rect2)

        # Add result text
        self.ax2.text(
            self.world.size / 2,
            -1.5,
            result_text,
            ha="center",
            fontsize=14,
            fontweight="bold",
            color=result_color,
        )

        plt.tight_layout()
        plt.pause(0.5)

        return result

    def run_experiment(self, num_measurements=10):
        """Run multiple measurements"""
        print("=" * 60)
        print("🎮 MINECRAFT QUANTUM EXPERIMENT")
        print("=" * 60)
        print(f"World size: {self.world.size}×{self.world.size}")
        print(f"Diamond probability: {self.world.diamond_probability:.1%}")
        print(f"Measurements: {num_measurements}")
        print()

        diamonds_found = 0
        measurements = []

        for i in range(num_measurements):
            # Random block
            x, y = np.random.randint(0, self.world.size, size=2)

            print(f"\nMeasurement {i + 1}/{num_measurements}: Block ({x}, {y})")
            result = self.visualize_step(x, y)

            if result == 1:
                diamonds_found += 1
                print(f"  ✅ DIAMANT gefunden! (Total: {diamonds_found})")
            else:
                print(f"  ❌ Nur Stein (Total: {diamonds_found})")

            measurements.append(
                {
                    "step": i + 1,
                    "position": (int(x), int(y)),
                    "result": "diamond" if result == 1 else "stone",
                    "total_diamonds": diamonds_found,
                }
            )

        # Final statistics
        print("\n" + "=" * 60)
        print("📊 EXPERIMENT RESULTS")
        print("=" * 60)
        print(f"Total measurements: {num_measurements}")
        print(f"Diamonds found: {diamonds_found}")
        print(f"Success rate: {diamonds_found / num_measurements:.1%}")
        print(f"Expected rate: {self.world.diamond_probability:.1%}")

        # Quantum explanation
        print("\n" + "=" * 60)
        print("🎓 QUANTUM MECHANICS ERKLÄRT")
        print("=" * 60)
        print("1. SUPERPOSITION:")
        print("   Vor der Messung: Diamanten sind in ALLEN Blöcken gleichzeitig!")
        print("   Quantenformel: |ψ⟩ = √0.1|Diamant⟩ + √0.9|Stein⟩")
        print()
        print("2. MESSUNG (Block aufbrechen):")
        print("   Wellenfunktion kollabiert → Diamant IST oder IST NICHT")
        print("   Keine Zwischenzustände mehr!")
        print()
        print("3. WAHRSCHEINLICHKEIT:")
        print(f"   P(Diamant) = {self.world.diamond_probability:.1%}")
        print("   P(Stein) = {1-self.world.diamond_probability:.1%}")
        print()
        print("4. REALE QUANTEN:")
        print("   Elektron ist überall (Wolke), bis du misst (Ort kollabiert!)")
        print("   Photon ist Welle UND Teilchen, bis Detektor → Teilchen!")

        # Save results
        output_dir = "../08-experimente-validierung/experiments/results"
        import os

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": datetime.now().isoformat(),
            "experiment": "superposition_minecraft",
            "config": {
                "world_size": self.world.size,
                "diamond_probability": self.world.diamond_probability,
                "num_measurements": num_measurements,
            },
            "results": {
                "diamonds_found": diamonds_found,
                "success_rate": diamonds_found / num_measurements,
                "expected_rate": self.world.diamond_probability,
            },
            "measurements": measurements,
        }

        json_path = f"{output_dir}/minecraft_quantum_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {json_path}")

        plt.savefig(f"{output_dir}/minecraft_quantum_{timestamp}.png", dpi=300, bbox_inches="tight")
        print(f"📊 Plot saved: minecraft_quantum_{timestamp}.png")

        return results


def main():
    """Run Minecraft Quantum Experiment"""
    print("\n" + "🌟" * 30)
    print("⛏️  QUANTUM SUPERPOSITION VIA MINECRAFT! 💎")
    print("🌟" * 30)
    print()
    print("KONZEPT:")
    print("Diamanten sind ÜBERALL (Superposition), bis du Block aufbrichst (Messung)!")
    print("Dann kollabiert die Wellenfunktion → Diamant ist HIER oder NICHT!")
    print()
    print("FÜR KINDER:")
    print("'Stell dir vor, Diamanten verstecken sich in JEDEM Block gleichzeitig!'")
    print("'Aber sobald du einen Block kaputtmachst, müssen sie sich entscheiden:'")
    print("'HIER sein oder NICHT sein!' 💎")
    print()

    # Run experiment
    viz = QuantumMinecraftVisualizer(world_size=10)
    results = viz.run_experiment(num_measurements=10)

    plt.show()

    return results


if __name__ == "__main__":
    main()
