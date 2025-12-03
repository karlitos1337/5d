"""
5D-Net: Neural Network Architecture Based on 5D Intelligence Framework
========================================================================

Master-Hypothese: 5D-Systeme > 1D-Kontroll in Stabilität, Transfer, Glück, Innovation

Research Agenda #4: AI-Simulation (PRIORITY 1)
Timeline: 1 Woche (03-09 Dec 2025)
Expected: -12% Accuracy-Drop (vs. Baseline -28%)

Scientific Basis:
- D1 (Instinct): Polyvagal Theory (Porges 2011) - HRV-Simulation
- D2 (Self-Regulation): SDT Autonomy (Deci & Ryan 1985) - AutonomyGate
- D3 (System Intelligence): Theory of Mind + Interoception - MultiPerspectiveAttention
- D4 (Collaborative Intelligence): Emergence (Holland 1998) - EmergentNetwork
- 5 Components: A × IM × R × SP × Au (multiplicative, testable)

Tasks:
1. MNIST mit Noise (0-30%) - Robustness Test
2. Transfer CIFAR10 - Generalization Test
3. FGSM-Attack - Adversarial Robustness Test

Metrics:
- Accuracy-Drop (lower = better)
- Transfer-Accuracy (higher = better)
- Adversarial Success Rate (lower = better)

Author: Karlitos1337 | 5D Research Lab
Date: 2025-12-03
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional
import numpy as np


# ============================================================================
# D1: INSTINCT LAYER (Polyvagal-Simulation)
# ============================================================================

class InstinctLayer(nn.Module):
    """
    D1: Reptiliengehirn / Polyvagal Safety Detection
    
    Scientific Basis: Porges (2011) - Ventral Vagal → Safety → Learning
    Implementation: Self-normalizing with adaptive noise tolerance
    """
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.fc = nn.Linear(in_features, out_features)
        self.bn = nn.BatchNorm1d(out_features)
        # Polyvagal "Safety" parameter (learnable threshold)
        self.safety_threshold = nn.Parameter(torch.tensor(0.5))
        
    def forward(self, x: torch.Tensor, noise_level: float = 0.0) -> torch.Tensor:
        """
        Forward pass with noise tolerance (simulates stress response)
        
        Args:
            x: Input tensor [batch, features]
            noise_level: Gaussian noise std (0.0 = safe, 0.3 = stress)
            
        Returns:
            Normalized output with safety gating
        """
        x = self.fc(x)
        x = self.bn(x)
        
        # Safety gating: suppress activation under high noise (dorsal vagal)
        safety_gate = torch.sigmoid(self.safety_threshold - noise_level)
        x = F.selu(x) * safety_gate  # SELU for self-normalization
        
        return x


# ============================================================================
# D2: AUTONOMY GATE (Self-Determination Theory)
# ============================================================================

class AutonomyGate(nn.Module):
    """
    D2: Self-Regulation / Autonomy
    
    Scientific Basis: Deci & Ryan (1985) - Autonomy → Intrinsic Motivation
    Implementation: Attention mechanism that learns to select relevant features
    """
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.fc = nn.Linear(in_features, out_features)
        # Autonomy = learned attention weights (what to focus on)
        self.attention = nn.Linear(in_features, out_features)
        self.bn = nn.BatchNorm1d(out_features)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with autonomy-based feature selection
        
        Args:
            x: Input tensor [batch, features]
            
        Returns:
            Gated output (autonomy-weighted features)
        """
        # Main pathway
        out = self.fc(x)
        
        # Autonomy pathway (attention weights)
        attention_weights = torch.sigmoid(self.attention(x))
        
        # Gate: only pass autonomously selected features
        out = out * attention_weights
        out = self.bn(out)
        out = F.relu(out)
        
        return out
    
    def autonomy_score(self) -> float:
        """
        Calculate autonomy score (diversity of attention weights)
        
        Returns:
            Entropy of attention weights (higher = more autonomous)
        """
        with torch.no_grad():
            weights = torch.sigmoid(self.attention.weight).mean(dim=0)
            # Shannon entropy
            weights = weights / weights.sum()
            entropy = -(weights * torch.log(weights + 1e-8)).sum()
            return entropy.item()


# ============================================================================
# D3: MULTI-PERSPECTIVE ATTENTION (Theory of Mind)
# ============================================================================

class MultiPerspectiveAttention(nn.Module):
    """
    D3: System Intelligence / Theory of Mind
    
    Scientific Basis: Premack & Woodruff (1978) - Multiple perspectives
    Implementation: Multi-head attention with perspective diversity
    """
    def __init__(self, in_features: int, out_features: int, num_perspectives: int = 4):
        super().__init__()
        self.num_perspectives = num_perspectives
        
        # Multiple "perspectives" (attention heads)
        self.perspectives = nn.ModuleList([
            nn.Linear(in_features, out_features // num_perspectives)
            for _ in range(num_perspectives)
        ])
        
        # Integration layer (combine perspectives)
        self.integration = nn.Linear(out_features, out_features)
        self.bn = nn.BatchNorm1d(out_features)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with multi-perspective integration
        
        Args:
            x: Input tensor [batch, features]
            
        Returns:
            Integrated multi-perspective output
        """
        # Get all perspectives
        perspectives = [F.relu(p(x)) for p in self.perspectives]
        
        # Concatenate perspectives
        combined = torch.cat(perspectives, dim=1)
        
        # Integrate perspectives
        out = self.integration(combined)
        out = self.bn(out)
        out = F.relu(out)
        
        return out


# ============================================================================
# D4: EMERGENT NETWORK (Collaborative Intelligence)
# ============================================================================

class EmergentNetwork(nn.Module):
    """
    D4: Collaborative Intelligence / Emergence
    
    Scientific Basis: Holland (1998) - Emergence through interaction
    Implementation: Residual connections + lateral inhibition (self-organizing)
    """
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.fc1 = nn.Linear(in_features, in_features)
        self.fc2 = nn.Linear(in_features, out_features)
        
        # Lateral inhibition (competition between units)
        self.inhibition = nn.Parameter(torch.ones(out_features) * 0.1)
        
        self.bn = nn.BatchNorm1d(out_features)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with emergent self-organization
        
        Args:
            x: Input tensor [batch, features]
            
        Returns:
            Emergent output with lateral inhibition
        """
        # Residual pathway (preserve input)
        identity = x
        
        # Main pathway
        out = F.relu(self.fc1(x))
        out = self.fc2(out)
        
        # Lateral inhibition (winner-take-all-like)
        out = out * torch.sigmoid(-self.inhibition.abs())
        
        out = self.bn(out)
        
        # Residual connection (if dimensions match)
        if identity.shape[1] == out.shape[1]:
            out = out + identity
            
        out = F.relu(out)
        
        return out


# ============================================================================
# 5D-NET: FULL ARCHITECTURE
# ============================================================================

class FiveDNet(nn.Module):
    """
    5D-Net: Full Architecture
    
    Layers:
    - D1: InstinctLayer (Polyvagal Safety)
    - D2: AutonomyGate (Self-Determination)
    - D3: MultiPerspectiveAttention (Theory of Mind)
    - D4: EmergentNetwork (Collaborative Intelligence)
    - Output: Classification head
    
    5 Components (multiplicative):
    - Autonomy: Attention diversity
    - Intrinsic Motivation: Activation strength
    - Resilience: Noise tolerance
    - Social Participation: Perspective diversity
    - Authenticity: Alignment between layers
    """
    def __init__(self, input_size: int = 784, num_classes: int = 10, hidden_size: int = 128):
        super().__init__()
        
        # D1: Instinct (Polyvagal)
        self.d1_instinct = InstinctLayer(input_size, hidden_size)
        
        # D2: Autonomy (Self-Regulation)
        self.d2_autonomy = AutonomyGate(hidden_size, hidden_size)
        
        # D3: System Intelligence (Theory of Mind)
        self.d3_system = MultiPerspectiveAttention(hidden_size, hidden_size, num_perspectives=4)
        
        # D4: Collaborative Intelligence (Emergence)
        self.d4_collab = EmergentNetwork(hidden_size, hidden_size)
        
        # Output layer
        self.fc_out = nn.Linear(hidden_size, num_classes)
        
    def forward(self, x: torch.Tensor, noise_level: float = 0.0) -> torch.Tensor:
        """
        Forward pass through all 5D layers
        
        Args:
            x: Input tensor [batch, 1, 28, 28] (MNIST) or [batch, 3, 32, 32] (CIFAR10)
            noise_level: Gaussian noise std (0.0 = clean, 0.3 = high noise)
            
        Returns:
            Logits [batch, num_classes]
        """
        # Flatten if needed
        if len(x.shape) == 4:
            x = x.view(x.size(0), -1)
        
        # D1: Instinct (with noise tolerance)
        x = self.d1_instinct(x, noise_level=noise_level)
        
        # D2: Autonomy
        x = self.d2_autonomy(x)
        
        # D3: System Intelligence
        x = self.d3_system(x)
        
        # D4: Collaborative Intelligence
        x = self.d4_collab(x)
        
        # Output
        x = self.fc_out(x)
        
        return x
    
    def stability_score(self) -> float:
        """
        Calculate 5D stability score (multiplicative components)
        
        5 Components:
        - Autonomy: Attention diversity (entropy)
        - Intrinsic Motivation: Activation strength (mean abs activation)
        - Resilience: Noise tolerance (safety threshold)
        - Social Participation: Perspective diversity (not directly measurable)
        - Authenticity: Alignment between layers (gradient similarity)
        
        Returns:
            Stability score (0-1, higher = more stable)
        """
        with torch.no_grad():
            # Autonomy
            autonomy = self.d2_autonomy.autonomy_score() / 10.0  # Normalize entropy
            
            # Intrinsic Motivation (proxy: activation strength in D3)
            intrinsic_motivation = 0.5  # Placeholder (would need activation tracking)
            
            # Resilience (proxy: safety threshold in D1)
            resilience = torch.sigmoid(self.d1_instinct.safety_threshold).item()
            
            # Social Participation (proxy: num perspectives)
            social_participation = 0.75  # 4 perspectives / 5.33 (max)
            
            # Authenticity (proxy: alignment, would need gradient analysis)
            authenticity = 0.6  # Placeholder
            
            # Multiplicative (weak-link logic)
            stability = autonomy * intrinsic_motivation * resilience * social_participation * authenticity
            
            return stability


# ============================================================================
# BASELINE NETWORK (Standard CNN)
# ============================================================================

class BaselineNet(nn.Module):
    """
    Baseline Network: Standard CNN for comparison
    
    Architecture: Conv → Conv → FC → FC
    No special 5D mechanisms, just standard layers
    """
    def __init__(self, input_size: int = 784, num_classes: int = 10, hidden_size: int = 128):
        super().__init__()
        
        # Standard layers
        self.fc1 = nn.Linear(input_size, hidden_size * 2)
        self.fc2 = nn.Linear(hidden_size * 2, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc_out = nn.Linear(hidden_size, num_classes)
        
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x: torch.Tensor, noise_level: float = 0.0) -> torch.Tensor:
        """
        Forward pass (standard architecture)
        
        Args:
            x: Input tensor
            noise_level: Ignored (baseline has no noise mechanism)
            
        Returns:
            Logits
        """
        # Flatten if needed
        if len(x.shape) == 4:
            x = x.view(x.size(0), -1)
        
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = F.relu(self.fc3(x))
        x = self.fc_out(x)
        
        return x


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def count_parameters(model: nn.Module) -> int:
    """Count trainable parameters in model"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def add_noise(x: torch.Tensor, noise_level: float) -> torch.Tensor:
    """Add Gaussian noise to input"""
    if noise_level == 0.0:
        return x
    noise = torch.randn_like(x) * noise_level
    return x + noise


def fgsm_attack(model: nn.Module, x: torch.Tensor, y: torch.Tensor, epsilon: float = 0.3) -> torch.Tensor:
    """
    FGSM (Fast Gradient Sign Method) adversarial attack
    
    Args:
        model: Neural network
        x: Input images
        y: True labels
        epsilon: Attack strength
        
    Returns:
        Adversarial examples
    """
    x.requires_grad = True
    
    # Forward pass
    logits = model(x)
    loss = F.cross_entropy(logits, y)
    
    # Backward pass (get gradient)
    model.zero_grad()
    loss.backward()
    
    # Create adversarial example
    x_adv = x + epsilon * x.grad.sign()
    x_adv = torch.clamp(x_adv, 0, 1)  # Keep in valid range
    
    return x_adv.detach()


if __name__ == "__main__":
    # Quick test
    print("5D-Net Architecture Test")
    print("=" * 60)
    
    # Create models
    five_d = FiveDNet(input_size=784, num_classes=10, hidden_size=128)
    baseline = BaselineNet(input_size=784, num_classes=10, hidden_size=128)
    
    print(f"5D-Net parameters: {count_parameters(five_d):,}")
    print(f"Baseline parameters: {count_parameters(baseline):,}")
    
    # Test forward pass
    x = torch.randn(4, 784)  # Batch of 4 MNIST images
    
    print("\nTesting 5D-Net:")
    y_5d = five_d(x, noise_level=0.1)
    print(f"Output shape: {y_5d.shape}")
    print(f"Stability score: {five_d.stability_score():.4f}")
    
    print("\nTesting Baseline:")
    y_baseline = baseline(x)
    print(f"Output shape: {y_baseline.shape}")
    
    print("\n✅ Architecture test passed!")
