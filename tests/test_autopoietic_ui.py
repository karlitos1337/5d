# tests/test_autopoietic_ui.py
import os
import sys
from unittest.mock import patch

import pytest

# Ensure the pages directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Streamlit to avoid runtime errors
try:
    from pages.pages_9_Autopoietic_Class import AutopoieticClassABM  # noqa: F401
except ImportError:
    # If direct import fails (likely due to emojis in filename), we might need to mock or skip
    pass

@pytest.fixture
def mock_streamlit():
    """Mock Streamlit components."""
    with patch('streamlit.sidebar') as mock_sidebar:
        with patch('streamlit.columns') as mock_columns:
            yield mock_sidebar, mock_columns

def test_syntax():
    """Simple syntax check for the file."""
    with open('pages/9_🧪_Autopoietic_Class.py') as f:
        compile(f.read(), 'pages/9_🧪_Autopoietic_Class.py', 'exec')
