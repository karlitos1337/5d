import yaml
from pathlib import Path


def load_config(config_path: str = 'config/default.yaml'):
    """Lädt YAML-Konfiguration für den 5D-Extractor."""
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(f"Konfigurationsdatei fehlt: {config_path}")
    with p.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)


CONFIG = None
try:
    CONFIG = load_config()
except Exception:
    # Fallback: minimale Defaults
    CONFIG = {
        'extractor': {
            'manifest_dir': 'manifest',
            'output_file': '5d_solutions.json',
            'recursive': True,
            'file_types': ['*.md', '*.txt', '*.pdf'],
            'pdf_extraction': {'method': 'pypdf', 'max_pages': 50},
        },
        'defaults': {'high_score': 0.75, 'missing_score': 0.5},
        'keywords': {},
        'patterns': {},
    }
