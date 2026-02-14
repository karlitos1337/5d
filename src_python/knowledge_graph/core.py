from typing import Any

import networkx as nx


class CognitiveGraph:
    """
    Manages the 5D cognitive graph structure using NetworkX.
    Nodes represent 5D concepts, edges represent relationships.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_concept(self, concept_id: str, metadata: dict[str, Any]) -> None:
        self.graph.add_node(concept_id, **metadata)

    def add_relationship(self, source_id: str, target_id: str, weight: float = 1.0) -> None:
        self.graph.add_edge(source_id, target_id, weight=weight)

    def calculate_serendipity_score(self, context_nodes: list[str]) -> float:
        if not context_nodes:
            return 0.0

        subgraph = self.graph.subgraph(context_nodes)
        if len(subgraph) < 2:
            return 0.0

        return nx.density(subgraph)

    def suggest_connections(self, concept_id: str, limit: int = 5) -> list[str]:
        if concept_id not in self.graph:
            return []

        # Basic suggestion: neighbors of neighbors (simple recommendation)
        suggestions = []
        for neighbor in self.graph.neighbors(concept_id):
            for second_neighbor in self.graph.neighbors(neighbor):
                if second_neighbor != concept_id and second_neighbor not in self.graph[concept_id]:
                    suggestions.append(second_neighbor)

        return list(set(suggestions))[:limit]
