"""Graph relationship traversal for Zypher Brain."""

from __future__ import annotations

from collections import deque

from brain.ingestion.loader import KnowledgeBase
from brain.types import Document, ScoredDocument


class GraphIndex:
    def __init__(self, kb: KnowledgeBase, max_hops: int = 2, max_extra: int = 8):
        self.kb = kb
        self.max_hops = max_hops
        self.max_extra = max_extra

    def expand(self, seeds: list[Document]) -> list[ScoredDocument]:
        seen = {d.doc_id for d in seeds}
        results: list[ScoredDocument] = []
        queue: deque[tuple[Document, int]] = deque((doc, 0) for doc in seeds)

        while queue and len(results) < self.max_extra:
            current, depth = queue.popleft()
            if depth >= self.max_hops:
                continue
            for related in self.kb.get_related(current, max_chunks=self.max_extra):
                if related.doc_id in seen:
                    continue
                seen.add(related.doc_id)
                hop_score = max(0.3, 0.8 - depth * 0.2)
                results.append(ScoredDocument(document=related, score=hop_score, source="graph"))
                queue.append((related, depth + 1))
        return results

    def search_from_seeds(self, seeds: list[ScoredDocument]) -> list[ScoredDocument]:
        docs = [s.document for s in seeds]
        return self.expand(docs)
