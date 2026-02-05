"""
Topological Data Analysis: Persistent Homology
Reference: Carlsson 2009, DOI:10.1090/S0273-0979-09-01249-X
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class PersistenceInterval:
    """Represents a topological feature's birth-death interval.

    Attributes:
        birth: Scale at which feature appears
        death: Scale at which feature disappears
        dimension: Topological dimension (0=component, 1=loop, 2=void)
    """

    birth: float
    death: float
    dimension: int

    @property
    def persistence(self) -> float:
        """How long the feature persists."""
        return self.death - self.birth


class SimpleTDA:
    """Minimal TDA implementation for educational purposes.

    Note: For production use, see libraries like:
    - Ripser (https://ripser.scikit-tda.org/)
    - Gudhi (https://gudhi.inria.fr/)
    - giotto-tda (https://giotto-ai.github.io/gtda-docs/)
    """

    def __init__(self, points: np.ndarray):
        """Initialize with point cloud.

        Args:
            points: Array of shape (n_points, n_dimensions)
        """
        self.points = points
        self.distance_matrix = self._compute_distances()

    def _compute_distances(self) -> np.ndarray:
        """Compute pairwise Euclidean distances."""
        n = len(self.points)
        distances = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(self.points[i] - self.points[j])
                distances[i, j] = dist
                distances[j, i] = dist

        return distances

    def compute_persistent_homology_0d(self, max_scale: float = 2.0) -> list[PersistenceInterval]:
        """Compute 0-dimensional persistence (connected components).

        Simplified version using Union-Find algorithm.

        Args:
            max_scale: Maximum radius to consider

        Returns:
            List of persistence intervals for connected components
        """
        n = len(self.points)

        # Union-Find data structure
        parent = list(range(n))
        birth_time = [0.0] * n  # All components born at t=0

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y, time):
            root_x, root_y = find(x), find(y)
            if root_x != root_y:
                # Merge younger into older
                if birth_time[root_x] < birth_time[root_y]:
                    parent[root_y] = root_x
                    return root_y, time  # root_y dies
                else:
                    parent[root_x] = root_y
                    return root_x, time  # root_x dies
            return None, None

        # Sort edges by distance
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                edges.append((self.distance_matrix[i, j], i, j))
        edges.sort()

        intervals = []

        for dist, i, j in edges:
            if dist > max_scale:
                break

            died_component, death_time = union(i, j, dist)
            if died_component is not None:
                intervals.append(PersistenceInterval(birth=birth_time[died_component], death=death_time, dimension=0))

        # Add infinite interval for final component
        final_root = find(0)
        intervals.append(PersistenceInterval(birth=birth_time[final_root], death=np.inf, dimension=0))

        return intervals


# Example Usage
if __name__ == "__main__":
    print("🔍 Topological Data Analysis Demo")
    print("=" * 50)

    # Generate sample data: 3 clusters
    np.random.seed(42)
    cluster1 = np.random.randn(10, 2) * 0.3 + np.array([0, 0])
    cluster2 = np.random.randn(10, 2) * 0.3 + np.array([3, 0])
    cluster3 = np.random.randn(10, 2) * 0.3 + np.array([1.5, 2.5])

    points = np.vstack([cluster1, cluster2, cluster3])

    print(f"\n📈 Data: {len(points)} points in {points.shape[1]}D")

    # Compute persistent homology
    tda = SimpleTDA(points)
    intervals = tda.compute_persistent_homology_0d(max_scale=5.0)

    print("\n🧲 Persistence Intervals (Dimension 0):")
    print(f"{'Birth':>8} {'Death':>8} {'Persistence':>12}")
    print("-" * 32)

    for interval in sorted(intervals, key=lambda x: x.persistence, reverse=True)[:5]:
        death_str = "Inf" if np.isinf(interval.death) else f"{interval.death:.3f}"
        pers_str = "Inf" if np.isinf(interval.persistence) else f"{interval.persistence:.3f}"
        print(f"{interval.birth:8.3f} {death_str:>8} {pers_str:>12}")

    # Interpretation
    finite_intervals = [i for i in intervals if not np.isinf(i.death)]
    significant = [i for i in finite_intervals if i.persistence > 0.5]

    print("\n🔎 Interpretation:")
    print(f"  Total components: {len(intervals)}")
    print(f"  Significant features (pers > 0.5): {len(significant)}")
    print(f"  → Data has ~{len(significant) + 1} robust clusters")

    print("\n📚 Reference: Carlsson 2009, Topology and Data")
    print("   DOI: 10.1090/S0273-0979-09-01249-X")
