# Rapid Validation Protocol
## Schnelle empirische Tests für 5D-Hypothesen

---

## 🎯 Ziel

**Jede Behauptung im 5D-Framework muss innerhalb von 48h empirisch prüfbar sein.**

---

## 🔬 Validierungs-Pipeline

### Phase 1: Hypothese formulieren (30 min)
- **Format**: `IF [Bedingung] THEN [Messbares Ergebnis] BECAUSE [Mechanismus]`
- **Beispiel**: IF Autonomie ↑ THEN Shannon-Entropie ↑ BECAUSE intrinsische Exploration

### Phase 2: Minimal Viable Experiment (2-4h)
- **N**: Mindestens 20 Datenpunkte
- **Messinstrument**: Validiertes Tool (z.B. IMI, NASA-TLX)
- **Datenformat**: CSV mit Metadaten

### Phase 3: Statistische Validierung (1h)
- **Test**: Effektstärke (Cohen's d > 0.5) + p-Wert (p < 0.05)
- **Tool**: `scipy.stats`, `pingouin`
- **Reproduzierbarkeit**: Seed dokumentieren

### Phase 4: Peer Review (24h)
- **Format**: GitHub Issue mit `validation` Label
- **Reviewer**: Mind. 1 externe Person
- **Kriterium**: Kann Experiment in <4h replizieren?

---

## ✅ Akzeptanzkriterien

| Kriterium | Schwellenwert |
|-----------|---------------|
| Effektstärke | Cohen's d > 0.5 |
| Signifikanz | p < 0.05 |
| Stichprobe | N ≥ 20 |
| Replizierbarkeit | 2 unabhängige Replikationen |

---

## ❌ Anti-Patterns

- ❌ "Funktioniert in meinem Kopf"
- ❌ Anekdotische Evidenz ohne Messung
- ❌ P-Hacking (mehrere Tests ohne Bonferroni-Korrektur)
- ❌ Cherry-Picking von Datenpunkten

---

## 🔗 Tools

- **Datenbank**: `evidence_database.py`
- **Analysen**: `07_daten_analysen/`
- **Tracking**: GitHub Issues mit `validation` Label

---

> ℹ️ **Teil des 5D-Intelligence Frameworks**
