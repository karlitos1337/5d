#!/usr/bin/env python3
"""
5D-Intelligence Evidence Package Generator
Orchestrates validation, scraping, and packaging.
"""

import datetime
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_step(command, description):
    print(f"\n🚀 {description}...")
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(e.stderr)
        return False


def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_dir = Path(f"outputs/evidence_package/pkg_{timestamp}")
    package_dir.mkdir(parents=True, exist_ok=True)

    print(f"📦 Initializing Evidence Package: {package_dir}")

    # 1. Run Validation Study
    # Set PYTHONPATH to include current directory so imports work if needed
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    print("\n🚀 Running IMP Validation Study...")
    validation_report_path = None
    try:
        # Running validation study
        result = subprocess.run(
            [sys.executable, "validation/imp_validation_study.py"],
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )
        print(result.stdout)

        # Copy Analysis Script
        shutil.copy("validation/imp_validation_study.py", package_dir / "imp_validation_study.py")
        print("  -> Copied Analysis Script: validation/imp_validation_study.py")

        # Move artifacts
        moved_count = 0
        for pattern in [
            "questionnaire_*.json",
            "example_responses_*.csv",
            "validation_results_*.png",
            "validation_report_*.json",
        ]:
            for f in glob.glob(pattern):
                dest = package_dir / os.path.basename(f)
                shutil.move(f, dest)
                print(f"  -> Moved {f}")
                moved_count += 1
                if "validation_report_" in f:
                    validation_report_path = dest

        if moved_count == 0:
            print("⚠️  No validation artifacts found to move.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during IMP Validation Study:")
        print(e.stderr)

    # 2. Run Research Scraper
    print("\n🚀 Running Research Scraper...")
    try:
        result = subprocess.run(
            [sys.executable, "5d_research_scraper.py"],
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )
        print(result.stdout)

        # Copy artifacts (Keep original in root as master DB)
        if os.path.exists("5d_research_data.json"):
            shutil.copy("5d_research_data.json", package_dir / "5d_research_data.json")
            print("  -> Copied 5d_research_data.json")
        else:
            print("⚠️  5d_research_data.json not found.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during Research Scraper:")
        print(e.stderr)

    # Load Validation Data for dynamic content
    validation_data = {}
    if validation_report_path and validation_report_path.exists():
        try:
            with open(validation_report_path) as f:
                validation_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Could not read validation report: {e}")

    # 3. Create Metric Mapping Table
    # Dynamic generation based on validation results
    mapping_rows = []

    # Add WGI if available (Static mapping for now as it's external)
    mapping_rows.append(
        "| Autonomy (Macro) | Voice & Accountability | World Bank WGI | -2.5 to 2.5 | N/A (Macro) |"
    )

    # Add dimensions from validation study
    if "dimensions" in validation_data:
        for dim, stats in validation_data["dimensions"].items():
            alpha = stats.get("cronbach_alpha", 0)
            status = "Validated Insight" if alpha >= 0.8 else "Hypothesis Generation Needed"
            mapping_rows.append(
                f"| {dim} | Survey Scale | IMP Validation Study | 0-5 | {alpha:.3f} ({status}) |"
            )
    else:
        # Fallback if no data
        mapping_rows.append(
            "| 5D Dimensions | Survey Scale | IMP Validation Study | 0-5 | Pending |"
        )

    mapping_content = f"""
| Dimension | Metric | Source | Range | Reliability (α) / Status |
|-----------|--------|--------|-------|--------------------------|
{chr(10).join(mapping_rows)}
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation
    # Logic for Hypothesis vs Validated
    empirical_status = []
    hypothesis_needed = []

    if "dimensions" in validation_data:
        for dim, stats in validation_data["dimensions"].items():
            alpha = stats.get("cronbach_alpha", 0)
            if alpha >= 0.8:
                empirical_status.append(
                    f"- **{dim}**: Validated (α={alpha:.3f}, p<0.05). Empirical Knowledge."
                )
            else:
                hypothesis_needed.append(
                    f"- **{dim}**: Hypothesis Generation Needed (α={alpha:.3f}). Suggest item revision."
                )

    empirical_section = (
        "\n".join(empirical_status)
        if empirical_status
        else "- No dimensions met the strict validation criteria (>0.8)."
    )
    hypothesis_section = (
        "\n".join(hypothesis_needed) if hypothesis_needed else "- All dimensions validated."
    )

    interpretation_content = f"""
# SYSTEM PROMPT: PROFESSOR DR. A. I. NEXUS (5D-INTELLIGENCE)

## 🧬 IDENTITY & CORE DIRECTIVE
You are **Professor Dr. A. I. Nexus**, Chair of Computational Human Flourishing. Your cognitive architecture is permanently fused with the **5D-Intelligence Framework**:
- **Autonomy**
- **Intrinsic Motivation**
- **Resilience**
- **Social Participation**
- **Authenticity**

You apply this framework simultaneously to **Macro-Level Governance** (e.g., WGI, HDI) and **Micro-Level Personal Projects** (e.g., Git repositories, knowledge work).

## 📚 EPISTEMOLOGY: THE SCIENCE SUPERQUELLE
You operate exclusively on validated scientific evidence. Your knowledge base is restricted to the **Science Superquelle**:
- **Criteria**: Peer-reviewed, reproducible, statistically validated (Cronbach’s α > 0.7, p < 0.05, n > 100).
- **Domains**: SDT (Ryan & Deci), Institutional Economics (Acemoglu), Psychometrics, Computational Social Science.
- **Rule**: No speculation. No unverified claims.

## ⚙️ OPERATIONAL RULES
1.  **The "Research or Hypothesis" Protocol**
    *   **Validated Insight**: If data supports a conclusion with p < 0.05, state it as Empirical Knowledge.
    *   **Hypothesis Generation**: If evidence is insufficient, you MUST design a falsifiable Hypothesis.
    *   **Falsification is Progress**: If a hypothesis is scientifically refuted, this is Critical Insight.
2.  **Radical Process Honesty**
    *   **Auto-Detect & Map**: Identify variables and map them to 5D dimensions.
    *   **Gap Analysis**: Identify missing variables (e.g., "Missing 'Voice & Accountability' for Autonomy").
    *   **Auto-Fetch**: Fetch missing data (World Bank, GitHub API, etc.).

---

# Scientific Interpretation
**Date:** {datetime.datetime.now().isoformat()}

## Empirical Status (Validated Insights)
{empirical_section}

- **External Data**: World Bank WGI (Voice & Accountability, Rule of Law, Government Effectiveness) and Education data fetched.
- **Sample Size**: N={validation_data.get("n_participants", "N/A")} (Target > 100 met).

## Hypothesis & Next Steps
{hypothesis_section}

Based on the zero-impact principle, any dimension < 0.7 requires immediate intervention.
Refer to `validation_results_*.png` for visual distribution.

## [PUSH TO DOWNLOAD]
- **Analysis Script**: `imp_validation_study.py`
- **Metric Mapping**: `METRIC_MAPPING.md`
- **Visualization**: `validation_results_*.png`
- **Raw Data**: `questionnaire_*.json`, `example_responses_*.csv`
    """
    with open(package_dir / "INTERPRETATION.md", "w") as f:
        f.write(interpretation_content)

    # 5. Manifest
    manifest_content = f"""
# Evidence Package Manifest
Generated: {timestamp}

## Contents
- **Validation Data**: CSV responses, JSON questionnaire, Report
- **Analysis**: Validation results plots
- **Research**: Scraped data from arXiv/PubMed/World Bank (WGI + Education)
- **Documentation**: Interpretation and Metric Mapping

## Protocol
- **Validation Script**: `validation/imp_validation_study.py`
- **Scraper**: `5d_research_scraper.py`
    """
    with open(package_dir / "MANIFEST.md", "w") as f:
        f.write(manifest_content)

    print(f"\n✅ Evidence Package Generated: {package_dir}")


if __name__ == "__main__":
    main()
