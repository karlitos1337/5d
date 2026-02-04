import math

from src.universal_system_genesis_5d.formulas_math import (
    dot,
    min_max_normalize,
    sigmoid,
    softmax,
    weighted_mean,
)


def test_sigmoid_bounds():
    assert 0.0 < sigmoid(0.0) < 1.0
    assert math.isclose(sigmoid(0), 0.5, rel_tol=1e-9)


def test_softmax_distribution():
    v = softmax([1.0, 2.0, 3.0])
    assert len(v) == 3
    assert math.isclose(sum(v), 1.0, rel_tol=1e-9)


def test_min_max_normalize():
    assert min_max_normalize(5, 0, 10) == 0.5
    assert min_max_normalize(-1, 0, 10) == 0.0
    assert min_max_normalize(11, 0, 10) == 1.0


def test_dot_and_weighted_mean():
    assert dot([1, 2, 3], [4, 5, 6]) == 32
    assert math.isclose(
        weighted_mean([1, 2, 3], [1, 1, 2]), (1 * 1 + 2 * 1 + 3 * 2) / 4
    )
