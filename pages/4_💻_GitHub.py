#!/usr/bin/env python3
"""
5D Dashboard - GitHub & Open Source
EdTech repositories, activity metrics, developer community
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="5D GitHub & Open Source",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=300)
def load_github_data():
    """Loads GitHub data with caching (TTL: 5 minutes)"""
    try:
        with open('5d_github_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("⚠️ 5d_github_data.json nicht gefunden - führe `python 5d_github_api.py` aus")
        return {}
    except Exception as e:
        st.error(f"❌ Fehler beim Laden: {e}")
        return {}

def calculate_activity_score(repo):
    """
    Activity Score Calculation
    
    Formula: Activity = (Stars × 0.4) + (Forks × 0.3) + (Updates × 0.2) + (Contributors × 0.1)
    
    Normalized to 0-100 scale
    """
    stars = repo.get('stars', 0)
    forks = repo.get('forks', 0)
    # Estimate updates from created/updated dates (simplified)
    updates = 100 if repo.get('updated_at') else 0
    contributors = repo.get('contributors', 1)
    
    raw_score = (stars * 0.4) + (forks * 0.3) + (updates * 0.2) + (contributors * 0.1)
    
    # Normalize to 0-100 (assuming max score ~10000)
    normalized = min(raw_score / 100, 100)
    
    return round(normalized, 2)

def main():
    # Sidebar
    with st.sidebar:
        st.title("💻 GitHub")
        st.markdown("**Open Source EdTech**")
        
        st.divider()
        
        st.markdown("### 🔬 Scientific Basis")
        st.markdown("""
        **Activity Score:**
        
        Basiert auf:
        - GitHub Metrics
        - Open Source Best Practices
        - Community Engagement
        
        **Status:** ⚠️ Own Research
        """)
        
        st.divider()
        
        st.markdown("### 🔑 API Info")
        st.markdown("""
        **Rate Limits:**
        - Ohne Token: 60/hour
        - Mit Token: 5000/hour
        
        **Setup:**
        ```bash
        export GITHUB_TOKEN=ghp_xxx
        python 5d_github_api.py
        ```
        """)
    
    # Main Content
    st.title("💻 GitHub & Open Source Projects")
    st.markdown("### EdTech Repositories & Developer Community")
    
    # Load Data
    github_data = load_github_data()
    
    # Metrics
    repos = github_data.get('repositories', {})
    trending = github_data.get('trending', {})
    
    total_repos = sum(len(repo_list) for repo_list in repos.values())
    total_trending = sum(len(items) for items in trending.values())
    
    # Calculate average stars
    all_repos = [repo for repo_list in repos.values() for repo in repo_list]
    avg_stars = sum(repo.get('stars', 0) for repo in all_repos) / len(all_repos) if all_repos else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Repositories", total_repos, help="EdTech Projects")
    
    with col2:
        st.metric("Trending Topics", total_trending, help="Hot Topics")
    
    with col3:
        st.metric("Avg Stars", f"{avg_stars:.0f}", help="Durchschnitt")
    
    with col4:
        st.metric("Queries", len(repos), help="Suchbegriffe")
    
    st.divider()
    
    # Main Content (2 columns)
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.header("🔍 Repositories nach Thema")
        
        if not repos:
            st.warning("""
            **Keine GitHub-Daten verfügbar.**
            
            Führe den GitHub Explorer aus:
            ```bash
            python 5d_github_api.py
            ```
            
            **Optional:** Setze `GITHUB_TOKEN` für höhere Rate Limits
            """)
        else:
            # Query Filter
            queries = list(repos.keys())
            selected_query = st.selectbox(
                "Thema auswählen",
                queries,
                index=0 if queries else None
            )
            
            if selected_query:
                repo_list = repos[selected_query]
                
                st.subheader(f"📦 {len(repo_list)} Repositories zu '{selected_query}'")
                
                # Sort options
                sort_by = st.radio(
                    "Sortieren nach:",
                    ["Stars", "Activity Score", "Forks", "Name"],
                    horizontal=True
                )
                
                if sort_by == "Stars":
                    repo_list = sorted(repo_list, key=lambda x: x.get('stars', 0), reverse=True)
                elif sort_by == "Activity Score":
                    repo_list = sorted(repo_list, key=calculate_activity_score, reverse=True)
                elif sort_by == "Forks":
                    repo_list = sorted(repo_list, key=lambda x: x.get('forks', 0), reverse=True)
                else:
                    repo_list = sorted(repo_list, key=lambda x: x.get('name', ''))
                
                for i, repo in enumerate(repo_list[:15], 1):
                    with st.expander(f"{i}. {repo.get('name', 'No name')} ⭐ {repo.get('stars', 0)}"):
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.markdown(f"**Link:** [{repo.get('url', '')}]({repo.get('url', '')})")
                            
                            description = repo.get('description', 'No description')
                            st.markdown(f"**Description:** {description}")
                            
                            language = repo.get('language', 'N/A')
                            st.markdown(f"**Language:** {language}")
                        
                        with col_b:
                            st.metric("⭐ Stars", repo.get('stars', 0))
                            st.metric("🍴 Forks", repo.get('forks', 0))
                            
                            activity = calculate_activity_score(repo)
                            st.metric("📊 Activity", activity)
    
    with col_right:
        st.header("📈 Trending Topics")
        
        if trending:
            for topic, items in list(trending.items())[:5]:
                st.subheader(f"🔥 {topic}")
                
                for item in items[:3]:
                    st.markdown(f"**[{item.get('name', '')}]({item.get('url', '')})**")
                    st.caption(f"⭐ {item.get('stars', 0)} | 🍴 {item.get('forks', 0)}")
                
                st.divider()
        else:
            st.info("Keine Trending-Daten verfügbar")
        
        st.divider()
        
        # Mini Map Placeholder
        st.subheader("🗺️ Developer Community")
        st.info("""
        **Coming Soon:**
        - Entwickler-Standorte (Heatmap)
        - Contributions pro Land
        - Hauptentwickler-Hubs
        """)
        
        st.divider()
        
        # License Distribution
        st.subheader("📜 License Info")
        st.markdown("""
        **Open Source Lizenzen:**
        - MIT (am häufigsten)
        - Apache 2.0
        - GPL-3.0
        - BSD-3-Clause
        
        **Best Practice:** MIT für maximale Kompatibilität
        """)
    
    st.divider()
    
    # Formulas Section (3 tabs)
    st.header("📐 Formeln & Metriken")
    
    tab1, tab2, tab3 = st.tabs(["Activity Score", "Quality Metrics", "Community Health"])
    
    with tab1:
        st.subheader("Activity Score Berechnung")
        
        st.latex(r"A_{score} = 0.4 \cdot S + 0.3 \cdot F + 0.2 \cdot U + 0.1 \cdot C")
        
        st.markdown("""
        **Komponenten:**
        - **S (Stars):** GitHub Stars (Community Interest)
        - **F (Forks):** Anzahl Forks (Active Usage)
        - **U (Updates):** Commit-Frequenz (Maintenance)
        - **C (Contributors):** Anzahl Contributors (Community Size)
        
        **Gewichte:** w₁=0.4, w₂=0.3, w₃=0.2, w₄=0.1
        
        **Normalisierung:** Score / 100, max = 100
        
        **Quelle:** Eigene Gewichtung (basiert auf GitHub Insights)
        
        **Status:** ⚠️ Own Research (nicht peer-reviewed)
        
        **Validierung:**
        - Vergleich mit GitHub Trending Algorithm
        - Korrelation mit Download-Statistiken
        - Community Feedback (Developer Survey)
        """)
        
        # Interactive Calculator
        st.subheader("🧮 Activity Score Rechner")
        
        calc_col1, calc_col2 = st.columns(2)
        
        with calc_col1:
            stars_input = st.number_input("Stars", 0, 100000, 1000, 100)
            forks_input = st.number_input("Forks", 0, 10000, 100, 10)
        
        with calc_col2:
            updates_input = st.number_input("Updates (commits/month)", 0, 1000, 50, 5)
            contributors_input = st.number_input("Contributors", 1, 1000, 10, 1)
        
        calculated_score = (
            (stars_input * 0.4) +
            (forks_input * 0.3) +
            (updates_input * 0.2) +
            (contributors_input * 0.1)
        ) / 100
        
        st.metric("Berechneter Activity Score", f"{calculated_score:.2f}")
    
    with tab2:
        st.subheader("Quality Metrics")
        
        st.markdown("""
        **Repository Quality Assessment:**
        
        | Metric | Weight | Source |
        |--------|--------|--------|
        | Code Coverage | 25% | CI/CD Reports |
        | Documentation | 20% | README Score |
        | Test Suite | 20% | Test Files Ratio |
        | Issue Response Time | 15% | GitHub Issues |
        | Release Frequency | 10% | GitHub Releases |
        | Community Engagement | 10% | Discussions, PRs |
        
        **Scoring:**
        - **Excellent:** 80-100 points
        - **Good:** 60-79 points
        - **Fair:** 40-59 points
        - **Poor:** 0-39 points
        
        **Implementation:** Custom scoring algorithm in `5d_github_api.py`
        """)
    
    with tab3:
        st.subheader("Community Health")
        
        st.markdown("""
        **GitHub Community Health Score:**
        
        Automatisch berechnet von GitHub (seit 2017):
        
        ✅ **Checklist:**
        - [ ] LICENSE file
        - [ ] README.md with description
        - [ ] CONTRIBUTING.md guidelines
        - [ ] CODE_OF_CONDUCT.md
        - [ ] Issue templates
        - [ ] Pull request template
        - [ ] Description field filled
        - [ ] Website/docs URL provided
        
        **Unser Score:** 7/8 (siehe [GitHub Insights](https://github.com/karlitos1337/5d/community))
        
        **Best Practices:**
        1. Respond to issues within 48h
        2. Review PRs within 72h
        3. Monthly releases (semantic versioning)
        4. Maintain CHANGELOG.md
        5. Clear documentation structure
        
        **Resources:**
        - [GitHub Community Guidelines](https://docs.github.com/en/communities)
        - [Open Source Guides](https://opensource.guide)
        """)
    
    st.divider()
    
    # Scientific References
    st.header("📚 Open Source Best Practices")
    
    with st.expander("🔬 Resources & Standards (expandable)"):
        st.markdown("""
        ### Relevante Standards & Richtlinien
        
        **Open Source Licenses:**
        - Open Source Initiative (OSI): [opensource.org](https://opensource.org)
        - Choose A License: [choosealicense.com](https://choosealicense.com)
        - SPDX License List: [spdx.org/licenses](https://spdx.org/licenses)
        
        **Community Guidelines:**
        - Contributor Covenant: [contributor-covenant.org](https://www.contributor-covenant.org)
        - GitHub Community Guidelines: [docs.github.com/communities](https://docs.github.com/en/communities)
        
        **Best Practices:**
        - Raymond, E. S. (1999). *The Cathedral and the Bazaar.* O'Reilly.
        - Fogel, K. (2005). *Producing Open Source Software.* O'Reilly.
        
        **Metrics & Analytics:**
        - CHAOSS Project: [chaoss.community](https://chaoss.community) (Linux Foundation)
        - GitHub Insights: Native GitHub Analytics
        - OpenSSF Scorecard: [github.com/ossf/scorecard](https://github.com/ossf/scorecard)
        
        ---
        
        **Implementation:** Siehe `5d_github_api.py` für API-Integration
        """)
    
    # Footer
    st.divider()
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        timestamp = github_data.get('timestamp', 'N/A')
        st.markdown(f"**Last Update:** {timestamp[:10] if timestamp != 'N/A' else 'N/A'}")
    
    with col_b:
        st.markdown(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d')}")
    
    with col_c:
        st.markdown("[Explorer Source](5d_github_api.py) | [GitHub Repo](https://github.com/karlitos1337/5d)")

if __name__ == "__main__":
    main()
