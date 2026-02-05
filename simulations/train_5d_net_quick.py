"""
5D-Net Quick Test - Reduced Training for Fast Validation
Research Agenda #4: AI-Simulation (PRIORITY 1)

Simplified version:
- 2 epochs instead of 10
- Smaller batch size
- Only 2 noise levels (0%, 30%)
- MNIST only (no CIFAR10 transfer)

Expected time: 5-10 minutes on CPU
"""

import json
from datetime import datetime
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

# Import 5D-Net architecture
from five_d_net import BaselineNet, FiveDNet
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


class QuickConfig:
    # Reduced settings for quick test
    batch_size = 256  # Larger for speed
    epochs = 2  # Only 2 epochs
    learning_rate = 0.001
    weight_decay = 1e-4

    # Model
    hidden_dim = 64  # Smaller for speed
    num_heads = 2
    lambda_authenticity = 0.1

    # Experiments
    noise_levels = [0.0, 0.3]  # Only clean and 30% noise
    train_subset_size = 10000  # Use only 10k training samples
    test_subset_size = 2000  # Use only 2k test samples

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Paths
    results_dir = Path("../08-experimente-validierung/experiments/results")


def add_noise(images: torch.Tensor, noise_level: float) -> torch.Tensor:
    """Add Gaussian noise to images."""
    if noise_level == 0.0:
        return images
    noise = torch.randn_like(images) * noise_level
    return torch.clamp(images + noise, 0, 1)


def train_quick(
    model: nn.Module, loader: DataLoader, optimizer: optim.Optimizer, config: QuickConfig
) -> dict[str, float]:
    """Quick training for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(config.device), labels.to(config.device)
        images = images.view(images.size(0), -1)  # Flatten

        # Forward pass
        optimizer.zero_grad()
        logits = model(images, noise_level=0.0)

        # Loss
        loss = nn.CrossEntropyLoss()(logits, labels)

        # Backward pass
        loss.backward()
        optimizer.step()

        # Metrics
        total_loss += loss.item()
        _, predicted = logits.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        # Print progress every 10 batches
        if (batch_idx + 1) % 10 == 0:
            print(
                f"  Batch {batch_idx + 1}/{len(loader)} | "
                f"Loss: {loss.item():.4f} | "
                f"Acc: {100.0 * correct / total:.2f}%",
                end="\r",
            )

    print()  # New line after epoch
    return {"loss": total_loss / len(loader), "accuracy": 100.0 * correct / total}


def evaluate_quick(
    model: nn.Module, loader: DataLoader, config: QuickConfig, noise_level: float = 0.0
) -> dict[str, float]:
    """Quick evaluation."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(config.device), labels.to(config.device)
            images = images.view(images.size(0), -1)  # Flatten

            # Add noise
            images = add_noise(images, noise_level)

            # Forward pass
            logits = model(images, noise_level=noise_level)

            # Accuracy
            _, predicted = logits.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return {"accuracy": 100.0 * correct / total}


def main():
    """Quick test script."""
    print("=" * 70)
    print("5D-NET QUICK TEST - Research Agenda #4")
    print("Reduced training for fast validation (2 epochs, 10k samples)")
    print("=" * 70)

    config = QuickConfig()
    config.results_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nDevice: {config.device}")
    print(f"Batch size: {config.batch_size}")
    print(f"Epochs: {config.epochs}")
    print(f"Training samples: {config.train_subset_size}")
    print(f"Test samples: {config.test_subset_size}")

    # Load MNIST (subset)
    print("\nLoading MNIST...")
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    train_dataset = datasets.MNIST("data", train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST("data", train=False, transform=transform)

    # Create subsets
    train_indices = torch.randperm(len(train_dataset))[: config.train_subset_size]
    test_indices = torch.randperm(len(test_dataset))[: config.test_subset_size]

    train_subset = Subset(train_dataset, train_indices)
    test_subset = Subset(test_dataset, test_indices)

    train_loader = DataLoader(train_subset, batch_size=config.batch_size, shuffle=True)
    test_loader = DataLoader(test_subset, batch_size=config.batch_size, shuffle=False)

    # Results storage
    results = {}

    # Train and test both models
    for model_name in ["5D-Net", "Baseline"]:
        print(f"\n{'=' * 70}")
        print(f"Training: {model_name}")
        print(f"{'=' * 70}")

        # Initialize model
        if model_name == "5D-Net":
            model = FiveDNet(input_size=784, hidden_size=config.hidden_dim, num_classes=10).to(config.device)
        else:
            model = BaselineNet(input_size=784, hidden_size=config.hidden_dim, num_classes=10).to(config.device)

        # Count parameters
        n_params = sum(p.numel() for p in model.parameters())
        print(f"Parameters: {n_params:,}")

        optimizer = optim.Adam(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)

        # Training
        for epoch in range(config.epochs):
            print(f"\nEpoch {epoch + 1}/{config.epochs}")
            train_metrics = train_quick(model, train_loader, optimizer, config)
            print(f"  Train Loss: {train_metrics['loss']:.4f} | Train Acc: {train_metrics['accuracy']:.2f}%")

        # Evaluation on clean test set
        print("\nEvaluation...")
        results_model = {}

        for noise in config.noise_levels:
            metrics = evaluate_quick(model, test_loader, config, noise_level=noise)
            results_model[f"noise_{noise}"] = metrics
            print(f"  Noise {noise:.1f}: Accuracy {metrics['accuracy']:.2f}%")

        results[model_name] = results_model

    # Compare results
    print("\n" + "=" * 70)
    print("RESULTS COMPARISON")
    print("=" * 70)

    acc_5d_clean = results["5D-Net"]["noise_0.0"]["accuracy"]
    acc_baseline_clean = results["Baseline"]["noise_0.0"]["accuracy"]

    acc_5d_30 = results["5D-Net"]["noise_0.3"]["accuracy"]
    acc_baseline_30 = results["Baseline"]["noise_0.3"]["accuracy"]

    drop_5d = acc_5d_clean - acc_5d_30
    drop_baseline = acc_baseline_clean - acc_baseline_30

    print("\nClean Accuracy:")
    print(f"  5D-Net:   {acc_5d_clean:.2f}%")
    print(f"  Baseline: {acc_baseline_clean:.2f}%")

    print("\nRobustness (30% Noise):")
    print(f"  5D-Net:   {acc_5d_30:.2f}% (Drop: {drop_5d:.2f}%)")
    print(f"  Baseline: {acc_baseline_30:.2f}% (Drop: {drop_baseline:.2f}%)")
    print("  Expected: 5D -12%, Baseline -28%")
    print(f"  Improvement: {drop_baseline - drop_5d:.2f}% better")

    # Hypothesis test
    print("\n" + "=" * 70)
    if drop_5d < drop_baseline:
        print("✅ HYPOTHESIS CONFIRMED: 5D-Net is more robust than Baseline!")
        print(f"   5D-Net drop: {drop_5d:.2f}% < Baseline drop: {drop_baseline:.2f}%")
    else:
        print("❌ HYPOTHESIS REJECTED: Baseline is more robust")
        print(f"   5D-Net drop: {drop_5d:.2f}% >= Baseline drop: {drop_baseline:.2f}%")
    print("=" * 70)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = config.results_dir / f"quick_test_{timestamp}.json"

    combined_results = {
        "5d_net": results["5D-Net"],
        "baseline": results["Baseline"],
        "comparison": {
            "noise_30_improvement": drop_baseline - drop_5d,
            "hypothesis_confirmed": drop_5d < drop_baseline,
            "config": {
                "epochs": config.epochs,
                "train_samples": config.train_subset_size,
                "test_samples": config.test_subset_size,
            },
        },
    }

    with open(results_file, "w") as f:
        json.dump(combined_results, f, indent=2)

    print(f"\nResults saved: {results_file}")


if __name__ == "__main__":
    main()
