"""Retrieval engine — reasoning-oriented retrieval wrapper."""

from __future__ import annotations

from typing import Any


class RetrievalEngine:
    def __init__(self, brain):
        self._brain = brain

    def retrieve(self, query: str, *, with_context: bool = False) -> dict[str, Any]:
        result = self._brain.retrieve(query)
        out: dict[str, Any] = {
            "query": query,
            "documents": [
                {"id": s.document.doc_id, "title": s.document.title, "score": s.score}
                for s in result.documents
            ],
        }
        if with_context:
            out["context"] = result.context
        return out

    def stats(self) -> dict[str, Any]:
        return {"engine": "retrieval", "status": "active"}
