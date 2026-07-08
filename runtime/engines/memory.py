"""Memory engine — five-tier knowledge memory model."""

from __future__ import annotations

from typing import Any

MEMORY_TIERS = ["working", "project", "organization", "historical", "archive"]


class MemoryEngine:
    """
    Working Memory → Project Memory → Organization Memory → Historical Memory → Archive
    """

    def __init__(self, brain):
        self._brain = brain

    def stats(self) -> dict[str, Any]:
        counts = {t: 0 for t in MEMORY_TIERS}
        for doc in self._brain.kb.documents:
            counts[self.resolve_tier(doc)] += 1
        return {
            "engine": "memory",
            "status": "active",
            "tiers": MEMORY_TIERS,
            "distribution": counts,
            "total_documents": sum(counts.values()),
        }

    def resolve_tier(self, doc) -> str:
        path = doc.path.replace("\\", "/").lower()
        if "/memory/working/" in path or "/quick-reference/" in path:
            return "working"
        if "/domains/" in path or "/clusters/" in path:
            return "project"
        if "/hubs/" in path or "/graph-links/" in path or "/domain-routes/" in path:
            return "organization"
        if "/memory/episodic/" in path or "/memory/procedural/" in path:
            return "historical"
        if "/memory/" in path or "_excluded" in path or "deprecated" in path:
            return "archive"
        return "organization"

    def evolution_state(self, doc) -> str:
        path = doc.path.replace("\\", "/").lower()
        content = (doc.content or "").lower()
        if "deprecated" in content[:500] or "deprecated" in path:
            return "deprecated"
        if "_excluded" in path:
            return "archived"
        if doc.doc_type in ("runbook", "api_reference", "best_practices"):
            return "published"
        if doc.doc_type in ("architecture_decision", "design_document"):
            return "verified"
        return "created"
