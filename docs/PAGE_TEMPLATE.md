# Page Template Guide – 5D Dashboard

**Purpose:** Standard-Template für alle Dashboard-Pages  
**Status:** v1.0 (2025-12-03)  
**Usage:** Copy-paste für neue Pages oder Refactoring bestehender Pages

---

## 📋 Vollständiges Page-Template

```python
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="[Thema] - 5D Intelligence Framework",
    page_icon="[Emoji]",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("[Emoji] [Thema]")
st.markdown("### Wissenschaftliche Grundlage")

# Info-Box: Scientific Basis
with st.expander("ℹ️ Was ist [Thema]?", expanded=False):
    st.markdown("""
    **Definition:** [1-2 Sätze]
    
    **Wissenschaftliche Basis:**
    - [Theorie/Modell 1] (Autor Jahr)
    - [Theorie/Modell 2] (Autor Jahr)
    
    **Evidenz:** ✅ Fakt / ⚠️ Hypothese / 🔮 Spekulation
    
    **Relevanz für 5D:**
    - Dimension [A/IM/R/SP/Au]: [Kurze Erklärung]
    """)

# ============================================================
# HAUPTTEXT (200-400 Wörter)
# ============================================================

st.markdown("""
## 📖 Kontext

[Paragraph 1: Motivation, Problem, Forschungsfrage]

[Paragraph 2: Theoretischer Hintergrund, Key Concepts]

[Paragraph 3: Empirische Evidenz, Studien, Daten]

**Key Insights:**
- **Insight 1:** [Wichtigste Erkenntnis]
- **Insight 2:** [Zweitwichtigste Erkenntnis]
- **Insight 3:** [Drittwichtigste Erkenntnis]
""")

# ============================================================
# METRICS (4 Spalten)
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="[Metrik 1]",
        value="[Wert]",
        delta="[Änderung]",
        help="[Tooltip-Text]"
    )

with col2:
    st.metric(
        label="[Metrik 2]",
        value="[Wert]",
        delta="[Änderung]",
        help="[Tooltip-Text]"
    )

with col3:
    st.metric(
        label="[Metrik 3]",
        value="[Wert]",
        delta="[Änderung]",
        help="[Tooltip-Text]"
    )

with col4:
    st.metric(
        label="[Metrik 4]",
        value="[Wert]",
        delta="[Änderung]",
        help="[Tooltip-Text]"
    )

# ============================================================
# FORMELN (3 Tabs)
# ============================================================

st.header("🔬 Formeln & Berechnungen")

tab1, tab2, tab3 = st.tabs(["Formel 1", "Formel 2", "Formel 3"])

with tab1:
    st.markdown("### [Formel 1 Name]")
    
    # LaTeX Formula
    st.latex(r"IMP = A \times IM \times R \times SP \times Au")
    
    # Explanation
    st.markdown("""
    **Variablen:**
    - **A:** Autonomy (0-1)
    - **IM:** Intrinsic Motivation (0-1)
    - **R:** Resilience (0-1)
    - **SP:** Social Participation (0-1)
    - **Au:** Authenticity (0-1)
    
    **Begründung:**
    - Multiplikativ: Schwächstes Glied bestimmt (weak-link logic)
    - Alle Dimensionen notwendig (A=0 → IMP=0)
    
    **Quelle:** Eigene Modellierung, basierend auf:
    - Deci & Ryan (1985) – Self-Determination Theory [@deci1985intrinsic]
    - Csíkszentmihályi (1990) – Flow Theory [@csikszentmihalyi1990flow]
    
    **Evidenz:** ⚠️ Hypothese (testbar, noch nicht validiert)
    """)

with tab2:
    st.markdown("### [Formel 2 Name]")
    
    st.latex(r"ROI = \frac{Benefits - Costs}{Costs} \times 100\%")
    
    st.markdown("""
    **Variablen:**
    - **Benefits:** Total monetarisierter Nutzen ($)
    - **Costs:** Total Investitionskosten ($)
    
    **Begründung:**
    - Heckman-Methode: NPV (Net Present Value) über Lebensspanne
    - Discount Rate: 3% p.a. (Standard für soziale Projekte)
    
    **Quelle:**
    - Heckman et al. (2006) – Skill Formation [@heckman2006skill]
    - Schweinhart et al. (2005) – Perry Preschool [@schweinhart2005lifetime]
    
    **Evidenz:** ✅ Fakt (Perry ROI 7.16:1 repliziert)
    """)

with tab3:
    st.markdown("### [Formel 3 Name]")
    
    st.latex(r"Success\_Rate = \frac{Graduated}{Enrolled} \times 100\%")
    
    st.markdown("""
    **Variablen:**
    - **Graduated:** Anzahl Absolventen
    - **Enrolled:** Anzahl Eingeschriebene
    
    **Begründung:**
    - Standard-Metrik für Bildungserfolg
    - Dropout-Rate = 100% - Success Rate
    
    **Quelle:**
    - World Bank EdStats [@worldbank2023edstats]
    - OECD Education at a Glance [@oecd2020bli]
    
    **Evidenz:** ✅ Fakt (standardisierte Messung)
    """)

# ============================================================
# INTERACTIVE VISUALIZATION
# ============================================================

st.header("📊 Interaktive Visualisierung")

# Example: Plotly Chart
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Value": [10, 25, 15, 30]
})

fig = px.bar(
    df,
    x="Category",
    y="Value",
    title="[Chart Title]",
    color="Value",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================
# MINI-MAP (Geographic Distribution)
# ============================================================

st.header("🗺️ Geografische Verteilung")

# Example: Folium Map
m = folium.Map(
    location=[51.1657, 10.4515],  # Germany center
    zoom_start=5,
    tiles="CartoDB positron"
)

# Add markers
folium.Marker(
    location=[52.5200, 13.4050],  # Berlin
    popup="Berlin<br>IMP: 0.72",
    icon=folium.Icon(color="green", icon="school", prefix="fa")
).add_to(m)

folium.Marker(
    location=[48.1351, 11.5820],  # München
    popup="München<br>IMP: 0.68",
    icon=folium.Icon(color="green", icon="school", prefix="fa")
).add_to(m)

# Render map
st_folium(m, width=700, height=350)

# ============================================================
# OWN APPS / SIMULATIONS
# ============================================================

st.header("🧪 Interaktive Tools")

with st.expander("🎮 Simulation / Calculator", expanded=False):
    st.markdown("### [Tool Name]")
    
    # Input sliders
    param1 = st.slider("Parameter 1", 0.0, 1.0, 0.5, 0.01)
    param2 = st.slider("Parameter 2", 0.0, 1.0, 0.7, 0.01)
    
    # Calculation
    result = param1 * param2
    
    # Output
    st.metric("Result", f"{result:.2f}")
    
    st.markdown("""
    **Erklärung:**
    - [Was macht dieses Tool?]
    - [Wie interpretiert man die Resultate?]
    """)

# ============================================================
# SCIENTIFIC REFERENCES (Footer)
# ============================================================

st.divider()
st.header("📚 Wissenschaftliche Quellen")

st.markdown("""
### Peer-Reviewed (✅ Fakt)

1. **Deci, E. L., & Ryan, R. M. (1985).** *Intrinsic Motivation and Self-Determination in Human Behavior.*  
   Springer. [DOI: 10.1007/978-1-4899-2271-7](https://doi.org/10.1007/978-1-4899-2271-7)  
   BibTeX: `deci1985intrinsic`

2. **Csíkszentmihályi, M. (1990).** *Flow: The Psychology of Optimal Experience.*  
   Harper & Row. ISBN: 978-0060920432  
   BibTeX: `csikszentmihalyi1990flow`

3. **Heckman, J. J. (2006).** *Skill Formation and the Economics of Investing in Disadvantaged Children.*  
   Science, 312(5782), 1900-1902. [DOI: 10.1126/science.1128898](https://doi.org/10.1126/science.1128898)  
   BibTeX: `heckman2006skill`

### Eigene Analysen (⚠️ Hypothese)

4. **5D Intelligence Framework (2025).** *IMP-Formel: Eigene Modellierung.*  
   GitHub: [karlitos1337/5d](https://github.com/karlitos1337/5d)  
   Status: Testbar, noch nicht peer-reviewed  
   BibTeX: `5d_repo`

### Datenquellen (✅ Fakt)

5. **World Bank (2023).** *World Development Indicators.*  
   URL: [https://databank.worldbank.org](https://databank.worldbank.org)  
   BibTeX: `worldbank2023wdi`

6. **WHO (2017).** *Depression and Other Common Mental Disorders: Global Health Estimates.*  
   Geneva: WHO. URL: [https://apps.who.int/iris/handle/10665/254610](https://apps.who.int/iris/handle/10665/254610)  
   BibTeX: `who2017depression`

---

**Vollständige Literatur:** Siehe [5d-relevant-sources.bib](../07_daten_analysen/5d-relevant-sources.bib) (70 Einträge)

**Evidenzmatrix:** Siehe [CLAIMS_EVIDENCE_MATRIX.md](../docs/CLAIMS_EVIDENCE_MATRIX.md) (40 Behauptungen, Fakt/Hypothese/Spekulation)
""")

# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.divider()
st.header("💾 Downloads")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="📄 Download Data (CSV)",
        data=df.to_csv(index=False),
        file_name="data.csv",
        mime="text/csv"
    )

with col2:
    st.markdown("📊 [Download Full Report (PDF)](#)")  # Placeholder

with col3:
    st.markdown("📚 [BibTeX Export](../07_daten_analysen/5d-relevant-sources.bib)")

# ============================================================
# NAVIGATION (Footer)
# ============================================================

st.divider()
st.markdown("### 🔗 Navigation")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("5d_dashboard.py", label="🏠 Home / Wiki", icon="🏠")

with col2:
    st.page_link("pages/1_📊_IMP_Analysis.py", label="📊 IMP Analysis", icon="📊")

with col3:
    st.page_link("pages/2_🚀_Projects.py", label="🚀 Projects", icon="🚀")

# ============================================================
# SIDEBAR (Optional: Additional Info)
# ============================================================

with st.sidebar:
    st.header("ℹ️ About this Page")
    
    st.markdown("""
    **Topic:** [Thema]
    
    **Scientific Basis:**
    - ✅ Peer-reviewed: [X]
    - ⚠️ Own Research: [Y]
    - 🔮 Speculative: [Z]
    
    **Data Sources:**
    - [Source 1]
    - [Source 2]
    
    **Last Updated:** 2025-12-03
    
    **Maintainer:** [Name/Team]
    """)
    
    st.divider()
    
    st.markdown("**Feedback?**")
    st.markdown("[Open GitHub Issue](https://github.com/karlitos1337/5d/issues)")
```

---

## 📋 Checklist für neue Page

Vor Go-Live:

- [ ] **Header:** Titel + Emoji passend?
- [ ] **Info-Box:** Wissenschaftliche Basis erklärt? (✅⚠️🔮 Label)
- [ ] **Haupttext:** 200-400 Wörter, 3 Paragraphen?
- [ ] **Metrics:** 4 Spalten mit sinnvollen KPIs?
- [ ] **Formeln:** Mind. 3 Tabs (Hauptformel, ROI, Success Rate)?
- [ ] **LaTeX:** Formeln korrekt dargestellt?
- [ ] **Quellen:** Alle Formeln mit BibTeX-Keys referenziert?
- [ ] **Visualisierung:** Plotly/Folium Chart implementiert?
- [ ] **Mini-Map:** 700x350px, CartoDB positron, klickbare Marker?
- [ ] **Interaktives Tool:** Calculator/Simulation eingebettet?
- [ ] **Scientific References:** Mind. 3 peer-reviewed + 1 eigene Analyse + 2 Datenquellen?
- [ ] **Downloads:** CSV/PDF/BibTeX Buttons vorhanden?
- [ ] **Navigation:** Footer-Links zu anderen Pages?
- [ ] **Sidebar:** About-Sektion mit Last Updated, Maintainer, Feedback-Link?
- [ ] **Tests:** Entsprechende `tests/test_xxx.py` vorhanden? (Phase 8)

---

## 🎨 Design Guidelines

### Farbcodes (konsistent)

```python
# IMP-Scores
def get_imp_color(score):
    if score >= 0.70:
        return "green"  # 🟢 Hoch
    elif score >= 0.50:
        return "orange"  # 🟡 Mittel
    else:
        return "red"  # 🔴 Niedrig

# Evidenz-Labels
EVIDENZ_COLORS = {
    "✅ Fakt": "green",
    "⚠️ Hypothese": "orange",
    "🔮 Spekulation": "blue"
}
```

### Icon-Konventionen

- **📊** – Analysis, Charts
- **🚀** – Projects, ROI
- **📚** – Research, Literature
- **💻** – GitHub, Code
- **🧬** – Game of Life, Cellular Automata
- **🤝** – Non-Coercion, Cooperation
- **🌍** – World Map, Global Data
- **📈** – Projections, Future
- **🧠** – Autopoietic Class, Neuroscience
- **🕸️** – Participation Networks, Topology

### Layout-Standards

- **Page Width:** `layout="wide"`
- **Mini-Maps:** 700x350px
- **Full Maps:** 700x500px (World Map)
- **Column Layout:** 4 columns for metrics, 3 columns for navigation
- **Tabs:** Max 3-4 tabs per section (Formeln, Scenarios, etc.)

---

## 📖 Siehe auch

- **[TODO_MULTIPAGE.md](../TODO_MULTIPAGE.md)** – Phase 5 Progress Tracking
- **[50-UI-Tips](../docs/50-UI-Tips.md)** – UX Guidelines (if exists)
- **[LITERATUR_INDEX.md](../07_daten_analysen/LITERATUR_INDEX.md)** – 70 BibTeX sources
- **[CLAIMS_EVIDENCE_MATRIX.md](../docs/CLAIMS_EVIDENCE_MATRIX.md)** – Evidence labels for all claims

---

**Version:** 1.0  
**Last Updated:** 2025-12-03  
**Maintainer:** Siehe [CONTRIBUTING.md](../CONTRIBUTING.md)
