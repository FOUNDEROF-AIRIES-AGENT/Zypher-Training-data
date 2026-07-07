"""Graph engine — relationship and topology operations."""

from __future__ import annotations

from typing import Any


class GraphEngine:
    def __init__(self, brain):
        self._brain = brain

    def stats(self) -> dict[str, Any]:
        report = self._brain.report()
        arch = report.get("architecture", {})
        return {
            "engine": "graph",
            "status": "active",
            "graph_edges": arch.get("graph_edges", 0),
            "graph_density": arch.get("graph_density", 0),
            "hubs": arch.get("hub_count", 0),
            "domains": arch.get("domain_count", 0),
        }

    def neighbors(self, doc_id: str) -> dict[str, Any]:
        for doc in self._brain.kb.documents:
            if doc.doc_id == doc_id:
                return {
                    "id": doc_id,
                    "related": list(doc.related or []),
                    "relationships": {k: list(v) for k, v in doc.relationships.items()},
                }
        return {"id": doc_id, "error": "not_found"}
