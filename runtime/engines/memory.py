"""Memory engine — tiered knowledge memory model."""

from __future__ import annotations

from typing import Any


MEMORY_TIERS = ["working", "episodic", "semantic", "procedural", "archive"]


class MemoryEngine:
    def __init__(self, brain):
        self._brain = brain

    def stats(self) -> dict[str, Any]:
        report = self._brain.report()
        tiers = report.get("architecture", {}).get("memory_tiers", {})
        return {
            "engine": "memory",
            "status": "active",
            "tiers": MEMORY_TIERS,
            "distribution": tiers,
            "total_documents": report.get("documents", 0),
        }

    def resolve_tier(self, doc) -> str:
        path = doc.path.replace("\\", "/")
        if "/memory/working/" in path:
            return "working"
        if "/memory/episodic/" in path:
            return "episodic"
        if "/memory/procedural/" in path:
            return "procedural"
        if "/memory/" in path:
            return "semantic"
        return "semantic"
