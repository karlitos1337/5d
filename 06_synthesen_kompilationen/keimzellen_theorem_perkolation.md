# Das Keimzellen-Theorem: Funktionale Vollständigkeit als Perkolationsbedingung

**Autor:** Patrick Karletz / Kognitiver Resonanz-Partner  
**Datum:** 30.03.2026, 02:30 CET  
**Status:** Arbeitspapier — Pre-Peer-Review  
**Repo:** karlitos1337/5d  
**Lizenz:** CC BY 4.0

---

## Abstract

Die bisherige Perkolationsgleichung des 5D-Frameworks postuliert einen festen Schwellenwert ρ_c ≈ 0,075 für die Emergenz kollektiver Intelligenz. Diese Arbeit zeigt, dass feste Schwellenwerte nur in homogenen (oder manipulierten) Netzwerken gültig sind und entwickelt eine erweiterte Formulierung: das **Keimzellen-Theorem**. Es besagt, dass in heterogenen menschlichen Netzwerken nicht die absolute Anzahl authentischer Knoten entscheidend ist, sondern die **funktionale Vollständigkeit** kleiner Gruppen — definiert als die Mindestrepräsentation aller Intelligenzdimensionen (1D–5D). Daraus folgt eine zweistufige Perkolationsgleichung: (1) Keimzellenbildung durch Dimensionsdiversität, (2) Netzwerk-Perkolation durch Keimzellenvernetzung. Die Nicht-Erzwingbarkeit dieser Voraussetzungen wird als notwendige Systemeigenschaft formalisiert.

---

## 1. Problemstellung: Warum ρ_c = 0,075 zu starr ist

### 1.1 Die aktuelle Formulierung

Das 5D-Framework definiert kollektive Intelligenz (CI) als:

```
CI = Σ IMPᵢ · Θ(ρ − ρ_c)     wobei ρ_c ≈ 0,075
```

Hierbei ist Θ die Heaviside-Stufenfunktion, ρ die Dichte authentisch vernetzter Knoten, und ρ_c der kritische Schwellenwert aus der Perkolationstheorie für zufällige Netzwerke (Erdős-Rényi-Modell).

### 1.2 Das Problem

Dieser Schwellenwert gilt unter drei Annahmen, die in menschlichen Systemen nicht erfüllt sind:

| Annahme | Erdős-Rényi | Menschliche Netzwerke | Quelle |
|---------|-------------|----------------------|--------|
| Knoten sind identisch | ✅ | ❌ Menschen haben verschiedene kognitive Profile | [Hong & Page, 2004](https://doi.org/10.1073/pnas.0403723101) |
| Verbindungen sind zufällig | ✅ | ❌ Homophilie, Clustering, Hubs | [Newman, 2002](https://doi.org/10.1103/PhysRevLett.89.208701) |
| Netzwerk hat kein Gedächtnis | ✅ | ❌ Hysterese: Aktivierung ≠ Recovery | [PNAS Nexus, 2025](https://academic.oup.com/pnasnexus/article/4/6/pgaf192/8160299) |

**Empirische Korrektur:** Meta-Analyse sozialer Kipp-Punkte (Modellierung + Empirie) ergibt ρ_c ∈ [0,10; 0,43], Mittelwert 0,24–0,27 ([Everall et al., 2023](https://egusphere.copernicus.org/preprints/2023/egusphere-2023-2241/)).

### 1.3 Kernbeobachtung

> **"Es gibt nur absolute Schwellenwerte, wenn das System manipuliert ist."**  
> — P. Karletz, 30.03.2026

Manipulation eliminiert Varianz. Ein System, in dem alle Knoten homogen gemacht werden (einheitlicher Lehrplan, Noten, Uniformen, algorithmische Feeds), erzeugt seine eigene Berechenbarkeit. Der feste ρ_c ist ein Artefakt der Gleichschaltung — nicht eine Eigenschaft des Systems.

In natürlichen, heterogenen Systemen ist ρ_c selbst eine Variable.

---

## 2. Drei Theoreme als Fundament

### 2.1 Ashbys Gesetz der erforderlichen Varietät (1956)

> **"Only variety can absorb variety."**  
> — W. Ross Ashby, *Introduction to Cybernetics*, 1956

**Formal:** Für ein System S mit Varietät V(S) und einen Regler R mit Varietät V(R) gilt:

```
V(R) ≥ V(S)     (notwendige Bedingung für Regulation)
```

**Übersetzung ins 5D-Framework:** Eine Gruppe, die ein komplexes Problem lösen soll (V(S) = hoch), benötigt mindestens so viele verschiedene kognitive Werkzeuge wie das Problem Dimensionen hat. Wenn das Problem alle 5 Dimensionen der Intelligenz erfordert (Gefahrenerkennung, Selbstregulation, Empathie, Dezentrale Vernetzung, Systemgestaltung), muss die Gruppe alle 5 Dimensionen repräsentieren.

**Quelle:** Ashby, W.R. (1956). *An Introduction to Cybernetics.* Chapman & Hall. [Online-Volltext](http://pespmc1.vub.ac.be/books/IntroCyb.pdf)

### 2.2 Das Hong-Page-Diversitäts-Theorem (2004)

> **"Diversity trumps ability."**

[Hong & Page (2004, PNAS)](https://doi.org/10.1073/pnas.0403723101) zeigten formal und simulativ:

**Theorem (Hong-Page):** Unter den Bedingungen (a) das Problem ist hinreichend schwer, (b) die Agenten sind intelligent genug (nicht zufällig), und (c) die Population ist groß — übertrifft eine **zufällig gewählte, funktional diverse Gruppe** eine Gruppe der **individuell besten** Problemlöser.

**Mathematisch:** Agenten besitzen *Perspektiven* (Repräsentationen des Problemraums) und *Heuristiken* (Suchstrategien). Funktionale Diversität = Varianz der Perspektiven × Varianz der Heuristiken. Wenn die besten Individuen ähnliche Heuristiken haben (was bei Selektion unvermeidlich ist), ist ihre kollektive Leistung geringer als die einer diverseren Gruppe.

**Kritische Einschränkung (2023):** [Aggarwal & Woolley (Frontiers in Psychology, 2019)](https://doi.org/10.3389/fpsyg.2019.00112) fanden eine **umgekehrte U-Kurve**: Moderate kognitive Diversität maximiert kollektive Intelligenz. Zu viel Diversität erhöht Koordinationskosten und reduziert implizites Lernen (β = −0.91, p = 0.03). Das Optimum ist nicht "maximale Diversität", sondern **funktionale Vollständigkeit ohne Redundanz-Overhead**.

### 2.3 Conant-Ashby Good Regulator Theorem (1970)

> **"Every good regulator of a system must be a model of that system."**

[Conant & Ashby (1970)](https://doi.org/10.1080/00207727008920220) bewiesen:

**Theorem:** Der einfachste optimale Regler R eines Systems S erzeugt Aktionen, die mit den Systemzuständen durch eine Abbildung h: S → R verbunden sind. Der Regler muss isomorph zum System sein.

**Übersetzung:** Eine Gruppe, die ein 5-dimensionales System regulieren soll (z.B. eine Schule, ein Unternehmen, eine Gesellschaft), muss selbst alle 5 Dimensionen als interne Zustände besitzen. Nicht als Wissen — als **verkörperte kognitive Werkzeuge**.

---

## 3. Das Keimzellen-Theorem

### 3.1 Definition: Funktionale Vollständigkeit

**Definition 1 (Funktionale Vollständigkeit):** Eine Gruppe G = {g₁, g₂, ..., gₙ} ist *funktional vollständig* bezüglich eines Dimensionsraums D = {D₁, D₂, ..., Dₖ}, wenn:

```
∀ Dᵢ ∈ D : ∃ gⱼ ∈ G mit dom(gⱼ) ∩ Dᵢ ≠ ∅
```

In Worten: Für jede Dimension existiert mindestens ein Gruppenmitglied, dessen dominante kognitive Kompetenz diese Dimension abdeckt.

Für das 5D-Framework: D = {1D, 2D, 3D, 4D, 5D}, also k = 5.

### 3.2 Definition: Keimzelle

**Definition 2 (Keimzelle):** Eine *Keimzelle* K ist eine funktional vollständige Gruppe minimaler Größe:

```
K = arg min |G| subject to: G ist funktional vollständig
```

Für k = 5 Dimensionen: |K| ≥ 5 (Mindestgröße), praktisch |K| ∈ [5, 8] (moderate Diversität optimal nach Aggarwal & Woolley, 2019).

### 3.3 Liebigs Gesetz auf Gruppenzusammensetzung

Analog zu [Liebigs Minimumgesetz](https://en.wikipedia.org/wiki/Liebig%27s_law_of_the_minimum) (1840) — "Wachstum wird durch den knappsten Nährstoff begrenzt" — formulieren wir:

**Satz 1 (Dimensionales Minimum):** Die kollektive Intelligenz einer Keimzelle K wird durch die am schwächsten repräsentierte Dimension begrenzt:

```
CI(K) = f(min{rep(D₁), rep(D₂), ..., rep(Dₖ)})
```

wobei rep(Dᵢ) die Repräsentationstiefe der Dimension Dᵢ in der Gruppe ist.

**Konsequenz:** Fünf 5D-Denker bilden keine funktional vollständige Keimzelle. Fünf 1D-Überlebensexperten auch nicht. Die Mischung ist die Voraussetzung.

Dies verbindet Liebigs Minimumgesetz mit der multiplikativen IMP-Formel:

```
IMP_Keimzelle = Π rep(Dᵢ)     für i = 1, ..., k
```

Wenn eine Dimension nicht repräsentiert ist (rep(Dᵢ) = 0), fällt die gesamte kollektive Intelligenz auf Null. Die multiplikative Struktur ist hier nicht willkürlich — sie ist die formale Entsprechung von Liebigs Gesetz, angewandt auf kognitive statt biochemische Ressourcen.

**Kritische Nuance (2021):** [Tang & Riley (Ecological Applications, 2021)](https://doi.org/10.1002/eap.2458) zeigten, dass Liebigs Gesetz eine **grobe Approximation** des Massenwirkungsgesetzes ist. Genauere Modelle (Synthesizing Unit Model, Additives Modell) erklären Wachstum unter Co-Limitation besser. Das stützt den geplanten 4-Modell-Vergleich (Q2 2026) — auch auf Gruppenebene könnte ein Geometric Mean oder Synthesizing-Unit-Modell präziser sein als reine Multiplikation.

### 3.4 Zweistufige Perkolationsgleichung

**Stufe 1: Keimzellenbildung (lokal)**

```
K_vollständig = Π Θ(rep(Dᵢ))     für i = 1, ..., 5
```

K_vollständig = 1 genau dann, wenn jede Dimension mindestens einmal vertreten ist (Heaviside-Funktion: 1 wenn rep > 0, sonst 0).

**Stufe 2: Netzwerk-Perkolation (global)**

```
CI_global = Σⱼ CI(Kⱼ) · Θ(ρ_K − ρ_c(T))
```

wobei:
- ρ_K = Dichte der vernetzten Keimzellen (nicht Individuen)
- ρ_c(T) = topologieabhängiger Schwellenwert des Keimzellen-Netzwerks
- T = Netzwerktopologie (Clustering, Hub-Struktur, Manipulation)

**Kernunterschied zur alten Gleichung:**

| Eigenschaft | Alt | Neu |
|-------------|-----|-----|
| Einheit der Perkolation | Individuum | Keimzelle |
| Schwellenwert | fest (0,075) | variabel: ρ_c(T) |
| Dimensionsbedarf | nicht definiert | funktionale Vollständigkeit |
| Skalierung | linear (mehr authentische Individuen) | zweistufig (Keimzellen → Netzwerk) |

---

## 4. Nicht-Erzwingbarkeit als Systemeigenschaft

### 4.1 Das Erzwingbarkeits-Paradoxon

**Satz 2 (Nicht-Erzwingbarkeit):** Die Grundvoraussetzungen für funktionale Vollständigkeit — authentische Repräsentation der eigenen dominanten Dimension — können nicht extern erzwungen werden, weil Erzwingung die Authentizitäts-Dimension (Au) auf Null setzt, was die IMP-Formel auf Null setzt.

**Formal:**

```
Erzwingung → Au = 0 → IMP = A × IM × R × SP × 0 = 0
```

Das ist kein ethisches Argument. Das ist ein **mathematisches**: Die multiplikative Struktur macht Zwang selbst-destruktiv.

### 4.2 Verbindung zum Zwanglosigkeitsprinzip

Das [Zwanglosigkeitsprinzip](/03_philosophie_epistemologie/zwanglosigkeitsprinzip.md) im Repo formuliert empirisch:

> "Jedes System, das ohne menschlichen Eingriff entsteht und sich über evolutionäre Zeiträume erhält, organisiert sich zwanglos durch interne Kohärenz, nicht durch externe Steuerung."

Das Keimzellen-Theorem formalisiert dies: Keimzellen können nicht designed werden. Sie können nur **emergieren** — wenn die Bedingungen stimmen (minimales negatives Feld, Autonomie, Fehler als Signal, Authentizität, Partizipation = die 5 Prinzipien aus VISION.md).

### 4.3 Implikation für Manipulation

In einem manipulierten System (1D-Zwangsarchitektur) gilt:

```
ρ_c(T_manipuliert) >> ρ_c(T_natürlich)
```

**Weil:**
- Homogenisierung eliminiert funktionale Diversität → Keimzellen können nicht entstehen
- Kontrolle erzwingt Maskierung → Au sinkt → IMP sinkt → Knoten fallen unter Aktivierungsschwelle
- Clustering durch Algorithmen erzeugt Echokammern → Information bleibt lokal gefangen

**Numerische Illustration:**

| System | ρ_c geschätzt | Begründung |
|--------|---------------|------------|
| Zufallsnetzwerk (Erdős-Rényi) | 0,075 | Theoretisch, idealisiert |
| Natürliches heterogenes Netzwerk | 0,10–0,15 | Hubs senken ρ_c ([Newman, 2002](https://doi.org/10.1103/PhysRevLett.89.208701)) |
| Moderater sozialer Kontext | 0,20–0,27 | Empirischer Durchschnitt ([Everall et al., 2023](https://egusphere.copernicus.org/preprints/2023/egusphere-2023-2241/)) |
| Stark manipuliertes System | 0,30–0,43 | Obere empirische Grenze, hohe Homophilie + Clustering |

---

## 5. Empirische Verankerung

### 5.1 Woolley et al. (2010, 2021): Der c-Faktor

[Woolley et al. (2010, Science)](https://doi.org/10.1126/science.1193147) und die erweiterte Meta-Analyse [(2021, PNAS)](https://doi.org/10.1073/pnas.2005737118) mit 22 Studien (5.279 Individuen, 1.356 Gruppen) zeigten:

- Ein allgemeiner Faktor kollektiver Intelligenz (c) existiert — er erklärt 43–44% der Varianz in Gruppenleistung
- c korreliert **nicht** stark mit dem Durchschnitt oder Maximum der individuellen Intelligenz
- c korreliert mit: **Gleichheit der Gesprächsanteile**, **soziale Sensitivität** (Reading the Mind in the Eyes Test), **Anteil von Frauen** in der Gruppe
- **Gruppenprozess** (Kongruenz, Strategie, Effort) erklärt mehr Varianz in c als individuelle Fähigkeiten

**5D-Übersetzung:** Woolley zeigt, dass kollektive Intelligenz eine **emergente** Eigenschaft ist — nicht die Summe individueller Intelligenzen. Die Interaktionsqualität (3D: Empathie, 4D: Dezentrale Partizipation) dominiert über Einzelleistung. Das ist empirische Evidenz für das 5D-Dimensionsmodell auf Gruppenebene.

### 5.2 Aggarwal & Woolley (2019): Die umgekehrte U-Kurve

[Frontiers in Psychology](https://doi.org/10.3389/fpsyg.2019.00112), 98 Teams:

```
Kognitive Diversität → Kollektive Intelligenz: umgekehrt U-förmig (β = −0.91, p = 0.03)
```

**Interpretation:** Moderate Diversität = Maximum. Zu wenig → Redundanz, keine neuen Perspektiven. Zu viel → Koordinationskosten übersteigen Diversitätsgewinne.

**5D-Übersetzung:** Eine Keimzelle braucht 5 verschiedene Dimensionen — aber nicht 50 verschiedene Untervarianten. Funktionale Vollständigkeit ohne Überkomplexität. Das bestätigt |K| ∈ [5, 8] als optimale Keimzellengröße.

### 5.3 Hong & Page (2004): Diversität schlägt Fähigkeit

[PNAS](https://doi.org/10.1073/pnas.0403723101), Simulation + Theorem:

In der Simulation (Gruppen von 10 Agenten, Problemlösungsraum mit l = 2000 Punkten):
- Gruppe der 10 Besten: Score 97,3 (Diversitätsmaß: niedrig)
- Zufällig gewählte Gruppe von 10: Score 99,5 (Diversitätsmaß: hoch)

**Theorem (formal):** Unter den gegebenen Bedingungen konvergiert die Wahrscheinlichkeit, dass die diverse Zufallsgruppe die Elitegruppe übertrifft, gegen 1 für n → ∞.

**5D-Übersetzung:** Fünf "durchschnittliche" Menschen, jeder mit einer anderen dominanten Dimension, übertreffen fünf "brillante" Menschen mit derselben Dimension — weil die Elitegruppe im Problemraum redundant sucht.

---

## 6. Fernandez-Maße: Emergenz formalisiert

[Fernandez, Maldonado & Gershenson (2013)](https://doi.org/10.1002/cplx.21424) liefern die formale Sprache:

### 6.1 Emergenz einer Keimzelle

```
E(K) = H(Output_K) − H_shared(Output_K, Σ Outputs_individuell)
```

Hohe Emergenz = die Keimzelle generiert Lösungen, die kein Mitglied allein hätte generieren können. Das ist per Definition nur möglich bei funktionaler Vollständigkeit: verschiedene Perspektiven erzeugen neue Kombinationen.

### 6.2 Komplexität als Qualitätsmaß

```
C(K) = E(K) × SO(K)
```

Maximale Komplexität am **Edge of Chaos**: genug Diversität für Emergenz, genug Kohärenz für Selbstorganisation. Eine Keimzelle am Rand des Chaos ist das 5D-Äquivalent zum optimalen Punkt der umgekehrten U-Kurve (Aggarwal & Woolley, 2019).

### 6.3 Autopoiesis-Koeffizient

```
A_auto(K) = C(K) / C(Env)
```

Wenn A_auto > 1: Die Keimzelle ist komplexer als ihre Umgebung — sie kann ihre Umgebung aktiv gestalten (echte Autopoiesis, Transformation). Wenn A_auto < 1: Die Umgebung dominiert die Keimzelle — sie wird absorbiert.

**Implikation:** In einem 1D-Zwangssystem ist C(Env) künstlich niedrig (homogenisiert), aber die Kontrollmechanismen sind stark. Eine Keimzelle mit hohem C(K) hat A_auto >> 1, wird aber aktiv unterdrückt. Das ist der Mechanismus der Manipulation: nicht Komplexität der Umgebung, sondern **Erzwingung niedriger Komplexität**.

---

## 7. Gesamtformulierung

### 7.1 Vollständige zweistufige Gleichung

**Stufe 1 — Keimzellenbildung:**

```
CI_lokal(K) = [Π rep(Dᵢ)]^(1/k) × C(K) × A_auto(K)
```

wobei:
- `[Π rep(Dᵢ)]^(1/k)` = Geometric Mean der Dimensionsrepräsentation (entschärft Zero-Inflation, behält Weak-Link-Logik)
- `C(K)` = Fernandez-Komplexität (Emergenz × Selbstorganisation)
- `A_auto(K)` = Autopoiesis-Koeffizient

**Stufe 2 — Netzwerk-Perkolation:**

```
CI_global = Σⱼ CI_lokal(Kⱼ) · Θ(ρ_K − ρ_c(T))
```

wobei:
- `ρ_K` = Anteil funktional vollständiger und vernetzter Keimzellen
- `ρ_c(T)` = topologieabhängiger Schwellenwert: ρ_c ∈ [0,075 (ideal); 0,43 (manipuliert)]

### 7.2 Nicht-Erzwingbarkeits-Constraint

```
∀ Kⱼ: CI_lokal(Kⱼ) > 0 ⟹ Au(gᵢ) > 0 ∀ gᵢ ∈ Kⱼ
```

Erzwingung → Au = 0 → CI_lokal = 0. Die Gleichung schützt sich selbst vor Instrumentalisierung.

---

## 8. Schlussfolgerungskette

| # | Schlussfolgerung | Begründung | Status |
|---|-----------------|------------|--------|
| 1 | Feste Perkolationsschwellenwerte gelten nur in homogenen Netzwerken | Erdős-Rényi-Modell vs. reale Topologie; Newman 2002 | ✅ |
| 2 | Homogenität in menschlichen Systemen ist Artefakt von Manipulation | Einheitliche Curricula, Noten, Algorithmen eliminieren Varianz | ✅ Zwanglosigkeitsprinzip |
| 3 | In heterogenen Netzwerken ist ρ_c eine Funktion der Topologie, nicht eine Konstante | ρ_c ∈ [0,10; 0,43] empirisch; Everall et al. 2023 | ✅ |
| 4 | Kollektive Intelligenz emergiert nicht aus Masse, sondern aus funktionaler Diversität | Hong & Page 2004; Woolley et al. 2010, 2021 | ✅ |
| 5 | Funktionale Vollständigkeit = Mindestrepräsentation aller Dimensionen | Ashbys Gesetz der erforderlichen Varietät | ✅ |
| 6 | Optimale Diversität folgt einer umgekehrten U-Kurve | Aggarwal & Woolley 2019: moderate Diversität > maximale | ✅ |
| 7 | Die Einheit der Perkolation ist nicht das Individuum, sondern die funktional vollständige Keimzelle | Keimzellen-Theorem (neu) | ⚠️ Hypothese |
| 8 | Die multiplikative Struktur (Liebigs Gesetz) gilt für Keimzellen stärker als für Individuen | Fehlende Dimension = systemisches Versagen; Tang & Riley 2021: LLM ist Approximation | ⚠️ Hypothese, testbar |
| 9 | Nicht-Erzwingbarkeit ist keine ethische Präferenz, sondern mathematische Notwendigkeit | Au = 0 → IMP = 0 → CI = 0 in multiplikativer Struktur | ✅ (axiomatisch) |
| 10 | Manipulation erhöht ρ_c: Je mehr Zwang, desto mehr Menschen braucht es zum Kippen | Homogenisierung + Echokammern + Maskierung | ⚠️ Plausibel, empirisch unterstützt |

---

## 9. Offene Fragen und Testvorschläge

### 9.1 Empirisch testbar (Pilotstudien)

| Test | Design | n | Erwartung |
|------|--------|---|-----------|
| Keimzellen vs. homogene Gruppen | 10 Gruppen à 5–8, Dimensionsprofil messen, Problemlösungsaufgabe | 50–80 | Funktional vollständige Gruppen > homogene (d ≥ 0.50) |
| Umgekehrte U-Kurve replizieren | 20 Gruppen mit variierender Diversität, CI messen (Woolley-Methodik) | 100–160 | Peak bei moderater Diversität, Einbruch bei Überdiversität |
| ρ_c in verschieden manipulierten Kontexten | Agent-Based Simulation: variiere Homogenisierungsgrad, miss ρ_c | Simulation | ρ_c steigt monoton mit Manipulationsgrad |

### 9.2 Theoretisch offen

1. **Hysterese:** Gilt die zweistufige Gleichung symmetrisch für Aktivierung und Zerfall? Das Cron-Finding vom 27.03.2026 (Hysterese in growth-induced percolation) suggeriert: Nein. Separate Gleichungen für Aufbau und Erhalt könnten nötig sein.

2. **Geometric Mean vs. Multiplikativ vs. Synthesizing Unit auf Gruppenebene:** Tang & Riley (2021) zeigen, dass Liebigs Gesetz eine grobe Approximation ist. Der geplante 4-Modell-Vergleich (Q2 2026) sollte auch auf Gruppenebene durchgeführt werden.

3. **Dimensionsmessung:** Wie wird rep(Dᵢ) für ein Individuum operationalisiert? Aktuell keine validierte Skala. Der IMP-Survey (25 Items + SWLS) misst A, IM, R, SP, Au — aber nicht die dominante Dimension eines Individuums. Ein Dimensionsprofil-Instrument wird gebraucht.

4. **Conant-Ashby auf 5D:** Wenn jeder gute Regler ein Modell seines Systems sein muss — und das 5D-Framework ein Modell menschlicher Systeme ist — dann muss das Framework selbst alle 5 Dimensionen verkörpern. Tut es das? Oder ist es ein 5D-Modell, gebaut aus einer 2D/3D-Perspektive (Autodidakt, systemisch, aber einzeln)?

---

## 10. Zusammenfassung in einem Satz

**Das Keimzellen-Theorem:** Kollektive Intelligenz perkoliert nicht durch die Masse authentischer Individuen, sondern durch Netzwerke funktional vollständiger Kleingruppen — und diese können nicht erzwungen werden, weil Erzwingung die Authentizitätsdimension eliminiert, die ihre Existenz bedingt.

---

## Quellen

1. Ashby, W.R. (1956). *Introduction to Cybernetics.* Chapman & Hall.
2. Conant, R.C. & Ashby, W.R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science, 1*(2), 89–97. [DOI](https://doi.org/10.1080/00207727008920220)
3. Everall, J. et al. (2023). The Pareto effect in tipping social networks. *Earth System Dynamics.* [Preprint](https://egusphere.copernicus.org/preprints/2023/egusphere-2023-2241/)
4. Fernandez, N., Maldonado, C. & Gershenson, C. (2013). Information Measures of Complexity, Emergence, Self-organization, Homeostasis, and Autopoiesis. *Complexity, 19*(5). [DOI](https://doi.org/10.1002/cplx.21424)
5. Hong, L. & Page, S.E. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. *PNAS, 101*(46), 16385–16389. [DOI](https://doi.org/10.1073/pnas.0403723101)
6. Liebig, J. von (1840). *Die organische Chemie in ihrer Anwendung auf Agricultur und Physiologie.* Vieweg.
7. Newman, M.E.J. (2002). Spread of epidemic disease on networks. *Physical Review E, 66*, 016128. [DOI](https://doi.org/10.1103/PhysRevLett.89.208701)
8. Aggarwal, I. & Woolley, A.W. (2019). The Impact of Cognitive Style Diversity on Implicit Learning in Teams. *Frontiers in Psychology, 10*, 112. [DOI](https://doi.org/10.3389/fpsyg.2019.00112)
9. Tang, J. & Riley, W.J. (2021). Finding Liebig's law of the minimum. *Ecological Applications, 31*(8), e02458. [DOI](https://doi.org/10.1002/eap.2458)
10. Woolley, A.W. et al. (2010). Evidence for a Collective Intelligence Factor in the Performance of Human Groups. *Science, 330*(6004), 686–688. [DOI](https://doi.org/10.1126/science.1193147)
11. Woolley, A.W. et al. (2021). Quantifying collective intelligence in human groups. *PNAS, 118*(21), e2005737118. [DOI](https://doi.org/10.1073/pnas.2005737118)
12. PNAS Nexus (2025). Growth-induced percolation: Hysterese in activation vs. recovery. [Link](https://academic.oup.com/pnasnexus/article/4/6/pgaf192/8160299)

---

**Prepared:** 30.03.2026, 02:30–03:15 CET  
**Next:** Dimensionsprofil-Instrument entwerfen; Agent-Based Simulation für ρ_c(T)
