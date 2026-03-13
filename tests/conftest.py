import sys
from pathlib import Path

# Add the project root directory to sys.path
# This ensures that packages like 'storage', 'models', 'auth' are discoverable
# regardless of where pytest is run from.
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
