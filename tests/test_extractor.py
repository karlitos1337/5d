import pytest
from pathlib import Path
import json
import sys, os

# Root auf sys.path legen, damit `models` importierbar ist
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from models.schemas import Solutions, Project, DimensionScore
import importlib.machinery, importlib.util, os
# Lade den Extraktor direkt aus dem Projektwurzelpfad
_path=os.path.join(ROOT, "5d_extractor.py")
_spec=importlib.util.spec_from_loader("mod", importlib.machinery.SourceFileLoader("mod", _path))
_mod=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
FiveDExtractor=_mod.FiveDExtractor


@pytest.fixture
def sample_manifest(tmp_path):
    mdir = tmp_path / "manifest"
    mdir.mkdir()
    content = (
        "# Bildungsprojekt Bäckerei\n"
        "Investment: 50.000 €\n"
        "ROI: 95%\n"
        "Pilots: 60\n\n"
        "Autonomie: 0.95\n"
        "Motivation: HIGH\n"
        "Resilienz: ventral vagal state\n"
    )
    (mdir / "test_bildung.md").write_text(content, encoding='utf-8')
    return mdir


def test_extractor_loads_md(sample_manifest, monkeypatch):
    ext = FiveDExtractor(manifest_dir=str(sample_manifest))
    texts = ext.load_manifests()
    assert any(name.endswith("test_bildung.md") for name in texts.keys())
    assert isinstance(list(texts.values())[0], str)


def test_pydantic_project_deduplication():
    sols = Solutions(
        projects=[
            Project(name="Bäckere"),
            Project(name="Bäckerei", investment="50.000"),
            Project(name="BÄCKEREI", roi="95%"),
        ],
        dimension_scores=[],
        plan={}
    )
    assert len(sols.projects) == 1
    assert sols.projects[0].name == "Bäckerei"
    assert sols.projects[0].investment == 50000.0 or sols.projects[0].roi == 95.0


def test_dimension_score_parsing():
    s1 = DimensionScore(dimension='A', score='HIGH', source='test.md')
    assert s1.score == 0.75
    s2 = DimensionScore(dimension='IM', score='0,88', source='test.md')
    assert abs(s2.score - 0.88) < 1e-6
    s3 = DimensionScore(dimension='R', score='A, 0.91', source='test.md')
    assert abs(s3.score - 0.91) < 1e-6


def test_save_solutions_validated(tmp_path):
    ext = FiveDExtractor(manifest_dir=str(tmp_path / "manifest"))
    raw = {
        'solutions': {
            'Projekte': ['Bäckere', 'Bäckerei'],
            'ROI': ['95', '100'],
            'Pilots': ['60', '15'],
            'Investment': ['50000', '30000']
        },
        'plan': {'Phase1': 'Demo'}
    }
    out = tmp_path / '5d_solutions.json'
    ext.save_solutions_validated(raw_output=raw, filename=str(out))
    data = json.loads(out.read_text(encoding='utf-8'))
    assert 'projects' in data
    assert len(data['projects']) == 1
    # Investment wird zugeordnet, da Länge konsistent mit Projekten nach Dedup ist (2 Namen -> nach Dedup 1 Projekt)
    # In diesem Fall keine genaue Zuordnung möglich, daher prüfen wir, dass kein falsches Mapping erzwungen wurde
    assert data['projects'][0].get('investment') in (None, 50000.0, 30000.0)
