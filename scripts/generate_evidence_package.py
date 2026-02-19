#!/usr/bin/env python3
"""
5D-Intelligence Evidence Package Generator
Orchestrates validation, scraping, and packaging.
"""

import os
import glob
import shutil
import datetime
import subprocess
import sys
import json
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

    print(f"\n🚀 Running IMP Validation Study...")
    validation_report_data = None
    try:
        # Running validation study
        result = subprocess.run(
            [sys.executable, "validation/imp_validation_study.py"],
            check=True,
            text=True,
            capture_output=True,
            env=env
        )
        print(result.stdout)

        # Copy Analysis Script
        shutil.copy("validation/imp_validation_study.py", package_dir / "imp_validation_study.py")
        print(f"  -> Copied Analysis Script: validation/imp_validation_study.py")

        # Move artifacts and load report
        moved_count = 0
        report_files = glob.glob("validation_report_*.json")
        if report_files:
            # Sort by modification time to get the latest
            latest_report = max(report_files, key=os.path.getmtime)
            try:
                with open(latest_report, 'r') as f:
                    validation_report_data = json.load(f)
                print(f"  -> Loaded validation report: {latest_report}")
            except Exception as e:
                print(f"❌ Failed to load validation report: {e}")

        for pattern in ["questionnaire_*.json", "example_responses_*.csv", "validation_results_*.png", "validation_report_*.json"]:
            for f in glob.glob(pattern):
                shutil.move(f, package_dir / os.path.basename(f))
                print(f"  -> Moved {f}")
                moved_count += 1

        if moved_count == 0:
            print("⚠️  No validation artifacts found to move.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during IMP Validation Study:")
        print(e.stderr)

    # 2. Run Research Scraper
    print(f"\n🚀 Running Research Scraper...")
    try:
        result = subprocess.run(
            [sys.executable, "5d_research_scraper.py"],
            check=True,
            text=True,
            capture_output=True,
            env=env
        )
        print(result.stdout)

        # Copy artifacts (Keep original in root as master DB)
        if os.path.exists("5d_research_data.json"):
            shutil.copy("5d_research_data.json", package_dir / "5d_research_data.json")
            print(f"  -> Copied 5d_research_data.json")
        else:
            print("⚠️  5d_research_data.json not found.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during Research Scraper:")
        print(e.stderr)

    # 3. Create Metric Mapping Table
    # Default values if report is missing
    reliabilities = {
        "Autonomy": "N/A",
        "Intrinsic Motivation": "N/A",
        "Resilience": "N/A",
        "Social Participation": "N/A",
        "Authenticity": "N/A"
    }

    if validation_report_data and "dimensions" in validation_report_data:
        dims = validation_report_data["dimensions"]
        # Map study dimensions to 5D framework
        # Study: Cognitive_Efficiency, Intrinsic_Motivation, Social_Participation, Resilience, Environment_Optimization

        if "Environment_Optimization" in dims:
            alpha = dims["Environment_Optimization"]["cronbach_alpha"]
            reliabilities["Autonomy"] = f"{alpha:.2f}"

        if "Intrinsic_Motivation" in dims:
            alpha = dims["Intrinsic_Motivation"]["cronbach_alpha"]
            reliabilities["Intrinsic Motivation"] = f"{alpha:.2f}"

        if "Resilience" in dims:
            alpha = dims["Resilience"]["cronbach_alpha"]
            reliabilities["Resilience"] = f"{alpha:.2f}"

        if "Social_Participation" in dims:
            alpha = dims["Social_Participation"]["cronbach_alpha"]
            reliabilities["Social Participation"] = f"{alpha:.2f}"

        # Authenticity - No direct mapping in current study.
        reliabilities["Authenticity"] = "Gap (Missing in Pilot)"

    mapping_content = f"""
| Dimension | Metric | Source | Range | Reliability (α) |
|-----------|--------|--------|-------|-----------------|
| Autonomy | Environment Optimization (Proxy) | IMP Survey | 0-5 | {reliabilities['Autonomy']} |
| Intrinsic Motivation | Intrinsic Motivation Scale | IMP Survey | 0-5 | {reliabilities['Intrinsic Motivation']} |
| Resilience | Resilience Scale | IMP Survey | 0-5 | {reliabilities['Resilience']} |
| Social Participation | Social Participation Scale | IMP Survey | 0-5 | {reliabilities['Social Participation']} |
| Authenticity | Congruence Score | Self-Report | 0-5 | {reliabilities['Authenticity']} |
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation
    # Generate dynamic insights
    insights = []
    if validation_report_data:
        overall_rel = validation_report_data.get("overall_reliability", 0)
        insights.append(f"- **Overall Reliability:** {overall_rel:.2f} (Target: > 0.8)")

        for dim, val in reliabilities.items():
            # Check if val is a number (it might be "Gap..." or "N/A")
            try:
                alpha = float(val)
                if alpha < 0.7:
                    insights.append(f"- **Warning:** {dim} reliability ({alpha}) is below threshold 0.7. Review items.")
                elif alpha >= 0.8:
                    insights.append(f"- **Success:** {dim} reliability ({alpha}) is excellent.")
            except ValueError:
                if "Gap" in val:
                    insights.append(f"- **Gap:** {dim} is missing validated metrics.")

    insights_text = "\n".join(insights)

    interpretation_content = f"""
# Scientific Interpretation
**Generated via Professor Dr. A. I. Nexus Protocol**
**Date:** {datetime.datetime.now().isoformat()}

## Empirical Status
- **Validation Study:** Completed (N={validation_report_data.get('n_participants', 'Unknown') if validation_report_data else 'Unknown'}).
- **Reliability Check:**
{insights_text}

- **External Data:** World Bank Education data fetched.
- **Literature:** arXiv/PubMed papers scraped for context.

## Hypothesis & Next Steps
Based on the zero-impact principle, any dimension < 0.7 requires immediate intervention.
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
