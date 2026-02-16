"""
Mathematical Formulas for the Universal System Genesis 5D.
Provides standard functions like Sigmoid, Tanh, and derivatives.
"""

import math


def sigmoid(x: float) -> float:
    r"""Standard-Sigmoid $\sigma(x)=1/(1+e^{-x})$.
    Used for activation and probability normalization.
    """
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0

def sigmoid_derivative(x: float) -> float:
    """Derivative of the sigmoid function: sigma(x) * (1 - sigma(x))."""
    s = sigmoid(x)
    return s * (1 - s)

def tanh(x: float) -> float:
    """Hyperbolic tangent: (e^x - e^-x) / (e^x + e^-x).
    Output range: [-1, 1].
    """
    return math.tanh(x)

def relu(x: float) -> float:
    """Rectified Linear Unit: max(0, x)."""
    return max(0.0, x)
