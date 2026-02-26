import sys
import os

# Add the project root to sys.path so that 'storage', 'auth', etc. can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
