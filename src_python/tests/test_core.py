from src_python.knowledge_graph.core import CognitiveGraph


def test_serendipity_calculation():
    kg = CognitiveGraph()
    kg.add_concept("A", {})
    kg.add_concept("B", {})
    kg.add_relationship("A", "B")
    score = kg.calculate_serendipity_score(["A", "B"])
    assert score > 0, "Connected thoughts should have positive serendipity"

def test_empty_graph():
    kg = CognitiveGraph()
    score = kg.calculate_serendipity_score([])
    assert score == 0.0, "Empty context should yield zero serendipity"
