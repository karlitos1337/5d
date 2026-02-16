"""
5D-Net Training & Evaluation Script
====================================

Research Agenda #4: AI-Simulation (PRIORITY 1)
Timeline: 1 Woche (03-09 Dec 2025)

Tasks:
1. MNIST mit Noise (0-30%) - Robustness Test
2. Transfer CIFAR10 - Generalization Test
3. FGSM-Attack - Adversarial Robustness Test

Expected Results:
- 5D-Net: -12% Accuracy-Drop (robust)
- Baseline: -28% Accuracy-Drop (fragile)

Author: Karlitos1337 | 5D Research Lab
Date: 2025-12-03
"""

import json
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from five_d_net import BaselineNet, FiveDNet, add_noise, count_parameters, fgsm_attack
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "dataset": "MNIST",
    "batch_size": 128,
    "epochs": 10,
    "learning_rate": 0.001,
    "hidden_size": 128,
    "device": "cuda" if torch.cuda.is_available() else "cpu",
    "noise_levels": [0.0, 0.1, 0.2, 0.3],  # Robustness test
    "fgsm_epsilon": 0.3,  # Adversarial attack strength
    "results_dir": "simulations/results",
}


# ============================================================================
# DATA LOADING
# ============================================================================


def get_mnist_loaders(batch_size: int = 128) -> tuple[DataLoader, DataLoader]:
    """Load MNIST train and test datasets"""
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    return train_loader, test_loader


def get_cifar10_loader(batch_size: int = 128) -> DataLoader:
    """Load CIFAR10 test dataset (for transfer test)"""
    transform = transforms.Compose(
        [
            transforms.Grayscale(),  # Convert to grayscale (like MNIST)
            transforms.Resize(28),  # Resize to MNIST size
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,)),
        ]
    )

    test_dataset = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)

    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    return test_loader


# ============================================================================
# TRAINING
# ============================================================================


def train_epoch(
    model: nn.Module,
    train_loader: DataLoader,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    device: str,
) -> float:
    """Train for one epoch"""
    model.train()
    total_loss = 0.0

    for _batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # Forward pass
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(train_loader)


def evaluate(
    model: nn.Module, test_loader: DataLoader, device: str, noise_level: float = 0.0
) -> tuple[float, float]:
    """Evaluate model accuracy"""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)

            # Add noise if specified
            if noise_level > 0:
                data = add_noise(data, noise_level)

            # Forward pass
            output = model(data, noise_level=noise_level)
            pred = output.argmax(dim=1)

            correct += (pred == target).sum().item()
            total += target.size(0)

    accuracy = 100.0 * correct / total
    return accuracy, total


def evaluate_adversarial(
    model: nn.Module, test_loader: DataLoader, device: str, epsilon: float = 0.3
) -> tuple[float, float]:
    """Evaluate model on adversarial examples (FGSM attack)"""
    model.eval()
    correct = 0
    total = 0

    for data, target in test_loader:
        data, target = data.to(device), target.to(device)

        # Generate adversarial examples
        data_adv = fgsm_attack(model, data, target, epsilon=epsilon)

        # Evaluate on adversarial examples
        with torch.no_grad():
            output = model(data_adv)
            pred = output.argmax(dim=1)

            correct += (pred == target).sum().item()
            total += target.size(0)

    accuracy = 100.0 * correct / total
    return accuracy, total


# ============================================================================
# EXPERIMENT RUNNER
# ============================================================================


def run_experiment(config: dict) -> dict:
    """
    Run full experiment:
    1. Train 5D-Net and Baseline on MNIST
    2. Test robustness with noise (0%, 10%, 20%, 30%)
    3. Test transfer to CIFAR10
    4. Test adversarial robustness (FGSM)
    """
    device = config["device"]
    print(f"Using device: {device}")
    print("=" * 80)

    # Load data
    print("\nLoading datasets...")
    train_loader, test_loader = get_mnist_loaders(config["batch_size"])
    cifar_loader = get_cifar10_loader(config["batch_size"])

    # Create models
    print("\nInitializing models...")
    five_d = FiveDNet(input_size=784, num_classes=10, hidden_size=config["hidden_size"]).to(device)

    baseline = BaselineNet(input_size=784, num_classes=10, hidden_size=config["hidden_size"]).to(
        device
    )

    print(f"5D-Net parameters: {count_parameters(five_d):,}")
    print(f"Baseline parameters: {count_parameters(baseline):,}")
    print(f"5D-Net stability: {five_d.stability_score():.4f}")

    # Training setup
    criterion = nn.CrossEntropyLoss()
    optimizer_5d = optim.Adam(five_d.parameters(), lr=config["learning_rate"])
    optimizer_baseline = optim.Adam(baseline.parameters(), lr=config["learning_rate"])

    results = {"config": config, "5d_net": {}, "baseline": {}, "comparison": {}}

    # ========================================================================
    # TASK 1: TRAIN ON MNIST
    # ========================================================================

    print("\n" + "=" * 80)
    print("TASK 1: Training on MNIST")
    print("=" * 80)

    for epoch in range(config["epochs"]):
        print(f"\nEpoch {epoch+1}/{config['epochs']}")

        # Train 5D-Net
        loss_5d = train_epoch(five_d, train_loader, optimizer_5d, criterion, device)
        acc_5d, _ = evaluate(five_d, test_loader, device)

        # Train Baseline
        loss_baseline = train_epoch(baseline, train_loader, optimizer_baseline, criterion, device)
        acc_baseline, _ = evaluate(baseline, test_loader, device)

        print(f"5D-Net    - Loss: {loss_5d:.4f}, Accuracy: {acc_5d:.2f}%")
        print(f"Baseline  - Loss: {loss_baseline:.4f}, Accuracy: {acc_baseline:.2f}%")

    # Final clean accuracy
    clean_acc_5d, _ = evaluate(five_d, test_loader, device)
    clean_acc_baseline, _ = evaluate(baseline, test_loader, device)

    results["5d_net"]["clean_accuracy"] = clean_acc_5d
    results["baseline"]["clean_accuracy"] = clean_acc_baseline

    print("\nFinal Clean Accuracy:")
    print(f"5D-Net:   {clean_acc_5d:.2f}%")
    print(f"Baseline: {clean_acc_baseline:.2f}%")

    # ========================================================================
    # TASK 2: ROBUSTNESS TEST (NOISE)
    # ========================================================================

    print("\n" + "=" * 80)
    print("TASK 2: Robustness Test (Gaussian Noise)")
    print("=" * 80)

    noise_results_5d = {}
    noise_results_baseline = {}

    for noise_level in config["noise_levels"]:
        print(f"\nNoise level: {noise_level*100:.0f}%")

        # Test 5D-Net
        acc_5d, _ = evaluate(five_d, test_loader, device, noise_level=noise_level)
        drop_5d = clean_acc_5d - acc_5d

        # Test Baseline
        acc_baseline, _ = evaluate(baseline, test_loader, device, noise_level=noise_level)
        drop_baseline = clean_acc_baseline - acc_baseline

        print(f"5D-Net:   {acc_5d:.2f}% (drop: {drop_5d:.2f}%)")
        print(f"Baseline: {acc_baseline:.2f}% (drop: {drop_baseline:.2f}%)")

        noise_results_5d[f"noise_{int(noise_level*100)}"] = {
            "accuracy": acc_5d,
            "drop": drop_5d,
        }
        noise_results_baseline[f"noise_{int(noise_level*100)}"] = {
            "accuracy": acc_baseline,
            "drop": drop_baseline,
        }

    results["5d_net"]["noise"] = noise_results_5d
    results["baseline"]["noise"] = noise_results_baseline

    # Average drop
    avg_drop_5d = np.mean([r["drop"] for r in noise_results_5d.values()])
    avg_drop_baseline = np.mean([r["drop"] for r in noise_results_baseline.values()])

    print("\nAverage Accuracy Drop:")
    print(f"5D-Net:   {avg_drop_5d:.2f}%")
    print(f"Baseline: {avg_drop_baseline:.2f}%")
    print(f"5D-Net Advantage: {avg_drop_baseline - avg_drop_5d:.2f}% less drop")

    results["comparison"]["avg_noise_drop_5d"] = avg_drop_5d
    results["comparison"]["avg_noise_drop_baseline"] = avg_drop_baseline
    results["comparison"]["noise_advantage"] = avg_drop_baseline - avg_drop_5d

    # ========================================================================
    # TASK 3: TRANSFER TEST (CIFAR10)
    # ========================================================================

    print("\n" + "=" * 80)
    print("TASK 3: Transfer Test (CIFAR10)")
    print("=" * 80)

    transfer_acc_5d, _ = evaluate(five_d, cifar_loader, device)
    transfer_acc_baseline, _ = evaluate(baseline, cifar_loader, device)

    print("\nTransfer Accuracy (MNIST → CIFAR10):")
    print(f"5D-Net:   {transfer_acc_5d:.2f}%")
    print(f"Baseline: {transfer_acc_baseline:.2f}%")
    print(f"5D-Net Advantage: {transfer_acc_5d - transfer_acc_baseline:.2f}%")

    results["5d_net"]["transfer_accuracy"] = transfer_acc_5d
    results["baseline"]["transfer_accuracy"] = transfer_acc_baseline
    results["comparison"]["transfer_advantage"] = transfer_acc_5d - transfer_acc_baseline

    # ========================================================================
    # TASK 4: ADVERSARIAL TEST (FGSM)
    # ========================================================================

    print("\n" + "=" * 80)
    print("TASK 4: Adversarial Robustness (FGSM Attack)")
    print("=" * 80)

    adv_acc_5d, _ = evaluate_adversarial(
        five_d, test_loader, device, epsilon=config["fgsm_epsilon"]
    )
    adv_acc_baseline, _ = evaluate_adversarial(
        baseline, test_loader, device, epsilon=config["fgsm_epsilon"]
    )

    adv_drop_5d = clean_acc_5d - adv_acc_5d
    adv_drop_baseline = clean_acc_baseline - adv_acc_baseline

    print(f"\nAdversarial Accuracy (ε={config['fgsm_epsilon']}):")
    print(f"5D-Net:   {adv_acc_5d:.2f}% (drop: {adv_drop_5d:.2f}%)")
    print(f"Baseline: {adv_acc_baseline:.2f}% (drop: {adv_drop_baseline:.2f}%)")
    print(f"5D-Net Advantage: {adv_drop_baseline - adv_drop_5d:.2f}% less drop")

    results["5d_net"]["adversarial_accuracy"] = adv_acc_5d
    results["5d_net"]["adversarial_drop"] = adv_drop_5d
    results["baseline"]["adversarial_accuracy"] = adv_acc_baseline
    results["baseline"]["adversarial_drop"] = adv_drop_baseline
    results["comparison"]["adversarial_advantage"] = adv_drop_baseline - adv_drop_5d

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print("\n" + "=" * 80)
    print("EXPERIMENT SUMMARY")
    print("=" * 80)

    print("\n1. Clean Accuracy:")
    print(f"   5D-Net:   {clean_acc_5d:.2f}%")
    print(f"   Baseline: {clean_acc_baseline:.2f}%")

    print("\n2. Robustness (Avg Noise Drop):")
    print(f"   5D-Net:   {avg_drop_5d:.2f}%")
    print(f"   Baseline: {avg_drop_baseline:.2f}%")
    print("   ✅ Expected: 5D < Baseline (5D more robust)")

    print("\n3. Transfer (MNIST → CIFAR10):")
    print(f"   5D-Net:   {transfer_acc_5d:.2f}%")
    print(f"   Baseline: {transfer_acc_baseline:.2f}%")

    print("\n4. Adversarial (FGSM Drop):")
    print(f"   5D-Net:   {adv_drop_5d:.2f}%")
    print(f"   Baseline: {adv_drop_baseline:.2f}%")

    # Hypothesis test
    hypothesis_confirmed = avg_drop_5d < avg_drop_baseline

    print("\n" + "=" * 80)
    print("HYPOTHESIS TEST:")
    print("H₁: 5D-Net < Baseline in Accuracy Drop")
    print(f"Result: {'✅ CONFIRMED' if hypothesis_confirmed else '❌ REJECTED'}")
    print(f"5D-Net: {avg_drop_5d:.2f}% vs Baseline: {avg_drop_baseline:.2f}%")
    print("=" * 80)

    results["comparison"]["hypothesis_confirmed"] = hypothesis_confirmed

    return results


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Run full experiment and save results"""
    print("\n" + "=" * 80)
    print("5D-NET EXPERIMENT - Research Agenda #4")
    print("Master-Hypothese: 5D > 1D in Stabilität, Transfer, Glück, Innovation")
    print("=" * 80)

    # Run experiment
    start_time = time.time()
    results = run_experiment(CONFIG)
    elapsed_time = time.time() - start_time

    results["elapsed_time_seconds"] = elapsed_time
    results["elapsed_time_human"] = f"{elapsed_time//60:.0f}m {elapsed_time%60:.0f}s"

    # Save results
    results_dir = Path(CONFIG["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)

    results_file = results_dir / "5d_net_experiment_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved to: {results_file}")
    print(f"⏱️  Total time: {results['elapsed_time_human']}")

    print("\n🎉 Experiment complete!")
    print("\nNext steps:")
    print("1. Commit results to Git")
    print("2. Create visualization plots")
    print("3. Write paper draft (arXiv)")


if __name__ == "__main__":
    main()
