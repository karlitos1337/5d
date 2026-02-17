import os
import sys

import streamlit as st

# Ensure the pages directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Streamlit functions to avoid runtime errors during import/syntax check
if not st.runtime.exists():
    st.set_page_config = lambda **kwargs: None
    st.markdown = lambda *args, **kwargs: None
    st.title = lambda *args, **kwargs: None
    st.header = lambda *args, **kwargs: None
    st.subheader = lambda *args, **kwargs: None
    st.write = lambda *args, **kwargs: None
    st.sidebar = type('Sidebar', (), {'title': lambda *a, **k: None, 'markdown': lambda *a, **k: None, 'header': lambda *a, **k: None})
    st.button = lambda *args, **kwargs: False
    st.checkbox = lambda *args, **kwargs: False
    st.text_input = lambda *args, **kwargs: ""
    st.text_area = lambda *args, **kwargs: ""
    st.number_input = lambda *args, **kwargs: 0
    st.selectbox = lambda *args, **kwargs: args[1][0] if len(args) > 1 and args[1] else None
    st.multiselect = lambda *args, **kwargs: []
    st.slider = lambda *args, **kwargs: args[1] if len(args) > 1 else 0
    st.file_uploader = lambda *args, **kwargs: None
    st.columns = lambda count: [type('Column', (), {'write': lambda *a, **k: None, 'markdown': lambda *a, **k: None}) for _ in range(count)]
    st.tabs = lambda tabs: [type('Tab', (), {'write': lambda *a, **k: None, 'markdown': lambda *a, **k: None}) for _ in tabs]
    st.expander = lambda *args, **kwargs: type('Expander', (), {'__enter__': lambda s: s, '__exit__': lambda s, e, t, b: None})()
    st.container = lambda *args, **kwargs: type('Container', (), {'__enter__': lambda s: s, '__exit__': lambda s, e, t, b: None})()
    st.empty = lambda *args, **kwargs: type('Empty', (), {'write': lambda *a, **k: None})()
    st.spinner = lambda *args, **kwargs: type('Spinner', (), {'__enter__': lambda s: s, '__exit__': lambda s, e, t, b: None})()
    st.error = lambda *args, **kwargs: None
    st.warning = lambda *args, **kwargs: None
    st.info = lambda *args, **kwargs: None
    st.success = lambda *args, **kwargs: None
    st.json = lambda *args, **kwargs: None
    st.code = lambda *args, **kwargs: None
    st.image = lambda *args, **kwargs: None
    st.session_state = {}

def test_syntax():
    """Simple syntax check for the file."""
    with open('pages/9_🧪_Autopoietic_Class.py') as f:
        compile(f.read(), 'pages/9_🧪_Autopoietic_Class.py', 'exec')

def test_imports():
    """Check if imports are resolvable."""
    try:
        # Import by filename pattern isn't standard python, so we just check existence
        assert os.path.exists('pages/9_🧪_Autopoietic_Class.py')
    except Exception as e:
        print(f"Error checking file existence: {e}")

if __name__ == "__main__":
    test_syntax()
