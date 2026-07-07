"""Shared utilities for Coltex Product builds."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator

import yaml

import sys

ROOT = Path(__file__).resolve().parent.parent.parent


def ensure_workspace_path() -> None:
    root = str(ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)


ensure_workspace_path()

from brain.ingestion.loader import KnowledgeBase, parse_markdown, RELATIONSHIP_FIELDS


def load_product_config(path: Path | str = "config/product.yaml") -> dict[str, Any]:
    cfg_path = Path(path)
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    with cfg_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def load_knowledge_base(cfg: dict[str, Any]) -> KnowledgeBase:
    kb_cfg = cfg["knowledge_base"]
    return KnowledgeBase(
        paths=kb_cfg["paths"],
        glob_pattern=kb_cfg.get("glob", "CHUNK-*.md"),
        exclude=kb_cfg.get("exclude"),
    )


def distribution_cfg(cfg: dict[str, Any]) -> dict[str, Any]:
    return cfg.get("distribution", {})


def is_substantive_document(doc, dist_cfg: dict[str, Any]) -> tuple[bool, str]:
    """Check whether a document is suitable for commercial distribution."""
    min_chars = int(dist_cfg.get("min_substantive_chars", 60))
    for marker in dist_cfg.get("forbidden_body_markers", []):
        if marker in doc.content:
            return False, f"forbidden marker: {marker[:40]}..."
    content_lower = doc.content.lower()
    for pattern in dist_cfg.get("forbidden_source_patterns", []):
        if pattern.lower() in content_lower:
            return False, f"forbidden source pattern: {pattern}"
    if len(doc.content.strip()) < min_chars:
        return False, f"content too short ({len(doc.content.strip())} < {min_chars} chars)"
    return True, "ok"


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def chunk_document(
    doc,
    *,
    max_chars: int,
    overlap: int,
    split_on: str,
    license_name: str,
) -> list[dict[str, Any]]:
    """Split a parsed Document into vector-ready chunks."""
    import hashlib

    body = doc.content
    doc_id = doc.doc_id
    title = doc.title
    sections = re.split(rf"(?={re.escape(split_on)})", body) if split_on in body else [body]
    chunks: list[dict[str, Any]] = []

    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) < 40:
            continue
        step = max(max_chars - overlap, 1)
        for j, start in enumerate(range(0, len(section), step)):
            text = section[start : start + max_chars].strip()
            if len(text) < 40:
                continue
            chunk_id = hashlib.sha1(f"{doc_id}:{i}:{j}:{text[:64]}".encode()).hexdigest()[:16]
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "title": title,
                "category": doc.category,
                "doc_type": doc.doc_type or "documentation",
                "tags": doc.tags,
                "relationships": doc.relationships,
                "source_path": doc.path,
                "section_index": i,
                "chunk_index": j,
                "text": text,
                "char_count": len(text),
                "content_hash": hashlib.sha1(f"{doc_id}|{text}".encode()).hexdigest(),
                "license": license_name,
                "curated": True,
            })
    return chunks


def export_graph_edges(kb: KnowledgeBase) -> list[dict[str, Any]]:
    """Export typed graph edges from curated documents."""
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    for doc in kb.documents:
        for edge_type in RELATIONSHIP_FIELDS:
            for target in doc.relationships.get(edge_type, []):
                key = (doc.doc_id, edge_type, target)
                if key in seen:
                    continue
                seen.add(key)
                edges.append({
                    "source": doc.doc_id,
                    "target": target,
                    "type": edge_type,
                    "source_path": doc.path,
                })
        for target in doc.related:
            key = (doc.doc_id, "related", target)
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                "source": doc.doc_id,
                "target": target,
                "type": "related",
                "source_path": doc.path,
            })
    return edges


def normalize_doc_id(doc_id: str) -> str:
    """Normalize CHUNK-00000-LONG-TITLE → CHUNK-00000 for consistent matching."""
    if doc_id.startswith("CHUNK-"):
        parts = doc_id.split("-")
        if len(parts) >= 2 and parts[1].isdigit():
            return f"CHUNK-{parts[1]}"
    return doc_id


def normalize_id_list(ids: list[str]) -> list[str]:
    return list(dict.fromkeys(normalize_doc_id(i) for i in ids))


def extract_faq_question(doc) -> str | None:
    """Extract FAQ question from document title or first heading."""
    if "faq" not in doc.tags and doc.doc_type != "faq":
        return None
    title = doc.title.strip()
    if title and not title.lower().startswith("chunk "):
        return title
    m = re.search(r"^#\s+(.+)$", doc.content, re.MULTILINE)
    return m.group(1).strip() if m else None
