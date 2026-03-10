import pytest
import os

def test_xss_protection_in_dashboard():
    dashboard_file = "web/templates/5d_forschungsplanung.html"
    assert os.path.exists(dashboard_file)
    with open(dashboard_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "DOMPurify.sanitize" in content, "Dashboard should sanitize external inputs using DOMPurify to prevent XSS"
    assert "purify.min.js" in content, "DOMPurify script should be included in the dashboard"
    assert "aiResponse.innerHTML = DOMPurify.sanitize(marked.parse(text));" in content, "Markdown parsing must be wrapped in DOMPurify.sanitize"
