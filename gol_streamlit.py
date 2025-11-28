#!/usr/bin/env python3
"""
Streamlit Game of Life (Demo)
- Wähle Größe, Preset, Schrittzahl und Geschwindigkeit
- Steppen oder kurze Auto-Run-Sequenz
Hinweis: Für große, lange Animationen weiterhin CLI nutzen.
"""

import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
import pandas as pd
import io

# Optional: MP4 Export via imageio (falls verfügbar)
try:
    import imageio.v2 as imageio  # type: ignore
    HAS_IMAGEIO = True
except Exception:
    HAS_IMAGEIO = False

from typing import Tuple

# --- Game of Life Core ---

def game_of_life_step(grid: np.ndarray) -> np.ndarray:
    rows, cols = grid.shape
    neighbors = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            total = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = (i + di) % rows, (j + dj) % cols
                    total += grid[ni, nj]
            neighbors[i, j] = total
    new_grid = np.zeros((rows, cols), dtype=int)
    new_grid[(grid == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    new_grid[(grid == 0) & (neighbors == 3)] = 1
    return new_grid


def place_glider(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)
    h, w = glider.shape
    grid[top:top + h, left:left + w] = glider


def place_blinker(grid: np.ndarray, top: int, left: int) -> None:
    blinker = np.array([[1, 1, 1]], dtype=int)
    h, w = blinker.shape
    grid[top:top + h, left:left + w] = blinker


def place_toad(grid: np.ndarray, top: int, left: int) -> None:
    toad = np.array([[0, 1, 1, 1], [1, 1, 1, 0]], dtype=int)
    h, w = toad.shape
    grid[top:top + h, left:left + w] = toad


def place_gosper_glider_gun(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    pattern = [
        (0, 24), (1, 22), (1, 24), (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
        (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
        (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
        (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
        (6, 10), (6, 16), (6, 24), (7, 11), (7, 15), (8, 12), (8, 13)
    ]
    for di, dj in pattern:
        i, j = top + di, left + dj
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            grid[i, j] = 1


def place_block(grid: np.ndarray, top: int, left: int) -> None:
    block = np.array([[1, 1], [1, 1]], dtype=int)
    h, w = block.shape
    grid[top:top + h, left:left + w] = block


def place_beehive(grid: np.ndarray, top: int, left: int) -> None:
    beehive = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ], dtype=int)
    h, w = beehive.shape
    grid[top:top + h, left:left + w] = beehive


def place_loaf(grid: np.ndarray, top: int, left: int) -> None:
    loaf = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ], dtype=int)
    h, w = loaf.shape
    grid[top:top + h, left:left + w] = loaf


def place_boat(grid: np.ndarray, top: int, left: int) -> None:
    boat = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ], dtype=int)
    h, w = boat.shape
    grid[top:top + h, left:left + w] = boat


def place_tub(grid: np.ndarray, top: int, left: int) -> None:
    tub = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ], dtype=int)
    h, w = tub.shape
    grid[top:top + h, left:left + w] = tub


def place_beacon(grid: np.ndarray, top: int, left: int) -> None:
    beacon = np.array([
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ], dtype=int)
    h, w = beacon.shape
    grid[top:top + h, left:left + w] = beacon


def place_lwss(grid: np.ndarray, top: int, left: int) -> None:
    lwss = np.array([
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0]
    ], dtype=int)
    h, w = lwss.shape
    grid[top:top + h, left:left + w] = lwss


def place_pulsar(grid: np.ndarray, top: int, left: int) -> None:
    base = np.zeros((17, 17), dtype=int)
    pts = [
        (2,4),(2,5),(2,6),(2,10),(2,11),(2,12),
        (4,2),(5,2),(6,2),(4,7),(5,7),(6,7),(4,9),(5,9),(6,9),(4,14),(5,14),(6,14),
        (7,4),(7,5),(7,6),(7,10),(7,11),(7,12),
        (9,4),(9,5),(9,6),(9,10),(9,11),(9,12),
        (10,2),(11,2),(12,2),(10,7),(11,7),(12,7),(10,9),(11,9),(12,9),(10,14),(11,14),(12,14),
        (14,4),(14,5),(14,6),(14,10),(14,11),(14,12)
    ]
    for r, c in pts:
        if 0 <= top + r < grid.shape[0] and 0 <= left + c < grid.shape[1]:
            grid[top + r, left + c] = 1


def place_acorn(grid: np.ndarray, top: int, left: int) -> None:
    pts = [
        (0,1),
        (1,3),
        (2,0),(2,1),(2,4),(2,5),(2,6)
    ]
    for r, c in pts:
        if 0 <= top + r < grid.shape[0] and 0 <= left + c < grid.shape[1]:
            grid[top + r, left + c] = 1


def place_diehard(grid: np.ndarray, top: int, left: int) -> None:
    pts = [
        (0,6),
        (1,0),(1,1),
        (2,1),(2,5),(2,6),(2,7)
    ]
    for r, c in pts:
        if 0 <= top + r < grid.shape[0] and 0 <= left + c < grid.shape[1]:
            grid[top + r, left + c] = 1


# --- UI ---

st.set_page_config(page_title="Game of Life", page_icon="🧬", layout="centered")
st.title("🧬 Conway's Game of Life – Streamlit Demo")

with st.sidebar:
    st.header("Einstellungen")
    # Dynamische Min/Max-Skalierung (in Session State halten)
    if "_ui_bounds" not in st.session_state:
        st.session_state._ui_bounds = {
            "size_min": 10, "size_max": 200,
            "steps_min": 1, "steps_max": 1000,
            "interval_min": 10, "interval_max": 1000,
            "px_min": 100, "px_max": 2000,
        }
    b = st.session_state._ui_bounds

    with st.expander("Skalierung (Min/Max)"):
        c1, c2 = st.columns(2)
        with c1:
            b["size_min"] = st.number_input("Grid min", min_value=1, max_value=1000, value=b["size_min"], step=1)
            b["steps_min"] = st.number_input("Steps min", min_value=1, max_value=100000, value=b["steps_min"], step=1)
            b["interval_min"] = st.number_input("Intervall min (ms)", min_value=1, max_value=10000, value=b["interval_min"], step=1)
            b["px_min"] = st.number_input("Bild min (px)", min_value=10, max_value=10000, value=b["px_min"], step=10)
        with c2:
            b["size_max"] = st.number_input("Grid max", min_value=b["size_min"], max_value=2000, value=b["size_max"], step=1)
            b["steps_max"] = st.number_input("Steps max", min_value=b["steps_min"], max_value=200000, value=b["steps_max"], step=10)
            b["interval_max"] = st.number_input("Intervall max (ms)", min_value=b["interval_min"], max_value=60000, value=b["interval_max"], step=10)
            b["px_max"] = st.number_input("Bild max (px)", min_value=b["px_min"], max_value=20000, value=b["px_max"], step=50)

    preset = st.selectbox(
        "Preset",
        [
            "glider",
            "blinker",
            "toad",
            "beacon",
            "block",
            "beehive",
            "loaf",
            "boat",
            "tub",
            "lwss",
            "pulsar",
            "acorn",
            "diehard",
            "gosper",
        ],
        index=0,
        help="Startmuster: einfacher = stabiler, komplexer = dynamischer."
    )
    engine = st.selectbox(
        "Engine",
        ["Wrap (NumPy)", "Bounded (Pure Python)"],
        index=0,
        help="Wrap: periodische Ränder; Bounded: harte Kanten ohne Wrap."
    )
    # Defaults im erlaubten Bereich halten
    default_size = 40 if preset == "gosper" else 25
    default_size = int(min(max(default_size, b["size_min"]), b["size_max"]))
    size = st.slider(
        "Grid-Größe",
        min_value=int(b["size_min"]), max_value=int(b["size_max"]), value=default_size, step=1,
        help="Je größer, desto langlebigere Dynamik; je kleiner, desto schneller."
    )

    steps = st.slider(
        "Schritte (Auto-Run)",
        min_value=int(b["steps_min"]), max_value=int(b["steps_max"]), value=min(60, int(b["steps_max"])), step=1,
        help="Auto-Run Startschritte: mehr = weiter vorspulen, weniger = feinere Beobachtung."
    )
    interval_ms = st.slider(
        "Intervall (ms)",
        min_value=int(b["interval_min"]), max_value=int(b["interval_max"]), value=min(120, int(b["interval_max"])), step=10,
        help="Zeit pro Tick: kleiner = flüssiger, größer = ruhiger."
    )
    size_px = st.number_input(
        "Bild-Pixelgröße",
        min_value=int(b["px_min"]), max_value=int(b["px_max"]), value=min(400, int(b["px_max"])), step=50,
        help="Bildgröße: größer = lesbarer, kleiner = schnelleres Rendering."
    )
    st.subheader("Auto-Run")
    autoplay_batch = st.selectbox("Batch-Steps pro Tick", [1,2,5,10], index=0, help="Schritte pro Tick im Auto-Run; höher = schnelleres Vorspulen.")
    start_btn = st.button("Start", help="Auto-Run starten (nutzt Batch-Steps pro Tick).")
    pause_btn = st.button("Pause", help="Auto-Run pausieren; Zustand bleibt erhalten.")
    stop_btn = st.button("Stop", help="Auto-Run stoppen und Pausen-Status zurücksetzen.")
    reset_btn = st.button("Reset Grid", help="Grid neu initialisieren mit aktuellem Preset/Größe.")

    st.subheader("Speichern")
    save_snapshot_btn = st.button("Snapshot speichern (Grid + PNG)", help="Speichert aktuelles Grid als .npy und PNG.")
    save_history_btn = st.button("Verlauf speichern (CSV)", help="Speichert (step, live_cells) als CSV.")

    st.subheader("Export")
    export_steps = st.number_input(
        "Export-Schritte",
        min_value=1, max_value=5000, value=120, step=10,
        help="Anzahl Schritte für Export (ohne das aktuelle Grid zu verändern)."
    )
    export_ms = st.number_input(
        "Frame-Dauer (ms)",
        min_value=10, max_value=2000, value=100, step=10,
        help="Frame-Dauer: kleiner = höhere Abspielgeschwindigkeit."
    )
    export_gif_btn = st.button("GIF exportieren", help="Exportiert Sequenz als GIF.")
    export_mp4_btn = st.button("MP4 exportieren (ffmpeg)", help="Exportiert MP4 (ffmpeg erforderlich).")

    st.subheader("Laden")
    up_npy = st.file_uploader("Grid laden (.npy)", type=["npy"], accept_multiple_files=False, help="Binäres Grid laden (0/1).")
    up_png = st.file_uploader("Grid laden (.png)", type=["png"], accept_multiple_files=False, help="Graustufen-PNG wird skaliert und binarisiert (>=128 → 1).")
    load_npy_btn = st.button("NPY laden", help="Übernimmt hochgeladenes .npy in das Grid.")
    load_png_btn = st.button("PNG laden", help="Übernimmt skaliertes/binarisiertes PNG in das Grid.")

# Session State init
if "grid" not in st.session_state or reset_btn:
    min_size = {
        "gosper": 40,
        "pulsar": 25,
        "lwss": 20,
        "acorn": 20,
        "diehard": 20,
    }.get(preset, 10)
    n = max(min_size, size)
    grid = np.zeros((n, n), dtype=int)
    if preset == "glider":
        place_glider(grid, 1, 1)
    elif preset == "blinker":
        place_blinker(grid, n // 2, max(1, n // 2 - 1))
    elif preset == "toad":
        place_toad(grid, n // 2 - 1, max(1, n // 2 - 2))
    elif preset == "beacon":
        place_beacon(grid, n // 2 - 2, n // 2 - 2)
    elif preset == "block":
        place_block(grid, n // 2 - 1, n // 2 - 1)
    elif preset == "beehive":
        place_beehive(grid, n // 2 - 1, n // 2 - 2)
    elif preset == "loaf":
        place_loaf(grid, n // 2 - 2, n // 2 - 2)
    elif preset == "boat":
        place_boat(grid, n // 2 - 1, n // 2 - 1)
    elif preset == "tub":
        place_tub(grid, n // 2 - 1, n // 2 - 1)
    elif preset == "lwss":
        place_lwss(grid, max(1, n // 2 - 2), max(1, n // 2 - 3))
    elif preset == "pulsar":
        place_pulsar(grid, max(1, n // 2 - 8), max(1, n // 2 - 8))
    elif preset == "acorn":
        place_acorn(grid, n // 2 - 1, n // 2 - 3)
    elif preset == "diehard":
        place_diehard(grid, n // 2 - 1, n // 2 - 4)
    elif preset == "gosper":
        place_gosper_glider_gun(grid, 1, 1)
    st.session_state.grid = grid
    st.session_state.history = []
    st.session_state.step_idx = 0
    st.session_state.running = False
    st.session_state.paused = False

# Plot helper
plot_area = st.empty()
chart_area = st.empty()

def render(grid: np.ndarray, size_px: int = 400):
    # Erzeuge ein 2D-Grayscale-Bild aus dem Grid und skaliere auf size_px x size_px
    img = (grid * 255).astype(np.uint8)
    pil = Image.fromarray(img, mode='L').resize((size_px, size_px), resample=Image.NEAREST)
    plot_area.image(pil, caption=None, width=size_px, clamp=True)

def render_chart(history):
    if not history:
        chart_area.empty()
        return
    df = pd.DataFrame(history, columns=["step", "live_cells"]).set_index("step")
    chart_area.line_chart(df)


def simulate_frames(grid: np.ndarray, steps: int, engine_mode: str, size_px: int):
    """Erzeuge PIL-Frames und History, ohne das Session-Grid zu verändern."""
    frames = []
    history = []
    g = grid.copy()
    local_step = 0
    for _ in range(int(steps)):
        # Render current frame
        img_arr = (g * 255).astype(np.uint8)
        pil = Image.fromarray(img_arr, mode='L').resize((size_px, size_px), resample=Image.NEAREST)
        frames.append(pil)
        local_step += 1
        history.append((local_step, int(np.sum(g))))
        # advance
        if engine_mode.startswith("Wrap"):
            g = game_of_life_step(g)
        else:
            lst = g.astype(int).tolist()
            lst = game_of_life_py(lst, steps=1)
            g = np.array(lst, dtype=int)
    return frames, history

# --- Alternative Engine (Pure Python, bounded) ---
def game_of_life_py(grid_list, steps=1):
    rows, cols = len(grid_list), len(grid_list[0])
    for _ in range(steps):
        new_grid = [[0]*cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                neighbors = 0
                for x in range(max(0, i-1), min(rows, i+2)):
                    for y in range(max(0, j-1), min(cols, j+2)):
                        if (x, y) != (i, j):
                            neighbors += grid_list[x][y]
                new_grid[i][j] = 1 if ((grid_list[i][j] and neighbors in (2,3)) or (not grid_list[i][j] and neighbors == 3)) else 0
        grid_list[:] = [row[:] for row in new_grid]
    return grid_list

# Controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Step"):
        if engine.startswith("Wrap"):
            st.session_state.grid = game_of_life_step(st.session_state.grid)
        else:
            lst = st.session_state.grid.astype(int).tolist()
            lst = game_of_life_py(lst, steps=1)
            st.session_state.grid = np.array(lst, dtype=int)
        st.session_state.step_idx += 1
        st.session_state.history.append((st.session_state.step_idx, int(np.sum(st.session_state.grid))))
        render(st.session_state.grid, size_px=size_px)
with col2:
    if st.button("10 Steps"):
        g = st.session_state.grid
        if engine.startswith("Wrap"):
            for _ in range(10):
                g = game_of_life_step(g)
                st.session_state.step_idx += 1
                st.session_state.history.append((st.session_state.step_idx, int(np.sum(g))))
        else:
            lst = g.astype(int).tolist()
            lst = game_of_life_py(lst, steps=10)
            g = np.array(lst, dtype=int)
            st.session_state.step_idx += 10
            st.session_state.history.append((st.session_state.step_idx, int(np.sum(g))))
        st.session_state.grid = g
        render(st.session_state.grid, size_px=size_px)
with col3:
    if st.button("Clear"):
        st.session_state.grid = np.zeros_like(st.session_state.grid)
        st.session_state.step_idx = 0
        st.session_state.history = []
        render(st.session_state.grid, size_px=size_px)
        render_chart(st.session_state.history)
    if st.button("Verlauf zurücksetzen"):
        st.session_state.step_idx = 0
        st.session_state.history = []
        render_chart(st.session_state.history)
with col4:
    st.write("")
    st.write("")
    st.caption("Autoplay (einmalig):")
    cA, cB, cC, cD = st.columns(4)
    with cA:
        if st.button("+1"):
            g = st.session_state.grid
            for _ in range(1):
                if engine.startswith("Wrap"):
                    g = game_of_life_step(g)
                else:
                    lst = g.astype(int).tolist()
                    lst = game_of_life_py(lst, steps=1)
                    g = np.array(lst, dtype=int)
                st.session_state.grid = g
                render(g, size_px=size_px)
                time.sleep(max(0.001, interval_ms/1000.0))
    with cB:
        if st.button("+2"):
            g = st.session_state.grid
            for _ in range(2):
                if engine.startswith("Wrap"):
                    g = game_of_life_step(g)
                else:
                    lst = g.astype(int).tolist()
                    lst = game_of_life_py(lst, steps=1)
                    g = np.array(lst, dtype=int)
                st.session_state.grid = g
                render(g, size_px=size_px)
                time.sleep(max(0.001, interval_ms/1000.0))
    with cC:
        if st.button("+5"):
            g = st.session_state.grid
            for _ in range(5):
                if engine.startswith("Wrap"):
                    g = game_of_life_step(g)
                else:
                    lst = g.astype(int).tolist()
                    lst = game_of_life_py(lst, steps=1)
                    g = np.array(lst, dtype=int)
                st.session_state.grid = g
                render(g, size_px=size_px)
                time.sleep(max(0.001, interval_ms/1000.0))
    with cD:
        if st.button("+10"):
            g = st.session_state.grid
            for _ in range(10):
                if engine.startswith("Wrap"):
                    g = game_of_life_step(g)
                else:
                    lst = g.astype(int).tolist()
                    lst = game_of_life_py(lst, steps=1)
                    g = np.array(lst, dtype=int)
                st.session_state.grid = g
                render(g, size_px=size_px)
                time.sleep(max(0.001, interval_ms/1000.0))

# Render
render(st.session_state.grid, size_px=size_px)
render_chart(st.session_state.get('history', []))

# Start/Pause/Stop Handling
if start_btn:
    st.session_state.running = True
    st.session_state.paused = False
if pause_btn:
    st.session_state.paused = True
if stop_btn:
    st.session_state.running = False
    st.session_state.paused = False

# Save actions
if save_snapshot_btn:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    np.save(f'gol_grid_{ts}.npy', st.session_state.grid)
    img = (st.session_state.grid * 255).astype(np.uint8)
    Image.fromarray(img, mode='L').resize((size_px, size_px), resample=Image.NEAREST).save(f'gol_grid_{ts}.png')
    st.success(f"Snapshot gespeichert: gol_grid_{ts}.npy / gol_grid_{ts}.png")
if save_history_btn:
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    hist = np.array(st.session_state.get('history', []), dtype=int) if st.session_state.get('history') else np.zeros((0,2), dtype=int)
    np.savetxt(f'gol_history_{ts}.csv', hist, delimiter=',', header='step,live_cells', fmt='%d')
    st.success(f"Verlauf gespeichert: gol_history_{ts}.csv")

# Export actions
if export_gif_btn:
    try:
        frames, h = simulate_frames(st.session_state.grid, steps=export_steps, engine_mode=engine, size_px=size_px)
        buf = io.BytesIO()
        frames[0].save(buf, format='GIF', save_all=True, append_images=frames[1:], duration=int(export_ms), loop=0)
        buf.seek(0)
        st.download_button("GIF herunterladen", buf, file_name=f"gol_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif", mime="image/gif")
        st.info("Export basiert auf Kopie – aktuelles Grid wurde nicht verändert.")
    except Exception as e:
        st.error(f"GIF Export fehlgeschlagen: {e}")

if export_mp4_btn:
    if not HAS_IMAGEIO:
        st.warning("imageio/ffmpeg nicht verfügbar – bitte 'pip install imageio imageio-ffmpeg' und ffmpeg installieren.")
    else:
        try:
            frames, h = simulate_frames(st.session_state.grid, steps=export_steps, engine_mode=engine, size_px=size_px)
            buf = io.BytesIO()
            # imageio benötigt raw arrays (H,W,3) oder (H,W) – konvertieren zu RGB
            fps = max(1, int(1000 / max(1, export_ms)))
            # Temporär auf Disk schreiben, dann anbieten (in-memory Writer nicht überall stabil)
            out_name = f"gol_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            with imageio.get_writer(out_name, fps=fps) as writer:
                for pil in frames:
                    writer.append_data(np.array(pil.convert('RGB')))
            with open(out_name, 'rb') as f:
                st.download_button("MP4 herunterladen", f.read(), file_name=out_name, mime="video/mp4")
            st.info("MP4 wurde erzeugt (ffmpeg erforderlich).")
        except Exception as e:
            st.error(f"MP4 Export fehlgeschlagen: {e}")

# Load actions
if load_npy_btn and up_npy is not None:
    try:
        import io
        buf = io.BytesIO(up_npy.read())
        arr = np.load(buf, allow_pickle=False)
        arr = (arr > 0).astype(int)
        st.session_state.grid = arr
        st.session_state.step_idx = 0
        st.session_state.history = []
        render(st.session_state.grid, size_px=size_px)
        render_chart(st.session_state.history)
        st.success("NPY geladen und gesetzt.")
    except Exception as e:
        st.error(f"NPY Laden fehlgeschlagen: {e}")
if load_png_btn and up_png is not None:
    try:
        img = Image.open(up_png).convert('L')
        # auf aktuelle Grid-Größe skalieren und binarisieren
        n = st.session_state.grid.shape[0]
        img = img.resize((n, n), resample=Image.NEAREST)
        arr = np.array(img)
        arr = (arr >= 128).astype(int)
        st.session_state.grid = arr
        st.session_state.step_idx = 0
        st.session_state.history = []
        render(st.session_state.grid, size_px=size_px)
        render_chart(st.session_state.history)
        st.success("PNG geladen, skaliert und gesetzt.")
    except Exception as e:
        st.error(f"PNG Laden fehlgeschlagen: {e}")

# Auto-run (kurze Demo, nicht endlos)
# Non-blocking-ish auto-run via reruns
if st.session_state.get('running') and not st.session_state.get('paused'):
    g = st.session_state.grid
    batch = int(autoplay_batch)
    if engine.startswith("Wrap"):
        for _ in range(batch):
            g = game_of_life_step(g)
            st.session_state.step_idx += 1
            st.session_state.history.append((st.session_state.step_idx, int(np.sum(g))))
    else:
        lst = g.astype(int).tolist()
        lst = game_of_life_py(lst, steps=batch)
        g = np.array(lst, dtype=int)
        st.session_state.step_idx += batch
        st.session_state.history.append((st.session_state.step_idx, int(np.sum(g))))
    st.session_state.grid = g
    render(g, size_px=size_px)
    render_chart(st.session_state.history)
    time.sleep(max(0.005, interval_ms / 1000.0))
    # Streamlit API: bevorzugt st.rerun(), kompatibel mit älteren Versionen
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# Editor-Modus
with st.expander("Editor-Modus (Zellen anklicken/setzen)"):
    enable_editor = st.checkbox("Editor aktiv", value=False, help="Bearbeite das Grid als Tabelle (0/1). Für sehr große Grids kann das langsam sein.")
    if enable_editor:
        n = st.session_state.grid.shape[0]
        if n > 50:
            st.warning("Grid > 50 kann langsam sein im Editor. Reduziere 'Grid-Größe' für flüssige Bearbeitung.")
        df_grid = pd.DataFrame(st.session_state.grid)
        edited = st.data_editor(df_grid, use_container_width=True, num_rows="fixed")
        if st.button("Übernehmen"):
            try:
                arr = edited.to_numpy()
                arr = (arr > 0).astype(int)
                st.session_state.grid = arr
                st.session_state.step_idx = 0
                st.session_state.history = []
                render(st.session_state.grid, size_px=size_px)
                render_chart(st.session_state.history)
                st.success("Grid übernommen.")
            except Exception as e:
                st.error(f"Übernahme fehlgeschlagen: {e}")

# Parameter-Übersicht
with st.expander("Parameter-Übersicht"):
    st.markdown(
        f"""
        | Parameter | Attribut | Wert | Min | Max |
        |---|---|---:|---:|---:|
        | Preset | Muster | `{preset}` | - | - |
        | Grid-Größe | Zellen N | `{size}` | `{int(b['size_min'])}` | `{int(b['size_max'])}` |
        | Schritte (Auto) | Iterationen | `{steps}` | `{int(b['steps_min'])}` | `{int(b['steps_max'])}` |
        | Intervall | ms/Step | `{interval_ms}` | `{int(b['interval_min'])}` | `{int(b['interval_max'])}` |
        | Bild-Pixelgröße | px | `{size_px}` | `{int(b['px_min'])}` | `{int(b['px_max'])}` |
        """
    )

# Umso mehr / desto … – Kontext-Hinweise
with st.expander("Umso mehr … desto … / Umso weniger … dann …"):
    st.markdown(
        """
        - Grid-Größe: Je mehr Zellen, desto detailreicher und langlebiger die Dynamik; je weniger, desto schneller, aber randempfindlicher.
        - Schritte (Auto-Run): Je mehr, desto größer der zeitliche Vorsprung pro Start; je weniger, desto feinere Beobachtung.
        - Intervall (ms): Je höher, desto gemächlicher die Aktualisierung; je niedriger, desto flüssiger, aber CPU-intensiver.
        - Bild-Pixelgröße: Je größer, desto lesbarer; je kleiner, desto schnelleres Rendering.
        - Batch-Steps pro Tick: Je höher, desto mehr "Vorspulen" pro Tick; je niedriger, desto dichter die Zwischenzustände.
        - Engine: Wrap (Torus) hält Muster am Rand zusammen; Bounded dämpft an den Kanten und zerstäubt eher Kollisionen.
        - Editor: Je größer das Grid, desto träger die tabellarische Bearbeitung; je kleiner, desto direkter editierbar.
        - Export-Schritte: Je mehr, desto längere Clips und größere Dateien; je weniger, desto kompakt.
        - Frame-Dauer (ms): Je höher, desto längere Gesamtspielzeit bei gleicher Schrittzahl; je niedriger, desto schnellere Wiedergabe.
        - Preset: Einfache Oszillatoren (Blinker/Toad) sind stabil; komplexe Muster (Gosper) erzeugen wandernde Glider und Interferenzen.
        """
    )
