#!/usr/bin/env python3
"""
Evidence Package Generator
Bundles all validation scripts, data, and results into a zip file for download.
"""

import datetime
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_step(command, description):
    """Runs a shell command and prints status."""
    print(f"\n🚀 {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print("✅ Done.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)


def generate_package():
    """Generates the evidence package."""
    # Setup paths
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"5d_evidence_package_{timestamp}"
    output_dir = Path("outputs")
    package_dir = output_dir / package_name

    # Create directories
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)
    (package_dir / "plots").mkdir()
    (package_dir / "data").mkdir()

    print(f"📦 Creating evidence package in: {package_dir}")

    # Set PYTHONPATH to include current directory
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    print("\n🚀 Running IMP Validation Study...")
    try:
        # Running validation study
        subprocess.run([sys.executable, "validation/imp_validation_study.py"], check=True, env=env)
        print("✅ Validation study completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Validation study failed: {e}")
        # Continue anyway to package what we have

    # 1. Copy Scripts
    print("\n📂 Bundling Scripts...")
    try:
        # Copy Analysis Script
        shutil.copy("validation/imp_validation_study.py", package_dir / "imp_validation_study.py")
        print("  -> Copied Analysis Script: validation/imp_validation_study.py")

        # Move artifacts
        for plot in glob.glob("outputs/*.png"):
            shutil.copy(plot, package_dir / "plots" / os.path.basename(plot))

        for csv in glob.glob("outputs/*.csv"):
            shutil.copy(csv, package_dir / "data" / os.path.basename(csv))

        for json_file in glob.glob("outputs/*.json"):
            shutil.copy(json_file, package_dir / "data" / os.path.basename(json_file))

    except Exception as e:
        print(f"⚠️  Error copying artifacts: {e}")

    # 2. Run Research Scraper
    print("\n🚀 Running Research Scraper...")
    try:
        subprocess.run(
            [sys.executable, "5d_research_scraper.py"],
            check=False,  # Don't fail if scraper has network issues
            env=env,
        )
        # Copy Scraper Script
        shutil.copy("5d_research_scraper.py", package_dir / "5d_research_scraper.py")

        # Copy Data if exists
        if os.path.exists("5d_research_data.json"):
            shutil.copy("5d_research_data.json", package_dir / "5d_research_data.json")
            print("  -> Copied 5d_research_data.json")
        else:
            print("⚠️  5d_research_data.json not found.")

    except Exception as e:
        print(f"⚠️  Scraper step failed: {e}")

    # 3. Copy Documentation
    print("\n📄 Bundling Documentation...")
    docs = ["METRIC_MAPPING.md", "INTERPRETATION.md", "README.md"]
    for doc in docs:
        if os.path.exists(f"validation/{doc}"):
            shutil.copy(f"validation/{doc}", package_dir / doc)
        elif os.path.exists(doc):
            shutil.copy(doc, package_dir / doc)

    # 4. Create Archive
    print("\n🗜️  Zipping package...")
    shutil.make_archive(str(package_dir), "zip", output_dir, package_name)

    # Cleanup directory (optional, keep zip)
    # shutil.rmtree(package_dir)

    print(f"\n✅ SUCCESS! Evidence package generated:\n   {package_dir}.zip")


if __name__ == "__main__":
    generate_package()
