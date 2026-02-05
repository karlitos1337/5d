#!/usr/bin/env python3
"""
BibTeX Helper Utilities for Dashboard Pages
============================================

Provides reusable functions for displaying scientific references
with copy-to-clipboard functionality.
"""

from pathlib import Path

import streamlit as st


def load_bibtex_entries():
    """
    Load all BibTeX entries from the central file.

    Returns:
        dict: Mapping of BibTeX keys to full entry text
    """
    bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")

    if not bibtex_path.exists():
        return {}

    content = bibtex_path.read_text(encoding="utf-8")

    # Parse BibTeX entries
    entries = {}
    current_key = None
    current_entry = []
    in_entry = False

    for line in content.split("\n"):
        # Start of new entry
        if line.strip().startswith("@"):
            if current_key and current_entry:
                entries[current_key] = "\n".join(current_entry)

            # Extract key: @article{key, or @book{key,
            parts = line.split("{")
            if len(parts) > 1:
                current_key = parts[1].split(",")[0].strip()
                current_entry = [line]
                in_entry = True
        elif in_entry:
            current_entry.append(line)
            # End of entry
            if line.strip() == "}":
                in_entry = False

    # Add last entry
    if current_key and current_entry:
        entries[current_key] = "\n".join(current_entry)

    return entries


def display_bibtex_reference(key: str, title: str, description: str = None):
    """
    Display a single BibTeX reference with copy button.

    Args:
        key: BibTeX key (e.g., 'deci1985intrinsic')
        title: Short title/citation to display
        description: Optional description of relevance
    """
    entries = load_bibtex_entries()

    if key not in entries:
        st.warning(f"⚠️ BibTeX key not found: {key}")
        return

    with st.expander(f"📄 {title}"):
        if description:
            st.markdown(description)

        # Display BibTeX entry
        st.code(entries[key], language="bibtex")

        # Copy button (using Streamlit's native functionality)
        st.caption("💡 Click the copy icon in the code block above to copy BibTeX entry")


def display_reference_section(references: list[dict], title: str = "📚 Wissenschaftliche Referenzen"):
    """
    Display a section with multiple references.

    Args:
        references: List of dicts with keys: 'key', 'title', 'description' (optional)
        title: Section header

    Example:
        references = [
            {
                'key': 'deci1985intrinsic',
                'title': 'Deci & Ryan (1985) - Self-Determination Theory',
                'description': 'Foundation for Intrinsic Motivation dimension'
            },
            {
                'key': 'csikszentmihalyi1990flow',
                'title': 'Csíkszentmihályi (1990) - Flow Theory'
            }
        ]
        display_reference_section(references)
    """
    st.divider()
    st.header(title)

    st.markdown(
        """
    **Alle Referenzen verfügbar in:** `07_daten_analysen/5d-relevant-sources.bib`
    
    Klicken Sie auf eine Referenz, um die vollständige BibTeX-Citation anzuzeigen.
    """
    )

    for ref in references:
        display_bibtex_reference(key=ref["key"], title=ref["title"], description=ref.get("description", None))


def get_reference_count():
    """
    Get total number of BibTeX references.

    Returns:
        int: Number of entries in BibTeX file
    """
    entries = load_bibtex_entries()
    return len(entries)


def search_references(query: str):
    """
    Search BibTeX entries by keyword.

    Args:
        query: Search term (case-insensitive)

    Returns:
        dict: Filtered entries matching query
    """
    entries = load_bibtex_entries()
    query_lower = query.lower()

    return {key: entry for key, entry in entries.items() if query_lower in entry.lower()}


# Example usage (can be imported in dashboard pages)
if __name__ == "__main__":
    # Test the module
    st.set_page_config(page_title="BibTeX Helper Test", page_icon="📚")
    st.title("📚 BibTeX Helper Test")

    # Show total count
    count = get_reference_count()
    st.metric("Total References", count)

    # Example display
    references = [
        {
            "key": "deci1985intrinsic",
            "title": "Deci & Ryan (1985) - Self-Determination Theory",
            "description": "Foundation for Intrinsic Motivation (IM) dimension",
        },
        {
            "key": "csikszentmihalyi1990flow",
            "title": "Csíkszentmihályi (1990) - Flow Theory",
            "description": "Optimal experience and engagement",
        },
        {
            "key": "granovetter1973strength",
            "title": "Granovetter (1973) - Weak Ties Theory",
            "description": "Social networks and information diffusion",
        },
    ]

    display_reference_section(references)

    # Search demo
    st.divider()
    st.subheader("🔍 Search References")
    query = st.text_input("Search term", "network")

    if query:
        results = search_references(query)
        st.write(f"Found {len(results)} matches:")
        for key in results.keys():
            st.code(key, language="text")
