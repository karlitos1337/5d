#!/usr/bin/env python3
"""
Data Export Utilities for Dashboard Simulations
================================================

Provides standardized CSV/JSON export functionality for all interactive tools.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


def create_export_buttons(
    data: dict[str, Any], filename_base: str, include_formats: list[str] | None = None
):
    """
    Create download buttons for multiple export formats.

    Args:
        data: Dictionary with simulation results
        filename_base: Base filename (without extension)
        include_formats: List of formats to support ['json', 'csv', 'txt']

    Example:
        results = {
            'parameters': {'n': 100, 'threshold': 0.2},
            'metrics': {'final_activation': 0.85, 't_50': 23},
            'history': pd.DataFrame({'step': [0,1,2], 'value': [0.1, 0.3, 0.5]})
        }
        create_export_buttons(results, 'network_simulation')
    """
    if include_formats is None:
        include_formats = ["json", "csv"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    cols = st.columns(len(include_formats))

    for i, format_type in enumerate(include_formats):
        with cols[i]:
            if format_type == "json":
                _export_json(data, filename_base, timestamp)
            elif format_type == "csv":
                _export_csv(data, filename_base, timestamp)
            elif format_type == "txt":
                _export_txt(data, filename_base, timestamp)


def _export_json(data: dict[str, Any], filename_base: str, timestamp: str):
    """Export data as JSON."""
    # Convert DataFrames to dictionaries
    json_data = _prepare_for_json(data)

    json_str = json.dumps(json_data, indent=2, ensure_ascii=False)

    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=f"{filename_base}_{timestamp}.json",
        mime="application/json",
        help="Complete simulation data with all parameters and results",
    )


def _export_csv(data: dict[str, Any], filename_base: str, timestamp: str):
    """Export data as CSV (converts DataFrames, lists to CSV format)."""
    # Find first DataFrame in data
    df = None

    if "history" in data and isinstance(data["history"], pd.DataFrame):
        df = data["history"]
    elif "results" in data and isinstance(data["results"], pd.DataFrame):
        df = data["results"]
    else:
        # Try to find any DataFrame
        for value in data.values():
            if isinstance(value, pd.DataFrame):
                df = value
                break

    if df is not None:
        csv_str = df.to_csv(index=False)

        st.download_button(
            label="📊 Download CSV",
            data=csv_str,
            file_name=f"{filename_base}_{timestamp}.csv",
            mime="text/csv",
            help="Time series data in spreadsheet format",
        )
    else:
        st.caption("ℹ️ CSV export not available (no tabular data)")


def _export_txt(data: dict[str, Any], filename_base: str, timestamp: str):
    """Export data as human-readable text."""
    lines = [
        "5D Framework Simulation Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
    ]

    # Parameters
    if "parameters" in data:
        lines.append("PARAMETERS:")
        for key, value in data["parameters"].items():
            lines.append(f"  {key}: {value}")
        lines.append("")

    # Metrics
    if "metrics" in data:
        lines.append("RESULTS:")
        for key, value in data["metrics"].items():
            if isinstance(value, float):
                lines.append(f"  {key}: {value:.4f}")
            else:
                lines.append(f"  {key}: {value}")
        lines.append("")

    # IMP Proxies
    if "IMP_proxies" in data:
        lines.append("5D DIMENSION PROXIES:")
        for dim, score in data["IMP_proxies"].items():
            if isinstance(score, float):
                lines.append(f"  {dim}: {score:.3f}")
            else:
                lines.append(f"  {dim}: {score}")
        lines.append("")

    txt_str = "\n".join(lines)

    st.download_button(
        label="📄 Download TXT",
        data=txt_str,
        file_name=f"{filename_base}_{timestamp}.txt",
        mime="text/plain",
        help="Human-readable summary report",
    )


def _prepare_for_json(data: dict[str, Any]) -> dict[str, Any]:
    """Convert data to JSON-serializable format."""
    result = {}

    for key, value in data.items():
        if isinstance(value, pd.DataFrame):
            # Convert DataFrame to dict of lists
            result[key] = value.to_dict("list")
        elif isinstance(value, (pd.Series, pd.Index)):
            result[key] = value.tolist()
        elif isinstance(value, dict):
            result[key] = _prepare_for_json(value)
        elif isinstance(value, (list, tuple)):
            result[key] = [
                _prepare_for_json(item) if isinstance(item, dict) else item for item in value
            ]
        else:
            result[key] = value

    return result


def save_to_simulations_folder(data: dict[str, Any], filename: str) -> Path:
    """
    Save simulation results to simulations/ directory.

    Args:
        data: Simulation data
        filename: Filename (with extension)

    Returns:
        Path: Full path to saved file
    """
    sim_dir = Path("simulations")
    sim_dir.mkdir(exist_ok=True)

    filepath = sim_dir / filename

    json_data = _prepare_for_json(data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return filepath


def create_save_button(data: dict[str, Any], filename_base: str):
    """
    Create button to save simulation to simulations/ folder.

    Args:
        data: Simulation data
        filename_base: Base filename
    """
    if st.button("💾 Save to simulations/ folder"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_base}_{timestamp}.json"

        filepath = save_to_simulations_folder(data, filename)
        st.success(f"✅ Saved: `{filepath}`")


def display_export_section(
    data: dict[str, Any],
    filename_base: str,
    title: str = "💾 Export Results",
    include_formats: list[str] | None = None,
):
    """
    Display complete export section with all options.

    Args:
        data: Simulation results
        filename_base: Base filename
        title: Section title
        include_formats: Export formats to include
    """
    if include_formats is None:
        include_formats = ["json", "csv", "txt"]
    st.divider()
    st.header(title)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("**Download formats:**")
        create_export_buttons(data, filename_base, include_formats)

    with col2:
        st.markdown("**Save locally:**")
        create_save_button(data, filename_base)

    st.caption("""
    💡 **Tip:** JSON files include complete simulation state and can be re-loaded.
    CSV files are best for analysis in Excel/Python/R.
    """)


# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="Export Utilities Test", page_icon="💾")
    st.title("💾 Export Utilities Test")

    # Sample data
    sample_data = {
        "timestamp": datetime.now().isoformat(),
        "parameters": {"n_agents": 100, "threshold": 0.2, "steps": 50},
        "metrics": {"final_activation": 0.856, "t_50": 23, "clustering": 0.412},
        "IMP_proxies": {"A": 0.5, "IM": 0.72, "R": 0.54, "SP": 0.63, "Au": 0.5, "IMP": 0.061},
        "history": pd.DataFrame(
            {
                "step": list(range(10)),
                "active_fraction": [0.05 + i * 0.08 for i in range(10)],
                "active_count": [5 + i * 8 for i in range(10)],
            }
        ),
    }

    # Display sample data
    st.subheader("Sample Data Preview")
    st.json(sample_data["parameters"])
    st.dataframe(sample_data["history"])

    # Export section
    display_export_section(sample_data, "test_simulation")
