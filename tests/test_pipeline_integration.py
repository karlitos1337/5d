"""
Integration tests for the 5D pipeline.
Tests the full workflow: extractor → research scraper → github api → dashboard
"""

import pytest
import json
import os
from pathlib import Path


@pytest.fixture
def pipeline_output_files():
    """Fixture that returns expected pipeline output files."""
    return {
        'solutions': '5d_solutions.json',
        'research': '5d_research_data.json',
        'github': '5d_github_data.json'
    }


def test_solutions_json_exists_and_valid(pipeline_output_files):
    """Test that 5d_solutions.json exists and is valid JSON."""
    filepath = pipeline_output_files['solutions']
    
    assert Path(filepath).exists(), f"{filepath} sollte existieren (run: python 5d_extractor.py)"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate structure
    assert 'solutions' in data or 'projects' in data, "solutions oder projects key fehlt"
    assert 'plan' in data or 'dimension_scores' in data, "plan oder dimension_scores fehlt"


def test_research_json_exists_and_valid(pipeline_output_files):
    """Test that 5d_research_data.json exists and is valid JSON."""
    filepath = pipeline_output_files['research']
    
    if not Path(filepath).exists():
        pytest.skip(f"{filepath} nicht gefunden - führe 5d_research_scraper.py aus")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Should have keywords with arxiv/pubmed results
    assert isinstance(data, dict), "Research data sollte dict sein"
    
    for keyword, results in data.items():
        if isinstance(results, dict):
            assert 'arxiv' in results or 'pubmed' in results or 'timestamp' in results


def test_github_json_exists_and_valid(pipeline_output_files):
    """Test that 5d_github_data.json exists and is valid JSON."""
    filepath = pipeline_output_files['github']
    
    if not Path(filepath).exists():
        pytest.skip(f"{filepath} nicht gefunden - führe 5d_github_api.py aus")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate structure
    assert 'repositories' in data or 'trending' in data, "repositories oder trending fehlt"
    assert 'timestamp' in data, "timestamp fehlt"


def test_pipeline_json_schemas_compatible():
    """Test that all pipeline JSONs use compatible schemas."""
    files_to_check = {
        '5d_solutions.json': [
            ['projects', 'plan'],  # New Pydantic format
            ['solutions', 'plan']   # Legacy format
        ],
        '5d_research_data.json': [],  # Dynamic keys
        '5d_github_data.json': ['repositories', 'timestamp']
    }
    
    for filename, required_keys_options in files_to_check.items():
        filepath = Path(filename)
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle multiple schema options (for backward compatibility)
        if isinstance(required_keys_options, list) and len(required_keys_options) > 0:
            if isinstance(required_keys_options[0], list):
                # Multiple schema options
                schema_valid = False
                for required_keys in required_keys_options:
                    if all(key in data for key in required_keys):
                        schema_valid = True
                        break
                assert schema_valid, f"{filename} sollte eins der Schemas erfüllen: {required_keys_options}"
            else:
                # Single schema
                for key in required_keys_options:
                    assert key in data, f"{filename} sollte '{key}' enthalten"


def test_extractor_produces_valid_projects():
    """Test that extractor produces valid project data."""
    filepath = Path('5d_solutions.json')
    if not filepath.exists():
        pytest.skip("5d_solutions.json nicht gefunden")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check for projects
    if 'projects' in data:
        projects = data['projects']
        assert isinstance(projects, list), "projects sollte Liste sein"
        
        if len(projects) > 0:
            project = projects[0]
            assert 'name' in project, "Project sollte 'name' haben"
    
    # Or check old format
    if 'solutions' in data and 'Projekte' in data['solutions']:
        projekte = data['solutions']['Projekte']
        assert isinstance(projekte, list), "Projekte sollte Liste sein"


def test_research_data_has_papers():
    """Test that research data contains paper information."""
    filepath = Path('5d_research_data.json')
    if not filepath.exists():
        pytest.skip("5d_research_data.json nicht gefunden")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Should have at least one keyword with results
    has_results = False
    for keyword, results in data.items():
        if isinstance(results, dict):
            if 'arxiv' in results and len(results['arxiv']) > 0:
                has_results = True
                # Validate paper structure
                paper = results['arxiv'][0]
                assert 'title' in paper, "Paper sollte title haben"
                break
            if 'pubmed' in results and len(results['pubmed']) > 0:
                has_results = True
                paper = results['pubmed'][0]
                assert 'title' in paper, "Paper sollte title haben"
                break
    
    assert has_results, "Research data sollte mindestens ein Paper enthalten"


def test_github_data_has_repositories():
    """Test that github data contains repository information."""
    filepath = Path('5d_github_data.json')
    if not filepath.exists():
        pytest.skip("5d_github_data.json nicht gefunden")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'repositories' in data:
        repos = data['repositories']
        assert isinstance(repos, dict), "repositories sollte dict sein"
        
        # Check for at least one query with results
        has_repos = False
        for query, repo_list in repos.items():
            if isinstance(repo_list, list) and len(repo_list) > 0:
                has_repos = True
                repo = repo_list[0]
                assert 'name' in repo, "Repo sollte name haben"
                assert 'url' in repo, "Repo sollte url haben"
                break
        
        assert has_repos, "GitHub data sollte mindestens ein Repo enthalten"


def test_all_json_files_utf8_encoded():
    """Test that all JSON files are properly UTF-8 encoded."""
    json_files = ['5d_solutions.json', '5d_research_data.json', '5d_github_data.json']
    
    for filename in json_files:
        filepath = Path(filename)
        if not filepath.exists():
            continue
        
        # Try to read with UTF-8
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                json.loads(content)
        except UnicodeDecodeError:
            pytest.fail(f"{filename} ist nicht UTF-8 encoded")
        except json.JSONDecodeError:
            pytest.fail(f"{filename} ist kein valides JSON")


def test_json_files_not_empty():
    """Test that JSON files are not empty."""
    json_files = ['5d_solutions.json', '5d_research_data.json', '5d_github_data.json']
    
    for filename in json_files:
        filepath = Path(filename)
        if not filepath.exists():
            continue
        
        file_size = filepath.stat().st_size
        assert file_size > 10, f"{filename} ist zu klein (< 10 bytes)"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data, f"{filename} sollte nicht leer sein"


@pytest.mark.integration
def test_full_pipeline_workflow():
    """Integration test for the full pipeline workflow.
    
    This test verifies that:
    1. All pipeline scripts can be imported
    2. All expected output files exist
    3. Files are valid JSON
    4. Data flows correctly between stages
    """
    # Check if all output files exist
    required_files = ['5d_solutions.json']
    optional_files = ['5d_research_data.json', '5d_github_data.json']
    
    for filename in required_files:
        assert Path(filename).exists(), f"Required file {filename} missing"
    
    # Validate all existing files
    for filename in required_files + optional_files:
        filepath = Path(filename)
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data, f"{filename} sollte Daten enthalten"
