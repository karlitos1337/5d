from typing import Any

import networkx as nx


class CognitiveGraph:
    """
    A graph-based representation of knowledge/concepts (Concepts, Dimensions) and their relationships.
    Uses NetworkX for graph operations.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_concept(self, concept_id: str, metadata: dict[str, Any]) -> None:
        self.graph.add_node(concept_id, **metadata)

    def link_concepts(self, source_id: str, target_id: str, weight: float = 1.0) -> None:
        self.graph.add_edge(source_id, target_id, weight=weight)

    def calculate_serendipity_score(self, context_nodes: list[str]) -> float:
        if not context_nodes:
            return 0.0

        subgraph = self.graph.subgraph(context_nodes)
        # Simplified serendipity metric: Inverse of density (sparser graphs might imply more "surprising" connections if connected)
        # Or maybe average shortest path length?
        # For now, let's use 1 - density.
        if len(subgraph.nodes) < 2:
            return 0.0
        return 1.0 - nx.density(subgraph)

    def suggest_connections(self, concept_id: str, limit: int = 5) -> list[str]:
        if concept_id not in self.graph:
            return []

        # Suggest neighbors of neighbors (Jaccard coefficient or Adamic/Adar)
        # Using built-in adamic_adar_index for undirected view (approximation)
        undirected_view = self.graph.to_undirected()
        preds = nx.adamic_adar_index(
            undirected_view,
            [
                (concept_id, n)
                for n in self.graph.nodes
                if n != concept_id and not self.graph.has_edge(concept_id, n)
            ],
        )

        sorted_preds = sorted(preds, key=lambda x: x[2], reverse=True)
        return [p[1] for p in sorted_preds[:limit]]
