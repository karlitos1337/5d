# SoSci Survey — Direct Import Guide: 5D-IMP-Studie

**Studie:** 5-Dimensionen Integrative Measures of Potential (5D-IMP)  
**Erstellt:** 2026-04-02  
**Zweck:** Vollständige Anleitung zum manuellen Aufbau des Fragebogens in SoSci Survey über den Direct-Import-Mechanismus.

---

## Inhaltsverzeichnis

1. [Allgemeine Hinweise zu SoSci Survey](#1-allgemeine-hinweise)
2. [Fragebogenstruktur (Seitenplan)](#2-seitenplan)
3. [Rubrik 1 — IMP Autonomie](#3-rubrik-1--imp-autonomie)
4. [Rubrik 2 — IMP Kompetenz](#4-rubrik-2--imp-kompetenz)
5. [Rubrik 3 — IMP Resonanz](#5-rubrik-3--imp-resonanz)
6. [Rubrik 4 — IMP Partizipation](#6-rubrik-4--imp-partizipation)
7. [Rubrik 5 — IMP Authentizität](#7-rubrik-5--imp-authentizit%C3%A4t)
8. [Attention Check](#8-attention-check)
9. [SWLS — Lebenszufriedenheit](#9-swls--lebenszufriedenheit)
10. [Demographische Daten](#10-demographische-daten)
11. [Variable-Mapping-Tabelle](#11-variable-mapping-tabelle)
12. [Reverse-Coding-Hinweise](#12-reverse-coding-hinweise)

---

## 1. Allgemeine Hinweise

### Was ist der Direct Import in SoSci Survey?

SoSci Survey bietet beim Anlegen einer neuen Frage die Funktion **„Items importieren"** (auch: Direct Import). Damit können Items und Antwortoptionen per Copy-Paste eingefügt werden, ohne sie einzeln eintippen zu müssen.

### Syntax-Regeln für den Direct Import

| Element | Syntax | Beispiel |
|---|---|---|
| Item-Text | Einfache Zeile | `Ich bestimme selbst meine Ziele.` |
| Variablenname | In eckigen Klammern hinter dem Text | `Ich bestimme selbst meine Ziele. [AUT1]` |
| Antwortoptionen | Zahl + `=` + Text | `1=Trifft gar nicht zu` |
| Kommentare | Zeilen mit `#` am Anfang | `# Dies ist ein Kommentar` |

### ⚠️ Wichtige Regeln für Variablennamen

- Variablennamen dürfen **NICHT** dem Muster `[Buchstabe][Zahl][Zahl]` entsprechen (z. B. `A1`, `B2`, `K12` sind **verboten**)
- Erlaubt: `AUT1`, `KOM1`, `SWLS1`, `ALTER`, `GESCHL` usw.
- Maximal **8 Zeichen**, nur Buchstaben und Ziffern, kein Leerzeichen
- Variablennamen sind **eindeutig** im gesamten Projekt (nicht doppelt vergeben)

### Wo findet man den Direct Import?

1. In SoSci Survey: **Fragebogen → Fragen → Neue Frage**
2. Fragetyp auswählen (z. B. „Skala")
3. Auf den Reiter **„Items"** klicken
4. Button **„Importieren"** (oder „Direktimport") klicken
5. Text einfügen und bestätigen

---

## 2. Seitenplan

Empfohlene Fragebogen-Struktur (eine Rubrik pro Seite):

| Seite | Inhalt | Fragetyp | Fragen-ID |
|---|---|---|---|
| 1 | Begrüßung / Einleitung | Statischer Text | — |
| 2 | IMP Autonomie (5 Items) | Skala 1–5 | IA |
| 3 | IMP Kompetenz (5 Items) | Skala 1–5 | IK |
| 4 | IMP Resonanz (5 Items) | Skala 1–5 | IR |
| 5 | IMP Partizipation (5 Items) | Skala 1–5 | IP |
| 6 | IMP Authentizität (5 Items) | Skala 1–5 | IU |
| 7 | Attention Check (1 Item) | Skala 1–5 | AC |
| 8 | SWLS Lebenszufriedenheit (5 Items) | Skala 1–7 | SW |
| 9 | Demographische Daten | Diverse | DA / DG / DB / DJ |
| 10 | Abschluss / Danke | Statischer Text | — |

> **Tipp:** Der Attention Check (Seite 7) kann auch zwischen zwei IMP-Blöcken platziert werden, um Careless Responding früher abzufangen.

---

## 3. Rubrik 1 — IMP Autonomie

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala" (auch: „Bewertungsskala" / Rating Scale)
3. **Fragen-ID setzen:** `IA` (oder vom System vergeben lassen, z. B. `IA00`)
4. **Fragetitel eingeben:** `IMP Autonomie`
5. **Fragetext eingeben:**
   > Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft.
6. **Reiter „Skalenpunkte":** Antwortoptionen eingeben (siehe unten)
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Ich bestimme weitgehend selbst, wie ich meine Ziele verfolge. [AUT1]
Externe Regeln und Sanktionen bestimmen meinen Alltag stark. [AUT2]
Ich fühle mich durch Bewertungssysteme (Noten/KPIs) eingeschränkt. [AUT3]
Meine Motivation kommt hauptsächlich von innen, nicht von außen. [AUT4]
Ich habe Angst vor Konsequenzen bei Abweichung von Vorgaben. [AUT5]
```

### Hinweise

- **Reverse-Coding:** AUT2, AUT3, AUT5 sind negativ formuliert → Umkehrcodierung erforderlich (6 − x bei 5er-Skala)
- **SoSci interne Variablen:** Nach dem Import heißen die Variablen intern `IA01`, `IA02`, `IA03`, `IA04`, `IA05` (Fragekennung + laufende Nummer) — die Custom-Namen `AUT1`–`AUT5` sind zusätzliche Labels
- **Skalenpunkte:** Sicherstellen, dass genau 5 Punkte definiert sind (1–5)

---

## 4. Rubrik 2 — IMP Kompetenz

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala"
3. **Fragen-ID setzen:** `IK`
4. **Fragetitel eingeben:** `IMP Kompetenz`
5. **Fragetext eingeben:**
   > Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft.
6. **Antwortoptionen:** Gleiche Skala wie Rubrik 1 (1–5, siehe oben) — oder Skala aus vorheriger Frage kopieren
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Ich kann meine Impulse gut regulieren und fokussieren. [KOM1]
Chronischer Stress beeinträchtigt meine Konzentration stark. [KOM2]
Mein Körper fühlt sich energiegeladen und ausgeglichen an. [KOM3]
Ich erhole mich schnell von Rückschlägen. [KOM4]
Ich spüre oft Erschöpfung durch innere Konflikte. [KOM5]
```

### Hinweise

- **Reverse-Coding:** KOM2, KOM5 sind negativ formuliert → Umkehrcodierung erforderlich (6 − x)
- **SoSci interne Variablen:** `IK01`–`IK05`

---

## 5. Rubrik 3 — IMP Resonanz

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala"
3. **Fragen-ID setzen:** `IR`
4. **Fragetitel eingeben:** `IMP Resonanz`
5. **Fragetext eingeben:**
   > Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft.
6. **Antwortoptionen:** Likert 1–5 (wie oben)
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Ich kann mich bewusst in andere Perspektiven versetzen. [RES1]
Ich bin oft in festen Rollen/Überzeugungen gefangen. [RES2]
Ich reflektiere regelmäßig meine eigenen Narrative. [RES3]
Konflikte löse ich durch Perspektivenwechsel. [RES4]
Emotionale Reaktionen überlagern oft mein rationales Denken. [RES5]
```

### Hinweise

- **Reverse-Coding:** RES2, RES5 sind negativ formuliert → Umkehrcodierung erforderlich (6 − x)
- **SoSci interne Variablen:** `IR01`–`IR05`

---

## 6. Rubrik 4 — IMP Partizipation

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala"
3. **Fragen-ID setzen:** `IP`
4. **Fragetitel eingeben:** `IMP Partizipation`
5. **Fragetext eingeben:**
   > Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft.
6. **Antwortoptionen:** Likert 1–5 (wie oben)
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Ich kooperiere horizontal mit anderen ohne Hierarchie. [PAR1]
Mein Netzwerk besteht aus vertrauensvollen, authentischen Beziehungen. [PAR2]
Ideen entstehen emergent aus Gruppeninteraktionen. [PAR3]
Zentrale Entscheidungen blockieren oft unseren Fortschritt. [PAR4]
Ich fühle mich isoliert von potenziellen Verbündeten. [PAR5]
```

### Hinweise

- **Reverse-Coding:** PAR4, PAR5 sind negativ formuliert → Umkehrcodierung erforderlich (6 − x)
- **SoSci interne Variablen:** `IP01`–`IP05`

---

## 7. Rubrik 5 — IMP Authentizität

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala"
3. **Fragen-ID setzen:** `IU` (Authentizität = „Uth", da `IA` schon vergeben)
4. **Fragetitel eingeben:** `IMP Authentizität`
5. **Fragetext eingeben:**
   > Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft.
6. **Antwortoptionen:** Likert 1–5 (wie oben)
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Meine Handlungen fühlen sich kongruent mit meiner Identität an. [AUTH1]
Ich erlebe oft Flow-Zustände ohne innere Reibung. [AUTH2]
Mein Leben hat eine klare, innere Sinnstiftung. [AUTH3]
Ich maskiere Teile meiner Persönlichkeit, um zu passen. [AUTH4]
Ich kann mit meinen Entscheidungen "selbst schlafen". [AUTH5]
```

### Hinweise

- **Reverse-Coding:** AUTH4 ist negativ formuliert → Umkehrcodierung erforderlich (6 − x)
- **SoSci interne Variablen:** `IU01`–`IU05`

---

## 8. Attention Check

### Zweck

Der Attention Check filtert Teilnehmer heraus, die den Fragebogen nicht aufmerksam ausfüllen. Die korrekte Antwort ist **Wert 3 (Teils/teils)**.

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala" (gleicher Typ wie IMP-Fragen, damit nicht auffällt)
3. **Fragen-ID setzen:** `AC`
4. **Fragetitel eingeben:** `Attention Check` (wird Teilnehmern nicht angezeigt)
5. **Fragetext eingeben:**
   > Bitte lesen Sie die folgende Aussage sorgfältig.
6. **Antwortoptionen:** Gleiche Likert 1–5 Skala wie bei IMP-Fragen
7. **Reiter „Items" → Importieren:** Item einfügen (siehe unten)
8. **Speichern**
9. **Auswertung:** In der Datenanalyse alle Fälle ausschließen, bei denen `AC01` ≠ 3

### Antwortoptionen (Likert 1–5) — zum Kopieren

```
1=Trifft gar nicht zu
2=Trifft eher nicht zu
3=Teils/teils
4=Trifft eher zu
5=Trifft voll zu
```

### Items — Direct Import Text (zum Kopieren)

```
Dies ist eine Kontrollfrage. Bitte wählen Sie "Teils/teils" (3). [ATTN1]
```

### Hinweise

- **Korrekter Wert:** 3 (Teils/teils)
- **Ausschlussregel in R:** `filter(ATTN1 == 3)` oder `subset(data, AC01 == 3)`
- **Positionierung:** Entweder nach Rubrik 5 (IMP Authentizität) oder eingebettet zwischen zwei IMP-Blöcken (z. B. zwischen Kompetenz und Resonanz)

---

## 9. SWLS — Lebenszufriedenheit

### Schritt-für-Schritt-Anleitung

1. **Neue Frage anlegen:** Fragebogen → Fragen → Neue Frage anlegen
2. **Fragetyp wählen:** „Skala"
3. **Fragen-ID setzen:** `SW`
4. **Fragetitel eingeben:** `SWLS Lebenszufriedenheit`
5. **Fragetext eingeben:**
   > Die folgenden fünf Aussagen beziehen sich auf Ihre allgemeine Lebenszufriedenheit. Bitte geben Sie an, inwieweit Sie jeder Aussage zustimmen.
6. **Reiter „Skalenpunkte":** 7 Antwortoptionen eingeben (siehe unten)
7. **Reiter „Items" → Importieren:** Items einfügen (siehe unten)
8. **Speichern**

> ⚠️ **Wichtig:** Die SWLS verwendet eine **7-Punkte-Skala** — nicht die 5-Punkte-Skala der IMP-Items. Neue Skalendefinition nötig!

### Antwortoptionen (Likert 1–7) — zum Kopieren

```
1=Stimme überhaupt nicht zu
2=Stimme nicht zu
3=Stimme eher nicht zu
4=Weder noch
5=Stimme eher zu
6=Stimme zu
7=Stimme voll und ganz zu
```

### Items — Direct Import Text (zum Kopieren)

```
In den meisten Bereichen entspricht mein Leben meinen Idealvorstellungen. [SWLS1]
Meine Lebensbedingungen sind ausgezeichnet. [SWLS2]
Ich bin mit meinem Leben zufrieden. [SWLS3]
Bisher habe ich die wesentlichen Dinge erreicht, die ich mir im Leben wünsche. [SWLS4]
Wenn ich mein Leben noch einmal leben könnte, würde ich kaum etwas ändern. [SWLS5]
```

### Hinweise

- **Keine Reverse-Items** in der SWLS — alle 5 Items sind positiv formuliert
- **SWLS-Gesamtscore:** Summe aller 5 Items (Range: 5–35)
  - 5–9: Extrem unzufrieden
  - 20–24: Leicht zufrieden
  - 31–35: Extrem zufrieden
- **SoSci interne Variablen:** `SW01`–`SW05`
- **Original-Quelle:** Diener, E., Emmons, R. A., Larsen, R. J., & Griffin, S. (1985). The satisfaction with life scale. *Journal of Personality Assessment, 49*(1), 71–75.

---

## 10. Demographische Daten

### Allgemeine Anleitung

Die demographischen Fragen werden in einer eigenen Rubrik/Seite am Ende des Fragebogens platziert. Jede Frage wird separat angelegt.

---

### 10.1 Alter — Offene Zahleneingabe

**Schritt-für-Schritt:**
1. **Neue Frage anlegen** → Fragetyp: **„Offene Eingabe"** oder **„Zahl"**
2. **Fragen-ID:** `DA`
3. **Fragetext:** `Wie alt sind Sie?`
4. **Eingabeformat:** Zahl (Ganzzahl), Wertebereich optional einschränken (z. B. 16–99)
5. **Variable:** `ALTER`

**Direct Import (falls Fragetyp „Zahl" mit Items):**

```
Ihr Alter (in Jahren): [ALTER]
```

**Hinweise:**
- Kein Direct Import über Antwortoptionen nötig — offenes Textfeld
- In R: `as.numeric(ALTER)` sicherstellen

---

### 10.2 Geschlecht — Single Choice / Dropdown

**Schritt-für-Schritt:**
1. **Neue Frage anlegen** → Fragetyp: **„Einfachnennung"** oder **„Auswahlliste (Dropdown)"**
2. **Fragen-ID:** `DG`
3. **Fragetext:** `Was ist Ihr Geschlecht?`
4. **Reiter „Antwortoptionen" → Importieren:** Antwortoptionen einfügen
5. **Variable:** `GESCHL`

**Antwortoptionen — Direct Import (zum Kopieren):**

```
1=Männlich
2=Weiblich
3=Non-binär
4=Keine Angabe
```

**Hinweise:**
- Fragetyp „Einfachnennung" zeigt Radiobuttons, „Auswahlliste" zeigt Dropdown
- Für Dropdown: Fragetyp „Auswahlliste" wählen, dann Antworten importieren
- Variable `GESCHL` kann als Factor in R kodiert werden: `factor(GESCHL, labels=c("Männlich","Weiblich","Non-binär","Keine Angabe"))`

---

### 10.3 Bildungsniveau — Dropdown

**Schritt-für-Schritt:**
1. **Neue Frage anlegen** → Fragetyp: **„Auswahlliste (Dropdown)"**
2. **Fragen-ID:** `DB`
3. **Fragetext:** `Was ist Ihr höchster Bildungsabschluss?`
4. **Reiter „Antwortoptionen" → Importieren:** Antwortoptionen einfügen
5. **Variable:** `BILDUNG`

**Antwortoptionen — Direct Import (zum Kopieren):**

```
1=Kein Abschluss
2=Hauptschulabschluss
3=Mittlere Reife
4=Fachabitur
5=Abitur
6=Berufsausbildung
7=Bachelor
8=Master
9=Promotion
```

**Hinweise:**
- Ordinalskaliert — in R als geordneter Factor anlegen: `factor(BILDUNG, ordered=TRUE)`

---

### 10.4 Berufliche Situation — Dropdown

**Schritt-für-Schritt:**
1. **Neue Frage anlegen** → Fragetyp: **„Auswahlliste (Dropdown)"**
2. **Fragen-ID:** `DJ`
3. **Fragetext:** `Was beschreibt Ihre aktuelle berufliche Situation am besten?`
4. **Reiter „Antwortoptionen" → Importieren:** Antwortoptionen einfügen
5. **Variable:** `BERUF`

**Antwortoptionen — Direct Import (zum Kopieren):**

```
1=Vollzeit beschäftigt
2=Teilzeit beschäftigt
3=Selbständig
4=Student:in
5=Arbeitssuchend
6=Rente/Pension
7=Sonstiges
```

**Hinweise:**
- Nominalskala — in R als ungeordneter Factor anlegen
- Kategorie „Sonstiges" ggf. mit offener Freitextergänzung kombinieren (separate Folgefrage)

---

## 11. Variable-Mapping-Tabelle

Diese Tabelle zeigt die Zuordnung zwischen SoSci Survey internen Variablennamen, den Direct-Import-Variablenlabels und den empfohlenen R-Code-Variablen. Reverse-kodierte Items sind markiert.

### IMP-Skala — Vollständiges Mapping

| SoSci Intern | Direct-Import Label | Dimension | Item-Text (Kurzform) | Reverse? | R-Variable (Roh) | R-Variable (Rekodiert) |
|---|---|---|---|---|---|---|
| `IA01` | `AUT1` | Autonomie | Ich bestimme selbst meine Ziele. | Nein | `AUT1_roh` | `AUT1` |
| `IA02` | `AUT2` | Autonomie | Externe Regeln bestimmen meinen Alltag. | **Ja** | `AUT2_roh` | `AUT2` (= 6−roh) |
| `IA03` | `AUT3` | Autonomie | Ich fühle mich durch Bewertungssysteme eingeschränkt. | **Ja** | `AUT3_roh` | `AUT3` (= 6−roh) |
| `IA04` | `AUT4` | Autonomie | Meine Motivation kommt von innen. | Nein | `AUT4_roh` | `AUT4` |
| `IA05` | `AUT5` | Autonomie | Ich habe Angst vor Konsequenzen. | **Ja** | `AUT5_roh` | `AUT5` (= 6−roh) |
| `IK01` | `KOM1` | Kompetenz | Ich kann meine Impulse regulieren. | Nein | `KOM1_roh` | `KOM1` |
| `IK02` | `KOM2` | Kompetenz | Chronischer Stress beeinträchtigt mich. | **Ja** | `KOM2_roh` | `KOM2` (= 6−roh) |
| `IK03` | `KOM3` | Kompetenz | Mein Körper fühlt sich ausgeglichen an. | Nein | `KOM3_roh` | `KOM3` |
| `IK04` | `KOM4` | Kompetenz | Ich erhole mich schnell von Rückschlägen. | Nein | `KOM4_roh` | `KOM4` |
| `IK05` | `KOM5` | Kompetenz | Ich spüre oft Erschöpfung. | **Ja** | `KOM5_roh` | `KOM5` (= 6−roh) |
| `IR01` | `RES1` | Resonanz | Ich versetze mich in andere Perspektiven. | Nein | `RES1_roh` | `RES1` |
| `IR02` | `RES2` | Resonanz | Ich bin in festen Rollen gefangen. | **Ja** | `RES2_roh` | `RES2` (= 6−roh) |
| `IR03` | `RES3` | Resonanz | Ich reflektiere meine Narrative. | Nein | `RES3_roh` | `RES3` |
| `IR04` | `RES4` | Resonanz | Konflikte löse ich durch Perspektivenwechsel. | Nein | `RES4_roh` | `RES4` |
| `IR05` | `RES5` | Resonanz | Emotionale Reaktionen überlagern mein Denken. | **Ja** | `RES5_roh` | `RES5` (= 6−roh) |
| `IP01` | `PAR1` | Partizipation | Ich kooperiere horizontal. | Nein | `PAR1_roh` | `PAR1` |
| `IP02` | `PAR2` | Partizipation | Mein Netzwerk ist vertrauensvoll. | Nein | `PAR2_roh` | `PAR2` |
| `IP03` | `PAR3` | Partizipation | Ideen entstehen emergent. | Nein | `PAR3_roh` | `PAR3` |
| `IP04` | `PAR4` | Partizipation | Zentrale Entscheidungen blockieren uns. | **Ja** | `PAR4_roh` | `PAR4` (= 6−roh) |
| `IP05` | `PAR5` | Partizipation | Ich fühle mich isoliert. | **Ja** | `PAR5_roh` | `PAR5` (= 6−roh) |
| `IU01` | `AUTH1` | Authentizität | Handlungen fühlen sich kongruent an. | Nein | `AUTH1_roh` | `AUTH1` |
| `IU02` | `AUTH2` | Authentizität | Ich erlebe Flow-Zustände. | Nein | `AUTH2_roh` | `AUTH2` |
| `IU03` | `AUTH3` | Authentizität | Mein Leben hat klare Sinnstiftung. | Nein | `AUTH3_roh` | `AUTH3` |
| `IU04` | `AUTH4` | Authentizität | Ich maskiere meine Persönlichkeit. | **Ja** | `AUTH4_roh` | `AUTH4` (= 6−roh) |
| `IU05` | `AUTH5` | Authentizität | Ich kann mit meinen Entscheidungen schlafen. | Nein | `AUTH5_roh` | `AUTH5` |

### Attention Check

| SoSci Intern | Direct-Import Label | Item-Text | Korrekter Wert |
|---|---|---|---|
| `AC01` | `ATTN1` | Dies ist eine Kontrollfrage. Bitte wählen Sie "Teils/teils" (3). | 3 |

### SWLS-Mapping

| SoSci Intern | Direct-Import Label | Item-Text (Kurzform) | Reverse? | Scoring |
|---|---|---|---|---|
| `SW01` | `SWLS1` | Mein Leben entspricht meinen Idealvorstellungen. | Nein | Summenscore |
| `SW02` | `SWLS2` | Meine Lebensbedingungen sind ausgezeichnet. | Nein | Summenscore |
| `SW03` | `SWLS3` | Ich bin mit meinem Leben zufrieden. | Nein | Summenscore |
| `SW04` | `SWLS4` | Ich habe wesentliche Dinge erreicht. | Nein | Summenscore |
| `SW05` | `SWLS5` | Ich würde kaum etwas ändern. | Nein | Summenscore |

### Demographische Variablen

| SoSci Intern | Direct-Import Label | Variable | Skalenniveau | Beschreibung |
|---|---|---|---|---|
| `DA01` | `ALTER` | `ALTER` | Metrisch | Alter in Jahren |
| `DG01` | `GESCHL` | `GESCHL` | Nominal | 1=Männl., 2=Weibl., 3=Non-binär, 4=k.A. |
| `DB01` | `BILDUNG` | `BILDUNG` | Ordinal | 1–9, aufsteigend nach Bildungsgrad |
| `DJ01` | `BERUF` | `BERUF` | Nominal | 1–7, Beschäftigungsstatus |

---

## 12. Reverse-Coding-Hinweise

### Formel für 5-Punkte-Skala (IMP)

```
Rekodierter Wert = (Maximaler Skalenwert + 1) − Roher Wert
                 = (5 + 1) − x
                 = 6 − x
```

**Beispiel:** Rohwert 2 → Rekodiert: 6 − 2 = 4

### R-Code für Reverse-Coding (IMP-Skala)

```r
# Alle negativ formulierten IMP-Items umkodieren
# Formel: 6 - x (für 5-Punkte-Skala)

data <- data %>%
  mutate(
    # Autonomie
    AUT2 = 6 - IA02,
    AUT3 = 6 - IA03,
    AUT5 = 6 - IA05,
    # Kompetenz
    KOM2 = 6 - IK02,
    KOM5 = 6 - IK05,
    # Resonanz
    RES2 = 6 - IR02,
    RES5 = 6 - IR05,
    # Partizipation
    PAR4 = 6 - IP04,
    PAR5 = 6 - IP05,
    # Authentizität
    AUTH4 = 6 - IU04
  )
```

### Dimensionsscores berechnen (IMP)

```r
data <- data %>%
  mutate(
    # Positiv-Items direkt übernehmen (keine Umkodierung)
    AUT1  = IA01, AUT4  = IA04,
    KOM1  = IK01, KOM3  = IK03, KOM4  = IK04,
    RES1  = IR01, RES3  = IR03, RES4  = IR04,
    PAR1  = IP01, PAR2  = IP02, PAR3  = IP03,
    AUTH1 = IU01, AUTH2 = IU02, AUTH3 = IU03, AUTH5 = IU05,
    
    # Dimensionsscores (Mittelwert je 5 Items)
    IMP_AUT  = rowMeans(cbind(AUT1,  AUT2,  AUT3,  AUT4,  AUT5),  na.rm=TRUE),
    IMP_KOM  = rowMeans(cbind(KOM1,  KOM2,  KOM3,  KOM4,  KOM5),  na.rm=TRUE),
    IMP_RES  = rowMeans(cbind(RES1,  RES2,  RES3,  RES4,  RES5),  na.rm=TRUE),
    IMP_PAR  = rowMeans(cbind(PAR1,  PAR2,  PAR3,  PAR4,  PAR5),  na.rm=TRUE),
    IMP_AUTH = rowMeans(cbind(AUTH1, AUTH2, AUTH3, AUTH4, AUTH5), na.rm=TRUE),
    
    # IMP-Gesamtscore (Mittelwert aller 25 Items)
    IMP_GESAMT = rowMeans(cbind(IMP_AUT, IMP_KOM, IMP_RES, IMP_PAR, IMP_AUTH), na.rm=TRUE),
    
    # SWLS-Gesamtscore (Summe)
    SWLS_GESAMT = SW01 + SW02 + SW03 + SW04 + SW05
  )
```

### Attention Check Filter

```r
# Alle Fälle ausschließen, bei denen Attention Check nicht korrekt beantwortet
data_clean <- data %>%
  filter(AC01 == 3)

cat("Ausgeschlossene Fälle:", nrow(data) - nrow(data_clean), "\n")
cat("Verbleibende Fälle:", nrow(data_clean), "\n")
```

---

*Ende des Direct-Import-Guides — 5D-IMP-Studie*  
*Datei: sosci_direct_import.md | Erstellt: 2026-04-02*
