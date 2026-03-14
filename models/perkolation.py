"""Perkolations-Modell fuer 5D Bewusstseinsdynamik

Implementiert das Perkolationsmodell fuer die Emergenz von kohaerenten
Bewusstseinszustaenden als kritisches Phaenomen.

Theoretische Basis:
    - Stauffer & Aharony (1994) Percolation Theory
    - Wilson (1971) Renormalization Group Theory (kritische Phaenomene)
    - Tononi et al. (2016) IIT als Emergenz-Metrik
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Optional, List, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


@dataclass
class PerkolationConfig:
    """Konfiguration fuer das Perkolationsmodell."""
    grid_size: int = 50          # Netzwerkgroesse
    n_dimensions: int = 5        # 5D Bewusstseinsdimensionen
    pc_default: float = 0.593    # Kritische Perkolationsschwelle (2D square lattice)
    beta: float = 0.139          # Kritischer Exponent (2D Ising universality class)
    n_simulations: int = 100     # Anzahl Monte-Carlo Durchlaeufe


class PerkolationsNetzwerk:
    """5D Bewusstseinsnetzwerk mit Perkolations-Dynamik."""

    def __init__(self, config: Optional[PerkolationConfig] = None):
        self.config = config or PerkolationConfig()
        self.N = self.config.grid_size

    def verbindungsgrad(self, psi: np.ndarray, weights: Optional[np.ndarray] = None) -> float:
        """Berechnet den lokalen Verbindungsgrad p aus 5D Zustandsvektor.

        Args:
            psi: 5D Zustandsvektor [0, 1]^5
            weights: Dimensionsgewichte (Standard: uniform)

        Returns:
            Verbindungsgrad p in [0, 1]
        """
        if weights is None:
            weights = np.ones(len(psi)) / len(psi)
        linear_comb = np.dot(weights, psi)
        threshold = self.config.pc_default
        return float(1.0 / (1.0 + np.exp(-8 * (linear_comb - threshold))))

    def ordnungsparameter(self, p: float) -> float:
        """Berechnet den Perkolations-Ordnungsparameter P_infty.

        P_infty = 0           fuer p < pc
        P_infty = (p-pc)^beta fuer p >= pc

        Args:
            p: Verbindungsgrad

        Returns:
            Anteil des grossen Clusters (Bewusstseins-Emergenz)
        """
        pc = self.config.pc_default
        beta = self.config.beta
        if p >= pc:
            return float((p - pc) ** beta)
        return 0.0

    def korrelationslaenge(self, p: float) -> float:
        """Berechnet die Korrelationslaenge xi.

        xi ~ |p - pc|^(-nu) mit nu = 4/3 (2D)

        Args:
            p: Verbindungsgrad

        Returns:
            Korrelationslaenge (divergiert bei p -> pc)
        """
        pc = self.config.pc_default
        nu = 4.0 / 3.0
        epsilon = abs(p - pc)
        if epsilon < 1e-8:
            return float(self.N)  # Systemgroesse als Maximum
        return float(min(epsilon ** (-nu), self.N))

    def simuliere_gitter(
        self, p: float, grid_size: Optional[int] = None
    ) -> Tuple[np.ndarray, float, int]:
        """Simuliert ein 2D Perkolationsgitter (Proxy fuer 5D Netzwerk).

        Args:
            p: Besetzungswahrscheinlichkeit
            grid_size: Gittergroesse (Standard aus Config)

        Returns:
            (Gitter, Anteil groesster Cluster, Anzahl Cluster)
        """
        N = grid_size or self.N
        gitter = np.random.random((N, N)) < p

        # Cluster-Labeling mit Union-Find
        labels = np.zeros((N, N), dtype=int)
        label_counter = 0
        parent = {0: 0}  # Union-Find

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[py] = px

        # Erste Reihe scannen
        for i in range(N):
            for j in range(N):
                if gitter[i, j]:
                    # Nachbarn pruefen
                    neighbors = []
                    if i > 0 and gitter[i-1, j]:
                        neighbors.append(labels[i-1, j])
                    if j > 0 and gitter[i, j-1]:
                        neighbors.append(labels[i, j-1])

                    if not neighbors:
                        label_counter += 1
                        labels[i, j] = label_counter
                        parent[label_counter] = label_counter
                    else:
                        root = find(neighbors[0])
                        labels[i, j] = root
                        for nb in neighbors[1:]:
                            union(root, find(nb))

        # Cluster-Groessen berechnen
        cluster_sizes = {}
        for i in range(N):
            for j in range(N):
                if gitter[i, j]:
                    root = find(labels[i, j])
                    cluster_sizes[root] = cluster_sizes.get(root, 0) + 1

        if not cluster_sizes:
            return gitter, 0.0, 0

        max_cluster = max(cluster_sizes.values())
        n_clusters = len(cluster_sizes)
        return gitter, max_cluster / (N * N), n_clusters

    def phasendiagramm(self, n_points: int = 50) -> dict:
        """Berechnet das Phasendiagramm P_infty(p).

        Args:
            n_points: Anzahl p-Werte

        Returns:
            Dictionary mit p-Werten, Ordnungsparameter, Korrelationslaenge
        """
        p_vals = np.linspace(0, 1, n_points)
        order_params = np.array([self.ordnungsparameter(p) for p in p_vals])
        corr_lengths = np.array([self.korrelationslaenge(p) for p in p_vals])

        return {
            "p": p_vals,
            "order_parameter": order_params,
            "correlation_length": corr_lengths,
            "pc": self.config.pc_default,
        }

    def plot_phasendiagramm(self, diagramm: Optional[dict] = None) -> None:
        """Visualisiert das Perkolations-Phasendiagramm."""
        if not HAS_MATPLOTLIB:
            print("Installiere matplotlib: pip install matplotlib")
            return
        if diagramm is None:
            diagramm = self.phasendiagramm()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Perkolations-Phasendiagramm (5D Bewusstsein)", fontsize=13)

        ax1.plot(diagramm["p"], diagramm["order_parameter"], "b-", linewidth=2)
        ax1.axvline(diagramm["pc"], color="red", linestyle="--", label=f"pc = {diagramm['pc']:.3f}")
        ax1.set_xlabel("Verbindungsgrad p")
        ax1.set_ylabel("Ordnungsparameter P_infty")
        ax1.set_title("Emergenz kohaerenten Bewusstseins")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2.plot(diagramm["p"], diagramm["correlation_length"], "g-", linewidth=2)
        ax2.axvline(diagramm["pc"], color="red", linestyle="--", label=f"pc = {diagramm['pc']:.3f}")
        ax2.set_xlabel("Verbindungsgrad p")
        ax2.set_ylabel("Korrelationslaenge xi")
        ax2.set_title("Kritische Verlangsamung")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


def bewusstseins_perkolation(psi: np.ndarray, config: Optional[PerkolationConfig] = None) -> dict:
    """Berechnet alle Perkolations-Metriken fuer einen 5D Bewusstseinszustand.

    Args:
        psi: 5D Zustandsvektor
        config: Perkolationskonfiguration

    Returns:
        Dictionary mit p, Ordnungsparameter, Korrelationslaenge, Kohaerenz-Status
    """
    netz = PerkolationsNetzwerk(config)
    p = netz.verbindungsgrad(psi)
    order = netz.ordnungsparameter(p)
    corr = netz.korrelationslaenge(p)
    pc = netz.config.pc_default

    if p < pc - 0.05:
        status = "fragmentiert"    # Unterhalb kritischer Schwelle
    elif p < pc + 0.05:
        status = "kritisch"        # Kritischer Uebergangsbereich
    else:
        status = "koharent"        # Makroskopisch kohaerentes Bewusstsein

    return {
        "p": p,
        "order_parameter": order,
        "correlation_length": corr,
        "pc": pc,
        "status": status,
        "distance_to_pc": p - pc,
    }


if __name__ == "__main__":
    config = PerkolationConfig(grid_size=30)
    netz = PerkolationsNetzwerk(config)

    print("Perkolations-Analyse fuer 5D Bewusstseinszustaende")
    print("=" * 55)

    states = {
        "Stresszustand":  np.array([0.4, 0.3, 0.35, 0.25, 0.2]),
        "Normaler Alltag": np.array([0.55, 0.6, 0.5, 0.5, 0.4]),
        "Flow-Zustand":   np.array([0.8, 0.75, 0.7, 0.65, 0.6]),
        "Meditation":     np.array([0.75, 0.85, 0.8, 0.7, 0.9]),
    }

    for name, psi in states.items():
        result = bewusstseins_perkolation(psi, config)
        print(f"\n{name}:")
        print(f"  psi = {psi}")
        print(f"  p = {result['p']:.4f} (pc = {result['pc']:.3f})")
        print(f"  Ordnungsparameter = {result['order_parameter']:.4f}")
        print(f"  Korrelationslaenge = {result['correlation_length']:.2f}")
        print(f"  Status: {result['status']}")

    # Phasendiagramm
    diagramm = netz.phasendiagramm(100)
    netz.plot_phasendiagramm(diagramm)
