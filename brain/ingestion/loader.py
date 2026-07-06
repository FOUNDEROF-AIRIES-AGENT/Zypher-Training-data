"""Load markdown documents into Zypher Brain."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from brain.types import Document

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

RELATIONSHIP_FIELDS = (
    "related",
    "depends_on",
    "uses",
    "implements",
    "calls",
    "owned_by",
    "documents",
    "fixes",
    "replaces",
    "see_also",
)

SUPPORTED_DOC_TYPES = frozenset({
    "documentation", "guide", "tutorial", "faq", "troubleshooting",
    "api_reference", "architecture_decision", "design_document", "runbook",
    "incident_report", "support_ticket", "release_notes", "migration_guide",
    "code_walkthrough", "code_review", "meeting_notes", "database_schema",
    "sql_example", "deep_dive", "comparison", "best_practices", "anti_patterns",
    "cheat_sheet", "interview_prep", "case_study", "benchmark", "evaluation",
})


def _parse_relationships(meta: dict) -> dict[str, list[str]]:
    rels: dict[str, list[str]] = {}
    for key in RELATIONSHIP_FIELDS:
        raw = meta.get(key)
        if raw:
            rels[key] = [str(r) for r in raw]
    return rels


def _merge_meta(outer: dict, inner: dict) -> dict:
    meta = {**outer, **inner}
    for key in RELATIONSHIP_FIELDS:
        outer_vals = outer.get(key) or []
        inner_vals = inner.get(key) or []
        combined = list(dict.fromkeys([str(v) for v in outer_vals + inner_vals]))
        if combined:
            meta[key] = combined
    if inner.get("title"):
        meta["title"] = inner["title"]
    if inner.get("tags"):
        meta["tags"] = inner["tags"]
    return meta


def parse_markdown(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text

    m = FRONTMATTER_RE.match(text)
    if m:
        try:
            loaded = yaml.safe_load(m.group(1))
            meta = loaded if isinstance(loaded, dict) else {}
        except yaml.YAMLError:
            meta = {}
        body = text[m.end() :].strip()
    elif text.count("---") >= 2:
        parts = text.split("---")
        outer: dict = {}
        inner: dict = {}
        if parts[0].strip():
            try:
                loaded = yaml.safe_load(parts[0].strip())
                outer = loaded if isinstance(loaded, dict) else {}
            except yaml.YAMLError:
                outer = {}
        if len(parts) > 2 and parts[2].strip():
            try:
                loaded = yaml.safe_load(parts[2].strip())
                inner = loaded if isinstance(loaded, dict) else {}
            except yaml.YAMLError:
                inner = {}
        meta = _merge_meta(outer, inner)
        body = "---".join(parts[3:]).strip() if len(parts) > 3 else ""

    relationships = _parse_relationships(meta)
    related = list(meta.get("related") or [])
    if not related:
        for key in ("see_also", "depends_on", "uses", "implements"):
            related.extend(relationships.get(key, []))
        related = list(dict.fromkeys(related))

    return Document(
        doc_id=str(meta.get("id", path.stem)),
        title=str(meta.get("title") or path.stem),
        path=str(path),
        content=body,
        category=str(meta.get("category", "")),
        doc_type=str(meta.get("doc_type", "")),
        hub=str(meta.get("hub", "")),
        tags=list(meta.get("tags") or []),
        related=related,
        relationships=relationships,
    )


class KnowledgeBase:
    """Primary document store for Zypher Brain."""

    def __init__(
        self,
        paths: list[str],
        glob_pattern: str = "**/*.md",
        exclude: list[str] | None = None,
    ):
        self.documents: list[Document] = []
        self.by_id: dict[str, Document] = {}
        exclude = exclude or []
        for base in paths:
            root = Path(base)
            if not root.exists():
                continue
            for path in sorted(root.glob(glob_pattern)):
                if "_seed" in path.parts:
                    continue
                if any(path.match(pat) for pat in exclude):
                    continue
                if not path.is_file():
                    continue
                doc = parse_markdown(path)
                self.documents.append(doc)
                self.by_id[doc.doc_id] = doc
                if doc.doc_id.startswith("CHUNK-"):
                    parts = doc.doc_id.split("-")
                    if len(parts) >= 2:
                        self.by_id.setdefault(f"CHUNK-{parts[1]}", doc)

    def __len__(self) -> int:
        return len(self.documents)

    def get(self, doc_id: str) -> Document | None:
        return self.by_id.get(doc_id)

    def get_related(
        self,
        doc: Document,
        max_chunks: int = 8,
        edge_types: list[str] | None = None,
    ) -> list[Document]:
        found: list[Document] = []
        seen: set[str] = {doc.doc_id}
        types = edge_types or list(RELATIONSHIP_FIELDS)

        for edge_type in types:
            for rel_id in doc.relationships.get(edge_type, []):
                related = self.by_id.get(rel_id)
                if related and rel_id not in seen:
                    found.append(related)
                    seen.add(rel_id)
                if len(found) >= max_chunks:
                    return found

        for rel_id in doc.related:
            related = self.by_id.get(rel_id)
            if related and rel_id not in seen:
                found.append(related)
                seen.add(rel_id)
            if len(found) >= max_chunks:
                break
        return found
