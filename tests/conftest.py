import sys
from pathlib import Path

# Add the project root to sys.path so that 'storage', 'models', etc. can be imported
root_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root_dir))
