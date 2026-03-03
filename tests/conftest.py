import sys
import os
from pathlib import Path

# Add the project root to the python path to allow importing top-level packages (like storage, models)
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
