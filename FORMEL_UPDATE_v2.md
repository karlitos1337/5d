# 5D-Intelligence Framework - Formel Update v2.0

**Datum**: 05.12.2025, 00:30 CET  
**Status**: Definitive mathematische Spezifikation

---

## 1. KERN-FORMEL (Normalisiert)

### Vollständige Formel:

```
IMP = [(A/xₐ) × (IM/xᵢₘ) × (R/xᵣ) × (SP/xₛₚ) × (AU/xₐᵤ)] / k
```

**Wo**:
- **IMP** = Intelligence-Motivation-Participation Score (Endergebnis: 0.001 - 0.95)
- **A** = Autonomie-Score (gemessen: 0.001 - 5.0)
- **IM** = Intrinsische Motivation-Score (gemessen: 0.001 - 5.0)
- **R** = Resilienz-Score (gemessen: 0.001 - 5.0)
- **SP** = Soziale Partizipation-Score (gemessen: 0.001 - 5.0)
- **AU** = Authentizität/Umgebung-Score (gemessen: 0.001 - 5.0)
- **xₐ, xᵢₘ, xᵣ, xₛₚ, xₐᵤ** = Genetische Veranlagungsfaktoren (0.1 - 10.0)
- **k** = Normalisierungskonstante (siehe unten)

---

## 2. GENETISCHER VERANLAGUNGSFAKTOR (x)

### Bedeutung:

**x repräsentiert den "genetischen Aufwandsmultiplikator"**:

- **x < 1.0** → **Hochbegabung**: Genetisch bevorzugt, wenig Aufwand nötig
  - Beispiel: x = 0.5 bedeutet "doppelte Effizienz" durch genetische Begabung
  - Score/x wird größer → höherer IMP

- **x = 1.0** → **Durchschnitt**: Normales genetisches Potenzial
  - Score/x = Score (keine Veränderung)

- **x > 1.0** → **Benachteiligung**: Genetisch erschwert, mehr Aufwand nötig
  - Beispiel: x = 2.0 bedeutet "doppelter Aufwand" für gleiches Ergebnis
  - Score/x wird kleiner → niedrigerer IMP

### Wertebereich:

```
xₘᵢₙ = 0.1  (extreme genetische Begabung - 10x Effizienz)
xₙₒᵣₘ = 1.0  (durchschnittliche Veranlagung)
xₘₐₓ = 10.0 (extreme genetische Benachteiligung - 10x Aufwand)
```

### Praktische Interpretation:

| x-Wert | Bedeutung | Reales Beispiel |
|--------|-----------|----------------|
| 0.2 | Hochbegabt (5x Effizienz) | Naturtalent in Mathematik |
| 0.5 | Überdurchschnittlich (2x) | Schnelles Lernen |
| 1.0 | Durchschnitt | Normale Entwicklung |
| 2.0 | Unterdurchschnittlich | Lernschwierigkeit |
| 5.0 | Stark benachteiligt | Schwere Beeinträchtigung |

---

## 3. SCORE-BESCHRÄNKUNGEN

### Minimum-Regel:

```
ALLE Dimensionen: Score ≥ 0.001 (statt 0.0)
```

**Begründung**: 
- **Realistische Modellierung**: Niemand hat wirklich 0% in einer Dimension
- **Mathematische Stabilität**: Vermeidet Division durch Null
- **Psychologische Validität**: Selbst bei schwersten Einschränkungen existiert Restfunktion

### Maximum-Regel:

```
ALLE Dimensionen: Score ≤ 4.75 (95% von 5.0)
```

**Begründung**:
- **Realistische Modellierung**: Niemand erreicht 100% Perfektion
- **Messtheorie**: Deckeneffekte vermeiden
- **Empirische Validierung**: Höchste gemessene Werte liegen bei 90-95%

---

## 4. IMP-BESCHRÄNKUNGEN

```
IMP_min = 0.001  (minimales menschliches Potenzial)
IMP_max = 0.95   (maximal erreichbar, 95% des Theoretischen)
```

---

## 5. PYTHON IMPLEMENTATION

```python
import numpy as np

class IMP_Calculator_v2:
    def __init__(self):
        self.SCORE_MIN = 0.001
        self.SCORE_MAX = 4.75  # 95% von 5.0
        self.IMP_MIN = 0.001
        self.IMP_MAX = 0.95
        self.K = 3125  # 5^5
        
    def clip_score(self, score):
        return max(self.SCORE_MIN, min(self.SCORE_MAX, score))
    
    def clip_imp(self, imp):
        return max(self.IMP_MIN, min(self.IMP_MAX, imp))
    
    def calculate(self, dimensions, x_factors):
        # Normalisierung mit genetischen Faktoren
        A_norm = self.clip_score(dimensions['A']) / x_factors['x_a']
        IM_norm = self.clip_score(dimensions['IM']) / x_factors['x_im']
        R_norm = self.clip_score(dimensions['R']) / x_factors['x_r']
        SP_norm = self.clip_score(dimensions['SP']) / x_factors['x_sp']
        AU_norm = self.clip_score(dimensions['AU']) / x_factors['x_au']
        
        # Multiplikation und Normalisierung
        raw_product = A_norm * IM_norm * R_norm * SP_norm * AU_norm
        imp_normalized = raw_product / self.K
        
        # IMP-Clipping
        return self.clip_imp(imp_normalized)

# Beispiel:
calc = IMP_Calculator_v2()

imp = calc.calculate(
    dimensions={'A': 4.0, 'IM': 4.5, 'R': 3.5, 'SP': 2.5, 'AU': 3.8},
    x_factors={'x_a': 0.2, 'x_im': 1.0, 'x_r': 1.0, 'x_sp': 1.5, 'x_au': 1.0}
)
print(f"IMP: {imp:.3f} ({imp*100:.1f}%)")
```

---

**Status**: ✅ Ready for Implementation  
**Version**: 2.0  
**Datum**: 05.12.2025
