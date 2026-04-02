# ============================================================================
# CFA Analysis: 5D-IMP Framework
# The 5D-Framework: Confirmatory Factor Analysis of the 25-Item IMP Scale
# and its Multiplicative Structure vs. Additive SDT Models
#
# Author: Karletz, P.
# Date: April 2026
# Repository: github.com/karlitos1337/5d
# OSF: [to be registered]
#
# NotebookLM Knowledge Base: 194 source documents
# (5D-Systemdynamik: Intelligence, Education, and Potential Theory)
#
# NOMENCLATURE BRIDGE (GitHub imp.py → Study Labels):
#   imp.py: A, IM, R, SP, Au  →  Study: A, C, R, P, Au
#   IM (Intrinsic Motivation) = C (Competence)
#   SP (Social Participation) = P (Participation)
#
# Preregistered decision criteria:
#   CFI/TLI >= .95 (Hu & Bentler, 1999)
#   RMSEA   <= .06 (Hu & Bentler, 1999)
#   SRMR    <= .08 (Hu & Bentler, 1999)
#   Chi-square difference p < .05 for nested model comparison
#   Bonferroni-corrected alpha for H3 validity correlations: .05/25 = .002
# ============================================================================


# ============================================================================
# 0. SETUP: REPRODUCIBILITY, PACKAGES, DIRECTORIES
# ============================================================================

set.seed(42)  # Ensure reproducibility for any random processes (e.g., MICE imputation)

# --- Package Installation & Loading ---
# Install missing packages automatically; CRAN mirror set for reproducibility.
required_packages <- c(
  "lavaan",    # Structural equation modeling (CFA core engine)
  "semTools",  # Reliability (McDonald's omega), measurement invariance helpers
  "dplyr",     # Data manipulation
  "tidyr",     # Data reshaping
  "psych",     # Descriptive stats, alpha, polychoric correlations
  "mice",      # Multiple imputation by chained equations (MAR handling)
  "ggplot2",   # Publication-quality visualizations
  "knitr",     # Table formatting for console/markdown reports
  "corrplot",  # Correlation matrix heatmaps
  "pwr",       # Power analysis
  "semPlot"    # Path diagrams for SEM/CFA models (optional, graceful fallback)
)

install_if_missing <- function(pkgs) {
  to_install <- pkgs[!sapply(pkgs, requireNamespace, quietly = TRUE)]
  if (length(to_install) > 0) {
    message("Installing missing packages: ", paste(to_install, collapse = ", "))
    install.packages(to_install, repos = "https://cloud.r-project.org")
  }
}
install_if_missing(required_packages)

# Load all required packages
suppressPackageStartupMessages({
  library(lavaan)
  library(semTools)
  library(dplyr)
  library(tidyr)
  library(psych)
  library(mice)
  library(ggplot2)
  library(knitr)
  library(corrplot)
  library(pwr)
})

# semPlot is optional — some systems lack the Rgraphviz dependency
semPlot_available <- requireNamespace("semPlot", quietly = TRUE)
if (semPlot_available) library(semPlot)

# --- Directory Structure ---
# Create output directories if they do not yet exist
dirs_to_create <- c("results", "results/figures", "results/tables")
invisible(lapply(dirs_to_create, function(d) {
  if (!dir.exists(d)) dir.create(d, recursive = TRUE)
}))

cat("============================================================\n")
cat("5D-IMP Framework — CFA Analysis Pipeline\n")
cat("Started:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
cat("R version:", R.version$version.string, "\n")
cat("lavaan version:", as.character(packageVersion("lavaan")), "\n")
cat("============================================================\n\n")


# ============================================================================
# 1. DATA IMPORT & CLEANING
# ============================================================================

cat("=== SECTION 1: Data Import & Cleaning ===\n")

# --- 1.1 Import ---
# Data file expected at data/5d_prolific_sample.csv (relative to working directory).
# Columns expected: participant_id, completion_time_minutes,
#   A1_1D ... Au5_5D (25 IMP items, 5-point Likert),
#   SWLS_1 ... SWLS_5 (7-point Likert),
#   NEO_N, NEO_E, NEO_O, NEO_A, NEO_C (Big Five domain scores).
data_path <- "data/5d_prolific_sample.csv"

if (!file.exists(data_path)) {
  stop(
    "Data file not found at: '", data_path, "'\n",
    "  Please place the Prolific export CSV at that path and re-run the script.\n",
    "  Expected columns: participant_id, completion_time_minutes, ",
    "A1_1D...Au5_5D, SWLS_1...SWLS_5, NEO_N, NEO_E, NEO_O, NEO_A, NEO_C"
  )
}

df_raw <- read.csv(data_path, stringsAsFactors = FALSE)
n_raw <- nrow(df_raw)
cat("Rows imported:", n_raw, "\n")

# --- 1.2 Define item vectors for convenience ---
items_autonomie      <- c("A1_1D",  "A2_2D",  "A3_3D",  "A4_4D",  "A5_5D")
items_kompetenz      <- c("C1_1D",  "C2_2D",  "C3_3D",  "C4_4D",  "C5_5D")
items_resonanz       <- c("R1_1D",  "R2_2D",  "R3_3D",  "R4_4D",  "R5_5D")
items_partizipation  <- c("P1_1D",  "P2_2D",  "P3_3D",  "P4_4D",  "P5_5D")
items_authentizitaet <- c("Au1_1D", "Au2_2D", "Au3_3D", "Au4_4D", "Au5_5D")
items_swls           <- paste0("SWLS_", 1:5)
items_neo            <- c("NEO_N", "NEO_E", "NEO_O", "NEO_A", "NEO_C")
items_imp_all        <- c(items_autonomie, items_kompetenz, items_resonanz,
                          items_partizipation, items_authentizitaet)
items_all            <- c(items_imp_all, items_swls, items_neo)

# --- 1.3 Exclusion Criteria ---
df <- df_raw  # working copy; df_raw preserved for audit trail

# Criterion 1: Completion time < 3 minutes (likely bots or inattentive respondents)
# 3-minute threshold: 25 IMP + 5 SWLS + 120 IPIP items → ~10 s/item minimum
exclude_time <- df$completion_time_minutes < 3
n_excl_time  <- sum(exclude_time, na.rm = TRUE)
cat("Excluded (completion time < 3 min):", n_excl_time, "\n")
df <- df[!exclude_time | is.na(exclude_time), ]

# Criterion 2: Straight-lining on IMP items (SD = 0 across all 25 items)
# Straight-lining indicates careless/random responding
row_sd_imp <- apply(df[, items_imp_all], 1, sd, na.rm = TRUE)
exclude_straight <- row_sd_imp == 0
n_excl_straight  <- sum(exclude_straight, na.rm = TRUE)
cat("Excluded (straight-lining, IMP SD = 0):", n_excl_straight, "\n")
df <- df[!exclude_straight | is.na(exclude_straight), ]

# Criterion 3: Missing > 20% of all scale items (IMP + SWLS + NEO)
# 20% threshold: pre-registered; > 20% missingness makes imputation unreliable
n_items_total <- length(items_all)
row_missing_pct <- rowMeans(is.na(df[, items_all[items_all %in% names(df)]]))
exclude_missing <- row_missing_pct > 0.20
n_excl_missing  <- sum(exclude_missing, na.rm = TRUE)
cat("Excluded (missing > 20% of items):", n_excl_missing, "\n")
df <- df[!exclude_missing | is.na(exclude_missing), ]

n_final <- nrow(df)
cat("\n--- Sample Summary ---\n")
cat("  N before exclusions:", n_raw, "\n")
cat("  N after exclusions: ", n_final, "\n")
cat("  Total excluded:     ", n_raw - n_final, "\n\n")

# Save cleaned-but-pre-imputed data for audit
write.csv(df, "results/tables/01_sample_after_exclusions.csv", row.names = FALSE)


# ============================================================================
# 2. REVERSE CODING
# ============================================================================

cat("=== SECTION 2: Reverse Coding ===\n")

# Items marked (*) in the preregistration are reverse-keyed.
# Formula for 5-point Likert: reversed = 6 - raw_score
# Affects: A2, A3, A5, C2, C5, R2, R5, P4, P5, Au4
reverse_cols <- c("A2_2D", "A3_3D", "A5_5D",
                  "C2_2D", "C5_5D",
                  "R2_2D", "R5_5D",
                  "P4_4D", "P5_5D",
                  "Au4_4D")

# Store originals as backup BEFORE transforming (data provenance)
for (col in reverse_cols) {
  if (col %in% names(df)) {
    df[[paste0(col, "_orig")]] <- df[[col]]
  } else {
    warning("Reverse-coded column not found in data: ", col)
  }
}

# Apply reverse coding
for (col in reverse_cols) {
  if (col %in% names(df)) {
    df[[col]] <- 6 - df[[col]]
    cat("  Reverse-coded:", col, "\n")
  }
}
cat("Reverse coding complete. Originals stored with '_orig' suffix.\n\n")


# ============================================================================
# 3. DESCRIPTIVE STATISTICS
# ============================================================================

cat("=== SECTION 3: Descriptive Statistics ===\n")

# --- 3.1 Item-level descriptives for all 25 IMP items ---
desc_list <- lapply(items_imp_all, function(item) {
  x <- df[[item]]
  data.frame(
    Item     = item,
    N        = sum(!is.na(x)),
    Mean     = round(mean(x, na.rm = TRUE), 3),
    SD       = round(sd(x, na.rm = TRUE), 3),
    Skewness = round(psych::skew(x, na.rm = TRUE), 3),
    Kurtosis = round(psych::kurtosi(x, na.rm = TRUE), 3),  # excess kurtosis
    stringsAsFactors = FALSE
  )
})
desc_table <- do.call(rbind, desc_list)

# Flag items that require MLR estimator due to non-normality
# Thresholds: |skew| > 2 or |excess kurtosis| > 7 (West et al., 1995)
desc_table$Flag_NonNormal <- ifelse(
  abs(desc_table$Skewness) > 2 | abs(desc_table$Kurtosis) > 7,
  "FLAG: MLR recommended", ""
)

cat("\n--- Item-Level Descriptives (25 IMP Items) ---\n")
print(knitr::kable(desc_table, format = "simple"))
write.csv(desc_table, "results/tables/03_item_descriptives.csv", row.names = FALSE)

n_flagged <- sum(desc_table$Flag_NonNormal != "")
cat("\nItems flagged for non-normality:", n_flagged,
    "(MLR estimator will be used regardless as a robust default)\n\n")

# --- 3.2 Correlation matrix heatmap of all 25 items ---
imp_cor_matrix <- cor(df[, items_imp_all], use = "pairwise.complete.obs")

pdf("results/figures/03_imp_correlation_heatmap.pdf", width = 10, height = 9)
corrplot(imp_cor_matrix,
         method   = "color",
         type     = "upper",
         order    = "original",
         tl.cex   = 0.75,
         tl.col   = "black",
         addCoef.col = "black",
         number.cex  = 0.5,
         col      = colorRampPalette(c("#2166AC", "white", "#D6604D"))(200),
         title    = "IMP Item Correlation Matrix (N = 25 items)",
         mar      = c(0, 0, 2, 0))
dev.off()
cat("Correlation heatmap saved to results/figures/03_imp_correlation_heatmap.pdf\n\n")


# ============================================================================
# 4. RELIABILITY ANALYSIS
# ============================================================================

cat("=== SECTION 4: Reliability Analysis ===\n")

# Define subscale item sets
subscales <- list(
  Autonomie      = items_autonomie,
  Kompetenz      = items_kompetenz,
  Resonanz       = items_resonanz,
  Partizipation  = items_partizipation,
  Authentizitaet = items_authentizitaet
)

# Initialize results containers
alpha_results <- data.frame()
itc_flags     <- data.frame()

for (subscale_name in names(subscales)) {
  items <- subscales[[subscale_name]]
  sub_data <- df[, items]

  cat("\n---", subscale_name, "---\n")

  # --- 4.1 Cronbach's Alpha (target: alpha >= .70) ---
  alpha_obj <- tryCatch(
    psych::alpha(sub_data, check.keys = FALSE),
    error = function(e) { cat("  Alpha error:", conditionMessage(e), "\n"); NULL }
  )

  if (!is.null(alpha_obj)) {
    alpha_val <- round(alpha_obj$total$raw_alpha, 3)
    cat("  Cronbach's alpha:", alpha_val,
        ifelse(alpha_val >= .70, "[OK]", "[BELOW .70 THRESHOLD]"), "\n")

    # Item-total correlations; flag if r_it < .30 (Nunnally & Bernstein, 1994)
    itc <- alpha_obj$item.stats[, "r.cor", drop = FALSE]
    itc_df <- data.frame(
      Subscale = subscale_name,
      Item     = rownames(itc),
      r_it     = round(itc[, "r.cor"], 3),
      Flag     = ifelse(itc[, "r.cor"] < .30, "FLAG: r_it < .30", "")
    )
    print(itc_df)
    itc_flags <- rbind(itc_flags, itc_df)

    alpha_row <- data.frame(
      Subscale       = subscale_name,
      Cronbach_alpha = alpha_val,
      Meets_threshold = alpha_val >= .70
    )
    alpha_results <- rbind(alpha_results, alpha_row)
  }
}

# --- 4.2 McDonald's Omega via semTools ---
# Omega requires a CFA model; we fit the first-order model per subscale
cat("\n--- McDonald's Omega (semTools::reliability) ---\n")

omega_results <- data.frame()

for (subscale_name in names(subscales)) {
  items <- subscales[[subscale_name]]
  model_str <- paste0(subscale_name, " =~ ", paste(items, collapse = " + "))

  fit_omega <- tryCatch(
    lavaan::cfa(model_str, data = df, estimator = "MLR"),
    error = function(e) {
      cat("  Omega model failed for", subscale_name, ":", conditionMessage(e), "\n")
      NULL
    }
  )

  if (!is.null(fit_omega) && lavaan::lavInspect(fit_omega, "converged")) {
    rel <- tryCatch(
      semTools::reliability(fit_omega),
      error = function(e) NULL
    )
    if (!is.null(rel)) {
      omega_val <- round(rel["omega", 1], 3)
      cat(" ", subscale_name, "omega =", omega_val, "\n")
      omega_results <- rbind(omega_results, data.frame(
        Subscale = subscale_name,
        Omega    = omega_val
      ))
    }
  }
}

# Merge and save reliability table
reliability_table <- merge(alpha_results, omega_results, by = "Subscale", all = TRUE)
write.csv(reliability_table, "results/tables/04_reliability.csv", row.names = FALSE)
write.csv(itc_flags,         "results/tables/04_item_total_correlations.csv", row.names = FALSE)
cat("\nReliability tables saved to results/tables/\n\n")


# ============================================================================
# 5. CFA MODEL SPECIFICATION
# ============================================================================

cat("=== SECTION 5: CFA Model Specification ===\n")

# All models use the same 25 IMP indicators.
# Estimator: MLR (Maximum Likelihood with Robust standard errors and Satorra-Bentler
# scaled test statistic) — appropriate for ordinal/non-normal data (Finney & DiStefano, 2006).
# Standard errors are robust to violations of multivariate normality.

# --- Model 1: First-Order 5-Factor CFA (Correlated Factors) ---
# Tests whether 5 correlated, distinct factors underlie the 25 items.
# This is the primary measurement model per preregistration.
imp_first_order <- '
  Autonomie      =~ A1_1D + A2_2D + A3_3D + A4_4D + A5_5D
  Kompetenz      =~ C1_1D + C2_2D + C3_3D + C4_4D + C5_5D
  Resonanz       =~ R1_1D + R2_2D + R3_3D + R4_4D + R5_5D
  Partizipation  =~ P1_1D + P2_2D + P3_3D + P4_4D + P5_5D
  Authentizitaet =~ Au1_1D + Au2_2D + Au3_3D + Au4_4D + Au5_5D
'

# --- Model 2: Second-Order CFA (IMP_Global) ---
# Tests whether a higher-order general IMP factor accounts for correlations
# among the five first-order factors. This mirrors the 5D-Framework's claim
# that A, C, R, P, Au are facets of a superordinate IMP construct.
imp_second_order <- '
  Autonomie      =~ A1_1D + A2_2D + A3_3D + A4_4D + A5_5D
  Kompetenz      =~ C1_1D + C2_2D + C3_3D + C4_4D + C5_5D
  Resonanz       =~ R1_1D + R2_2D + R3_3D + R4_4D + R5_5D
  Partizipation  =~ P1_1D + P2_2D + P3_3D + P4_4D + P5_5D
  Authentizitaet =~ Au1_1D + Au2_2D + Au3_3D + Au4_4D + Au5_5D

  IMP_Global =~ Autonomie + Kompetenz + Resonanz + Partizipation + Authentizitaet
'

# --- Model 3: Single-Factor (Null/Comparison Model) ---
# Worst-case alternative: all 25 items load on one general factor.
# Used as a baseline to show discriminant validity of the 5-factor solution.
imp_single_factor <- '
  IMP_General =~ A1_1D + A2_2D + A3_3D + A4_4D + A5_5D +
                 C1_1D + C2_2D + C3_3D + C4_4D + C5_5D +
                 R1_1D + R2_2D + R3_3D + R4_4D + R5_5D +
                 P1_1D + P2_2D + P3_3D + P4_4D + P5_5D +
                 Au1_1D + Au2_2D + Au3_3D + Au4_4D + Au5_5D
'

cat("Model syntax defined for:\n")
cat("  Model 1: First-order 5-factor CFA (correlated factors)\n")
cat("  Model 2: Second-order CFA (IMP_Global higher-order factor)\n")
cat("  Model 3: Single-factor null/comparison model\n\n")


# ============================================================================
# 6. CFA ESTIMATION & MODEL COMPARISON
# ============================================================================

cat("=== SECTION 6: CFA Estimation & Model Comparison ===\n\n")

# Shared CFA options
cfa_opts <- list(
  estimator = "MLR",   # Robust ML; handles non-normality of Likert data
  data      = df
)

# Helper: safely fit a CFA model with informative error messages
safe_cfa <- function(model_syntax, model_label, opts) {
  cat("Fitting:", model_label, "...\n")
  fit <- tryCatch(
    do.call(lavaan::cfa, c(list(model = model_syntax), opts)),
    error = function(e) {
      cat("  ERROR fitting", model_label, ":", conditionMessage(e), "\n")
      NULL
    }
  )
  if (!is.null(fit)) {
    conv <- lavaan::lavInspect(fit, "converged")
    cat("  Converged:", conv, "\n")
    if (!conv) {
      warning("Model '", model_label, "' did not converge. Inspect carefully.")
    }
  }
  fit
}

fit_m1 <- safe_cfa(imp_first_order,  "Model 1: First-order 5-factor",  cfa_opts)
fit_m2 <- safe_cfa(imp_second_order, "Model 2: Second-order IMP_Global", cfa_opts)
fit_m3 <- safe_cfa(imp_single_factor,"Model 3: Single-factor",          cfa_opts)

# --- 6.1 Extract Fit Indices ---
# Fit index extraction helper
extract_fit <- function(fit_obj, model_label) {
  if (is.null(fit_obj)) {
    return(data.frame(Model = model_label, ChiSq = NA, df = NA, p = NA,
                      CFI = NA, TLI = NA, RMSEA = NA,
                      RMSEA_CI_lo = NA, RMSEA_CI_hi = NA,
                      SRMR = NA, AIC = NA, BIC = NA))
  }
  fi <- lavaan::fitMeasures(fit_obj, c(
    "chisq.scaled", "df.scaled", "pvalue.scaled",
    "cfi.robust",   "tli.robust",
    "rmsea.robust", "rmsea.ci.lower.robust", "rmsea.ci.upper.robust",
    "srmr",
    "aic", "bic"
  ))
  data.frame(
    Model       = model_label,
    ChiSq       = round(fi["chisq.scaled"],           3),
    df          = fi["df.scaled"],
    p           = round(fi["pvalue.scaled"],           4),
    CFI         = round(fi["cfi.robust"],              3),
    TLI         = round(fi["tli.robust"],              3),
    RMSEA       = round(fi["rmsea.robust"],            3),
    RMSEA_CI_lo = round(fi["rmsea.ci.lower.robust"],   3),
    RMSEA_CI_hi = round(fi["rmsea.ci.upper.robust"],   3),
    SRMR        = round(fi["srmr"],                    3),
    AIC         = round(fi["aic"],                     1),
    BIC         = round(fi["bic"],                     1),
    row.names   = NULL
  )
}

fit_table <- rbind(
  extract_fit(fit_m1, "M1: 5-Factor First-Order"),
  extract_fit(fit_m2, "M2: Second-Order IMP_Global"),
  extract_fit(fit_m3, "M3: Single-Factor")
)

cat("\n--- CFA Fit Indices ---\n")
print(knitr::kable(fit_table, format = "simple"))

# Decision criteria annotation
cat("\nDecision Criteria (Hu & Bentler, 1999):\n")
cat("  CFI/TLI >= .95 | RMSEA <= .06 | SRMR <= .08\n")
cat("  Winning model: lowest AIC/BIC with acceptable absolute fit\n\n")

write.csv(fit_table, "results/tables/06_cfa_fit_indices.csv", row.names = FALSE)

# --- 6.2 Nested Model Chi-Square Difference Tests (Satorra-Bentler scaled) ---
cat("--- Chi-Square Difference Tests (Satorra-Bentler) ---\n")

# M1 vs M3: Does 5-factor solution fit better than single-factor?
lrt_m1_m3 <- tryCatch(
  lavaan::lavTestLRT(fit_m3, fit_m1),
  error = function(e) { cat("LRT M1 vs M3 failed:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(lrt_m1_m3)) {
  cat("M1 (5-factor) vs M3 (single-factor):\n")
  print(lrt_m1_m3)
}

# M2 vs M1: Does second-order factor fit as well as first-order?
lrt_m2_m1 <- tryCatch(
  lavaan::lavTestLRT(fit_m1, fit_m2),
  error = function(e) { cat("LRT M2 vs M1 failed:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(lrt_m2_m1)) {
  cat("\nM2 (second-order) vs M1 (first-order):\n")
  print(lrt_m2_m1)
}

# --- 6.3 Standardized Factor Loadings for Primary Model (M1) ---
cat("\n--- Standardized Factor Loadings: Model 1 (5-Factor First-Order) ---\n")
if (!is.null(fit_m1)) {
  std_loadings <- lavaan::standardizedSolution(fit_m1) %>%
    dplyr::filter(op == "=~") %>%
    dplyr::select(Latent = lhs, Item = rhs, Std_Loading = est.std, SE = se,
                  z = z, p = pvalue) %>%
    dplyr::mutate(across(c(Std_Loading, SE, z, p), ~ round(.x, 3)))
  print(knitr::kable(std_loadings, format = "simple"))
  write.csv(std_loadings, "results/tables/06_standardized_loadings_M1.csv", row.names = FALSE)

  # Flag weak loadings (< .40 is concerning; < .30 is critical)
  weak_loadings <- std_loadings %>% dplyr::filter(Std_Loading < .40)
  if (nrow(weak_loadings) > 0) {
    cat("\nWEAK LOADINGS (< .40):\n")
    print(weak_loadings)
  } else {
    cat("\nAll loadings >= .40 [OK]\n")
  }
}

# Inter-factor correlations (Model 1)
cat("\n--- Inter-Factor Correlations (Model 1) ---\n")
if (!is.null(fit_m1)) {
  factor_cors <- lavaan::standardizedSolution(fit_m1) %>%
    dplyr::filter(op == "~~", lhs != rhs,
                  lhs %in% c("Autonomie","Kompetenz","Resonanz","Partizipation","Authentizitaet"),
                  rhs %in% c("Autonomie","Kompetenz","Resonanz","Partizipation","Authentizitaet")) %>%
    dplyr::select(Factor1 = lhs, Factor2 = rhs, r = est.std) %>%
    dplyr::mutate(r = round(r, 3))
  print(knitr::kable(factor_cors, format = "simple"))
  write.csv(factor_cors, "results/tables/06_interfactor_correlations.csv", row.names = FALSE)
}
cat("\n")


# ============================================================================
# 7. H2 TEST: MULTIPLICATIVE vs. ADDITIVE STRUCTURE
# ============================================================================

cat("=== SECTION 7: H2 — Multiplicative vs. Additive IMP Structure ===\n\n")

# Preregistered hypothesis H2: The multiplicative (geometric mean) combination
# of the five IMP dimension scores predicts SWLS better than additive alternatives,
# consistent with the 5D-Framework's formula IMP ∝ A·C·R·P·Au.

# --- 7.1 Compute Dimension Scores (mean of 5 items per dimension) ---
df$A_score  <- rowMeans(df[, items_autonomie],      na.rm = TRUE)
df$C_score  <- rowMeans(df[, items_kompetenz],      na.rm = TRUE)
df$R_score  <- rowMeans(df[, items_resonanz],       na.rm = TRUE)
df$P_score  <- rowMeans(df[, items_partizipation],  na.rm = TRUE)
df$Au_score <- rowMeans(df[, items_authentizitaet], na.rm = TRUE)

# SWLS total score (mean across 5 items; 7-point Likert)
df$SWLS_total <- rowMeans(df[, items_swls], na.rm = TRUE)

# --- 7.2 Composite IMP Scores ---

# Additive SDT (traditional Need Satisfaction: Autonomy + Competence + Relatedness)
# Note: SDT uses "Relatedness" not "Resonanz" — Resonanz (R) is the closest analogue
df$IMP_add_SDT <- (df$A_score + df$C_score + df$R_score) / 3

# Additive 5D (arithmetic mean of all 5 dimensions)
df$IMP_add_5D <- (df$A_score + df$C_score + df$R_score + df$P_score + df$Au_score) / 5

# Multiplicative 5D (geometric mean — the 5D-Framework's core predictive claim)
# Geometric mean penalizes low scores on any single dimension (weak-link logic)
df$IMP_mult_5D <- (df$A_score * df$C_score * df$R_score * df$P_score * df$Au_score)^(1/5)

# Weak-link composite: minimum dimension score (bottleneck/constraint perspective)
df$IMP_min <- pmin(df$A_score, df$C_score, df$R_score, df$P_score, df$Au_score)

# --- 7.3 Descriptives for Composite Scores ---
composites_desc <- psych::describe(
  df[, c("A_score","C_score","R_score","P_score","Au_score",
         "SWLS_total","IMP_add_SDT","IMP_add_5D","IMP_mult_5D","IMP_min")]
)[, c("n","mean","sd","skew","kurtosis","min","max")]
cat("--- Descriptives: Dimension and Composite Scores ---\n")
print(round(composites_desc, 3))
write.csv(composites_desc, "results/tables/07_composite_descriptives.csv")

# --- 7.4 Hierarchical Regression Models ---
cat("\n--- Regression Models: SWLS ~ IMP composites ---\n")

# Remove rows with missing values on key variables for comparable model samples
h2_vars <- c("SWLS_total","A_score","C_score","R_score","P_score","Au_score",
              "IMP_add_SDT","IMP_add_5D","IMP_mult_5D","IMP_min")
df_h2 <- df[complete.cases(df[, h2_vars]), ]
cat("N for H2 regression (listwise):", nrow(df_h2), "\n\n")

model_sdt       <- lm(SWLS_total ~ IMP_add_SDT,   data = df_h2)
model_add       <- lm(SWLS_total ~ IMP_add_5D,    data = df_h2)
model_mult      <- lm(SWLS_total ~ IMP_mult_5D,   data = df_h2)
model_weaklink  <- lm(SWLS_total ~ IMP_min,        data = df_h2)
# Full interaction model: all 5 dimensions + all two-way through five-way interactions
# WARNING: This model has 2^5 - 1 = 31 terms and may be overfit with N=400
model_interaction <- lm(SWLS_total ~ A_score * C_score * R_score * P_score * Au_score,
                         data = df_h2)

# --- 7.5 Model Comparisons ---

cat("--- Nested Comparison: SDT (3D) vs. Additive 5D ---\n")
# Tests whether adding P and Au improves prediction beyond SDT's A+C+R
# Note: These models are nested (IMP_add_SDT is a restricted IMP_add_5D)
# We reformulate as nested lm for a proper F-test
model_sdt_raw  <- lm(SWLS_total ~ A_score + C_score + R_score,               data = df_h2)
model_add_raw  <- lm(SWLS_total ~ A_score + C_score + R_score + P_score + Au_score, data = df_h2)
nested_anova   <- anova(model_sdt_raw, model_add_raw)
print(nested_anova)

cat("\n--- AIC / BIC Comparison (all models) ---\n")
aic_table <- AIC(model_sdt, model_add, model_mult, model_weaklink, model_interaction)
bic_table <- BIC(model_sdt, model_add, model_mult, model_weaklink, model_interaction)
aic_bic   <- cbind(aic_table, BIC = bic_table$BIC)
rownames(aic_bic) <- c("SDT Additive (A+C+R)", "5D Additive (5 dims)",
                        "5D Multiplicative (GM)", "Weak-Link (Minimum)",
                        "Full Interaction (5-way)")
print(round(aic_bic, 2))
write.csv(aic_bic, "results/tables/07_aic_bic_comparison.csv")

# --- 7.6 R² Summary Table ---
cat("\n=== H2 Results: Multiplicative vs. Additive ===\n")
cat("SDT Additive (A+C+R):        R² =", round(summary(model_sdt)$r.squared,  4), "\n")
cat("5D Additive (A+C+R+P+Au):    R² =", round(summary(model_add)$r.squared,  4), "\n")
cat("5D Multiplicative (GM):      R² =", round(summary(model_mult)$r.squared, 4), "\n")
cat("Weak-Link (Minimum):         R² =", round(summary(model_weaklink)$r.squared, 4), "\n")
cat("Full Interaction (5-way):    R² =", round(summary(model_interaction)$r.squared, 4), "\n\n")

# Interpretation guide (pre-registered decision rule):
# If R²(multiplicative) > R²(additive_5D) AND delta-R² is practically meaningful (>= .01),
# this supports H2 (multiplicative structure). If not, H2 is not supported by this criterion.
r2_sdt  <- summary(model_sdt)$r.squared
r2_add  <- summary(model_add)$r.squared
r2_mult <- summary(model_mult)$r.squared
r2_wl   <- summary(model_weaklink)$r.squared

cat("Delta R² (5D-Mult vs 5D-Add):", round(r2_mult - r2_add, 4), "\n")
cat("H2 decision (pre-registered criterion: delta-R² >= .01):",
    ifelse(r2_mult - r2_add >= .01, "SUPPORTED", "NOT SUPPORTED"), "\n\n")

# Save R² table
r2_results <- data.frame(
  Model   = c("SDT_Additive","5D_Additive","5D_Multiplicative","Weak_Link","Full_Interaction"),
  R2      = round(c(r2_sdt, r2_add, r2_mult, r2_wl, summary(model_interaction)$r.squared), 4),
  Adj_R2  = round(c(summary(model_sdt)$adj.r.squared, summary(model_add)$adj.r.squared,
                    summary(model_mult)$adj.r.squared, summary(model_weaklink)$adj.r.squared,
                    summary(model_interaction)$adj.r.squared), 4)
)
write.csv(r2_results, "results/tables/07_r2_comparison.csv", row.names = FALSE)


# ============================================================================
# 8. H3 TEST: CONVERGENT & DISCRIMINANT VALIDITY
# ============================================================================

cat("=== SECTION 8: H3 — Convergent & Discriminant Validity ===\n\n")

# A priori directional hypotheses (preregistered, r >= .30):
#   Autonomie    <-> NEO_O  (autonomy associated with openness to experience)
#   Kompetenz    <-> NEO_C  (competence associated with conscientiousness)
#   Resonanz     <-> NEO_A  (resonance associated with agreeableness)
#   Partizipation<-> NEO_E  (participation associated with extraversion)
#   Authentizitaet <-> NEO_N (authenticity negatively associated with neuroticism)

imp_scores <- c("A_score","C_score","R_score","P_score","Au_score")
neo_scores <- c("NEO_N","NEO_E","NEO_O","NEO_A","NEO_C")

# Ensure all NEO columns exist
missing_neo <- neo_scores[!neo_scores %in% names(df)]
if (length(missing_neo) > 0) {
  warning("Missing NEO columns in dataset: ", paste(missing_neo, collapse = ", "),
          ". H3 analysis will be skipped.")
} else {
  # --- 8.1 Full 5×5 Validity Correlation Matrix ---
  validity_matrix <- cor(
    df[, imp_scores],
    df[, neo_scores],
    use = "pairwise.complete.obs"
  )
  rownames(validity_matrix) <- c("Autonomie","Kompetenz","Resonanz","Partizipation","Authentizitaet")
  colnames(validity_matrix) <- c("Neuroticism","Extraversion","Openness","Agreeableness","Conscientiousness")

  cat("--- 5x5 IMP × Big Five Correlation Matrix ---\n")
  print(round(validity_matrix, 3))
  write.csv(round(validity_matrix, 3), "results/tables/08_validity_matrix.csv")

  # --- 8.2 Targeted Hypothesis Tests with Bonferroni Correction ---
  # Bonferroni: alpha_adj = .05 / 25 = .002 (25 correlations in the 5×5 matrix)
  alpha_bonferroni <- .05 / 25  # = .002
  cat("\n--- A Priori Hypothesis Tests (Bonferroni-corrected alpha =",
      round(alpha_bonferroni, 4), ") ---\n")

  hypotheses <- list(
    list(imp = "A_score",  neo = "NEO_O", direction = "+", label = "Autonomie  <-> Openness"),
    list(imp = "C_score",  neo = "NEO_C", direction = "+", label = "Kompetenz  <-> Conscientiousness"),
    list(imp = "R_score",  neo = "NEO_A", direction = "+", label = "Resonanz   <-> Agreeableness"),
    list(imp = "P_score",  neo = "NEO_E", direction = "+", label = "Partizip.  <-> Extraversion"),
    list(imp = "Au_score", neo = "NEO_N", direction = "-", label = "Authentiz. <-> Neuroticism (neg.)")
  )

  hyp_results <- data.frame()
  for (h in hypotheses) {
    ct <- cor.test(df[[h$imp]], df[[h$neo]], alternative = "two.sided",
                   use = "pairwise.complete.obs")
    supported <- ifelse(
      ct$p.value < alpha_bonferroni,
      ifelse(h$direction == "+", ct$estimate > 0, ct$estimate < 0),
      FALSE
    )
    cat(sprintf("  %-40s r = %+.3f, p = %.4f, %s\n",
                h$label, ct$estimate, ct$p.value,
                ifelse(supported, "[SUPPORTED]", "[NOT SUPPORTED]")))
    hyp_results <- rbind(hyp_results, data.frame(
      Hypothesis  = h$label,
      r           = round(ct$estimate, 3),
      p           = round(ct$p.value,  4),
      CI_lo       = round(ct$conf.int[1], 3),
      CI_hi       = round(ct$conf.int[2], 3),
      Supported   = supported
    ))
  }
  write.csv(hyp_results, "results/tables/08_validity_hypotheses.csv", row.names = FALSE)
  cat("\n")
}


# ============================================================================
# 9. VISUALIZATION
# ============================================================================

cat("=== SECTION 9: Visualization ===\n")

# --- 9.1 Factor Loading Plot (Model 1: First-Order 5-Factor) ---
if (!is.null(fit_m1)) {
  std_load_plot <- lavaan::standardizedSolution(fit_m1) %>%
    dplyr::filter(op == "=~") %>%
    dplyr::mutate(
      Subscale = factor(lhs, levels = c("Autonomie","Kompetenz","Resonanz",
                                        "Partizipation","Authentizitaet")),
      Item     = factor(rhs, levels = rev(c(items_imp_all)))
    )

  p_loadings <- ggplot(std_load_plot, aes(x = est.std, y = Item, fill = Subscale)) +
    geom_col(width = 0.7) +
    geom_vline(xintercept = c(.40, .70), linetype = "dashed",
               color = c("#E69F00","#009E73"), linewidth = 0.5) +
    annotate("text", x = .40, y = 1.5, label = ".40", color = "#E69F00", size = 3) +
    annotate("text", x = .70, y = 1.5, label = ".70", color = "#009E73", size = 3) +
    scale_fill_manual(values = c("#0072B2","#E69F00","#009E73","#CC79A7","#D55E00")) +
    labs(
      title    = "Standardized Factor Loadings: 5D-IMP First-Order CFA",
      subtitle = "Dashed lines: .40 (minimum acceptable) and .70 (strong loading)",
      x        = "Standardized Loading (λ)",
      y        = "Item",
      fill     = "Subscale"
    ) +
    theme_minimal(base_size = 11) +
    theme(legend.position = "bottom")

  ggsave("results/figures/09_factor_loadings.pdf", plot = p_loadings,
         width = 9, height = 8)
  cat("Factor loading plot saved.\n")
}

# --- 9.2 Fit Index Comparison Table (bar chart style) ---
if (nrow(fit_table) > 0 && !all(is.na(fit_table$CFI))) {
  fit_long <- fit_table %>%
    dplyr::select(Model, CFI, TLI, RMSEA, SRMR) %>%
    tidyr::pivot_longer(cols = -Model, names_to = "Index", values_to = "Value") %>%
    dplyr::mutate(
      Threshold = dplyr::case_when(
        Index == "CFI"  ~ .95,
        Index == "TLI"  ~ .95,
        Index == "RMSEA"~ .06,
        Index == "SRMR" ~ .08
      )
    )

  p_fit <- ggplot(fit_long, aes(x = Model, y = Value, fill = Model)) +
    geom_col(width = 0.6, alpha = 0.85) +
    geom_hline(aes(yintercept = Threshold), linetype = "dashed",
               color = "red", linewidth = 0.6) +
    facet_wrap(~ Index, scales = "free_y", ncol = 2) +
    scale_fill_manual(values = c("#0072B2","#E69F00","#D55E00")) +
    labs(title = "CFA Fit Indices Across Three IMP Models",
         subtitle = "Red dashed line = decision threshold (Hu & Bentler, 1999)",
         x = NULL, y = "Fit Index Value") +
    theme_minimal(base_size = 10) +
    theme(axis.text.x = element_text(angle = 25, hjust = 1),
          legend.position = "none")

  ggsave("results/figures/09_fit_comparison.pdf", plot = p_fit, width = 9, height = 6)
  cat("Fit comparison plot saved.\n")
}

# --- 9.3 R² Comparison Bar Chart (H2 Models) ---
r2_plot_data <- data.frame(
  Model = c("SDT\nAdditive\n(A+C+R)",
            "5D\nAdditive\n(5 dims)",
            "5D\nMultiplicative\n(Geom. Mean)",
            "Weak-Link\n(Minimum)"),
  R2    = c(r2_sdt, r2_add, r2_mult, r2_wl)
)

p_r2 <- ggplot(r2_plot_data, aes(x = reorder(Model, -R2), y = R2,
                                   fill = Model == "5D\nMultiplicative\n(Geom. Mean)")) +
  geom_col(width = 0.6, alpha = 0.9) +
  geom_text(aes(label = round(R2, 3)), vjust = -0.4, size = 4) +
  scale_fill_manual(values = c("grey60", "#0072B2"), guide = "none") +
  scale_y_continuous(limits = c(0, max(r2_sdt, r2_add, r2_mult, r2_wl) * 1.20),
                     labels = scales::label_number(accuracy = .01)) +
  labs(
    title    = "Predictive Power of IMP Composites for Life Satisfaction (SWLS)",
    subtitle = "Highlighted bar = 5D multiplicative composite (H2 focal predictor)",
    x        = "IMP Composite Model",
    y        = expression(R^2)
  ) +
  theme_minimal(base_size = 12)

ggsave("results/figures/09_r2_comparison.pdf", plot = p_r2, width = 8, height = 5)
cat("R² comparison plot saved.\n")

# --- 9.4 Validity Correlation Heatmap (H3) ---
if (exists("validity_matrix")) {
  pdf("results/figures/09_validity_heatmap.pdf", width = 8, height = 6)
  corrplot(validity_matrix,
           method   = "color",
           type     = "full",
           tl.cex   = 0.85,
           tl.col   = "black",
           addCoef.col = "black",
           number.cex  = 0.8,
           col      = colorRampPalette(c("#2166AC","white","#D6604D"))(200),
           title    = "IMP Subscales × Big Five (H3 Validity Matrix)",
           mar      = c(0, 0, 2, 0))
  dev.off()
  cat("Validity heatmap saved.\n")
}

# --- 9.5 Path Diagram (Second-Order CFA) ---
if (semPlot_available && !is.null(fit_m2)) {
  pdf("results/figures/09_path_diagram_second_order.pdf", width = 12, height = 10)
  semPlot::semPaths(fit_m2,
                    what       = "std",       # standardized estimates
                    layout     = "tree2",
                    rotation   = 2,
                    edge.label.cex = 0.6,
                    node.label.cex = 0.7,
                    color      = list(lat = "#AED6F1", man = "#D5E8D4"),
                    title      = TRUE,
                    style      = "lisrel",
                    nCharNodes = 0)
  title("Second-Order CFA: IMP_Global", line = 3)
  dev.off()
  cat("Path diagram (second-order CFA) saved.\n")
} else if (!semPlot_available) {
  cat("semPlot not available — path diagram skipped. Install semPlot to enable.\n")
}
cat("\n")


# ============================================================================
# 10. POWER ANALYSIS (Post-hoc verification)
# ============================================================================

cat("=== SECTION 10: Power Analysis ===\n\n")

# --- 10.1 RMSEA-Based Power for CFA (MacCallum, Browne & Sugawara, 1996) ---
# Tests whether N=400 provides adequate power to reject a misspecified model.
#
# Degrees of freedom for Model 1 (5-factor first-order):
# df = p*(p+1)/2 - q
#   p = 25 observed variables
#   q = 25 loadings (1 fixed per factor) + 10 factor variances/covariances + 5 factor variances
#     = 25 free loadings (20 free, 5 fixed to 1) + 10 factor covariances + 25 residuals
# Standard formula: df = p*(p+1)/2 - (free parameters)
# For 5-factor, 25-indicator model with no cross-loadings:
#   Free parameters = 20 loadings + 10 factor covariances + 5 factor variances + 25 residual variances
#   = 60 parameters
#   df = 25*26/2 - 60 = 325 - 60 = 265
df_model1 <- 265  # Degrees of freedom for Model 1 (pre-calculated)
N_planned  <- 400  # Pre-registered target sample size

# Null hypothesis RMSEA (acceptable fit): H0: RMSEA <= .05
# Alternative hypothesis RMSEA (poor fit): H1: RMSEA >= .08
rmsea_null <- .05   # Close-fit hypothesis threshold
rmsea_alt  <- .08   # Not-close-fit threshold (MacCallum et al., 1996)

# Non-centrality parameters for chi-square distributions
ncp_null <- N_planned * df_model1 * rmsea_null^2
ncp_alt  <- N_planned * df_model1 * rmsea_alt^2

# Critical value at alpha = .05 (right tail of central chi-square)
crit_val_90 <- qchisq(.90, df = df_model1, ncp = ncp_null)

# Power = P(chi-square > critical value | H1 is true)
power_rmsea <- pchisq(crit_val_90, df = df_model1, ncp = ncp_alt, lower.tail = FALSE)

cat("--- RMSEA-Based CFA Power (MacCallum et al., 1996) ---\n")
cat("  Model 1 df:          ", df_model1, "\n")
cat("  N (planned):         ", N_planned, "\n")
cat("  H0: RMSEA <=",  rmsea_null, "(close fit)\n")
cat("  H1: RMSEA >=",  rmsea_alt,  "(not-close fit)\n")
cat("  Achieved power:      ", round(power_rmsea, 3), "\n")
cat("  Adequate (>= .80)?  ", ifelse(power_rmsea >= .80, "YES", "NO"), "\n\n")

# --- 10.2 Conventional Power for Regression (H2) ---
# Effect size f² for medium effect (Cohen, 1992): f² = .15
# Predictors: k = 5 (H2 regression with A, C, R, P, Au as separate predictors)
f2_medium <- .15
k_pred    <- 5

pwr_regression <- pwr::pwr.f2.test(
  u = k_pred,
  f2 = f2_medium,
  sig.level = .05,
  power = NULL,
  v = N_planned - k_pred - 1  # denominator df
)

cat("--- Conventional Regression Power (Cohen, 1992) ---\n")
cat("  N =", N_planned, ", k =", k_pred, "predictors\n")
cat("  Effect size f² = .15 (medium)\n")
cat("  Achieved power:", round(pwr_regression$power, 3), "\n")
cat("  Adequate (>= .80)?", ifelse(pwr_regression$power >= .80, "YES", "NO"), "\n\n")

# --- 10.3 Correlations (H3): Power for r >= .30 with Bonferroni correction ---
# Two-tailed, Bonferroni alpha = .002
pwr_cor <- pwr::pwr.r.test(
  r         = .30,
  n         = N_planned,
  sig.level = alpha_bonferroni,  # = .002 from Section 8
  alternative = "two.sided"
)
cat("--- Correlation Power (H3): r >= .30, Bonferroni alpha = .002 ---\n")
cat("  Achieved power:", round(pwr_cor$power, 3), "\n")
cat("  Adequate (>= .80)?", ifelse(pwr_cor$power >= .80, "YES", "NO"), "\n\n")

# Save power summary
power_summary <- data.frame(
  Analysis          = c("CFA (RMSEA-based)", "Regression (H2)", "Correlation (H3)"),
  N                 = N_planned,
  Achieved_Power    = round(c(power_rmsea, pwr_regression$power, pwr_cor$power), 3),
  Adequate_80pct    = c(power_rmsea >= .80, pwr_regression$power >= .80, pwr_cor$power >= .80)
)
write.csv(power_summary, "results/tables/10_power_analysis.csv", row.names = FALSE)
cat("Power summary saved to results/tables/10_power_analysis.csv\n\n")


# ============================================================================
# 11. OUTPUT & SUMMARY REPORT
# ============================================================================

cat("=== SECTION 11: Output & Reporting ===\n\n")

# --- 11.1 Save complete processed dataset ---
write.csv(df, "results/tables/00_processed_data.csv", row.names = FALSE)
cat("Processed dataset saved to results/tables/00_processed_data.csv\n")

# --- 11.2 Summary report printed to console (can be captured via sink()) ---
cat("\n")
cat("============================================================\n")
cat("  5D-IMP FRAMEWORK — CFA ANALYSIS SUMMARY REPORT\n")
cat("  Generated:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
cat("============================================================\n\n")

cat("SAMPLE\n")
cat("------\n")
cat("  N (raw):           ", n_raw, "\n")
cat("  N (after exclusions):", n_final, "\n\n")

cat("SECTION 4 — RELIABILITY\n")
cat("------------------------\n")
if (nrow(alpha_results) > 0) {
  for (i in seq_len(nrow(alpha_results))) {
    cat(sprintf("  %-16s alpha = %.3f %s\n",
                alpha_results$Subscale[i],
                alpha_results$Cronbach_alpha[i],
                ifelse(alpha_results$Meets_threshold[i], "[OK]", "[BELOW .70]")))
  }
}
cat("\n")

cat("SECTION 6 — CFA FIT\n")
cat("--------------------\n")
if (nrow(fit_table) > 0) {
  print(knitr::kable(
    fit_table[, c("Model","CFI","TLI","RMSEA","SRMR","AIC","BIC")],
    format = "simple"
  ))
}
cat("\n")

cat("SECTION 7 — H2 (Multiplicative vs. Additive)\n")
cat("----------------------------------------------\n")
cat(sprintf("  SDT Additive   (A+C+R):   R² = %.4f\n", r2_sdt))
cat(sprintf("  5D  Additive   (all 5):   R² = %.4f\n", r2_add))
cat(sprintf("  5D  Multiplicative (GM):  R² = %.4f\n", r2_mult))
cat(sprintf("  Weak-Link (Minimum):      R² = %.4f\n", r2_wl))
cat(sprintf("  Delta-R² (Mult - Add):    %.4f\n",      r2_mult - r2_add))
cat(sprintf("  H2 Decision:              %s\n",
            ifelse(r2_mult - r2_add >= .01, "SUPPORTED", "NOT SUPPORTED")))
cat("\n")

cat("SECTION 8 — H3 (Convergent/Discriminant Validity)\n")
cat("---------------------------------------------------\n")
if (exists("hyp_results") && nrow(hyp_results) > 0) {
  for (i in seq_len(nrow(hyp_results))) {
    cat(sprintf("  %-40s r = %+.3f, p = %.4f %s\n",
                hyp_results$Hypothesis[i],
                hyp_results$r[i],
                hyp_results$p[i],
                ifelse(hyp_results$Supported[i], "[SUPPORTED]", "[NOT SUPPORTED]")))
  }
} else {
  cat("  H3 results not available (missing NEO columns).\n")
}
cat("\n")

cat("SECTION 10 — POWER\n")
cat("-------------------\n")
for (i in seq_len(nrow(power_summary))) {
  cat(sprintf("  %-25s Power = %.3f %s\n",
              power_summary$Analysis[i],
              power_summary$Achieved_Power[i],
              ifelse(power_summary$Adequate_80pct[i], "[OK]", "[LOW]")))
}
cat("\n")

cat("OUTPUT FILES\n")
cat("------------\n")
cat("  results/tables/  — CSV tables (fit indices, loadings, reliability, validity)\n")
cat("  results/figures/ — PDF plots (loadings, fit comparison, R², heatmaps, path diagram)\n")
cat("\n")

# ============================================================================
# 12. EXPLORATORY: ETHICS COMPILER & PERCOLATION THRESHOLD
#     (From imp_v2.py and NotebookLM 5D-Systemdynamik archive)
# ============================================================================

cat("\n")
cat("=== SECTION 12: EXPLORATORY — Ethics Compiler & Percolation ===")
cat("\n\n")

# --- 12a. Ethics Compiler (adapted from imp_v2.py .min(axis=1) logic) ---
# The 5D-Framework's imp_v2.py includes an "ethics compiler" that sets
# Phi_5D = 0 if any dimension indicates coercion (score < threshold).
# We operationalize this as: if min(dimension scores) < 1.5 (bottom 10% of
# possible range on 1-5 Likert), the participant is flagged as "coerced".

coercion_threshold <- 1.5  # Exploratory threshold; not pre-registered
df$min_dimension <- pmin(df$A_score, df$C_score, df$R_score,
                          df$P_score, df$Au_score)
df$coerced_flag <- ifelse(df$min_dimension < coercion_threshold, 1, 0)

cat("Ethics Compiler Analysis:\n")
cat(sprintf("  Coercion threshold: %.1f (any dimension < %.1f)\n",
            coercion_threshold, coercion_threshold))
cat(sprintf("  N flagged as coerced: %d (%.1f%%)\n",
            sum(df$coerced_flag, na.rm = TRUE),
            100 * mean(df$coerced_flag, na.rm = TRUE)))

# Compare SWLS between coerced and non-coerced groups
if (sum(df$coerced_flag, na.rm = TRUE) >= 5) {
  t_ethics <- t.test(SWLS_total ~ coerced_flag, data = df)
  cat(sprintf("  SWLS coerced vs. non-coerced: t = %.2f, p = %.4f\n",
              t_ethics$statistic, t_ethics$p.value))
  cat(sprintf("  Mean SWLS (coerced): %.2f | Mean SWLS (non-coerced): %.2f\n",
              t_ethics$estimate[2], t_ethics$estimate[1]))
} else {
  cat("  Too few coerced cases for group comparison.\n")
}

# --- 12b. Percolation Threshold Analysis ---
# The 5D-Framework posits a critical percolation threshold (rho_c ≈ 0.075
# for network density; Centola et al., 2018 suggest ~25% for social tipping).
# We test whether there is a nonlinear breakpoint in the IMP-SWLS relationship.

percolation_threshold_5d <- 0.8  # From imp_v2.py: Phi_5D_Ethical > 0.8
# Normalize IMP_mult to [0,1] range for comparison
df$IMP_mult_norm <- (df$IMP_mult_5D - 1) / 4  # Rescale from [1,5] to [0,1]
df$above_percolation <- ifelse(df$IMP_mult_norm >= percolation_threshold_5d, 1, 0)

cat("\nPercolation Threshold Analysis (exploratory):\n")
cat(sprintf("  Threshold: IMP_mult_norm >= %.1f\n", percolation_threshold_5d))
cat(sprintf("  N above threshold: %d (%.1f%%)\n",
            sum(df$above_percolation, na.rm = TRUE),
            100 * mean(df$above_percolation, na.rm = TRUE)))

# Piecewise regression to detect breakpoint
tryCatch({
  # Simple segmented approach: compare R² of linear vs. two-segment model
  df$IMP_below <- ifelse(df$IMP_mult_norm < percolation_threshold_5d,
                          df$IMP_mult_norm, percolation_threshold_5d)
  df$IMP_above <- ifelse(df$IMP_mult_norm >= percolation_threshold_5d,
                          df$IMP_mult_norm - percolation_threshold_5d, 0)
  model_piecewise <- lm(SWLS_total ~ IMP_below + IMP_above, data = df)
  model_linear    <- lm(SWLS_total ~ IMP_mult_norm, data = df)

  cat(sprintf("  Linear model R²: %.4f\n", summary(model_linear)$r.squared))
  cat(sprintf("  Piecewise model R²: %.4f\n", summary(model_piecewise)$r.squared))
  cat(sprintf("  F-test p-value: %.4f\n", anova(model_linear, model_piecewise)$`Pr(>F)`[2]))
  cat("  NOTE: The 0.8 threshold from imp_v2.py is a 'magic number' that\n")
  cat("        requires empirical grounding. This analysis is exploratory.\n")
}, error = function(e) {
  cat("  Piecewise regression failed:", e$message, "\n")
})

cat("\n")

# ============================================================================
# 13. FINAL SUMMARY & SESSION INFO
# ============================================================================

cat("============================================================\n")
cat("Analysis complete:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n")
cat("Session info:\n")
print(sessionInfo())
cat("============================================================\n")
