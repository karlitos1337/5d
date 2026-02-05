"""
Wave Interference erklärt via MUSIK! 🎵🌊

KONZEPT:
Zwei Wellen treffen sich → Addieren oder Auslöschen!
Konstruktive Interferenz: 🔊 (louder)
Destruktive Interferenz: 🔇 (silence)

WISSENSCHAFTLICH:
- Wave superposition: ψ_total = ψ_1 + ψ_2
- Konstruktiv: Gleiche Phase → Amplitude verdoppelt!
- Destruktiv: Gegen-Phase → Amplitude = 0 (STILLE!)
- Real example: Noise-cancelling headphones!

FÜR KINDER (8-14):
"Zwei Wellen können sich VERSTÄRKEN (🔊) oder AUSLÖSCHEN (🔇)!
Noise-Cancelling Kopfhörer: Anti-Lärm-Welle löscht Lärm aus!
MAGIE? NEIN! Physik! 🎧✨"

Usage:
    python interference_music.py

Author: 5D Intelligence Framework
Date: 2025-12-03
"""

import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


class WaveInterference:
    """Two waves interfering"""

    def __init__(self, frequency1=5, frequency2=5, phase_diff=0):
        self.f1 = frequency1  # Hz
        self.f2 = frequency2
        self.phase_diff = phase_diff  # radians

        # Time and space
        self.t = np.linspace(0, 2, 1000)
        self.x = np.linspace(0, 10, 1000)

        # Waves
        self.wave1 = None
        self.wave2 = None
        self.wave_total = None

        self.generate_waves()

    def generate_waves(self):
        """Generate two sine waves"""
        # Wave 1: sin(2πf1·t)
        self.wave1 = np.sin(2 * np.pi * self.f1 * self.t)

        # Wave 2: sin(2πf2·t + φ)
        self.wave2 = np.sin(2 * np.pi * self.f2 * self.t + self.phase_diff)

        # Total: Superposition!
        self.wave_total = self.wave1 + self.wave2

    def get_interference_type(self):
        """Determine interference type"""
        # Check phase difference
        phase_normalized = self.phase_diff % (2 * np.pi)

        if phase_normalized < 0.2 or phase_normalized > 2 * np.pi - 0.2:
            return "constructive"
        elif np.abs(phase_normalized - np.pi) < 0.2:
            return "destructive"
        else:
            return "mixed"

    def get_amplitude_ratio(self):
        """Amplitude of total vs individual waves"""
        amp1 = np.max(np.abs(self.wave1))
        amp_total = np.max(np.abs(self.wave_total))
        return amp_total / amp1


class InterferenceVisualizer:
    """Interactive visualization"""

    def __init__(self):
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        self.setup_plot()

    def setup_plot(self):
        """Setup matplotlib figure"""
        self.fig.suptitle("Wave Interference via MUSIK! 🎵🌊", fontsize=16, fontweight="bold")

        # Top-left: Wave 1
        self.ax1.set_title("Wave 1: Erste Ton 🎵", fontsize=12)
        self.ax1.set_xlabel("Zeit (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_ylim(-2.5, 2.5)

        # Top-right: Wave 2
        self.ax2.set_title("Wave 2: Zweite Ton 🎶", fontsize=12)
        self.ax2.set_xlabel("Zeit (s)")
        self.ax2.set_ylabel("Amplitude")
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(-2.5, 2.5)

        # Bottom-left: Superposition
        self.ax3.set_title("TOTAL: Wave 1 + Wave 2 (Interferenz!)", fontsize=12, fontweight="bold")
        self.ax3.set_xlabel("Zeit (s)")
        self.ax3.set_ylabel("Amplitude")
        self.ax3.grid(True, alpha=0.3)
        self.ax3.set_ylim(-2.5, 2.5)

        # Bottom-right: Explanation
        self.ax4.axis("off")

    def visualize_interference(self, phase_diff=0, title_suffix=""):
        """Visualize one interference case"""
        # Create waves
        waves = WaveInterference(frequency1=5, frequency2=5, phase_diff=phase_diff)

        # Clear axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.setup_plot()

        # Plot Wave 1
        self.ax1.plot(waves.t, waves.wave1, "b-", linewidth=2)
        self.ax1.axhline(0, color="k", linestyle="--", alpha=0.3)
        self.ax1.fill_between(waves.t, 0, waves.wave1, alpha=0.2, color="blue")

        # Plot Wave 2
        self.ax2.plot(waves.t, waves.wave2, "r-", linewidth=2)
        self.ax2.axhline(0, color="k", linestyle="--", alpha=0.3)
        self.ax2.fill_between(waves.t, 0, waves.wave2, alpha=0.2, color="red")

        # Plot Total (with individual waves as dashed)
        self.ax3.plot(waves.t, waves.wave1, "b--", linewidth=1, alpha=0.5, label="Wave 1")
        self.ax3.plot(waves.t, waves.wave2, "r--", linewidth=1, alpha=0.5, label="Wave 2")
        self.ax3.plot(waves.t, waves.wave_total, "g-", linewidth=3, label="TOTAL")
        self.ax3.axhline(0, color="k", linestyle="--", alpha=0.3)
        self.ax3.fill_between(waves.t, 0, waves.wave_total, alpha=0.3, color="green")
        self.ax3.legend(fontsize=10)

        # Determine interference type
        int_type = waves.get_interference_type()
        amp_ratio = waves.get_amplitude_ratio()

        # Explanation text
        self.ax4.text(
            0.1,
            0.9,
            "INTERFERENZ ERKLÄRT:",
            fontsize=14,
            fontweight="bold",
            transform=self.ax4.transAxes,
        )

        if int_type == "constructive":
            self.ax4.text(
                0.1,
                0.75,
                "🔊 KONSTRUKTIVE INTERFERENZ!",
                fontsize=12,
                fontweight="bold",
                color="green",
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.65,
                "✅ Wellen in gleicher Phase (synchron)",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.57,
                "✅ Amplituden ADDIEREN: 1 + 1 = 2!",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.49,
                f"✅ Amplitude Ratio: {amp_ratio:.2f}x LOUDER!",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.38,
                "📢 Beispiel: Zwei Lautsprecher synchron",
                fontsize=10,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(0.1, 0.30, "   → Musik 2x lauter! 🎵🎵", fontsize=10, transform=self.ax4.transAxes)

        elif int_type == "destructive":
            self.ax4.text(
                0.1,
                0.75,
                "🔇 DESTRUKTIVE INTERFERENZ!",
                fontsize=12,
                fontweight="bold",
                color="red",
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.65,
                "❌ Wellen in Gegen-Phase (180°)",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.57,
                "❌ Amplituden AUSLÖSCHEN: 1 + (-1) = 0!",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.49,
                f"❌ Amplitude Ratio: {amp_ratio:.2f} → SILENCE!",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.38,
                "🎧 Beispiel: Noise-Cancelling Kopfhörer!",
                fontsize=10,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.30,
                "   Mikrofon misst Lärm → Anti-Lärm erzeugt",
                fontsize=10,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.22,
                "   → Lärm + Anti-Lärm = STILLE! ✨",
                fontsize=10,
                transform=self.ax4.transAxes,
            )
        else:
            self.ax4.text(
                0.1,
                0.75,
                "🎵 MIXED INTERFERENZ",
                fontsize=12,
                fontweight="bold",
                color="orange",
                transform=self.ax4.transAxes,
            )
            self.ax4.text(0.1, 0.65, "⚠️ Wellen teilweise in Phase", fontsize=11, transform=self.ax4.transAxes)
            self.ax4.text(
                0.1,
                0.57,
                "⚠️ Komplexes Muster (nicht ganz laut, nicht ganz still)",
                fontsize=11,
                transform=self.ax4.transAxes,
            )
            self.ax4.text(
                0.1,
                0.49,
                f"⚠️ Amplitude Ratio: {amp_ratio:.2f}",
                fontsize=11,
                transform=self.ax4.transAxes,
            )

        # Quantum connection
        self.ax4.text(
            0.1,
            0.12,
            "⚛️ QUANTUM CONNECTION:",
            fontsize=11,
            fontweight="bold",
            transform=self.ax4.transAxes,
        )
        self.ax4.text(
            0.1,
            0.04,
            "Alle Quanten-Teilchen sind WELLEN! Elektronen, Photonen...",
            fontsize=10,
            transform=self.ax4.transAxes,
        )
        self.ax4.text(
            0.1,
            -0.04,
            "→ Doppelspalt-Experiment: Elektronen interferieren wie Musik! 🌊",
            fontsize=10,
            transform=self.ax4.transAxes,
        )

        plt.tight_layout()
        plt.pause(2)

        return waves

    def run_experiment(self):
        """Run interference experiment"""
        print("\n" + "=" * 60)
        print("🎵 WAVE INTERFERENCE EXPERIMENT")
        print("=" * 60)
        print("Zwei Wellen treffen sich → Was passiert?")
        print()

        results = {"cases": []}

        # Case 1: Constructive (in phase)
        print("\n🔹 CASE 1: KONSTRUKTIVE INTERFERENZ (Same Phase)")
        print("-" * 60)
        print("Phase difference: 0° (synchron)")
        waves1 = self.visualize_interference(phase_diff=0)
        print(f"Interference type: {waves1.get_interference_type()}")
        print(f"Amplitude ratio: {waves1.get_amplitude_ratio():.2f}x")
        print("Result: 🔊 LOUDER!")

        results["cases"].append(
            {
                "name": "Constructive",
                "phase_diff": 0,
                "type": waves1.get_interference_type(),
                "amplitude_ratio": float(waves1.get_amplitude_ratio()),
            }
        )

        # Case 2: Destructive (opposite phase)
        print("\n🔹 CASE 2: DESTRUKTIVE INTERFERENZ (Opposite Phase)")
        print("-" * 60)
        print("Phase difference: 180° (Gegen-Phase)")
        waves2 = self.visualize_interference(phase_diff=np.pi)
        print(f"Interference type: {waves2.get_interference_type()}")
        print(f"Amplitude ratio: {waves2.get_amplitude_ratio():.2f}")
        print("Result: 🔇 SILENCE!")

        results["cases"].append(
            {
                "name": "Destructive",
                "phase_diff": float(np.pi),
                "type": waves2.get_interference_type(),
                "amplitude_ratio": float(waves2.get_amplitude_ratio()),
            }
        )

        # Case 3: Mixed (90° phase)
        print("\n🔹 CASE 3: MIXED INTERFERENZ (90° Phase)")
        print("-" * 60)
        print("Phase difference: 90°")
        waves3 = self.visualize_interference(phase_diff=np.pi / 2)
        print(f"Interference type: {waves3.get_interference_type()}")
        print(f"Amplitude ratio: {waves3.get_amplitude_ratio():.2f}")
        print("Result: 🎵 Complex pattern")

        results["cases"].append(
            {
                "name": "Mixed",
                "phase_diff": float(np.pi / 2),
                "type": waves3.get_interference_type(),
                "amplitude_ratio": float(waves3.get_amplitude_ratio()),
            }
        )

        # Results summary
        print("\n" + "=" * 60)
        print("📊 EXPERIMENT RESULTS")
        print("=" * 60)
        for case in results["cases"]:
            print(f"{case['name']:15s}: {case['type']:15s} | Amp = {case['amplitude_ratio']:.2f}x")

        # Quantum explanation
        print("\n" + "=" * 60)
        print("🎓 QUANTUM MECHANICS ERKLÄRT")
        print("=" * 60)
        print("1. WAVE SUPERPOSITION:")
        print("   ψ_total = ψ_1 + ψ_2 (einfach addieren!)")
        print("   Konstruktiv: Gleiche Phase → 1 + 1 = 2 🔊")
        print("   Destruktiv: Gegen-Phase → 1 + (-1) = 0 🔇")
        print()
        print("2. NOISE-CANCELLING HEADPHONES:")
        print("   Mikrofon misst Umgebungslärm")
        print("   → Computer erzeugt ANTI-Lärm (180° Phase)")
        print("   → Lärm + Anti-Lärm = STILLE! ✨")
        print("   Real example: Bose QuietComfort, Sony WH-1000XM")
        print()
        print("3. QUANTUM INTERFERENCE:")
        print("   Doppelspalt-Experiment (Young 1801):")
        print("   Elektronen gehen durch BEIDE Spalte gleichzeitig!")
        print("   → Interferenzmuster auf Schirm (helle + dunkle Streifen)")
        print("   → Beweis: Elektronen sind WELLEN! 🌊")
        print()
        print("4. REAL-WORLD APPLICATIONS:")
        print("   • Noise-cancelling headphones 🎧")
        print("   • Interferometer (Gravitationswellen-Detektor LIGO)")
        print("   • Holographie (Laser-Interferenz)")
        print("   • Quantum computing (Qubit-Interferenz)")
        print()
        print("5. WARUM MUSIK?")
        print("   Kinder HÖREN Musik JEDEN TAG! 🎵")
        print("   'Zwei Töne können laut oder still sein!' viel einfacher als")
        print("   'Quantenzustände superponieren mit komplexer Amplitude' 😅")

        # Save results
        output_dir = "../08-experimente-validierung/experiments/results"
        import os

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results["timestamp"] = datetime.now().isoformat()
        results["experiment"] = "interference_music"

        json_path = f"{output_dir}/music_interference_{timestamp}.json"
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {json_path}")

        plt.savefig(f"{output_dir}/music_interference_{timestamp}.png", dpi=300, bbox_inches="tight")
        print(f"📊 Plot saved: music_interference_{timestamp}.png")

        return results


def main():
    """Run Music Interference Experiment"""
    print("\n" + "🌟" * 30)
    print("🎵  WAVE INTERFERENCE VIA MUSIK! 🌊")
    print("🌟" * 30)
    print()
    print("KONZEPT:")
    print("Zwei Wellen treffen sich → Addieren oder Auslöschen!")
    print("Konstruktiv: 🔊 (louder)")
    print("Destruktiv: 🔇 (silence)")
    print()
    print("FÜR KINDER:")
    print("'Zwei Wellen können lauter machen ODER stumm machen!' 🎵")
    print("'Noise-Cancelling Kopfhörer: Anti-Lärm löscht Lärm aus!'")
    print("'Keine Magie - nur Physik!' ✨")
    print()

    # Run experiment
    viz = InterferenceVisualizer()
    results = viz.run_experiment()

    plt.show()

    return results


if __name__ == "__main__":
    main()
