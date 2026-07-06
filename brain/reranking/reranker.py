"""Merge and re-rank retrieval results from multiple sources."""

from __future__ import annotations

from brain.types import ScoredDocument

SOURCE_WEIGHTS = {
    "vector": 1.0,
    "metadata": 0.85,
    "graph": 0.65,
}


class Reranker:
    def __init__(self, source_weights: dict[str, float] | None = None):
        self.weights = source_weights or SOURCE_WEIGHTS

    def merge(self, *result_sets: list[ScoredDocument], top_k: int = 10) -> list[ScoredDocument]:
        combined: dict[str, ScoredDocument] = {}
        for results in result_sets:
            for item in results:
                doc_id = item.document.doc_id
                weighted = item.score * self.weights.get(item.source, 0.5)
                if doc_id in combined:
                    existing = combined[doc_id]
                    combined[doc_id] = ScoredDocument(
                        document=existing.document,
                        score=existing.score + weighted,
                        source=f"{existing.source}+{item.source}",
                    )
                else:
                    combined[doc_id] = ScoredDocument(
                        document=item.document,
                        score=weighted,
                        source=item.source,
                    )
        ranked = sorted(combined.values(), key=lambda s: s.score, reverse=True)
        return ranked[:top_k]
