"""IMP v2.0 - Integrierte Manifestations-Potential Formel

Erweiterte Version mit:
- Polyvagal-Theorie Integration (HRV-basierte Daempfung)
- IIT-basierte integrierte Information (Phi)
- Perkolations-Dynamik fuer Bewusstseinsphasenuebergaenge
- Lagrange-Formalismus als theoretisches Fundament

Referenzen:
    - Tononi et al. (2016) Integrated Information Theory
    - Porges (2011) The Polyvagal Theory
    - Stauffer & Aharony (1994) Introduction to Percolation Theory
    - Friston (2010) The free-energy principle
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class State5D:
    """5D Bewusstseinszustand nach IMP v2.0 Modell."""

    psi_1: float = 0.5  # Kognitive Kohaerenz [0, 1]
    psi_2: float = 0.5  # Emotionale Regulation [0, 1]
    psi_3: float = 0.5  # Somatische Integration [0, 1]
    psi_4: float = 0.5  # Soziale Verbundenheit [0, 1]
    psi_5: float = 0.5  # Transzendente Oeffnung [0, 1]
    hrv_rmssd: float = 50.0  # HRV RMSSD in ms
    hrv_sdnn: float = 60.0   # HRV SDNN in ms

    @property
    def psi_vec(self) -> np.ndarray:
        """Gibt den 5D Zustandsvektor zurueck."""
        return np.array([self.psi_1, self.psi_2, self.psi_3, self.psi_4, self.psi_5])

    @property
    def polyvagal_state(self) -> str:
        """Bestimmt den Polyvagal-Zustand aus HRV."""
        if self.hrv_rmssd >= 50:
            return "ventral_vagal"  # Sicherheit, Verbundenheit
        elif self.hrv_rmssd >= 25:
            return "sympathisch"    # Mobilisierung, Stress
        else:
            return "dorsal_vagal"   # Erstarrung, Dissoziation


@dataclass
class IMPv2Config:
    """Konfiguration fuer IMP v2.0 Berechnung."""

    # Polyvagal-Daempfungskoeffizienten
    gamma_ventral: float = 0.1   # Niedrige Daempfung bei Sicherheit
    gamma_sympathisch: float = 0.4  # Moderate Daempfung bei Mobilisierung
    gamma_dorsal: float = 0.8    # Starke Daempfung bei Erstarrung

    # IIT-Gewicht
    k_phi: float = 1.0

    # Perkolations-Parameter
    perkolation_threshold: float = 0.6  # Kritischer Schwellenwert pc
    perkolation_beta: float = 0.45      # Kritischer Exponent (2D)

    # Dimensionsgewichte fuer IMP
    weights: np.ndarray = field(
        default_factory=lambda: np.array([0.25, 0.25, 0.20, 0.15, 0.15])
    )


def gamma_hrv(state: State5D, config: IMPv2Config) -> float:
    """Berechnet den HRV-basierten Daempfungskoeffizienten.

    Args:
        state: Aktueller 5D Bewusstseinszustand
        config: IMP v2.0 Konfiguration

    Returns:
        Daempfungskoeffizient gamma basierend auf Polyvagal-Zustand
    """
    pv_state = state.polyvagal_state
    if pv_state == "ventral_vagal":
        # Kontinuierliche Interpolation basierend auf RMSSD
        normalized_hrv = min(state.hrv_rmssd / 100.0, 1.0)
        return config.gamma_ventral * (1.0 - 0.5 * normalized_hrv)
    elif pv_state == "sympathisch":
        return config.gamma_sympathisch
    else:
        return config.gamma_dorsal


def phi_iit(psi: np.ndarray) -> float:
    """Approximiert die integrierte Information Phi nach IIT.

    Vereinfachte Berechnung als Proxy-Mass:
        Phi ~ Varianz(system) - Mittel(Varianz(parts))

    Args:
        psi: 5D Zustandsvektor

    Returns:
        Naehreungsweiser Phi-Wert (>0 = integriert)
    """
    system_var = np.var(psi)
    # Teile System in zwei Haelften (grobe Partition)
    mid = len(psi) // 2
    part1_var = np.var(psi[:mid]) if mid > 0 else 0
    part2_var = np.var(psi[mid:]) if len(psi) - mid > 0 else 0
    phi_approx = system_var - (part1_var + part2_var) / 2
    return float(max(phi_approx, 0.0))


def perkolation_p(psi: np.ndarray, config: IMPv2Config) -> float:
    """Berechnet den effektiven Verbindungsgrad fuer Perkolationsmodell.

    Args:
        psi: 5D Zustandsvektor
        config: IMP v2.0 Konfiguration

    Returns:
        Verbindungsgrad p in [0, 1]
    """
    linear_comb = np.dot(config.weights, psi)
    return float(1.0 / (1.0 + np.exp(-10 * (linear_comb - config.perkolation_threshold))))


def perkolation_order_param(p: float, config: IMPv2Config) -> float:
    """Berechnet den Perkolations-Ordnungsparameter.

    Args:
        p: Verbindungsgrad
        config: IMP v2.0 Konfiguration

    Returns:
        Ordnungsparameter (0 = kein makroskopisches Cluster,
                          >0 = kohaerentes Bewusstsein emergiert)
    """
    pc = config.perkolation_threshold
    beta = config.perkolation_beta
    if p >= pc:
        return float((p - pc) ** beta)
    return 0.0


def imp_v2(
    state: State5D,
    config: Optional[IMPv2Config] = None,
    verbose: bool = False,
) -> dict:
    """Berechnet IMP v2.0 - Integriertes Manifestations-Potential.

    Formel:
        IMP = w^T * psi * (1 - gamma(HRV)) * (1 + k_Phi * Phi) * P_perc

    Args:
        state: 5D Bewusstseinszustand
        config: Konfiguration (Standard wenn None)
        verbose: Gibt Zwischenergebnisse aus

    Returns:
        Dictionary mit IMP-Wert und allen Teilkomponenten
    """
    if config is None:
        config = IMPv2Config()

    psi = state.psi_vec

    # 1. Basispotential aus gewichteten Dimensionen
    base = float(np.dot(config.weights, psi))

    # 2. Polyvagal-Daempfung
    gamma = gamma_hrv(state, config)
    polyvagal_factor = 1.0 - gamma

    # 3. IIT-Integration
    phi = phi_iit(psi)
    iit_factor = 1.0 + config.k_phi * phi

    # 4. Perkolations-Emergenz
    p = perkolation_p(psi, config)
    p_order = perkolation_order_param(p, config)
    # Emergenz-Booster: volle Wirkung wenn Perkolation > 0
    perc_factor = 1.0 + p_order

    # Gesamt-IMP
    imp = base * polyvagal_factor * iit_factor * perc_factor

    result = {
        "imp": imp,
        "base": base,
        "gamma": gamma,
        "polyvagal_state": state.polyvagal_state,
        "polyvagal_factor": polyvagal_factor,
        "phi": phi,
        "iit_factor": iit_factor,
        "perkolation_p": p,
        "perkolation_order": p_order,
        "perc_factor": perc_factor,
        "psi": psi.tolist(),
        "hrv_rmssd": state.hrv_rmssd,
    }

    if verbose:
        print(f"IMP v2.0 Berechnung:")
        print(f"  Basis (w^T * psi):        {base:.4f}")
        print(f"  HRV/Polyvagal:            {state.polyvagal_state} (gamma={gamma:.3f})")
        print(f"  IIT Phi:                  {phi:.4f} (Faktor: {iit_factor:.4f})")
        print(f"  Perkolation p:            {p:.4f} (Ordnung: {p_order:.4f})")
        print(f"  Gesamt IMP:               {imp:.4f}")

    return result


if __name__ == "__main__":
    # Beispiel 1: Optimaler Zustand (hohe HRV, alle Dimensionen aktiv)
    print("=" * 50)
    print("Beispiel 1: Optimaler Zustand")
    optimal = State5D(
        psi_1=0.9, psi_2=0.85, psi_3=0.8, psi_4=0.75, psi_5=0.7,
        hrv_rmssd=80.0
    )
    result1 = imp_v2(optimal, verbose=True)
    print(f"  IMP = {result1['imp']:.4f}")

    print()

    # Beispiel 2: Stresszustand (niedrige HRV, reduzierte Verbundenheit)
    print("=" * 50)
    print("Beispiel 2: Akuter Stresszustand")
    stress = State5D(
        psi_1=0.6, psi_2=0.3, psi_3=0.4, psi_4=0.3, psi_5=0.2,
        hrv_rmssd=20.0
    )
    result2 = imp_v2(stress, verbose=True)
    print(f"  IMP = {result2['imp']:.4f}")

    print()

    # Beispiel 3: Erholung (mittlere HRV, wachsende Integration)
    print("=" * 50)
    print("Beispiel 3: Erholungszustand")
    recovery = State5D(
        psi_1=0.7, psi_2=0.65, psi_3=0.6, psi_4=0.55, psi_5=0.5,
        hrv_rmssd=40.0
    )
    result3 = imp_v2(recovery, verbose=True)
    print(f"  IMP = {result3['imp']:.4f}")
