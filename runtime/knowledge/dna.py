"""Knowledge object identity — DNA schema."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class KnowledgeDNA:
    """Identity and health metadata for a knowledge object."""

    id: str
    source: str = "filesystem"
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    confidence: float = 0.85
    freshness: float = 1.0
    quality_score: float = 0.0
    usage_count: int = 0
    related_concepts: list[str] = field(default_factory=list)
    evolution_state: str = "v1"
    verification_status: str = "draft"
    license: str = "Coltex-Enterprise"
    author: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    object_type: str = "document"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_document(cls, doc) -> KnowledgeDNA:
        deps = list(getattr(doc, "depends_on", []) or [])
        if not deps and hasattr(doc, "relationships"):
            deps = list(doc.relationships.get("depends_on", []))
        related = list(getattr(doc, "related", []) or [])
        concepts = list(getattr(doc, "tags", []) or [])[:12]
        if getattr(doc, "hub", None):
            concepts.append(doc.hub)
        if getattr(doc, "category", None):
            concepts.append(doc.category)
        content_len = len(getattr(doc, "content", "") or "")
        meta_score = 1.0 if doc.title and doc.doc_id else 0.5
        link_score = min(1.0, (len(related) + len(deps)) / 5)
        quality = round(min(1.0, 0.4 * meta_score + 0.3 * link_score + 0.3 * min(1.0, content_len / 500)), 3)
        return cls(
            id=doc.doc_id,
            source=getattr(doc, "source", "filesystem") or "filesystem",
            dependencies=deps,
            related_concepts=sorted(set(concepts)),
            quality_score=quality,
            author=getattr(doc, "author", None),
            object_type="document",
        )
