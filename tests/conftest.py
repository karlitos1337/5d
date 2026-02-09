import sys
from pathlib import Path

# Add project root to sys.path so tests can import from top-level packages
# like storage, models, auth, etc.
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
