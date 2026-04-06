"""
5D-Natursystem: IMP v3.0 Masterformeln
========================================
Architekturspezifikation v3.0 — Epistemologie, Thermodynamik und Maschinelle Kohärenz

Implementiert:
  - Φ₅D  : Intrinsisches Motivationspotenzial (IMP 2.0)
  - SM    : System-Manifestation (kinetische Handlungsamplitude)
  - dS    : Entropieschuld (biologischer Kollaps-Indikator)

Autor : karlitos1337
Datum : 2026-04-06
Version: 3.0.0
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Konstanten & Triage-Parameter
# ---------------------------------------------------------------------------

EPSILON: float = 1e-6          # Asymptotischer Nullpunkt — verhindert harten Kollaps auf 0
VAGAL_TRAUMA: float = -2.0     # σ_vagal bei schwerem Trauma   → Φ₅D ≈ 13 % Normwert
VAGAL_FLOW:   float = 1.5      # σ_vagal bei Flow-Zustand      → Φ₅D ≈ 448 % Normwert
RHO_SEED:     float = 0.075    # Perkolations-Keimzelle   ρ_seed ≈ 7,5 %
RHO_CRITICAL: float = 0.25     # Normativer Tipping Point  ρ_crit ≈ 24–27 %


# ---------------------------------------------------------------------------
# Datenmodell: SDT-Parameter eines Systemknotens
# ---------------------------------------------------------------------------

@dataclass
class SDTNode:
    """
    Repräsentiert einen autopoietischen Systemknoten mit allen SDT-Variablen.

    Alle Rohwerte werden intern per Triage-Faktor max(ε, X) gesichert,
    sodass ein Kollaps auf 0 biologisch unmöglich ist (asymptotische Triage).

    Attribute
    ----------
    autonomy        : A_t  — Autonomieerleben   [0, 1]
    competence      : C_t  — Kompetenzerleben   [0, 1]
    resonance       : R_t  — Resonanz / Relatedness [0, 1]
    participation   : P_t  — Partizipation      [0, 1]
    authenticity    : Au_t — Authentizität      [0, 1]
    sigma_vagal     : σ_vagal — Z-normierte HRV (RMSSD); typisch [-3, +3]
    epsilon_mask    : ε_mask — Interner Verstellungsaufwand [0, ∞)
    epsilon_exo     : ε_exo  — Toxischer Umweltdruck       [0, ∞)
    """
    autonomy:      float = 0.5
    competence:    float = 0.5
    resonance:     float = 0.5
    participation: float = 0.5
    authenticity:  float = 0.5
    sigma_vagal:   float = 0.0
    epsilon_mask:  float = 0.0
    epsilon_exo:   float = 0.0

    def __post_init__(self) -> None:
        for attr in ("autonomy", "competence", "resonance", "participation", "authenticity"):
            val = getattr(self, attr)
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"{attr} muss in [0, 1] liegen, erhalten: {val}")
        if self.epsilon_mask < 0 or self.epsilon_exo < 0:
            raise ValueError("Entropie-Terme müssen ≥ 0 sein.")

    # ------------------------------------------------------------------
    # Triage-Mechanik: X_t = max(ε, X)
    # ------------------------------------------------------------------

    @property
    def _A(self) -> float: return max(EPSILON, self.autonomy)
    @property
    def _C(self) -> float: return max(EPSILON, self.competence)
    @property
    def _R(self) -> float: return max(EPSILON, self.resonance)
    @property
    def _P(self) -> float: return max(EPSILON, self.participation)
    @property
    def _Au(self) -> float: return max(EPSILON, self.authenticity)


# ---------------------------------------------------------------------------
# Dimension 5: Masterformeln
# ---------------------------------------------------------------------------

class NaturSystem5D:
    """
    Implementierung der drei Masterformeln des 5D-Natursystems (v3.0).

    Formeln
    -------
    Φ₅D = (A·C·R·P·Au)^0.2 · e^σ_vagal − (ε_mask + ε_exo)

    SM  = Φ₅D · D_ext                          wenn Φ₅D > 0  (Resonanz-Zustand)
        = D_ext · Au_t                          wenn Φ₅D ≤ 0  (Zwangs-Zustand)

    dS  = |Φ₅D| · D_ext · e^(−σ_vagal)         (nur relevant wenn Φ₅D ≤ 0)
    """

    def __init__(self, node: SDTNode) -> None:
        self.node = node

    # ------------------------------------------------------------------
    # 5.1 — Intrinsisches Motivationspotenzial Φ₅D
    # ------------------------------------------------------------------

    def phi_5d(self) -> float:
        """
        Φ₅D: Autopoietische Bandbreite des Systemknotens.

        Geometrisches Mittel der SDT-Parameter (Liebigs Minimumgesetz →
        strikt multiplikativ), potenziert durch den vagalen Booster,
        abzüglich subtraktiver Entropie.

        Returns
        -------
        float — kann negativ sein (1D-Zwangszustand)
        """
        n = self.node
        geometric_mean = (n._A * n._C * n._R * n._P * n._Au) ** 0.2
        vagal_booster  = math.exp(n.sigma_vagal)
        entropy_loss   = n.epsilon_mask + n.epsilon_exo
        return geometric_mean * vagal_booster - entropy_loss

    # ------------------------------------------------------------------
    # 5.2 — System-Manifestation SM
    # ------------------------------------------------------------------

    def system_manifestation(self, d_ext: float) -> float:
        """
        SM: Kinetische Handlungsamplitude unter externem Druck D_ext.

        Zustandslogik
        -------------
        5D-Resonanz  (Φ₅D > 0) : SM = Φ₅D · D_ext
            → Leistung aus autopoietischer Kraft; Entropieschuld = 0

        1D-Zwang     (Φ₅D ≤ 0) : SM = D_ext · Au_t
            → Leistung durch Cortisol-Zwang; innere Entkopplung,
              Entropieschuld wächst exponentiell (→ dS)

        Parameters
        ----------
        d_ext : externer Druck [0, ∞)

        Returns
        -------
        float ≥ 0
        """
        if d_ext < 0:
            raise ValueError("Externer Druck D_ext muss ≥ 0 sein.")
        phi = self.phi_5d()
        if phi > 0:
            return phi * d_ext                    # 5D-Resonanzzustand
        else:
            return d_ext * self.node._Au          # 1D-Zwangssystem

    # ------------------------------------------------------------------
    # 5.3 — Entropieschuld dS (Biologischer Kollaps-Indikator)
    # ------------------------------------------------------------------

    def entropy_debt(self, d_ext: float) -> float:
        """
        dS: Akkumulierte Entropieschuld pro Zeiteinheit.

        Nur relevant im 1D-Zwangszustand (Φ₅D ≤ 0).
        Übersteigt ΣdS die biologische Kapazität → SM friert auf 0 ein
        (strukturelle Singularität: Burnout / Herzinfarkt).

        dS = |Φ₅D| · D_ext · e^(−σ_vagal)

        Parameters
        ----------
        d_ext : externer Druck [0, ∞)

        Returns
        -------
        float ≥ 0  (0 wenn Φ₅D > 0, da kein Verschleiß im Resonanzzustand)
        """
        if d_ext < 0:
            raise ValueError("Externer Druck D_ext muss ≥ 0 sein.")
        phi = self.phi_5d()
        if phi > 0:
            return 0.0                                          # Kein Verschleiß
        return abs(phi) * d_ext * math.exp(-self.node.sigma_vagal)

    # ------------------------------------------------------------------
    # Vollständiger System-Report
    # ------------------------------------------------------------------

    def report(self, d_ext: float) -> dict:
        """
        Gibt alle Systemwerte als Dict zurück.

        Parameters
        ----------
        d_ext : externer Druck

        Returns
        -------
        dict mit Φ₅D, SM, dS, Systemzustand, vagalem Booster-Faktor
        """
        phi  = self.phi_5d()
        sm   = self.system_manifestation(d_ext)
        ds   = self.entropy_debt(d_ext)
        state = "5D-Resonanz ✅" if phi > 0 else "1D-Zwang ⚠️"

        return {
            "Φ₅D":              round(phi, 6),
            "SM":               round(sm,  6),
            "dS":               round(ds,  6),
            "Systemzustand":    state,
            "vagaler_booster":  round(math.exp(self.node.sigma_vagal), 4),
            "D_ext":            d_ext,
            "sigma_vagal":      self.node.sigma_vagal,
            "SDT_geo_mean":     round(
                (self.node._A * self.node._C * self.node._R
                 * self.node._P * self.node._Au) ** 0.2, 6
            ),
        }


# ---------------------------------------------------------------------------
# Perkolations-Schwellenwert-Check (Dimension 3)
# ---------------------------------------------------------------------------

def percolation_state(rho: float) -> str:
    """
    Gibt den Netzwerkzustand basierend auf dem Anteil authentischer Knoten ρ zurück.

    Parameters
    ----------
    rho : Anteil authentischer 5D-Akteure im Netzwerk [0, 1]

    Returns
    -------
    str — Zustandsbeschreibung mit Schwellenwert-Einordnung
    """
    if rho < RHO_SEED:
        return f"🔴 Isoliert (ρ={rho:.1%} < ρ_seed={RHO_SEED:.1%}): Kein Giant Component."
    elif rho < RHO_CRITICAL:
        return (f"🟡 Vernetzt (ρ={rho:.1%} ≥ ρ_seed={RHO_SEED:.1%}): "
                f"Giant Component aktiv, normativer Druck hält noch an.")
    else:
        return (f"🟢 Kipppunkt überschritten (ρ={rho:.1%} ≥ ρ_crit={RHO_CRITICAL:.1%}): "
                f"Minority Rule — 1D-System kollabiert thermodynamisch.")


# ---------------------------------------------------------------------------
# Schnelltest / Demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("5D-Natursystem — IMP v3.0 Masterformeln")
    print("=" * 60)

    scenarios = [
        ("Trauma-Zustand",     SDTNode(0.2, 0.2, 0.1, 0.15, 0.1, VAGAL_TRAUMA, 0.3, 0.4)),
        ("Durchschnitts-Knoten", SDTNode(0.5, 0.5, 0.5, 0.5, 0.5, 0.0,          0.1, 0.1)),
        ("Flow-Zustand",       SDTNode(0.9, 0.85, 0.9, 0.8, 0.95, VAGAL_FLOW,   0.0, 0.0)),
    ]

    D_EXT = 1.0

    for name, node in scenarios:
        sys5d = NaturSystem5D(node)
        r = sys5d.report(D_EXT)
        print(f"\n--- {name} ---")
        for k, v in r.items():
            print(f"  {k:<20}: {v}")

    print("\n--- Perkolations-Check ---")
    for rho in [0.04, 0.10, 0.27]:
        print(f"  {percolation_state(rho)}")

    print("\n✅ IMP v3.0 geladen.")
