import sys
import os
from pathlib import Path

# Add project root to sys.path to allow importing top-level modules like 'storage', 'models', 'utils'
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
