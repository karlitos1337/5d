#!/usr/bin/env python3
"""
Partizipations-Netzwerke – Streamlit Simulation
- Netzwerk-Topologien vergleichen (Erdos-Renyi, Small-World, Scale-Free)
- Wissens-/Interessen-Diffusion mit Schwellen oder probabilistisch
- Kennzahlen + Diffusionsgeschwindigkeit; JSON-Run speichern
"""

from __future__ import annotations

import streamlit as st
import plotly.express as px
import networkx as nx
import numpy as np
from simulations.utils import write_run

st.set_page_config(page_title="Partizipations-Netzwerke", page_icon="🕸️", layout="centered")
st.title("🕸️ Partizipations-Netzwerke – Simulation")

with st.sidebar:
    st.header("Parameter")
    n = st.slider("Knoten", 10, 1000, 120, step=10)
    topo = st.selectbox("Topologie", ["erdos_renyi", "small_world", "scale_free"], index=1)
    p = st.slider("Kantenwahrscheinlichkeit p / Rewire", 0.001, 0.5, 0.05, step=0.001)
    k = st.slider("Nachbarn k (Small-World)", 2, 20, 6)
    steps = st.slider("Schritte", 5, 500, 100)
    seed_frac = st.slider("Initiale Aktivierung (%)", 1, 50, 5) / 100.0
    threshold = st.slider("Schwelle (0..1)", 0.0, 1.0, 0.2, step=0.05)
    share_prob = st.slider("Sharing-Wahrsch.", 0.0, 1.0, 0.6, step=0.05)
    meeting_cost = st.slider("Meetingkosten", 0.0, 1.0, 0.2, step=0.05)

# Netzwerk generieren
if topo == "erdos_renyi":
    G = nx.erdos_renyi_graph(n=n, p=p, seed=42)
elif topo == "small_world":
    G = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=42)
else:
    G = nx.barabasi_albert_graph(n=n, m=max(1, k//2), seed=42)

# Initiale Aktivierung
rs = np.random.default_rng(42)
active = {node: (rs.random() < seed_frac) for node in G.nodes}

hist = {"step": [], "active_frac": []}

for t in range(steps):
    new_active = active.copy()
    for u in G.nodes:
        if active[u]:
            continue
        nbrs = list(G.neighbors(u))
        if not nbrs:
            continue
        # Anteil aktiver Nachbarn
        a = sum(1 for v in nbrs if active[v]) / len(nbrs)
        # Wahrscheinlichkeit, dass Sharing stattfindet und Schwelle überwunden wird
        effective_share = share_prob * (1.0 - meeting_cost)
        if (a >= threshold) and (rs.random() < effective_share):
            new_active[u] = True
    active = new_active
    hist["step"].append(t)
    hist["active_frac"].append(sum(1 for v in active.values() if v) / n)

# Kennzahlen (robust, mit Fallbacks)
metrics = {}
try:
    metrics["durchmesser"] = int(nx.diameter(G)) if nx.is_connected(G) else None
except Exception:
    metrics["durchmesser"] = None
try:
    metrics["avg_path_len"] = float(nx.average_shortest_path_length(G)) if nx.is_connected(G) else None
except Exception:
    metrics["avg_path_len"] = None
metrics["clustering"] = float(nx.average_clustering(G)) if G.number_of_nodes() > 0 else 0.0

# Diffusions-Kennzahlen
arr = np.array(hist["active_frac"]) if hist["active_frac"] else np.array([0.0])
metrics["t_50"] = int(np.argmax(arr >= 0.5)) if np.any(arr >= 0.5) else None
metrics["final_frac"] = float(arr[-1])

cols = st.columns(2)
with cols[0]:
    st.plotly_chart(px.line(hist, x="step", y="active_frac", title="Aktive Fraktion"), use_container_width=True)
with cols[1]:
    st.write({"Kennzahlen": metrics})

# IMP-bezogene Proxy-Metriken (grobe Zuordnung)
# SP ~ clustering & final_frac, R ~ Konnektivität (t_50 niedrig), IM ~ share_prob/threshold-Kontext
IMP = {
    "SP": float(min(1.0, 0.5 * metrics.get("clustering", 0.0) + 0.5 * metrics.get("final_frac", 0.0))),
    "R": float(0.0 if metrics.get("t_50") is None else max(0.0, 1.0 - metrics["t_50"] / max(1, steps))),
    "IM": float(max(0.0, min(1.0, share_prob * (1.0 - threshold))))
}
IMP["A"] = float(0.5)  # neutral
IMP["Au"] = float(0.5) # neutral
IMP_score = float(IMP["A"]*IMP["IM"]*IMP["R"]*IMP["SP"]*IMP["Au"]) 

st.subheader("IMP-Proxies (grob)")
st.write({**IMP, "IMP": IMP_score})

if st.button("Run speichern"):
    params = {
        "n": int(n), "topologie": topo, "p_or_rewire": float(p), "k": int(k),
        "steps": int(steps), "seed_frac": float(seed_frac), "threshold": float(threshold),
        "share_prob": float(share_prob), "meeting_cost": float(meeting_cost)
    }
    metrics_out = {**metrics, "IMP": IMP_score, "final_frac": metrics.get("final_frac")}
    path = write_run("partnet", params, metrics_out)
    st.success(f"Run gespeichert: {path.name}")
