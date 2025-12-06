#!/usr/bin/env python3
"""
5D Dashboard - Future Projections
Adoption Curves, Economic Impact, Scenario Modeling
"""

import sys
from datetime import datetime
from pathlib import Path

import folium
import numpy as np
import streamlit as st
from streamlit_folium import st_folium

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.mobile_responsive import inject_mobile_css

st.set_page_config(
    page_title="5D Projections", page_icon="📈", layout="wide", initial_sidebar_state="expanded"
)

# Inject mobile-responsive CSS
inject_mobile_css()


def logistic_curve(x, L, k, x0):
    """
    Logistic Growth Curve (S-Curve)

    L: Maximum value (carrying capacity)
    k: Steepness of curve
    x0: Midpoint (inflection point)
    """
    return L / (1 + np.exp(-k * (x - x0)))


def calculate_economic_impact(adoption_rate, avg_roi, num_projects):
    """
    Economic Impact Calculation

    Based on Heckman's NPV methodology (2006)
    """
    # Net Present Value (simplified)
    total_investment = num_projects * 50000  # Average investment per project
    total_return = total_investment * (1 + avg_roi / 100) * adoption_rate

    net_impact = total_return - total_investment

    return {
        "investment": total_investment,
        "return": total_return,
        "net_impact": net_impact,
        "roi": (net_impact / total_investment) * 100 if total_investment > 0 else 0,
    }


@st.cache_data(ttl=3600)
def load_regional_adoption_projections():
    """
    Load projected adoption rates for 5D Framework by region (2030 forecast).

    ⚠️ Hypothese: Basierend auf Rogers Diffusion Curve + aktuelle Bildungsreformen

    Returns:
        list: Regions with projected adoption rates, readiness indicators
    """
    regions = [
        # Nordeuropa - High readiness (existing alternative education infrastructure)
        {
            "name": "Nordic Countries",
            "location": "Copenhagen, Denmark",
            "lat": 55.6761,
            "lon": 12.5683,
            "adoption_2030": 0.45,  # 45% adoption projected
            "readiness_score": 0.88,
            "key_drivers": ["Folk High Schools legacy", "High WGI governance", "Low dropout rates"],
            "scenario": "Optimistic"
        },
        {
            "name": "Netherlands",
            "location": "Amsterdam, Netherlands",
            "lat": 52.3676,
            "lon": 4.9041,
            "adoption_2030": 0.42,
            "readiness_score": 0.85,
            "key_drivers": ["Montessori tradition", "Progressive education policy", "High autonomy"],
            "scenario": "Optimistic"
        },
        # Westeuropa - Moderate readiness
        {
            "name": "Germany",
            "location": "Berlin, Germany",
            "lat": 52.5200,
            "lon": 13.4050,
            "adoption_2030": 0.35,
            "readiness_score": 0.78,
            "key_drivers": ["Waldorf schools network", "Federal education system", "Mixed governance"],
            "scenario": "Moderate"
        },
        {
            "name": "UK",
            "location": "London, UK",
            "lat": 51.5074,
            "lon": -0.1278,
            "adoption_2030": 0.32,
            "readiness_score": 0.75,
            "key_drivers": ["Summerhill legacy", "Democratic schools movement", "High mental health burden"],
            "scenario": "Moderate"
        },
        # Nordamerika - Mixed adoption
        {
            "name": "USA - New England",
            "location": "Boston, MA, USA",
            "lat": 42.3601,
            "lon": -71.0589,
            "adoption_2030": 0.38,
            "readiness_score": 0.80,
            "key_drivers": ["Sudbury schools", "MIT/Harvard research hubs", "Homeschooling culture"],
            "scenario": "Moderate"
        },
        {
            "name": "USA - California",
            "location": "San Francisco, CA, USA",
            "lat": 37.7749,
            "lon": -122.4194,
            "adoption_2030": 0.40,
            "readiness_score": 0.82,
            "key_drivers": ["EdTech innovation", "Progressive policies", "High depression rates drive demand"],
            "scenario": "Optimistic"
        },
        # Asien - Rapid growth regions
        {
            "name": "Japan",
            "location": "Tokyo, Japan",
            "lat": 35.6762,
            "lon": 139.6503,
            "adoption_2030": 0.28,
            "readiness_score": 0.70,
            "key_drivers": ["Tokkatsu tradition", "Low dropout but high stress", "Aging population concerns"],
            "scenario": "Conservative"
        },
        {
            "name": "South Korea",
            "location": "Seoul, South Korea",
            "lat": 37.5665,
            "lon": 126.9780,
            "adoption_2030": 0.25,
            "readiness_score": 0.68,
            "key_drivers": ["Mental health crisis", "High education pressure", "Tech infrastructure"],
            "scenario": "Conservative"
        },
        {
            "name": "India",
            "location": "Bangalore, India",
            "lat": 12.9716,
            "lon": 77.5946,
            "adoption_2030": 0.22,
            "readiness_score": 0.62,
            "key_drivers": ["EdTech growth", "Large youth population", "Governance challenges"],
            "scenario": "Conservative"
        },
        # Lateinamerika - Emerging adoption
        {
            "name": "Brazil",
            "location": "São Paulo, Brazil",
            "lat": -23.5505,
            "lon": -46.6333,
            "adoption_2030": 0.20,
            "readiness_score": 0.58,
            "key_drivers": ["Inequality driver", "Democratic education pilots", "Limited resources"],
            "scenario": "Conservative"
        },
        {
            "name": "Chile",
            "location": "Santiago, Chile",
            "lat": -33.4489,
            "lon": -70.6693,
            "adoption_2030": 0.24,
            "readiness_score": 0.65,
            "key_drivers": ["Education reform efforts", "Student activism", "Moderate governance"],
            "scenario": "Conservative"
        },
        # Afrika - Early-stage
        {
            "name": "Kenya",
            "location": "Nairobi, Kenya",
            "lat": -1.2864,
            "lon": 36.8172,
            "adoption_2030": 0.15,
            "readiness_score": 0.48,
            "key_drivers": ["Mobile EdTech", "Youth demographic dividend", "Resource constraints"],
            "scenario": "Conservative"
        },
        # Ozeanien
        {
            "name": "Australia",
            "location": "Sydney, Australia",
            "lat": -33.8688,
            "lon": 151.2093,
            "adoption_2030": 0.36,
            "readiness_score": 0.77,
            "key_drivers": ["Indigenous education models", "High mental health awareness", "Strong governance"],
            "scenario": "Moderate"
        },
        {
            "name": "New Zealand",
            "location": "Auckland, New Zealand",
            "lat": -36.8485,
            "lon": 174.7633,
            "adoption_2030": 0.40,
            "readiness_score": 0.83,
            "key_drivers": ["Māori Kura Kaupapa", "Progressive policies", "Low population enables pilots"],
            "scenario": "Optimistic"
        }
    ]
    return regions


def create_regional_adoption_map(regions_data):
    """
    Create Folium map showing projected 2030 adoption rates by region.

    Args:
        regions_data: List of region dicts with lat, lon, adoption_2030, scenario

    Returns:
        folium.Map: Interactive map with regional adoption projections
    """
    # Create base map centered on global view
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="OpenStreetMap",
        width="100%",
        height=400
    )

    # Scenario colors
    scenario_colors = {
        "Optimistic": "#2ECC40",    # Green
        "Moderate": "#FF851B",       # Orange
        "Conservative": "#0074D9"    # Blue
    }

    for region in regions_data:
        adoption_2030 = region.get("adoption_2030", 0)
        readiness_score = region.get("readiness_score", 0)
        scenario = region.get("scenario", "Conservative")

        # Marker color by scenario
        scenario_color = scenario_colors.get(scenario, "#AAAAAA")

        # Icon color by adoption rate
        if adoption_2030 >= 0.35:
            icon_color = "green"     # High adoption (≥35%)
        elif adoption_2030 >= 0.25:
            icon_color = "orange"    # Medium adoption (25-34%)
        else:
            icon_color = "blue"      # Lower adoption (<25%)

        # Circle size by readiness score
        radius = 8 + (readiness_score * 12)

        # Create popup content
        drivers_html = "<br>".join([f"• {d}" for d in region["key_drivers"]])

        popup_html = f"""
        <div style="font-family: Arial; width: 240px;">
            <h4 style="margin: 0 0 8px 0; color: {scenario_color};">{region['name']}</h4>
            <p style="margin: 4px 0;"><strong>Projected Adoption 2030:</strong> {adoption_2030 * 100:.0f}%</p>
            <p style="margin: 4px 0;"><strong>Readiness Score:</strong> {readiness_score:.2f}</p>
            <p style="margin: 4px 0;"><strong>Scenario:</strong> <span style="color: {scenario_color};">{scenario}</span></p>
            <p style="margin: 8px 0 4px 0;"><strong>Key Drivers:</strong></p>
            <div style="font-size: 11px; margin-left: 10px;">{drivers_html}</div>
        </div>
        """

        # Add circle marker with size based on readiness
        folium.CircleMarker(
            location=[region["lat"], region["lon"]],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=280),
            color=scenario_color,
            fill=True,
            fillColor=scenario_color,
            fillOpacity=0.5,
            weight=2
        ).add_to(m)

        # Add standard marker on top
        folium.Marker(
            location=[region["lat"], region["lon"]],
            popup=folium.Popup(popup_html, max_width=280),
            icon=folium.Icon(color=icon_color, icon="line-chart", prefix="fa"),
            tooltip=f"{region['name']}: {adoption_2030 * 100:.0f}% by 2030 ({scenario})"
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px; 
                background-color: white; border: 2px solid grey; z-index: 9999; 
                font-size: 12px; padding: 10px;">
        <p style="margin: 0 0 8px 0; font-weight: bold;">2030 Adoption Scenarios</p>
        <p style="margin: 4px 0;"><span style="color: #2ECC40;">●</span> Optimistic (≥35%)</p>
        <p style="margin: 4px 0;"><span style="color: #FF851B;">●</span> Moderate (25-34%)</p>
        <p style="margin: 4px 0;"><span style="color: #0074D9;">●</span> Conservative (<25%)</p>
        <p style="margin: 8px 0 0 0; font-size: 10px; color: grey;">
            Circle size = Readiness score
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def main():
    # Sidebar
    with st.sidebar:
        st.title("📈 Projections")
        st.markdown("**Future Scenarios & Impact**")

        st.divider()

        st.markdown("### 🔬 Scientific Basis")
        st.markdown(
            """
        **Diffusion Theory:**
        
        Rogers, E. M. (2003)
        *Diffusion of Innovations*
        
        **Economic Impact:**
        
        Heckman, J. J. (2006)
        *Skill Formation & Economics*
        
        **Status:** ✅ Peer-Reviewed
        """
        )

        st.divider()

        st.markdown("### 📊 Scenarios")
        st.markdown(
            """
        **3 Szenarien:**
        
        🐌 **Conservative:**
        - Langsame Adoption
        - Status Quo
        
        🚀 **Moderate:**
        - Realistische Projection
        - Business as Usual
        
        🌟 **Optimistic:**
        - Schnelle Adoption
        - Policy Support
        """
        )

    # Main Content
    st.title("📈 Future Projections: 5D Intelligence Adoption")
    st.markdown("### Scenario Modeling, Economic Impact, Adoption Curves")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Projection Years", "10-30", help="2025-2055")

    with col2:
        st.metric("Scenarios", "3", help="Conservative, Moderate, Optimistic")

    with col3:
        st.metric("Target Adoption", "50%", help="Global Education Systems")

    with col4:
        st.metric("Est. ROI", "485%", help="Avg from Projects")

    st.divider()

    # World Map: Regional Adoption Projections
    st.header("🗺️ Regional Adoption Projections (2030)")
    st.markdown(
        """
        Interactive map showing **projected adoption rates** for 5D Framework by region. 
        **Readiness Score** combines governance quality, existing alternative education infrastructure, 
        and mental health/dropout drivers.
        
        📊 **Legend:** Green = Optimistic (≥35%), Orange = Moderate (25-34%), Blue = Conservative (<25%)
        """
    )

    regions_data = load_regional_adoption_projections()
    adoption_map = create_regional_adoption_map(regions_data)
    st_folium(adoption_map, width=None, height=400, returned_objects=[])

    st.caption(
        "⚠️ **Projection Method:** Rogers Diffusion Curve + current education reform trends + "
        "WGI governance indicators. Optimistic scenario assumes policy support; Conservative assumes status quo."
    )

    st.divider()

    # Main Content (2 columns)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.header("🎯 Adoption Curve Simulation")

        st.markdown(
            """
        **Logistic Growth Model (S-Curve):**
        
        Typisch für Innovation Diffusion (Rogers 2003)
        """
        )

        # Parameters
        st.subheader("⚙️ Parameter")

        param_col1, param_col2 = st.columns(2)

        with param_col1:
            max_adoption = st.slider(
                "Max Adoption (%)", 10, 100, 50, 5, help="Carrying Capacity (L)"
            )

            inflection_year = st.slider(
                "Inflection Year", 2030, 2045, 2035, 1, help="Midpoint (x₀)"
            )

        with param_col2:
            steepness = st.slider("Steepness (k)", 0.1, 1.0, 0.3, 0.05, help="Höher = schneller")

            start_year = st.slider("Start Year", 2025, 2030, 2025, 1)

        end_year = start_year + 30

        # Generate Curves
        years = np.arange(start_year, end_year + 1)

        # Conservative
        conservative = logistic_curve(
            years, max_adoption * 0.6, steepness * 0.5, inflection_year + 5
        )

        # Moderate
        moderate = logistic_curve(years, max_adoption, steepness, inflection_year)

        # Optimistic
        optimistic = logistic_curve(years, max_adoption * 1.2, steepness * 1.5, inflection_year - 5)

        # Display
        st.divider()
        st.subheader("📊 Adoption Over Time")

        # ASCII Chart (simplified)
        st.markdown("**Adoption Rate (%) per Year**")
        st.markdown("```")
        st.markdown("Legend: 🐌 Conservative | 🚀 Moderate | 🌟 Optimistic")
        st.markdown("")

        # Sample every 5 years
        sample_years = list(range(start_year, end_year + 1, 5))

        for year in sample_years:
            idx = year - start_year

            c = conservative[idx]
            m = moderate[idx]
            o = optimistic[idx]

            st.markdown(f"{year}: 🐌 {c:5.1f}% | 🚀 {m:5.1f}% | 🌟 {o:5.1f}%")

        st.markdown("```")

        # Key Milestones
        st.divider()
        st.subheader("🎯 Milestones")

        # Find year when adoption reaches 25%, 50%
        def find_milestone_year(curve, target, years):
            for i, value in enumerate(curve):
                if value >= target:
                    return years[i]
            return None

        milestone_col1, milestone_col2, milestone_col3 = st.columns(3)

        with milestone_col1:
            st.markdown("**25% Adoption:**")
            cons_25 = find_milestone_year(conservative, 25, years)
            mod_25 = find_milestone_year(moderate, 25, years)
            opt_25 = find_milestone_year(optimistic, 25, years)

            st.markdown(f"- 🐌 {cons_25 if cons_25 else 'N/A'}")
            st.markdown(f"- 🚀 {mod_25 if mod_25 else 'N/A'}")
            st.markdown(f"- 🌟 {opt_25 if opt_25 else 'N/A'}")

        with milestone_col2:
            st.markdown("**50% Adoption:**")
            cons_50 = find_milestone_year(conservative, 50, years)
            mod_50 = find_milestone_year(moderate, 50, years)
            opt_50 = find_milestone_year(optimistic, 50, years)

            st.markdown(f"- 🐌 {cons_50 if cons_50 else 'N/A'}")
            st.markdown(f"- 🚀 {mod_50 if mod_50 else 'N/A'}")
            st.markdown(f"- 🌟 {opt_50 if opt_50 else 'N/A'}")

        with milestone_col3:
            st.markdown("**75% Adoption:**")
            cons_75 = find_milestone_year(conservative, 75, years)
            mod_75 = find_milestone_year(moderate, 75, years)
            opt_75 = find_milestone_year(optimistic, 75, years)

            st.markdown(f"- 🐌 {cons_75 if cons_75 else 'N/A'}")
            st.markdown(f"- 🚀 {mod_75 if mod_75 else 'N/A'}")
            st.markdown(f"- 🌟 {opt_75 if opt_75 else 'N/A'}")

        # Economic Impact
        st.divider()
        st.subheader("💰 Economic Impact (2055)")

        # Calculate for moderate scenario
        final_adoption = moderate[-1] / 100
        avg_roi = 485  # From 5d_solutions.json
        num_projects = 100  # Estimate

        impact = calculate_economic_impact(final_adoption, avg_roi, num_projects)

        impact_col1, impact_col2, impact_col3 = st.columns(3)

        with impact_col1:
            st.metric("Investment", f"€{impact['investment']:,.0f}")

        with impact_col2:
            st.metric("Return", f"€{impact['return']:,.0f}")

        with impact_col3:
            st.metric(
                "Net Impact", f"€{impact['net_impact']:,.0f}", delta=f"{impact['roi']:.1f}% ROI"
            )

    with col_right:
        st.header("🌍 Global Impact")

        st.markdown(
            """
        **Projection by Sector:**
        
        🚗 **Automotive (Electric Vehicles):**
        - 2025: 10% global sales
        - 2030: 30% (moderate)
        - 2040: 60% (optimistic)
        - 2050: 80%+ (conservative: 50%)
        
        ✈️ **Aviation (Sustainable Fuel):**
        - 2025: 1% SAF usage
        - 2030: 5%
        - 2040: 20%
        - 2050: 50%+
        
        🚢 **Shipping (Green Tech):**
        - 2025: 2% alternative fuels
        - 2030: 10%
        - 2040: 30%
        - 2050: 60%+
        
        🏫 **Education (5D Intelligence):**
        - 2025: 5% alternative schools
        - 2030: 12%
        - 2040: 30%
        - 2050: 50%+
        """
        )

        st.divider()

        st.subheader("🗺️ Regional Projections for 2040")

        from utils.map_helpers import create_regional_adoption_map, render_minimap

        m = create_regional_adoption_map()
        render_minimap(m, "Projected 5D Intelligence adoption rates by region (2040 estimates)")

        st.divider()

        st.markdown(
            """
        **Detailed Breakdown:**
        
        🇪🇺 **Europe:** 40-60%
        - Nordics führend (70%+)
        - Policy Support
        
        🇺🇸 **North America:** 30-50%
        - USA: 35%
        - Canada: 45%
        
        🌏 **Asia:** 20-40%
        - Japan: 50%
        - China: 25%
        - Indien: 15%
        
        🌍 **Africa:** 10-25%
        - Starke Varianz
        - Urban > Rural
        
        🌎 **Latin America:** 15-35%
        - Brasilien: 30%
        - Chile: 40%
        """
        )

        st.divider()

        st.subheader("⚡ Tipping Points")

        st.markdown(
            """
        **Critical Mass:** 16-20% adoption
        
        **Rogers' Diffusion:**
        1. Innovators (2.5%)
        2. Early Adopters (13.5%)
        3. **Early Majority (34%)** ← Tipping Point
        4. Late Majority (34%)
        5. Laggards (16%)
        
        **Bei 16%:** Self-sustaining growth
        """
        )

    st.divider()

    # Formulas Section
    st.header("📐 Projection Formulas")

    tab1, tab2, tab3 = st.tabs(["Logistic Curve", "Economic Impact", "Diffusion Theory"])

    with tab1:
        st.subheader("Logistic Growth Curve (S-Curve)")

        st.latex(r"A(t) = \frac{L}{1 + e^{-k(t - t_0)}}")

        st.markdown(
            """
        **Parameter:**
        - **A(t):** Adoption rate zur Zeit t (%)
        - **L:** Maximum adoption (Carrying Capacity)
        - **k:** Steepness (Wachstumsrate)
        - **t₀:** Inflection point (Wendepunkt)
        
        **Eigenschaften:**
        - **S-förmig:** Langsamer Start, schnelles Wachstum, Sättigung
        - **Inflection Point:** Bei t = t₀, maximales Wachstum
        - **Asymptoten:** 0 (unten), L (oben)
        
        **Anwendung:**
        - Innovation Diffusion (Rogers 2003)
        - Population Growth (Verhulst 1838)
        - Technology Adoption (Bass 1969)
        
        **Ableitungen:**
        """
        )

        st.latex(r"\frac{dA}{dt} = k \cdot A \cdot (1 - \frac{A}{L})")

        st.markdown(
            """
        **Interpretation:**
        - Wachstum proportional zu A (mehr Adopters → mehr Adoption)
        - Gebremst durch (1 - A/L) (Sättigung)
        
        **Quelle:** Verhulst, P. F. (1838). *Notice sur la loi que la population suit dans son accroissement*
        """
        )

    with tab2:
        st.subheader("Economic Impact Calculation")

        st.latex(r"\text{NPV} = \sum_{t=0}^{T} \frac{R_t - C_t}{(1 + r)^t}")

        st.markdown(
            """
        **Net Present Value (NPV):**
        
        - **R_t:** Returns in year t
        - **C_t:** Costs in year t
        - **r:** Discount rate (typically 3-7%)
        - **T:** Time horizon (years)
        
        **Simplified (für Projection):**
        """
        )

        st.latex(r"\text{Impact} = I \cdot (1 + \text{ROI}) \cdot A_t - I")

        st.markdown(
            """
        **Wo:**
        - **I:** Total Investment
        - **ROI:** Return on Investment (%)
        - **A_t:** Adoption rate zur Zeit t
        
        **Beispiel:**
        - I = €5,000,000 (100 Projects × €50,000)
        - ROI = 485% (aus 5d_solutions.json)
        - A_t = 50% (moderate scenario 2055)
        - **Impact = €5M × (1 + 4.85) × 0.5 - €5M = €9.625M**
        
        **Quelle:** Heckman, J. J. (2006). *Skill Formation and the Economics of Investing in Disadvantaged Children*
        
        **Validation:**
        - Perry Preschool: 7-10% annual return
        - Abecedarian: 10-13% annual return
        - **Alternative Bildung:** 15-20% geschätzt (konservativ)
        """
        )

    with tab3:
        st.subheader("Diffusion of Innovations Theory")

        st.markdown(
            """
        **Rogers (2003): 5 Adopter Categories**
        
        | Category | % of Population | Characteristics |
        |----------|----------------|-----------------|
        | **Innovators** | 2.5% | Risk-takers, wealthy, educated |
        | **Early Adopters** | 13.5% | Opinion leaders, respected |
        | **Early Majority** | 34% | Deliberate, social connections |
        | **Late Majority** | 34% | Skeptical, economic pressure |
        | **Laggards** | 16% | Traditional, isolated |
        
        **Tipping Point:** Bei ~16% (Innovators + Early Adopters)
        
        **Bass Diffusion Model:**
        """
        )

        st.latex(r"f(t) = \frac{dA}{dt} = (p + q \cdot A(t)) \cdot (L - A(t))")

        st.markdown(
            """
        **Parameter:**
        - **p:** Coefficient of Innovation (external influence)
        - **q:** Coefficient of Imitation (internal influence)
        - **L:** Market Potential
        - **A(t):** Cumulative Adopters
        
        **Typische Werte:**
        - p ≈ 0.03 (3% innovators)
        - q ≈ 0.38 (38% imitators)
        - **Peak:** When A(t) = L × p / q
        
        **Anwendung:**
        - Consumer Products (TV, Mobile Phones)
        - Technology (Internet, Smartphones)
        - Education Reforms (Montessori took 80 years to 10%)
        
        **Literatur:**
        - Rogers, E. M. (2003). *Diffusion of Innovations* (5th ed.). Free Press.
        - Bass, F. M. (1969). *A New Product Growth Model for Consumer Durables*. Management Science, 15(5): 215-227.
        - Mahajan, V., Muller, E., & Bass, F. M. (1990). *New Product Diffusion Models in Marketing*. Journal of Marketing, 54(1): 1-26.
        """
        )

    st.divider()

    # Scientific References
    st.header("📚 Wissenschaftliche Quellen")

    with st.expander("🔬 References (expandable)"):
        st.markdown(
            """
        ### Primärquellen
        
        **1. Rogers, E. M. (2003)**
        - *Diffusion of Innovations* (5th ed.)
        - Free Press
        - ISBN: 978-0743222099
        
        **2. Bass, F. M. (1969)**
        - *A New Product Growth Model for Consumer Durables*
        - Management Science, 15(5): 215-227
        - DOI: 10.1287/mnsc.15.5.215
        
        **3. Verhulst, P. F. (1838)**
        - *Notice sur la loi que la population suit dans son accroissement*
        - Correspondence Mathématique et Physique, 10: 113-121
        
        **4. Heckman, J. J. (2006)**
        - *Skill Formation and the Economics of Investing in Disadvantaged Children*
        - Science, 312(5782): 1900-1902
        - DOI: 10.1126/science.1128898
        
        ---
        
        ### Economic Impact Studies
        
        **5. Schweinhart, L. J., et al. (2005)**
        - *Lifetime Effects: The High/Scope Perry Preschool Study Through Age 40*
        - High/Scope Press
        - **ROI:** 7-10% per annum
        
        **6. Campbell, F. A., et al. (2014)**
        - *Early Childhood Investments Substantially Boost Adult Health*
        - Science, 343(6178): 1478-1485
        - DOI: 10.1126/science.1248429
        - **ROI:** 10-13% per annum
        
        ---
        
        ### Technology Adoption
        
        **7. Comin, D., & Hobijn, B. (2004)**
        - *Cross-country Technology Adoption: Making the Theories Face the Facts*
        - Journal of Monetary Economics, 51(1): 39-83
        - DOI: 10.1016/j.jmoneco.2003.07.003
        
        **8. Geroski, P. A. (2000)**
        - *Models of technology diffusion*
        - Research Policy, 29(4-5): 603-625
        - DOI: 10.1016/S0048-7333(99)00092-X
        
        ---
        
        ### Education Reform Adoption
        
        **9. Cuban, L. (2013)**
        - *Why So Many Structural Changes in Schools and So Little Reform in Teaching Practice?*
        - Journal of Educational Administration, 51(2): 109-125
        - DOI: 10.1108/09578231311304661
        
        **10. Tyack, D., & Cuban, L. (1995)**
        - *Tinkering Toward Utopia: A Century of Public School Reform*
        - Harvard University Press
        - ISBN: 978-0674892835
        
        ---
        
        **BibTeX:** Siehe `07_daten_analysen/5d-relevant-sources.bib`
        """
        )

    # Footer
    st.divider()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(f"**Projection:** {start_year}-{end_year}")

    with col_b:
        st.markdown(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d')}")

    with col_c:
        st.markdown(
            "[Rogers 2003](https://books.google.com/books?id=v1ii4QsB7jIC) | [Heckman 2006](https://doi.org/10.1126/science.1128898)"
        )


if __name__ == "__main__":
    main()
