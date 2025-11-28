#!/usr/bin/env python3
"""
Autopoietische Klasse – Streamlit Simulation (leichte ABM-Variante)
- Ziel: Einfluss von Zwanglosigkeit/Wahlfreiheit/Peers auf A, IM, R, SP, Au
- Output: JSON-Run in simulations/ mit Parametern und Metriken
"""

from __future__ import annotations

import numpy as np
import streamlit as st
import plotly.express as px
from datetime import datetime
from simulations.utils import write_run

st.set_page_config(page_title="Autopoietische Klasse", page_icon="🧪", layout="centered")
st.title("🧪 Autopoietische Klasse – Simulation")

with st.sidebar:
    st.header("Parameter")
    n_agents = st.slider("Anzahl Lernende", 5, 500, 80, step=5)
    steps = st.slider("Schritte", 10, 1000, 200, step=10)
    zwang = st.slider("Zwangsgrad", 0.0, 1.0, 0.2, step=0.05, help="Erhöht Stress, senkt IM/R")
    freiheit = st.slider("Wahlfreiheit", 0.0, 1.0, 0.7, step=0.05, help="Erhöht IM/Au")
    peers = st.slider("Peer-Interaktion", 0.0, 1.0, 0.5, step=0.05, help="Fördert SP/IM")
    lehrer_support = st.slider("Lehrer-Support", 0.0, 1.0, 0.5, step=0.05, help="Senkt Stress, erhöht R")
    aufgaben_vielfalt = st.slider("Aufgabenvielfalt", 0.0, 1.0, 0.6, step=0.05, help="Erhöht IM durch Passung")

# Init Agentenzustände (0..1)
rs = np.random.default_rng(42)
A = rs.uniform(0.4, 0.7, size=n_agents)
IM = rs.uniform(0.4, 0.7, size=n_agents)
R = rs.uniform(0.4, 0.7, size=n_agents)
SP = rs.uniform(0.3, 0.6, size=n_agents)
Au = rs.uniform(0.4, 0.7, size=n_agents)

interest = rs.uniform(0.0, 1.0, size=n_agents)

hist = {"step": [], "A": [], "IM": [], "R": [], "SP": [], "Au": [], "dropout": []}

for t in range(steps):
    # Stress/Entlastung
    stress = zwang * (1.0 - lehrer_support)
    # Aufgabenzuordnung: Passung ~ Aufgabenvielfalt und Wahlfreiheit
    passung = freiheit * aufgaben_vielfalt * (1.0 - np.abs(interest - rs.random(n_agents)))

    # Updates (kleine Lernrate)
    IM += 0.05 * (passung - stress)
    R += 0.04 * (lehrer_support - stress)
    SP += 0.03 * (peers - 0.3)
    Au += 0.03 * (freiheit - 0.3)
    A  += 0.02 * (freiheit - zwang)

    # Dropout-Bedingung (IM oder R < Schwelle)
    active = (IM > 0.1) & (R > 0.1)
    # Leichte natürliche Drift/Begrenzung
    for arr in (A, IM, R, SP, Au):
        arr[~active] *= 0.98
        np.clip(arr, 0.0, 1.0, out=arr)

    # Interest drift (neue Neigungen)
    interest = np.clip(interest + rs.normal(0, 0.02, size=n_agents), 0.0, 1.0)

    hist["step"].append(t)
    hist["A"].append(float(np.mean(A)))
    hist["IM"].append(float(np.mean(IM)))
    hist["R"].append(float(np.mean(R)))
    hist["SP"].append(float(np.mean(SP)))
    hist["Au"].append(float(np.mean(Au)))
    hist["dropout"].append(int(np.size(active) - int(np.sum(active))))

# Visualisierung
cols = st.columns(2)
with cols[0]:
    fig = px.line(hist, x="step", y=["A","IM","R","SP","Au"], title="IMP-Dimensionen (Mittelwerte)")
    st.plotly_chart(fig, use_container_width=True)
with cols[1]:
    fig2 = px.line(hist, x="step", y="dropout", title="Dropout pro Schritt")
    st.plotly_chart(fig2, use_container_width=True)

# Metriken aggregiert
imp = np.array([hist["A"][-1], hist["IM"][-1], hist["R"][-1], hist["SP"][-1], hist["Au"][-1]])
imp_score = float(np.prod(imp))

st.subheader("Ergebnis")
st.write({
    "A": hist["A"][-1],
    "IM": hist["IM"][-1],
    "R": hist["R"][-1],
    "SP": hist["SP"][-1],
    "Au": hist["Au"][-1],
    "IMP": imp_score,
    "Dropout_total": int(np.sum(hist["dropout"]))
})

# Speichern
if st.button("Run speichern"):
    params = {
        "n_agents": int(n_agents),
        "steps": int(steps),
        "zwang": float(zwang),
        "freiheit": float(freiheit),
        "peers": float(peers),
        "lehrer_support": float(lehrer_support),
        "aufgaben_vielfalt": float(aufgaben_vielfalt),
    }
    metrics = {
        "A": hist["A"][-1],
        "IM": hist["IM"][-1],
        "R": hist["R"][-1],
        "SP": hist["SP"][-1],
        "Au": hist["Au"][-1],
        "IMP": imp_score,
        "dropout_total": int(np.sum(hist["dropout"])),
    }
    path = write_run("autopoietisch", params, metrics)
    st.success(f"Run gespeichert: {path.name}")
