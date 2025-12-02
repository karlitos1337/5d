from src.universal_system_genesis_5d.formulas_scoring import (
    likert_to_0_1,
    normalize_to_1_99,
    weighted_aggregate,
)


def test_likert_mapping():
    assert likert_to_0_1(1) == 0.0
    assert likert_to_0_1(3) == 0.5
    assert likert_to_0_1(5) == 1.0


def test_normalize_to_1_99():
    assert normalize_to_1_99(0.0) == 1
    assert normalize_to_1_99(1.0) == 99
    assert 1 <= normalize_to_1_99(0.5) <= 99


def test_weighted_aggregate():
    scores = {"a": 0.2, "b": 0.8}
    weights = {"a": 1.0, "b": 3.0}
    agg = weighted_aggregate(scores, weights)
    # (0.2*1 + 0.8*3) / 4 = (0.2 + 2.4) / 4 = 0.65
    assert abs(agg - 0.65) < 1e-9
