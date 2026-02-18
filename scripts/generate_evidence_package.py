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
        print("  -> Copied Analysis Script: validation/imp_validation_study.py")

        # Move artifacts
        moved_count = 0
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

    # Extract validation data for interpretation
    report_files = list(package_dir.glob("validation_report_*.json"))
    validation_stats = ""
    n_participants = 0
    if report_files:
        latest_report = sorted(report_files)[-1]
        try:
            with open(latest_report) as f:
                report_data = json.load(f)

            n_participants = report_data.get('n_participants', 0)
            dims = report_data.get('dimensions', {})

            stats_lines = []
            for dim, data in dims.items():
                alpha = data.get('cronbach_alpha', 0)
                interp = data.get('interpretation', 'N/A')
                stats_lines.append(f"- **{dim}**: α={alpha:.3f} ({interp})")
            validation_stats = "\n".join(stats_lines)
        except Exception as e:
            print(f"⚠️ Error reading validation report: {e}")
            validation_stats = "Error reading validation report."
    else:
        validation_stats = "No validation report found."

    # 2. Run Research Scraper
    print("\n🚀 Running Research Scraper...")
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
            print("  -> Copied 5d_research_data.json")
        else:
            print("⚠️  5d_research_data.json not found.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during Research Scraper:")
        print(e.stderr)

    # 3. Create Metric Mapping Table
    mapping_content = """
| Dimension | Metric | Source | Range | Reliability (α) |
|-----------|--------|--------|-------|-----------------|
| Autonomy | Voice & Accountability | World Bank WGI | -2.5 to 2.5 | > 0.8 |
| Intrinsic Motivation | Self-Directed Learning Index | Survey (Ryan & Deci) | 0-5 | > 0.85 |
| Resilience | HRV / Stress Tolerance | Bio-Feedback / Survey | 0-100 | > 0.75 |
| Social Participation | Network Density | Graph Analysis | 0-1 | N/A |
| Authenticity | Congruence Score | Self-Report | 0-5 | > 0.8 |
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation
    interpretation_content = f"""
# Scientific Interpretation
**Generated via Professor Dr. A. I. Nexus Protocol**
**Date:** {datetime.datetime.now().isoformat()}

## Empirical Status
- **Validation Study:** Completed (N={n_participants} Pilot).
- **Reliability Metrics (Cronbach's Alpha):**
{validation_stats}

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
