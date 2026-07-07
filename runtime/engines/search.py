"""Search engine — hybrid retrieval over knowledge objects."""

from __future__ import annotations

from typing import Any


class SearchEngine:
    def __init__(self, brain):
        self._brain = brain

    def search(self, query: str) -> dict[str, Any]:
        result = self._brain.retrieve(query)
        return {
            "query": query,
            "results": [
                {
                    "id": s.document.doc_id,
                    "title": s.document.title,
                    "score": round(s.score, 4),
                    "source": s.source,
                }
                for s in result.documents
            ],
            "context_chars": len(result.context),
        }

    def stats(self) -> dict[str, Any]:
        return {"engine": "search", "status": "active", **self._brain.stats()}
