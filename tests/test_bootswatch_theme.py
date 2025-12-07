import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HTML_PATH = BASE / 'external' / 'sources' / 'awesome-piracy-main' / 'index.html'


def read_html():
    assert HTML_PATH.exists(), f"expected {HTML_PATH} to exist"
    return HTML_PATH.read_text(encoding='utf-8')


def test_link_id_present():
    html = read_html()
    assert 'id="bootswatch-css"' in html, 'bootswatch link id bootswatch-css not found in index.html'


def test_whitelist_present():
    html = read_html()
    # ensure the allowedThemes identifier exists
    assert 'allowedThemes' in html, 'allowedThemes identifier not found in index.html'
    # check for explicit names to make sure whitelist contains at least these
    for theme in ('darkly', 'united', 'flatly', 'quartz'):
        assert theme in html, f"expected theme '{theme}' to be present in whitelist in index.html"


def test_bootswatch_variables_present():
    html = read_html()
    # simple presence checks for the variables used by the changeCSS implementation
    assert 'bootswatchVersion' in html, 'bootswatchVersion reference not found in index.html'
    assert 'defaultTheme' in html, 'defaultTheme reference not found in index.html'


def test_semver_validation_present():
    """Test that semver validation regex is present in the code."""
    html = read_html()
    # Check for the semver validation pattern
    assert r'/^[0-9]+\.[0-9]+\.[0-9]+' in html, 'semver validation pattern not found in index.html'
    assert 'versionSafe' in html, 'versionSafe variable not found in index.html'


def test_encode_uri_component_usage():
    """Test that encodeURIComponent is used for URL construction."""
    html = read_html()
    assert 'encodeURIComponent' in html, 'encodeURIComponent not found in index.html'
    # Should appear at least twice (for version and theme)
    count = html.count('encodeURIComponent')
    assert count >= 2, f'encodeURIComponent should appear at least 2 times, found {count}'


def test_preload_mechanism():
    """Test that preload mechanism is implemented."""
    html = read_html()
    assert "rel = 'preload'" in html, "preload mechanism not found in index.html"
    assert "as = 'style'" in html, "preload 'as' attribute not set in index.html"
    assert 'onload' in html, 'onload handler not found in index.html'


def test_cross_origin_set():
    """Test that crossOrigin attribute is set for SRI support."""
    html = read_html()
    assert 'crossOrigin' in html, 'crossOrigin not set in index.html'
    assert "'anonymous'" in html or '"anonymous"' in html, 'anonymous crossOrigin value not found'


def test_error_handler_present():
    """Test that onerror handler with fallback is present."""
    html = read_html()
    assert 'onerror' in html, 'onerror handler not found in index.html'
    assert 'console.error' in html, 'console.error for failed loads not found in index.html'
    assert 'fallbackHref' in html or 'fallback' in html.lower(), 'fallback mechanism not found in index.html'


def test_theme_safe_variable():
    """Test that themeSafe variable is used for validation."""
    html = read_html()
    assert 'themeSafe' in html, 'themeSafe variable not found in index.html'
    assert 'fallbackTheme' in html, 'fallbackTheme variable not found in index.html'
