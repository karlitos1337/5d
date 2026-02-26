import sys
import os
from pathlib import Path

# Add the project root to sys.path so that 'storage', 'models', etc. can be imported
# when running tests from the 'tests/' directory.
# This mimics the behavior of running python -m pytest from the root.
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
