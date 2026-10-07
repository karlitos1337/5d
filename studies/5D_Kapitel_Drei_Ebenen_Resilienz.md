# 5D-Kapitel: Drei-Ebenen-Resilienz

**Status des Dokuments:** formal-heuristisches Denkmodell zur Veranschaulichung der ungefähren Funktionsweise. Es ist **kein** kausal validiertes Systemmodell und enthält **keine** Beweise empirischer Sachverhalte. Mathematisch bewiesen sind nur „Wenn-dann“-Aussagen: Gelten die Annahmen, folgt die Folgerung.

> **Hinweis zum Umfang:** Dieses Dokument wurde im Zuge des Epistemic Upgrades (Patches M1–M7) neu angelegt. Es enthält die Sektionen 4–7. Die Sektionen 1–3 existieren im Repository noch nicht und sind hier nicht rekonstruiert.

## Legende: Status-Tags

| Tag | Bedeutung |
|---|---|
| `[Satz]` | Mathematisch bewiesen (unter den genannten Annahmen) |
| `[Modellannahme]` | Gestaltungsentscheidung des Modells, nicht empirisch geprüft |
| `[Analogie]` | Didaktisches Werkzeug, überträgt Struktur, nicht Kausalität |
| `[Hypothese]` | Prüfbare, noch nicht geprüfte Aussage |
| `[empirisch belegt]` | Durch Fachliteratur gestützt (Quelle angegeben) |
| `[Forschungsprogramm]` | Skizze dessen, was erst noch formalisiert/erhoben werden müsste |

Alle Zahlenwerte in diesem Kapitel (z. B. p = 0,4) sind **Platzhalter zur Illustration**, keine Messwerte.

---

## 4. Kontroll-Kosten: Das Trilemma als Bias-Varianz-Trade-off

### 4.1 Ausgangslage (Patch M3)

Status des gesamten Abschnitts: `[Analogie]`. Die Schätztheorie liefert eine **Struktur**, mit der sich das Trilemma *Aktualisieren / Kontrollieren / Loslassen* präzise beschreiben lässt. Dass Gesellschaften tatsächlich so funktionieren, ist damit nicht gezeigt.

Die Umwelt ist nicht-stationär: Der wahre Zustand μ(t) driftet `[Modellannahme]`. Ein Kollektiv führt einen Schätzer μ̂(t) nach, z. B. als exponentiell gleitenden Mittelwert mit Lernrate α ∈ (0, 1]:

μ̂(t) = α · y(t) + (1 − α) · μ̂(t − 1),  mit Beobachtung y(t) = μ(t) + Rauschen (Varianz r)

### 4.2 Der Fehler eines nachführenden Schätzers

Für eine lineare Drift μ(t) = μ_0 + d·t gilt im eingeschwungenen Zustand `[Satz]`:

- Nachlauf-Bias: Bias(α) = d · (1 − α) / α
- Rausch-Varianz: Var(α) = α · r / (2 − α)
- Gesamtfehler: MSE(α) = Bias(α)² + Var(α)

Kleines α (träge) → kleine Varianz, großer Bias. Großes α (sprunghaft) → kleiner Bias, große Varianz. Für d > 0 hat MSE(α) ein Minimum bei einer **mittleren** Lernrate `[Satz]`.

Rechenbeispiel (Illustration: d = 0,1, r = 1):

| α | Bias² | Varianz | MSE |
|---|---|---|---|
| 0,05 (starr) | 3,61 | 0,03 | 3,64 |
| 0,20 | 0,16 | 0,11 | 0,27 |
| ≈ 0,28 (Optimum) | – | – | ≈ 0,23 |
| 0,50 | 0,01 | 0,33 | 0,34 |
| 0,90 (sprunghaft) | < 0,001 | 0,82 | 0,82 |

> **Annahmen-Box M3**
> - **Muss gelten:** (1) Drift-Modell (hier: linear mit Rate d). (2) Beobachtungsrauschen unabhängig über die Zeit, Varianz r. (3) Eingeschwungener Zustand (lange genug beobachtet).
> - **Wenn (1) nicht gilt:** Bei Sprüngen oder Zufallsdrift verschiebt sich das optimale α, die Struktur „Minimum bei mittlerer Lernrate“ bleibt aber typischerweise erhalten (Standardergebnis für Kalman-Filter mit Random-Walk-Zustand).
> - **Wenn d = 0 (stationäre Umwelt):** Dann ist α → 0 optimal. Starre Kontrolle ist im Modell also **nur in einer stabilen Umwelt** günstig.

### 4.3 Zuordnung der drei Trilemma-Pole `[Analogie]`

| Pol | Entspricht im Modell | Fehlerprofil |
|---|---|---|
| **Kontrollieren** (Gleichschaltung) | α → 0: Schätzer wird eingefroren, alle folgen derselben Vorgabe | Niedrige Varianz, **wachsender Bias**. Das ist eher **Underfitting** bzw. „Anpassung an die Vergangenheit“, nicht Overfitting. |
| **Aktualisieren** (Exploration) | Mittleres α: neue Beobachtungen fließen dosiert ein | Bias bleibt klein, Varianz und Energieaufwand steigen moderat. Im Modell nahe am MSE-Minimum. |
| **Loslassen** (Dezentralisieren) | Mehrere lokale Schätzer statt eines zentralen; Aggregation wie in Sektion 6 | Senkt Varianz über Response-Diversity, sofern die lokalen Schätzer gering korreliert sind. |

**Lesart:** Im Modell ist Aktualisieren mit moderater Lernrate in einer driftenden Umwelt **günstiger** als starre Kontrolle. Das stützt sich auf die MSE-Zerlegung, **nicht** auf Chebyshev, und es ist **nicht** „die einzige Strategie“: Loslassen (Dezentralisieren) und Aktualisieren lassen sich kombinieren. Die Übertragung auf reale Governance bleibt `[Hypothese]`.

---

## 5. Bunker-Mathematik: Eskapismus als Konjunktion

### 5.1 Statistische Modellierung des Eskapismus (Patch M2)

Sei S das Ereignis „Langzeitüberleben in Isolation“. Das Modell nimmt an `[Modellannahme]`, dass S nur eintritt, wenn **alle** k Bedingungen E_1, …, E_k gleichzeitig erfüllt sind (Vorräte, Gesundheit, Sicherheit, Wartung, psychische Stabilität, …). Dann ist S = E_1 ∩ … ∩ E_k.

**Allgemein (Multiplikationssatz / Kettenregel)** `[Satz]`:

P(S) = P(E_1) · P(E_2 | E_1) · P(E_3 | E_1 ∩ E_2) · … · P(E_k | E_1 ∩ … ∩ E_{k−1})

**Nur bei stochastischer Unabhängigkeit** vereinfacht sich das zu `[Satz]`:

P(S) = ∏ P(E_i)

**Rechenbeispiel** (Illustration, kein Messwert): k = 7 Bedingungen, je p = 0,4 → P(S) = 0,4⁷ ≈ 0,0016.

> **Annahmen-Box M2 (Eskapismus)**
> - **Muss gelten:** (1) Alle k Bedingungen sind *notwendig* (UND-Struktur). (2) Für das Produkt ∏P(E_i): Unabhängigkeit der E_i. (3) Gleiches Zeitfenster für alle Bedingungen.
> - **Wenn (2) nicht gilt:** Bei positiv korrelierten Bedingungen (z. B. Geld verbessert Vorräte *und* Sicherheit) liegt die echte Wahrscheinlichkeit **höher** als ∏P(E_i). Obere Schranke ist immer P(S) ≤ min P(E_i) (Fréchet-Schranke) `[Satz]`, hier also ≤ 0,4.
> - **Wenn (1) nicht gilt:** Kann eine Bedingung durch eine andere ersetzt werden, ist die UND-Struktur falsch und das Rechenbeispiel unterschätzt P(S).

### 5.2 Faire Gegenrechnung: kollektive Systeme als Disjunktion

Kollektive Systeme werden hier modelliert `[Modellannahme]` als k **redundante, alternative** Pfade: Es genügt, dass **mindestens einer** trägt. Dann ist S = E_1 ∪ … ∪ E_k.

- Allgemein für zwei Ereignisse `[Satz]`: P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
- Bei Unabhängigkeit für k Ereignisse `[Satz]`: P(S) = 1 − ∏(1 − P(E_i)) = 1 − (1 − p)ᵏ

Rechenbeispiel (gleiche Illustrationswerte): 1 − 0,6⁷ ≈ 0,972.

> **Annahmen-Box M2 (Kollektiv)**
> - **Muss gelten:** (1) Die Pfade sind echte Alternativen (ODER-Struktur). (2) Unabhängigkeit der Pfade.
> - **Wenn (2) nicht gilt:** Positiv korrelierte Pfade (gemeinsame Ursache, z. B. derselbe Stromausfall trifft alle) senken die Union-Wahrscheinlichkeit. Dann schrumpft der Vorteil des Kollektivs. Das ist der Übergang zu Sektion 6 (Kovarianz).
> - **Fairness-Hinweis:** Der Vergleich UND vs. ODER ist eine Aussage über **Struktur**, nicht über Isolation vs. Gemeinschaft an sich. Ein Kollektiv mit UND-Abhängigkeiten (Single Point of Failure) verhält sich mathematisch wie der Bunker.

### 5.3 Sensitivitätstabelle (Illustration)

Werte: P(UND) = pᵏ / P(ODER) = 1 − (1 − p)ᵏ, jeweils unter Unabhängigkeit.

| p | k = 3 | k = 5 | k = 7 |
|---|---|---|---|
| 0,40 | 0,064 / 0,784 | 0,010 / 0,922 | 0,0016 / 0,972 |
| 0,60 | 0,216 / 0,936 | 0,078 / 0,990 | 0,028 / 0,998 |
| 0,80 | 0,512 / 0,992 | 0,328 / >0,999 | 0,210 / >0,999 |
| 0,90 | 0,729 / 0,999 | 0,590 / >0,999 | 0,478 / >0,999 |
| 0,95 | 0,857 / >0,999 | 0,774 / >0,999 | 0,698 / >0,999 |

**Lesart:** Auch bei hohen Einzelwahrscheinlichkeiten (p = 0,9) frisst die UND-Struktur bei k = 7 mehr als die Hälfte der Überlebenschance. Im Modell gilt: Eskapismus tauscht eine ODER-Struktur gegen eine UND-Struktur. Ob reale Fluchtstrategien diese Struktur haben, ist eine `[Hypothese]`.

---

## 6. Drei-Ebenen-Architektur: Response-Diversity statt Redundanz

### 6.1 Statistische Modellierung der Response-Diversity (Patch M1)

Das Modell betrachtet drei Ebenen (Individuum, Gemeinschaft, Institution) mit Antworten X_1, X_2, X_3 auf dieselbe Störung. Jede Antwort hat Fehlervarianz Var(X_i) = σ² (vereinfachend gleich) und paarweise Korrelation ρ `[Modellannahme]`.

**Für die Summe** Y = X_1 + X_2 + X_3 gilt allgemein `[Satz]`:

Var(Y) = ∑ Var(X_i) + 2 ∑_{i<j} Cov(X_i, X_j)

Mit gleicher Varianz und gleicher Korrelation: Var(Y) = nσ² + n(n−1)ρσ².

**Für den Mittelwert** Ȳ = Y / n gilt `[Satz]`:

Var(Ȳ) = (σ² / n) · (1 + (n − 1)ρ)

| Fall | ρ | Var(Summe), n = 3 | Var(Mittelwert), n = 3 |
|---|---|---|---|
| Identische Redundanz (Groupthink) | 1 | 9σ² (wächst mit n²) | σ² (keine Reduktion) |
| Unabhängige Ebenen | 0 | 3σ² | σ²/3 |
| Kompensierende Ebenen | −0,5 (Minimum für n = 3) | 0 | 0 |

**Lesart:**
- „Quadratisch“ gilt nur für die **Summe**: Bei ρ = 1 wächst ihre Varianz mit n² statt mit n. Beim **Mittelwert** bedeutet ρ = 1, dass drei Ebenen nicht mehr Sicherheit bringen als eine.
- Ziel ist daher nicht „Kovarianz gegen null“, sondern **Kovarianz möglichst klein, idealerweise negativ**: Ebenen, die gegenläufig reagieren (eine fängt auf, wo die andere versagt), senken die Varianz unter σ²/n. Die Untergrenze ist ρ ≥ −1/(n − 1), weil eine Kovarianzmatrix positiv semidefinit sein muss `[Satz]`.

### 6.2 Chebyshev als obere Schranke, nicht als Garantie

Sei μ̂ der kollektive Schätzer (z. B. Ȳ) und μ der wahre Zustand. Die Chebyshev-Ungleichung lautet `[Satz]`:

P(|μ̂ − E[μ̂]| ≥ ε) ≤ Var(μ̂) / ε²

Bezogen auf den wahren Wert μ (Markov-Ungleichung auf den quadrierten Fehler) gilt `[Satz]`:

P(|μ̂ − μ| ≥ ε) ≤ MSE(μ̂) / ε², mit MSE = Bias² + Var(μ̂)

Beispiel (Illustration, n = 3, ε = σ, Bias = 0): Bei ρ = 1 ist die Schranke 1 (also wertlos). Bei ρ = 0 ist sie 1/3.

**Was daraus folgt und was nicht:**
- Kleinere Varianz senkt die **Schranke** für das Risiko eines großen Fehlers. Das ist **ein** wirksamer Hebel, aber **nicht** „der einzige Weg“. Weitere Hebel sind mehr Ebenen (größeres n), weniger Bias und bessere Einzelschätzer (kleineres σ²).
- Chebyshev ist eine Schranke für *beliebige* Verteilungen. Die echte Fehlerwahrscheinlichkeit kann deutlich darunter liegen.
- **Vielfalt allein reicht nicht:** Sind alle drei Ebenen in dieselbe Richtung verzerrt, bleibt der Bias im Mittelwert vollständig erhalten. Diversität senkt die Varianz, nicht den gemeinsamen Bias.

> **Annahmen-Box M1**
> - **Muss gelten:** (1) Festgelegt ist, ob Y Summe (Gesamtlast) oder Mittelwert (kollektive Schätzung) ist; dieses Kapitel nutzt für Risiko-Aussagen den Mittelwert. (2) Varianzen und Kovarianzen existieren (endliche zweite Momente). (3) Alle Ebenen antworten auf dieselbe Störung im selben Zeitfenster.
> - **Unabhängigkeit ist Annahme, nicht Befund:** Gemeinsame Ursachen (gleiche Medien, gleiche Ausbildung, gleiche Infrastruktur) erzeugen positive Kovarianz, auch ohne direkte Absprache. Wer ρ = 0 unterstellt, muss begründen, warum es keine gemeinsamen Ursachen gibt.
> - **Wenn (3) nicht gilt:** Zeitversetzte Antworten erfordern ein dynamisches Modell (siehe Sektion 7).
> - **Status:** Die Formeln sind `[Satz]`. Die Übertragung auf Individuum/Gemeinschaft/Institution ist `[Analogie]`. Dass reale Gesellschaften mit höherer Response-Diversity robuster sind, ist `[Hypothese]` (ökologisch für Artengemeinschaften diskutiert unter „Response Diversity“, Elmqvist et al., 2003).

---

## Referenzen

- Elmqvist, T., Folke, C., Nyström, M., Peterson, G., Bengtsson, J., Walker, B., & Norberg, J. (2003). Response diversity, ecosystem change, and resilience. *Frontiers in Ecology and the Environment*, 1(9), 488–494.
