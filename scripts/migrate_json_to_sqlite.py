#!/usr/bin/env python3
"""
Migration script: JSON → SQLite

Reads:
  - 5d_research_data.json  → research_papers table
  - 5d_github_data.json    → github_repositories table

Usage:
    python scripts/migrate_json_to_sqlite.py
    python scripts/migrate_json_to_sqlite.py --db my_custom.db
    python scripts/migrate_json_to_sqlite.py --dry-run

Idempotent: rows with the same (title, source, keyword) are skipped to
avoid duplicates when the script is run more than once.
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Allow running from repo root without installing the package
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy.orm import Session  # noqa: E402

from models.research import (  # noqa: E402
    DEFAULT_DB_PATH,
    GitHubRepository,
    ResearchPaper,
    init_db,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# JSON loading helpers
# ---------------------------------------------------------------------------

RESEARCH_JSON = ROOT / "5d_research_data.json"
GITHUB_JSON = ROOT / "5d_github_data.json"


def _load_json(path: Path) -> dict:
    """Load a JSON file, returning an empty dict on any error."""
    if not path.exists():
        logger.warning("File not found: %s – skipping", path)
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("JSON parse error in %s: %s – skipping", path, exc)
        return {}


def _parse_dt(value: str | None) -> datetime | None:
    """
    Best-effort datetime parser for the varied date strings found in the JSON
    files (ISO 8601, 'YYYY Mon', 'YYYY').
    Returns *None* if the value cannot be parsed.
    """
    if not value:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%Y %b",
        "%Y",
    ):
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Migration helpers
# ---------------------------------------------------------------------------


def _existing_paper_keys(session: Session) -> set[tuple]:
    """Return a set of (title, source, keyword) tuples already in the DB."""
    rows = session.query(
        ResearchPaper.title, ResearchPaper.source, ResearchPaper.keyword
    ).all()
    return {(r.title, r.source, r.keyword) for r in rows}


def _existing_repo_keys(session: Session) -> set[tuple]:
    """Return a set of (name, category) tuples already in the DB."""
    rows = session.query(GitHubRepository.name, GitHubRepository.category).all()
    return {(r.name, r.category) for r in rows}


def migrate_research(session: Session, data: dict, dry_run: bool = False) -> int:
    """
    Insert research papers from *data* into the DB.

    Parameters:
        session: Active SQLAlchemy session.
        data: Parsed contents of 5d_research_data.json.
        dry_run: If True, log actions but do not commit.

    Returns:
        Number of rows inserted (or that would be inserted in dry-run mode).
    """
    existing = _existing_paper_keys(session)
    inserted = 0

    for keyword, topic in data.items():
        if not isinstance(topic, dict):
            continue
        for source in ("arxiv", "pubmed"):
            papers = topic.get(source, [])
            if not isinstance(papers, list):
                continue
            for paper in papers:
                if not isinstance(paper, dict):
                    continue
                title = (paper.get("title") or "").strip()
                if not title:
                    continue
                key = (title, source, keyword)
                if key in existing:
                    continue
                existing.add(key)

                authors_raw = paper.get("authors", [])
                if isinstance(authors_raw, str):
                    authors_raw = [authors_raw]

                row = ResearchPaper(
                    title=title,
                    source=source,
                    keyword=keyword,
                    published=_parse_dt(paper.get("published")),
                    authors=authors_raw,
                    summary=paper.get("summary") or paper.get("abstract"),
                    link=paper.get("link"),
                )
                if not dry_run:
                    session.add(row)
                inserted += 1

    if not dry_run:
        session.commit()
    logger.info("research_papers: %d row(s) %s", inserted, "would be inserted" if dry_run else "inserted")
    return inserted


def migrate_github(session: Session, data: dict, dry_run: bool = False) -> int:
    """
    Insert GitHub repositories from *data* into the DB.

    Parameters:
        session: Active SQLAlchemy session.
        data: Parsed contents of 5d_github_data.json.
        dry_run: If True, log actions but do not commit.

    Returns:
        Number of rows inserted (or that would be inserted in dry-run mode).
    """
    existing = _existing_repo_keys(session)
    inserted = 0

    repositories = data.get("repositories", {})
    if not isinstance(repositories, dict):
        logger.warning("github data missing 'repositories' dict – skipping")
        return 0

    for category, repos in repositories.items():
        if not isinstance(repos, list):
            continue
        for repo in repos:
            if not isinstance(repo, dict):
                continue
            name = (repo.get("name") or "").strip()
            if not name:
                continue
            key = (name, category)
            if key in existing:
                continue
            existing.add(key)

            row = GitHubRepository(
                name=name,
                full_name=repo.get("full_name"),
                description=repo.get("description"),
                category=category,
                stars=repo.get("stars"),
                forks=repo.get("forks"),
                language=repo.get("language"),
                url=repo.get("url"),
                updated=_parse_dt(repo.get("updated")),
            )
            if not dry_run:
                session.add(row)
            inserted += 1

    if not dry_run:
        session.commit()
    logger.info(
        "github_repositories: %d row(s) %s",
        inserted,
        "would be inserted" if dry_run else "inserted",
    )
    return inserted


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate 5D JSON files to SQLite.")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the SQLite database file (default: 5d_research.db)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without writing to the DB",
    )
    args = parser.parse_args()

    logger.info("Initialising database: %s", args.db)
    engine = init_db(db_path=args.db)

    research_data = _load_json(RESEARCH_JSON)
    github_data = _load_json(GITHUB_JSON)

    with Session(engine) as session:
        migrate_research(session, research_data, dry_run=args.dry_run)
        migrate_github(session, github_data, dry_run=args.dry_run)

    if args.dry_run:
        logger.info("Dry-run complete – no data was written.")
    else:
        logger.info("Migration complete – database: %s", args.db)


if __name__ == "__main__":
    main()
