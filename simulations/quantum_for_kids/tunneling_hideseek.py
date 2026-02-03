"""
Quantum Tunneling erklärt via VERSTECKSPIEL! 👻🧱

KONZEPT:
Normalerweise: Wand = undurchdringlich
Quantum: 0.0001% Chance DURCH Wand zu gehen!
Elektronen tun das STÄNDIG in Computer-Chips!

WISSENSCHAFTLICH:
- Tunneling probability: T ≈ e^(-2κa) [κ = √(2m(V-E)/ℏ²)]
- Auch wenn Energie < Barriere → kann durchgehen!
- Schrödinger-Gleichung erlaubt es (exponentielle Abklingung)

FÜR KINDER (8-14):
"Stell dir vor: 1 von 10,000 Mal gehst du DURCH Wand! 👻🧱
Nicht kaputt machen - einfach DURCH!
Elektronen in deinem Handy tun das MILLIONEN Mal pro Sekunde!"

Usage:
    python tunneling_hideseek.py

Author: 5D Intelligence Framework
Date: 2025-12-03
"""

import json
from datetime import datetime

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


class QuantumTunneling:
    """Particle attempting to tunnel through barrier"""

    def __init__(self, barrier_height=10, barrier_width=2, particle_energy=5):
        self.V0 = barrier_height  # Barrier height (eV)
        self.a = barrier_width  # Barrier width (nm)
        self.E = particle_energy  # Particle energy (eV)

        # Physical constants (simplified units)
        self.hbar = 1.0  # ℏ (reduced Planck's constant)
        self.m = 1.0  # mass

        # Calculate tunneling probability
        self.T = self._calculate_tunneling_prob()
        self.attempts = []

    def _calculate_tunneling_prob(self):
        """Calculate quantum tunneling probability"""
        if self.E >= self.V0:
            # Over the barrier (classical)
            return 1.0

        # Quantum tunneling (E < V0)
        kappa = np.sqrt(2 * self.m * (self.V0 - self.E)) / self.hbar
        T = np.exp(-2 * kappa * self.a)

        return T

    def attempt_tunneling(self):
        """Attempt to tunnel (Monte Carlo)"""
        success = np.random.random() < self.T
        self.attempts.append(
            {"success": success, "probability": self.T, "energy": self.E, "barrier_height": self.V0}
        )
        return success


class TunnelingVisualizer:
    """Interactive visualization"""

    def __init__(self):
        self.tunneling = QuantumTunneling(barrier_height=10, barrier_width=2, particle_energy=5)
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(
            2, 2, figsize=(16, 10)
        )
        self.setup_plot()

    def setup_plot(self):
        """Setup matplotlib figure"""
        self.fig.suptitle(
            "Quantum Tunneling via VERSTECKSPIEL! 👻🧱", fontsize=16, fontweight="bold"
        )

        # Top-left: Potential barrier
        self.ax1.set_title("Potential Barrier (Die Wand)", fontsize=12)
        self.ax1.set_xlabel("Position (nm)")
        self.ax1.set_ylabel("Energy (eV)")
        self.ax1.grid(True, alpha=0.3)

        # Top-right: Wave function
        self.ax2.set_title("Wave Function |ψ(x)|² (Probability)", fontsize=12)
        self.ax2.set_xlabel("Position (nm)")
        self.ax2.set_ylabel("Probability Density")
        self.ax2.grid(True, alpha=0.3)

        # Bottom-left: Tunneling attempts
        self.ax3.set_title("Tunneling Attempts (Monte Carlo)", fontsize=12)
        self.ax3.set_xlabel("Attempt Number")
        self.ax3.set_ylabel("Cumulative Success Rate")
        self.ax3.grid(True, alpha=0.3)

        # Bottom-right: Explanation
        self.ax4.axis("off")

    def draw_barrier(self, ax, particle_pos=None, tunneled=False):
        """Draw potential barrier + particle"""
        # Clear
        ax.clear()
        ax.set_title("Potential Barrier (Die Wand)", fontsize=12)
        ax.set_xlabel("Position (nm)")
        ax.set_ylabel("Energy (eV)")
        ax.set_xlim(-2, 10)
        ax.set_ylim(0, 12)
        ax.grid(True, alpha=0.3)

        # Barrier
        barrier_rect = patches.Rectangle(
            (2, 0),
            self.tunneling.a,
            self.tunneling.V0,
            linewidth=2,
            edgecolor="black",
            facecolor="gray",
            alpha=0.5,
        )
        ax.add_patch(barrier_rect)
        ax.text(3, 11, "WAND 🧱", ha="center", fontsize=14, fontweight="bold")

        # Particle energy line
        ax.axhline(
            self.tunneling.E,
            color="blue",
            linestyle="--",
            linewidth=2,
            label=f"Particle Energy (E = {self.tunneling.E} eV)",
        )

        # Barrier height line
        ax.axhline(
            self.tunneling.V0,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Barrier Height (V₀ = {self.tunneling.V0} eV)",
        )

        ax.legend(fontsize=10, loc="upper right")

        # Particle
        if particle_pos is not None:
            color = "green" if tunneled else "blue"
            emoji = "😄" if tunneled else "🏃"
            ax.plot(
                particle_pos,
                self.tunneling.E,
                "o",
                markersize=30,
                color=color,
                markeredgecolor="black",
                markeredgewidth=2,
            )
            ax.text(particle_pos, self.tunneling.E, emoji, ha="center", va="center", fontsize=20)

            if tunneled:
                # Arrow showing tunneling
                ax.annotate(
                    "TUNNELED! 👻",
                    xy=(particle_pos, self.tunneling.E),
                    xytext=(6, 8),
                    arrowprops=dict(arrowstyle="->", lw=3, color="green"),
                    fontsize=12,
                    fontweight="bold",
                    color="green",
                )

    def draw_wave_function(self, ax):
        """Draw quantum wave function"""
        ax.clear()
        ax.set_title("Wave Function |ψ(x)|² (Probability)", fontsize=12)
        ax.set_xlabel("Position (nm)")
        ax.set_ylabel("Probability Density")
        ax.set_xlim(-2, 10)
        ax.grid(True, alpha=0.3)

        x = np.linspace(-2, 10, 500)

        # Region 1: Before barrier (x < 2)
        k1 = np.sqrt(2 * self.tunneling.m * self.tunneling.E) / self.tunneling.hbar
        psi1 = np.where(x < 2, np.cos(k1 * x), 0)

        # Region 2: Inside barrier (2 ≤ x ≤ 4)
        kappa = (
            np.sqrt(2 * self.tunneling.m * (self.tunneling.V0 - self.tunneling.E))
            / self.tunneling.hbar
        )
        x_barrier = x[(x >= 2) & (x <= 4)]
        psi2 = np.exp(-kappa * (x_barrier - 2)) if len(x_barrier) > 0 else np.array([])

        # Region 3: After barrier (x > 4)
        k3 = k1
        x_after = x[x > 4]
        amplitude_transmitted = psi2[-1] if len(psi2) > 0 else 0
        psi3 = (
            amplitude_transmitted * np.cos(k3 * (x_after - 4)) if len(x_after) > 0 else np.array([])
        )

        # Combine
        psi = np.zeros_like(x)
        psi[x < 2] = psi1[x < 2]
        psi[(x >= 2) & (x <= 4)] = psi2
        psi[x > 4] = psi3

        # Plot
        ax.plot(x, psi**2, "b-", linewidth=2)
        ax.fill_between(x, 0, psi**2, alpha=0.3, color="blue")

        # Barrier region
        ax.axvspan(2, 4, alpha=0.2, color="gray")
        ax.text(3, ax.get_ylim()[1] * 0.9, "BARRIER", ha="center", fontsize=10)

        # Annotations
        ax.text(
            0,
            ax.get_ylim()[1] * 0.8,
            "Incident Wave\n(Approaching)",
            ha="center",
            fontsize=9,
            bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.5),
        )
        ax.text(
            7,
            ax.get_ylim()[1] * 0.8,
            "Transmitted Wave\n(Tunneled!)",
            ha="center",
            fontsize=9,
            bbox=dict(boxstyle="round", facecolor="lightgreen", alpha=0.5),
        )

    def visualize_attempts(self, num_attempts=100):
        """Visualize tunneling attempts"""
        print("\n" + "=" * 60)
        print("👻 QUANTUM TUNNELING ATTEMPTS")
        print("=" * 60)
        print(f"Tunneling Probability: T = {self.tunneling.T:.6f} ({self.tunneling.T * 100:.4f}%)")
        print(f"Expected successes: {num_attempts * self.tunneling.T:.2f} out of {num_attempts}")
        print()

        successes = []
        success_count = 0

        for i in range(num_attempts):
            # Attempt tunneling
            success = self.tunneling.attempt_tunneling()
            if success:
                success_count += 1

            # Track cumulative success rate
            successes.append(success_count / (i + 1))

            # Visualize every 10 attempts
            if (i + 1) % 10 == 0:
                # Update plots
                self.draw_barrier(self.ax1, particle_pos=6 if success else 1, tunneled=success)
                self.draw_wave_function(self.ax2)

                # Plot success rate
                self.ax3.clear()
                self.ax3.set_title("Tunneling Attempts (Monte Carlo)", fontsize=12)
                self.ax3.set_xlabel("Attempt Number")
                self.ax3.set_ylabel("Cumulative Success Rate")
                self.ax3.set_ylim(0, max(0.01, max(successes) * 1.5))
                self.ax3.grid(True, alpha=0.3)

                self.ax3.plot(range(1, i + 2), successes, "b-", linewidth=2, label="Observed")
                self.ax3.axhline(
                    self.tunneling.T,
                    color="r",
                    linestyle="--",
                    linewidth=2,
                    label=f"Expected: {self.tunneling.T:.6f}",
                )
                self.ax3.legend(fontsize=10)

                # Explanation
                self.ax4.clear()
                self.ax4.axis("off")
                self.ax4.text(
                    0.1,
                    0.9,
                    "QUANTUM TUNNELING:",
                    fontsize=14,
                    fontweight="bold",
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.80,
                    f"Attempts: {i + 1}/{num_attempts}",
                    fontsize=12,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.72,
                    f"Successes: {success_count} ({success_count / (i + 1) * 100:.2f}%)",
                    fontsize=12,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.64,
                    f"Expected: {self.tunneling.T * 100:.4f}%",
                    fontsize=12,
                    transform=self.ax4.transAxes,
                )

                self.ax4.text(
                    0.1,
                    0.52,
                    "⚛️ WIE FUNKTIONIERT ES?",
                    fontsize=12,
                    fontweight="bold",
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.44,
                    "1. Teilchen hat zu wenig Energie",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.38,
                    f"   (E = {self.tunneling.E} < V₀ = {self.tunneling.V0})",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.30,
                    "2. Klassisch: BLOCKED! 🚫",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.22,
                    "3. Quantum: TUNNELT durch! 👻",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.14,
                    "4. Wahrscheinlichkeit: e^(-2κa)",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )
                self.ax4.text(
                    0.1,
                    0.06,
                    "   → Exponentiell klein, aber NICHT NULL!",
                    fontsize=10,
                    transform=self.ax4.transAxes,
                )

                plt.tight_layout()
                plt.pause(0.1)

                print(
                    f"Attempt {i + 1}: {success_count} successes ({success_count / (i + 1) * 100:.2f}%)"
                )

        # Final stats
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        print(f"Total attempts: {num_attempts}")
        print(f"Successes: {success_count} ({success_count / num_attempts * 100:.2f}%)")
        print(f"Expected: {self.tunneling.T * 100:.4f}%")
        print(f"Difference: {abs(success_count / num_attempts - self.tunneling.T) * 100:.4f}%")

        return successes

    def run_experiment(self):
        """Run tunneling experiment"""
        print("\n" + "=" * 60)
        print("👻 QUANTUM TUNNELING EXPERIMENT")
        print("=" * 60)
        print("Particle tries to go through barrier!")
        print("Classically: IMPOSSIBLE! (E < V₀)")
        print("Quantum: POSSIBLE! (tunneling)")
        print()

        # Run attempts
        _successes = self.visualize_attempts(num_attempts=100)  # noqa: F841

        # Results
        print("\n" + "=" * 60)
        print("🎓 QUANTUM MECHANICS ERKLÄRT")
        print("=" * 60)
        print("1. QUANTUM TUNNELING:")
        print("   Teilchen kann durch Barriere gehen, AUCH WENN E < V₀!")
        print("   Formel: T ≈ e^(-2κa) [κ = √(2m(V-E)/ℏ²)]")
        print("   Bedeutung: Exponentiell klein, aber NICHT NULL!")
        print()
        print("2. WARUM GEHT DAS?")
        print("   Schrödinger-Gleichung erlaubt es:")
        print("   Wellenfunktion KLINGT AB in Barriere (e^(-κx))")
        print("   → Aber erreicht andere Seite mit kleiner Amplitude!")
        print()
        print("3. REAL-WORLD EXAMPLES:")
        print("   • Computer-Chips: Elektronen tunneln durch Isolator!")
        print("     (Problem: Leakage current in nano-transistors)")
        print("   • Scanning Tunneling Microscope (STM):")
        print("     Elektronen tunneln zwischen Spitze ↔ Oberfläche")
        print("     → Atome SEHEN! (Nobelpreis 1986)")
        print("   • Fusion in der Sonne:")
        print("     Protonen tunneln durch Coulomb-Barriere")
        print("     → Sonnenenergie! ☀️")
        print("   • Radioaktiver Zerfall (Alpha-Teilchen)")
        print()
        print("4. WARUM VERSTECKSPIEL?")
        print("   'Durch Wand gehen' ist UNMÖGLICH... oder?")
        print("   Kinder verstehen sofort: 'Manchmal geht es doch!' 👻")
        print("   Viel einfacher als 'exponentielle Wellenfunktions-Abklingung' 😅")

        # Save results
        output_dir = "../08-experimente-validierung/experiments/results"
        import os

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": datetime.now().isoformat(),
            "experiment": "tunneling_hideseek",
            "parameters": {
                "barrier_height": self.tunneling.V0,
                "barrier_width": self.tunneling.a,
                "particle_energy": self.tunneling.E,
                "tunneling_probability": float(self.tunneling.T),
            },
            "attempts": self.tunneling.attempts,
            "statistics": {
                "total_attempts": len(self.tunneling.attempts),
                "successes": sum(1 for a in self.tunneling.attempts if a["success"]),
                "observed_rate": sum(1 for a in self.tunneling.attempts if a["success"])
                / len(self.tunneling.attempts),
            },
        }

        json_path = f"{output_dir}/tunneling_hideseek_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {json_path}")

        plt.savefig(
            f"{output_dir}/tunneling_hideseek_{timestamp}.png", dpi=300, bbox_inches="tight"
        )
        print(f"📊 Plot saved: tunneling_hideseek_{timestamp}.png")

        return results


def main():
    """Run Quantum Tunneling Experiment"""
    print("\n" + "🌟" * 30)
    print("👻  QUANTUM TUNNELING VIA VERSTECKSPIEL! 🧱")
    print("🌟" * 30)
    print()
    print("KONZEPT:")
    print("Normalerweise: Wand = undurchdringlich 🚫")
    print("Quantum: 0.0001% Chance DURCH Wand! 👻")
    print("Elektronen in deinem Handy tun das MILLIONEN Mal pro Sekunde!")
    print()
    print("FÜR KINDER:")
    print("'Stell dir vor: 1 von 10,000 Mal gehst du DURCH Wand!' 🧱👻")
    print("'Nicht kaputt machen - einfach DURCH (wie Geist)!'")
    print("'Elektronen können das - du auch (quantum-mechanisch)!' ✨")
    print()

    # Run experiment
    viz = TunnelingVisualizer()
    results = viz.run_experiment()

    plt.show()

    return results


if __name__ == "__main__":
    main()
