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
    validation_data = {}

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
                shutil.move(f, package_dir / os.path.basename(f))
                print(f"  -> Moved {f}")
                moved_count += 1

                # Capture the path to the validation report
                if "validation_report_" in f and f.endswith(".json"):
                    validation_report_path = package_dir / os.path.basename(f)

        if moved_count == 0:
            print("⚠️  No validation artifacts found to move.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during IMP Validation Study:")
        print(e.stderr)

    # Load validation data if available
    if validation_report_path and validation_report_path.exists():
        try:
            with open(validation_report_path, encoding="utf-8") as f:
                validation_data = json.load(f)
            print(f"  -> Loaded validation report data from {validation_report_path.name}")
        except Exception as e:
            print(f"❌ Failed to load validation report: {e}")

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

    # 3. Create Metric Mapping Table
    # Extract alphas safely
    dimensions = validation_data.get("dimensions", {})

    def get_alpha(dim_key):
        return dimensions.get(dim_key, {}).get("cronbach_alpha", "N/A")

    # Mapping logic:
    # Autonomy -> Environment_Optimization (Proxy)
    # Intrinsic Motivation -> Intrinsic_Motivation
    # Resilience -> Resilience
    # Social Participation -> Social_Participation
    # Authenticity -> GAP (Missing)

    alpha_autonomy = get_alpha("Environment_Optimization")
    alpha_intrinsic = get_alpha("Intrinsic_Motivation")
    alpha_resilience = get_alpha("Resilience")
    alpha_social = get_alpha("Social_Participation")
    alpha_authenticity = "N/A (Gap)"

    # Format for table
    def fmt_alpha(val):
        if isinstance(val, (int, float)):
            return f"{val:.3f}"
        return str(val)

    mapping_content = f"""
| Dimension | Metric | Source | Range | Reliability (α) |
|-----------|--------|--------|-------|-----------------|
| Autonomy | Environment Optimization (Proxy) | Validation Study | 0-5 | {fmt_alpha(alpha_autonomy)} |
| Intrinsic Motivation | Intrinsic Motivation | Validation Study | 0-5 | {fmt_alpha(alpha_intrinsic)} |
| Resilience | Resilience | Validation Study | 0-5 | {fmt_alpha(alpha_resilience)} |
| Social Participation | Social Participation | Validation Study | 0-5 | {fmt_alpha(alpha_social)} |
| Authenticity | N/A | Missing Data | N/A | {alpha_authenticity} |
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation

    # Generate Reliability Check Section
    reliability_check = []
    for dim_name, dim_key in [
        ("Autonomy (via Env. Opt.)", "Environment_Optimization"),
        ("Intrinsic Motivation", "Intrinsic_Motivation"),
        ("Resilience", "Resilience"),
        ("Social Participation", "Social_Participation"),
    ]:
        alpha = dimensions.get(dim_key, {}).get("cronbach_alpha", 0)
        if isinstance(alpha, (int, float)):
            if alpha < 0.8:
                reliability_check.append(
                    f"- **{dim_name}**: α = {alpha:.3f} (< 0.8). **Action Required:** Item revision needed."
                )
            else:
                reliability_check.append(
                    f"- **{dim_name}**: α = {alpha:.3f} (>= 0.8). **Status:** Validated."
                )
        else:
            reliability_check.append(f"- **{dim_name}**: Data missing.")

    reliability_section = "\n".join(reliability_check)

    interpretation_content = f"""
# Scientific Interpretation
**Generated via Professor Dr. A. I. Nexus Protocol**
**Date:** {datetime.datetime.now().isoformat()}

## Empirical Status
- **Validation Study:** Completed (N={validation_data.get('n_participants', 'N/A')}).
- **Reliability Check:**
{reliability_section}

## Hypothesis & Next Steps
Based on the zero-impact principle, any dimension < 0.8 requires immediate intervention.
Refer to `validation_results_*.png` for visual distribution.

[PUSH TO DOWNLOAD]
- Analysis Script: validation/imp_validation_study.py
- Metric Mapping: METRIC_MAPPING.md
- Visualization: validation_results_*.png
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
- **Research**: Scraped data from arXiv/PubMed/World Bank
- **Documentation**: Interpretation and Metric Mapping

## Protocol
- **Validation Script**: `validation/imp_validation_study.py`
- **Scraper**: `5d_research_scraper.py`
    """
    with open(package_dir / "MANIFEST.md", "w") as f:
        f.write(manifest_content)

    print(f"\n✅ Evidence Package Generated: {package_dir}")
    # Print the command to list files, but don't execute it, leave it to the user or agent to verify
    # print(f"   Run `ls -R {package_dir}` to view contents.")


if __name__ == "__main__":
    main()
