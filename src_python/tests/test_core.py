from src_python.knowledge_graph.core import CognitiveGraph

def test_serendipity_calculation():
    # Setup
    graph = CognitiveGraph()
    graph.add_concept("c1", {"domain": "science"})
    graph.add_concept("c2", {"domain": "art"})
    graph.add_concept("c3", {"domain": "tech"})

    graph.link_concepts("c1", "c2", 0.5)

    # Execute
    score = graph.calculate_serendipity_score(["c1", "c3"])

    # Assert
    assert score >= 0.0
