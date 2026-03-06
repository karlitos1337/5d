import sys
from pathlib import Path

# Add the project root (one level up from tests/) to sys.path
# This ensures that top-level packages like 'storage', 'models', 'auth', and 'utils'
# can be resolved correctly when running 'pytest tests' without PYTHONPATH=.
root_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root_dir))
