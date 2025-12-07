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


def test_theme_config_centralized():
    """Test that theme configuration is centralized in THEME_CONFIG object"""
    html = read_html()
    assert 'THEME_CONFIG' in html, 'THEME_CONFIG object not found - configuration should be centralized'
    # Verify the config object contains expected properties
    assert 'THEME_CONFIG.bootswatchVersion' in html or 'bootswatchVersion:' in html, \
        'bootswatchVersion not in THEME_CONFIG'
    assert 'THEME_CONFIG.defaultTheme' in html or 'defaultTheme:' in html, \
        'defaultTheme not in THEME_CONFIG'
    assert 'THEME_CONFIG.allowedThemes' in html or 'allowedThemes:' in html, \
        'allowedThemes not in THEME_CONFIG'


def test_url_building_function_exists():
    """Test that there's a dedicated URL building function for safety"""
    html = read_html()
    assert 'buildThemeUrl' in html, 'buildThemeUrl function not found - URL construction should be centralized'
    assert 'function buildThemeUrl' in html, 'buildThemeUrl should be a function'


def test_sanitization_present():
    """Test that theme name sanitization is implemented"""
    html = read_html()
    # Look for sanitization logic - checking for patterns that indicate input validation
    assert 'replace' in html and ('[^a-z0-9\\-]' in html or '[^a-z0-9-]' in html), \
        'Theme name sanitization (alphanumeric + hyphen filter) not found'


def test_encoding_present():
    """Test that URI encoding is used for safety"""
    html = read_html()
    assert 'encodeURIComponent' in html, 'encodeURIComponent not found - URL components should be encoded'


def test_error_handling_present():
    """Test that error handling for CSS loading failures is implemented"""
    html = read_html()
    assert 'onerror' in html, 'onerror handler not found - should handle CSS load failures'
    assert 'onload' in html, 'onload handler not found - should verify successful CSS loading'
