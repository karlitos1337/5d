# Mapping Resonanz → IMP (Template)

Dieses Dokument dient als Vorlage, um Begriffe aus den externen Repositories (`resonance-formula-5d-intelligence`, `universal-system-genesis-5d`) sauber auf die 5D-IMP Dimensionen abzubilden.

## Ziel
Externe Konzepte (Resonanz, Frequenz, Emergenz etc.) sollen die bestehenden Scores ergänzen – niemals direkt ersetzen. Nutzung über Prefix-Felder in `5d_solutions_merged.json` (`external`).

## Vorgehen
1. Extraktion aus Submodules per `python merge_external_solutions.py` (erzeugt `solutions_external.json` + `5d_solutions_merged.json`).
2. Identifikation relevanter Resonanz-/Genesis-Begriffe.
3. Manuelles oder regelbasiertes Mapping -> numerischer Einflussfaktor (0–1 oder Gewichtung).
4. Aggregation: IMP Roh-Scores × (1 + gewichtete Resonanz-Faktoren) (nicht > 1.2 ohne Begründung).

## Beispiel-Mapping Tabelle
| Externer Begriff | Kategorie         | IMP-Dimension | Gewicht | Begründung kurz |
|------------------|------------------|---------------|---------|-----------------|
| Resonanz         | Resonanz/Bindung | Authentizität | 0.05    | Stärkt Kongruenz |
| Kohärenz         | Systemqualität   | Resilienz     | 0.04    | Stabilität       |
| Emergenz         | Systemdynamik    | Partizipation | 0.05    | Kooperationsfluss|
| Selbstorganisation| Systemprozess   | Autonomie     | 0.06    | Eigensteuerung   |
| Frequenz         | Muster/Tempo     | Motivation    | 0.03    | Aktivierungsgrad |

## Platz für Mapping (ausfüllen)
```
# mapping_v1
resonanz -> Au:0.05
kohärenz -> R:0.04
...
```

## Validierung
- Max kumulative Zusatzverstärkung < +0.20 (Deckel, um Overfitting zu vermeiden).
- Bei neuen Begriffen zuerst in Tabelle aufnehmen, dann faktorisiert nutzen.

## Nicht mischen
- Keine direkten numerischen Überschreibungen der bestehenden `A-Score`, `IM-Score`, etc. Felder.
- Zusatzwerte nur als Multiplikativ-Faktor oder additive Annotation.

## Nächste Schritte
- (Optional) Python-Skript `apply_resonance_mapping.py` erstellen, das diese Datei parst und neue Felder `imp_adjusted` generiert.

---
Template v1.0 – Bitte bei Erstbefüllung Versionskommentar hinzufügen.
