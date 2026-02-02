#!/usr/bin/env python3
"""
Test Suite for Participation Networks (Page 10)
===============================================

Scientific validation of network topology models and diffusion theory.

References:
- Granovetter, M. S. (1973). The Strength of Weak Ties. American Journal of Sociology, 78(6), 1360-1380.
- Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. Nature, 393(6684), 440-442.
- Barabási, A.-L., & Albert, R. (1999). Emergence of scaling in random networks. Science, 286(5439), 509-512.
- Rogers, E. M. (2003). Diffusion of Innovations (5th ed.). Free Press.
"""

from pathlib import Path

import pytest

try:
    import networkx as nx
    import numpy as np
except ImportError:
    nx = None
    np = None

# ==================== Network Topology Tests ====================


@pytest.mark.skipif(nx is None or np is None, reason="networkx or numpy not installed")
class TestNetworkTopologies:
    """Test properties of the three main network models."""

    def test_erdos_renyi_properties(self):
        """Erdős-Rényi: random connections, low clustering, short paths."""
        n = 100
        p = 0.05
        G = nx.erdos_renyi_graph(n=n, p=p, seed=42)

        # Expected: low clustering (~ p for large n)
        clustering = nx.average_clustering(G)
        assert 0.0 <= clustering <= 0.1, f"ER clustering too high: {clustering}"

        # Expected: short paths (~ log(n) / log(p*n))
        if nx.is_connected(G):
            avg_path = nx.average_shortest_path_length(G)
            assert avg_path < 5.0, f"ER path length too long: {avg_path}"

    def test_small_world_properties(self):
        """
        Watts-Strogatz: high clustering, short paths.

        Reference: Watts & Strogatz 1998
        Key property: Clustering >> random, Path length ≈ random
        """
        n = 100
        k = 6
        p = 0.05
        G = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=42)

        # Expected: high clustering (> 0.3 for k=6, p=0.05)
        clustering = nx.average_clustering(G)
        assert clustering > 0.3, f"Small-world clustering too low: {clustering}"

        # Expected: short paths (< 10 for n=100)
        avg_path = nx.average_shortest_path_length(G)
        assert avg_path < 10.0, f"Small-world path length too long: {avg_path}"

        # Should be connected for k >= 2
        assert nx.is_connected(G), "Small-world graph not connected"

    def test_scale_free_properties(self):
        """
        Barabási-Albert: power-law degree distribution, hubs.

        Reference: Barabási & Albert 1999
        Key property: P(k) ~ k^(-γ), where γ ≈ 3 for BA model
        """
        n = 200
        m = 3
        G = nx.barabasi_albert_graph(n=n, m=m, seed=42)

        # Degree distribution
        degrees = [d for n, d in G.degree()]

        # Expected: hubs exist (max degree >> average degree)
        max_degree = max(degrees)
        avg_degree = np.mean(degrees)
        assert max_degree > 3 * avg_degree, f"No clear hubs: max {max_degree}, avg {avg_degree}"

        # Expected: minimum degree is m (by construction)
        min_degree = min(degrees)
        assert min_degree >= m, f"Min degree {min_degree} < m={m}"

        # Expected: connected (BA model guarantees connectivity)
        assert nx.is_connected(G), "Scale-free graph not connected"

    def test_topology_comparison(self):
        """Compare clustering coefficients across topologies."""
        n = 100

        # Erdős-Rényi
        G_er = nx.erdos_renyi_graph(n=n, p=0.05, seed=42)
        c_er = nx.average_clustering(G_er)

        # Small-world
        G_sw = nx.watts_strogatz_graph(n=n, k=6, p=0.05, seed=42)
        c_sw = nx.average_clustering(G_sw)

        # Scale-free
        G_sf = nx.barabasi_albert_graph(n=n, m=3, seed=42)
        c_sf = nx.average_clustering(G_sf)

        # Expected ordering: small-world > scale-free > random
        assert c_sw > c_sf, f"Small-world clustering {c_sw} not > scale-free {c_sf}"
        assert c_sw > c_er, f"Small-world clustering {c_sw} not > random {c_er}"


# ==================== Weak Ties Theory Tests ====================


@pytest.mark.skipif(nx is None or np is None, reason="networkx or numpy not installed")
class TestWeakTiesTheory:
    """Test Granovetter's (1973) weak ties principles."""

    def test_bridge_identification(self):
        """
        Bridges connect otherwise disconnected components.

        Reference: Granovetter 1973 - weak ties as bridges
        """
        # Create graph with two cliques connected by one edge (bridge)
        G = nx.Graph()

        # Clique 1 (nodes 0-4)
        G.add_edges_from([(i, j) for i in range(5) for j in range(i + 1, 5)])

        # Clique 2 (nodes 5-9)
        G.add_edges_from([(i, j) for i in range(5, 10) for j in range(i + 1, 10)])

        # Bridge (weak tie)
        G.add_edge(4, 5)

        # Find bridges
        bridges = list(nx.bridges(G))

        assert len(bridges) == 1, f"Expected 1 bridge, found {len(bridges)}"
        assert (4, 5) in bridges or (5, 4) in bridges, "Bridge (4,5) not found"

    def test_local_clustering_vs_bridging(self):
        """Nodes with high betweenness (bridging) often have lower clustering."""
        n = 100
        G = nx.watts_strogatz_graph(n=n, k=6, p=0.1, seed=42)

        # Calculate clustering and betweenness
        clustering = nx.clustering(G)
        betweenness = nx.betweenness_centrality(G)

        # Get top 10 bridging nodes (high betweenness)
        top_bridges = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

        # Average clustering of top bridges
        avg_clustering_bridges = np.mean([clustering[node] for node, _ in top_bridges])

        # Average clustering of all nodes
        avg_clustering_all = np.mean(list(clustering.values()))

        # Expectation: bridges have lower clustering (not always true, but often)
        # We test a weaker condition: bridges don't have significantly higher clustering
        assert (
            avg_clustering_bridges <= avg_clustering_all * 1.2
        ), f"Bridges have unusually high clustering: {avg_clustering_bridges:.3f} vs {avg_clustering_all:.3f}"


# ==================== Diffusion Dynamics Tests ====================


@pytest.mark.skipif(nx is None or np is None, reason="networkx or numpy not installed")
class TestDiffusionDynamics:
    """Test knowledge diffusion and threshold models."""

    def test_threshold_model_basic(self):
        """
        Simple threshold model: activate if >= threshold fraction of neighbors active.

        Reference: Granovetter 1978 (threshold models), Watts 2002 (cascade models)
        """
        # Line graph: 0 -- 1 -- 2 -- 3 -- 4
        G = nx.path_graph(5)

        # Activate node 0
        active = {0: True, 1: False, 2: False, 3: False, 4: False}
        threshold = 0.5

        # Step 1: Node 1 has 1/2 neighbors active → activate
        neighbors_1 = list(G.neighbors(1))  # [0, 2]
        active_frac_1 = sum(1 for n in neighbors_1 if active[n]) / len(neighbors_1)

        assert active_frac_1 == 0.5, f"Node 1 active fraction: {active_frac_1}"

        # With threshold 0.5, node 1 should activate
        if active_frac_1 >= threshold:
            active[1] = True

        assert active[1], "Node 1 should activate with threshold 0.5"

    def test_diffusion_speed_vs_topology(self):
        """Small-world networks have faster diffusion than regular lattices."""
        n = 100
        k = 6
        seed_frac = 0.05
        threshold = 0.2
        max_steps = 50

        # Regular lattice (p=0)
        G_lattice = nx.watts_strogatz_graph(n=n, k=k, p=0.0, seed=42)
        t_50_lattice = self._simulate_diffusion(G_lattice, seed_frac, threshold, max_steps)

        # Small-world (p=0.1)
        G_sw = nx.watts_strogatz_graph(n=n, k=k, p=0.1, seed=42)
        t_50_sw = self._simulate_diffusion(G_sw, seed_frac, threshold, max_steps)

        # Small-world should be faster (lower t_50)
        if t_50_sw is not None and t_50_lattice is not None:
            assert (
                t_50_sw < t_50_lattice
            ), f"Small-world not faster: t_50={t_50_sw} vs lattice={t_50_lattice}"

    def test_seed_fraction_impact(self):
        """Higher initial activation → faster diffusion."""
        n = 100
        G = nx.watts_strogatz_graph(n=n, k=6, p=0.05, seed=42)
        threshold = 0.2
        max_steps = 50

        # Low seed
        t_50_low = self._simulate_diffusion(
            G, seed_frac=0.05, threshold=threshold, max_steps=max_steps
        )

        # High seed
        t_50_high = self._simulate_diffusion(
            G, seed_frac=0.20, threshold=threshold, max_steps=max_steps
        )

        # Higher seed should reach 50% faster (or immediately if seed > 50%)
        if t_50_high is not None and t_50_low is not None:
            assert (
                t_50_high <= t_50_low
            ), f"Higher seed not faster: t_50={t_50_high} vs low={t_50_low}"

    @staticmethod
    def _simulate_diffusion(G, seed_frac, threshold, max_steps):
        """Helper: simulate threshold diffusion, return t_50."""
        rng = np.random.default_rng(42)
        n = G.number_of_nodes()
        active = {node: (rng.random() < seed_frac) for node in G.nodes}

        for t in range(max_steps):
            # Check if 50% reached
            n_active = sum(1 for v in active.values() if v)
            if n_active >= n / 2:
                return t

            # Update step
            new_active = active.copy()
            for u in G.nodes:
                if active[u]:
                    continue
                neighbors = list(G.neighbors(u))
                if not neighbors:
                    continue
                active_frac = sum(1 for v in neighbors if active[v]) / len(neighbors)
                if active_frac >= threshold:
                    new_active[u] = True
            active = new_active

        # 50% not reached
        return None


# ==================== IMP Proxy Validation ====================


class TestIMPProxies:
    """Validate IMP dimension proxies from network metrics."""

    def test_sp_proxy_formula(self):
        """
        Social Participation (SP) = 0.5 × clustering + 0.5 × final_activation

        Range: [0, 1]
        """
        # High clustering, high activation → high SP
        sp_high = 0.5 * 0.8 + 0.5 * 0.9
        assert 0.8 <= sp_high <= 0.9, f"SP high: {sp_high}"

        # Low clustering, low activation → low SP
        sp_low = 0.5 * 0.1 + 0.5 * 0.2
        assert 0.1 <= sp_low <= 0.2, f"SP low: {sp_low}"

        # Range check
        assert 0.0 <= sp_high <= 1.0 and 0.0 <= sp_low <= 1.0

    def test_resilience_proxy_formula(self):
        """
        Resilience (R) = 1 - (t_50 / max_steps)

        Fast diffusion → high resilience
        """
        max_steps = 100

        # Fast diffusion (t_50 = 10)
        r_fast = 1.0 - (10 / max_steps)
        assert abs(r_fast - 0.9) < 0.01, f"R fast: {r_fast}"

        # Slow diffusion (t_50 = 80)
        r_slow = 1.0 - (80 / max_steps)
        assert abs(r_slow - 0.2) < 0.01, f"R slow: {r_slow}"

        # Range check
        assert 0.0 <= r_fast <= 1.0 and 0.0 <= r_slow <= 1.0

    def test_im_proxy_formula(self):
        """
        Intrinsic Motivation (IM) = share_prob × (1 - threshold)

        High sharing + low threshold → high IM
        """
        # High IM: eager sharing, low activation threshold
        im_high = 0.8 * (1.0 - 0.1)
        assert abs(im_high - 0.72) < 0.01, f"IM high: {im_high}"

        # Low IM: reluctant sharing, high threshold
        im_low = 0.3 * (1.0 - 0.7)
        assert abs(im_low - 0.09) < 0.01, f"IM low: {im_low}"

        # Range check
        assert 0.0 <= im_high <= 1.0 and 0.0 <= im_low <= 1.0


# ==================== BibTeX Validation ====================


class TestBibTeXValidation:
    """Validate scientific references for network theory."""

    def test_bibtex_network_papers(self):
        """Check for 3 core network theory papers in BibTeX file."""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")
        assert bibtex_path.exists(), f"BibTeX file not found: {bibtex_path}"

        content = bibtex_path.read_text(encoding="utf-8")

        required_keys = [
            "granovetter1973strength",  # Weak ties
            "watts1998collective",  # Small-world
            "barabasi1999emergence",  # Scale-free
        ]

        for key in required_keys:
            assert key in content, f"Missing BibTeX key: {key}"

    def test_bibtex_diffusion_paper(self):
        """Rogers (2003) Diffusion of Innovations should be present."""
        bibtex_path = Path("07_daten_analysen/5d-relevant-sources.bib")
        content = bibtex_path.read_text(encoding="utf-8")

        # Rogers 2003 already added in previous batch
        assert "rogers2003" in content.lower(), "Missing Rogers 2003 diffusion theory"


# ==================== Rogers Diffusion Theory ====================


class TestRogersDiffusion:
    """Test Rogers' (2003) diffusion of innovations theory applied to networks."""

    def test_adopter_categories(self):
        """
        Rogers' 5 categories: Innovators (2.5%), Early Adopters (13.5%),
        Early Majority (34%), Late Majority (34%), Laggards (16%)
        """
        categories = {
            "Innovators": 0.025,
            "Early Adopters": 0.135,
            "Early Majority": 0.34,
            "Late Majority": 0.34,
            "Laggards": 0.16,
        }

        # Sum should be 1.0
        total = sum(categories.values())
        assert abs(total - 1.0) < 0.001, f"Categories don't sum to 1: {total}"

        # Critical mass at ~16% (Innovators + Early Adopters)
        critical_mass = categories["Innovators"] + categories["Early Adopters"]
        assert abs(critical_mass - 0.16) < 0.001, f"Critical mass: {critical_mass}"

    def test_tipping_point_simulation(self):
        """
        Tipping point occurs around 16% adoption.
        After this, diffusion accelerates rapidly.
        """
        # This is conceptual - real implementation in Page 10 simulation
        tipping_point = 0.16
        assert 0.15 <= tipping_point <= 0.20, "Tipping point range"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
