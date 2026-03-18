from typing import Any, List

import networkx as nx


class CognitiveGraph:
    """5D Core: Semantic Knowledge Graph (Hypothesis H1)"""

    def __init__(self):
        self.graph = nx.DiGraph()
        

    def add_concept(self, concept_id: str, metadata: dict[str, Any]) -> None:
        self.graph.add_node(concept_id, **metadata)

    def link_concepts(self, source_id: str, target_id: str, weight: float = 1.0) -> None:
        self.graph.add_edge(source_id, target_id, weight=weight)
        

    def calculate_serendipity_score(self, context_nodes: List[str]) -> float:
        if not context_nodes:
            return 0.0
        subgraph = self.graph.subgraph(context_nodes)
        if len(subgraph.nodes) < 2:
            return 0.0
        return nx.density(subgraph)

    def suggest_connections(self, concept_id: str, limit: int = 5) -> list[str]:
        if concept_id not in self.graph:
            return []
        return list(self.graph.neighbors(concept_id))[:limit]


def main():
    print("Initializing 5D Cognitive Graph...")
    kg = CognitiveGraph()
    kg.add_concept("Quantum", {"type": "physics"})
    kg.add_concept("Consciousness", {"type": "philosophy"})
    kg.link_concepts("Quantum", "Consciousness", weight=0.8)
    score = kg.calculate_serendipity_score(["Quantum", "Consciousness"])
    print(f"Serendipity Score: {score}")


if __name__ == "__main__":
    main()
