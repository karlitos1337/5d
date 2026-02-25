import sys
from pathlib import Path

# Add project root to sys.path to allow imports of top-level packages like 'storage'
# This is necessary when running tests from the project root or from within the tests directory
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
