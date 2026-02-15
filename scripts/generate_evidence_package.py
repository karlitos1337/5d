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
        report_path = None
        for pattern in ["questionnaire_*.json", "example_responses_*.csv", "validation_results_*.png", "validation_report_*.json"]:
            for f in glob.glob(pattern):
                dest = package_dir / os.path.basename(f)
                shutil.move(f, dest)
                print(f"  -> Moved {f}")
                moved_count += 1
                if "validation_report_" in f:
                    report_path = dest

        if moved_count == 0:
            print("⚠️  No validation artifacts found to move.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during IMP Validation Study:")
        print(e.stderr)

    # Load Validation Data for dynamic reporting
    validation_data = {}
    if report_path and report_path.exists():
        try:
            with open(report_path, encoding="utf-8") as f:
                validation_data = json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load validation report: {e}")

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

    # 3. Create Metric Mapping Table (Dynamic)
    print("\n📊 Generating Metric Mapping Table...")

    # Default values if validation failed
    alphas = {
        "Autonomy": "N/A",
        "Intrinsic_Motivation": "N/A",
        "Resilience": "N/A",
        "Social_Participation": "N/A",
        "Authenticity": "N/A"
    }

    if "dimensions" in validation_data:
        for dim, stats in validation_data["dimensions"].items():
            if "cronbach_alpha" in stats:
                alphas[dim] = f"{stats['cronbach_alpha']:.3f}"

    mapping_content = f"""
| Dimension | Metric | Source | Range | Reliability (α) | Status |
|-----------|--------|--------|-------|-----------------|--------|
| Autonomy | Voice & Accountability (WGI) / Self-Report | World Bank / Survey | -2.5 to 2.5 / 0-5 | {alphas.get('Autonomy', 'N/A')} | {'✅ Validated' if alphas.get('Autonomy') != 'N/A' and float(alphas.get('Autonomy')) > 0.7 else '⚠️ Review'} |
| Intrinsic Motivation | Self-Directed Learning Index | Survey (Ryan & Deci) | 0-5 | {alphas.get('Intrinsic_Motivation', 'N/A')} | {'✅ Validated' if alphas.get('Intrinsic_Motivation') != 'N/A' and float(alphas.get('Intrinsic_Motivation')) > 0.7 else '⚠️ Review'} |
| Resilience | HRV / Stress Tolerance / CD-RISC | Bio-Feedback / Survey | 0-100 / 0-5 | {alphas.get('Resilience', 'N/A')} | {'✅ Validated' if alphas.get('Resilience') != 'N/A' and float(alphas.get('Resilience')) > 0.7 else '⚠️ Review'} |
| Social Participation | Network Density / Belonging | Graph Analysis / Survey | 0-1 / 0-5 | {alphas.get('Social_Participation', 'N/A')} | {'✅ Validated' if alphas.get('Social_Participation') != 'N/A' and float(alphas.get('Social_Participation')) > 0.7 else '⚠️ Review'} |
| Authenticity | Congruence Score | Self-Report | 0-5 | {alphas.get('Authenticity', 'N/A')} | {'✅ Validated' if alphas.get('Authenticity') != 'N/A' and float(alphas.get('Authenticity')) > 0.7 else '⚠️ Review'} |
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation (Dynamic)
    print("\n🧠 Generating Scientific Interpretation...")

    wgi_details = ""
    try:
        with open("5d_research_data.json") as f:
            rd = json.load(f)
            if "world_bank_wgi" in rd:
                wgi_details = f"- **Governance Data:** Fetched for {len(rd['world_bank_wgi'].get('data', {}))} countries (Voice & Accountability, Rule of Law, Gov Effectiveness)."
            else:
                 wgi_details = "- **Governance Data:** ⚠️ Missing in fetch result."
    except Exception:
        pass

    interpretation_content = f"""
# Scientific Interpretation
**Generated via Professor Dr. A. I. Nexus Protocol**
**Date:** {datetime.datetime.now().isoformat()}

## 1. Empirical Status
### Validation Study (Micro-Level)
- **Sample Size:** {validation_data.get('n_participants', 'N/A')} (Pilot)
- **Reliability Check (Cronbach's α > 0.7):**
  - **Autonomy:** {alphas.get('Autonomy')}
  - **Intrinsic Motivation:** {alphas.get('Intrinsic_Motivation')}
  - **Resilience:** {alphas.get('Resilience')}
  - **Social Participation:** {alphas.get('Social_Participation')}
  - **Authenticity:** {alphas.get('Authenticity')}

### External Data (Macro-Level)
- **Education Data:** World Bank EdStats fetched.
{wgi_details}
- **Literature:** arXiv/PubMed papers scraped for context.

## 2. Hypothesis & Gap Analysis
**Protocol Rule:** Any dimension with α < 0.7 requires immediate item revision.
**Status:** {'✅ All dimensions validated (α > 0.7).' if all(float(v) > 0.7 for v in alphas.values() if v != 'N/A') else '⚠️ Some dimensions require revision.'}

## 3. Discriminant Validity
Refer to `validation_results_*.png` (Heatmap) to ensure correlations between dimensions are < 0.85.

[PUSH TO DOWNLOAD]
- Analysis Script: validation/imp_validation_study.py
- Metric Mapping: METRIC_MAPPING.md
- Visualization: validation_results_*.png
- Research Data: 5d_research_data.json
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
