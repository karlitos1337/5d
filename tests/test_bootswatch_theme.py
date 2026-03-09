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
    """Test that theme name sanitization is implemented with correct pattern and flags"""
    html = read_html()
    # Look for sanitization logic - checking for the complete implementation
    assert 'replace' in html, 'replace method not found for sanitization'
    # Check for the regex pattern with proper character class
    assert '[^a-z0-9\\-]' in html or '[^a-z0-9-]' in html, \
        'Theme name sanitization regex pattern not found'
    # Verify the pattern has global and case-insensitive flags
    # Pattern should be: /[^a-z0-9\-]/gi with the flags immediately after the closing /
    assert '/gi,' in html or '/gi;' in html or '/gi ' in html, \
        'Sanitization regex must have "gi" flags for global case-insensitive matching'
    # Verify sanitization is applied before URL construction (sanitizedTheme variable)
    assert 'sanitizedTheme' in html, \
        'sanitizedTheme variable not found - sanitization must be applied before URL construction'


def test_encoding_present():
    """Test that URI encoding is used for safety"""
    html = read_html()
    assert 'encodeURIComponent' in html, 'encodeURIComponent not found - URL components should be encoded'


def test_error_handling_present():
    """Test that error handling for CSS loading failures is implemented"""
    html = read_html()
    assert 'onerror' in html, 'onerror handler not found - should handle CSS load failures'
    assert 'onload' in html, 'onload handler not found - should verify successful CSS loading'


def test_version_validation():
    """Test that bootswatchVersion is validated with semver pattern"""
    html = read_html()
    assert 'safeVersion' in html, 'safeVersion function not found - version validation required'
    assert 'safeFallbackVersion' in html, 'safeFallbackVersion not in config - need pinned safe version'
    # Check for semver-like regex pattern
    assert 'semverPattern' in html or 'semver' in html.lower(), \
        'semver validation pattern not found'


def test_preload_pattern():
    """Test that preload -> stylesheet swap pattern is used to reduce FOUC"""
    html = read_html()
    assert "rel = 'preload'" in html or 'rel = "preload"' in html, \
        'preload pattern not found - should use preload for FOUC reduction'
    assert "as = 'style'" in html or 'as = "style"' in html, \
        'as="style" attribute not found - required for preload pattern'


def test_crossorigin_attribute():
    """Test that crossOrigin attribute is set for future SRI support"""
    html = read_html()
    assert 'crossOrigin' in html, 'crossOrigin attribute not found - needed for future SRI support'
    assert "'anonymous'" in html or '"anonymous"' in html, \
        'crossOrigin="anonymous" value not found'
