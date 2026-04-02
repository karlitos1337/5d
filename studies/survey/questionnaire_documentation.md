# 5D-IMP Studie — Fragebogen-Dokumentation

**Studientitel (intern):** 5D-IMP-Studie  
**Studientitel (extern/Prolific):** Motivation und Lebenszufriedenheit: Eine Studie zu persönlichen Ressourcen  
**Forscher:** Patrick Karletz (Unabhängiger Forscher)  
**Kontakt:** pkarletz@gmail.com  
**Plattform:** SoSci Survey (soscisurvey.de) — deutsche Server (DSGVO-konform)  
**Rekrutierung:** Prolific (deutschsprachige Teilnehmer, N = 400)  
**Geschätzte Dauer:** 15–20 Minuten  
**Vergütung:** ca. £1.50–2.00  
**Version:** 1.0 | **Datum:** 2026-04-01  
**OSF-Präregistrierung:** [Link einfügen nach Präregistrierung]  
**GitHub:** https://github.com/karlitos1337/5d

---

## Inhaltsverzeichnis

1. [Studienübersicht & Methodik](#1-studienübersicht--methodik)
2. [SoSci Survey Konfiguration](#2-sosci-survey-konfiguration)
3. [Block 0: Einverständniserklärung](#block-0-einverständniserklärung)
4. [Block 1: Demographische Daten](#block-1-demographische-daten)
5. [Block 2: IMP-Skala](#block-2-imp-skala)
6. [Block 3: SWLS](#block-3-swls---satisfaction-with-life-scale)
7. [Block 4: IPIP-NEO-120](#block-4-ipip-neo-120)
8. [Block 5: Debriefing](#block-5-debriefing)
9. [Scoring & Reverse Coding](#scoring--reverse-coding)
10. [Codebook / Variablen-Mapping](#codebook--variablen-mapping)
11. [Qualitätskontrolle & Exclusion Criteria](#qualitätskontrolle--exclusion-criteria)
12. [Prolific-Integration & URL-Parameter](#prolific-integration--url-parameter)
13. [Datenschutz & DSGVO](#datenschutz--dsgvo)

---

## 1. Studienübersicht & Methodik

### Forschungsziel
Validierung des 5D-IMP-Frameworks (fünf Dimensionen: Autonomie, Kompetenz, Resonanz, Partizipation, Authentizität) und Untersuchung des Zusammenhangs mit Lebenszufriedenheit (SWLS) sowie Big-Five-Persönlichkeitsmerkmalen (IPIP-NEO-120).

### Stichprobe
- **N (angestrebt):** 400
- **Einschlusskriterien:** Deutsch als Muttersprache oder fließend, Alter ≥ 18 Jahre
- **Rekrutierungsplattform:** Prolific
- **Vergütung:** ~£1.50–2.00 (entspricht ~£9/h bei 10–13 Min.)

### Instrumente
| Instrument | Kürzel | Items | Antwortformat | Block |
|---|---|---|---|---|
| IMP-Skala | IMP | 25 + 1 AC | 5-Punkt Likert | 2 |
| Satisfaction with Life Scale | SWLS | 5 | 7-Punkt Likert | 3 |
| IPIP-NEO-120 | BIG5 | 120 | 5-Punkt Likert | 4 |
| Demographika | DEMO | 4 | Verschiedene | 1 |

### Ablauf (Reihenfolge festgelegt)
```
Einverständnis → Demographika → IMP-Skala → SWLS → IPIP-NEO-120 → Debriefing
```

### Randomisierung
- Items **innerhalb** jeder IMP-Dimension werden randomisiert
- Die **Reihenfolge der Dimensionen** ist fest (A → C → R → P → Au)
- IPIP-NEO-120 Items werden innerhalb jeder Domäne randomisiert
- Kein Block-Rotation zwischen Teilnehmern

---

## 2. SoSci Survey Konfiguration

### Projekteinstellungen
```
Projektname: 5D_IMP_Study_2026
Sprache: Deutsch
Datenspeicherung: SoSci Survey Server (Deutschland)
SSL: Aktiviert
HTTPS: Erforderlich
Datenlöschung: 5 Jahre nach Abschluss
```

### URL-Parameter (Prolific)
SoSci Survey muss so konfiguriert werden, dass die Prolific-ID als URL-Parameter übergeben und gespeichert wird:

```
Survey-URL für Prolific:
https://www.soscisurvey.de/5d_imp/?source=prolific&PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
```

In SoSci Survey: **Extras → URL-Parameter** → folgende Parameter aktivieren:
| Parameter | Variable | Beschreibung |
|---|---|---|
| `PROLIFIC_PID` | `prolific_pid` | Eindeutige Prolific-Teilnehmer-ID |
| `STUDY_ID` | `study_id` | Prolific Studie-ID |
| `SESSION_ID` | `session_id` | Prolific Session-ID |
| `source` | `source` | Rekrutierungsquelle (= "prolific") |

### Zeitstempel-Erfassung
Folgende internen Variablen werden automatisch von SoSci Survey erfasst:

```
STARTED    — Startzeitpunkt (Unix-Timestamp)
LASTDATA   — Letzter Datenspeicherungs-Zeitpunkt
FINISHED   — Abschlusszeitpunkt (Boolean: 1/0)
TIME_SUM   — Gesamtdauer in Sekunden
TIME001–TIME008 — Dauer pro Seite in Sekunden
```

**Response-Time-Exclusion:** Teilnehmer mit `TIME_SUM < 300` (< 5 Minuten) werden als Speed-Responder ausgeschlossen (vgl. Exclusion Criteria).

### Fragebogen-Seiten in SoSci Survey
| Seite | Inhalt | SoSci-Typ |
|---|---|---|
| 1 | Einverständniserklärung | `welcome` / Textseite + Checkboxen |
| 2 | Demographika | `survey` — 4 Items |
| 3 | IMP: Autonomie (5 Items, randomisiert) | `survey` — Likert |
| 4 | IMP: Kompetenz (5 Items, randomisiert) | `survey` — Likert |
| 5 | IMP: Resonanz (5 Items, randomisiert) + Attention Check | `survey` — Likert |
| 6 | IMP: Partizipation (5 Items, randomisiert) | `survey` — Likert |
| 7 | IMP: Authentizität (5 Items, randomisiert) | `survey` — Likert |
| 8 | SWLS (5 Items) | `survey` — Likert |
| 9–13 | IPIP-NEO-120 (5 Seiten à 24 Items) | `survey` — Likert |
| 14 | Debriefing + Completion Code | `final` |

---

## Block 0: Einverständniserklärung

### Seitentyp: `welcome` (SoSci Survey Startseite)

### Titel (sichtbar für Teilnehmer):
**Willkommen zur Studie: Motivation und Lebenszufriedenheit: Eine Studie zu persönlichen Ressourcen**

### Text:
---
*Sehr geehrte Teilnehmerin, sehr geehrter Teilnehmer,*

*wir laden Sie herzlich ein, an einer wissenschaftlichen Online-Studie teilzunehmen, die von Patrick Karletz (Unabhängiger Forscher) durchgeführt wird.*

**Worum geht es?**
Diese Studie untersucht den Zusammenhang zwischen persönlichen Ressourcen, Motivation und Lebenszufriedenheit.

**Was erwartet Sie?**
Sie werden gebeten, mehrere Fragebogen zu Ihrem alltäglichen Erleben, Ihrer Persönlichkeit und Ihrer Lebenszufriedenheit auszufüllen. Die Bearbeitung dauert ca. **15–20 Minuten**.

**Vergütung**
Sie erhalten eine Vergütung von ca. **£1.50–2.00** über Prolific.

**Datenschutz**
- Alle Daten werden **anonym** erhoben und gespeichert.
- Die Daten werden auf Servern von SoSci Survey in Deutschland verarbeitet (**DSGVO-konform**).
- Es werden keine Rückschlüsse auf Ihre Person möglich sein.
- Ihre Daten werden ausschließlich für wissenschaftliche Zwecke verwendet.
- Die Daten werden nach Abschluss der Studie für maximal 5 Jahre gespeichert.

**Freiwilligkeit**
Ihre Teilnahme ist freiwillig. Sie können die Studie jederzeit und ohne Angabe von Gründen abbrechen. Ein Abbruch hat keine negativen Konsequenzen für Sie.

**Kontakt**
Bei Fragen wenden Sie sich bitte an: **pkarletz@gmail.com**

---

### Consent-Checkboxen (beide PFLICHT):

| Variable | Label | Typ | Pflicht |
|---|---|---|---|
| `CONSENT_1` | "Ich habe die oben stehenden Informationen gelesen und verstanden und stimme der Teilnahme an dieser Studie freiwillig zu." | Checkbox | Ja |
| `CONSENT_2` | "Ich bin 18 Jahre alt oder älter." | Checkbox | Ja |

**Validierung in SoSci Survey:** Beide Checkboxen müssen aktiviert sein (PHP-Filterfunktion oder SoSci-Pflichtfeld-Einstellung). Wenn eine Checkbox nicht aktiviert ist → Fehlermeldung: *"Bitte bestätigen Sie beide Felder, um fortzufahren."*

---

## Block 1: Demographische Daten

**SoSci-Seite:** 2  
**Seitenüberschrift:** "Bitte machen Sie zunächst einige Angaben zu Ihrer Person."

| # | Variable | Label | Typ | Optionen | Pflicht |
|---|---|---|---|---|---|
| 1 | `DEMO_01` | "Wie alt sind Sie?" | Numerisches Eingabefeld | Min: 18, Max: 99, Einheit: "Jahre" | Ja |
| 2 | `DEMO_02` | "Welchem Geschlecht ordnen Sie sich zu?" | Dropdown | Männlich / Weiblich / Non-binär / Keine Angabe | Ja |
| 3 | `DEMO_03` | "Was ist Ihr höchster Bildungsabschluss?" | Dropdown | Kein Abschluss / Hauptschulabschluss / Mittlere Reife / Fachabitur / Abitur / Berufsausbildung / Bachelor / Master / Promotion | Ja |
| 4 | `DEMO_04` | "Was ist Ihre aktuelle berufliche Situation?" | Dropdown | Vollzeit beschäftigt / Teilzeit beschäftigt / Selbständig / Student:in / Arbeitssuchend / Rente oder Pension / Sonstiges | Ja |

### Codierung Demographika
```
DEMO_02: 1=Männlich, 2=Weiblich, 3=Non-binär, 4=Keine Angabe
DEMO_03: 1=Kein Abschluss, 2=Hauptschulabschluss, 3=Mittlere Reife,
         4=Fachabitur, 5=Abitur, 6=Berufsausbildung,
         7=Bachelor, 8=Master, 9=Promotion
DEMO_04: 1=Vollzeit, 2=Teilzeit, 3=Selbständig, 4=Student:in,
         5=Arbeitssuchend, 6=Rente/Pension, 7=Sonstiges
```

---

## Block 2: IMP-Skala

**SoSci-Seiten:** 3–7 (je eine Seite pro Dimension)  
**Skala:** 5-Punkt Likert

### Antwortskala
| Wert | Label |
|---|---|
| 1 | Trifft gar nicht zu |
| 2 | Trifft eher nicht zu |
| 3 | Teils/teils |
| 4 | Trifft eher zu |
| 5 | Trifft voll zu |

### Instruktion (Seitenanfang, vor den Items):
> *"Die folgenden Aussagen beschreiben verschiedene Aspekte Ihres alltäglichen Erlebens. Bitte geben Sie an, inwieweit jede Aussage auf Sie zutrifft."*

### Randomisierung in SoSci Survey:
- Für jede Dimension eine separate `rotate`-Gruppe in SoSci Survey
- Die 5 Items pro Dimension werden per `rotate` (vollständig) oder `randomize` randomisiert
- PHP-Code in SoSci: `$aItems = shuffle(array('IMP01_01','IMP01_02','IMP01_03','IMP01_04','IMP01_05'));`
- Alternativ: SoSci Survey "Zufällige Anordnung von Items" Funktion pro Seite

---

### Dimension 1: Autonomie (A) — Seite 3

**Seitenüberschrift:** "Autonomie"

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `IMP01_01` | A1_1D | "Ich bestimme weitgehend selbst, wie ich meine Ziele verfolge." | + |
| `IMP01_02` | A2_2D | "Externe Regeln und Sanktionen bestimmen meinen Alltag stark." | − (R) |
| `IMP01_03` | A3_3D | "Ich fühle mich durch Bewertungssysteme (Noten/KPIs) eingeschränkt." | − (R) |
| `IMP01_04` | A4_4D | "Meine Motivation kommt hauptsächlich von innen, nicht von außen." | + |
| `IMP01_05` | A5_5D | "Ich habe Angst vor Konsequenzen bei Abweichung von Vorgaben." | − (R) |

**Reverse-coded Items (Autonomie):** `IMP01_02`, `IMP01_03`, `IMP01_05`

---

### Dimension 2: Kompetenz (C) — Seite 4

**Seitenüberschrift:** "Kompetenz"

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `IMP02_01` | C1_1D | "Ich kann meine Impulse gut regulieren und fokussieren." | + |
| `IMP02_02` | C2_2D | "Chronischer Stress beeinträchtigt meine Konzentration stark." | − (R) |
| `IMP02_03` | C3_3D | "Mein Körper fühlt sich energiegeladen und ausgeglichen an." | + |
| `IMP02_04` | C4_4D | "Ich erhole mich schnell von Rückschlägen." | + |
| `IMP02_05` | C5_5D | "Ich spüre oft Erschöpfung durch innere Konflikte." | − (R) |

**Reverse-coded Items (Kompetenz):** `IMP02_02`, `IMP02_05`

---

### Dimension 3: Resonanz (R) — Seite 5 (inkl. Attention Check)

**Seitenüberschrift:** "Resonanz"

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `IMP03_01` | R1_1D | "Ich kann mich bewusst in andere Perspektiven versetzen." | + |
| `IMP03_02` | R2_2D | "Ich bin oft in festen Rollen/Überzeugungen gefangen." | − (R) |
| `IMP03_03` | R3_3D | "Ich reflektiere regelmäßig meine eigenen Narrative." | + |
| `IMP03_04` | R4_4D | "Konflikte löse ich durch Perspektivenwechsel." | + |
| `IMP03_05` | R5_5D | "Emotionale Reaktionen überlagern oft mein rationales Denken." | − (R) |

**Reverse-coded Items (Resonanz):** `IMP03_02`, `IMP03_05`

#### Attention Check (eingebettet auf Seite 5, Position randomisiert):

| Variable | Itemtext | Korrekte Antwort |
|---|---|---|
| `ATTN_01` | "Dies ist eine Kontrollfrage. Bitte wählen Sie 'Teils/teils' (3)." | 3 |

**Hinweis:** Der Attention Check wird optisch nicht als solcher erkennbar gemacht. Er erscheint als reguläres Item in der Liste, mit dem gleichen Antwortformat (5-Punkt Likert: 1–5). Falsche Antwort → Exclusion-Flag gesetzt.

---

### Dimension 4: Partizipation (P) — Seite 6

**Seitenüberschrift:** "Partizipation"

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `IMP04_01` | P1_1D | "Ich kooperiere horizontal mit anderen ohne Hierarchie." | + |
| `IMP04_02` | P2_2D | "Mein Netzwerk besteht aus vertrauensvollen, authentischen Beziehungen." | + |
| `IMP04_03` | P3_3D | "Ideen entstehen emergent aus Gruppeninteraktionen." | + |
| `IMP04_04` | P4_4D | "Zentrale Entscheidungen blockieren oft unseren Fortschritt." | − (R) |
| `IMP04_05` | P5_5D | "Ich fühle mich isoliert von potenziellen Verbündeten." | − (R) |

**Reverse-coded Items (Partizipation):** `IMP04_04`, `IMP04_05`

---

### Dimension 5: Authentizität (Au) — Seite 7

**Seitenüberschrift:** "Authentizität"

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `IMP05_01` | Au1_1D | "Meine Handlungen fühlen sich kongruent mit meiner Identität an." | + |
| `IMP05_02` | Au2_2D | "Ich erlebe oft Flow-Zustände ohne innere Reibung." | + |
| `IMP05_03` | Au3_3D | "Mein Leben hat eine klare, innere Sinnstiftung." | + |
| `IMP05_04` | Au4_4D | "Ich maskiere Teile meiner Persönlichkeit, um zu passen." | − (R) |
| `IMP05_05` | Au5_5D | "Ich kann mit meinen Entscheidungen 'selbst schlafen'." | + |

**Reverse-coded Items (Authentizität):** `IMP05_04`

---

## Block 3: SWLS — Satisfaction with Life Scale

**SoSci-Seite:** 8  
**Skala:** 7-Punkt Likert  
**Referenz:** Glaesmer, H., Grande, G., Braehler, E., & Roth, M. (2011). The German version of the Satisfaction with Life Scale (SWLS): Psychometric properties, validity, and population-based norms. *European Journal of Psychological Assessment, 27*(2), 127–132. https://doi.org/10.1027/1015-5759/a000058

*(Hinweis: Die Original-Referenz für die deutsche Version ist häufig zitiert als Glaesmer et al., 2011, Diagnostica 57(2), 76–85.)*

### Antwortskala
| Wert | Label |
|---|---|
| 1 | Stimme überhaupt nicht zu |
| 2 | Stimme nicht zu |
| 3 | Stimme eher nicht zu |
| 4 | Weder noch |
| 5 | Stimme eher zu |
| 6 | Stimme zu |
| 7 | Stimme voll und ganz zu |

### Instruktion:
> *"Die folgenden fünf Aussagen beziehen sich auf Ihre allgemeine Lebenszufriedenheit. Bitte geben Sie an, inwieweit Sie jeder Aussage zustimmen."*

### Items

| Variable | Item-Code | Itemtext | Richtung |
|---|---|---|---|
| `SWLS_01` | SWLS_1 | "In den meisten Bereichen entspricht mein Leben meinen Idealvorstellungen." | + |
| `SWLS_02` | SWLS_2 | "Meine Lebensbedingungen sind ausgezeichnet." | + |
| `SWLS_03` | SWLS_3 | "Ich bin mit meinem Leben zufrieden." | + |
| `SWLS_04` | SWLS_4 | "Bisher habe ich die wesentlichen Dinge erreicht, die ich mir im Leben wünsche." | + |
| `SWLS_05` | SWLS_5 | "Wenn ich mein Leben noch einmal leben könnte, würde ich kaum etwas ändern." | + |

**Keine Reverse-coded Items in der SWLS.**

### Scoring SWLS
```
SWLS_total = SWLS_01 + SWLS_02 + SWLS_03 + SWLS_04 + SWLS_05
Range: 5–35
Interpretation (Pavot & Diener, 1993):
  31–35: Extremely satisfied
  26–30: Satisfied
  21–25: Slightly satisfied
  20:    Neutral
  15–19: Slightly dissatisfied
  10–14: Dissatisfied
  5–9:   Extremely dissatisfied
```

---

## Block 4: IPIP-NEO-120

**SoSci-Seiten:** 9–13 (je eine Seite pro Domäne, 24 Items pro Seite)  
**Skala:** 5-Punkt Likert  
**Quelle:** International Personality Item Pool (IPIP), https://ipip.ori.org/  
**Deutsche Version:** Basierend auf der IPIP-Übersetzung sowie Goldberg et al. (2006)

**Goldberg, L. R., Johnson, J. A., Eber, H. W., Hogan, R., Ashton, M. C., Cloninger, C. R., & Gough, H. C. (2006). The International Personality Item Pool and the future of public-domain personality measures. *Journal of Research in Personality, 40*(1), 84–96. https://doi.org/10.1016/j.jrp.2005.08.007**

### Antwortskala
| Wert | Label |
|---|---|
| 1 | Sehr unzutreffend |
| 2 | Eher unzutreffend |
| 3 | Weder noch |
| 4 | Eher zutreffend |
| 5 | Sehr zutreffend |

### Instruktion:
> *"Die folgenden Aussagen beschreiben verschiedene Verhaltensweisen und Einstellungen. Bitte geben Sie an, wie genau jede Aussage auf Sie zutrifft."*

---

### Domäne 1: Neurotizismus (N) — Seite 9

**SoSci-Variablen:** `N01` bis `N24`  
**Beschreibung:** Misst emotionale Instabilität, Angst, Reizbarkeit, Depression, Impulsivität, Verletzlichkeit.  
**Items:** 24 (12 positiv kodiert [+], 12 negativ kodiert [R])  
**Vollständige Itemliste:** https://ipip.ori.org/newNEOKey.htm (Skala: Neuroticism)

**Beispiel-Items (erste 3):**

| Variable | Itemtext (Deutsch) | Richtung | Facette |
|---|---|---|---|
| `N01` | "Ich mache mir oft Sorgen um Dinge." | + | Ängstlichkeit |
| `N02` | "Ich bin leicht zu erschüttern." | + | Reizbarkeit |
| `N03` | "Ich fühle mich selten traurig oder deprimiert." | − (R) | Depression |
| ... | *[21 weitere Items — vollständige Liste: ipip.ori.org]* | | |

**Reverse-coded Items (Neurotizismus):** N03, N05, N07, N09, N11, N13, N15, N17, N19, N21, N23, N24 *(genaue Zuweisung gemäß IPIP-Schlüssel)*

---

### Domäne 2: Extraversion (E) — Seite 10

**SoSci-Variablen:** `E01` bis `E24`  
**Beschreibung:** Misst Geselligkeit, Durchsetzungsvermögen, positive Emotionen, Aktivität, Aufregungssuche, Wärme.  
**Items:** 24 (12 positiv, 12 negativ)  
**Vollständige Itemliste:** https://ipip.ori.org/newNEOKey.htm (Skala: Extraversion)

**Beispiel-Items (erste 3):**

| Variable | Itemtext (Deutsch) | Richtung | Facette |
|---|---|---|---|
| `E01` | "Ich bin gern unter anderen Menschen." | + | Geselligkeit |
| `E02` | "Ich bin ein gesprächiger Mensch." | + | Geselligkeit |
| `E03` | "Ich halte mich gern im Hintergrund." | − (R) | Durchsetzungsvermögen |
| ... | *[21 weitere Items — vollständige Liste: ipip.ori.org]* | | |

**Reverse-coded Items (Extraversion):** E03, E05, E07, E09, E11, E13, E15, E17, E19, E21, E23, E24 *(genaue Zuweisung gemäß IPIP-Schlüssel)*

---

### Domäne 3: Offenheit für Erfahrungen (O) — Seite 11

**SoSci-Variablen:** `O01` bis `O24`  
**Beschreibung:** Misst Fantasie, Ästhetik, Gefühle, Handlungen, Ideen, Werte/Überzeugungen.  
**Items:** 24 (12 positiv, 12 negativ)  
**Vollständige Itemliste:** https://ipip.ori.org/newNEOKey.htm (Skala: Openness)

**Beispiel-Items (erste 3):**

| Variable | Itemtext (Deutsch) | Richtung | Facette |
|---|---|---|---|
| `O01` | "Ich habe eine lebhafte Vorstellungskraft." | + | Fantasie |
| `O02` | "Mich faszinieren abstrakte Ideen." | + | Ideen |
| `O03` | "Ich bevorzuge Routine vor Abwechslung." | − (R) | Handlungen |
| ... | *[21 weitere Items — vollständige Liste: ipip.ori.org]* | | |

**Reverse-coded Items (Offenheit):** O03, O05, O07, O09, O11, O13, O15, O17, O19, O21, O23, O24 *(genaue Zuweisung gemäß IPIP-Schlüssel)*

---

### Domäne 4: Verträglichkeit (A) — Seite 12

**SoSci-Variablen:** `A01` bis `A24`  
**Beschreibung:** Misst Vertrauen, Aufrichtigkeit, Altruismus, Kooperativität, Bescheidenheit, Mitgefühl.  
**Items:** 24 (12 positiv, 12 negativ)  
**Vollständige Itemliste:** https://ipip.ori.org/newNEOKey.htm (Skala: Agreeableness)

**Beispiel-Items (erste 3):**

| Variable | Itemtext (Deutsch) | Richtung | Facette |
|---|---|---|---|
| `A01` | "Ich habe ein gutes Wort für jeden." | + | Altruismus |
| `A02` | "Ich interessiere mich für andere Menschen." | + | Altruismus |
| `A03` | "Ich beleidige andere manchmal." | − (R) | Aufrichtigkeit |
| ... | *[21 weitere Items — vollständige Liste: ipip.ori.org]* | | |

**Reverse-coded Items (Verträglichkeit):** A03, A05, A07, A09, A11, A13, A15, A17, A19, A21, A23, A24 *(genaue Zuweisung gemäß IPIP-Schlüssel)*

---

### Domäne 5: Gewissenhaftigkeit (C) — Seite 13

**SoSci-Variablen:** `C01` bis `C24`  
**Beschreibung:** Misst Kompetenz, Ordnung, Pflichtbewusstsein, Leistungsstreben, Selbstdisziplin, Besonnenheit.  
**Items:** 24 (12 positiv, 12 negativ)  
**Vollständige Itemliste:** https://ipip.ori.org/newNEOKey.htm (Skala: Conscientiousness)

**Beispiel-Items (erste 3):**

| Variable | Itemtext (Deutsch) | Richtung | Facette |
|---|---|---|---|
| `C01` | "Ich erledige meine Aufgaben sofort." | + | Selbstdisziplin |
| `C02` | "Ich halte immer meine Versprechen." | + | Pflichtbewusstsein |
| `C03` | "Ich mache oft ein Durcheinander." | − (R) | Ordnung |
| ... | *[21 weitere Items — vollständige Liste: ipip.ori.org]* | | |

**Reverse-coded Items (Gewissenhaftigkeit):** C03, C05, C07, C09, C11, C13, C15, C17, C19, C21, C23, C24 *(genaue Zuweisung gemäß IPIP-Schlüssel)*

---

## Block 5: Debriefing

**SoSci-Seite:** 14 (Abschlussseite)  
**Seitentyp:** `final`

### Text:

---
**Vielen Dank für Ihre Teilnahme!**

Ihre Antworten wurden erfolgreich gespeichert und helfen, die Forschung zu persönlichen Ressourcen und Lebenszufriedenheit voranzubringen.

**Worum ging es in dieser Studie?**

Diese Studie untersuchte das **5D-IMP-Framework** — ein Modell, das fünf Dimensionen personaler Ressourcen beschreibt:
- **Autonomie:** Selbstbestimmung und intrinsische Motivation
- **Kompetenz:** Selbstregulation, Resilienz und körperliches Wohlbefinden
- **Resonanz:** Perspektivenwechsel und Reflexionsfähigkeit
- **Partizipation:** Kooperative, horizontale Vernetzung
- **Authentizität:** Kongruenz zwischen Handlungen und Identität

Wir untersuchen, wie diese fünf Dimensionen mit Lebenszufriedenheit (SWLS) und Persönlichkeitsmerkmalen (Big Five) zusammenhängen.

**Mehr erfahren:**
Das Projekt ist Open Science — alle Materialien sind öffentlich zugänglich:
🔗 GitHub: https://github.com/karlitos1337/5d

**Fragen oder Anmerkungen?**
Wenden Sie sich jederzeit an: pkarletz@gmail.com

**Ihren Prolific-Abschluss-Code erhalten Sie hier:**

> **Completion Code: [WIRD VON PROLIFIC GENERIERT UND HIER EINGEFÜGT]**

*Bitte kopieren Sie diesen Code und kehren Sie zu Prolific zurück, um Ihre Vergütung zu erhalten.*

---

### SoSci Survey Redirect (automatisch nach Debriefing):
```
Weiterleitung zu Prolific:
https://app.prolific.co/submissions/complete?cc=[COMPLETION_CODE]
```

Diese URL wird in SoSci Survey unter **Projekteinstellungen → Abschlussseite → Weiterleitung** eingetragen.

---

## Scoring & Reverse Coding

### Allgemeine Formel Reverse Coding
```
x_r = (Skalenmax + Skalenmin) - x
```
- **5-Punkt-Skala:** `x_r = 6 - x`
- **7-Punkt-Skala:** (nicht relevant, da SWLS keine R-Items hat)

### IMP-Skala Scoring

#### Reverse Coding (5-Punkt-Skala: x_r = 6 - x)
| Variable | Item | Original | Rekodiert als |
|---|---|---|---|
| `IMP01_02` | A2_2D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP01_02r` |
| `IMP01_03` | A3_3D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP01_03r` |
| `IMP01_05` | A5_5D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP01_05r` |
| `IMP02_02` | C2_2D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP02_02r` |
| `IMP02_05` | C5_5D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP02_05r` |
| `IMP03_02` | R2_2D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP03_02r` |
| `IMP03_05` | R5_5D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP03_05r` |
| `IMP04_04` | P4_4D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP04_04r` |
| `IMP04_05` | P5_5D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP04_05r` |
| `IMP05_04` | Au4_4D | 1→5, 2→4, 3→3, 4→2, 5→1 | `IMP05_04r` |

#### Dimensionswerte (Mittelwerte)
```r
# R-Code zur Berechnung:
IMP_Autonomie    <- rowMeans(data[, c("IMP01_01", "IMP01_02r", "IMP01_03r", "IMP01_04", "IMP01_05r")])
IMP_Kompetenz    <- rowMeans(data[, c("IMP02_01", "IMP02_02r", "IMP02_03", "IMP02_04", "IMP02_05r")])
IMP_Resonanz     <- rowMeans(data[, c("IMP03_01", "IMP03_02r", "IMP03_03", "IMP03_04", "IMP03_05r")])
IMP_Partizipation<- rowMeans(data[, c("IMP04_01", "IMP04_02", "IMP04_03", "IMP04_04r", "IMP04_05r")])
IMP_Authentizitat<- rowMeans(data[, c("IMP05_01", "IMP05_02", "IMP05_03", "IMP05_04r", "IMP05_05")])
IMP_Gesamt       <- rowMeans(cbind(IMP_Autonomie, IMP_Kompetenz, IMP_Resonanz,
                                    IMP_Partizipation, IMP_Authentizitat))
```

#### SWLS-Score
```r
SWLS_Gesamt <- rowSums(data[, c("SWLS_01","SWLS_02","SWLS_03","SWLS_04","SWLS_05")])
# Range: 5–35
```

#### IPIP-NEO-120 Scores
```r
# Reverse Coding gemäß IPIP-Schlüssel (https://ipip.ori.org/newNEOKey.htm)
# Beispiel Neurotizismus:
N_positiv <- c("N01","N02","N04","N06","N08","N10","N12","N14","N16","N18","N20","N22")
N_negativ <- c("N03","N05","N07","N09","N11","N13","N15","N17","N19","N21","N23","N24")
# Rekodierung: N_neg_r <- 6 - data[, N_negativ]
N_Gesamt  <- rowMeans(cbind(data[, N_positiv], 6 - data[, N_negativ]))
# Analog für E, O, A, C
```

---

## Codebook / Variablen-Mapping

### Vollständige Variablenliste

| Variable | Label | Typ | Werte | Block |
|---|---|---|---|---|
| `prolific_pid` | Prolific Teilnehmer-ID | String | — | System |
| `study_id` | Prolific Studie-ID | String | — | System |
| `session_id` | Prolific Session-ID | String | — | System |
| `source` | Rekrutierungsquelle | String | "prolific" | System |
| `STARTED` | Startzeitpunkt | Timestamp | Unix | System |
| `FINISHED` | Abgeschlossen | Boolean | 0/1 | System |
| `TIME_SUM` | Gesamtdauer | Integer | Sekunden | System |
| `CONSENT_1` | Einverständnis gelesen | Boolean | 0/1 | 0 |
| `CONSENT_2` | Alter ≥ 18 | Boolean | 0/1 | 0 |
| `DEMO_01` | Alter | Integer | 18–99 | 1 |
| `DEMO_02` | Geschlecht | Integer | 1–4 | 1 |
| `DEMO_03` | Bildungsniveau | Integer | 1–9 | 1 |
| `DEMO_04` | Berufliche Situation | Integer | 1–7 | 1 |
| `IMP01_01`–`IMP01_05` | IMP Autonomie Items 1–5 | Integer | 1–5 | 2 |
| `IMP02_01`–`IMP02_05` | IMP Kompetenz Items 1–5 | Integer | 1–5 | 2 |
| `IMP03_01`–`IMP03_05` | IMP Resonanz Items 1–5 | Integer | 1–5 | 2 |
| `ATTN_01` | Attention Check | Integer | 1–5 | 2 |
| `IMP04_01`–`IMP04_05` | IMP Partizipation Items 1–5 | Integer | 1–5 | 2 |
| `IMP05_01`–`IMP05_05` | IMP Authentizität Items 1–5 | Integer | 1–5 | 2 |
| `SWLS_01`–`SWLS_05` | SWLS Items 1–5 | Integer | 1–7 | 3 |
| `N01`–`N24` | IPIP Neurotizismus Items 1–24 | Integer | 1–5 | 4 |
| `E01`–`E24` | IPIP Extraversion Items 1–24 | Integer | 1–5 | 4 |
| `O01`–`O24` | IPIP Offenheit Items 1–24 | Integer | 1–5 | 4 |
| `A01`–`A24` | IPIP Verträglichkeit Items 1–24 | Integer | 1–5 | 4 |
| `C01`–`C24` | IPIP Gewissenhaftigkeit Items 1–24 | Integer | 1–5 | 4 |

**Berechnete Variablen (post-hoc im Analyseskript):**

| Variable | Formel | Range |
|---|---|---|
| `IMP_Autonomie` | Mean(IMP01_01, IMP01_02r, IMP01_03r, IMP01_04, IMP01_05r) | 1–5 |
| `IMP_Kompetenz` | Mean(IMP02_01, IMP02_02r, IMP02_03, IMP02_04, IMP02_05r) | 1–5 |
| `IMP_Resonanz` | Mean(IMP03_01, IMP03_02r, IMP03_03, IMP03_04, IMP03_05r) | 1–5 |
| `IMP_Partizipation` | Mean(IMP04_01, IMP04_02, IMP04_03, IMP04_04r, IMP04_05r) | 1–5 |
| `IMP_Authentizitat` | Mean(IMP05_01, IMP05_02, IMP05_03, IMP05_04r, IMP05_05) | 1–5 |
| `IMP_Gesamt` | Mean(alle 5 Dimensionen) | 1–5 |
| `SWLS_Gesamt` | Sum(SWLS_01–SWLS_05) | 5–35 |
| `N_Gesamt` | Mean(N01–N24, mit Reverse Coding) | 1–5 |
| `E_Gesamt` | Mean(E01–E24, mit Reverse Coding) | 1–5 |
| `O_Gesamt` | Mean(O01–O24, mit Reverse Coding) | 1–5 |
| `A_Gesamt` | Mean(A01–A24, mit Reverse Coding) | 1–5 |
| `C_Gesamt` | Mean(C01–C24, mit Reverse Coding) | 1–5 |

---

## Qualitätskontrolle & Exclusion Criteria

### A priori festgelegte Ausschlusskriterien (präregistriert)

| Kriterium | Variable | Schwellenwert | Aktion |
|---|---|---|---|
| 1. Einverständnis fehlt | `CONSENT_1`, `CONSENT_2` | Nicht beide = 1 | Ausschluss |
| 2. Nicht abgeschlossen | `FINISHED` | ≠ 1 | Ausschluss |
| 3. Speed-Responder | `TIME_SUM` | < 300 Sekunden (5 Min.) | Ausschluss |
| 4. Attention Check | `ATTN_01` | ≠ 3 | Ausschluss |
| 5. Straight-lining | SD über alle IMP-Items | < 0.1 | Ausschluss |
| 6. Alter außerhalb Bereich | `DEMO_01` | < 18 oder > 99 | Ausschluss |

### R-Code für Ausschluss-Pipeline
```r
data_clean <- data %>%
  filter(CONSENT_1 == 1 & CONSENT_2 == 1) %>%
  filter(FINISHED == 1) %>%
  filter(TIME_SUM >= 300) %>%
  filter(ATTN_01 == 3) %>%
  filter(apply(.[, IMP_vars], 1, sd) >= 0.1) %>%
  filter(DEMO_01 >= 18 & DEMO_01 <= 99)
```

### Fehlende Werte
- Weniger als 10% fehlende Werte pro Item: Verbleib im Datensatz
- Mehr als 20% fehlende Werte über alle Items: Ausschluss
- Imputation: Full Information Maximum Likelihood (FIML) im SEM-Modell

---

## Prolific-Integration & URL-Parameter

### Konfiguration in SoSci Survey

**Schritt 1: URL-Parameter aktivieren**
1. SoSci Survey → Ihr Projekt → Extras → URL-Parameter
2. Folgende Parameter hinzufügen:
   - `PROLIFIC_PID` → Variablenname: `prolific_pid`
   - `STUDY_ID` → Variablenname: `study_id`
   - `SESSION_ID` → Variablenname: `session_id`

**Schritt 2: Study-URL für Prolific**
```
https://www.soscisurvey.de/[IHR-PROJEKT-NAME]/?source=prolific&PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
```

**Schritt 3: Completion URL in Prolific**
In Prolific → Study Settings → Completion URL:
```
https://app.prolific.co/submissions/complete?cc=[IHR_COMPLETION_CODE]
```

Dieser Link wird auch am Ende des SoSci-Fragebogens angezeigt (Debriefing-Seite).

**Schritt 4: SoSci Survey Weiterleitung**
Projekt → Einstellungen → Abschlussseite:
```
URL: https://app.prolific.co/submissions/complete?cc=[IHR_COMPLETION_CODE]
Typ: Automatische Weiterleitung nach 5 Sekunden
```

### Datenschutz Prolific-ID
Die `PROLIFIC_PID` ermöglicht die Zuordnung zur Prolific-Plattform (für Vergütung), ist aber kein persönliches Identifikationsmerkmal. Sie wird nach Abschluss der Studie von den Antwortdaten getrennt gespeichert.

---

## Datenschutz & DSGVO

### Rechtsgrundlage
- **Art. 6 Abs. 1 lit. a DSGVO:** Einwilligung (informierte Einverständniserklärung)
- **Art. 89 DSGVO:** Verarbeitung zu wissenschaftlichen Forschungszwecken

### Technische und organisatorische Maßnahmen (TOM)
- Datenspeicherung: SoSci Survey Server, Deutschland
- Verschlüsselung: SSL/TLS für alle Übertragungen
- Anonymisierung: Keine direkt identifizierenden Merkmale erhoben
- Pseudonymisierung: Prolific-ID wird separat von Antwortdaten verwaltet
- Datenlöschung: Spätestens 5 Jahre nach Studienabschluss
- Zugriff: Nur Patrick Karletz (Forscher)

### Datenschutzerklärung (Kurzfassung im Fragebogen)
Vollständige Datenschutzerklärung: Auf Anfrage per E-Mail erhältlich (pkarletz@gmail.com)

---

## Änderungshistorie

| Version | Datum | Änderung | Autor |
|---|---|---|---|
| 1.0 | 2026-04-01 | Initiale Version | P. Karletz |

---

*Dokument erstellt am: 2026-04-01*  
*Basiert auf OSF-Präregistrierung 5D-IMP-Study*  
*Alle Instrumente gemäß ihren jeweiligen Nutzungsbedingungen verwendet.*  
*IPIP-Items: Public Domain (https://ipip.ori.org/)*  
*SWLS: Deutsche Version gemäß Glaesmer et al. (2011)*
