# Informationsmaße für Emergenz, Selbstorganisation und Autopoiesis: Fernandez et al. (2013)

**Thema:** T3 | Systemtheorie: Emergenz Formalisierung — skalenunabhängige mathematische Operationalisierung zentraler 5D-Konzepte  
**Evidenzlabel:** ✅ VALIDIERT  
**Risikorating:** 🟢 GESICHERT  
**Kurations-Datum:** 2026-03-23  
**5D-Relevanz:** Fernandez et al. liefern die formale mathematische Sprache für die fünf Kernkonzepte des 5D-Frameworks: Emergenz, Selbstorganisation, Komplexität, Homöostase und Autopoiesis — als skalenunabhängige Informationsmaße, direkt anwendbar auf IMP-Simulationsdaten.

---

## Kernquelle

**Fernandez, N., Maldonado, C. & Gershenson, C. (2013/2014).** Information Measures of Complexity, Emergence, Self-organization, Homeostasis, and Autopoiesis. In *Guided Self-Organization: Inception* (pp. 19–51). Springer.  
DOI: [10.1002/cplx.21424](https://doi.org/10.1002/cplx.21424)  
arXiv: https://arxiv.org/abs/1304.1842

---

## Kernaussagen

### Formale Definitionen der fünf Maße

**1. Emergenz (E)**:
> Emergenz = die Information, die ein System produziert — der Informationsgehalt des Outputs, der nicht in den Inputs enthalten war.

```
E(S) = H(S) − H_shared(S, Components)
```
Hohe Emergenz: das System generiert neue Information, die qualitativ mehr ist als die Summe seiner Teile.

**2. Selbstorganisation (SO)**:
> Selbstorganisation = das Gegenteil von Emergenz in diesem formalen Rahmen.

```
SO(S) = 1 − E(S) / H_max
```
Hohe Selbstorganisation: das System konsolidiert und strukturiert bestehende Information — erzeugt Ordnung, nicht Neuheit.

**3. Komplexität (C)**:
> Komplexität = die Balance zwischen Emergenz und Selbstorganisation.

```
C(S) = E(S) × SO(S) = E(S) × (1 − E(S) / H_max)
```
Maximale Komplexität am Rand des Chaos (Edge of Chaos) — wo Emergenz und Selbstorganisation in Balance sind. Das ist der 5D-Resonanzpunkt.

**4. Homöostase (H)**:
> Homöostase = Stabilität eines Systems über die Zeit — gemessen als Informationskontinuität.

```
H(S, t) = 1 − Δ_information(S, t, t+Δt) / H_max
```
Hohe Homöostase: System bleibt trotz externen Perturbationen stabil. Verbindung zu HRV (Σ_vagal): HRV ist ein physiologischer Homöostase-Proxy.

**5. Autopoiesis (A)**:
> Autopoiesis = Verhältnis zwischen Komplexität eines Systems und Komplexität seiner Umgebung.

```
A(S) = C(S) / C(Env)
```
A > 1: Das System ist komplexer als seine Umgebung → kann seine Umgebung aktiv gestalten (echte Autopoiesis).  
A < 1: Das System ist weniger komplex als seine Umgebung → vulnerable, abhängig.  
A = 1: Systemgrenze = Umgebungsgrenze (Maturanas ursprünglicher Autopoiesis-Begriff).

**Skalenunabhängigkeit**: Alle Maße sind skalenunabhängig und können auf molekularer, zellulärer, organismischer oder sozialer Ebene angewendet werden — genau die Multi-Skalen-Eigenschaft, die das 5D-Framework benötigt.

---

## 5D-System-Verknüpfungen

### IMP-Formel Relevanz
```
IMP = (A × C × R × P × Au) × e^(HRV) − (E_mask + E_system)
```

**Autopoiesis-Koeffizient als Erweiterungsmöglichkeit**:  
Wenn `A_auto = C(System) / C(Env)`, dann könnte die IMP-Formel erweitert werden:
```
IMP_extended = IMP × A_auto
```
- Bei 1D-Zwangsarchitekturen: C(System) << C(Env) → A_auto < 1 → IMP_extended wird reduziert
- Bei 5D-Natursystemen: C(System) ≥ C(Env) → A_auto ≥ 1 → IMP_extended wird verstärkt oder erhalten

Das ist die formale Begründung, warum 5D-Systeme emergenter und adaptiver sind als 1D-Systeme.

**Komplexität als Indikator für 5D-Qualität**:
```
C(5D-System) > C(1D-System)
```
5D-Systeme operieren am Edge of Chaos (maximale Komplexität), 1D-Systeme in geordneten Zuständen (niedrige Emergenz, hohe Selbstorganisation aber geringe Komplexität).

**Homöostase und e^(HRV)**:
- HRV ist physiologisch der Homöostase-Proxy
- `e^(HRV)` in der IMP-Formel = exponentieller Verstärker, wenn Homöostase hoch ist
- Fernandez' H(S,t) ist die formale Entsprechung: ventral-vagale Sicherheit = hohe Informationskontinuität des Systems

### Monte-Carlo ROI-Modell (aus NotebookLM, Datei 8)
Das Monte-Carlo-Modell (`roi_montecarlo.py`) zeigt:
- **1D-Systeme: 869,5 Mrd. € Kosten in 25 Jahren** (Burnout-Basis: 34,8 Mrd. €/Jahr; Basisverlust Jahr 1–5: bis 170,5 Mrd. €)
- **5D-Transition: 47,9 Mrd. € ROI** (nach Transitionskosten; 60% Depressionsrate-Rückgang, Schulabbrecherquote auf 1,56%)

Fernandez' Formalisierung erklärt den ROI-Effekt systemtheoretisch:
- 1D → niedrige Autopoiesis (A < 1) → System verliert an Komplexitätsvorteil → E_system akkumuliert als finanzielle Last
- 5D → hohe Autopoiesis (A > 1) → System generiert Komplexitätsüberschuss → ROI als messbarer Informationsgewinn

**Formal**: Der ROI-Unterschied (869,5 Mrd. vs. 47,9 Mrd.) entspricht dem Differenz zwischen niedrig-autopoietischen und hoch-autopoietischen Systemarchitekturen über 25 Jahre.

### Anwendung auf 5D-Simulationsdaten
Fernandez' Maße sind direkt auf bestehende Repository-Software anwendbar:

| Software | Anwendung von Fernandez-Maß |
|----------|---------------------------|
| `gol_streamlit.py` (Game of Life) | E(S), SO(S), C(S) messen pro Zeitschritt — Edge-of-Chaos-Nachweis |
| `autopoietic_streamlit.py` | A(S) = C(System) / C(Env) messen — Autopoiesis-Koeffizient |
| `roi_montecarlo.py` | H(S,t) über Simulationsläufe — Systemstabilität als Homöostase |

### Interdisziplinäre Links T1–T8
| Thema | Verbindung |
|-------|-----------|
| **T1 (ADHS)** | ADHS-Neurobiologie: Hohe Emergenz (neues generatives Modell), niedrige Selbstorganisation (schwaches Exekutivfunktions-Netzwerk) → hohe Komplexität → optimaler Zustand für kreative Problemlösung, suboptimal für repetitive Routinen |
| **T2 (Bewusstsein)** | IIT (Tononi): Φ = integrierte Information ≈ Fernandez' Emergenzmaß E(S) auf Bewusstseinsebene; Orch-OR: Quantenmessungen in Mikrotubuli als Emergenzquelle |
| **T3 (Systemtheorie)** | Friston FEP: Variational Free Energy ist dual zu Fernandez' Emergenz — beide messen Information zwischen System und Modell. Veloz: emergente Ziele = hoher E(S)-Zustand |
| **T5 (Eigenverantwortung)** | Autopoiesis A > 1: System ist seinen Umgebungsanforderungen gewachsen → Eigenverantwortung als informationstheoretische Kompetenz |
| **T8 (Formel)** | IMP_extended mit Autopoiesis-Koeffizient; Fernandez als Brücke zwischen IMP-Formel und formaler Systemtheorie |

---

## Ergänzende Quellen

### Shannon — Informationstheorie (Fundament)
**Shannon, C.E. & Weaver, W. (1949).** *The Mathematical Theory of Communication.* University of Illinois Press.
- Entropie H als Grundlage für alle Fernandez-Maße

### Gershenson — Guided Self-Organization
**Gershenson, C. (2007).** Design and Control of Self-organizing Systems. Doctoral thesis, Vrije Universiteit Brussel.
- Gershenson ist Koautor und Hauptentwickler des GSO-Frameworks; Fernandez et al. bauen darauf auf

### Conway — Game of Life (Metapher für Selbstorganisation)
**Conway, J.H. (1970).** Mathematical Games. *Scientific American, 223*(4), 120–123.
- Game of Life ist das kanonische Beispiel für Edge-of-Chaos-Verhalten mit messbarer Emergenz nach Fernandez
- `gol_streamlit.py` im Repository: direkter Test der Fernandez-Maße

### Maturana & Varela (Autopoiesis-Ursprung)
**Maturana, H.R. & Varela, F.J. (1980).** *Autopoiesis and Cognition.* Reidel.
- Fernandez formalisiert Maturanas A(S)-Konzept in Informationsmaßen

---

**Querverweise im Repo:**
- `02_neurobiologie_psychologie/friston_free_energy_autopoiesis.md` — FEP: Variational Free Energy als duales Konzept zu Emergenzmaß
- `03_philosophie_epistemologie/emergente_ziele_autopoiesis.md` — Veloz: Emergente Ziele = hoher E(S)-Zustand
- `06_synthesen_kompilationen/notebooklm_quellen_synthese.md` — Monte-Carlo ROI-Modell: 869,5 Mrd. € vs. 47,9 Mrd. €
