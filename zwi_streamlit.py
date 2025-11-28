#!/usr/bin/env python3
"""
Zwanglosigkeits-Spiel (Non-Coercive Interaction) – Streamlit App
- Modelle: Zustimmung (willingness), Zwang (coercer), Payoff-Dynamik
- Visualisierung: willingness / payoff / type
"""

import time
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Zwanglosigkeit", page_icon="🤝", layout="centered")

st.title("🤝 Zwanglosigkeits-Spiel – Non-Coercive Interaction")

with st.sidebar:
    st.header("Einstellungen")
    n = st.slider("Grid N", 10, 120, 40, 1)
    coercer_ratio = st.slider("Anteil Zwinger (%)", 0, 100, 10, 1)
    consent_thr = st.slider("Zustimmungsschwelle", 0.0, 1.0, 0.5, 0.01)
    steps = st.slider("Schritte (Auto)", 1, 500, 60, 1)
    interval_ms = st.slider("Intervall (ms)", 10, 1000, 120, 10)

rng = np.random.default_rng(42)

def init_world(n: int, coercer_ratio: float):
    types = np.zeros((n, n), dtype=int)
    mask = rng.random((n, n)) < (coercer_ratio/100.0)
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

state_key = f"zwi_{n}_{coercer_ratio}_{consent_thr:.2f}"
if state_key not in st.session_state:
    st.session_state[state_key] = init_world(n, coercer_ratio)

z_types, z_will, z_pay = st.session_state[state_key]

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Step"):
        z_types, z_will, z_pay = interaction_step(z_types, z_will, z_pay, thr=consent_thr)
with col2:
    if st.button("10 Steps"):
        for _ in range(10):
            z_types, z_will, z_pay = interaction_step(z_types, z_will, z_pay, thr=consent_thr)
with col3:
    if st.button("Auto-Run"):
        for _ in range(steps):
            z_types, z_will, z_pay = interaction_step(z_types, z_will, z_pay, thr=consent_thr)
            time.sleep(max(0.005, interval_ms/1000.0))
with col4:
    if st.button("Reset"):
        z_types, z_will, z_pay = init_world(n, coercer_ratio)

st.session_state[state_key] = (z_types, z_will, z_pay)

st.write(
    f"Ø Bereitschaft: {float(np.mean(z_will)):.2f} | Ø Payoff: {float(np.mean(z_pay)):.2f} | Zwinger %: {float(np.mean(z_types==1)*100):.1f}%"
)

mode = st.selectbox("Visualisierung", ["Willingness", "Payoff", "Type"], index=0)
if mode == "Willingness":
    mat = z_will
    scale = 'Viridis'
elif mode == "Payoff":
    mat = z_pay
    scale = 'Plasma'
else:
    mat = z_types
    scale = 'Gray'

st.plotly_chart(px.imshow(mat, color_continuous_scale=scale, origin='upper'), use_container_width=True)
