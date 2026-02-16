
import pytest
from src.universal_system_genesis_5d.formulas_math import (
    relu,
    sigmoid,
    sigmoid_derivative,
    tanh,
)

def test_sigmoid():
    # Test values
    assert sigmoid(0) == pytest.approx(0.5)
    # Check limits
    assert sigmoid(100) == pytest.approx(1.0)
    assert sigmoid(-100) == pytest.approx(0.0)

def test_sigmoid_derivative():
    # d/dx sigma(x) = sigma(x)(1-sigma(x))
    # at x=0, sigma(0)=0.5, deriv=0.5*0.5=0.25
    assert sigmoid_derivative(0) == pytest.approx(0.25)

def test_tanh():
    assert tanh(0) == 0.0
    assert tanh(100) == pytest.approx(1.0)
    assert tanh(-100) == pytest.approx(-1.0)

def test_relu():
    assert relu(5) == 5
    assert relu(-5) == 0
    assert relu(0) == 0
