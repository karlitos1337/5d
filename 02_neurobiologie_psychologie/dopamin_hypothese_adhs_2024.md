# Die Dopamin-Hypothese bei ADHS: 40 Jahre Evidenz (2024 Review)

**Thema:** T1 | Neurobiologie + ADHS + Intrinsische Motivation
**Evidenzlabel:** ✅ Fakt (peer-reviewed, umfassender Review)
**Risikorating:** 🟢 GESICHERT
**Kurations-Datum:** 2026-03-23
**5D-Relevanz:** IMP-Formel (Variable IM als dynamischer Wert)

---

## Kernquelle

**MacDonald, H. J., Haavik, J., Szigetvari, P. D., & Kleppe, R.** (2024). The dopamine hypothesis for ADHD: An evaluation of evidence accumulated from human studies and animal models. *Frontiers in Psychiatry, 15*, 1492126.

- **DOI:** [10.3389/fpsyt.2024.1492126](https://doi.org/10.3389/fpsyt.2024.1492126)
- **Volltext:** [PMC11604610](https://pmc.ncbi.nlm.nih.gov/articles/PMC11604610/)

---

## Kernaussagen

### 1. Kein einfaches Defizit
Die einfache Erzählung "ADHS = zu wenig Dopamin" hält der Evidenz nicht stand. Die Datenlage zeigt:

- **Striatales System:** Veränderte Dopamin-Transporter-Dichte (DAT), aber nicht konsistent erhöht oder erniedrigt
- **Kortikales System:** Veränderte Signalverarbeitung im präfrontalen Kortex, moduliert durch Kontextfaktoren
- **Genetische Befunde:** Polymorphismen in DRD4, DRD5, DAT1 — aber mit kleinen Effektgrößen und hoher Variabilität

### 2. Signalmuster statt Mangel
Die aktuelle Evidenz spricht für ein **kontextabhängiges Signalstörungs-Muster**:

| Kontext | Dopamin-Reaktion bei ADHS | Konsequenz |
|---------|---------------------------|------------|
| Neue, interessante Aufgabe | Normal bis erhöht (Hyperfokus) | Hohe Leistung, hohe IM |
| Repetitive, langweilige Aufgabe | Stark reduziert | Aufmerksamkeitsverlust, niedrige IM |
| Sofortige Belohnung | Überschießend | Impulsivität |
| Verzögerte Belohnung | Abgeschwächt | Delay Aversion |

### 3. Methylphenidat-Wirkung
Methylphenidat (Ritalin) erhöht tonisches Dopamin und hemmt gleichzeitig phasische Dopamin-Freisetzung. Das bedeutet: Das Medikament glättet das Signalmuster, statt einfach "mehr Dopamin" zu liefern. Die Wirkung ist kontextabhängig und bei manchen Patient:innen paradox.

### 4. Tiermodelle
Die Spontaneously Hypertensive Rat (SHR) als ADHS-Modell zeigt: Veränderte Dopamin-Signalverarbeitung führt zu veränderter Reaktion auf Verstärkung — nicht zu grundsätzlich geringerer Motivation. Das unterstützt die SDT-Perspektive (siehe `adhs_sdt_motivation.md`).

---

## 5D-System-Verknüpfungen

### IMP-Formel Konsequenz
Wenn Dopamin ein kontextabhängiges Signalmuster ist (kein Defizit), dann muss die Variable **IM** in der IMP-Formel dynamisch modelliert werden:

```
IM_alt = 1 - (depression_rate / 100)       # statisch, populationsbasiert
IM_neu = f(Kontext, Interesse, Belohnungsverzögerung)  # dynamisch, individuell
```

Das hat direkte Konsequenzen für die Operationalisierung der IMP-Formel auf individueller Ebene (vs. Länder-Aggregat).

### Interdisziplinäre Links
- **T1↔T8:** Formel-Revision notwendig — IM als Funktion, nicht als Konstante
- **T1↔T4:** Kontextabhängigkeit von Dopamin bestätigt, dass Lernumgebungen (nicht Lernende) das Problem sind
- **T1↔T3:** Dopamin-Signalmuster sind emergente Systemeigenschaften, nicht deterministische Defizite

---

## Ergänzende Quellen

- **Tripp, G., & Wickens, J. R.** (2009). Neurobiology of ADHD. *Neuropharmacology, 57*, 579–589.
- **Sagvolden, T., et al.** (2005). A dynamic developmental theory of ADHD. *Behavioral and Brain Sciences, 28*, 397–419.
- **Del Campo, N., et al.** (2013). PET study of nigro-striatal dopaminergic mechanisms underlying attention. *Brain, 136*(11), 3252–3270. DOI: [10.1093/brain/awt263](https://doi.org/10.1093/brain/awt263)

---

**Querverweise im Repo:**
- `02_neurobiologie_psychologie/adhs_sdt_motivation.md`
- `FORMEL_UPDATE_v2.md`
- `docs/CLAIMS_EVIDENCE_MATRIX.md`
