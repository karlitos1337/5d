# Simulation Data

Large datasets (e.g., MNIST) are not stored in Git.

## MNIST Setup
```python
from torchvision import datasets
datasets.MNIST('./MNIST', download=True)
```
