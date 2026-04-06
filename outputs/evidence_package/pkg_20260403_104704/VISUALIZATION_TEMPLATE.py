
import matplotlib.pyplot as plt
import numpy as np

def plot_radar_chart(scores, title="5D Profile"):
    labels = list(scores.keys())
    values = list(scores.values())

    # Number of variables
    N = len(labels)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += [angles[0]]

    values += [values[0]]

    ax = plt.subplot(111, polar=True)

    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], labels)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([1,2,3,4,5], ["1","2","3","4","5"], color="grey", size=7)
    plt.ylim(0,5)

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.title(title)
    plt.show()

if __name__ == "__main__":
    # Example Data (canonical 5D dimension names)
    data = {
        "A (Autonomie)": 4.2,
        "IM (Intrinsische Motivation)": 3.8,
        "R (Resilienz)": 4.5,
        "SP (Sympoietische Partizipation)": 3.2,
        "Au (Authentizität)": 4.0
    }
    plot_radar_chart(data)
