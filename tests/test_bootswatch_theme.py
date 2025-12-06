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
    # ensure the allowedThemes identifier exists and at least the expected theme names are present
    assert 'allowedThemes' in html or "new Set(['darkly'" in html or 'new Set([' in html, 'allowedThemes Set not found in index.html'
    # check for explicit names to make sure whitelist contains at least these
    for theme in ('darkly', 'united', 'flatly', 'quartz'):
        assert theme in html, f"expected theme '{theme}' to be present in whitelist in index.html"


def test_bootswatch_variables_present():
    html = read_html()
    # simple presence checks for the variables used by the changeCSS implementation
    assert 'bootswatchVersion' in html, 'bootswatchVersion reference not found in index.html'
    assert 'defaultTheme' in html, 'defaultTheme reference not found in index.html'
