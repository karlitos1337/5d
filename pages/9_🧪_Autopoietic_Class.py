#!/usr/bin/env python3
"""
Page 9: Autopoietic Class Simulation
Agent-based model showing how 5D dimensions evolve under different conditions
"""

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Autopoietic Class", page_icon="🧪", layout="wide")

# === HEADER ===
st.title("🧪 Autopoietic Class Simulation")
st.markdown(
    """
Agent-based model demonstrating how the 5 dimensions (A, IM, R, SP, Au) 
evolve over time under different classroom conditions.

**Autopoiesis** (Maturana & Varela 1980): Self-creating, self-maintaining systems.  
An **autopoietic classroom** fosters intrinsic motivation and self-organization without external coercion.
"""
)

# === SIDEBAR: PARAMETERS ===
with st.sidebar:
    st.header("⚙️ Simulation Parameters")

    st.subheader("Population")
    n_agents = st.slider("Number of Students", 10, 200, 50, step=10)
    steps = st.slider("Simulation Steps", 50, 1000, 300, step=50)

    st.divider()
    st.subheader("Classroom Conditions")

    zwang = st.slider(
        "Coercion Level",
        0.0,
        1.0,
        0.2,
        step=0.05,
        help="External pressure, deadlines, punishment. Increases stress, decreases IM/R.",
    )

    freiheit = st.slider(
        "Freedom of Choice",
        0.0,
        1.0,
        0.7,
        step=0.05,
        help="Autonomy in topics, pace, methods. Increases IM/Au.",
    )

    peers = st.slider(
        "Peer Interaction",
        0.0,
        1.0,
        0.6,
        step=0.05,
        help="Collaboration, discussion, mutual support. Increases SP/IM.",
    )

    lehrer_support = st.slider(
        "Teacher Support",
        0.0,
        1.0,
        0.6,
        step=0.05,
        help="Emotional support, constructive feedback. Reduces stress, increases R.",
    )

    aufgaben_vielfalt = st.slider(
        "Task Diversity",
        0.0,
        1.0,
        0.7,
        step=0.05,
        help="Variety of activities matching different interests. Increases IM through fit.",
    )

    st.divider()
    st.subheader("Display Options")
    show_dropouts = st.checkbox("Show Dropout Events", value=True)
    show_individual = st.checkbox("Show Individual Trajectories (sample)", value=False)


# === SIMULATION ===
@st.cache_data
def run_simulation(n, steps, zwang, freiheit, peers, lehrer, vielfalt, seed=42):
    """Run autopoietic classroom simulation"""
    rs = np.random.default_rng(seed)

    # Initialize agents with realistic starting values
    A = rs.uniform(0.4, 0.7, size=n)
    IM = rs.uniform(0.4, 0.7, size=n)
    R = rs.uniform(0.4, 0.7, size=n)
    SP = rs.uniform(0.3, 0.6, size=n)
    Au = rs.uniform(0.4, 0.7, size=n)

    # Individual interests (affects task fit)
    interest = rs.uniform(0.0, 1.0, size=n)

    # History tracking
    hist = {
        "step": [],
        "A_mean": [],
        "IM_mean": [],
        "R_mean": [],
        "SP_mean": [],
        "Au_mean": [],
        "A_std": [],
        "IM_std": [],
        "R_std": [],
        "SP_std": [],
        "Au_std": [],
        "active_count": [],
        "dropout_events": [],
    }

    # Individual trajectories (sample 5 agents)
    sample_indices = rs.choice(n, size=min(5, n), replace=False)
    individual_hist = {i: {"A": [], "IM": [], "R": [], "SP": [], "Au": []} for i in sample_indices}

    active = np.ones(n, dtype=bool)

    for t in range(steps):
        # Calculate stress and fit
        stress = zwang * (1.0 - lehrer)

        # Task fit: combination of choice freedom and task diversity
        # Better fit when student's interest aligns with available tasks
        task_match = vielfalt * (1.0 - np.abs(interest - rs.random(n)))
        passung = freiheit * task_match

        # Update dimensions (only for active students)
        # Learning rates calibrated to reach equilibrium
        IM[active] += 0.04 * (passung[active] - stress - 0.3)
        R[active] += 0.03 * (lehrer - stress - 0.2)
        SP[active] += 0.025 * (peers - 0.3)
        Au[active] += 0.025 * (freiheit - 0.3)
        A[active] += 0.02 * (freiheit - zwang - 0.1)

        # Dropout condition: IM or R falls too low
        new_dropouts = active & ((IM < 0.15) | (R < 0.15))
        if np.any(new_dropouts):
            hist["dropout_events"].append({"step": t, "count": int(np.sum(new_dropouts))})
            active[new_dropouts] = False

        # Inactive students: slow decay
        IM[~active] *= 0.98
        R[~active] *= 0.98
        A[~active] *= 0.99
        SP[~active] *= 0.99
        Au[~active] *= 0.99

        # Clip to valid range
        for arr in (A, IM, R, SP, Au):
            np.clip(arr, 0.0, 1.0, out=arr)

        # Natural interest drift
        interest = np.clip(interest + rs.normal(0, 0.01, size=n), 0.0, 1.0)

        # Record statistics
        hist["step"].append(t)
        hist["A_mean"].append(float(np.mean(A)))
        hist["IM_mean"].append(float(np.mean(IM)))
        hist["R_mean"].append(float(np.mean(R)))
        hist["SP_mean"].append(float(np.mean(SP)))
        hist["Au_mean"].append(float(np.mean(Au)))

        hist["A_std"].append(float(np.std(A)))
        hist["IM_std"].append(float(np.std(IM)))
        hist["R_std"].append(float(np.std(R)))
        hist["SP_std"].append(float(np.std(SP)))
        hist["Au_std"].append(float(np.std(Au)))

        hist["active_count"].append(int(np.sum(active)))

        # Individual trajectories
        for idx in sample_indices:
            individual_hist[idx]["A"].append(A[idx])
            individual_hist[idx]["IM"].append(IM[idx])
            individual_hist[idx]["R"].append(R[idx])
            individual_hist[idx]["SP"].append(SP[idx])
            individual_hist[idx]["Au"].append(Au[idx])

    # Final metrics
    final_A = float(np.mean(A))
    final_IM = float(np.mean(IM))
    final_R = float(np.mean(R))
    final_SP = float(np.mean(SP))
    final_Au = float(np.mean(Au))
    final_IMP = final_A * final_IM * final_R * final_SP * final_Au
    total_dropouts = n - int(np.sum(active))

    return (
        hist,
        individual_hist,
        {
            "A": final_A,
            "IM": final_IM,
            "R": final_R,
            "SP": final_SP,
            "Au": final_Au,
            "IMP": final_IMP,
            "total_dropouts": total_dropouts,
            "retention_rate": float(np.sum(active)) / n,
        },
    )


# Run simulation
with st.spinner("Running simulation..."):
    history, individual_history, final_metrics = run_simulation(
        n_agents, steps, zwang, freiheit, peers, lehrer_support, aufgaben_vielfalt
    )

# Toast notification for successful run
if "last_run" not in st.session_state or st.session_state.last_run != final_metrics["IMP"]:
    st.toast("Simulation completed successfully!", icon="✅")
    st.session_state.last_run = final_metrics["IMP"]

# === RESULTS ===
st.header("📊 Simulation Results")

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        "Final IMP",
        f"{final_metrics['IMP']:.3f}",
        help="Individual Potential (Geometric Mean of 5 dimensions). >0.2 is sustainable.",
    )
with col2:
    st.metric(
        "Retention Rate",
        f"{final_metrics['retention_rate']:.1%}",
        help="Percentage of students who remained active until the end.",
    )
with col3:
    st.metric(
        "Total Dropouts",
        final_metrics["total_dropouts"],
        help="Students who left due to low Motivation or Resilience (<0.15).",
    )
with col4:
    st.metric(
        "Final Autonomy",
        f"{final_metrics['A']:.2f}",
        help="Self-determination capability at the end of simulation.",
    )
with col5:
    st.metric(
        "Final IM",
        f"{final_metrics['IM']:.2f}",
        help="Intrinsic Motivation level at the end of simulation.",
    )

st.divider()

# === DIMENSION EVOLUTION ===
st.subheader("🌊 Evolution of 5D Dimensions Over Time")

# Create figure with mean + std bands
fig = go.Figure()

colors = {"A": "#FF6B6B", "IM": "#4ECDC4", "R": "#45B7D1", "SP": "#FFA07A", "Au": "#98D8C8"}

for dim in ["A", "IM", "R", "SP", "Au"]:
    mean = history[f"{dim}_mean"]
    std = history[f"{dim}_std"]
    steps_list = history["step"]

    # Upper and lower bounds
    upper = [m + s for m, s in zip(mean, std, strict=False)]
    lower = [m - s for m, s in zip(mean, std, strict=False)]

    # Add std band
    fig.add_trace(
        go.Scatter(
            x=steps_list + steps_list[::-1],
            y=upper + lower[::-1],
            fill="toself",
            fillcolor=colors[dim],
            opacity=0.2,
            line=dict(color="rgba(255,255,255,0)"),
            showlegend=False,
            name=f"{dim} ±σ",
        )
    )

    # Add mean line
    fig.add_trace(go.Scatter(x=steps_list, y=mean, mode="lines", name=dim, line=dict(color=colors[dim], width=2)))

fig.update_layout(
    title="5D Dimensions: Mean ± Standard Deviation",
    xaxis_title="Step",
    yaxis_title="Score (0-1)",
    hovermode="x unified",
    height=500,
)

st.plotly_chart(fig, width="stretch")

# === INDIVIDUAL TRAJECTORIES ===
if show_individual and len(individual_history) > 0:
    st.subheader("👤 Individual Student Trajectories (Sample)")

    fig_ind = go.Figure()

    for idx, traj in individual_history.items():
        # Calculate individual IMP over time
        imp_traj = [
            traj["A"][t] * traj["IM"][t] * traj["R"][t] * traj["SP"][t] * traj["Au"][t] for t in range(len(traj["A"]))
        ]

        fig_ind.add_trace(go.Scatter(x=history["step"], y=imp_traj, mode="lines", name=f"Student {idx}", opacity=0.7))

    fig_ind.update_layout(
        title="Individual IMP Scores Over Time",
        xaxis_title="Step",
        yaxis_title="IMP Score",
        height=400,
    )

    st.plotly_chart(fig_ind, width="stretch")

# === DROPOUT EVENTS ===
if show_dropouts and history["dropout_events"]:
    st.subheader("🚪 Dropout Events")

    dropout_steps = [e["step"] for e in history["dropout_events"]]
    dropout_counts = [e["count"] for e in history["dropout_events"]]

    fig_dropout = go.Figure()
    fig_dropout.add_trace(
        go.Scatter(
            x=dropout_steps,
            y=dropout_counts,
            mode="markers+lines",
            marker=dict(size=10, color="red"),
            line=dict(color="red", dash="dash"),
            name="Dropouts",
        )
    )

    fig_dropout.update_layout(
        title="Dropout Events Over Time",
        xaxis_title="Step",
        yaxis_title="Number of Dropouts",
        height=300,
    )

    st.plotly_chart(fig_dropout, width="stretch")

# === ACTIVE STUDENTS ===
col1, col2 = st.columns(2)

with col1:
    fig_active = px.line(
        x=history["step"],
        y=history["active_count"],
        title="Active Students Over Time",
        labels={"x": "Step", "y": "Active Students"},
    )
    fig_active.add_hline(y=n_agents, line_dash="dash", line_color="gray", annotation_text="Initial")
    st.plotly_chart(fig_active, width="stretch")

with col2:
    # Final distribution
    final_dims = {
        "Dimension": ["A", "IM", "R", "SP", "Au"],
        "Score": [
            final_metrics["A"],
            final_metrics["IM"],
            final_metrics["R"],
            final_metrics["SP"],
            final_metrics["Au"],
        ],
    }

    fig_final = px.bar(
        final_dims,
        x="Dimension",
        y="Score",
        title="Final Dimension Scores",
        color="Dimension",
        color_discrete_map=colors,
    )
    fig_final.update_yaxes(range=[0, 1])
    st.plotly_chart(fig_final, width="stretch")

# === INTERPRETATION ===
st.divider()
st.header("🔬 Scientific Interpretation")

with st.expander("📖 What is Autopoiesis?"):
    st.markdown(
        """
    **Autopoiesis** (Greek: *auto* = self, *poiesis* = creation) is a concept from biology 
    describing self-creating, self-maintaining systems.
    
    **Key Papers:**
    - Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*
    - Luhmann, N. (1995). *Social Systems* (applied to social systems)
    
    **In Education:**
    An autopoietic classroom is a self-organizing learning environment where:
    - Students regulate their own learning (autonomy)
    - Intrinsic motivation drives engagement
    - Peer interactions create emergent social structures
    - Teacher acts as facilitator, not controller
    """
    )

with st.expander("📊 Model Parameters Explained"):
    st.markdown(
        """
    **Coercion Level:**
    - High coercion → Stress → Decreased IM, R
    - Examples: Strict deadlines, punishment, surveillance
    - Scientific basis: Deci & Ryan (1985) - Self-Determination Theory
    
    **Freedom of Choice:**
    - High freedom → Increased IM, Au
    - Examples: Choose topics, pace, assessment methods
    - Scientific basis: Sudbury Valley School (Greenberg 1992)
    
    **Peer Interaction:**
    - Collaboration → Increased SP, IM
    - Examples: Group projects, peer tutoring, discussion
    - Scientific basis: Bandura (1977) - Social Learning Theory
    
    **Teacher Support:**
    - Emotional support → Reduced stress, Increased R
    - Examples: Constructive feedback, empathy, availability
    - Scientific basis: Porges (2011) - Polyvagal Theory (safety → learning)
    
    **Task Diversity:**
    - Variety matches interests → Increased IM
    - Examples: Multiple pathways, differentiated instruction
    - Scientific basis: Csíkszentmihályi (1990) - Flow Theory (challenge-skill balance)
    """
    )

with st.expander("🎯 Interpreting Results"):
    st.markdown(
        f"""
    **Your Simulation Results:**
    - Final IMP: **{final_metrics["IMP"]:.3f}**
    - Retention: **{final_metrics["retention_rate"]:.1%}**
    - Dropouts: **{final_metrics["total_dropouts"]}** students
    
    **Interpretation Ranges:**
    - **IMP > 0.20:** Healthy learning environment (sustainable)
    - **IMP 0.10-0.20:** Marginal (risk of burnout)
    - **IMP < 0.10:** Critical (high dropout risk)
    
    **Retention Benchmarks:**
    - Traditional schools: 70-85% (OECD average)
    - Alternative models: 85-95% (Sudbury, Folk High Schools)
    - Your simulation: **{final_metrics["retention_rate"]:.1%}**
    
    **Key Insights:**
    - Coercion = {zwang:.2f}: {"⚠️ High stress environment" if zwang > 0.5 else "✅ Moderate stress"}
    - Freedom = {freiheit:.2f}: {"✅ High autonomy" if freiheit > 0.6 else "⚠️ Limited autonomy"}
    - Balance: {"✅ Freedom > Coercion (healthy)" if freiheit > zwang else "⚠️ Coercion ≥ Freedom (problematic)"}
    """
    )

# === SAVE RESULTS ===
st.divider()
st.header("💾 Save Simulation")

if st.button("📥 Export Results (JSON)", type="primary"):
    output = {
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "n_agents": n_agents,
            "steps": steps,
            "coercion": zwang,
            "freedom": freiheit,
            "peers": peers,
            "teacher_support": lehrer_support,
            "task_diversity": aufgaben_vielfalt,
        },
        "final_metrics": final_metrics,
        "history": {
            "steps": history["step"],
            "A_mean": history["A_mean"],
            "IM_mean": history["IM_mean"],
            "R_mean": history["R_mean"],
            "SP_mean": history["SP_mean"],
            "Au_mean": history["Au_mean"],
            "active_count": history["active_count"],
        },
    }

    # Create simulations directory if needed
    sim_dir = Path("simulations")
    sim_dir.mkdir(exist_ok=True)

    filename = f"autopoietic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = sim_dir / filename

    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)

    st.success(f"✅ Saved to: `{filepath}`")

    # Offer download
    st.download_button(
        label="⬇️ Download JSON",
        data=json.dumps(output, indent=2),
        file_name=filename,
        mime="application/json",
    )

# === REFERENCES ===
st.divider()
st.header("📚 Scientific References")

st.markdown(
    """
**Core Concepts:**
1. **Maturana, H. R., & Varela, F. J. (1980).** *Autopoiesis and Cognition: The Realization of the Living.* 
   D. Reidel Publishing Company. [DOI: 10.1007/978-94-009-8947-4](https://doi.org/10.1007/978-94-009-8947-4)

2. **Deci, E. L., & Ryan, R. M. (1985).** *Intrinsic Motivation and Self-Determination in Human Behavior.* 
   Springer. [DOI: 10.1007/978-1-4899-2271-7](https://doi.org/10.1007/978-1-4899-2271-7)

3. **Csíkszentmihályi, M. (1990).** *Flow: The Psychology of Optimal Experience.* 
   Harper & Row.

4. **Porges, S. W. (2011).** *The Polyvagal Theory: Neurophysiological Foundations of Emotions.* 
   W. W. Norton & Company.

**Alternative Education Models:**
5. **Greenberg, D. (1992).** *The Sudbury Valley School Experience.* 
   Sudbury Valley School Press.

6. **Bandura, A. (1977).** *Social Learning Theory.* 
   Prentice Hall.

**All references available in:** `07_daten_analysen/5d-relevant-sources.bib`
"""
)
