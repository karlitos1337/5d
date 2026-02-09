"""
Wave Packets erklärt via FUSSBALL! ⚽🌊

KONZEPT:
Ball ist KEINE Punkt, sondern WELLE!
Ball ist überall auf Feld (Wahrscheinlichkeitswolke)
Torwart fängt → Welle kollabiert zu EINEM Punkt!

WISSENSCHAFTLICH:
- Wave packet: ψ(x,t) = ∫ A(k)e^(i(kx-ωt)) dk
- Heisenberg: Δx·Δp ≥ ℏ/2 (Unschärferelation!)
- Messen von Position → Impuls unscharf (und umgekehrt)

FÜR KINDER (8-14):
"Ball ist überall auf Feld als WELLE! 🌊⚽
Du kannst nicht genau wissen: Wo UND wie schnell!
Torwart fängt → Welle wird PUNKT (aber Geschwindigkeit jetzt unscharf!)"

Usage:
    python wave_packet_soccer.py

Author: 5D Intelligence Framework
Date: 2025-12-03
"""

import json
from datetime import datetime

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


class QuantumSoccerBall:
    """Soccer ball as quantum wave packet"""

    def __init__(self, field_size=10):
        self.field_size = field_size
        self.x = np.linspace(0, field_size, 200)
        self.y = np.linspace(0, field_size, 200)
        self.X, self.Y = np.meshgrid(self.x, self.y)

        # Initial wave packet (center of field)
        self.x0, self.y0 = field_size / 2, field_size / 2
        self.sigma_x = 2.0  # Width of wave packet
        self.sigma_y = 2.0
        self.vx = 0.5  # Velocity
        self.vy = 0.3

        self.wave_packet = self._create_wave_packet()
        self.measured = False
        self.measured_pos = None
        self.measurements = []

    def _create_wave_packet(self):
        """Create Gaussian wave packet"""
        # Gaussian envelope: |ψ(x,y)|²
        gaussian = np.exp(
            -(
                (self.X - self.x0) ** 2 / (2 * self.sigma_x**2)
                + (self.Y - self.y0) ** 2 / (2 * self.sigma_y**2)
            )
        )

        # Add momentum (plane wave): e^(i(kx + ky))
        k_x = self.vx / self.sigma_x
        k_y = self.vy / self.sigma_y
        plane_wave = np.exp(1j * (k_x * self.X + k_y * self.Y))

        wave_packet = gaussian * plane_wave

        # Normalize
        wave_packet /= np.sqrt(np.sum(np.abs(wave_packet) ** 2))

        return np.abs(wave_packet) ** 2  # Probability density

    def evolve(self, dt=0.1):
        """Evolve wave packet in time"""
        if self.measured:
            return  # After measurement, no evolution (collapsed!)

        # Move wave packet (classical drift)
        self.x0 += self.vx * dt
        self.y0 += self.vy * dt

        # Spread (Heisenberg uncertainty: Δx increases over time)
        self.sigma_x += 0.05 * dt
        self.sigma_y += 0.05 * dt

        # Recreate wave packet
        self.wave_packet = self._create_wave_packet()

    def measure(self, goalkeeper_x, goalkeeper_y):
        """Goalkeeper catches ball → wave collapse!"""
        # Probability of catching at this position
        prob = self.wave_packet[
            int(goalkeeper_y * len(self.y) / self.field_size),
            int(goalkeeper_x * len(self.x) / self.field_size),
        ]

        # Sample from probability distribution
        flat_wave = self.wave_packet.flatten()
        flat_wave /= flat_wave.sum()

        idx = np.random.choice(len(flat_wave), p=flat_wave)
        measured_y, measured_x = np.unravel_index(idx, self.wave_packet.shape)

        self.measured = True
        self.measured_pos = (self.x[measured_x], self.y[measured_y])

        # Collapse: Wave packet → delta function
        collapsed = np.zeros_like(self.wave_packet)
        collapsed[measured_y, measured_x] = 1.0
        self.wave_packet = collapsed

        self.measurements.append(
            {
                "goalkeeper_pos": (goalkeeper_x, goalkeeper_y),
                "measured_pos": self.measured_pos,
                "probability": float(prob),
            }
        )

        return self.measured_pos, prob


class SoccerWaveVisualizer:
    """Interactive visualization"""

    def __init__(self):
        self.ball = QuantumSoccerBall(field_size=10)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 7))
        self.setup_plot()

    def setup_plot(self):
        """Setup matplotlib figure"""
        self.fig.suptitle("Quantum Wave Packets via FUSSBALL! ⚽🌊", fontsize=16, fontweight="bold")

        # Left: Before measurement (wave packet)
        self.ax1.set_title(
            "BEFORE: Ball als Welle (überall gleichzeitig!)", fontsize=12, fontweight="bold"
        )
        self.ax1.set_xlim(0, 10)
        self.ax1.set_ylim(0, 10)
        self.ax1.set_xlabel("Field X (m)")
        self.ax1.set_ylabel("Field Y (m)")
        self.ax1.set_aspect("equal")
        self.ax1.grid(True, alpha=0.3)

        # Right: After measurement (collapsed)
        self.ax2.set_title(
            "AFTER: Torwart fängt → Welle kollabiert!", fontsize=12, fontweight="bold"
        )
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(0, 10)
        self.ax2.set_xlabel("Field X (m)")
        self.ax2.set_ylabel("Field Y (m)")
        self.ax2.set_aspect("equal")
        self.ax2.grid(True, alpha=0.3)

    def draw_field(self, ax):
        """Draw soccer field"""
        # Field outline
        rect = patches.Rectangle(
            (0, 0), 10, 10, linewidth=2, edgecolor="green", facecolor="lightgreen", alpha=0.2
        )
        ax.add_patch(rect)

        # Goal
        goal = patches.Rectangle(
            (4, 0), 2, 0.5, linewidth=2, edgecolor="white", facecolor="white", alpha=0.5
        )
        ax.add_patch(goal)

        # Center circle
        circle = patches.Circle(
            (5, 5), 1.5, linewidth=2, edgecolor="white", facecolor="none", alpha=0.5
        )
        ax.add_patch(circle)

    def visualize_step(self, goalkeeper_x=5.0, goalkeeper_y=1.0, num_frames=5):
        """Visualize wave packet evolution + measurement"""
        print("\n" + "=" * 60)
        print("⚽ WAVE PACKET EVOLUTION")
        print("=" * 60)

        # Phase 1: Wave packet spreads
        print("\n🔹 PHASE 1: Ball als Welle (BEFORE measurement)")
        print("-" * 60)

        for frame in range(num_frames):
            # Clear
            self.ax1.clear()
            self.setup_plot()
            self.draw_field(self.ax1)

            # Plot wave packet (probability cloud)
            im = self.ax1.contourf(
                self.ball.X, self.ball.Y, self.ball.wave_packet, levels=20, cmap="YlOrRd", alpha=0.7  # noqa: E501
            )

            # Add colorbar
            if frame == 0:
                plt.colorbar(im, ax=self.ax1, label="Probability Density")

            # Add ball emoji at peak
            max_idx = np.unravel_index(self.ball.wave_packet.argmax(), self.ball.wave_packet.shape)
            peak_x = self.ball.x[max_idx[1]]
            peak_y = self.ball.y[max_idx[0]]
            self.ax1.plot(
                peak_x,
                peak_y,
                "o",
                markersize=20,
                color="white",
                markeredgecolor="black",
                markeredgewidth=2,
            )
            self.ax1.text(peak_x, peak_y, "⚽", ha="center", va="center", fontsize=20)

            # Add goalkeeper
            self.ax1.plot(
                goalkeeper_x,
                goalkeeper_y,
                "s",
                markersize=25,
                color="blue",
                markeredgecolor="black",
                markeredgewidth=2,
            )
            self.ax1.text(goalkeeper_x, goalkeeper_y, "🧤", ha="center", va="center", fontsize=20)

            # Annotations
            self.ax1.text(
                5,
                9.5,
                f"Frame {frame + 1}/{num_frames}: Welle breitet aus!",
                ha="center",
                fontsize=12,
                fontweight="bold",
                bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.7),
            )

            print(f"  Frame {frame + 1}: Wave width σ = {self.ball.sigma_x:.2f} m")

            # Evolve
            self.ball.evolve(dt=0.3)
            plt.pause(0.5)

        # Phase 2: Measurement (goalkeeper catches)
        print("\n🔹 PHASE 2: MEASUREMENT (Torwart fängt!)")
        print("-" * 60)

        measured_pos, prob = self.ball.measure(goalkeeper_x, goalkeeper_y)
        print(f"  Goalkeeper Position: ({goalkeeper_x}, {goalkeeper_y})")
        print(f"  Measured Position: ({measured_pos[0]:.2f}, {measured_pos[1]:.2f})")
        print(f"  Probability: {prob:.4f}")

        # Clear RIGHT plot
        self.ax2.clear()
        self.ax2.set_title(
            "AFTER: Torwart fängt → Welle kollabiert!", fontsize=12, fontweight="bold"
        )
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(0, 10)
        self.ax2.set_xlabel("Field X (m)")
        self.ax2.set_ylabel("Field Y (m)")
        self.ax2.set_aspect("equal")
        self.ax2.grid(True, alpha=0.3)
        self.draw_field(self.ax2)

        # Plot collapsed state
        im2 = self.ax2.contourf(
            self.ball.X, self.ball.Y, self.ball.wave_packet, levels=20, cmap="Blues", alpha=0.7
        )
        plt.colorbar(im2, ax=self.ax2, label="Collapsed State")

        # Ball at measured position
        self.ax2.plot(
            measured_pos[0],
            measured_pos[1],
            "o",
            markersize=30,
            color="white",
            markeredgecolor="black",
            markeredgewidth=3,
        )
        self.ax2.text(measured_pos[0], measured_pos[1], "⚽", ha="center", va="center", fontsize=25)

        # Goalkeeper
        self.ax2.plot(
            goalkeeper_x,
            goalkeeper_y,
            "s",
            markersize=25,
            color="blue",
            markeredgecolor="black",
            markeredgewidth=2,
        )
        self.ax2.text(goalkeeper_x, goalkeeper_y, "🧤", ha="center", va="center", fontsize=20)

        # Arrow showing collapse
        self.ax2.annotate(
            "COLLAPSE!",
            xy=measured_pos,
            xytext=(7, 7),
            arrowprops=dict(arrowstyle="->", lw=3, color="red"),
            fontsize=14,
            fontweight="bold",
            color="red",
        )

        # Annotation
        self.ax2.text(
            5,
            9.5,
            f"Welle → Punkt! Position NOW certain: ({measured_pos[0]:.1f}, {measured_pos[1]:.1f})",
            ha="center",
            fontsize=12,
            fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.7),
        )

        plt.tight_layout()
        plt.pause(2)

    def run_experiment(self):
        """Run wave packet experiment"""
        print("\n" + "=" * 60)
        print("⚽ QUANTUM WAVE PACKET EXPERIMENT")
        print("=" * 60)
        print("Ball ist WELLE (nicht Punkt)!")
        print("Torwart fängt → Welle kollabiert zu Punkt!")
        print()

        # Run visualization
        self.visualize_step(goalkeeper_x=5.0, goalkeeper_y=1.0, num_frames=5)

        # Results
        print("\n" + "=" * 60)
        print("📊 EXPERIMENT RESULTS")
        print("=" * 60)
        print(f"Number of measurements: {len(self.ball.measurements)}")
        for i, m in enumerate(self.ball.measurements):
            print(f"  Measurement {i + 1}:")
            print(f"    Goalkeeper: {m['goalkeeper_pos']}")
            print(f"    Ball measured at: ({m['measured_pos'][0]:.2f}, {m['measured_pos'][1]:.2f})")  # noqa: E501
            print(f"    Probability: {m['probability']:.4f}")

        # Quantum explanation
        print("\n" + "=" * 60)
        print("🎓 QUANTUM MECHANICS ERKLÄRT")
        print("=" * 60)
        print("1. WAVE PACKET:")
        print("   Teilchen ist WELLE (nicht Punkt!)")
        print("   Formel: ψ(x,t) = ∫ A(k)e^(i(kx-ωt)) dk")
        print("   Bedeutung: Ball hat Wahrscheinlichkeit ÜBERALL zu sein!")
        print()
        print("2. HEISENBERG UNCERTAINTY:")
        print("   Δx·Δp ≥ ℏ/2")
        print("   Bedeutung: Position UND Impuls NICHT gleichzeitig genau!")
        print("   Ball breit (Δx groß) → Geschwindigkeit unscharf (Δp groß)")
        print()
        print("3. MEASUREMENT (COLLAPSE):")
        print("   Torwart fängt → Welle wird PUNKT!")
        print("   Position NOW certain → aber Geschwindigkeit NOW uncertain!")
        print("   (Komplementäre Observablen)")
        print()
        print("4. WAVE PACKET SPREADING:")
        print("   Mit Zeit: Welle breitet aus (Δx increases)")
        print("   Quantenmechanisch UNVERMEIDBAR!")
        print()
        print("5. REALE QUANTEN:")
        print("   Elektronen-Wellen → Beugung am Doppelspalt (1920s)")
        print("   Photonen-Pulse → Femtosekunden-Laser (10^-15 s)")
        print("   Materie-Wellen → de Broglie (1924): λ = h/p")
        print()
        print("6. WARUM FUSSBALL?")
        print("   Kinder spielen Fussball JEDEN TAG! ⚽")
        print("   'Ball ist überall auf Feld!' viel einfacher als")
        print("   'Elektron-Wellenfunktion mit komplexer Amplitude' 😅")

        # Save results
        output_dir = "../08-experimente-validierung/experiments/results"
        import os

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "timestamp": datetime.now().isoformat(),
            "experiment": "wave_packet_soccer",
            "measurements": self.ball.measurements,
            "final_state": {"measured": self.ball.measured, "position": self.ball.measured_pos},
        }

        json_path = f"{output_dir}/soccer_wavepacket_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {json_path}")

        plt.savefig(f"{output_dir}/soccer_wavepacket_{timestamp}.png", dpi=300, bbox_inches="tight")  # noqa: E501
        print(f"📊 Plot saved: soccer_wavepacket_{timestamp}.png")

        return results


def main():
    """Run Soccer Wave Packet Experiment"""
    print("\n" + "🌟" * 30)
    print("⚽  QUANTUM WAVE PACKETS VIA FUSSBALL! 🌊")
    print("🌟" * 30)
    print()
    print("KONZEPT:")
    print("Ball ist WELLE (nicht Punkt)!")
    print("Ball ist ÜBERALL auf Feld gleichzeitig (Wahrscheinlichkeitswolke)!")
    print("Torwart fängt → Welle kollabiert zu EINEM Punkt!")
    print()
    print("FÜR KINDER:")
    print("'Stell dir vor, Ball ist überall auf Feld als Wolke!' ☁️⚽")
    print("'Wo genau? Weißt du erst, wenn Torwart fängt!'")
    print("'Dann: BÄÄÄM! Welle wird Punkt!' 💥")
    print()

    # Run experiment
    viz = SoccerWaveVisualizer()
    results = viz.run_experiment()

    plt.show()

    return results


if __name__ == "__main__":
    main()
