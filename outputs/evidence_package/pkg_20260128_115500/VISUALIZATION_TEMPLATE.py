import matplotlib.pyplot as plt
import numpy as np

def plot_radar_chart(categories, values, title):
    """
    Plots a radar chart for the given 5D categories and values.
    """
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    values += values[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories)
    ax.plot(angles, values)
    ax.fill(angles, values, 'b', alpha=0.1)
    plt.title(title)
    plt.show()
