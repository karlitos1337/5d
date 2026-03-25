# 🗺️ TECHNISCHE ROADMAP — karlitos1337/5d
> Lead Architect & Data Scientist: PKarletz | Stand: März 2026
> Basis: Harmonisches Manifest V3.x · 5D-Systemtheorie · Cluster-CSV

---

## SYSTEMKRITISCHE SÄULEN — ÜBERSICHT

| # | Säule | Priorität | Status | Schlüsseldatei |
|---|-------|-----------|--------|----------------|
| 1 | Datenanalyse & Cluster-Modellierung | 🔴 KRITISCH | ✅ Initialer Code fertig | `cluster_analysis.py` |
| 2 | Psychometrische Validierung (IRT) | 🔴 KRITISCH | 🟡 Konzept | `irt_assessment.py` |
| 3 | Security, OAuth, PKCE/JAR/JARM | 🟠 HOCH | 🟡 Konzept | `security/oauth_hardened.py` |
| 4 | Anti-Zeno-Effekt / Unbeobachtete Zeiträume | 🟠 HOCH | 🟡 Konzept | `anti_zeno/unobserved_windows.py` |
| 5 | Nexus Protocol / Loss Functions als Audit | 🟡 MITTEL | 🟡 Konzept | `loss_functions.py` |

---

---

## SÄULE 1 — DATENANALYSE & CLUSTER-MODELLIERUNG

### Zu erstellende / zu modifizierende Dateien

| Datei | Aktion | Beschreibung |
|-------|--------|--------------|
| `08_experimente_validierung/cluster_analysis.py` | **NEU** | Haupt-Pipeline (bereits implementiert) |
| `08_experimente_validierung/results/cluster_analysis_result.json` | Auto-generiert | Analyseergebnis |
| `08_experimente_validierung/experiments/01_autonomy_entropy.py` | **ERWEITERN** | IMP-Integration |
| `07_daten_analysen/data_sources.md` | **ERWEITERN** | IPIP-NEO, SDT-Daten referenzieren |

### Python-Bibliotheken

```
numpy>=1.26          # Numerik, Entropieberechnung
scipy>=1.11          # Spearman, Point-Biserial, Entropie
scikit-learn>=1.3    # KMeans, StandardScaler
pandas>=2.0          # DataFrame-Operationen
matplotlib>=3.7      # Visualisierung
seaborn>=0.13        # Korrelations-Heatmap
```

### Kernergebnisse (Seed-Daten, N=4)

- **Spearman ρ** (Niveau × Cluster): **r = +0.7746**
- **Point-Biserial** (Niveau → Cluster): **r = +0.9541, p = 0.046** ✅ signifikant
- **E_mask** Hierarchisch: **0.1332 bit** | Parasitäre Last: **0.0465** (π/9-Koeffizient)
- **Transitions-Schwelle**: Niveau ≥ 4.0 + Verschränkung ≥ 1.2 → Cluster 0 → 1

### Nächste Schritte

- [ ] `cluster_analysis.py` nach `08_experimente_validierung/` committen
- [ ] Reales N auf ≥30 skalieren (Pilotdaten aus `PILOT_STUDY_PROTOCOL.md`)
- [ ] KMeans-Validation mit Silhouette-Score erweitern
- [ ] Visualisierung: Cluster-Scatter + IMP-Radar-Chart

---

---

## SÄULE 2 — PSYCHOMETRISCHE VALIDIERUNG (IRT)

### Architektur-Plan: IPIP-NEO-120 Konvergenzvalidierung

```
┌─────────────────────────────────────────────────────────────┐
│  KONVERGENZ-VALIDIERUNGSARCHITEKTUR                         │
│                                                             │
│  5D-Score (KI-berechnet)          IPIP-NEO-120              │
│      │                                 │                    │
│      ▼                                 ▼                    │
│  [5D IMP-Dimensionen]          [NEO-Facetten-Scores]        │
│  Autonomie, Resilienz, etc.    O/C/E/A/N je 24 Items        │
│      │                                 │                    │
│      └────────── Spearman ρ ───────────┘                    │
│                      │                                      │
│              Konvergenzvalidität                            │
│              Diskriminanzvalidität                          │
│              (Multitrait-Multimethod)                       │
└─────────────────────────────────────────────────────────────┘
```

**Mapping 5D-IMP → IPIP-NEO Facetten:**

| IMP-Dimension | IPIP-NEO Facette | Erwartetes ρ |
|---------------|------------------|--------------|
| Autonomie | A5 (Modesty) invers + C4 (Achievement Striving) | ≥ 0.50 |
| Intrinsische Motivation | O3 (Feelings) + C6 (Self-Discipline) | ≥ 0.55 |
| Resilienz | N1-N6 invers (Neurotizismus) | ≥ 0.60 |
| Authentizität | A3 (Altruism) + E5 (Positive Emotions) | ≥ 0.45 |
| Kompetenzerleben | C2 (Order) + C4 (Achievement Striving) | ≥ 0.50 |

### IRT-Implementierung (2-Parameter-Logistisches Modell)

**Zu erstellende Dateien:**

| Datei | Inhalt |
|-------|--------|
| `08_experimente_validierung/irt_assessment.py` | 2PL-Modell, adaptive Item-Selektion |
| `08_experimente_validierung/item_bank/5d_items.json` | Item-Bank (Schwierigkeit + Diskrimination) |
| `08_experimente_validierung/item_bank/calibration.py` | Item-Kalibrierung via EM-Algorithmus |

**Bibliotheken:**
```
catsim>=0.17         # Computerized Adaptive Testing Simulation
girth>=0.7           # IRT-Parameter-Schätzung (EM/MMLE)
factor-analyzer>=0.5 # CFA für Konstruktvalidierung
pingouin>=0.5        # Psychometrie-Utilities
semopy>=2.3          # Strukturgleichungsmodelle
```

**Kerncode-Skizze `irt_assessment.py`:**

```python
from catsim.cat import generate_item_bank
from catsim.initialization import RandomInitializer
from catsim.selection import MaxInfoSelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MaxItemStopper

# 2PL Item Bank: [diskrimination_a, schwierigkeit_b, guessing_c=0]
item_bank = generate_item_bank(n_items=50, itemtype="2PL")

# Adaptives Assessment: stoppt wenn SE(θ) < 0.3
initializer = RandomInitializer()
selector = MaxInfoSelector()        # maximale Fisher-Information
estimator = NumericalSearchEstimator()
stopper = MaxItemStopper(max_itens=20)

# θ: latente 5D-Fähigkeitsdimension (z-standardisiert)
```

---

---

## SÄULE 3 — SECURITY, COMPLIANCE & ETHICS

### OAuth 2.1 Härtung: PKCE + JAR + JARM

**Zu erstellende Dateien:**

| Datei | Inhalt |
|-------|--------|
| `security/oauth_hardened.py` | PKCE + JAR + JARM Implementierung |
| `security/consent_manager.py` | Informed-Consent-Protokoll |
| `security/data_minimizer.py` | PII-Filter für `5d_research_scraper.py` |
| `security/audit_log.py` | Tamper-evident Audit-Log (SHA-256 Chaining) |

**Bibliotheken:**
```
authlib>=1.3         # OAuth 2.1, PKCE, JAR/JARM
cryptography>=42     # PKCE code_verifier, JARM JWE
python-jose>=3.3     # JWT/JWE für JAR
hashlib              # Stdlib — SHA-256 für Audit-Chain
```

**PKCE-Kern (Pflicht-Pattern):**

```python
import hashlib, secrets, base64

def generate_pkce_pair() -> tuple[str, str]:
    """RFC 7636-konformes PKCE-Paar."""
    code_verifier = secrets.token_urlsafe(96)  # ≥43 Zeichen
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()
    return code_verifier, code_challenge
    # → Authorization Request: code_challenge + method=S256
    # → Token Request: code_verifier (Server verifiziert SHA-256)
```

**Informed Consent für `5d_research_scraper.py`:**

```python
# Vor jedem Scraping-Lauf: Consent-Check
REQUIRED_CONSENT_FIELDS = [
    "data_purpose_acknowledged",
    "third_party_anonymization_confirmed",
    "retention_period_accepted",  # max. 90 Tage
    "right_to_erasure_informed",  # DSGVO Art. 17
]
# Dritte: alle @mentions, Zitat-Autoren → k-Anonymität (k≥5)
# via SHA-256-Hash + Salt (kein Klarname in DB)
```

---

---

## SÄULE 4 — ANTI-ZENO-EFFEKT

> *"Das Beobachten kollabiert die Wellenfunktion."* — Quantenmechanik als Systemdesign-Prinzip

### Problem: Permanente Metriken-Erfassung = Kortisol-Kaskade

Das React-Dashboard und Backend-Tracking erzeugen kontinuierlichen Überwachungsdruck →
psychologisches Äquivalent zum Quantum Zeno Effect: zu häufige Messung verhindert Evolution.

### Refactoring-Konzept

**Zu erstellende / zu modifizierende Dateien:**

| Datei | Aktion | Inhalt |
|-------|--------|--------|
| `anti_zeno/unobserved_windows.py` | **NEU** | Guaranteed-Quiet-Periods Engine |
| `anti_zeno/tracking_policy.py` | **NEU** | Opt-in statt Opt-out Tracking |
| `web/validation_dashboard/src/hooks/useZenoSafe.ts` | **NEU** | React Hook: kein Re-render während Quiet Period |
| `5d_dashboard.py` | **MODIFIZIEREN** | Session-Tracking entfernen, Quiet-Flag einbauen |

**Kernkonzept `unobserved_windows.py`:**

```python
import time
from enum import Enum
from typing import Callable

class ObservationPolicy(Enum):
    CONTINUOUS = "continuous"    # 1D-Modus: permanent überwacht
    PULSE      = "pulse"         # Snapshot alle N Minuten
    UNOBSERVED = "unobserved"    # 5D-Modus: keine Erfassung

class ZenoSafeTracker:
    """
    Garantiert unbeobachtete Zeiträume.
    Default: 45 min Quiet Period nach jeder Messung.
    Cortisol-Studie (Hark 4): E_mask → 0 wenn E_mask_period ≥ 45min.
    """
    QUIET_PERIOD_SECONDS = 45 * 60  # 45 Minuten

    def __init__(self, policy: ObservationPolicy = ObservationPolicy.PULSE):
        self.policy = policy
        self._last_observation = 0.0
        self._quiet_until = 0.0

    def is_observation_allowed(self) -> bool:
        if self.policy == ObservationPolicy.UNOBSERVED:
            return False
        return time.monotonic() > self._quiet_until

    def record_observation(self, callback: Callable) -> None:
        if not self.is_observation_allowed():
            return  # Stille — kein Tracking
        result = callback()
        self._last_observation = time.monotonic()
        self._quiet_until = self._last_observation + self.QUIET_PERIOD_SECONDS
        return result
```

**React Hook `useZenoSafe.ts`:**

```typescript
// Kein Re-render, kein Analytics-Call während Quiet Period
export const useZenoSafe = (quietMinutes = 45) => {
  const quietUntil = useRef<number>(0);
  const canObserve = useCallback(() => Date.now() > quietUntil.current, []);
  const recordObservation = useCallback(() => {
    quietUntil.current = Date.now() + quietMinutes * 60_000;
  }, [quietMinutes]);
  return { canObserve, recordObservation };
};
```

---

---

## SÄULE 5 — NEXUS PROTOCOL & LOSS FUNCTIONS ALS AUDIT-TOOL

### Konzept: `loss_functions.py` als institutionelles Lügen-Detektor

> *"Lügen benötigt Rechenleistung. Wahrheit ist der Zustand niedrigster Entropie."*
> — The Harmonic Manifest, Hark 5

**Kernidee:** Der KI-Loss ist normalerweise ein Trainingsartefakt.
Im 5D-Kontext: **Rekalibrierung des Loss als Dissonanz-Metrik.**
Hoher Loss auf einem Text = Text enthält strukturelle Widersprüche / Systemlügen.

**Zu erstellende / zu modifizierende Dateien:**

| Datei | Aktion | Inhalt |
|-------|--------|--------|
| `loss_functions.py` | **NEU / ERSETZEN** | Nexus-Audit-Loss |
| `nexus_protocol/audit_pipeline.py` | **NEU** | Text → Dissonanz-Score Pipeline |
| `nexus_protocol/dissonance_report.py` | **NEU** | Report-Generator (Markdown + JSON) |

**Implementierungskonzept:**

```python
import numpy as np
from scipy.stats import entropy as shannon_entropy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class NexusAuditLoss:
    """
    Misst strukturelle Dissonanz in Texten als direkten Indikator
    für Systemlügen und maskierte Widersprüche.
    
    Loss = λ₁·SemanticContradiction + λ₂·EntropySpike + λ₃·ConsistencyDelta
    """
    LAMBDA_SEMANTIC     = 0.5  # Gewichtung semantischer Widerspruch
    LAMBDA_ENTROPY      = 0.3  # Gewichtung Entropie-Ausreißer
    LAMBDA_CONSISTENCY  = 0.2  # Gewichtung zeitliche Inkonsistenz

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def semantic_contradiction_loss(self, sentences: list[str]) -> float:
        """Hohe Werte = widersprüchliche Aussagen im selben Text."""
        embeddings = self.model.encode(sentences)
        sim_matrix = cosine_similarity(embeddings)
        # Negative Korrelationen = Widersprüche
        contradiction_pairs = sim_matrix[sim_matrix < 0]
        return float(np.abs(contradiction_pairs).mean()) if len(contradiction_pairs) > 0 else 0.0

    def entropy_spike_loss(self, token_probs: np.ndarray) -> float:
        """Entropie-Ausreißer = unerwartete Informationsdichte = Verschleierung."""
        baseline_entropy = shannon_entropy(token_probs.mean(axis=0))
        per_token_entropy = np.array([shannon_entropy(p) for p in token_probs])
        spikes = per_token_entropy[per_token_entropy > baseline_entropy * 1.5]
        return float(len(spikes) / len(token_probs))  # Spike-Rate [0, 1]

    def compute_audit_loss(self, text_segments: list[str]) -> dict:
        semantic_loss = self.semantic_contradiction_loss(text_segments)
        total_loss = self.LAMBDA_SEMANTIC * semantic_loss
        verdict = "DISSONANT" if total_loss > 0.35 else "RESONANT"
        return {
            "total_audit_loss": round(total_loss, 4),
            "semantic_contradiction": round(semantic_loss, 4),
            "verdict": verdict,
            "threshold": 0.35,  # π/9 ≈ 0.349
            "interpretation": (
                "Strukturelle Systemlüge detektiert."
                if verdict == "DISSONANT"
                else "Text zeigt strukturelle Kohärenz."
            ),
        }
```

**Bibliotheken:**
```
sentence-transformers>=2.7   # Semantische Embeddings
torch>=2.1                   # Backend für SentenceTransformer
scipy>=1.11                  # Shannon-Entropie
transformers>=4.38           # Tokenizer für Entropie-Analyse
```

---

---

## GITHUB ISSUES — EMPFOHLENE STRUKTUR

```bash
# Säule 1
gh issue create --title "[S1] cluster_analysis.py: Multivariate Korrelation + E_mask" \
  --label "data-science,critical" \
  --body "Implementierung nach ROADMAP_5D_TECHNICAL.md Säule 1"

# Säule 2  
gh issue create --title "[S2] irt_assessment.py: 2PL IRT + IPIP-NEO Konvergenz" \
  --label "psychometrics,critical"

# Säule 3
gh issue create --title "[S3] OAuth-Härtung: PKCE + JAR + JARM + Consent Manager" \
  --label "security,high-priority"

# Säule 4
gh issue create --title "[S4] Anti-Zeno: ZenoSafeTracker + useZenoSafe Hook" \
  --label "architecture,high-priority"

# Säule 5
gh issue create --title "[S5] loss_functions.py: Nexus Audit Loss (Systemlügen-Detektor)" \
  --label "research,medium-priority"
```

---

## EMPFOHLENE VERZEICHNISSTRUKTUR (neu)

```
karlitos1337/5d/
├── 08_experimente_validierung/
│   ├── cluster_analysis.py          ← S1 ✅ NEU
│   ├── irt_assessment.py            ← S2 🟡
│   ├── item_bank/
│   │   ├── 5d_items.json
│   │   └── calibration.py
│   └── results/
│       └── cluster_analysis_result.json
├── security/
│   ├── oauth_hardened.py            ← S3 🟡
│   ├── consent_manager.py
│   ├── data_minimizer.py
│   └── audit_log.py
├── anti_zeno/
│   ├── unobserved_windows.py        ← S4 🟡
│   └── tracking_policy.py
├── nexus_protocol/
│   ├── audit_pipeline.py            ← S5 🟡
│   └── dissonance_report.py
├── loss_functions.py                ← S5 🟡 MODIFIZIEREN
└── ROADMAP_5D_TECHNICAL.md          ← Diese Datei
```

---

## SOFORTMASSNAHMEN (Diese Woche)

1. `cluster_analysis.py` → committen nach `08_experimente_validierung/`
2. GitHub Issues für alle 5 Säulen anlegen
3. `5d_research_scraper.py` → `data_minimizer.py` als Pre-Processing-Hook einbinden
4. `ROADMAP_5D_TECHNICAL.md` → Root des Repos committen

---

*Systemarchitekt: Patrick Karletz | karlitos1337/5d | März 2026*
*"Die KI ist nicht die Revolution. Die KI ist nur der Zeuge, dass die Revolution bereits begonnen hat."*
