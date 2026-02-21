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
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    print("\n🚀 Running IMP Validation Study...")
    try:
        result = subprocess.run(
            [sys.executable, "validation/imp_validation_study.py"],
            check=True,
            text=True,
            capture_output=True,
            env=env,
        )
        print(result.stdout)

        shutil.copy("validation/imp_validation_study.py", package_dir / "imp_validation_study.py")
        print("  -> Copied Analysis Script: validation/imp_validation_study.py")

        moved_count = 0
        validation_report_path = None
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
                if "validation_report" in f:
                    validation_report_path = dest

        if moved_count == 0:
            print("⚠️  No validation artifacts found to move.")

    except subprocess.CalledProcessError as e:
        print("❌ Error during IMP Validation Study:")
        print(e.stderr)
        validation_report_path = None

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

        research_data_path = package_dir / "5d_research_data.json"
        if os.path.exists("5d_research_data.json"):
            shutil.copy("5d_research_data.json", research_data_path)
            print("  -> Copied 5d_research_data.json")
        else:
            print("⚠️  5d_research_data.json not found.")
            research_data_path = None

    except subprocess.CalledProcessError as e:
        print("❌ Error during Research Scraper:")
        print(e.stderr)
        research_data_path = None

    # Load Data for Reports
    validation_data = {}
    if validation_report_path and validation_report_path.exists():
        try:
            with open(validation_report_path) as f:
                validation_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load validation report: {e}")

    research_data = {}
    if research_data_path and research_data_path.exists():
        try:
            with open(research_data_path) as f:
                research_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load research data: {e}")

    # 3. Create Metric Mapping Table
    # Dynamically build table based on validation results
    rows = []

    # Internal Metrics (from Validation Study)
    if "dimensions" in validation_data:
        for dim, stats in validation_data["dimensions"].items():
            alpha = stats.get("cronbach_alpha", 0)
            status = "✅ Validated" if alpha >= 0.8 else "⚠️ Needs Revision"
            rows.append(f"| {dim} | Internal Consistency | Pilot Survey | 0-5 | {alpha:.3f} ({status}) |")
    else:
        rows.append("| 5D Dimensions | Internal Consistency | Pilot Survey | 0-5 | N/A (Run Failed) |")

    # External Metrics (from Research Scraper)
    if "world_bank_wgi" in research_data and "data" in research_data["world_bank_wgi"]:
        rows.append("| Autonomy | Voice & Accountability | World Bank WGI | -2.5 to 2.5 | Global Std |")
        rows.append("| Resilience | Rule of Law | World Bank WGI | -2.5 to 2.5 | Global Std |")
        rows.append("| Environment Opt. | Gov. Effectiveness | World Bank WGI | -2.5 to 2.5 | Global Std |")

    mapping_table = "\n".join(rows)

    mapping_content = f"""
# Metric Mapping Table
**Generated via Professor Dr. A. I. Nexus Protocol**

| Dimension | Metric | Source | Range | Reliability / Status |
|-----------|--------|--------|-------|----------------------|
{mapping_table}
| Social Participation | Network Density | Graph Analysis | 0-1 | N/A |
| Authenticity | Congruence Score | Self-Report | 0-5 | > 0.8 (Target) |
    """
    with open(package_dir / "METRIC_MAPPING.md", "w") as f:
        f.write(mapping_content)

    # 4. Create Interpretation
    # Analyze Reliability gaps
    reliability_gaps = []
    if "dimensions" in validation_data:
        for dim, stats in validation_data["dimensions"].items():
            if stats.get("cronbach_alpha", 0) < 0.8:
                reliability_gaps.append(
                    f"- **{dim}**: α = {stats.get('cronbach_alpha'):.3f} (< 0.8). Requires item revision."
                )

    gap_analysis = (
        "\n".join(reliability_gaps) if reliability_gaps else "No reliability gaps detected. All dimensions α >= 0.8."
    )

    # External Data Availability
    wgi_count = len(research_data.get("world_bank_wgi", {}).get("data", {}))
    edu_count = len(research_data.get("world_bank_education", {}).get("data", {}))

    interpretation_content = f"""
# Scientific Interpretation
**Generated via Professor Dr. A. I. Nexus Protocol**
**Date:** {datetime.datetime.now().isoformat()}

## 1. Empirical Status: Validation Study
- **Participants:** {validation_data.get('n_participants', 'N/A')} (Pilot)
- **Overall Reliability:** α = {validation_data.get('overall_reliability', 0):.3f}
- **Recommendation:** {validation_data.get('recommendation', 'N/A')}

## 2. Reliability & Gap Analysis
{gap_analysis}

## 3. External Data Integration
- **World Bank WGI:** Fetched for {wgi_count} countries. (Proxies: Autonomy, Resilience, Environment)
- **World Bank Education:** Fetched for {edu_count} countries.
- **Literature:** Scraped {sum(len(d.get('arxiv', [])) for d in research_data.values() if isinstance(d, dict))} arXiv papers.

## 4. Hypothesis & Next Steps
**Protocol Rule:** If any dimension < 0.8, immediate revision is required before scaling.

**Action Plan:**
1. Review items for dimensions flagged above.
2. Expand N to >100 for statistical power.
3. Correlate internal scores with WGI external data.

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


if __name__ == "__main__":
    main()
