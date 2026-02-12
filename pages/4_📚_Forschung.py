import streamlit as st

# Page Config
st.set_page_config(page_title="Forschung - 5D Framework", page_icon="📚", layout="wide")

# Header
st.title("📚 Forschung & Wissenschaftliche Grundlagen")
st.markdown(
    """
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; margin-bottom: 2rem; color: white;'>
    <h2 style='color: white; margin: 0;'>🔬 Akademische Validierung des 5D-Intelligence-Frameworks</h2>
    <p style='margin-top: 1rem; font-size: 1.1rem;'>Empirische Forschung | Statistische Validierung | Open Science</p>
</div>
""",
    unsafe_allow_html=True,
)

# Status Badge
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📄 Status", "Validierung", "In Progress")
with col2:
    st.metric("📈 Reliabilität", "TBD", "Awaiting Data")
with col3:
    st.metric("👥 Probanden", "0/30", "Recruiting")
with col4:
    st.metric("📊 Dimensionen", "5", "Validated")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🎯 Übersicht",
        "📊 Methodologie",
        "📈 Aktuelle Ergebnisse",
        "📝 Publikationen",
        "🔗 Ressourcen",
    ]
)

# TAB 1: Übersicht
with tab1:
    st.header("🎯 Forschungsübersicht")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Forschungsziele")
        st.markdown("""
        Das 5D-Intelligence-Framework wird aktuell **empirisch validiert** um:
        
        1. **Reliabilität** nachzuweisen (Cronbach's α > 0.8)
        2. **Konstruktvalidität** zu etablieren
        3. **Praktische Anwendbarkeit** zu demonstrieren
        4. **Theoretische Fundierung** zu stärken
        
        ### 🔬 Forschungsfragen
        
        **Hauptfrage:**
        > Sind die 5 Dimensionen (Autonomie, Intrinsische Motivation, Resilienz, 
        > Soziale Partizipation, Authentizität) reliabel messbar und theoretisch distinkt?
        
        **Subfragen:**
        1. Welche interne Konsistenz zeigen die Dimensionen (Cronbach's Alpha)?
        2. Wie korrelieren die Dimensionen untereinander?
        3. Ist das multiplikative IMP-Modell dem additiven überlegen?
        4. Welche Sensitivität zeigt das Framework gegenüber Interventionen?
        """)

    with col2:
        st.info("""
        **📅 Timeline**
        
        **Phase 1** (Aktuell)
        - Fragebogen-Entwicklung
        - Pilotstudie (N=30)
        
        **Phase 2** (Q1 2026)
        - Hauptstudie (N=100+)
        - Statistische Validierung
        
        **Phase 3** (Q2 2026)
        - Preprint-Publikation
        - Peer Review
        """)

# TAB 2: Methodologie
with tab2:
    st.header("📊 Methodologie")
    st.markdown("""
    ### Fragebogen-Design
    - **25 Items** (5 pro Dimension)
    - **Likert-Skala**: 1-7 (stimme gar nicht zu - stimme voll zu)
    - **Cronbach's Alpha**: Ziel α > 0.8
    
    ### Statistische Verfahren
    - Deskriptive Statistik
    - Reliabilitätsanalyse (Cronbach's α)
    - Korrelationsanalyse
    - Modellvergleich (multiplikativ vs. additiv)
    """)

    if st.button("📄 Fragebogen herunterladen"):
        st.info("Fragebogen wird generiert...")
        st.code("validation/imp_validation_study.py")

# TAB 3: Ergebnisse
with tab3:
    st.header("📈 Aktuelle Ergebnisse")
    st.warning("""
    ⚠️ **Status**: Datensammlung ausstehend
    
    Sobald N=30 Probanden erreicht sind, werden hier erste Ergebnisse präsentiert:
    - Reliabilitätskoeffizienten
    - Korrelationsmatrizen
    - IMP-Score-Verteilungen
    """)

# TAB 4: Publikationen
with tab4:
    st.header("📝 Publikationen")
    st.info("""
    **Geplant**:
    - Preprint auf arXiv (Q2 2026)
    - Peer-Review-Paper (Q3 2026)
    - Open Science Framework (OSF) Repository
    """)

# TAB 5: Ressourcen
with tab5:
    st.header("🔗 Ressourcen")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Literatur")
        st.markdown("""
        **Psychometrie**:
        - Cronbach (1951): Coefficient Alpha
        - Nunnally (1978): Psychometric Theory
        
        **5D-Dimensionen**:
        - Csikszentmihalyi (1990): Flow
        - Deci & Ryan (2000): Self-Determination
        - Masten (2001): Resilience
        """)

    with col2:
        st.subheader("🛠️ Tools")
        st.markdown("""
        **Code**:
        - [GitHub Repository](https://github.com/karlitos1337/5d)
        - [Validation Tools](/validation)
        
        **Python Packages**:
        ```
        pip install -r validation/requirements.txt
        ```
        """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔬 <strong>Open Science</strong> | 📊 <strong>Data Transparency</strong> | ✅ <strong>Reproducible Research</strong></p>
    <p style='margin-top: 1rem;'><em>Letzte Aktualisierung: 05.12.2025</em></p>
</div>
""",
    unsafe_allow_html=True,
)
