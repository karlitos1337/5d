import sys
import os

# Add the project root to sys.path so that tests can import from top-level packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
