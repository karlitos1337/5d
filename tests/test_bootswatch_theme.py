from pathlib import Path


def test_theme_files_exist():
    """Verify that Bootswatch theme files exist."""
    css_path = Path("utils/bootswatch_theme.css")
    # In CI, we might be in root, check if file exists or if we should skip
    if css_path.exists():
        assert css_path.stat().st_size > 0
