#!/usr/bin/env python3
"""
Page 10: Participation Networks - Network Topology & Knowledge Diffusion Simulation
====================================================================================

**Scientific Basis:**
- Granovetter (1973): Strength of Weak Ties - information diffusion through weak connections
- Watts & Strogatz (1998): Small-world networks - clustering + short paths
- Barabási & Albert (1999): Scale-free networks - preferential attachment
- Rogers (2003): Diffusion of Innovations - adoption through social networks

**5D Connection:**
- Social Participation (SP): Network density, clustering, connectedness
- Resilience (R): Network robustness (avg path length, diameter)
- Intrinsic Motivation (IM): Sharing probability, voluntary participation

**Network Topologies:**
1. Erdős-Rényi: Random connections (baseline)
2. Watts-Strogatz: Small-world (high clustering, low path length)
3. Barabási-Albert: Scale-free (hubs, power-law distribution)
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import numpy as np
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(
    page_title="Participation Networks",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== HEADER ====================
st.title("🕸️ Partizipations-Netzwerke")
st.markdown("""
**Agent-Based Simulation von Wissens-Diffusion in sozialen Netzwerken**

Diese Seite untersucht, wie **Netzwerk-Topologien** die Verbreitung von Wissen, Ideen und Innovationen beeinflussen.
Wir vergleichen drei klassische Modelle und zeigen ihre Relevanz für **Social Participation (SP)** und **Resilience (R)**.
""")

# Scientific context in sidebar
with st.sidebar:
    st.header("Wissenschaftlicher Kontext")
    
    with st.expander("🔬 Netzwerk-Theorie", expanded=False):
        st.markdown("""
**Granovetter (1973) - Weak Ties:**
- Starke Verbindungen (Familie): redundante Information
- Schwache Verbindungen (Bekannte): neue Informationen
- **Paradox:** Weak ties sind wichtiger für Innovation

**Watts & Strogatz (1998) - Small-World:**
- Hohe Clusterbildung (wie bei Gittern)
- Kurze Pfadlängen (wie bei zufälligen Graphen)
- **Realwelt:** Soziale Netzwerke, Gehirn, Stromnetze

**Barabási & Albert (1999) - Scale-Free:**
- Hubs (hoch vernetzte Knoten)
- Power-Law-Verteilung: P(k) ~ k^(-γ)
- **Beispiele:** Internet, Flughäfen, Proteinnetze
""")
    
    with st.expander("📊 5D-Dimensionen", expanded=False):
        st.markdown("""
**Social Participation (SP):**
- Clustering-Koeffizient (lokale Dichte)
- Finale Aktivierungsrate (Teilnahme)

**Resilience (R):**
- Kurze Pfadlängen (schnelle Erholung)
- Zeit bis 50% Aktivierung (Robustheit)

**Intrinsic Motivation (IM):**
- Sharing-Wahrscheinlichkeit (freiwillig)
- Aktivierungs-Schwelle (Motivation)
""")

st.divider()

# ==================== SIDEBAR PARAMETERS ====================
with st.sidebar:
    st.header("🎛️ Simulation Parameter")
    
    # Network topology
    topology = st.selectbox(
        "Netzwerk-Topologie",
        ["small_world", "erdos_renyi", "scale_free"],
        index=0,
        help="Small-world: realistisch, Erdős-Rényi: Baseline, Scale-free: Hubs"
    )
    
    # Network size
    n_nodes = st.slider(
        "Anzahl Knoten",
        min_value=20,
        max_value=500,
        value=100,
        step=10,
        help="Größeres Netzwerk = realistischer, aber langsamer"
    )
    
    # Topology-specific parameters
    if topology == "small_world":
        k = st.slider("Nachbarn k", 2, 20, 6, help="Ausgangsgitter-Konnektivität")
        p = st.slider("Rewire-Wahrscheinlichkeit", 0.001, 0.5, 0.05, step=0.001, help="Höher = mehr Shortcuts")
    elif topology == "erdos_renyi":
        p = st.slider("Kantenwahrscheinlichkeit p", 0.001, 0.2, 0.05, step=0.001, help="Durchschnittlicher Grad ≈ p×n")
        k = 4  # dummy
    else:  # scale_free
        k = st.slider("Initiale Kanten m", 1, 10, 3, help="Neue Knoten verbinden sich mit m existierenden")
        p = 0.05  # dummy
    
    st.divider()
    
    # Diffusion parameters
    st.subheader("Diffusions-Parameter")
    
    seed_frac = st.slider(
        "Initiale Aktivierung (%)",
        min_value=1,
        max_value=50,
        value=5,
        help="Anteil der initial aktiven Knoten"
    ) / 100.0
    
    threshold = st.slider(
        "Aktivierungs-Schwelle",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Anteil aktiver Nachbarn nötig zur Aktivierung"
    )
    
    share_prob = st.slider(
        "Sharing-Wahrscheinlichkeit",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05,
        help="Bereitschaft, Wissen zu teilen (IM-Proxy)"
    )
    
    meeting_cost = st.slider(
        "Meeting-Kosten",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Reibungsverluste (Zeit, Aufwand)"
    )
    
    steps = st.slider(
        "Simulations-Schritte",
        min_value=10,
        max_value=500,
        value=100,
        help="Mehr Schritte = längere Laufzeit"
    )
    
    st.divider()
    
    # Display options
    st.subheader("Anzeige-Optionen")
    show_network_viz = st.checkbox("Netzwerk visualisieren", value=False, help="Kann bei >100 Knoten langsam sein")
    show_degree_dist = st.checkbox("Grad-Verteilung", value=True)

# ==================== SIMULATION ====================
@st.cache_data
def run_network_simulation(topology, n_nodes, k, p, steps, seed_frac, threshold, share_prob, meeting_cost):
    """
    Run knowledge diffusion simulation on different network topologies.
    
    Returns:
        - G: NetworkX graph
        - history: dict with step, active_frac, active_count
        - metrics: network and diffusion metrics
        - IMP_proxies: estimated 5D dimension scores
    """
    # Generate network
    if topology == "erdos_renyi":
        G = nx.erdos_renyi_graph(n=n_nodes, p=p, seed=42)
    elif topology == "small_world":
        G = nx.watts_strogatz_graph(n=n_nodes, k=k, p=p, seed=42)
    else:  # scale_free
        G = nx.barabasi_albert_graph(n=n_nodes, m=k, seed=42)
    
    # Initial activation (random seed nodes)
    rng = np.random.default_rng(42)
    active = {node: (rng.random() < seed_frac) for node in G.nodes}
    
    # History tracking
    history = {"step": [], "active_frac": [], "active_count": []}
    
    # Diffusion simulation (threshold model with probabilistic sharing)
    for t in range(steps):
        new_active = active.copy()
        
        for u in G.nodes:
            if active[u]:
                continue  # already active
            
            neighbors = list(G.neighbors(u))
            if not neighbors:
                continue
            
            # Fraction of active neighbors
            active_frac = sum(1 for v in neighbors if active[v]) / len(neighbors)
            
            # Effective sharing probability (reduced by meeting costs)
            effective_share = share_prob * (1.0 - meeting_cost)
            
            # Activation: threshold exceeded AND probabilistic sharing succeeds
            if (active_frac >= threshold) and (rng.random() < effective_share):
                new_active[u] = True
        
        active = new_active
        
        # Record state
        n_active = sum(1 for v in active.values() if v)
        history["step"].append(t)
        history["active_frac"].append(n_active / n_nodes)
        history["active_count"].append(n_active)
    
    # Network metrics (with robust error handling)
    metrics = {}
    
    # Connected components
    is_connected = nx.is_connected(G)
    metrics["connected"] = is_connected
    metrics["n_components"] = nx.number_connected_components(G)
    
    # Diameter and avg path length (only for connected graphs)
    if is_connected:
        try:
            metrics["diameter"] = int(nx.diameter(G))
        except:
            metrics["diameter"] = None
        try:
            metrics["avg_path_length"] = float(nx.average_shortest_path_length(G))
        except:
            metrics["avg_path_length"] = None
    else:
        metrics["diameter"] = None
        metrics["avg_path_length"] = None
    
    # Clustering coefficient
    try:
        metrics["clustering"] = float(nx.average_clustering(G))
    except:
        metrics["clustering"] = 0.0
    
    # Degree statistics
    degrees = [d for n, d in G.degree()]
    metrics["avg_degree"] = float(np.mean(degrees)) if degrees else 0.0
    metrics["max_degree"] = int(np.max(degrees)) if degrees else 0
    
    # Diffusion metrics
    arr = np.array(history["active_frac"]) if history["active_frac"] else np.array([0.0])
    
    # Time to 50% activation
    t_50_idx = np.argmax(arr >= 0.5) if np.any(arr >= 0.5) else None
    metrics["t_50"] = int(t_50_idx) if t_50_idx is not None else None
    
    # Final activation rate
    metrics["final_activation"] = float(arr[-1])
    
    # Diffusion speed (average slope in first half of simulation)
    if len(arr) > 1:
        half_point = len(arr) // 2
        metrics["diffusion_speed"] = float((arr[half_point] - arr[0]) / half_point) if half_point > 0 else 0.0
    else:
        metrics["diffusion_speed"] = 0.0
    
    # IMP-Proxy calculations (rough estimates based on network properties)
    IMP_proxies = {}
    
    # Social Participation (SP): clustering × final_activation
    IMP_proxies["SP"] = float(
        min(1.0, 0.5 * metrics["clustering"] + 0.5 * metrics["final_activation"])
    )
    
    # Resilience (R): based on network efficiency (inverse of t_50)
    if metrics["t_50"] is not None and metrics["t_50"] > 0:
        # Normalize: t_50 close to 0 → R close to 1
        IMP_proxies["R"] = float(max(0.0, 1.0 - (metrics["t_50"] / steps)))
    else:
        # No 50% reached → low resilience
        IMP_proxies["R"] = 0.2
    
    # Intrinsic Motivation (IM): share_prob × (1 - threshold)
    # High sharing + low threshold → high intrinsic motivation
    IMP_proxies["IM"] = float(max(0.0, min(1.0, share_prob * (1.0 - threshold))))
    
    # Autonomy (A): neutral (network topology doesn't directly affect autonomy)
    IMP_proxies["A"] = 0.5
    
    # Authenticity (Au): neutral
    IMP_proxies["Au"] = 0.5
    
    # IMP score (multiplicative)
    IMP_proxies["IMP"] = float(
        IMP_proxies["A"] * IMP_proxies["IM"] * IMP_proxies["R"] * 
        IMP_proxies["SP"] * IMP_proxies["Au"]
    )
    
    return G, history, metrics, IMP_proxies

# Run simulation
with st.spinner("Simuliere Netzwerk-Diffusion..."):
    G, history, metrics, IMP_proxies = run_network_simulation(
        topology, n_nodes, k, p, steps, seed_frac, 
        threshold, share_prob, meeting_cost
    )

# ==================== RESULTS DISPLAY ====================
st.header("📊 Ergebnisse")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Finale Aktivierung",
        f"{metrics['final_activation']:.1%}",
        help="Anteil der Knoten, die am Ende aktiv sind"
    )

with col2:
    t_50_display = f"{metrics['t_50']} Schritte" if metrics['t_50'] is not None else "Nicht erreicht"
    st.metric(
        "Zeit bis 50%",
        t_50_display,
        help="Schritte bis zur Hälfte der Knoten aktiv (Diffusions-Geschwindigkeit)"
    )

with col3:
    st.metric(
        "Clustering",
        f"{metrics['clustering']:.3f}",
        help="Durchschnittlicher Clustering-Koeffizient (lokale Dichte)"
    )

with col4:
    path_len_display = f"{metrics['avg_path_length']:.2f}" if metrics['avg_path_length'] is not None else "N/A"
    st.metric(
        "Ø Pfadlänge",
        path_len_display,
        help="Durchschnittliche kürzeste Pfadlänge (nur für zusammenhängende Graphen)"
    )

st.divider()

# ==================== VISUALIZATIONS ====================
st.subheader("📈 Diffusions-Verlauf")

# Main diffusion plot
fig_diffusion = px.line(
    history,
    x="step",
    y="active_frac",
    title="Aktivierung über Zeit",
    labels={"step": "Schritt", "active_frac": "Anteil Aktive"},
    template="plotly_white"
)
fig_diffusion.update_traces(line_color="#4ECDC4", line_width=3)
fig_diffusion.add_hline(
    y=0.5, 
    line_dash="dash", 
    line_color="red", 
    annotation_text="50% Schwelle",
    annotation_position="right"
)
fig_diffusion.update_layout(height=400)
st.plotly_chart(fig_diffusion, use_container_width=True)

# Side-by-side visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    if show_degree_dist:
        st.subheader("📊 Grad-Verteilung")
        
        # Degree distribution
        degrees = [d for n, d in G.degree()]
        
        fig_degree = px.histogram(
            x=degrees,
            nbins=min(30, max(degrees) if degrees else 10),
            title="Verteilung der Knotengrade",
            labels={"x": "Grad", "y": "Häufigkeit"},
            template="plotly_white"
        )
        fig_degree.update_traces(marker_color="#FF6B6B")
        fig_degree.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_degree, use_container_width=True)
        
        st.caption(f"Ø Grad: {metrics['avg_degree']:.1f}, Max: {metrics['max_degree']}")

with viz_col2:
    if show_network_viz and n_nodes <= 150:
        st.subheader("🕸️ Netzwerk-Struktur")
        
        # Network visualization (only for smaller networks)
        pos = nx.spring_layout(G, seed=42, k=0.5)
        
        # Extract positions
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_degrees = [G.degree(node) for node in G.nodes()]
        
        fig_network = go.Figure()
        
        # Edges
        fig_network.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Nodes
        fig_network.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            marker=dict(
                size=[5 + d/2 for d in node_degrees],
                color=node_degrees,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Grad"),
                line_width=1
            ),
            text=[f"Knoten {n}<br>Grad: {d}" for n, d in zip(G.nodes(), node_degrees)],
            hoverinfo='text',
            showlegend=False
        ))
        
        fig_network.update_layout(
            title="Netzwerk-Graph (Spring Layout)",
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=350
        )
        
        st.plotly_chart(fig_network, use_container_width=True)
    elif show_network_viz:
        st.info("Netzwerk-Visualisierung deaktiviert für >150 Knoten (Performance)")

# ==================== IMP PROXIES ====================
st.divider()
st.header("🎯 5D-Dimension Proxies")

st.markdown("""
**Achtung:** Diese Werte sind **grobe Schätzungen** basierend auf Netzwerk-Eigenschaften.
Echte 5D-Scores erfordern individuelle Messungen (Surveys, Verhaltensbeobachtungen).
""")

# IMP metrics
imp_col1, imp_col2, imp_col3, imp_col4, imp_col5, imp_col6 = st.columns(6)

with imp_col1:
    st.metric("Autonomy (A)", f"{IMP_proxies['A']:.2f}", help="Neutral (Netzwerk-unabhängig)")

with imp_col2:
    st.metric("Intrinsic Mot. (IM)", f"{IMP_proxies['IM']:.2f}", help="Sharing-Prob. × (1-Threshold)")

with imp_col3:
    st.metric("Resilience (R)", f"{IMP_proxies['R']:.2f}", help="1 - (t_50 / steps)")

with imp_col4:
    st.metric("Social Part. (SP)", f"{IMP_proxies['SP']:.2f}", help="Clustering × Final Activation")

with imp_col5:
    st.metric("Authenticity (Au)", f"{IMP_proxies['Au']:.2f}", help="Neutral (Netzwerk-unabhängig)")

with imp_col6:
    st.metric("IMP Score", f"{IMP_proxies['IMP']:.3f}", help="A × IM × R × SP × Au")

# ==================== INTERPRETATION ====================
st.divider()
st.header("💡 Interpretation")

with st.expander("🔬 Netzwerk-Metriken erklärt", expanded=False):
    st.markdown(f"""
**Clustering-Koeffizient:** {metrics['clustering']:.3f}
- **Bedeutung:** Wie stark sind Nachbarn untereinander vernetzt?
- **Range:** 0.0 (keine lokalen Cluster) bis 1.0 (perfekt geclustert)
- **Realwelt:** Soziale Netzwerke typisch 0.3-0.6, Zufallsgraphen ~0.01

**Durchschnittliche Pfadlänge:** {metrics['avg_path_length'] if metrics['avg_path_length'] else 'N/A'}
- **Bedeutung:** Durchschnittliche Distanz zwischen zwei Knoten
- **Small-World:** Niedrig (~3-6 bei 100 Knoten), trotz hohem Clustering
- **Bedeutung für Diffusion:** Kurze Pfade = schnelle Verbreitung

**Zeit bis 50% (t_50):** {metrics['t_50'] if metrics['t_50'] else 'Nicht erreicht'}
- **Bedeutung:** Wie schnell erreicht Innovation kritische Masse?
- **Rogers (2003):** 16% Early Adopters → Tipping Point bei ~50%
- **Hier:** Schritte bis zur Hälfte der Knoten aktiviert
""")

with st.expander("🎯 5D-Bezug zur Netzwerk-Theorie", expanded=False):
    st.markdown("""
**Social Participation (SP):**
- **Clustering:** Hohe lokale Dichte = starke Community-Bindung
- **Finale Aktivierung:** Anteil der Teilnehmenden am Ende
- **Granovetter (1973):** Weak ties bringen neue Informationen, strong ties fördern Clustering

**Resilience (R):**
- **Pfadlänge:** Kurze Pfade = schnelle Erholung nach Störungen
- **t_50:** Niedrig = resilientes System (schnelle Diffusion)
- **Scale-free:** Hubs machen Netzwerk anfällig (gezielte Angriffe), aber resilient gegen zufällige Ausfälle

**Intrinsic Motivation (IM):**
- **Sharing-Wahrscheinlichkeit:** Freiwilligkeit, innere Bereitschaft
- **Schwelle:** Niedrig = intrinsisch motiviert (geringe externe Anreize nötig)
- **Deci & Ryan (1985):** Autonomy, competence, relatedness fördern intrinsische Motivation
""")

with st.expander("📚 Topologie-Vergleich", expanded=False):
    st.markdown("""
| Topologie | Clustering | Pfadlänge | Robustheit | Realwelt-Beispiele |
|-----------|------------|-----------|------------|-------------------|
| **Erdős-Rényi** | Niedrig | Niedrig | Mittel | Theoretisches Baseline-Modell |
| **Small-World** | **Hoch** | **Niedrig** | **Hoch** | Soziale Netzwerke, Gehirn, Kooperationen |
| **Scale-Free** | Mittel | Niedrig | Anfällig für Hubs | Internet, Flughäfen, Zitate |

**Empfehlung für Bildungssysteme:**
- **Small-World:** Beste Balance (lokale Cluster + globale Erreichbarkeit)
- **Praxis:** Schulen mit starken Klassen (Clustering) + Austauschprogramme (Shortcuts)
- **Beispiel:** Montessori Mixed-Age-Klassen (starke Bindungen) + Schulübergreifende Projekte (weak ties)
""")

# ==================== EXPORT ====================
st.divider()
st.header("💾 Ergebnisse exportieren")

export_data = {
    "timestamp": datetime.now().isoformat(),
    "parameters": {
        "topology": topology,
        "n_nodes": int(n_nodes),
        "k": int(k),
        "p": float(p),
        "steps": int(steps),
        "seed_frac": float(seed_frac),
        "threshold": float(threshold),
        "share_prob": float(share_prob),
        "meeting_cost": float(meeting_cost)
    },
    "metrics": {k: (int(v) if isinstance(v, (np.integer, int)) else 
                   float(v) if isinstance(v, (np.floating, float)) else 
                   v) for k, v in metrics.items()},
    "IMP_proxies": IMP_proxies,
    "history": {
        "steps": [int(s) for s in history["step"]],
        "active_fraction": [float(f) for f in history["active_frac"]],
        "active_count": [int(c) for c in history["active_count"]]
    }
}

json_str = json.dumps(export_data, indent=2, ensure_ascii=False)

col_export1, col_export2 = st.columns([3, 1])

with col_export1:
    st.download_button(
        label="📥 Download als JSON",
        data=json_str,
        file_name=f"partnet_{topology}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

with col_export2:
    if st.button("💾 In simulations/ speichern"):
        sim_dir = Path("simulations")
        sim_dir.mkdir(exist_ok=True)
        
        filename = f"partnet_{topology}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = sim_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        st.success(f"✅ Gespeichert: {filename}")

# ==================== SCIENTIFIC REFERENCES ====================
st.divider()
st.header("📚 Wissenschaftliche Referenzen")

with st.expander("Literatur & BibTeX", expanded=False):
    st.markdown("""
**Zentrale Arbeiten:**

1. **Granovetter, M. S. (1973).** *The Strength of Weak Ties.*  
   American Journal of Sociology, 78(6), 1360-1380.  
   → BibTeX: `granovetter1973strength`

2. **Watts, D. J., & Strogatz, S. H. (1998).** *Collective dynamics of 'small-world' networks.*  
   Nature, 393(6684), 440-442.  
   → BibTeX: `watts1998collective`

3. **Barabási, A.-L., & Albert, R. (1999).** *Emergence of scaling in random networks.*  
   Science, 286(5439), 509-512.  
   → BibTeX: `barabasi1999emergence`

4. **Rogers, E. M. (2003).** *Diffusion of Innovations (5th ed.).*  
   Free Press.  
   → BibTeX: `rogers2003diffusion`

**Verbindung zu 5D:**

5. **Deci, E. L., & Ryan, R. M. (1985).** *Intrinsic Motivation and Self-Determination in Human Behavior.*  
   Plenum Press.  
   → BibTeX: `deci1985intrinsic` (IM-Dimension)

6. **Ostrom, E. (1990).** *Governing the Commons.*  
   Cambridge University Press.  
   → BibTeX: `ostrom1990governing` (SP-Dimension)

---

**Alle Referenzen verfügbar in:** `07_daten_analysen/5d-relevant-sources.bib`
""")

st.divider()
st.caption("Page 10 | Participation Networks | Version 1.0 | December 2, 2025")
