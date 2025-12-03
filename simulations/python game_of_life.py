import argparse
import numpy as np

# Optional: Visualisierung (nur wenn matplotlib installiert ist)
try:
    import matplotlib.pyplot as plt
    from matplotlib import animation
    HAS_MPL = True
except Exception:
    HAS_MPL = False


def game_of_life_step(grid: np.ndarray) -> np.ndarray:
    """Simuliert einen Game-of-Life Step (periodische Ränder)."""
    rows, cols = grid.shape
    neighbors = np.zeros((rows, cols), dtype=int)

    # 8 Nachbarn zählen (periodische Randbedingungen via Modulo)
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

    # Regeln: Überleben (2–3), Geburt (genau 3)
    new_grid = np.zeros((rows, cols), dtype=int)
    new_grid[(grid == 1) & ((neighbors == 2) | (neighbors == 3))] = 1
    new_grid[(grid == 0) & (neighbors == 3)] = 1
    return new_grid


def place_glider(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    """Platziert einen Glider bei (top,left)."""
    glider = np.array([[0, 1, 0],
                       [0, 0, 1],
                       [1, 1, 1]], dtype=int)
    h, w = glider.shape
    grid[top:top + h, left:left + w] = glider

def place_blinker(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    """Einfacher Oszillator (Periode 2)."""
    blinker = np.array([[1, 1, 1]], dtype=int)
    h, w = blinker.shape
    grid[top:top + h, left:left + w] = blinker

def place_toad(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    """Oszillator (Periode 2)."""
    toad = np.array([[0, 1, 1, 1],
                     [1, 1, 1, 0]], dtype=int)
    h, w = toad.shape
    grid[top:top + h, left:left + w] = toad

def place_gosper_glider_gun(grid: np.ndarray, top: int = 1, left: int = 1) -> None:
    """Gosper Glider Gun. Benötigt mind. ~40x40 Grid."""
    # Koordinaten der lebenden Zellen relativ zur (top,left) Position
    # Quelle: Standard-Koordinaten der Gosper Gun
    pattern = [
        (0, 24),
        (1, 22), (1, 24),
        (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
        (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
        (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
        (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
        (6, 10), (6, 16), (6, 24),
        (7, 11), (7, 15),
        (8, 12), (8, 13)
    ]
    for di, dj in pattern:
        i, j = top + di, left + dj
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            grid[i, j] = 1

def place_lwss(grid: np.ndarray, top: int, left: int) -> None:
    """Lightweight Spaceship (Periodisch, bewegt sich)."""
    # Form (5x4)
    lwss = np.array([
        [0,1,1,1,1],
        [1,0,0,0,1],
        [0,0,0,0,1],
        [1,0,0,1,0]
    ], dtype=int)
    h, w = lwss.shape
    grid[top:top+h, left:left+w] = lwss

def place_pulsar(grid: np.ndarray, top: int, left: int) -> None:
    """Pulsar (Periode 3). Benötigt ~17x17 Platz."""
    coords = [
        (2,4),(2,5),(2,6),(2,10),(2,11),(2,12),
        (7,4),(7,5),(7,6),(7,10),(7,11),(7,12),
        (9,4),(9,5),(9,6),(9,10),(9,11),(9,12),
        (14,4),(14,5),(14,6),(14,10),(14,11),(14,12),
        (4,2),(5,2),(6,2),(10,2),(11,2),(12,2),
        (4,7),(5,7),(6,7),(10,7),(11,7),(12,7),
        (4,9),(5,9),(6,9),(10,9),(11,9),(12,9),
        (4,14),(5,14),(6,14),(10,14),(11,14),(12,14)
    ]
    for di,dj in coords:
        i,j = top+di, left+dj
        if 0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]:
            grid[i,j] = 1


def simulate(grid: np.ndarray, steps: int):
    """Textuelle Simulation; gibt Liste (step, live_cells) zurück."""
    stats = []
    for step in range(steps):
        live_cells = int(np.sum(grid))
        stats.append([step, live_cells])
        print(f"Step {step:2d}: {live_cells:2d} Zellen lebendig")
        print(grid)
        print()
        grid = game_of_life_step(grid)
    return grid, np.array(stats)


def animate(grid: np.ndarray, steps: int, interval_ms: int = 150, save_csv: bool = True, save_gif: str | None = None, save_mp4: str | None = None):
    """Einfaches Matplotlib-Anim mit imshow; optional CSV schreiben."""
    if not HAS_MPL:
        raise RuntimeError("Matplotlib nicht installiert. Bitte 'pip install matplotlib' ausführen.")

    fig, ax = plt.subplots()
    im = ax.imshow(grid, cmap='binary', interpolation='nearest')
    ax.set_title("Conway's Game of Life – Glider")
    ax.set_xticks([])
    ax.set_yticks([])

    stats = []

    def update(_):
        nonlocal grid
        live = int(np.sum(grid))
        stats.append([len(stats), live])
        im.set_data(grid)
        grid = game_of_life_step(grid)
        return (im,)

    ani = animation.FuncAnimation(fig, update, frames=steps, interval=interval_ms, blit=True)

    # Optional: GIF speichern (Pillow-Writer)
    if save_gif:
        try:
            fps = max(1, int(1000 / max(1, interval_ms)))
            ani.save(save_gif, writer='pillow', fps=fps)
            print(f"💾 GIF gespeichert: {save_gif}")
        except Exception as e:
            print(f"⚠️  Konnte GIF nicht speichern: {e}")
    if save_mp4:
        try:
            fps = max(1, int(1000 / max(1, interval_ms)))
            ani.save(save_mp4, writer='ffmpeg', fps=fps)
            print(f"💾 MP4 gespeichert: {save_mp4}")
        except Exception as e:
            print(f"⚠️  Konnte MP4 nicht speichern (ffmpeg installiert?): {e}")

    plt.show()

    if save_csv and stats:
        csv = np.array(stats, dtype=int)
        np.savetxt('gol_glider_evolution.csv', csv, delimiter=',', header='step,live_cells', fmt='%d')
        print("✅ CSV 'gol_glider_evolution.csv' gespeichert:")
        print(csv)


def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life – Glider Demo")
    parser.add_argument('--size', type=int, default=10, help='Gittergröße NxN (>= 5)')
    parser.add_argument('--steps', type=int, default=50, help='Anzahl der Schritte')
    parser.add_argument('--animate', dest='animate', action='store_true', help='Animation mit Matplotlib anzeigen')
    parser.add_argument('--no-animate', dest='animate', action='store_false', help='Nur textuelle Ausgabe (kein Plot)')
    parser.add_argument('--interval', type=int, default=150, help='Frame-Intervall in ms')
    parser.add_argument('--preset', type=str, default='glider', choices=['glider', 'blinker', 'toad', 'gosper', 'lwss', 'pulsar'], help='Startmuster')
    parser.add_argument('--save-gif', type=str, default=None, help='GIF-Datei speichern (erfordert Pillow)')
    parser.add_argument('--save-mp4', type=str, default=None, help='MP4 speichern (erfordert ffmpeg)')
    parser.add_argument('--no-csv', dest='save_csv', action='store_false', help='Kein CSV schreiben')
    parser.set_defaults(animate=True, save_csv=True)
    args = parser.parse_args()

    # Größe je nach Preset sinnvoll setzen (Gosper braucht großflächig)
    min_size = 5
    if args.preset == 'gosper':
        min_size = 40
    elif args.preset == 'pulsar':
        min_size = 20
    n = max(min_size, args.size)
    grid = np.zeros((n, n), dtype=int)

    # Startmuster platzieren
    if args.preset == 'glider':
        place_glider(grid, top=1, left=1)
    elif args.preset == 'blinker':
        place_blinker(grid, top=n//2, left=max(1, n//2 - 1))
    elif args.preset == 'toad':
        place_toad(grid, top=n//2 - 1, left=max(1, n//2 - 2))
    elif args.preset == 'gosper':
        place_gosper_glider_gun(grid, top=1, left=1)
    elif args.preset == 'lwss':
        place_lwss(grid, top=max(1, n//2 - 2), left=max(1, n//2 - 3))
    elif args.preset == 'pulsar':
        place_pulsar(grid, top=max(1, n//2 - 8), left=max(1, n//2 - 8))

    print("=== CONWAY'S GAME OF LIFE: GLIDER ===")
    print("Regeln: <2 Tod | 2-3 Überleben | >3 Tod | 3 Geburt\n")
    print(f"Initial Grid ({n}x{n}):")
    print(grid)
    print()

    if args.animate:
        if not HAS_MPL:
            print("⚠️  Matplotlib fehlt – starte Textmodus. Installiere mit: pip install matplotlib")
            _, stats = simulate(grid, steps=min(args.steps, 20))
        else:
            animate(grid, steps=args.steps, interval_ms=args.interval, save_csv=args.save_csv, save_gif=args.save_gif, save_mp4=args.save_mp4)
    else:
        _, stats = simulate(grid, steps=args.steps)
        if args.save_csv:
            np.savetxt('gol_glider_evolution.csv', stats, delimiter=',', header='step,live_cells', fmt='%d')
            print("✅ CSV 'gol_glider_evolution.csv' gespeichert")

    print("Hinweis: Für umfangreiche Muster siehe Gosper Glider Gun etc.")


if __name__ == '__main__':
    main()