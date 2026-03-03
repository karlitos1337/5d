import sys
from pathlib import Path

# Add project root to sys.path to allow discovery of top-level packages
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
