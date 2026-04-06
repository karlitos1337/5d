#!/usr/bin/env python3
"""
Tests for the SQLite database layer (Phase 4 migration).

Covers:
- Schema creation and table existence
- ResearchPaper model CRUD
- GitHubRepository model CRUD
- Migration helpers (migrate_research, migrate_github)
- Idempotency (duplicate rows not inserted)
- Date parsing edge cases
- to_dict() serialisation
"""

import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import inspect as sa_inspect  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from models.research import (  # noqa: E402
    GitHubRepository,
    ResearchPaper,
    init_db,
)
from scripts.migrate_json_to_sqlite import (  # noqa: E402
    _parse_dt,
    migrate_github,
    migrate_research,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_db(tmp_path):
    """Initialise a fresh in-memory-style SQLite DB in a temp directory."""
    db_path = tmp_path / "test.db"
    engine = init_db(db_path=db_path)
    yield db_path, engine
    engine.dispose()


@pytest.fixture()
def session(tmp_db):
    """Yield an open Session against the temp DB, roll back after each test."""
    db_path, engine = tmp_db
    with Session(engine) as s:
        yield s


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestSchema:
    def test_tables_created(self, tmp_db):
        """Both tables must exist after init_db()."""
        _, engine = tmp_db
        insp = sa_inspect(engine)
        tables = insp.get_table_names()
        assert "research_papers" in tables
        assert "github_repositories" in tables

    def test_research_papers_columns(self, tmp_db):
        """research_papers must have all required columns."""
        _, engine = tmp_db
        insp = sa_inspect(engine)
        cols = {c["name"] for c in insp.get_columns("research_papers")}
        required = {"id", "title", "source", "keyword", "published", "authors", "summary", "link", "created_at"}
        assert required.issubset(cols)

    def test_github_repositories_columns(self, tmp_db):
        """github_repositories must have all required columns."""
        _, engine = tmp_db
        insp = sa_inspect(engine)
        cols = {c["name"] for c in insp.get_columns("github_repositories")}
        required = {"id", "name", "full_name", "description", "category", "stars", "forks", "language", "url", "updated", "created_at"}
        assert required.issubset(cols)

    def test_indexes_created(self, tmp_db):
        """Key indexes must exist on research_papers and github_repositories."""
        _, engine = tmp_db
        insp = sa_inspect(engine)

        rp_idx = {i["name"] for i in insp.get_indexes("research_papers")}
        assert "idx_keyword" in rp_idx
        assert "idx_source" in rp_idx
        assert "idx_published" in rp_idx

        gh_idx = {i["name"] for i in insp.get_indexes("github_repositories")}
        assert "idx_gh_category" in gh_idx
        assert "idx_gh_stars" in gh_idx


# ---------------------------------------------------------------------------
# ResearchPaper model tests
# ---------------------------------------------------------------------------


class TestResearchPaperModel:
    def test_insert_and_query(self, session):
        paper = ResearchPaper(
            title="Test Paper",
            source="arxiv",
            keyword="self-directed learning",
            published=datetime(2023, 6, 1),
            authors=["Alice", "Bob"],
            summary="A great summary.",
            link="https://arxiv.org/abs/1234.5678",
        )
        session.add(paper)
        session.commit()

        result = session.query(ResearchPaper).filter_by(title="Test Paper").first()
        assert result is not None
        assert result.source == "arxiv"
        assert result.keyword == "self-directed learning"

    def test_to_dict_structure(self, session):
        paper = ResearchPaper(
            title="Dict Test",
            source="pubmed",
            keyword="democratic schools",
            authors=["Carol"],
            link="https://pubmed.ncbi.nlm.nih.gov/99",
        )
        session.add(paper)
        session.commit()

        d = paper.to_dict()
        assert d["title"] == "Dict Test"
        assert d["source"] == "pubmed"
        assert isinstance(d["authors"], list)
        assert d["link"].startswith("https://")

    def test_nullable_fields_allowed(self, session):
        paper = ResearchPaper(title="Minimal", source="arxiv", keyword="kw")
        session.add(paper)
        session.commit()
        assert paper.id is not None
        assert paper.published is None
        assert paper.summary is None


# ---------------------------------------------------------------------------
# GitHubRepository model tests
# ---------------------------------------------------------------------------


class TestGitHubRepositoryModel:
    def test_insert_and_query(self, session):
        repo = GitHubRepository(
            name="my-edu-repo",
            full_name="owner/my-edu-repo",
            description="An educational repo",
            category="democratic education",
            stars=42,
            forks=7,
            language="Python",
            url="https://github.com/owner/my-edu-repo",
            updated=datetime(2024, 1, 15),
        )
        session.add(repo)
        session.commit()

        result = session.query(GitHubRepository).filter_by(name="my-edu-repo").first()
        assert result is not None
        assert result.stars == 42
        assert result.category == "democratic education"

    def test_to_dict_structure(self, session):
        repo = GitHubRepository(name="repo2", category="intrinsic motivation", stars=100)
        session.add(repo)
        session.commit()

        d = repo.to_dict()
        assert d["name"] == "repo2"
        assert d["stars"] == 100
        assert "category" in d


# ---------------------------------------------------------------------------
# Migration helper tests
# ---------------------------------------------------------------------------


class TestMigrateResearch:
    SAMPLE_DATA = {
        "self-directed learning": {
            "arxiv": [
                {
                    "title": "Autonomous Learning in Neural Nets",
                    "authors": ["Smith, J.", "Doe, A."],
                    "published": "2023-05-10",
                    "link": "https://arxiv.org/abs/2305.12345",
                    "summary": "We study autonomous systems.",
                }
            ],
            "pubmed": [
                {
                    "title": "Self-Directed Study in Adolescents",
                    "authors": ["Garcia, M."],
                    "published": "2022 Mar",
                    "link": "https://pubmed.ncbi.nlm.nih.gov/12345/",
                }
            ],
            "timestamp": "2026-04-05T10:00:00",
        }
    }

    def test_inserts_papers(self, session):
        count = migrate_research(session, self.SAMPLE_DATA)
        assert count == 2

    def test_correct_source_tags(self, session):
        migrate_research(session, self.SAMPLE_DATA)
        sources = {p.source for p in session.query(ResearchPaper).all()}
        assert "arxiv" in sources
        assert "pubmed" in sources

    def test_idempotent(self, session):
        first = migrate_research(session, self.SAMPLE_DATA)
        second = migrate_research(session, self.SAMPLE_DATA)
        assert first == 2
        assert second == 0  # Nothing new

    def test_dry_run_inserts_nothing(self, session):
        migrate_research(session, self.SAMPLE_DATA, dry_run=True)
        assert session.query(ResearchPaper).count() == 0

    def test_skips_papers_without_title(self, session):
        data = {
            "kw": {
                "arxiv": [{"title": "", "link": "https://x.com"}],
                "pubmed": [],
            }
        }
        count = migrate_research(session, data)
        assert count == 0

    def test_handles_empty_data(self, session):
        count = migrate_research(session, {})
        assert count == 0


class TestMigrateGitHub:
    SAMPLE_DATA = {
        "repositories": {
            "democratic education": [
                {
                    "name": "edu-repo-A",
                    "full_name": "org/edu-repo-A",
                    "description": "Demo repo",
                    "stars": 150,
                    "forks": 30,
                    "language": "Python",
                    "url": "https://github.com/org/edu-repo-A",
                    "updated": "2024-03-01T12:00:00Z",
                }
            ],
            "intrinsic motivation": [
                {
                    "name": "motivation-kit",
                    "full_name": "user/motivation-kit",
                    "description": "Motivational learning tools",
                    "stars": 50,
                    "forks": 5,
                    "language": "JavaScript",
                    "url": "https://github.com/user/motivation-kit",
                    "updated": "2025-01-10T08:00:00Z",
                }
            ],
        },
        "timestamp": "2026-04-05T10:00:00",
    }

    def test_inserts_repositories(self, session):
        count = migrate_github(session, self.SAMPLE_DATA)
        assert count == 2

    def test_correct_categories(self, session):
        migrate_github(session, self.SAMPLE_DATA)
        categories = {r.category for r in session.query(GitHubRepository).all()}
        assert "democratic education" in categories
        assert "intrinsic motivation" in categories

    def test_idempotent(self, session):
        first = migrate_github(session, self.SAMPLE_DATA)
        second = migrate_github(session, self.SAMPLE_DATA)
        assert first == 2
        assert second == 0

    def test_dry_run_inserts_nothing(self, session):
        migrate_github(session, self.SAMPLE_DATA, dry_run=True)
        assert session.query(GitHubRepository).count() == 0

    def test_handles_empty_data(self, session):
        count = migrate_github(session, {})
        assert count == 0


# ---------------------------------------------------------------------------
# Date parsing tests
# ---------------------------------------------------------------------------


class TestParseDt:
    def test_iso_with_z(self):
        dt = _parse_dt("2024-03-01T12:00:00Z")
        assert dt == datetime(2024, 3, 1, 12, 0, 0)

    def test_iso_without_z(self):
        dt = _parse_dt("2023-05-10")
        assert dt == datetime(2023, 5, 10)

    def test_year_month_string(self):
        dt = _parse_dt("2022 Mar")
        assert dt == datetime(2022, 3, 1)

    def test_year_only(self):
        dt = _parse_dt("2021")
        assert dt == datetime(2021, 1, 1)

    def test_none_input(self):
        assert _parse_dt(None) is None

    def test_empty_string(self):
        assert _parse_dt("") is None

    def test_unparseable_returns_none(self):
        assert _parse_dt("not-a-date") is None
