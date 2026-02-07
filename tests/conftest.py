import sys
from pathlib import Path

# Add project root to sys.path to allow importing modules like 'storage'
# from tests that are not run with PYTHONPATH set.
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
