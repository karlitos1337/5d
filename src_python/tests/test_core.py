import pytest

try:
    from src_python.knowledge_graph.core import CognitiveGraph
except ImportError:
    CognitiveGraph = None

@pytest.mark.skipif(CognitiveGraph is None, reason="networkx not installed")
def test_serendipity_calculation():
    try:
        kg = CognitiveGraph()
    except ImportError:
        pytest.skip("networkx not installed")
    kg.add_concept("A", {})
    kg.add_concept("B", {})
    kg.link_concepts("A", "B")
    score = kg.calculate_serendipity_score(["A", "B"])
    assert score > 0, "Connected thoughts should have positive serendipity"

@pytest.mark.skipif(CognitiveGraph is None, reason="networkx not installed")
def test_empty_graph():
    try:
        kg = CognitiveGraph()
    except ImportError:
        pytest.skip("networkx not installed")
    score = kg.calculate_serendipity_score([])
    assert score == 0.0, "Empty context should yield zero serendipity"
