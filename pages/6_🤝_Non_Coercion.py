#!/usr/bin/env python3
"""
5D Dashboard - Non-Coercion / Zwanglosigkeit
Cooperation vs. Coercion Simulation
"""

from datetime import datetime

import numpy as np
import streamlit as st

st.set_page_config(
    page_title="5D Non-Coercion", page_icon="🤝", layout="wide", initial_sidebar_state="expanded"
)


def simulate_cooperation(cooperation_payoff, coercion_penalty, agents, rounds):
    """
    Simulate cooperation vs. coercion dynamics

    Based on Game Theory and Common Pool Resource Management
    """
    # Initialize agents (50% cooperate, 50% defect)
    strategies = np.random.choice(["cooperate", "defect"], size=agents, p=[0.5, 0.5])

    scores = np.zeros(agents)
    history = {"cooperators": [], "defectors": [], "avg_score_coop": [], "avg_score_defect": []}

    for _round_num in range(rounds):
        cooperators = np.sum(strategies == "cooperate")
        defectors = agents - cooperators

        # Payoffs
        for i, strategy in enumerate(strategies):
            if strategy == "cooperate":
                # Cooperation payoff increases with more cooperators
                scores[i] += cooperation_payoff * (cooperators / agents)
            else:
                # Defection payoff decreases with coercion penalty
                scores[i] += (cooperation_payoff * 0.5) - (coercion_penalty * (defectors / agents))

        # Strategy update (agents switch to better strategy)
        avg_coop = np.mean(scores[strategies == "cooperate"]) if cooperators > 0 else 0
        avg_defect = np.mean(scores[strategies == "defect"]) if defectors > 0 else 0

        # Probabilistic strategy switch
        for i in range(agents):
            if strategies[i] == "cooperate" and avg_coop < avg_defect:
                if np.random.random() < 0.2:  # 20% chance to switch
                    strategies[i] = "defect"
            elif strategies[i] == "defect" and avg_defect < avg_coop:
                if np.random.random() < 0.3:  # 30% chance to switch (cooperation more attractive)
                    strategies[i] = "cooperate"

        # Record history
        history["cooperators"].append(cooperators)
        history["defectors"].append(defectors)
        history["avg_score_coop"].append(avg_coop)
        history["avg_score_defect"].append(avg_defect)

    return history, strategies, scores


def main():
    # Sidebar
    with st.sidebar:
        st.title("🤝 Non-Coercion")
        st.markdown("**Zwanglosigkeit & Kooperation**")

        st.divider()

        st.markdown("### 🔬 Scientific Basis")
        st.markdown(
            """
        **Commons Theory:**
        
        Ostrom, E. (1990)
        *Governing the Commons*
        
        **Konzept:**
        - Gemeingüter ohne Zwang
        - Selbstorganisation
        - Intrinsische Motivation
        
        **Status:** ✅ Peer-Reviewed (Nobelpreis 2009)
        """
        )

        st.divider()

        st.markdown("### 📖 Key Ideas")
        st.markdown(
            """
        **Zwanglosigkeit:**
        1. Freiwillige Teilnahme
        2. Keine Bestrafung
        3. Positive Anreize
        4. Intrinsische Motivation
        
        **Kooperation > Zwang**
        """
        )

    # Main Content
    st.title("🤝 Non-Coercion: Zwanglosigkeit & Kooperation")
    st.markdown("### Simulation: Cooperation vs. Coercion Dynamics")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Ostrom Principles", "8", help="Design Principles for Commons")

    with col2:
        st.metric("Nobel Prize", "2009", help="Economics Nobel Prize")

    with col3:
        st.metric("Documented Cases", "5000+", help="Successful Commons Worldwide")

    with col4:
        st.metric("Optimal Strategy", "Cooperate", help="Nash Equilibrium")

    st.divider()

    # Main Content (2 columns)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.header("🎮 Agent-Based Simulation")

        st.markdown(
            """
        **Modell:** Agenten wählen zwischen Kooperation und Defektion
        
        - **Kooperation:** Alle profitieren (Common Pool Resource)
        - **Defektion:** Kurzfristiger Vorteil, langfristige Kosten
        - **Zwang (Coercion Penalty):** Reduziert Defektion-Payoff
        """
        )

        # Parameters
        st.subheader("⚙️ Parameter")

        param_col1, param_col2 = st.columns(2)

        with param_col1:
            cooperation_payoff = st.slider(
                "Cooperation Payoff", 1.0, 10.0, 5.0, 0.5, help="Payoff pro Runde bei Kooperation"
            )

            agents = st.slider(
                "Anzahl Agents", 10, 200, 50, 10, help="Mehr Agents → komplexere Dynamik"
            )

        with param_col2:
            coercion_penalty = st.slider(
                "Coercion Penalty", 0.0, 10.0, 3.0, 0.5, help="Strafe für Defektion (Zwang)"
            )

            rounds = st.slider("Runden", 10, 200, 50, 10, help="Simulationsschritte")

        # Run Simulation
        if st.button("▶️ Simulation starten"):
            with st.spinner("Simuliere..."):
                history, final_strategies, final_scores = simulate_cooperation(
                    cooperation_payoff, coercion_penalty, agents, rounds
                )

                st.session_state.history = history
                st.session_state.final_strategies = final_strategies
                st.session_state.final_scores = final_scores

        # Display Results
        if "history" in st.session_state:
            st.divider()
            st.subheader("📊 Ergebnisse")

            history = st.session_state.history

            # Metrics
            final_cooperators = history["cooperators"][-1]
            final_defectors = history["defectors"][-1]

            coop_ratio = (final_cooperators / (final_cooperators + final_defectors)) * 100

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:
                st.metric(
                    "Final Cooperators",
                    final_cooperators,
                    delta=final_cooperators - history["cooperators"][0],
                )

            with result_col2:
                st.metric(
                    "Final Defectors",
                    final_defectors,
                    delta=final_defectors - history["defectors"][0],
                )

            with result_col3:
                st.metric("Cooperation Rate", f"{coop_ratio:.1f}%")

            # Interpretation
            st.divider()
            st.subheader("📈 Interpretation")

            if coop_ratio > 75:
                st.success(
                    f"""
                ✅ **Kooperation dominiert ({coop_ratio:.1f}%)**
                
                - Hohe Cooperation Payoffs fördern Zusammenarbeit
                - Coercion Penalty macht Defektion unattraktiv
                - Stabile Kooperation erreicht
                
                **Parallele:** Funktioniert wie alternative Schulen (Sudbury, Folk High Schools)
                """
                )
            elif coop_ratio > 40:
                st.warning(
                    f"""
                ⚠️ **Mixed Equilibrium ({coop_ratio:.1f}%)**
                
                - Kooperation und Defektion koexistieren
                - Instabile Dynamik
                - Potenzial für Verbesserung durch höhere Payoffs
                
                **Parallele:** Traditionelle Schulen mit Zwangsmaßnahmen
                """
                )
            else:
                st.error(
                    f"""
                ❌ **Defektion dominiert ({100-coop_ratio:.1f}%)**
                
                - Zu niedrige Cooperation Payoffs
                - Zwang ineffektiv
                - Kollabierende Kooperation
                
                **Parallele:** Gescheiterte Common Pool Resources (Hardin's "Tragedy of the Commons")
                """
                )

            # ASCII Chart (simple bar chart)
            st.divider()
            st.subheader("📉 Verlauf über Zeit")

            st.markdown("**Cooperators (🟢) vs. Defectors (🔴)**")

            # Sample every 5 rounds for display
            sample_rounds = list(
                range(0, len(history["cooperators"]), max(1, len(history["cooperators"]) // 20))
            )

            for i in sample_rounds:
                coop = history["cooperators"][i]
                defect = history["defectors"][i]
                total = coop + defect

                coop_bar = "🟢" * int((coop / total) * 20)
                defect_bar = "🔴" * int((defect / total) * 20)

                st.text(f"Round {i:3d}: {coop_bar}{defect_bar} ({coop}/{total})")

    with col_right:
        st.header("📖 Ostrom's Principles")

        st.markdown(
            """
        **8 Design Principles for Successful Commons:**
        
        1️⃣ **Clearly Defined Boundaries**
        - Wer gehört dazu?
        - Welche Ressourcen?
        
        2️⃣ **Proportional Equivalence**
        - Nutzen ∝ Beitrag
        - Fairness
        
        3️⃣ **Collective Choice**
        - Alle entscheiden mit
        - Demokratisch
        
        4️⃣ **Monitoring**
        - Transparenz
        - Peer-Überwachung
        
        5️⃣ **Graduated Sanctions**
        - Milde Strafen zuerst
        - Eskalation nur bei Wiederholung
        
        6️⃣ **Conflict Resolution**
        - Schnelle, lokale Lösungen
        - Mediation
        
        7️⃣ **Minimal Recognition of Rights**
        - Externe Anerkennung
        - Autonomie
        
        8️⃣ **Nested Enterprises**
        - Mehrere Ebenen
        - Polyzentrisch
        """
        )

        st.divider()

        st.subheader("🗺️ Global Examples of Successful Commons")

        from utils.map_helpers import create_cooperation_examples_map, render_minimap

        m = create_cooperation_examples_map()
        render_minimap(
            m,
            "Ostrom's documented examples: forests, water systems, fishing communities (centuries of success)",
        )

        st.divider()

        st.markdown(
            """
        **Categories:**
        
        🌊 **Fishing Communities:**
        - Japan: Coastal fishing (centuries)
        - Maine, USA: Lobster gangs
        
        🌲 **Forest Management:**
        - Swiss Alpine Commons (800+ years)
        - Nepal Community Forests
        
        💧 **Water Systems:**
        - Spanish Huertas (Valencia, 1000+ years)
        - Bali Subak (irrigation, UNESCO)
        
        🏫 **Education:**
        - Sudbury Valley School (USA)
        - Folk High Schools (Denmark)
        - Free Schools (UK)
        """
        )

        st.divider()

        st.subheader("🧮 Implementation")

        st.markdown(
            """
        **Simulation Details:**
        
        - Agent-Based Model
        - Probabilistic Strategy Updates
        - Dynamic Equilibrium
        
        **Code:** `zwi_streamlit.py` (standalone app)
        """
        )

    st.divider()

    # Formulas Section
    st.header("📐 Game Theory & Payoffs")

    tab1, tab2, tab3 = st.tabs(["Payoff Matrix", "Nash Equilibrium", "Ostrom Theory"])

    with tab1:
        st.subheader("Payoff Matrix")

        st.markdown(
            """
        **2-Player Game:**
        
        |   | Cooperate | Defect |
        |---|-----------|--------|
        | **Cooperate** | (R, R) | (S, T) |
        | **Defect** | (T, S) | (P, P) |
        
        **Wo:**
        - R (Reward): Beide kooperieren → beide gewinnen
        - S (Sucker): Ich kooperiere, anderer defektiert → ich verliere
        - T (Temptation): Ich defektiere, anderer kooperiert → ich gewinne kurzfristig
        - P (Punishment): Beide defektieren → beide verlieren
        
        **Prisoner's Dilemma:** T > R > P > S
        
        **In unserer Simulation:**
        """
        )

        st.latex(r"\text{Payoff}_{cooperate} = C \cdot \frac{N_{coop}}{N_{total}}")
        st.latex(
            r"\text{Payoff}_{defect} = 0.5 \cdot C - Penalty \cdot \frac{N_{defect}}{N_{total}}"
        )

        st.markdown(
            """
        **Parameter:**
        - C: Cooperation Payoff (Slider)
        - Penalty: Coercion Penalty (Slider)
        - N_coop: Anzahl Cooperators
        - N_defect: Anzahl Defectors
        - N_total: Gesamtzahl Agents
        
        **Interpretation:**
        - Mehr Cooperators → höherer Payoff für alle Cooperators
        - Mehr Defectors → höherer Penalty für alle Defectors
        - **Tipping Point:** Ab bestimmtem Cooperation-Anteil wird Kooperation dominant
        """
        )

    with tab2:
        st.subheader("Nash Equilibrium")

        st.markdown(
            """
        **Definition:**
        
        Ein **Nash Equilibrium** ist ein Strategieprofil, bei dem kein Spieler durch einseitige Strategieänderung seinen Payoff verbessern kann.
        
        **In Prisoner's Dilemma:**
        - Nash Equilibrium: **(Defect, Defect)**
        - Aber: Pareto-optimal ist **(Cooperate, Cooperate)**
        
        **Problem:** Individuell rational ≠ kollektiv rational
        
        **Lösung (Ostrom):**
        - Wiederholte Interaktionen (Iterated Game)
        - Reputation
        - Soziale Normen
        - Kommunikation
        
        **In unserer Simulation:**
        """
        )

        st.latex(
            r"\text{Equilibrium} = \begin{cases} \text{Cooperate} & \text{if } C > Penalty \\ \text{Defect} & \text{if } Penalty > C \end{cases}"
        )

        st.markdown(
            """
        **Dynamisches Gleichgewicht:**
        - Agents lernen und passen Strategien an
        - Evolutionär stabile Strategien (ESS)
        - **Tit-for-Tat** (Axelrod 1984) oft optimal
        
        **Relevanz für 5D:**
        - **Autonomy:** Freie Strategiewahl
        - **Intrinsic Motivation:** Kooperation belohnend
        - **Resilience:** System erholt sich von Defektion
        - **Social Participation:** Interaktion notwendig
        - **Authenticity:** Ehrliche Signale
        """
        )

    with tab3:
        st.subheader("Ostrom's Theory")

        st.markdown(
            """
        **Governing the Commons (1990):**
        
        Elinor Ostrom widerlegte **Garrett Hardin's "Tragedy of the Commons"** (1968):
        
        **Hardin:** Gemeingüter führen zwangsläufig zur Übernutzung
        → Lösung: Privatisierung oder staatliche Kontrolle
        
        **Ostrom:** Selbstorganisierte Communities können Commons nachhaltig verwalten
        → Lösung: Lokale Regeln, Partizipation, Monitoring
        
        **Empirische Evidenz:**
        - 5000+ dokumentierte Fälle weltweit
        - Jahrhunderte erfolgreicher Selbstverwaltung
        - Keine zentrale Autorität notwendig
        
        **Kernidee:**
        """
        )

        st.latex(
            r"\text{Cooperation} \propto \frac{\text{Trust} \times \text{Communication}}{\text{Coercion}}"
        )

        st.markdown(
            """
        **8 Design Principles** (siehe rechte Spalte) garantieren Erfolg
        
        **Nobelpreis 2009:**
        - Erste Frau mit Wirtschaftsnobelpreis für Commons-Forschung
        - Paradigmenwechsel: Nicht-staatliche, nicht-marktwirtschaftliche Lösungen
        
        **Anwendung auf Bildung:**
        - **Schulen als Commons:** Wissen ist Gemeingut
        - **Selbstverwaltung:** Sudbury, Summerhill, Folk High Schools
        - **Partizipation:** Schüler entscheiden mit
        - **Intrinsische Motivation:** Keine Zwangsnoten
        
        **Literatur:**
        - Ostrom, E. (1990). *Governing the Commons*. Cambridge University Press.
        - Ostrom, E. (2010). *Beyond Markets and States*. Nobel Prize Lecture.
        - Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
        """
        )

    st.divider()

    # Scientific References
    st.header("📚 Wissenschaftliche Quellen")

    with st.expander("🔬 References (expandable)"):
        st.markdown(
            """
        ### Primärquellen
        
        **1. Ostrom, E. (1990)**
        - *Governing the Commons: The Evolution of Institutions for Collective Action*
        - Cambridge University Press
        - ISBN: 978-0521405997
        - DOI: 10.1017/CBO9780511807763
        
        **2. Ostrom, E. (2010)**
        - *Beyond Markets and States: Polycentric Governance of Complex Economic Systems*
        - Nobel Prize Lecture, December 8, 2010
        - [nobelprize.org](https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/lecture/)
        
        **3. Axelrod, R. (1984)**
        - *The Evolution of Cooperation*
        - Basic Books
        - ISBN: 978-0465005642
        
        **4. Hardin, G. (1968)**
        - *The Tragedy of the Commons*
        - *Science* 162(3859): 1243-1248
        - DOI: 10.1126/science.162.3859.1243
        
        ---
        
        ### Game Theory
        
        **5. Nash, J. (1950)**
        - *Equilibrium Points in N-Person Games*
        - *Proceedings of the National Academy of Sciences* 36(1): 48-49
        - DOI: 10.1073/pnas.36.1.48
        
        **6. von Neumann, J. & Morgenstern, O. (1944)**
        - *Theory of Games and Economic Behavior*
        - Princeton University Press
        
        ---
        
        ### Empirische Studien
        
        **7. Berkes, F. (1989)**
        - *Common Property Resources: Ecology and Community-Based Sustainable Development*
        - Belhaven Press
        
        **8. Dietz, T., Ostrom, E., & Stern, P. C. (2003)**
        - *The Struggle to Govern the Commons*
        - *Science* 302(5652): 1907-1912
        - DOI: 10.1126/science.1091015
        
        ---
        
        **BibTeX:** Siehe `07_daten_analysen/5d-relevant-sources.bib`
        
        **Code:** `zwi_streamlit.py` (standalone app)
        """
        )

    # Footer
    st.divider()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Theory:** Ostrom 1990")

    with col_b:
        st.markdown(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d')}")

    with col_c:
        st.markdown(
            "[zwi_streamlit.py](zwi_streamlit.py) | [Nobel Prize](https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/facts/)"
        )


if __name__ == "__main__":
    main()
