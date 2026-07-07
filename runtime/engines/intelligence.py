"""Intelligence engine — relationship discovery and quality analysis."""

from __future__ import annotations

from typing import Any

from runtime.knowledge.dna import KnowledgeDNA


class IntelligenceEngine:
    def __init__(self, brain, event_bus):
        self._brain = brain
        self._bus = event_bus

    def analyze(self) -> dict[str, Any]:
        objects = [KnowledgeDNA.from_document(d) for d in self._brain.kb.documents]
        low_quality = [o.id for o in objects if o.quality_score < 0.5]
        orphans = [o.id for o in objects if not o.dependencies and not o.related_concepts]
        return {
            "engine": "intelligence",
            "status": "active",
            "objects_analyzed": len(objects),
            "low_quality_count": len(low_quality),
            "orphan_count": len(orphans),
        }

    def stats(self) -> dict[str, Any]:
        return self.analyze()
