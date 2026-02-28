import sys
import os
from pathlib import Path

# Insert the project root into sys.path to ensure modules like storage, models are discoverable
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
