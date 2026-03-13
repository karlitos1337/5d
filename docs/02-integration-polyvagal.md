# Polyvagal-Theorie Integration im 5D-System

## Uebersicht

Die Polyvagal-Theorie (Porges, 1994, 2011) beschreibt wie das autonome Nervensystem nicht binaer (Sympathikus/Parasympathikus), sondern hierarchisch in drei Stufen reguliert - mit direkten Implikationen fuer Bewusstsein und soziales Verhalten. Diese Seite dokumentiert die Integration dieser Theorie in das 5D-Modell.

## Grundlagen der Polyvagal-Theorie

### Die drei Regulationsstufen

| Stufe | System | HRV | Zustand | 5D-Korrelat |
|-------|--------|-----|---------|-------------|
| 1 | Ventral-vagal | Hoch (RMSSD > 50ms) | Sicherheit, Verbundenheit | psi_4 hoch |
| 2 | Sympathisch | Mittel (25-50ms) | Mobilisierung, Stress | psi_2 niedrig |
| 3 | Dorsal-vagal | Niedrig (< 25ms) | Erstarrung, Dissoziation | psi_3 niedrig |

### Neuroception

**Definition** (Porges): Unbewusste Wahrnehmung von Sicherheit/Gefahr durch das Nervensystem

- **Sicherheits-Neuroception**: Aktiviert ventral-vagalen Zustand
- **Gefahren-Neuroception**: Aktiviert Sympathikus
- **Lebensbedrohungs-Neuroception**: Aktiviert dorsalen Vagus

Implikation fuer 5D: Neuroception bestimmt den "baseline" HRV-Wert, der als Eingabe fuer gamma(HRV) im IMP v2.0 dient.

### Social Engagement System

Portes beschreibt ein "Social Engagement System" (SES) als Cluster von ventral-vaga regulierten Verhaltensweisen:

- Gesichtsmuskeln (Mimik, Blickkontakt)
- Mittelohr (prosodische Sprachwahrnehmung)
- Kehlkopf (Vokalisation)
- Herzrhythmus (vagale Bremse)

**5D-Mapping**:
- SES aktiv: psi_4 (Soziale Verbundenheit) max
- SES gehemmt: psi_4 sinkt, psi_1 ggf. kompensierend hoch

## Mathematische Integration

### HRV als Proxy-Variable

HRV (Herzratenvariabilitaet) als messbarer Proxy fuer vagalen Tonus:

```
HRV_RMSSD = sqrt(mean(diff(RR_intervalle)^2))
```

**Normwerte** (gesunde Erwachsene):
- RMSSD: 20-80 ms (Mittel ~42 ms)
- SDNN: 30-100 ms
- Altersbezogen: nimmt mit Alter ab

### Polyvagaler Zustand aus HRV

```python
def polyvagal_state(hrv_rmssd: float) -> str:
    if hrv_rmssd >= 50:
        return 'ventral_vagal'  # Sicherheit
    elif hrv_rmssd >= 25:
        return 'sympathisch'    # Mobilisierung  
    else:
        return 'dorsal_vagal'   # Erstarrung
```

### Daempfungskoeffizient gamma

Die Polyvagal-Daempfung des IMP-Potentials:

```
gamma(HRV) = {
    gamma_ventral * (1 - 0.5 * HRV/100)  wenn ventral-vagal
    gamma_sympathisch                      wenn sympathisch
    gamma_dorsal                           wenn dorsal-vagal
}
```

Standardwerte:
- gamma_ventral = 0.1 (niedrig, hohe Flexibilitaet)
- gamma_sympathisch = 0.4 (moderat)
- gamma_dorsal = 0.8 (stark, eingeschraenkte Flexibilitaet)

### IMP v2.0 Formel mit Polyvagal

```
IMP = (w^T * psi) * (1 - gamma(HRV)) * (1 + k_Phi * Phi) * P_perc
```

Interpretation des Polyvagal-Faktors (1 - gamma):
- Ventral-vagal: 0.85-0.90 (maximale Ausschoepfung des Potentials)
- Sympathisch: 0.60 (eingeschraenkt)
- Dorsal-vagal: 0.20 (stark eingeschraenkt)

## 5D-Dimensionen und Polyvagal

### Dimension 1: Kognitive Kohaerenz (psi_1)

Polyvagaler Einfluss auf Kognition:
- Ventral-vagal: prefrontale Regulation optimal, Executive Functions hoch
- Sympathisch: Tunnelblick, schnelle Verarbeitung, kreative Einschraenkung
- Dorsal-vagal: kognitive Verlangsamung, Dissoziation

**Messung**: Stroop-Test, N-back-Aufgaben, EEG-Kohaerenz

### Dimension 2: Emotionale Regulation (psi_2)

- Ventral-vagal: emotionale Flexibilitaet, Co-Regulation moeglich
- Sympathisch: erhoehte Reaktivitaet, eingeschraenkte Regulation
- Dorsal-vagal: emotionale Taubheit, Flat-affect

**Messung**: RMSSD waehrend Emotionsregulationsaufgaben

### Dimension 3: Somatische Integration (psi_3)

Interozeption (Koerperwahrnehmung):
- Ventral-vagal: gute Interozeption, Koerper-Geist-Verbindung
- Sympathisch: Hyperarousal, Koerperanspannung
- Dorsal-vagal: Interozeptionsdefizit, "felt sense" eingeschraenkt

**Messung**: Heartbeat Detection Task, SSAS (Somatic Symptom Questionnaire)

### Dimension 4: Soziale Verbundenheit (psi_4)

Direkte SES-Aktivierung:
- Ventral-vagal: SES voll aktiv, Augenkontakt, Prosodie, Empathie
- Sympathisch: defensive soziale Signale
- Dorsal-vagal: sozialer Rueckzug, Isolation

**Messung**: Oxytocin-Level, gaze tracking, prosodische Analyse

### Dimension 5: Transzendente Oeffnung (psi_5)

- Ventral-vagal: Zugang zu Bedeutung, Flow-Zustaenden, Awe
- Sympathisch: Kontrollbeduerfnis, geringe Offenheit
- Dorsal-vagal: existenzielle Leere, Sinnlosigkeit

**Messung**: Awe-Skala, Mystical Experience Questionnaire

## Klinische Relevanz

### Trauma und Polyvagal

Nach van der Kolk (2014) und Levine (2015) haengt Trauma-Heilung direkt mit vagaler Regulation zusammen:

1. **Traumatisiert**: Dominanz dorsaler Vagus-Reaktionen
2. **Heilungsprozess**: Schrittweise Reaktivierung des SES
3. **Heilung**: Stabiler ventral-vagaler Baseline

**5D-Implikation**: Trauma-Behandlungserfolg messbar als Anstieg von HRV-RMSSD und psi_3/psi_4

### Somatic Experiencing und 5D

Levines "Somatic Experiencing" (SE) arbeitet direkt mit Polyvagal-Regulation:
- Titration: schrittweise Annaeherung an traumatisches Material
- Pendulation: Wechsel zwischen Ressource und Aktivierung
- Completion: Vollstaendige Durcharbeitung von Abwehrreflexen

Diese Konzepte koennten als spezifische Trajektorien im 5D-Lagrange-Phasenraum formalisiert werden.

## Messprotokoll

### HRV-Messung

**Standard**: EKG oder Photoplethysmographie (PPG)

1. 5 Minuten Ruhemessung (liegend)
2. 1 Minute Tiefattmung (5s ein/aus)
3. 5 Minuten Stressinduktion (Stressoren nach Kontext)
4. 10 Minuten Erholung
5. RMSSD, SDNN, pNN50 berechnen

**Geraete**: Polar H10, Garmin strap, medizinisches Holter-EKG

### 5D-Assessment kombiniert mit HRV

```python
from models.imp_v2 import State5D, imp_v2

# Messung und Berechnung
state = State5D(
    psi_1=kognitive_kohaerenz,
    psi_2=emotionale_regulation,
    psi_3=somatische_integration,
    psi_4=soziale_verbundenheit,
    psi_5=transzendente_oeffnung,
    hrv_rmssd=gemessener_wert,
)

result = imp_v2(state, verbose=True)
```

## Validierung und Evidenz

### Empirische Studien

1. **HRV und Kognition**: Thayer et al. (2012) - vagale Aktivitaet korreliert mit prefrontalem Kortex
2. **HRV und Emotion**: Appelhans & Luecken (2006) - RMSSD als Emotionsregulations-Marker
3. **Polyvagal und Trauma**: Porges (2011) - Klinische Validierung
4. **Neuroception**: Porges (2003) - Grundlagenforschung

### Limitierungen der HRV-Messung

- HRV spiegelt nicht ausschliesslich vagalen Tonus wider
- Atemfrequenz und Koerperhaltung beeinflussen RMSSD
- Individuelle Baseline-Unterschiede gross
- Kontextabhaengigkeit (Koffein, Schlaef, Training)

**Empfehlung**: Longitudinale Messung, interindividuelle Kalibration

## Referenzen

- **Porges, S. W.** (1994). The polyvagal theory: Phylogenetic substrates of a social nervous system. International Journal of Psychophysiology.
- **Porges, S. W.** (2011). The Polyvagal Theory. Norton.
- **van der Kolk, B.** (2014). The Body Keeps the Score. Viking.
- **Levine, P.** (2015). Trauma and Memory. North Atlantic Books.
- **Thayer, J. F., et al.** (2012). A meta-analysis of heart rate variability and neuroimaging studies. Neuroscience & Biobehavioral Reviews.

---

**Status**: Aktiv  
**Implementierung**: `/models/imp_v2.py`  
**Simulator**: `/models/lagrange_simulator.py`
