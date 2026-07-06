"""Add documents to Zypher Brain without model retraining."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from brain.ingestion.loader import parse_markdown
from brain.types import Document

if TYPE_CHECKING:
    from brain.brain import ZypherBrain


def write_document(
    path: Path,
    title: str,
    content: str,
    doc_type: str = "documentation",
    category: str = "general",
    tags: list[str] | None = None,
    hub: str = "",
) -> Document:
    """Write a new markdown document to the knowledge base."""
    doc_id = path.stem
    metadata = {
        "id": doc_id,
        "title": title,
        "category": category,
        "doc_type": doc_type,
        "topic_slug": path.stem,
        "difficulty": "intermediate",
        "tags": tags or [doc_type, category],
        "hub": hub,
        "related": [],
        "depends_on": [],
        "uses": [],
        "implements": [],
        "calls": [],
        "owned_by": [],
        "documents": [],
        "fixes": [],
        "replaces": [],
        "see_also": [],
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "version": "3.0",
    }
    body = f"# {title}\n\n{content.strip()}\n"
    frontmatter = yaml.safe_dump(metadata, sort_keys=False).strip()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return parse_markdown(path)


def ingest_file(brain: ZypherBrain, path: Path, reindex: bool = True) -> Document:
    """Load a new file into Zypher Brain and optionally re-index it."""
    doc = parse_markdown(path)
    brain.kb.documents.append(doc)
    brain.kb.by_id[doc.doc_id] = doc
    if reindex:
        brain.index_document(doc)
    return doc


def ingest_directory(brain: ZypherBrain, directory: Path, reindex: bool = True) -> int:
    """Ingest all markdown files from a directory."""
    count = 0
    for path in sorted(directory.rglob("*.md")):
        if "_seed" in path.parts:
            continue
        ingest_file(brain, path, reindex=False)
        count += 1
    if reindex and count:
        brain.index(force=True)
    return count
