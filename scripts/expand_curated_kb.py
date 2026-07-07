#!/usr/bin/env python3
"""Expand curated seed knowledge-base with high-quality CHUNK documents."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from corpus_templates import TOPICS, Topic
from generate_corpus import build_document, SECTION_TEMPLATES
from brain_schema import PREMIUM_CATEGORIES, PREMIUM_DOC_TYPES

KB_DIR = ROOT / "knowledge-base"
START_CHUNK = 162

CURATED_DOC_TYPES = PREMIUM_DOC_TYPES

PRIORITY_CATEGORIES = PREMIUM_CATEGORIES


def _existing_chunk_max() -> int:
    max_num = START_CHUNK - 1
    for path in KB_DIR.glob("CHUNK-*.md"):
        m = re.match(r"CHUNK-(\d+)", path.name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:60]


def _chunk_id(num: int) -> str:
    return f"CHUNK-{num:05d}"


def _format_chunk_markdown(
    chunk_num: int,
    body: str,
    metadata: dict,
    related: list[str],
) -> str:
    slug = _slugify(metadata["title"])
    outer_id = f"{_chunk_id(chunk_num)}-{slug.upper().replace('_', '-')}"
    inner_id = _chunk_id(chunk_num)

    outer_meta = {
        "id": outer_id,
        "title": f"Chunk {chunk_num:05d} {metadata['title'][:80]}",
        "category": f"CHUNK-{chunk_num:05d}-{slug}.md",
        "tags": metadata.get("tags", [])[:12],
        "difficulty": metadata.get("difficulty", "intermediate"),
        "related": related,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "version": "2.0",
    }
    inner_meta = {
        "id": inner_id,
        "title": metadata["title"],
        "category": metadata.get("category", "general"),
        "doc_type": metadata.get("doc_type", "documentation"),
        "tags": metadata.get("tags", []),
        "difficulty": metadata.get("difficulty", "intermediate"),
        "related": [],
        "last_updated": outer_meta["last_updated"],
        "version": "2.0",
    }
    if metadata.get("hub"):
        inner_meta["hub"] = metadata["hub"]

    outer_yaml = yaml.safe_dump(outer_meta, sort_keys=False).strip()
    inner_yaml = yaml.safe_dump(inner_meta, sort_keys=False).strip()
    return f"---\n{outer_yaml}\n---\n\n---\n{inner_yaml}\n---\n\n{body}\n"


def iter_curated_jobs(target_count: int, start_num: int) -> list[tuple[int, Topic, str, int]]:
    jobs: list[tuple[int, Topic, str, int]] = []
    cat_set = set(PRIORITY_CATEGORIES)
    topics = [t for t in TOPICS if t.category in cat_set]
    chunk_num = start_num
    variant = 0

    while len(jobs) < target_count:
        for topic in topics:
            for doc_type in CURATED_DOC_TYPES:
                if len(jobs) >= target_count:
                    break
                jobs.append((chunk_num, topic, doc_type, variant))
                chunk_num += 1
                variant += 1
        if not topics:
            break
    return jobs


def expand_kb(target_count: int = 120, dry_run: bool = False) -> dict:
    start_num = _existing_chunk_max() + 1
    jobs = iter_curated_jobs(target_count, start_num)
    related_pool: list[str] = []
    written = 0

    for chunk_num, topic, doc_type, variant in jobs:
        body, metadata = build_document(topic, doc_type, variant, scale=1000)
        related = related_pool[-8:] if related_pool else []
        content = _format_chunk_markdown(chunk_num, body, metadata, related)
        slug = _slugify(metadata["title"])
        filename = f"CHUNK-{chunk_num:05d}-{slug}.md"
        path = KB_DIR / filename

        if not dry_run:
            path.write_text(content, encoding="utf-8")
        related_pool.append(_chunk_id(chunk_num))
        written += 1

    return {
        "documents_written": written,
        "start_chunk": start_num,
        "end_chunk": start_num + written - 1 if written else start_num,
        "categories": len({j[1].category for j in jobs}),
        "doc_types": len({j[2] for j in jobs}),
        "dry_run": dry_run,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Expand curated seed knowledge-base")
    parser.add_argument("--count", type=int, default=120, help="Number of CHUNK docs to generate")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    stats = expand_kb(target_count=args.count, dry_run=args.dry_run)
    print(yaml.safe_dump(stats, sort_keys=False))


if __name__ == "__main__":
    main()
