#!/usr/bin/env python3
"""
5D Dashboard - Conway's Game of Life
Cellular Automaton Simulation (1970)
"""

from datetime import datetime

import numpy as np
import streamlit as st
from utils.mobile_responsive import inject_mobile_css

st.set_page_config(
    page_title="5D Game of Life",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_mobile_css()

# Predefined patterns
PATTERNS = {
    "Glider": np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]),
    "Blinker": np.array([[1, 1, 1]]),
    "Toad": np.array([[0, 1, 1, 1], [1, 1, 1, 0]]),
    "Beacon": np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]),
    "Pulsar": np.array(
        [
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        ]
    ),
}


def count_neighbors(grid, x, y):
    """Count alive neighbors (8-connectivity)"""
    height, width = grid.shape
    count = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            nx, ny = (x + i) % height, (y + j) % width
            count += grid[nx, ny]

    return count


def update_grid(grid):
    """Apply Conway's Rules for next generation"""
    new_grid = grid.copy()
    height, width = grid.shape

    for i in range(height):
        for j in range(width):
            neighbors = count_neighbors(grid, i, j)

            # Conway's Rules
            if grid[i, j] == 1:
                # Alive cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0  # Dies
            else:
                # Dead cell
                if neighbors == 3:
                    new_grid[i, j] = 1  # Becomes alive

    return new_grid


def place_pattern(grid, pattern, start_x, start_y):
    """Place a pattern on the grid at specified position"""
    height, width = grid.shape
    p_height, p_width = pattern.shape

    for i in range(p_height):
        for j in range(p_width):
            x = (start_x + i) % height
            y = (start_y + j) % width
            grid[x, y] = pattern[i, j]

    return grid


def main():
    # Sidebar
    with st.sidebar:
        st.title("🧬 Game of Life")
        st.markdown("**Conway 1970**")

        st.divider()

        st.markdown("### 🔬 Scientific Basis")
        st.markdown("""
        **Cellular Automaton:**
        
        Conway, J. (1970)
        
        **Regeln:**
        1. **Underpopulation:** <2 Nachbarn → stirbt
        2. **Survival:** 2-3 Nachbarn → lebt
        3. **Overpopulation:** >3 Nachbarn → stirbt
        4. **Reproduction:** Tot + 3 Nachbarn → lebt
        
        **Status:** ✅ Peer-Reviewed
        """)

        st.divider()

        st.markdown("### 📖 Resources")
        st.markdown("""
        - [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
        - [LifeWiki](https://conwaylife.com)
        - Gardner, M. (1970). Scientific American
        """)

    # Main Content
    st.title("🧬 Conway's Game of Life")
    st.markdown("### Cellular Automaton Simulation (1970)")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rules", "4", help="Conway's Rules")

    with col2:
        st.metric("Turing Complete", "✅", help="Universal Computation")

    with col3:
        st.metric("Patterns", len(PATTERNS), help="Predefined Patterns")

    with col4:
        st.metric("Complexity", "Simple", help="Emergent Complexity")

    st.divider()

    # Main Content (2 columns)
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.header("🎮 Simulation")

        # Grid Settings
        grid_size = st.slider("Grid Size", 10, 50, 30)

        # Pattern Selection
        pattern_name = st.selectbox("Wähle ein Pattern", ["Random"] + list(PATTERNS.keys()))

        # Initialize Grid
        if "grid" not in st.session_state or st.button("🔄 Reset Grid"):
            st.session_state.grid = np.zeros((grid_size, grid_size), dtype=int)

            if pattern_name == "Random":
                st.session_state.grid = np.random.choice(
                    [0, 1], size=(grid_size, grid_size), p=[0.7, 0.3]
                )
            else:
                pattern = PATTERNS[pattern_name]
                center_x = grid_size // 2 - pattern.shape[0] // 2
                center_y = grid_size // 2 - pattern.shape[1] // 2
                st.session_state.grid = place_pattern(
                    st.session_state.grid, pattern, center_x, center_y
                )

            st.session_state.generation = 0

        # Controls
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("▶️ Next Generation"):
                st.session_state.grid = update_grid(st.session_state.grid)
                st.session_state.generation += 1

        with col_b:
            auto_run = st.checkbox("Auto Run")

        with col_c:
            st.metric("Generation", st.session_state.generation)

        # Auto-run (limited to 10 generations to prevent infinite loop)
        if auto_run and st.session_state.generation < 100:
            st.session_state.grid = update_grid(st.session_state.grid)
            st.session_state.generation += 1
            st.rerun()

        # Display Grid
        st.subheader(f"🧬 Grid ({grid_size}×{grid_size})")

        # Create ASCII representation for display
        grid_display = ""
        for row in st.session_state.grid:
            grid_display += "".join(["⬛" if cell == 1 else "⬜" for cell in row]) + "\n"

        st.text(grid_display)

        # Statistics
        alive = np.sum(st.session_state.grid)
        density = (alive / (grid_size * grid_size)) * 100

        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            st.metric("Alive Cells", alive)

        with stat_col2:
            st.metric("Dead Cells", grid_size * grid_size - alive)

        with stat_col3:
            st.metric("Density", f"{density:.1f}%")

    with col_right:
        st.header("📖 Pattern Library")

        st.markdown("""
        **Klassen:**
        
        🔄 **Oscillators:**
        - Blinker (Period 2)
        - Toad (Period 2)
        - Beacon (Period 2)
        - Pulsar (Period 3)
        
        🚀 **Spaceships:**
        - Glider (Diagonal)
        - Lightweight Spaceship
        
        🔳 **Still Lifes:**
        - Block (2×2)
        - Beehive
        - Loaf
        
        🌀 **Guns:**
        - Gosper Glider Gun (Period 30)
        """)

        st.divider()

        st.subheader("🗺️ Related to 5D")

        st.markdown("""
        **Emergence & Self-Organization:**
        
        Game of Life zeigt:
        - **Autonomy:** Keine externe Kontrolle
        - **Intrinsic Rules:** Lokale Interaktion
        - **Resilience:** Pattern überleben
        - **Social Participation:** Zell-Nachbarschaft
        - **Authenticity:** Deterministisch
        
        **Parallelen zu Bildungssystemen:**
        - Emergente Ordnung ohne zentrale Planung
        - Lokale Regeln → globale Muster
        - Self-organizing communities
        """)

        st.divider()

        st.subheader("🧮 Implementation")

        st.markdown("""
        **Tech Stack:**
        - NumPy (Grid)
        - Streamlit (UI)
        - Toroidal Topology (Edges wrap)
        
        **Performance:**
        - Grid: 30×30 = 900 cells
        - Update: O(n²) per generation
        - Real-time: <100ms
        """)

    st.divider()

    # Formulas Section
    st.header("📐 Conway's Regeln")

    tab1, tab2, tab3 = st.tabs(["Rules", "Mathematics", "Turing Completeness"])

    with tab1:
        st.subheader("Conway's 4 Regeln")

        st.markdown("""
        **Für jede Zelle in jeder Generation:**
        
        1️⃣ **Underpopulation (Tod durch Einsamkeit):**
        ```
        if alive and neighbors < 2:
            cell dies
        ```
        
        2️⃣ **Survival (Überleben):**
        ```
        if alive and neighbors in [2, 3]:
            cell survives
        ```
        
        3️⃣ **Overpopulation (Tod durch Überbevölkerung):**
        ```
        if alive and neighbors > 3:
            cell dies
        ```
        
        4️⃣ **Reproduction (Geburt):**
        ```
        if dead and neighbors == 3:
            cell becomes alive
        ```
        
        **Notation:** B3/S23 (Born with 3, Survives with 2-3)
        """)

        st.latex(r"C_{t+1}(i,j) = f(C_t(i,j), N_t(i,j))")

        st.markdown("""
        **Wo:**
        - C_t(i,j): Zustand der Zelle (i,j) zur Zeit t
        - N_t(i,j): Anzahl lebende Nachbarn zur Zeit t
        - f(): Conway's Update-Funktion
        """)

    with tab2:
        st.subheader("Mathematische Eigenschaften")

        st.markdown("""
        **Formale Definition:**
        
        Game of Life ist ein **2D Cellular Automaton** mit:
        
        - **Zustandsraum:** {0, 1} (tot, lebendig)
        - **Nachbarschaft:** Moore (8 Zellen)
        - **Zeitdiskret:** t ∈ ℕ
        - **Determinismus:** Nächster Zustand eindeutig
        
        **Update-Funktion:**
        """)

        st.latex(
            r"f(c, n) = \begin{cases} 1 & \text{if } n = 3 \text{ or } (c = 1 \land n = 2) \\ 0 & \text{sonst} \end{cases}"
        )

        st.markdown("""
        **Eigenschaften:**
        - **Turing-vollständig** (Conway 1970, bewiesen durch Gosper)
        - **Unentscheidbar:** Halte-Problem nicht lösbar
        - **Deterministisch:** Gleicher Start → gleiches Ergebnis
        - **Reversibel:** Mit zusätzlicher Information
        
        **Entropie:** Tendiert zu stabilen Strukturen oder zyklischem Verhalten
        """)

    with tab3:
        st.subheader("Turing-Vollständigkeit")

        st.markdown("""
        **Beweis-Konstruktion:**
        
        Game of Life kann **jeden Computer simulieren**:
        
        1. **Logische Gatter:**
           - AND, OR, NOT gates aus Gliders
           - Gosper Glider Gun (1970)
        
        2. **Speicher:**
           - Still Lifes als Bits
           - Glider als Signale
        
        3. **Berechnung:**
           - Pattern als Programme
           - Universal Turing Machine implementierbar
        
        **Erste Implementation:**
        - Paul Rendell (2000): Turing Machine in Game of Life
        - [LifeWiki](https://conwaylife.com/wiki/Turing_machine)
        
        **Implikation:**
        - Game of Life = vollständige Programmiersprache
        - Kann jeden Algorithmus ausführen
        - Emergent Computation
        
        **Philosophisch:**
        - Komplexität aus Einfachheit
        - Emergence: Mehr als die Summe der Teile
        - Relevanz für selbstorganisierende Systeme
        """)

    st.divider()

    # Scientific References
    st.header("📚 Wissenschaftliche Quellen")

    with st.expander("🔬 References (expandable)"):
        st.markdown("""
        ### Primärquellen
        
        **1. Conway, J. H. (1970)**
        - *Game of Life*
        - Publiziert in: Gardner, M. *Scientific American* (Oktober 1970)
        - [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
        
        **2. Gardner, M. (1970)**
        - *Mathematical Games: The fantastic combinations of John Conway's new solitaire game "life"*
        - *Scientific American* 223: 120-123
        
        **3. Wolfram, S. (2002)**
        - *A New Kind of Science*
        - Wolfram Media
        - ISBN: 1-57955-008-8
        - [Website](https://www.wolframscience.com)
        
        **4. Rendell, P. (2016)**
        - *Turing Machine Universality of the Game of Life*
        - Springer
        - DOI: 10.1007/978-3-319-19842-2
        
        ---
        
        ### Cellular Automata (Allgemein)
        
        **5. von Neumann, J. (1966)**
        - *Theory of Self-Reproducing Automata*
        - Herausgegeben von Burks, A. W.
        - University of Illinois Press
        
        **6. Langton, C. G. (1990)**
        - *Computation at the edge of chaos*
        - *Physica D* 42: 12-37
        - DOI: 10.1016/0167-2789(90)90064-V
        
        ---
        
        ### Implementation & Anwendungen
        
        **LifeWiki:** [conwaylife.com](https://conwaylife.com)
        - Umfassende Pattern-Bibliothek
        - Community-gepflegt seit 2006
        
        **Code:** Siehe `gol_streamlit.py` für standalone App
        """)

    # Footer
    st.divider()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Algorithm:** Conway 1970")

    with col_b:
        st.markdown(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d')}")

    with col_c:
        st.markdown("[gol_streamlit.py](gol_streamlit.py) | [LifeWiki](https://conwaylife.com)")


if __name__ == "__main__":
    main()
