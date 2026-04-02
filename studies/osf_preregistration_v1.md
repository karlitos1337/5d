# OSF Preregistration

**Template:** OSF Preregistration (Standard)
**Version:** 1.0
**Date:** April 2, 2026
**OSF Project:** [To be assigned upon submission]

---

# The 5D-Framework: A Confirmatory Factor Analysis of the 25-Item IMP Scale and its Multiplicative Structure vs. Additive SDT Models

---

## A. Study Information

### Title

The 5D-Framework: A Confirmatory Factor Analysis of the 25-Item IMP Scale and its Multiplicative Structure vs. Additive SDT Models

### Authors

Karletz, P.

*Affiliation:* Independent Researcher
*Corresponding author:* pkarletz@gmail.com
*ORCID:* [To be registered]

### Description

#### Abstract

This preregistration documents the first confirmatory empirical test of the 5D-Framework and its associated psychometric instrument, the 25-Item Intrinsic Motivation Potential (IMP) Scale. The 5D-Framework proposes that human motivational potential is a function of five irreducible dimensions: Autonomy (A), Competence (C), Resonance (R), Participation (P), and Authenticity (Au). Critically, the framework departs from the additive logic underlying classical Self-Determination Theory (SDT; Deci & Ryan, 2000; Ryan & Deci, 2017) by positing a multiplicative relationship among these dimensions, formalized as:

**Φ_5D ∝ A · C · R · P · Au**

This multiplicative postulate—operationalized as a geometric mean to correct for scale differences—implies that a deficit in any single dimension produces a disproportionate suppression of overall motivational potential, rather than a linear offset compensable by high scores on the remaining dimensions. This constitutes an epistemological break with additive psychometric aggregation.

The framework is grounded in three theoretical pillars: (1) **Axiom 0**, which designates conscious self-interpretation and phenomenal experience (qualia) as the primary unit of psychological measurement—not behavioral proxies or physiological markers alone; (2) **Masking Entropy (E_mask)**, a theoretical construct describing the energetic and cognitive cost of self-concealment, suppression, and incongruence between authentic self-expression and performed social identity; and (3) an information-theoretic account of conscious integration (Tononi, 2004) that motivates the non-additive aggregation logic.

The present study pursues three pre-specified research hypotheses. **H1** tests the five-factor structure of the IMP Scale via confirmatory factor analysis (CFA). **H2** compares the predictive validity of multiplicative vs. additive IMP composites for life satisfaction (SWLS; Diener et al., 1985). **H3** examines convergent and discriminant validity of IMP subscales vis-à-vis the Big Five personality dimensions (Johnson, 2014). Neurobiological validation of the framework (e.g., HRV-based Axis C) is designated for a subsequent study requiring a clinical laboratory setting and is explicitly out of scope for the present investigation.

---

## B. Design Plan

### Study Type

Observational study (cross-sectional online survey). No experimental manipulation is administered.

### Blinding

No blinding is employed. This is not an intervention study; all participants respond to the same questionnaire battery.

### Study Design

A single-session, cross-sectional online survey is administered via the Prolific platform (prolific.com). Participants complete the following battery in a fixed block order (with within-scale item randomization as specified under Randomization):

1. Informed consent page
2. Demographic items (age, gender, education, occupational status)
3. 25-Item IMP Scale (block-randomized item order within each dimension)
4. Satisfaction with Life Scale (SWLS; Diener et al., 1985)
5. IPIP-NEO-120 (Johnson, 2014)
6. Debrief page with information about the 5D-Framework

The fixed block order is chosen to prevent the IMP Scale—the focal instrument—from being contaminated by Big Five priming effects. SWLS is placed before the IPIP-NEO-120 to minimize fatigue effects on the primary criterion variable.

### Randomization

Item order within each of the five IMP dimensions is randomized across participants to control for item-position carryover effects. The five-dimensional block structure is preserved (i.e., items from different dimensions are not interleaved) to maintain conceptual coherence and reduce respondent confusion in this first validation study. Future studies may test fully randomized presentation. No between-participants randomization of conditions is implemented.

---

## C. Sampling Plan

### Existing Data

No data have been collected prior to this preregistration. Data collection will commence only after the preregistration has been time-stamped and locked on OSF. Any pilot testing of survey functionality (n ≤ 5) conducted for technical checks will be discarded entirely and is not included in analyses.

### Explanation of Existing Data

Not applicable. This is a prospective study with no prior data.

### Data Collection Procedures

**Platform:** Prolific Academic (prolific.com), a validated crowdsourcing platform for behavioral research (Peer et al., 2022).

**Inclusion criteria:**
- Age 18 years or older
- Self-reported fluency in English (Prolific screener: "Fluent languages = English")
- Completion of informed consent

**Exclusion criteria (applied prior to analysis):**
1. Response time < 3 minutes for the full survey (flagged as insufficient engagement)
2. Straight-lining: Standard deviation of all 25 IMP items = 0 (all items answered identically)
3. Missing data > 20% of total item pool
4. Prolific attention check failure (one embedded attention-check item will be included: "Please select option 3 for this question")

**Compensation:** Participants will be compensated at Prolific's recommended rate (approximately £6.00/hour), estimated at approximately £1.50–£2.00 per participant given an expected completion time of 15–20 minutes. Total estimated budget: approximately €800 (≈ €2.00 × 400 participants, inclusive of platform fees).

**Survey administration:** Hosted on Qualtrics. All items will be presented in German (original language of the IMP Scale), with the demographic section and consent form also in German for the current validation sample. Future cross-cultural validation will require translation.

*Note on language:* The survey will be administered to a German-speaking Prolific sample (Prolific screener: "First language = German" or "Country of birth = Germany/Austria/Switzerland") rather than the initially specified English-speaking sample, given that the IMP items are currently validated in German. This specification supersedes the abstract reference to an English-language Prolific sample.

### Sample Size

**Target N = 400 complete, analyzable responses.**

### Sample Size Rationale

The target sample size is justified by two independent power analyses:

**For H1 (CFA):** Muthén and Muthén (2002) provide Monte Carlo simulation guidelines for SEM/CFA power estimation. For a second-order CFA model with 5 first-order factors (each with 5 indicators), testing close fit against RMSEA (H0: RMSEA ≤ 0.05 vs. H1: RMSEA = 0.08) at α = .05 with power = .95, the minimum required N lies in the range of 200–315 depending on factor loading magnitudes (assuming standardized loadings ≥ 0.45). N = 400 provides substantial buffer for:
- Anticipated exclusions (estimated 5–10% of recruited sample)
- Non-normality of Likert distributions (Curran et al., 2002), which inflates required N under Maximum Likelihood estimation
- Model modifications if the initially specified structure requires respecification in an exploratory follow-up

**For H2 (Hierarchical Regression):** Using G*Power 3.1 (Faul et al., 2007), for a linear multiple regression with 5 predictors, f² = 0.08 (medium effect size per Cohen, 1988), α = .05, power = .95 → required N ≈ 262. N = 400 exceeds this requirement and accommodates H3 correlation tests as well.

**For H3 (Correlations):** For a one-tailed test of r ≥ 0.30 (H0: r = 0) at α = .05/15 = .003 (Bonferroni-corrected), power = .80 → N ≈ 160. N = 400 ensures adequate power for all 15 a priori correlation tests simultaneously.

The proposed sample size of N = 400 satisfies all three requirements with adequate power margins.

### Stopping Rule

Data collection will terminate upon reaching **N = 400 valid, complete responses** or after **30 calendar days** from the opening of the Prolific study, whichever comes first. If N < 350 is reached at the 30-day mark, a one-time extension of 14 additional days will be implemented; this extension is pre-registered here to avoid post-hoc justification. The final analytic sample will consist of all valid responses available at the stopping point.

---

## D. Variables

### Measured Variables

#### 1. IMP Scale — Primary Instrument

The 25-Item Intrinsic Motivation Potential (IMP) Scale measures five theoretically distinct dimensions of motivational self-organization. All items are rated on a 5-point Likert scale:

> 1 = *Trifft gar nicht zu* (Does not apply at all) → 5 = *Trifft voll zu* (Fully applies)

The five dimensions and their indicators are:

- **Dimension 1 — Autonomy (A):** 5 items (2 reverse-coded)
- **Dimension 2 — Competence (C):** 5 items (2 reverse-coded)
- **Dimension 3 — Resonance (R):** 5 items (2 reverse-coded)
- **Dimension 4 — Participation (P):** 5 items (2 reverse-coded)
- **Dimension 5 — Authenticity (Au):** 5 items (1 reverse-coded)

Full item text and coding direction are provided in **Appendix A**.

#### 2. Satisfaction with Life Scale (SWLS)

The SWLS (Diener et al., 1985) is a 5-item self-report scale assessing global cognitive life satisfaction (e.g., "In most ways my life is close to my ideal"). Items are rated on a 7-point Likert scale (1 = *Strongly disagree* → 7 = *Strongly agree*). The SWLS has demonstrated robust psychometric properties across cultures, with Cronbach's α typically > .80 and test-retest reliability of r ≈ .82 over 4 weeks. It serves as the **primary criterion variable** for H2 (incremental predictive validity of the multiplicative IMP composite).

#### 3. IPIP-NEO-120

The 120-item public domain Big Five inventory (Johnson, 2014) measures the five major personality dimensions: Neuroticism (N), Extraversion (E), Openness to Experience (O), Agreeableness (A), and Conscientiousness (C). Each domain is assessed by 24 items, 12 keyed positively and 12 negatively, on a 5-point Likert scale (1 = *Very Inaccurate* → 5 = *Very Accurate*). This instrument is freely available and psychometrically well-characterized (Johnson, 2014). It serves as the **convergent/discriminant validity battery** for H3.

#### 4. Demographic Variables

The following variables are collected for descriptive purposes and potential moderation analyses:

- Age (continuous, years)
- Gender (categorical: male / female / non-binary / prefer not to say)
- Education level (ordinal: no degree / secondary school / vocational / bachelor's / master's / doctoral)
- Occupational status (categorical: employed full-time / part-time / self-employed / student / unemployed / retired)

### Indices

All index computation is performed after data quality screening and reverse-coding.

**Reverse-coding:** Items designated as (*) Reverse are recoded as:
> Score_reversed = 6 − Score_original

This transformation applies to: A2, A3, A5, C2, C5, R2, R5, P4, P5, Au4 (using the item labels defined in Appendix A).

#### Dimension Scores

Each of the five dimension scores is computed as the unweighted arithmetic mean of its five items (after reverse-coding):

> Score_A = Mean(A1_R, A2_R, A3_R, A4_R, A5_R)
> Score_C = Mean(C1_R, C2_R, C3_R, C4_R, C5_R)
> Score_R = Mean(R1_R, R2_R, R3_R, R4_R, R5_R)
> Score_P = Mean(P1_R, P2_R, P3_R, P4_R, P5_R)
> Score_Au = Mean(Au1_R, Au2_R, Au3_R, Au4_R, Au5_R)

Where subscript _R denotes the reverse-coded version for reversed items and the original score otherwise.

#### IMP Additive — SDT Analogue (3-Dimension)

> **IMP_Additive_SDT** = Mean(Score_A + Score_C + Score_R) / 3

This replicates the classical SDT aggregation of Basic Psychological Needs (Autonomy, Competence, Relatedness; Deci & Ryan, 2000), with Resonance substituted for Relatedness as the closest conceptual parallel. Serves as the baseline model in H2 (Model 1).

#### IMP Additive — Full 5D (5-Dimension)

> **IMP_Additive_5D** = Mean(Score_A + Score_C + Score_R + Score_P + Score_Au) / 5

This tests whether the two novel dimensions (Participation, Authenticity) add incremental predictive validity over the SDT analogue, under an additive aggregation assumption. Serves as Model 2 in H2.

#### IMP Multiplicative — 5D Geometric Mean

> **IMP_Multiplicative_5D** = (Score_A × Score_C × Score_R × Score_P × Score_Au)^(1/5)

The geometric mean is employed rather than the raw product to correct for scale magnitude differences and to maintain interpretability on the original 1–5 metric. This operationalizes the core theoretical postulate of the 5D-Framework (Φ_5D ∝ A·C·R·P·Au) while avoiding the statistical issues of unbounded products. Serves as Model 3 in H2.

*Rationale for geometric mean:* The geometric mean is mathematically equivalent to the arithmetic mean of log-transformed scores, which is the appropriate central tendency measure when the theoretical model is multiplicative (Aitchison, 1986). It produces a value of 1 (minimum) when any dimension approaches 1, and 5 (maximum) when all dimensions equal 5—identical bounds to the additive mean, facilitating direct comparison.

---

## E. Analysis Plan

All analyses are conducted in **R** (version ≥ 4.3.0) using the following primary packages: `lavaan` (≥ 0.6-17; Rosseel, 2012) for CFA/SEM, `semTools` for reliability indices, `mice` for multiple imputation, `psych` for descriptive statistics and alpha, `ggplot2` for visualization. Analysis scripts will be made publicly available on OSF and GitHub (github.com/karlitos1337/5d) prior to the start of data collection.

### Hypotheses

#### H1 — Construct Validity (CFA)

**H1a:** A five-factor oblique CFA model (25 items loading on 5 correlated first-order factors: A, C, R, P, Au) will demonstrate acceptable model fit.

**H1b:** A bifactor or second-order CFA model (5 first-order factors + 1 second-order factor IMP_Global) will demonstrate acceptable or superior fit compared to the five-factor oblique model.

**H1c:** All standardized factor loadings will be ≥ **0.40** (a priori threshold).

**H1d:** McDonald's Omega (ω) will be ≥ **0.70** for each of the five subscales.

#### H2 — Multiplicative > Additive (Incremental Predictive Validity)

**H2a:** The 5D additive composite (IMP_Additive_5D) will explain significantly more variance in SWLS than the 3-dimension SDT analogue (IMP_Additive_SDT): ΔR² > 0, p < .05.

**H2b:** The multiplicative composite (IMP_Multiplicative_5D) will explain significantly more variance in SWLS than the 5D additive composite (IMP_Additive_5D): ΔR² > 0, p < .05, and will yield lower AIC/BIC values.

#### H3 — Convergent and Discriminant Validity

**H3a — Convergent:** The following a priori Pearson correlations will each be r ≥ **0.30** (one-tailed, α_adj = .003 after Bonferroni correction for 15 tests):
- IMP-Autonomy ↔ IPIP-Openness to Experience
- IMP-Competence ↔ IPIP-Conscientiousness
- IMP-Resonance ↔ IPIP-Agreeableness
- IMP-Participation ↔ IPIP-Extraversion
- IMP-Authenticity ↔ IPIP-Neuroticism (reversed, i.e., r ≥ .30 with Neuroticism scored inversely)

**H3b — Discriminant:** No cross-construct correlation will exceed r = **0.70** (a priori threshold for construct collapse).

---

### Statistical Models

#### H1: Confirmatory Factor Analysis

A series of nested CFA models is tested in the following sequence:

**Model 0 (Null/Independence):** All items uncorrelated; serves as baseline for comparative fit indices.

**Model 1 (One-Factor):** All 25 items loading on a single general IMP factor.

**Model 2 (Five-Factor Oblique):** Items load on their theoretically designated factor; all five factors are permitted to correlate freely. This is the primary H1a model.

**Model 3 (Five-Factor Orthogonal):** As Model 2 but inter-factor correlations constrained to zero; tested as a more restrictive alternative.

**Model 4 (Second-Order):** Five first-order factors as in Model 2, with an additional second-order latent factor (IMP_Global) loading on all five first-order factors. This is the primary H1b model.

**Estimator:** Robust Maximum Likelihood (MLR; Yuan & Bentler, 2000) to handle non-normality of ordinal Likert responses. Diagonally weighted least squares (DWLS) will be used as a sensitivity analysis.

**A priori fit criteria (Hu & Bentler, 1999; Brown, 2015):**

| Index | Acceptable | Good |
|-------|-----------|------|
| CFI | ≥ **0.90** | ≥ **0.95** |
| TLI | ≥ **0.90** | ≥ **0.95** |
| RMSEA | ≤ **0.08** | ≤ **0.06** |
| SRMR | ≤ **0.08** | ≤ **0.06** |

Model comparisons will use χ² difference tests (Satorra-Bentler scaled), AIC, and BIC. In case of model misfit, post-hoc modification indices will be inspected but any resulting model changes will be explicitly labeled as **exploratory** and reported separately from the confirmatory tests.

**Reliability:** McDonald's Omega (ω) is computed via `semTools::reliability()` as the primary reliability index. Cronbach's α is reported as a supplementary index. The a priori threshold is **ω ≥ 0.70** per subscale.

#### H2: Hierarchical Multiple Regression

Criterion variable: Total SWLS score (sum of 5 items, range 5–35).

Three nested ordinary least squares regression models are estimated:

- **Model 1:** SWLS ~ IMP_Additive_SDT (1 predictor: the 3-dimension SDT analogue)
- **Model 2:** SWLS ~ IMP_Additive_5D (1 predictor: the 5-dimension additive composite)
- **Model 3:** SWLS ~ IMP_Multiplicative_5D (1 predictor: the geometric mean composite)

The hierarchical regression framework tests:
- H2a: ΔR² (Model 2 − Model 1) significance via F-change test
- H2b: ΔR² (Model 3 − Model 2) significance via F-change test; additionally compared via AIC and BIC

**Supplementary multiplicativity test:** To directly test whether the multiplicative structure improves on a fully specified additive model including all five dimension scores as separate predictors, an additional model is estimated:

- **Model 4 (Additive Full):** SWLS ~ Score_A + Score_C + Score_R + Score_P + Score_Au (5 predictors)
- **Model 5 (Multiplicative Full):** SWLS ~ IMP_Multiplicative_5D (replacing the five subscores with their geometric mean)

AIC and BIC comparisons between Model 4 and Model 5 constitute the supplementary multiplicativity test. Because these models are non-nested, Vuong's (1989) non-nested test will be applied.

**Assumption checks:** Normality of residuals (Shapiro-Wilk), homoscedasticity (Breusch-Pagan), multicollinearity (VIF < 10), and absence of influential outliers (Cook's D < 1) will be verified and reported.

#### H3: Convergent and Discriminant Validity

Pearson correlations are computed between all five IMP subscale scores and all five IPIP-NEO-120 domain scores, yielding a 5 × 5 correlation matrix. For Neuroticism, a reflected score (6 − Neuroticism) is used so that the predicted positive association with IMP-Authenticity is directionally consistent.

**A priori predictions (convergent):** Five specific on-diagonal correlations ≥ 0.30 (see H3a above).

**A priori predictions (discriminant):** All off-diagonal correlations < 0.70 (H3b).

**Multiple testing correction:** Bonferroni correction applied to the 15 unique correlation tests in the 5 × 5 matrix → α_adj = .05/15 = **.003**. Uncorrected p-values are also reported for transparency.

**Confidence intervals:** 95% bootstrap CIs (1,000 iterations) for all reported correlation coefficients.

---

### Transformations

1. **Reverse-coding:** Applied before any analysis. Items A2, A3, A5, C2, C5, R2, R5, P4, P5, Au4 are recoded as: Score_reversed = 6 − Score_original.

2. **Log-transformation:** Not planned a priori. If any dimension score or composite exhibits |skewness| > 2 or |kurtosis| > 7 (Curran et al., 2002), the MLR estimator in CFA inherently provides robust corrections. For regression analyses, log-transformation of the criterion will be implemented as a sensitivity analysis if residuals show marked non-normality.

3. **Standardization:** All regression predictors and outcomes will be reported as standardized (z-scored) coefficients in addition to unstandardized B coefficients.

### Inference Criteria

- **Alpha level:** α = .05 (two-tailed) for all primary confirmatory tests (H1, H2), unless otherwise specified.
- **Bonferroni correction for H3:** α_adj = .05/15 = .003 (one-tailed for directional H3a predictions).
- **Effect sizes reported:** Cohen's f² and R² for regression; Cohen's d for mean comparisons (if applicable); r and r² for correlations; RMSEA, CFI, SRMR for model fit.
- **No optional stopping:** The sample size is fixed a priori (see Stopping Rule). No analyses will be conducted on partial data during collection.

### Data Exclusion

Participants are excluded from all analyses if any of the following criteria are met (applied sequentially):

1. **Response time < 3 minutes** (< 180 seconds for the complete survey as recorded by Qualtrics)
2. **Straight-lining:** Standard deviation of the 25 IMP items = 0 (no variation in responding)
3. **Missing data > 20%** of the full item pool (> 29 items missing across the entire battery)
4. **Attention check failure:** Incorrect response to the embedded instructed-response item

The number of participants excluded by each criterion will be reported in a CONSORT-style flowchart.

### Missing Data

Missing data handling depends on the proportion of missingness:

- **< 5% missing** (at the item level, within the analytic sample after exclusions): **Multiple Imputation by Chained Equations (MICE)** using the `mice` package (van Buuren & Groothuis-Oudshoorn, 2011), with m = 20 imputed datasets, predictive mean matching for Likert items.

- **5–20% missing** (within the analytic sample): **Full Information Maximum Likelihood (FIML)** within the lavaan CFA framework (which handles item-level missingness directly under MLR). For regression analyses, MICE with m = 20 will be applied.

- **> 20% missing:** Participant excluded (see Data Exclusion criterion 3).

A **sensitivity analysis** comparing listwise deletion vs. MICE/FIML results will be reported for the primary H1 and H2 models if any missingness is observed.

### Exploratory Analyses

The following analyses are designated **exploratory** (not pre-specified for hypothesis testing) and will be reported as such, with no α-correction for familywise error:

**(a) Measurement Invariance (Multi-Group CFA):** Configural, metric, and scalar invariance of the IMP Scale across gender groups (male vs. female, if cell sizes ≥ 100) and age groups (< 35 vs. ≥ 35 years). Tested via χ² difference tests and ΔCFI (acceptable invariance: ΔCFI ≤ .010; Cheung & Rensvold, 2002).

**(b) Nonlinear SEM Path Model:** A structural equation model in which SWLS is regressed on a latent product term representing the full multiplicative combination of all five IMP dimensions. Given the complexity of latent interaction modeling, the Kenny-Judd product indicator approach or the unconstrained approach (Marsh et al., 2004) will be applied as appropriate.

**(c) Cluster Analysis:** K-means and hierarchical agglomerative clustering (Ward's method) on the five IMP dimension scores to identify motivational profiles (e.g., "high Autonomy, low Participation"). Cluster solutions k = 2 through k = 6 will be evaluated using the elbow criterion and Average Silhouette Width.

**(d) Masking Entropy Distribution:** The E_mask construct is operationalized as the absolute discrepancy between IMP-Authenticity score and the mean of the remaining four dimensions:

> E_mask = |Score_Au − Mean(Score_A, Score_C, Score_R, Score_P)|

Descriptive statistics and distribution of E_mask will be reported. Its relationship to SWLS will be examined via simple regression (exploratory).

**(e) Item Response Theory:** If time and scope permit, a graded response model (GRM) will be fitted to the 25 IMP items to examine item information functions and category threshold parameters. This analysis is exploratory and may be reported in a separate manuscript.

---

## F. Other

### Theoretical Scope and Axes

The present study constitutes **Axis A** validation of the 5D-Framework: psychometric and systems-theoretical operationalization of the five dimensions using self-report methodology. The 5D-Framework encompasses additional validation axes not addressed here:

- **Axis B (Behavioral/Ecological):** Experience sampling methodology tracking daily motivational fluctuations. A pre-designed **Zero-Tracking-Window (ZTW) Pilot Study** (quasi-experimental, n ≈ 40–60, 14-day suspension of formal assessment in parallel school classes, measuring RMSSD/HRV wearable data, IMP-Scale, and PSS-10) is planned as a separate subsequent study testing the hypothesis that removal of 1D coercive evaluation structures reduces physiological stress markers and increases IMP scores.
- **Axis C (Neurobiological):** Heart Rate Variability (HRV) and extended HRV (eHRV) indices as autonomic proxies for Authenticity and Competence; requires a controlled clinical/laboratory setting with physiological measurement apparatus (Porges, 2011).

Axes B and C validation are explicitly **out of scope** for the present study. References to neurobiological constructs (e.g., Polyvagal Theory; Porges, 2011) and the ZTW protocol appear in the theoretical background and the 5D-Framework's NotebookLM knowledge base (194 source documents; Karletz, 2026) but do not generate empirical hypotheses in this investigation.

### Nomenclature Note

The 5D-Framework has used variable labels interchangeably across development iterations. Specifically, the GitHub implementation (`models/imp.py`; Karletz, 2025) uses `A, IM, R, SP, Au` (where IM = Intrinsic Motivation, SP = Social Participation), whereas the present preregistration adopts the standardized labels `A, C, R, P, Au` (where C = Competence, P = Participation). These are identical constructs with updated nomenclature to align with SDT conventions and psychometric practice. This mapping is:

| Study Label | Code Label | Construct |
|------------|------------|----------|
| A | A | Autonomy |
| C | IM | Competence / Intrinsic Motivation |
| R | R | Resonance |
| P | SP | Participation / Social Participation |
| Au | Au | Authenticity |

### Theoretical Heritage: Thermodynamic Correspondence

The 5D-Framework draws on a formal correspondence between motivational dynamics and thermodynamic principles (detailed in the framework's 194-source knowledge base). The key correspondences are:

| 5D-Concept | Physical Principle | Implication |
|---|---|---|
| Authenticity | Entropic null-point | E_mask → 0; no metabolic maintenance cost |
| IMP numerator (A·C·R·P·Au) | Kinetic energy T (Lagrange) | Active motivational capacity |
| Systemzwang + Maskierungskosten | Potential energy V (Lagrange) | Resistive constraints |
| L = T − V | Principle of Least Action | System seeks authentic equilibrium |
| Network tipping point | Percolation theory | 25% critical threshold (Centola et al., 2018) |

These correspondences motivate the multiplicative structure but are not directly tested in this psychometric validation study. They are documented here for theoretical transparency and to guide future Axis B/C investigations.

### Ethics

This study involves an anonymous, non-deceptive online survey of healthy adults recruited through a commercial crowdsourcing platform. No sensitive personal data (clinical diagnoses, genetic information, financial data) are collected. Participation is voluntary and remunerated. Under the ethical guidelines of the Deutsche Gesellschaft für Psychologie (DGPs, 2016) and APA Ethics Code (2017), this type of study does not require independent ethics committee review. Nevertheless, the following safeguards are implemented:

- **Informed consent:** Full electronic informed consent is obtained before survey commencement; participants are clearly informed of their right to withdraw at any time without penalty
- **Anonymity:** No personally identifiable information is collected; Prolific participant IDs are stored separately and deleted after payment confirmation
- **Data security:** Survey data are stored on GDPR-compliant Qualtrics servers (EU datacenter)
- **Debrief:** A full debriefing page explaining the study's purpose is provided upon completion

### Open Science Practices

In accordance with open science principles (Munafò et al., 2017), the following materials will be made publicly available on OSF (osf.io) and GitHub (github.com/karlitos1337/5d) upon data collection completion, and no later than at the time of manuscript submission:

- Anonymized raw data (CSV format)
- Complete analysis scripts (R Markdown)
- Survey instrument (Qualtrics .qsf export)
- All codebooks and data dictionaries
- This preregistration document

Data will be released under a CC BY 4.0 license; code under MIT license.

### Conflict of Interest Statement

The first and corresponding author (Karletz, P.) is the sole developer of the 5D-Framework and the IMP Scale. This potential conflict of interest is openly declared here and will be disclosed in any resulting publications. To mitigate bias risk, the following measures are employed: (1) pre-registration of all hypotheses, thresholds, and analysis plans prior to data collection; (2) full public availability of data and analysis code; (3) transparent reporting of non-significant findings. External peer review of the manuscript is strongly encouraged.

---

## References

Aitchison, J. (1986). *The statistical analysis of compositional data*. Chapman & Hall.

American Psychological Association. (2017). *Ethical principles of psychologists and code of conduct* (2002, amended effective June 1, 2010, and January 1, 2017). https://www.apa.org/ethics/code

Brown, T. A. (2015). *Confirmatory factor analysis for applied research* (2nd ed.). Guilford Press.

Cheung, G. W., & Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. *Structural Equation Modeling, 9*(2), 233–255. https://doi.org/10.1207/S15328007SEM0902_5

Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

Curran, P. J., West, S. G., & Finch, J. F. (2002). The robustness of test statistics to nonnormality and specification error in confirmatory factor analysis. *Structural Equation Modeling, 9*(1), 1–28. https://doi.org/10.1207/s15328007sem0901_1

Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry, 11*(4), 227–268. https://doi.org/10.1207/S15327965PLI1104_01

Deutsche Gesellschaft für Psychologie (DGPs). (2016). *Berufsethische Richtlinien*. https://www.dgps.de

Diener, E., Emmons, R. A., Larsen, R. J., & Griffin, S. (1985). The Satisfaction with Life Scale. *Journal of Personality Assessment, 49*(1), 71–75. https://doi.org/10.1207/s15327752jpa4901_13

Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*(2), 175–191. https://doi.org/10.3758/BF03193146

Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes in covariance structure analysis: Conventional criteria versus new alternatives. *Structural Equation Modeling, 6*(1), 1–55. https://doi.org/10.1080/10705519909540118

Johnson, J. A. (2014). Measuring thirty facets of the Five Factor Model with a 120-item public domain inventory: Development of the IPIP-NEO-120. *Journal of Research in Personality, 51*, 78–89. https://doi.org/10.1016/j.jrp.2014.05.003

Marsh, H. W., Wen, Z., & Hau, K.-T. (2004). Structural equation models of latent interactions: Evaluation of alternative estimation strategies and indicator construction. *Psychological Methods, 9*(3), 275–300. https://doi.org/10.1037/1082-989X.9.3.275

Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., Percie du Sert, N., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., & Ioannidis, J. P. A. (2017). A manifesto for reproducible science. *Nature Human Behaviour, 1*, Article 0021. https://doi.org/10.1038/s41562-016-0021

Muthén, L. K., & Muthén, B. O. (2002). How to use a Monte Carlo study to decide on sample size and determine power. *Structural Equation Modeling, 9*(4), 599–620. https://doi.org/10.1207/S15328007SEM0904_8

Peer, E., Rothschild, D., Gordon, A., Evernden, Z., & Damer, E. (2022). Data quality of platforms and panels for online behavioral research. *Behavior Research Methods, 54*(4), 1643–1662. https://doi.org/10.3758/s13428-021-01694-3

Porges, S. W. (2011). *The polyvagal theory: Neurophysiological foundations of emotions, attachment, communication, and self-regulation*. Norton.

Rosseel, Y. (2012). lavaan: An R package for structural equation modeling. *Journal of Statistical Software, 48*(2), 1–36. https://doi.org/10.18637/jss.v048.i02

Ryan, R. M., & Deci, E. L. (2017). *Self-determination theory: Basic psychological needs in motivation, development, and wellness*. Guilford Press.

Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience, 5*, Article 42. https://doi.org/10.1186/1471-2202-5-42

van Buuren, S., & Groothuis-Oudshoorn, K. (2011). mice: Multivariate imputation by chained equations in R. *Journal of Statistical Software, 45*(3), 1–67. https://doi.org/10.18637/jss.v045.i03

Vuong, Q. H. (1989). Likelihood ratio tests for model selection and non-nested hypotheses. *Econometrica, 57*(2), 307–333. https://doi.org/10.2307/1912557

Yuan, K.-H., & Bentler, P. M. (2000). Three likelihood-based methods for mean and covariance structure analysis with nonnormal missing data. *Sociological Methodology, 30*(1), 165–200. https://doi.org/10.1111/0081-1750.00078

---

## Appendix A: 25-Item IMP Scale — Full Item List (English Translation)

The original IMP items are written and validated in German. The following English translations are provided for international readability; the German originals constitute the validated instrument used in the study.

**Response scale:** 1 = *Does not apply at all* — 2 = *Barely applies* — 3 = *Somewhat applies* — 4 = *Mostly applies* — 5 = *Fully applies*

Items marked with **(R)** are reverse-coded before analysis: Score_reversed = 6 − Score_original.

---

### Dimension 1: Autonomy (A)

| Item ID | Item Text (English) | German Original | Coding |
|---------|---------------------|-----------------|--------|
| A1_1D | "I largely determine for myself how I pursue my goals." | "Ich bestimme weitgehend selbst, wie ich meine Ziele verfolge." | Forward |
| A2_2D | "External rules and sanctions strongly determine my daily life." | "Externe Regeln und Sanktionen bestimmen meinen Alltag stark." | **(R)** |
| A3_3D | "I feel constrained by evaluation systems (grades / KPIs)." | "Ich fühle mich durch Bewertungssysteme (Noten/KPIs) eingeschränkt." | **(R)** |
| A4_4D | "My motivation comes primarily from within, not from outside." | "Meine Motivation kommt hauptsächlich von innen, nicht von außen." | Forward |
| A5_5D | "I am afraid of consequences when I deviate from prescribed guidelines." | "Ich habe Angst vor Konsequenzen bei Abweichung von Vorgaben." | **(R)** |

---

### Dimension 2: Competence (C)

| Item ID | Item Text (English) | German Original | Coding |
|---------|---------------------|-----------------|--------|
| C1_1D | "I am able to regulate my impulses well and maintain focus." | "Ich kann meine Impulse gut regulieren und fokussieren." | Forward |
| C2_2D | "Chronic stress severely impairs my concentration." | "Chronischer Stress beeinträchtigt meine Konzentration stark." | **(R)** |
| C3_3D | "My body feels energized and balanced." | "Mein Körper fühlt sich energiegeladen und ausgeglichen an." | Forward |
| C4_4D | "I recover quickly from setbacks." | "Ich erhole mich schnell von Rückschlägen." | Forward |
| C5_5D | "I often feel exhausted by inner conflicts." | "Ich spüre oft Erschöpfung durch innere Konflikte." | **(R)** |

---

### Dimension 3: Resonance (R)

| Item ID | Item Text (English) | German Original | Coding |
|---------|---------------------|-----------------|--------|
| R1_1D | "I can consciously adopt other people's perspectives." | "Ich kann mich bewusst in andere Perspektiven versetzen." | Forward |
| R2_2D | "I am often trapped in fixed roles or convictions." | "Ich bin oft in festen Rollen/Überzeugungen gefangen." | **(R)** |
| R3_3D | "I regularly reflect on my own narratives." | "Ich reflektiere regelmäßig meine eigenen Narrative." | Forward |
| R4_4D | "I resolve conflicts by shifting perspective." | "Konflikte löse ich durch Perspektivenwechsel." | Forward |
| R5_5D | "Emotional reactions often override my rational thinking." | "Emotionale Reaktionen überlagern oft mein rationales Denken." | **(R)** |

---

### Dimension 4: Participation (P)

| Item ID | Item Text (English) | German Original | Coding |
|---------|---------------------|-----------------|--------|
| P1_1D | "I cooperate horizontally with others without relying on hierarchy." | "Ich kooperiere horizontal mit anderen ohne Hierarchie." | Forward |
| P2_2D | "My network consists of trusting, authentic relationships." | "Mein Netzwerk besteht aus vertrauensvollen, authentischen Beziehungen." | Forward |
| P3_3D | "Ideas emerge spontaneously from group interactions." | "Ideen entstehen emergent aus Gruppeninteraktionen." | Forward |
| P4_4D | "Centralized decisions often block our progress." | "Zentrale Entscheidungen blockieren oft unseren Fortschritt." | **(R)** ¹ |
| P5_5D | "I feel isolated from potential allies." | "Ich fühle mich isoliert von potenziellen Verbündeten." | **(R)** |

¹ *Note:* P4 is coded as Forward in the original CSV but is treated as Reverse here based on theoretical content (agreement = constraint, not participation). This recoding decision is pre-registered and will be examined in a sensitivity analysis using the originally coded direction.

---

### Dimension 5: Authenticity (Au)

| Item ID | Item Text (English) | German Original | Coding |
|---------|---------------------|-----------------|--------|
| Au1_1D | "My actions feel congruent with my identity." | "Meine Handlungen fühlen sich kongruent mit meiner Identität an." | Forward |
| Au2_2D | "I frequently experience flow states without inner friction." | "Ich erlebe oft Flow-Zustände ohne innere Reibung." | Forward |
| Au3_3D | "My life has a clear, inner sense of meaning." | "Mein Leben hat eine klare, innere Sinnstiftung." | Forward |
| Au4_4D | "I mask parts of my personality to fit in." | "Ich maskiere Teile meiner Persönlichkeit, um zu passen." | **(R)** |
| Au5_5D | "I can 'sleep soundly' with my own decisions." | "Ich kann mit meinen Entscheidungen 'selbst schlafen'." | Forward |

---

## Appendix B: Hypotheses Summary Table

| Hypothesis | Description | A Priori Criterion | Analysis |
|-----------|-------------|-------------------|----------|
| **H1a** | Five-factor oblique CFA fits the IMP-25 | CFI ≥ .90, RMSEA ≤ .08, SRMR ≤ .08 | CFA (MLR) |
| **H1b** | Second-order CFA fits acceptably | CFI ≥ .90, RMSEA ≤ .08 | CFA (MLR) |
| **H1c** | All standardized loadings ≥ .40 | λ_std ≥ **.40** for all 25 items | CFA |
| **H1d** | Subscale reliability ω ≥ .70 | ω ≥ **.70** per dimension | semTools |
| **H2a** | 5D additive > 3D SDT additive (SWLS) | ΔR² > 0, p < .05 | Hierarchical OLS |
| **H2b** | 5D multiplicative > 5D additive (SWLS) | ΔR² > 0, p < .05; lower AIC/BIC | Hierarchical OLS + Vuong |
| **H3a** | 5 convergent validity correlations | r ≥ **.30**, p < .003 (Bonferroni) | Pearson correlation |
| **H3b** | Discriminant validity | All cross-correlations r < **.70** | Pearson correlation |

---

## Appendix C: R Code Skeleton for Primary Analyses

```r
# ============================================================
# 5D-Framework IMP Scale — Pre-specified Analysis Script
# OSF Preregistration v1.0 | Karletz, P. (2026)
# ============================================================

library(lavaan)
library(semTools)
library(mice)
library(psych)
library(ggplot2)
library(tidyverse)

# --- 1. DATA IMPORT & CLEANING ---
dat <- read.csv("imp_raw_data.csv")

# Attention check exclusion
dat <- dat %>% filter(attention_check == 3)

# Response time exclusion (< 180 seconds)
dat <- dat %>% filter(response_time_sec >= 180)

# Straight-lining exclusion (SD of IMP items = 0)
imp_items <- dat %>% select(starts_with("A"), starts_with("C"),
                             starts_with("R"), starts_with("P"),
                             starts_with("Au"))
dat$imp_sd <- apply(imp_items, 1, sd)
dat <- dat %>% filter(imp_sd > 0)

# Missing data exclusion (> 20% of full battery)
dat <- dat %>% filter(rowMeans(is.na(.)) <= 0.20)

# --- 2. REVERSE CODING ---
reverse_items <- c("A2_2D", "A3_3D", "A5_5D",
                   "C2_2D", "C5_5D",
                   "R2_2D", "R5_5D",
                   "P4_4D", "P5_5D",
                   "Au4_4D")
dat[reverse_items] <- 6 - dat[reverse_items]

# --- 3. COMPOSITE SCORES ---
dat$Score_A  <- rowMeans(dat[, c("A1_1D","A2_2D","A3_3D","A4_4D","A5_5D")], na.rm=TRUE)
dat$Score_C  <- rowMeans(dat[, c("C1_1D","C2_2D","C3_3D","C4_4D","C5_5D")], na.rm=TRUE)
dat$Score_R  <- rowMeans(dat[, c("R1_1D","R2_2D","R3_3D","R4_4D","R5_5D")], na.rm=TRUE)
dat$Score_P  <- rowMeans(dat[, c("P1_1D","P2_2D","P3_3D","P4_4D","P5_5D")], na.rm=TRUE)
dat$Score_Au <- rowMeans(dat[, c("Au1_1D","Au2_2D","Au3_3D","Au4_4D","Au5_5D")], na.rm=TRUE)

dat$IMP_Additive_SDT <- rowMeans(dat[, c("Score_A","Score_C","Score_R")])
dat$IMP_Additive_5D  <- rowMeans(dat[, c("Score_A","Score_C","Score_R","Score_P","Score_Au")])
dat$IMP_Multiplicative_5D <- (dat$Score_A * dat$Score_C * dat$Score_R *
                               dat$Score_P * dat$Score_Au)^(1/5)

dat$E_mask <- abs(dat$Score_Au - rowMeans(dat[, c("Score_A","Score_C","Score_R","Score_P")]))

# --- 4. CFA MODEL SPECIFICATION (H1) ---
model_5factor <- '
  Autonomy     =~ A1_1D + A2_2D + A3_3D + A4_4D + A5_5D
  Competence   =~ C1_1D + C2_2D + C3_3D + C4_4D + C5_5D
  Resonance    =~ R1_1D + R2_2D + R3_3D + R4_4D + R5_5D
  Participation =~ P1_1D + P2_2D + P3_3D + P4_4D + P5_5D
  Authenticity =~ Au1_1D + Au2_2D + Au3_3D + Au4_4D + Au5_5D
'

model_2ndorder <- '
  Autonomy     =~ A1_1D + A2_2D + A3_3D + A4_4D + A5_5D
  Competence   =~ C1_1D + C2_2D + C3_3D + C4_4D + C5_5D
  Resonance    =~ R1_1D + R2_2D + R3_3D + R4_4D + R5_5D
  Participation =~ P1_1D + P2_2D + P3_3D + P4_4D + P5_5D
  Authenticity =~ Au1_1D + Au2_2D + Au3_3D + Au4_4D + Au5_5D
  IMP_Global   =~ Autonomy + Competence + Resonance + Participation + Authenticity
'

fit_5factor <- cfa(model_5factor, data = dat, estimator = "MLR", missing = "fiml")
fit_2nd     <- cfa(model_2ndorder, data = dat, estimator = "MLR", missing = "fiml")

summary(fit_5factor, fit.measures = TRUE, standardized = TRUE)
summary(fit_2nd, fit.measures = TRUE, standardized = TRUE)

# Reliability
reliability(fit_5factor)

# --- 5. HIERARCHICAL REGRESSION (H2) ---
m1 <- lm(SWLS_total ~ IMP_Additive_SDT, data = dat)
m2 <- lm(SWLS_total ~ IMP_Additive_5D,  data = dat)
m3 <- lm(SWLS_total ~ IMP_Multiplicative_5D, data = dat)

anova(m1, m2)   # H2a: deltaR2 test
anova(m2, m3)   # H2b: deltaR2 test
AIC(m1, m2, m3)
BIC(m1, m2, m3)

# --- 6. CONVERGENT/DISCRIMINANT VALIDITY (H3) ---
imp_scores  <- dat[, c("Score_A","Score_C","Score_R","Score_P","Score_Au")]
ipip_scores <- dat[, c("IPIP_O","IPIP_C","IPIP_A","IPIP_E","IPIP_N_inv")]
cor_matrix  <- cor(imp_scores, ipip_scores, use = "pairwise.complete.obs")
print(cor_matrix)
# Bootstrap CIs via psych::corr.test
corr.test(imp_scores, ipip_scores, method = "pearson",
          adjust = "bonferroni", alpha = .05)
```

---

*Document prepared in accordance with OSF Preregistration Template standards. This preregistration will be time-stamped and locked on OSF prior to any data collection. Any deviations from this plan will be transparently reported in the resulting manuscript.*

*Preregistered: April 2, 2026 | OSF DOI: [To be assigned]*

*Knowledge base: 194 source documents in the 5D-Framework NotebookLM archive (Karletz, 2026). GitHub repository: https://github.com/karlitos1337/5d*
