"""
This module provides a CognitiveGraph class for managing knowledge graphs.
"""

from typing import Any

import networkx as nx


class CognitiveGraph:
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
        return nx.density(subgraph)

    def suggest_connections(self, concept_id: str, limit: int = 5) -> list[str]:
        if concept_id not in self.graph:
            return []

        # Simple suggestion logic based on neighbors of neighbors
        suggestions = []
        for neighbor in self.graph.neighbors(concept_id):
            for nn in self.graph.neighbors(neighbor):
                if nn != concept_id and not self.graph.has_edge(concept_id, nn):
                    suggestions.append(nn)

        return suggestions[:limit]
