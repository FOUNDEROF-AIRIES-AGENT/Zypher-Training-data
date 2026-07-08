"""Knowledge analytics — metrics about knowledge, not users."""

from __future__ import annotations

from collections import Counter
from typing import Any

from runtime.knowledge.dna import KnowledgeDNA


class AnalyticsEngine:
    def __init__(self, brain):
        self._brain = brain

    def health(self) -> dict[str, Any]:
        docs = list(self._brain.kb.documents)
        ids = {d.doc_id for d in docs}
        dna_list = [KnowledgeDNA.from_document(d) for d in docs]

        if not docs:
            return self._empty_health()

        avg_quality = sum(d.quality_score for d in dna_list) / len(dna_list)
        with_links = sum(1 for d in docs if d.related or any(d.relationships.values()))
        graph_integrity = with_links / len(docs)

        disconnected = sum(
            1 for d in docs if not d.related and not any(d.relationships.values())
        )

        broken = 0
        for doc in docs:
            for ref in doc.related or []:
                if ref not in ids:
                    broken += 1
            for targets in doc.relationships.values():
                for ref in targets:
                    if ref not in ids:
                        broken += 1

        titles = [d.title.strip().lower() for d in docs if d.title]
        dup_risk = 0.0
        if titles:
            counts = Counter(titles)
            dups = sum(c - 1 for c in counts.values() if c > 1)
            dup_risk = dups / len(docs)

        report = self._brain.report()
        domain_count = report.get("architecture", {}).get("domain_count", 0)
        coverage = min(1.0, domain_count / 63) if domain_count else 0.0

        indexed = self._brain.stats().get("indexed_vectors", 0)
        retrieval_ready = min(1.0, indexed / max(len(docs), 1))

        knowledge_score = round(
            0.28 * avg_quality + 0.22 * graph_integrity + 0.20 * coverage
            + 0.15 * (1 - dup_risk) + 0.15 * retrieval_ready,
            3,
        )

        return {
            "engine": "analytics",
            "status": "active",
            "knowledge_score": round(knowledge_score * 100, 1),
            "knowledge_quality": round(avg_quality * 100, 1),
            "coverage": round(coverage * 100, 1),
            "freshness": round(max(0, 100 - disconnected / max(len(docs), 1) * 100), 1),
            "duplicate_risk": round(dup_risk * 100, 1),
            "retrieval_success": round(retrieval_ready * 100, 1),
            "broken_references": broken,
            "disconnected_graphs": disconnected,
            "graph_integrity": round(graph_integrity * 100, 1),
        }

    def _empty_health(self) -> dict[str, Any]:
        return {
            "engine": "analytics",
            "status": "empty",
            "knowledge_score": 0,
            "message": "No documents loaded",
        }

    def stats(self) -> dict[str, Any]:
        return self.health()
