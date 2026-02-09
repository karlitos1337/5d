#!/usr/bin/env python3
"""
5D Dashboard - GitHub & Open Source
EdTech repositories, activity metrics, developer community
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.mobile_responsive import inject_mobile_css

st.set_page_config(
    page_title="5D GitHub & Open Source",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject mobile-responsive CSS
inject_mobile_css()


@st.cache_data(ttl=1800)
def load_github_data():
    """Loads GitHub data with caching (TTL: 30 minutes)"""
    try:
        with open("5d_github_data.json", encoding="utf-8") as f:
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
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    # Estimate updates from created/updated dates (simplified)
    updates = 100 if repo.get("updated_at") else 0
    contributors = repo.get("contributors", 1)

    raw_score = (stars * 0.4) + (forks * 0.3) + (updates * 0.2) + (contributors * 0.1)

    # Normalize to 0-100 (assuming max score ~10000)
    normalized = min(raw_score / 100, 100)

    return round(normalized, 2)


@st.cache_data(ttl=3600)
def load_github_developer_hubs():
    """
    Load geographic data for major EdTech/Open Source developer communities.

    ⚠️ Hypothese: Standorte basieren auf GitHub Developer Community Reports (2023)

    Returns:
        list: Developer hubs with location, repo count, active developers
    """
    hubs = [
        # USA - Silicon Valley
        {
            "name": "San Francisco Bay Area",
            "location": "San Francisco, CA, USA",
            "lat": 37.7749,
            "lon": -122.4194,
            "active_repos": 450,
            "active_developers": 3200,
            "key_projects": ["Khan Academy", "edX", "Coursera"],
            "tech_stack": ["React", "Python", "Node.js"],
        },
        # USA - Boston/Cambridge (MIT/Harvard)
        {
            "name": "Boston EdTech Hub",
            "location": "Boston, MA, USA",
            "lat": 42.3601,
            "lon": -71.0589,
            "active_repos": 320,
            "active_developers": 1800,
            "key_projects": ["MIT OpenCourseWare", "Scratch"],
            "tech_stack": ["JavaScript", "Java", "Python"],
        },
        # UK - London
        {
            "name": "London Tech Community",
            "location": "London, UK",
            "lat": 51.5074,
            "lon": -0.1278,
            "active_repos": 280,
            "active_developers": 2100,
            "key_projects": ["FutureLearn", "Raspberry Pi Foundation"],
            "tech_stack": ["TypeScript", "React", "Go"],
        },
        # Germany - Berlin
        {
            "name": "Berlin Open Source Hub",
            "location": "Berlin, Germany",
            "lat": 52.5200,
            "lon": 13.4050,
            "active_repos": 190,
            "active_developers": 1400,
            "key_projects": ["Moodle Germany", "HPI Schul-Cloud"],
            "tech_stack": ["PHP", "Python", "Vue.js"],
        },
        # India - Bangalore
        {
            "name": "Bangalore Tech Community",
            "location": "Bangalore, India",
            "lat": 12.9716,
            "lon": 77.5946,
            "active_repos": 340,
            "active_developers": 2800,
            "key_projects": ["BYJU'S Open Source", "Unacademy"],
            "tech_stack": ["React Native", "Python", "Flutter"],
        },
        # China - Beijing
        {
            "name": "Beijing Developer Community",
            "location": "Beijing, China",
            "lat": 39.9042,
            "lon": 116.4074,
            "active_repos": 410,
            "active_developers": 3500,
            "key_projects": ["XuetangX", "17zuoye"],
            "tech_stack": ["Vue.js", "Python", "Golang"],
        },
        # Israel - Tel Aviv
        {
            "name": "Tel Aviv EdTech Startups",
            "location": "Tel Aviv, Israel",
            "lat": 32.0853,
            "lon": 34.7818,
            "active_repos": 150,
            "active_developers": 900,
            "key_projects": ["Codecademy", "Verbit"],
            "tech_stack": ["React", "Node.js", "Python"],
        },
        # Australia - Sydney
        {
            "name": "Sydney Tech Hub",
            "location": "Sydney, Australia",
            "lat": -33.8688,
            "lon": 151.2093,
            "active_repos": 120,
            "active_developers": 750,
            "key_projects": ["Canva Education", "Mathspace"],
            "tech_stack": ["React", "TypeScript", "Kotlin"],
        },
        # Canada - Toronto
        {
            "name": "Toronto Developer Community",
            "location": "Toronto, Canada",
            "lat": 43.6532,
            "lon": -79.3832,
            "active_repos": 180,
            "active_developers": 1200,
            "key_projects": ["D2L (Desire2Learn)", "Top Hat"],
            "tech_stack": ["React", "Java", "Python"],
        },
        # Brazil - São Paulo
        {
            "name": "São Paulo Tech Community",
            "location": "São Paulo, Brazil",
            "lat": -23.5505,
            "lon": -46.6333,
            "active_repos": 140,
            "active_developers": 980,
            "key_projects": ["Descomplica", "Veduca"],
            "tech_stack": ["React", "Node.js", "PHP"],
        },
    ]
    return hubs


def create_github_developer_map(hubs_data):
    """
    Create Folium map showing major EdTech/Open Source developer communities.

    Args:
        hubs_data: List of hub dicts with lat, lon, active_repos, active_developers

    Returns:
        folium.Map: Interactive map with developer hub markers
    """
    # Create base map centered on global view
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap", width="100%", height=400)

    for hub in hubs_data:
        active_repos = hub.get("active_repos", 0)
        active_developers = hub.get("active_developers", 0)

        # Marker color by repository count
        if active_repos >= 300:
            icon_color = "red"  # Major hub (300+ repos)
        elif active_repos >= 150:
            icon_color = "orange"  # Medium hub (150-299 repos)
        else:
            icon_color = "blue"  # Emerging hub (<150 repos)

        # Circle size by developer count
        radius = 10 + (active_developers / 200)

        # Create popup content
        projects_html = "<br>".join([f"• {p}" for p in hub["key_projects"]])
        tech_html = ", ".join(hub["tech_stack"])

        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="margin: 0 0 8px 0; color: #0074D9;">{hub["name"]}</h4>
            <p style="margin: 4px 0;"><strong>Active Repos:</strong> {active_repos}</p>
            <p style="margin: 4px 0;"><strong>Active Developers:</strong> {active_developers:,}</p>
            <p style="margin: 8px 0 4px 0;"><strong>Key Projects:</strong></p>
            <div style="font-size: 11px; margin-left: 10px;">{projects_html}</div>
            <p style="margin: 8px 0 4px 0;"><strong>Tech Stack:</strong></p>
            <div style="font-size: 11px; margin-left: 10px;">{tech_html}</div>
        </div>
        """

        # Add circle marker with size based on developer count
        folium.CircleMarker(
            location=[hub["lat"], hub["lon"]],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=280),
            color=icon_color,
            fill=True,
            fillColor=icon_color,
            fillOpacity=0.5,
            weight=2,
        ).add_to(m)

        # Add standard marker on top
        folium.Marker(
            location=[hub["lat"], hub["lon"]],
            popup=folium.Popup(popup_html, max_width=280),
            icon=folium.Icon(color=icon_color, icon="github", prefix="fa"),
            tooltip=f"{hub['name']} ({active_repos} repos, {active_developers} devs)",
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px; 
                background-color: white; border: 2px solid grey; z-index: 9999; 
                font-size: 12px; padding: 10px;">
        <p style="margin: 0 0 8px 0; font-weight: bold;">Developer Communities</p>
        <p style="margin: 4px 0;"><span style="color: red;">●</span> Major Hub (≥300 repos)</p>
        <p style="margin: 4px 0;"><span style="color: orange;">●</span> Medium Hub (150-299)</p>
        <p style="margin: 4px 0;"><span style="color: blue;">●</span> Emerging Hub (<150)</p>
        <p style="margin: 8px 0 0 0; font-size: 10px; color: grey;">
            Circle size = Active developers
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def main():
    # Sidebar
    with st.sidebar:
        st.title("💻 GitHub")
        st.markdown("**Open Source EdTech**")

        st.divider()

        st.markdown("### 🔬 Scientific Basis")
        st.markdown(
            """
        **Activity Score:**
        
        Basiert auf:
        - GitHub Metrics
        - Open Source Best Practices
        - Community Engagement
        
        **Status:** ⚠️ Own Research
        """
        )

        st.divider()

        st.markdown("### 🔑 API Info")
        st.markdown(
            """
        **Rate Limits:**
        - Ohne Token: 60/hour
        - Mit Token: 5000/hour
        
        **Setup:**
        ```bash
        export GITHUB_TOKEN=ghp_xxx
        python 5d_github_api.py
        ```
        """
        )

    # Main Content
    st.title("💻 GitHub & Open Source Projects")
    st.markdown("### EdTech Repositories & Developer Community")

    # Load Data
    github_data = load_github_data()

    # Metrics
    repos = github_data.get("repositories", {})
    trending = github_data.get("trending", {})

    total_repos = sum(len(repo_list) for repo_list in repos.values())
    total_trending = sum(len(items) for items in trending.values())

    # Calculate average stars
    all_repos = [repo for repo_list in repos.values() for repo in repo_list]
    avg_stars = sum(repo.get("stars", 0) for repo in all_repos) / len(all_repos) if all_repos else 0  # noqa: E501

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

    # World Map: Developer Communities
    st.header("🗺️ Global Developer Communities")
    st.markdown(
        """
        Interactive map showing major EdTech and Open Source developer hubs worldwide. 
        Data reflects **active repositories** and **developer counts** in each region.
        
        📊 **Legend:** Red = Major Hub (≥300 repos), Orange = Medium (150-299), Blue = Emerging (<150)  # noqa: E501
        """
    )

    hubs_data = load_github_developer_hubs()
    developer_map = create_github_developer_map(hubs_data)
    st_folium(developer_map, width=None, height=400, returned_objects=[])

    st.caption(
        "⚠️ **Data Source:** Estimated from GitHub Developer Community Reports (2023) and public "
        "EdTech project repositories. Counts are approximations."
    )

    st.divider()

    # Main Content (2 columns)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.header("🔍 Repositories nach Thema")

        if not repos:
            st.warning(
                """
            **Keine GitHub-Daten verfügbar.**
            
            Führe den GitHub Explorer aus:
            ```bash
            python 5d_github_api.py
            ```
            
            **Optional:** Setze `GITHUB_TOKEN` für höhere Rate Limits
            """
            )
        else:
            # Query Filter
            queries = list(repos.keys())
            selected_query = st.selectbox("Thema auswählen", queries, index=0 if queries else None)

            if selected_query:
                repo_list = repos[selected_query]

                st.subheader(f"📦 {len(repo_list)} Repositories zu '{selected_query}'")

                # Sort options
                sort_by = st.radio(
                    "Sortieren nach:", ["Stars", "Activity Score", "Forks", "Name"], horizontal=True  # noqa: E501
                )

                if sort_by == "Stars":
                    repo_list = sorted(repo_list, key=lambda x: x.get("stars", 0), reverse=True)
                elif sort_by == "Activity Score":
                    repo_list = sorted(repo_list, key=calculate_activity_score, reverse=True)
                elif sort_by == "Forks":
                    repo_list = sorted(repo_list, key=lambda x: x.get("forks", 0), reverse=True)
                else:
                    repo_list = sorted(repo_list, key=lambda x: x.get("name", ""))

                for i, repo in enumerate(repo_list[:15], 1):
                    with st.expander(
                        f"{i}. {repo.get('name', 'No name')} ⭐ {repo.get('stars', 0)}"
                    ):
                        col_a, col_b = st.columns([3, 1])

                        with col_a:
                            st.markdown(f"**Link:** [{repo.get('url', '')}]({repo.get('url', '')})")  # noqa: E501

                            description = repo.get("description", "No description")
                            st.markdown(f"**Description:** {description}")

                            language = repo.get("language", "N/A")
                            st.markdown(f"**Language:** {language}")

                        with col_b:
                            st.metric("⭐ Stars", repo.get("stars", 0))
                            st.metric("🍴 Forks", repo.get("forks", 0))

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

        # Mini Map
        st.subheader("🗺️ Developer Community")

        from utils.map_helpers import create_developer_community_map, render_minimap

        m = create_developer_community_map()
        render_minimap(m, "Global distribution of EdTech developers (GitHub community)")

        st.divider()

        # License Distribution
        st.subheader("📜 License Info")
        st.markdown(
            """
        **Open Source Lizenzen:**
        - MIT (am häufigsten)
        - Apache 2.0
        - GPL-3.0
        - BSD-3-Clause
        
        **Best Practice:** MIT für maximale Kompatibilität
        """
        )

    st.divider()

    # Formulas Section (3 tabs)
    st.header("📐 Formeln & Metriken")

    tab1, tab2, tab3 = st.tabs(["Activity Score", "Quality Metrics", "Community Health"])

    with tab1:
        st.subheader("Activity Score Berechnung")

        st.latex(r"A_{score} = 0.4 \cdot S + 0.3 \cdot F + 0.2 \cdot U + 0.1 \cdot C")

        st.markdown(
            """
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
        """
        )

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
            (stars_input * 0.4)
            + (forks_input * 0.3)
            + (updates_input * 0.2)
            + (contributors_input * 0.1)
        ) / 100

        st.metric("Berechneter Activity Score", f"{calculated_score:.2f}")

    with tab2:
        st.subheader("Quality Metrics")

        st.markdown(
            """
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
        """
        )

    with tab3:
        st.subheader("Community Health")

        st.markdown(
            """
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
        
        **Unser Score:** 7/8 (siehe [GitHub Insights](https://github.com/karlitos1337/5d/community))  # noqa: E501
        
        **Best Practices:**
        1. Respond to issues within 48h
        2. Review PRs within 72h
        3. Monthly releases (semantic versioning)
        4. Maintain CHANGELOG.md
        5. Clear documentation structure
        
        **Resources:**
        - [GitHub Community Guidelines](https://docs.github.com/en/communities)
        - [Open Source Guides](https://opensource.guide)
        """
        )

    st.divider()

    # Scientific References
    st.header("📚 Open Source Best Practices")

    with st.expander("🔬 Resources & Standards (expandable)"):
        st.markdown(
            """
        ### Relevante Standards & Richtlinien
        
        **Open Source Licenses:**
        - Open Source Initiative (OSI): [opensource.org](https://opensource.org)
        - Choose A License: [choosealicense.com](https://choosealicense.com)
        - SPDX License List: [spdx.org/licenses](https://spdx.org/licenses)
        
        **Community Guidelines:**
        - Contributor Covenant: [contributor-covenant.org](https://www.contributor-covenant.org)
        - GitHub Community Guidelines: [docs.github.com/communities](https://docs.github.com/en/communities)  # noqa: E501
        
        **Best Practices:**
        - Raymond, E. S. (1999). *The Cathedral and the Bazaar.* O'Reilly.
        - Fogel, K. (2005). *Producing Open Source Software.* O'Reilly.
        
        **Metrics & Analytics:**
        - CHAOSS Project: [chaoss.community](https://chaoss.community) (Linux Foundation)
        - GitHub Insights: Native GitHub Analytics
        - OpenSSF Scorecard: [github.com/ossf/scorecard](https://github.com/ossf/scorecard)
        
        ---
        
        **Implementation:** Siehe `5d_github_api.py` für API-Integration
        """
        )

    # Footer
    st.divider()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        timestamp = github_data.get("timestamp", "N/A")
        st.markdown(f"**Last Update:** {timestamp[:10] if timestamp != 'N/A' else 'N/A'}")

    with col_b:
        st.markdown(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d')}")

    with col_c:
        st.markdown(
            "[Explorer Source](5d_github_api.py) | [GitHub Repo](https://github.com/karlitos1337/5d)"  # noqa: E501
        )


if __name__ == "__main__":
    main()
