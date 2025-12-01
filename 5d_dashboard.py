#!/usr/bin/env python3
"""
5D Live Dashboard - Streamlit
Visualisiert IMP Scores, Projekte, Research, GitHub Trends
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Plotly optional laden (Fallback, falls nicht installiert)
try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

# Page Config
st.set_page_config(
    page_title="5D Intelligence Dashboard",
    page_icon="🎯",
    layout="wide"
)

@st.cache_data
def load_data():
    """Lädt alle 5D Daten"""
    data = {}
    
    try:
        with open('5d_solutions.json', 'r') as f:
            data['solutions'] = json.load(f)
    except:
        data['solutions'] = {'plan': {}, 'solutions': {}}
    
    try:
        with open('5d_research_data.json', 'r') as f:
            data['research'] = json.load(f)
    except:
        data['research'] = {}
    
    try:
        with open('5d_github_data.json', 'r') as f:
            data['github'] = json.load(f)
    except:
        data['github'] = {}
    
    return data

def create_imp_chart():
    """IMP Score Radar Chart"""
    if not HAS_PLOTLY:
        return None
    dimensions = ['Autonomie', 'Motivation', 'Resilienz', 'Partizipation', 'Authentizität']
    your_scores = [0.95, 0.88, 0.82, 0.79, 0.91]
    denmark_scores = [0.75, 0.70, 0.65, 0.75, 0.70]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=your_scores, theta=dimensions, fill='toself', name='5D Modell', line_color='#00ff00'))
    fig.add_trace(go.Scatterpolar(r=denmark_scores, theta=dimensions, fill='toself', name='Dänemark', line_color='#ff0000'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, title="IMP Score: 5D vs. Dänemark")
    return fig

def create_roi_chart(solutions):
    """ROI Visualization"""
    roi_data = solutions.get('solutions', {}).get('ROI', [])
    if not roi_data:
        roi_data = ['95', '485']
    # Robustes Parsen ("95", "485", "12,5" → float)
    roi_values = []
    for r in roi_data[:5]:
        try:
            roi_values.append(float(str(r).replace(',', '.')))
        except Exception:
            continue
    if not roi_values:
        roi_values = [0.0]
    
    if not HAS_PLOTLY:
        return None, roi_values
    fig = go.Figure(data=[go.Bar(x=['Projekt ' + str(i+1) for i in range(len(roi_values))], y=roi_values, marker_color='lightblue')])
    fig.update_layout(title="ROI der Bildungsprojekte (%)", xaxis_title="Projekte", yaxis_title="ROI %")
    return fig, roi_values


# --- Abschnitts-Renderer (für Tabs und Launcher) ---
def render_gol_demo(HAS_PLOTLY_local=None, key_prefix=""):
    """Render Conway's Game of Life Demo-Abschnitt (kapselt bisherigen Tab-Inhalt)."""
    st.header("Conway's Game of Life (Demo)")
    st.caption("Nicht-blockierende Mini-Demo. Für volle Kontrolle nutze `gol_streamlit.py` oder die CLI.")

    # Settings
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        preset = st.selectbox("Preset", ["glider", "blinker", "toad", "gosper", "lwss", "pulsar"], index=0, key=f"{key_prefix}gol_preset")
    with col_b:
        size = st.slider("Größe (N)", 10, 80, 30 if preset != "gosper" else 50, 1, key=f"{key_prefix}gol_size")
    with col_c:
        steps = st.slider("Steps", 1, 100, 10, 1, key=f"{key_prefix}gol_steps")

    # Local helpers (klein halten, keine I/O)
    import numpy as np
    def gol_step(g: np.ndarray) -> np.ndarray:
        rows, cols = g.shape
        neighbors = np.zeros((rows, cols), dtype=int)
        for i in range(rows):
            for j in range(cols):
                s = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue
                        s += g[(i+di) % rows, (j+dj) % cols]
                neighbors[i, j] = s
        newg = np.zeros_like(g)
        newg[(g == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
        newg[(g == 0) & (neighbors == 3)] = 1
        return newg

    def grid_for_preset(n: int, p: str) -> np.ndarray:
        grid = np.zeros((n, n), dtype=int)
        def place(r, c, arr):
            h, w = arr.shape
            max_h = min(h, max(0, n - r))
            max_w = min(w, max(0, n - c))
            if max_h <= 0 or max_w <= 0:
                return
            sub = arr[:max_h, :max_w]
            grid[r:r+max_h, c:c+max_w] = sub
        if p == 'glider':
            place(1,1, np.array([[0,1,0],[0,0,1],[1,1,1]], dtype=int))
        elif p == 'blinker':
            place(n//2, max(1, n//2-1), np.array([[1,1,1]], dtype=int))
        elif p == 'toad':
            place(n//2-1, max(1, n//2-2), np.array([[0,1,1,1],[1,1,1,0]], dtype=int))
        elif p == 'gosper':
            coords = [(0,24),(1,22),(1,24),(2,12),(2,13),(2,20),(2,21),(2,34),(2,35)]
            for di,dj in coords:
                i,j = 1+di, 1+dj
                if 0 <= i < n and 0 <= j < n:
                    grid[i,j] = 1
        elif p == 'lwss':
            place(max(1, n//2-2), max(1, n//2-3), np.array([[0,1,1,1,1],[1,0,0,0,1],[0,0,0,0,1],[1,0,0,1,0]], dtype=int))
        elif p == 'pulsar':
            base = np.zeros((17,17), dtype=int)
            pts = [
                (2,4),(2,5),(2,6),(2,10),(2,11),(2,12),
                (4,2),(5,2),(6,2),(4,7),(5,7),(6,7),(4,9),(5,9),(6,9),(4,14),(5,14),(6,14),
                (7,4),(7,5),(7,6),(7,10),(7,11),(7,12),
                (9,4),(9,5),(9,6),(9,10),(9,11),(9,12),
                (10,2),(11,2),(12,2),(10,7),(11,7),(12,7),(10,9),(11,9),(12,9),(10,14),(11,14),(12,14),
                (14,4),(14,5),(14,6),(14,10),(14,11),(14,12)
            ]
            for r,c in pts:
                if 0 <= r < 17 and 0 <= c < 17:
                    base[r,c] = 1
            place(max(1, n//2-8), max(1, n//2-8), base)
        return grid

    # Session State
    state_key = f"gol_grid_{preset}_{size}"
    if state_key not in st.session_state:
        st.session_state[state_key] = grid_for_preset(size, preset)
    grid = st.session_state[state_key]

    # Controls
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Step", key=f"{key_prefix}gol_step_btn"):
            grid = gol_step(grid)
    with c2:
        if st.button("10 Steps", key=f"{key_prefix}gol_10_btn"):
            for _ in range(10):
                grid = gol_step(grid)
    with c3:
        if st.button("Reset", key=f"{key_prefix}gol_reset_btn"):
            grid = grid_for_preset(size, preset)

    # Persist
    st.session_state[state_key] = grid

    # Plot (Plotly, kein Blocking)
    _HAS = HAS_PLOTLY if HAS_PLOTLY_local is None else HAS_PLOTLY_local
    if _HAS:
        import plotly.express as px
        st.plotly_chart(px.imshow(grid, color_continuous_scale='gray', origin='upper'), width='stretch')
    else:
        st.warning("Plotly nicht verfügbar – Textdarstellung des Grids:")
        st.text("\n".join("".join('#' if c else '.' for c in row) for row in grid))


def render_zwi_demo(HAS_PLOTLY_local=None, key_prefix=""):
    """Render Zwanglosigkeits-Spiel Abschnitt (kapselt bisherigen Tab-Inhalt)."""
    st.header("Zwanglosigkeits-Spiel (Non-Coercive Interaction)")
    st.caption("Modellierte, zwanglosigkeitsbasierte Wechselwirkungen: Kooperation mit beidseitiger Zustimmung vs. kurzfristige Zwangsgewinne.")

    ca, cb, cc = st.columns(3)
    with ca:
        z_n = st.slider("Agenten-Grid N", 10, 80, 30, 1, key=f"{key_prefix}zwi_n")
    with cb:
        z_coercer_ratio = st.slider("Anteil Zwinger (%)", 0, 100, 10, 1, key=f"{key_prefix}zwi_ratio")
    with cc:
        z_consent_thr = st.slider("Zustimmungsschwelle", 0.0, 1.0, 0.5, 0.01, key=f"{key_prefix}zwi_thr")

    import numpy as np
    rng = np.random.default_rng(42)

    def init_world(n: int, coercer_ratio: float):
        types = np.zeros((n, n), dtype=int)
        mask = rng.random((n, n)) < (coercer_ratio / 100.0)
        types[mask] = 1
        willingness = rng.uniform(0.6, 1.0, size=(n, n)).astype(np.float32)
        payoff = np.zeros((n, n), dtype=np.float32)
        return types, willingness, payoff

    def interaction_step(types, willingness, payoff, thr=0.5,
                          b_coop=0.5, b_coerce=0.4, pen_coerce=0.6,
                          rec=0.02, dec=0.05):
        n = types.shape[0]
        dirs = np.array([[-1,0],[1,0],[0,-1],[0,1]])
        for i in range(n):
            for j in range(n):
                di, dj = dirs[rng.integers(0, 4)]
                ni, nj = (i+di) % n, (j+dj) % n
                a_t, b_t = types[i,j], types[ni,nj]
                a_w, b_w = willingness[i,j], willingness[ni,nj]
                if a_t != 1 and b_t != 1 and a_w >= thr and b_w >= thr:
                    payoff[i,j] += b_coop
                    payoff[ni,nj] += b_coop
                    willingness[i,j] = min(1.0, a_w + rec)
                    willingness[ni,nj] = min(1.0, b_w + rec)
                elif a_t == 1 and b_w < thr:
                    payoff[i,j] += b_coerce
                    payoff[ni,nj] -= pen_coerce
                    willingness[ni,nj] = max(0.0, b_w - dec)
                elif b_t == 1 and a_w < thr:
                    payoff[ni,nj] += b_coerce
                    payoff[i,j] -= pen_coerce
                    willingness[i,j] = max(0.0, a_w - dec)
                else:
                    willingness[i,j] = min(1.0, a_w + rec*0.5)
                    willingness[ni,nj] = min(1.0, b_w + rec*0.5)
        return types, willingness, payoff

    key = f"zwi_{z_n}_{z_coercer_ratio}_{z_consent_thr:.2f}"
    if key not in st.session_state:
        st.session_state[key] = init_world(z_n, z_coercer_ratio)
    z_types, z_will, z_pay = st.session_state[key]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("Step (Zwanglos)", key=f"{key_prefix}zwi_step"):
            z_types, z_will, z_pay = interaction_step(z_types, z_will, z_pay, thr=z_consent_thr)
    with c2:
        if st.button("10 Steps (Zwanglos)", key=f"{key_prefix}zwi_10"):
            for _ in range(10):
                z_types, z_will, z_pay = interaction_step(z_types, z_will, z_pay, thr=z_consent_thr)
    with c3:
        if st.button("Reset (Zwanglos)", key=f"{key_prefix}zwi_reset"):
            z_types, z_will, z_pay = init_world(z_n, z_coercer_ratio)
    with c4:
        mode = st.selectbox("Visualisierung", ["Willingness", "Payoff", "Type"], index=0, key=f"{key_prefix}zwi_mode")

    st.session_state[key] = (z_types, z_will, z_pay)

    st.write(
        f"Durchschnittliche Bereitschaft: {float(np.mean(z_will)):.2f} | "
        f"Ø Payoff: {float(np.mean(z_pay)):.2f} | "
        f"Zwinger %: {float(np.mean(z_types==1)*100):.1f}%"
    )

    _HAS = HAS_PLOTLY if HAS_PLOTLY_local is None else HAS_PLOTLY_local
    if _HAS:
        import plotly.express as _px
        if mode == "Willingness":
            mat = z_will; color = 'Viridis'
        elif mode == "Payoff":
            mat = z_pay; color = 'Plasma'
        else:
            mat = z_types; color = 'Gray'
        st.plotly_chart(_px.imshow(mat, color_continuous_scale=color, origin='upper'), width='stretch')
    else:
        st.text("Plotly fehlt – einfache Textdarstellung:")
        st.text("\n".join("".join('C' if t==1 else ('·' if w<z_consent_thr else '+') for t,w in zip(row_t,row_w)) for row_t,row_w in zip(z_types, z_will)))

def main():
    """Hauptfunktion"""
    st.title("🎯 5D Intelligence Dashboard")
    st.markdown("**Autonomie × Motivation × Resilienz × Partizipation × Authentizität**")
    
    # Load Data
    data = load_data()
    solutions = data['solutions']
    research = data['research']
    github = data['github']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("IMP-Score", "0.77", "+25% vs DK")
    
    with col2:
        total_projects = len(set(solutions.get('solutions', {}).get('Projekte', [])))
        st.metric("Projekte", total_projects, "aktiv")
    
    with col3:
        roi_list = solutions.get('solutions', {}).get('ROI', ['485'])
        max_roi = max([float(r) for r in roi_list]) if roi_list else 0
        st.metric("Max ROI", f"{max_roi}%", "⭐")
    
    with col4:
        total_papers = sum(
            len(data.get('arxiv', [])) + len(data.get('pubmed', []))
            for data in research.values()
        )
        st.metric("Research Papers", total_papers, "🔍")
    
    # Tabs (Launcher + Inhalte)
    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["🧭 Launcher", "📊 IMP Analysis", "🚀 Projects", "📚 Research", "💻 GitHub", "🧬 Game of Life", "🤝 Zwanglosigkeit", "📜 Manifeste", "🌍 Weltgraphen", "📈 X‑Y Graphen", "🧪 Test Graph"]) 

    # Launcher: Kategorien + Startbefehle/Verweise
    with tab0:
        st.header("Launcher – Tests, Demos & Simulationen")
        st.caption("Kopiere den Startbefehl oder wechsle zum passenden Tab.")

        cA, cB = st.columns(2)
        with cA:
            st.subheader("Demos & Modelle")
            st.markdown("- Gehe zu Tab: 🧬 Game of Life (integriert)")
            st.markdown("- Gehe zu Tab: 🤝 Zwanglosigkeit (integriert)")
            st.markdown("- Externe GoL‑App (vollständige Kontrolle):")
            st.code("streamlit run gol_streamlit.py", language="bash")
            st.markdown("- Externes Zwanglosigkeits‑UI:")
            st.code("streamlit run zwi_streamlit.py", language="bash")
            st.divider()
            cA1, cA2 = st.columns(2)
            with cA1:
                if st.button("🧬 Game of Life hier öffnen", key="launcher_open_gol"):
                    st.session_state["launcher_show_gol"] = True
            with cA2:
                if st.button("🤝 Zwanglosigkeit hier öffnen", key="launcher_open_zwi"):
                    st.session_state["launcher_show_zwi"] = True
        with cB:
            st.subheader("Simulationen")
            st.markdown("- Autopoietische Klasse:")
            st.code("streamlit run autopoietic_streamlit.py", language="bash")
            st.markdown("- Partizipations‑Netzwerke:")
            st.code("streamlit run partnet_streamlit.py", language="bash")

        st.divider()
        cC, cD = st.columns(2)
        with cC:
            st.subheader("Kern‑Tools (CLI)")
            st.markdown("- Extractor → `5d_solutions.json`")
            st.code("python 5d_extractor.py", language="bash")
            st.markdown("- Research Scraper → `5d_research_data.json`")
            st.code("python 5d_research_scraper.py", language="bash")
            st.markdown("- GitHub Explorer → `5d_github_data.json`")
            st.code("python 5d_github_api.py", language="bash")
        with cD:
            st.subheader("Workflows & Optionales")
            st.markdown("- Komplettlauf inkl. Dashboard:")
            st.code("./RUN_ALL.sh", language="bash")
            st.markdown("- Externe Lösungen mergen:")
            st.code("python merge_external_solutions.py", language="bash")
            st.markdown("- Resonanz→IMP Vorschläge:")
            st.code("python apply_resonance_mapping.py", language="bash")
            st.markdown("- Manifest‑Zusammenfassung erzeugen:")
            st.code("python manifest_summary.py", language="bash")

        # Inline-Render der Demos im Launcher (optional)
        if st.session_state.get("launcher_show_gol"):
            st.divider()
            st.subheader("🧬 Game of Life – Inline")
            render_gol_demo(key_prefix="launcher_")
        if st.session_state.get("launcher_show_zwi"):
            st.divider()
            st.subheader("🤝 Zwanglosigkeit – Inline")
            render_zwi_demo(key_prefix="launcher_")
    
    with tab1:
        st.header("IMP Score Analyse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            imp_fig = create_imp_chart()
            if imp_fig is not None:
                st.plotly_chart(imp_fig, width='stretch')
            else:
                st.warning("Plotly nicht installiert – zeige Balkendiagramm als Fallback.")
                import pandas as _pd
                _dims = ['Autonomie', 'Motivation', 'Resilienz', 'Partizipation', 'Authentizität']
                _vals = [0.95, 0.88, 0.82, 0.79, 0.91]
                _df = _pd.DataFrame({'Dimension': _dims, 'Score': _vals}).set_index('Dimension')
                st.bar_chart(_df)
        
        with col2:
            st.subheader("5D Dimensionen")
            st.markdown("""
            **Autonomie (A):** 0.95 ✅  
            Freie Projektwahl, Selbstbestimmung
            
            **Motivation (IM):** 0.88 ✅  
            Intrinsische Neugier, Flow-Zustände
            
            **Resilienz (R):** 0.82 ✅  
            Polyvagal-Safety, Fehlerkultur
            
            **Partizipation (SP):** 0.79 ✅  
            Kooperation, Tokkatsu, Netzwerk
            
            **Authentizität (Au):** 0.91 ✅  
            Kongruenz, Wahrheit, Selbstausdruck
            """)
            # Formel und verifizierte Berechnung
            try:
                from models.imp import calculate_imp_verified
                dims = {'A': 0.95, 'IM': 0.88, 'R': 0.82, 'SP': 0.79, 'Au': 0.91}
                res = calculate_imp_verified(dims)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("IMP (multiplikativ)", f"{res['raw_multiplicative']:.3f}", "Mathematisch korrekt")
                with c2:
                    st.metric("IMP (gewichtet)", f"{res['weighted_additive']:.3f}", "Falls Adjustment")
                with c3:
                    st.metric("IMP (normiert)", f"{res['normalized']:.3f}")
                st.code(f"""
Formel: {res['formula_used']}
A={dims['A']} × IM={dims['IM']} × R={dims['R']} × SP={dims['SP']} × Au={dims['Au']}
= {res['raw_multiplicative']:.3f}
""")
                st.warning("⚠️ Falls 0.77 verwendet wird, MUSS Berechnungsweg dokumentiert sein!")
            except Exception:
                st.info("Formel-Berechnung nicht verfügbar. Stelle sicher, dass `models/imp.py` existiert.")
    
    with tab2:
        st.header("Action Plan & Projekte")
        
        # Action Plan
        plan = solutions.get('plan', {})
        for phase, action in plan.items():
            st.markdown(f"**{phase}:** {action}")
        
        st.divider()
        
        # ROI Chart
        roi_fig, roi_values = create_roi_chart(solutions)
        if roi_fig is not None:
            st.plotly_chart(roi_fig, width='stretch')
        else:
            st.warning("Plotly fehlt – zeige Balkendiagramm als Fallback.")
            import pandas as _pd
            if not roi_values:
                roi_values = [0.0]
            _df = _pd.DataFrame({'Projekt': [f'P{i+1}' for i in range(len(roi_values))], 'ROI': roi_values}).set_index('Projekt')
            st.bar_chart(_df)
        
        # Projekte
        projekte = list(set(solutions.get('solutions', {}).get('Projekte', [])))
        if projekte:
            st.subheader("Aktive Projekte")
            cols = st.columns(len(projekte[:4]))
            for i, projekt in enumerate(projekte[:4]):
                with cols[i]:
                    st.markdown(f"**{projekt}**")
                    st.progress(0.75)
    
    with tab3:
        st.header("Research Updates")
        
        if research:
            for keyword, data in list(research.items())[:3]:
                with st.expander(f"📚 {keyword}"):
                    
                    st.subheader("arXiv Papers")
                    for paper in data.get('arxiv', [])[:3]:
                        st.markdown(f"**[{paper['title']}]({paper['link']})**")
                        st.caption(f"Autoren: {', '.join(paper['authors'][:3])}")
                        st.text(paper['summary'][:150] + "...")
                        st.divider()
                    
                    st.subheader("PubMed Papers")
                    for paper in data.get('pubmed', [])[:3]:
                        st.markdown(f"**[{paper['title']}]({paper['link']})**")
                        st.caption(f"Published: {paper['published']}")
                        st.divider()
        else:
            st.warning("Keine Research-Daten. Führe `python 5d_research_scraper.py` aus.")
    
    with tab4:
        st.header("GitHub Trends")
        
        repos = github.get('repositories', {})
        if repos:
            for query, repo_list in list(repos.items())[:3]:
                with st.expander(f"💻 {query}"):
                    for repo in repo_list[:5]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**[{repo['name']}]({repo['url']})**")
                            st.caption(repo.get('description', 'No description'))
                        with col2:
                            st.metric("⭐", repo['stars'])
                        st.divider()
        else:
            st.warning("Keine GitHub-Daten. Führe `python 5d_github_api.py` aus.")

        # Trending Topics (optional Zusatzdaten)
        trending = github.get('trending', {})
        if trending:
            st.subheader("Trending Topics")
            for topic, items in list(trending.items())[:4]:
                with st.expander(f"🔥 {topic}"):
                    for item in items:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**[{item['name']}]({item['url']})**")
                        with col2:
                            st.metric("⭐", item.get('stars', 0))
                        st.divider()

    with tab5:
        render_gol_demo(key_prefix="tab5_")
    
    with tab6:
        render_zwi_demo(key_prefix="tab6_")

    with tab7:
        st.header("Manifeste – Zusammenfassung & Quellen")
        st.caption("Automatisch extrahierte Übersichten aus `manifest/**`. Externe Quellen dienen als Bezug; eigene Texte werden nicht als Autorität gewertet.")

        import os, json
        summary_md_path = "manifest_summary.md"
        summary_json_path = "manifest_summary.json"
        research_json_path = "5d_research_data.json"
        left, right = st.columns([2, 1])
        with left:
            # Filter & Suche
            q = st.text_input("Suche (Titel/Abschnitt)", value="")
            cat = st.text_input("Kategorie (optional)", value="")
            level = st.slider("Ebene (min/max)", 1, 6, (1, 6))
            # Laden JSON
            items = []
            research = {}
            if os.path.exists(summary_json_path):
                try:
                    with open(summary_json_path, "r", encoding="utf-8") as f:
                        data_js = json.load(f)
                        items = data_js.get("items", [])
                except Exception:
                    st.error("Fehler beim Laden `manifest_summary.json`.")
            else:
                st.warning("Keine `manifest_summary.json` gefunden. Bitte `python manifest_summary.py` ausführen.")
            if os.path.exists(research_json_path):
                try:
                    with open(research_json_path, "r", encoding="utf-8") as f:
                        research = json.load(f)
                except Exception:
                    st.error("Fehler beim Laden `5d_research_data.json`.")

            # Filter anwenden
            def match(item):
                if cat and str(item.get("category", "")) != cat:
                    return False
                secs = item.get("sections", [])
                if not secs:
                    return False
                for s in secs:
                    lvl = int(s.get("level", 1))
                    if not (level[0] <= lvl <= level[1]):
                        continue
                    text = (s.get("title", "") + " " + s.get("summary", "")).lower()
                    if q.lower() in text:
                        return True
                return False

            filtered = [it for it in items if match(it)] if q or cat or level != (1,6) else items

            # Anzeige
            for it in filtered[:200]:
                st.markdown(f"### Datei: {it.get('file','')}")
                st.caption(f"Kategorie: {it.get('category','root')}")
                for s in it.get("sections", []):
                    lvl = int(s.get("level", 1))
                    if not (level[0] <= lvl <= level[1]):
                        continue
                    title = s.get("title", "(ohne Titel)")
                    summary = s.get("summary", "")
                    st.markdown(f"**{title}** (Ebene {lvl})")
                    if summary:
                        st.write(summary)
                    # Relevante externe Referenzen (arXiv/PubMed) aus research-Daten anhand von Titel-Schlüsselwörtern
                    # einfache Heuristik: exakte Keyword-Treffer in research.keys()
                    related = []
                    try:
                        for k, v in research.items():
                            key = str(k).lower()
                            if key and key in title.lower():
                                related.append((k, v))
                    except Exception:
                        pass
                    if related:
                        with st.expander("Externe Referenzen (arXiv/PubMed)"):
                            for k, v in related[:3]:
                                st.markdown(f"- Thema: `{k}`")
                                for p in v.get("arxiv", [])[:2]:
                                    st.markdown(f"  - arXiv: [{p.get('title','')}]({p.get('link','')})")
                                for p in v.get("pubmed", [])[:2]:
                                    st.markdown(f"  - PubMed: [{p.get('title','')}]({p.get('link','')})")
                st.divider()

        with right:
            st.subheader("Downloads & Hinweise")
            if os.path.exists(summary_md_path):
                with open(summary_md_path, "r", encoding="utf-8") as f:
                    st.download_button("Markdown herunterladen", f.read(), file_name="manifest_summary.md", mime="text/markdown")
            else:
                st.info("`manifest_summary.md` wird nach Generierung hier zum Download angeboten.")
            if os.path.exists(summary_json_path):
                with open(summary_json_path, "r", encoding="utf-8") as f:
                    st.download_button("JSON herunterladen", f.read(), file_name="manifest_summary.json", mime="application/json")
            else:
                st.info("`manifest_summary.json` wird nach Generierung hier zum Download angeboten.")
            st.subheader("Externe Quellen bevorzugen")
            st.markdown("- Bewertung/Validierung anhand externer und überprüfbarer Quellen (arXiv/PubMed, externe Repos)")
            st.markdown("- Eigene Manifeste dienen als Themenindex und Navigationshilfe, nicht als Primärquelle")

            st.subheader("IMP-Berechnung (transparent)")
            A = st.slider("Autonomie", 0.0, 1.0, 0.95)
            IM = st.slider("Motivation", 0.0, 1.0, 0.88)
            R = st.slider("Resilienz", 0.0, 1.0, 0.82)
            SP = st.slider("Partizipation", 0.0, 1.0, 0.79)
            Au = st.slider("Authentizität", 0.0, 1.0, 0.91)
            try:
                from models.imp import calculate_imp_verified
                res = calculate_imp_verified({'A': A, 'IM': IM, 'R': R, 'SP': SP, 'Au': Au})
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("IMP (multiplikativ)", f"{res['raw_multiplicative']:.3f}")
                with c2:
                    st.metric("IMP (gewichtet)", f"{res['weighted_additive']:.3f}")
                st.caption(f"Formel: {res['formula_used']} • Normalisiert: {res['normalized']:.3f}")
            except Exception:
                imp_raw = A * IM * R * SP * Au
                weights = {'A': 1.1, 'IM': 1.05, 'R': 1.0, 'SP': 0.95, 'Au': 1.0}
                imp_weighted = (A * weights['A'] + IM * weights['IM'] + R * weights['R'] + SP * weights['SP'] + Au * weights['Au']) / sum(weights.values())
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("IMP (multiplikativ)", f"{imp_raw:.3f}")
                with c2:
                    st.metric("IMP (gewichtet)", f"{imp_weighted:.3f}")

    with tab8:
        st.header("Weltgraphen – Themen • Papers • Repos")
        st.caption("Netzwerkansicht: Verbindet Research‑Themen mit Papers und GitHub‑Repos.")

        # Build simple network graph from research + github
        try:
            import networkx as nx
            import plotly.graph_objects as _go
            G = nx.Graph()
            # Add topic nodes
            topics = list(research.keys())[:8]
            for t in topics:
                G.add_node(f"T:{t}", kind="topic")
                for p in research.get(t, {}).get('arxiv', [])[:3]:
                    pid = f"A:{p.get('title','')[:40]}"  # shorten
                    G.add_node(pid, kind="paper")
                    G.add_edge(f"T:{t}", pid)
                for p in research.get(t, {}).get('pubmed', [])[:2]:
                    pid = f"P:{p.get('title','')[:40]}"
                    G.add_node(pid, kind="paper")
                    G.add_edge(f"T:{t}", pid)
            # Link github repos to closest matching topics (name contains keyword)
            repos = github.get('repositories', {})
            for t in topics:
                for repo in repos.get(t, [])[:3]:
                    rid = f"R:{repo.get('name','')[:40]}"
                    G.add_node(rid, kind="repo")
                    G.add_edge(f"T:{t}", rid)

            if len(G.nodes) == 0:
                st.warning("Keine Daten für Weltgraph – bitte Scraper/Explorer ausführen.")
            else:
                pos = nx.spring_layout(G, seed=42, k=0.6)
                # Build edges for plotly
                edge_x, edge_y = [], []
                for u, v in G.edges():
                    x0, y0 = pos[u]
                    x1, y1 = pos[v]
                    edge_x += [x0, x1, None]
                    edge_y += [y0, y1, None]
                edge_trace = _go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#888'), hoverinfo='none')
                # Build node traces by kind
                def node_trace(kind, color, size):
                    xs, ys, texts = [], [], []
                    for n, d in G.nodes(data=True):
                        if d.get('kind') == kind:
                            x, y = pos[n]
                            xs.append(x); ys.append(y); texts.append(n[2:])
                    return _go.Scatter(x=xs, y=ys, mode='markers+text', text=texts, textposition='top center',
                                       marker=dict(size=size, color=color, opacity=0.85), name=kind)
                fig = _go.Figure(data=[edge_trace,
                                        node_trace('topic', '#1f77b4', 14),
                                        node_trace('paper', '#2ca02c', 10),
                                        node_trace('repo', '#ff7f0e', 12)])
                fig.update_layout(showlegend=True, title="Weltgraph: Topics ↔ Papers ↔ Repos",
                                  margin=dict(l=10, r=10, t=40, b=10), xaxis=dict(visible=False), yaxis=dict(visible=False))
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("NetworkX/Plotly nicht verfügbar – installiere mit: pip install networkx plotly")

    with tab9:
        st.header("X‑Y Graphen nach 5D‑Prinzip")
        st.caption("Unabhängige, einfache Streudiagramme: Dimension vs. Wirtschafts-Schadindex (synthetisch).")
        # Erzeuge unabhängige, synthetische Daten (keine Abhängigkeit von Scraper)
        import numpy as _np
        _rng = _np.random.default_rng(5)
        # 5D Dimensionen (Schieberegler zur Grundlage)
        cA, cB, cC, cD, cE = st.columns(5)
        with cA:
            _A = st.slider("A", 0.0, 1.0, 0.75)
        with cB:
            _IM = st.slider("IM", 0.0, 1.0, 0.70)
        with cC:
            _R = st.slider("R", 0.0, 1.0, 0.65)
        with cD:
            _SP = st.slider("SP", 0.0, 1.0, 0.75)
        with cE:
            _Au = st.slider("Au", 0.0, 1.0, 0.70)

        st.markdown("""
        Nach 5D‑Prinzip: Höhere Werte in A/IM/R/SP/Au reduzieren systemische Schäden (Kurzfrist‑Profit ≠ Langfrist‑Wohl).
        Wir zeigen synthetisch: je höher die Dimension, desto niedriger ein "Wirtschafts‑Schadindex" (WSI).
        """)

        # Synthetischer WSI: invers zu Dimension + Rauschen
        def mk_series(base, n=200):
            x = _rng.uniform(0.0, 1.0, n)
            # Schadindex fällt mit x und Grundniveau base
            y = (1.0 - x) * (1.0 - base) + _rng.normal(0, 0.05, n)
            return x, y
        pairs = {
            'Autonomie (A)': mk_series(_A),
            'Motivation (IM)': mk_series(_IM),
            'Resilienz (R)': mk_series(_R),
            'Partizipation (SP)': mk_series(_SP),
            'Authentizität (Au)': mk_series(_Au),
        }

        # Visualisierung: Plotly oder Fallback
        try:
            import plotly.graph_objects as _go
            _fig = _go.Figure()
            palette = {
                'Autonomie (A)': '#1f77b4',
                'Motivation (IM)': '#ff7f0e',
                'Resilienz (R)': '#2ca02c',
                'Partizipation (SP)': '#9467bd',
                'Authentizität (Au)': '#8c564b',
            }
            for name, (x, y) in pairs.items():
                _fig.add_trace(_go.Scatter(x=x, y=y, mode='markers', name=name,
                                           marker=dict(size=6, color=palette.get(name, '#333'), opacity=0.7)))
            _fig.update_layout(title="WSI vs. Dimension (synthetisch)",
                               xaxis_title="Dimension (0..1)", yaxis_title="Wirtschafts‑Schadindex (niedriger = besser)",
                               legend=dict(orientation='h'))
            st.plotly_chart(_fig, use_container_width=True)
        except Exception:
            st.warning("Plotly nicht verfügbar – Fallback Tabellenansicht.")
            import pandas as _pd
            rows = []
            for name, (x, y) in pairs.items():
                for xi, yi in zip(x[:50], y[:50]):
                    rows.append({'Dimension': name, 'x': float(xi), 'WSI': float(yi)})
            st.dataframe(_pd.DataFrame(rows))

        st.divider()
        st.subheader("Zukunftsauswirkungs‑Graph (projiziert)")
        st.caption("Hypothetische Entwicklung des Wirtschafts‑Schadindex (WSI) über die Zeit bei 5D‑Adoption.")
        # Sektoren: Autofahren (1D/Verbrenner), Fliegen, Schifffahrt
        c1, c2, c3 = st.columns(3)
        with c1:
            adopt_auto = st.slider("Auto 5D‑Adoption (Jahre bis 50%)", 1, 20, 8)
        with c2:
            adopt_flight = st.slider("Flug 5D‑Adoption (Jahre bis 50%)", 1, 30, 15)
        with c3:
            adopt_ship = st.slider("Schiff 5D‑Adoption (Jahre bis 50%)", 1, 30, 20)

        # Projektionsmodell: WSI_t = WSI0 * (1 - adoption_curve(t)) + noise
        # adoption_curve(t) ~ logistic mit T50 = adopt_*
        _T = 30
        _t = _np.arange(0, _T)
        def logistic_adopt(t, T50):
            k = 0.25  # Steilheit
            return 1.0 / (1.0 + _np.exp(-k * (t - T50)))
        base = { 'Auto': 0.8, 'Flug': 0.9, 'Schiff': 0.85 }  # aktueller hoher Schaden
        T50s = { 'Auto': adopt_auto, 'Flug': adopt_flight, 'Schiff': adopt_ship }
        proj = {}
        for name in base:
            curve = logistic_adopt(_t, T50s[name])
            wsi = base[name] * (1.0 - 0.6 * curve) + _rng.normal(0, 0.02, _T)  # 60% Reduktion bei hoher Adoption
            proj[name] = wsi.clip(0.0, 1.0)

        try:
            import plotly.graph_objects as _go
            fig2 = _go.Figure()
            palette2 = { 'Auto': '#d62728', 'Flug': '#17becf', 'Schiff': '#7f7f7f' }
            for name, y in proj.items():
                fig2.add_trace(_go.Scatter(x=list(_t), y=list(y), mode='lines', name=name,
                                           line=dict(width=3, color=palette2.get(name, '#333'))))
            fig2.update_layout(title="WSI Projektion bei 5D‑Adoption",
                               xaxis_title="Jahre", yaxis_title="WSI (niedriger = besser)",
                               legend=dict(orientation='h'))
            st.plotly_chart(fig2, use_container_width=True)
        except Exception:
            st.warning("Plotly nicht verfügbar – einfache Tabelle.")
            import pandas as _pd
            dfp = _pd.DataFrame({ 'Jahr': _t, **proj })
            st.dataframe(dfp.head(15))

    with tab10:
        st.header("Test Graph – Kopie IMP Radar")
        st.caption("Unabhängiger Test: gleiche Darstellung wie IMP‑Radar, mit einstellbaren Werten.")
        dims = ['Autonomie', 'Motivation', 'Resilienz', 'Partizipation', 'Authentizität']
        cA, cB, cC, cD, cE = st.columns(5)
        with cA:
            tA = st.slider("A", 0.0, 1.0, 0.95, 0.01)
        with cB:
            tIM = st.slider("IM", 0.0, 1.0, 0.88, 0.01)
        with cC:
            tR = st.slider("R", 0.0, 1.0, 0.82, 0.01)
        with cD:
            tSP = st.slider("SP", 0.0, 1.0, 0.79, 0.01)
        with cE:
            tAu = st.slider("Au", 0.0, 1.0, 0.91, 0.01)
        vals = [tA, tIM, tR, tSP, tAu]
        # Plotly Radar oder Fallback
        try:
            import plotly.graph_objects as _go
            fig = _go.Figure()
            fig.add_trace(_go.Scatterpolar(r=vals, theta=dims, fill='toself', name='Test 5D', line_color='#00aa00'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, title="Test: IMP‑Radar")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Plotly nicht verfügbar – Balken‑Fallback.")
            import pandas as _pd
            _df = _pd.DataFrame({'Dimension': dims, 'Score': vals}).set_index('Dimension')
            st.bar_chart(_df)

    # Footer
    st.divider()
    st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 5D Framework v1.0")

if __name__ == "__main__":
    main()
