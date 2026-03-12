"""Lagrange-Simulator fuer 5D Bewusstseinsdynamik

Numerische Integration der Euler-Lagrange-Gleichungen fuer das 5D-System
mit Polyvagal-Daempfung, IIT-Phi und Perkolations-Emergenz.

Verwendung:
    sim = LagrangeSimulator()
    trajectory = sim.simulate(initial_psi, t_span=(0, 100), n_steps=1000)
    sim.plot_trajectory(trajectory)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


@dataclass
class LagrangeConfig:
    """Konfiguration fuer den Lagrange-Simulator."""

    mass_diag: np.ndarray = field(
        default_factory=lambda: np.array([1.0, 1.0, 0.8, 0.8, 0.6])
    )
    spring_k: np.ndarray = field(
        default_factory=lambda: np.array([2.0, 2.0, 1.5, 1.5, 1.0])
    )
    equilibrium: np.ndarray = field(
        default_factory=lambda: np.array([0.6, 0.6, 0.55, 0.5, 0.45])
    )
    coupling_strength: float = 0.3
    gamma_base: float = 0.2
    hrv_rmssd: float = 50.0
    k_phi: float = 0.5
    perc_threshold: float = 0.55


class LagrangeSimulator:
    """Numerischer Simulator fuer 5D Lagrange Bewusstseinsdynamik."""

    def __init__(self, config: Optional[LagrangeConfig] = None):
        self.config = config or LagrangeConfig()
        self._dim = 5

    def _mass_matrix(self) -> np.ndarray:
        M = np.diag(self.config.mass_diag)
        c = self.config.coupling_strength * 0.1
        for i in range(self._dim - 1):
            M[i, i + 1] = c
            M[i + 1, i] = c
        return M

    def _potential_gradient(self, psi: np.ndarray) -> np.ndarray:
        psi0 = self.config.equilibrium
        k = self.config.spring_k
        grad = k * (psi - psi0)
        c = self.config.coupling_strength
        for i in range(self._dim):
            for j in range(self._dim):
                if i != j:
                    diff = psi[i] - psi[j]
                    grad[i] += 0.05 * c * diff * abs(diff)
        return grad

    def _phi_iit(self, psi: np.ndarray) -> float:
        system_var = float(np.var(psi))
        mid = self._dim // 2
        p1 = float(np.var(psi[:mid])) if mid > 0 else 0.0
        p2 = float(np.var(psi[mid:])) if self._dim - mid > 0 else 0.0
        return max(system_var - (p1 + p2) / 2, 0.0)

    def _phi_gradient(self, psi: np.ndarray) -> np.ndarray:
        eps = 1e-5
        grad = np.zeros(self._dim)
        for i in range(self._dim):
            pp = psi.copy(); pm = psi.copy()
            pp[i] += eps; pm[i] -= eps
            grad[i] = (self._phi_iit(pp) - self._phi_iit(pm)) / (2 * eps)
        return grad

    def _gamma_hrv(self) -> float:
        hrv = self.config.hrv_rmssd
        if hrv >= 50:
            return self.config.gamma_base * 0.5
        elif hrv >= 25:
            return self.config.gamma_base
        return self.config.gamma_base * 3.0

    def _equations_of_motion(self, t: float, state: np.ndarray) -> np.ndarray:
        psi = state[:self._dim]
        dpsi = state[self._dim:]
        M_inv = np.linalg.inv(self._mass_matrix())
        grad_V = self._potential_gradient(psi)
        grad_phi = self._phi_gradient(psi)
        gamma = self._gamma_hrv()
        force = -grad_V + self.config.k_phi * grad_phi - gamma * dpsi
        d2psi = M_inv @ force
        for i in range(self._dim):
            if psi[i] < 0 and dpsi[i] < 0:
                d2psi[i] += 10.0 * (-psi[i])
            elif psi[i] > 1 and dpsi[i] > 0:
                d2psi[i] += 10.0 * (1.0 - psi[i])
        return np.concatenate([dpsi, d2psi])

    def simulate(
        self,
        initial_psi: np.ndarray,
        initial_dpsi: Optional[np.ndarray] = None,
        t_span: Tuple[float, float] = (0, 50),
        n_steps: int = 500,
    ) -> dict:
        if initial_dpsi is None:
            initial_dpsi = np.zeros(self._dim)
        state = np.concatenate([initial_psi, initial_dpsi])
        dt = (t_span[1] - t_span[0]) / n_steps
        t = t_span[0]
        states, t_vals = [state.copy()], [t]
        for _ in range(n_steps - 1):
            k1 = self._equations_of_motion(t, state)
            k2 = self._equations_of_motion(t + dt/2, state + dt/2 * k1)
            k3 = self._equations_of_motion(t + dt/2, state + dt/2 * k2)
            k4 = self._equations_of_motion(t + dt, state + dt * k3)
            state = state + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
            t += dt
            states.append(state.copy())
            t_vals.append(t)
        states = np.array(states)
        t_vals = np.array(t_vals)
        psi_traj = states[:, :self._dim]
        phi_traj = np.array([self._phi_iit(p) for p in psi_traj])
        gamma = self._gamma_hrv()
        weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])
        imp_traj = np.array([
            np.dot(weights, p) * (1 - gamma) * (1 + self.config.k_phi * phi)
            for p, phi in zip(psi_traj, phi_traj)
        ])
        return {"t": t_vals, "psi": psi_traj, "dpsi": states[:, self._dim:], "phi": phi_traj, "imp": imp_traj}

    def plot_trajectory(self, trajectory: dict, title: str = "5D Bewusstseinsdynamik") -> None:
        if not HAS_MATPLOTLIB:
            print("Installiere matplotlib: pip install matplotlib")
            return
        t, psi, phi, imp = trajectory["t"], trajectory["psi"], trajectory["phi"], trajectory["imp"]
        names = ["Kognitiv", "Emotional", "Somatisch", "Sozial", "Transz."]
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        fig.suptitle(title, fontsize=14)
        for i, name in enumerate(names):
            axes[0].plot(t, psi[:, i], label=f"psi_{i+1} ({name})")
        axes[0].set_ylabel("psi"); axes[0].legend(fontsize=7); axes[0].grid(True, alpha=0.3); axes[0].set_ylim(0, 1)
        axes[1].plot(t, phi, color="purple", label="Phi (IIT)")
        axes[1].set_ylabel("Phi"); axes[1].legend(); axes[1].grid(True, alpha=0.3)
        axes[2].plot(t, imp, color="green", label="IMP v2.0")
        axes[2].set_xlabel("Zeit"); axes[2].set_ylabel("IMP"); axes[2].legend(); axes[2].grid(True, alpha=0.3)
        plt.tight_layout(); plt.show()


if __name__ == "__main__":
    config = LagrangeConfig(hrv_rmssd=60.0)
    sim = LagrangeSimulator(config)
    psi0 = np.array([0.7, 0.5, 0.6, 0.3, 0.2])
    print(f"Simuliere von {psi0}...")
    traj = sim.simulate(psi0, t_span=(0, 100), n_steps=1000)
    print(f"Endzustand: {traj['psi'][-1].round(3)}")
    print(f"Final IMP: {traj['imp'][-1]:.4f}")
    sim.plot_trajectory(traj)
