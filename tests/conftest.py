import sys
from pathlib import Path

# Add project root to sys.path so modules like storage, models, auth can be imported
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
