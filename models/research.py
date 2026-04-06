#!/usr/bin/env python3
"""
SQLAlchemy ORM models for research data storage.

Tables:
- research_papers: arXiv / PubMed publications indexed by keyword
- github_repositories: GitHub repositories indexed by education category

Schema follows the Phase-4 migration spec from GitHub issue #XX.
"""

import json
from datetime import datetime
from pathlib import Path

from sqlalchemy import (
    JSON,
    DateTime,
    Index,
    Integer,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ResearchPaper(Base):
    """
    Academic paper sourced from arXiv or PubMed.

    Attributes:
        id: Auto-increment primary key.
        title: Paper title (required).
        source: Data origin – 'arxiv' or 'pubmed'.
        keyword: Search keyword used to discover this paper.
        published: Original publication date (nullable).
        authors: List of author names stored as JSON array.
        summary: Abstract / summary text.
        link: Canonical URL to the paper.
        created_at: Row insertion timestamp.
    """

    __tablename__ = "research_papers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False)  # 'arxiv' | 'pubmed'
    keyword: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    authors: Mapped[str | None] = mapped_column(JSON, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    link: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Indexes for common dashboard queries
    __table_args__ = (
        Index("idx_keyword", "keyword"),
        Index("idx_source", "source"),
        Index("idx_published", "published"),
    )

    def to_dict(self) -> dict:
        """Return a plain dict compatible with the legacy JSON schema."""
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "keyword": self.keyword,
            "published": self.published.isoformat() if self.published else None,
            "authors": self.authors if isinstance(self.authors, list) else json.loads(self.authors or "[]"),
            "summary": self.summary,
            "link": self.link,
        }


class GitHubRepository(Base):
    """
    GitHub repository discovered via education-related keyword search.

    Attributes:
        id: Auto-increment primary key.
        name: Short repository name.
        full_name: owner/repo slug.
        description: Repository description text.
        category: Search category (e.g. 'self-directed learning').
        stars: GitHub stargazer count.
        forks: GitHub fork count.
        language: Primary programming language.
        url: HTML URL to the repository.
        updated: Last pushed / updated timestamp from GitHub.
        created_at: Row insertion timestamp.
    """

    __tablename__ = "github_repositories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    full_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    stars: Mapped[int | None] = mapped_column(Integer, nullable=True)
    forks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    language: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Indexes for common dashboard queries (category, stars, language)
    __table_args__ = (
        Index("idx_gh_category", "category"),
        Index("idx_gh_stars", "stars"),
        Index("idx_gh_language", "language"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description,
            "category": self.category,
            "stars": self.stars,
            "forks": self.forks,
            "language": self.language,
            "url": self.url,
            "updated": self.updated.isoformat() if self.updated else None,
        }


# ---------------------------------------------------------------------------
# Engine / session helpers
# ---------------------------------------------------------------------------

DEFAULT_DB_PATH = Path("5d_research.db")


def get_engine(db_path: Path = DEFAULT_DB_PATH):
    """Create (or reuse) a SQLite engine for *db_path*."""
    url = f"sqlite:///{db_path}"
    return create_engine(url, echo=False)


def init_db(db_path: Path = DEFAULT_DB_PATH):
    """Create all tables (idempotent – safe to call multiple times)."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    return engine


def get_session(db_path: Path = DEFAULT_DB_PATH) -> Session:
    """Return a new SQLAlchemy session bound to *db_path*."""
    engine = get_engine(db_path)
    return Session(engine)
