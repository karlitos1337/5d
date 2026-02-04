#!/usr/bin/env python3
"""
Streamlit-Seite: Forschungsplanung (Template) im 5D-Style
- Betten das bereitgestellte Homepage-Design inkl. Charts via st.components.html ein
"""

import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="5D Forschungsplanung (Template)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEMPLATE_PATH = Path("web/templates/5d_forschungsplanung.html")


def main():
    with st.sidebar:
        st.title("🧠 Forschungsplanung (Template)")
        st.markdown("Verwendet das 5D-Homepage-Design inkl. KPIs & Charts.")
        st.markdown("Quelle: internes 5D-Template")
        st.divider()
        st.info("Hinweis: Diese Seite rendert ein komplettes HTML-Template im iFrame.")

    st.title("🧠 Forschungsplanung – 5D Design-Template")
    st.caption("Template-Rendering via HTML (Tailwind, Chart.js, Plotly via CDN)")

    # Live-Daten (aus Artefakten) für schnelle Orientierung
    total_papers = total_arxiv = total_pubmed = total_repos = total_projects = 0
    avg_dimension = None

    try:
        with open("5d_research_data.json", encoding="utf-8") as f:
            research = json.load(f)
            total_arxiv = sum(len(v.get("arxiv", [])) for v in research.values())
            total_pubmed = sum(len(v.get("pubmed", [])) for v in research.values())
            total_papers = total_arxiv + total_pubmed
    except Exception:
        pass

    try:
        with open("5d_github_data.json", encoding="utf-8") as f:
            gh = json.load(f)
            repos = gh.get("repositories", {})
            total_repos = sum(len(v) for v in repos.values())
    except Exception:
        pass

    try:
        with open("5d_solutions.json", encoding="utf-8") as f:
            sols = json.load(f)
            total_projects = len(sols.get("projects", []))
            dims = [
                d.get("score")
                for d in sols.get("dimension_scores", [])
                if isinstance(d.get("score"), (int, float))
            ]
            if dims:
                avg_dimension = round(sum(dims) / len(dims), 2)
    except Exception:
        pass

    st.subheader("Live-Daten (aus Pipeline-Artefakten)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📄 Papers (arXiv+PubMed)", value=total_papers)
    with c2:
        st.metric("⭐️ GitHub Repos (gefunden)", value=total_repos)
    with c3:
        st.metric("🧩 Projekte (solutions)", value=total_projects)
    with c4:
        st.metric(
            "∅ Dimensions-Score",
            value=avg_dimension if avg_dimension is not None else "–",
        )

    if not TEMPLATE_PATH.exists():
        st.error(f"Template nicht gefunden: {TEMPLATE_PATH}")
        st.stop()

    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    # Höhe großzügig wählen (kann per Slider angepasst werden)
    height = st.slider(
        "Höhe (px)", min_value=1000, max_value=4000, value=2200, step=100
    )
    st.components.v1.html(html, height=height, scrolling=True)
    st.caption(
        "Evidence-Label: ⚠️ Hypothese – KPI-Zahlen im Template sind Platzhalter und nicht an Artefakte gebunden. Live-KPIs siehe oben."
    )


if __name__ == "__main__":
    main()
