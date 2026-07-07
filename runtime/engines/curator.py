"""AI Curator — active knowledge improvement recommendations."""

from __future__ import annotations

from collections import Counter
from typing import Any

from runtime.knowledge.dna import KnowledgeDNA


class CuratorEngine:
    """Surfaces actionable recommendations: merges, staleness, regen, disconnects."""

    def __init__(self, brain, event_bus):
        self._brain = brain
        self._bus = event_bus

    def recommend(self) -> dict[str, Any]:
        docs = list(self._brain.kb.documents)
        ids = {d.doc_id for d in docs}
        recommendations: list[dict[str, Any]] = []

        # Merge candidates — duplicate titles
        title_map: dict[str, list[str]] = {}
        for doc in docs:
            key = (doc.title or "").strip().lower()
            if key:
                title_map.setdefault(key, []).append(doc.doc_id)
        for title, doc_ids in title_map.items():
            if len(doc_ids) > 1:
                recommendations.append({
                    "type": "merge",
                    "severity": "medium",
                    "message": f"{len(doc_ids)} documents share title — consider merge",
                    "document_ids": doc_ids,
                    "title": title,
                })
                self._bus.emit("knowledge.merge.recommended", {"document_ids": doc_ids, "title": title})

        # Outdated / low quality
        for doc in docs:
            dna = KnowledgeDNA.from_document(doc)
            if dna.quality_score < 0.45:
                recommendations.append({
                    "type": "low_quality",
                    "severity": "high",
                    "message": "Chunk has low quality score — review or regenerate",
                    "document_id": doc.doc_id,
                    "quality_score": dna.quality_score,
                })
            if len(doc.content or "") < 80:
                recommendations.append({
                    "type": "low_quality",
                    "severity": "medium",
                    "message": "Document content too short",
                    "document_id": doc.doc_id,
                })

        # Broken references
        broken = 0
        for doc in docs:
            for ref in doc.related or []:
                if ref not in ids:
                    broken += 1
                    recommendations.append({
                        "type": "broken_reference",
                        "severity": "high",
                        "message": f"Broken reference to {ref}",
                        "document_id": doc.doc_id,
                        "target": ref,
                    })
            for targets in doc.relationships.values():
                for ref in targets:
                    if ref not in ids:
                        broken += 1

        # Disconnected graph
        disconnected = sum(
            1 for doc in docs
            if not doc.related and not any(doc.relationships.values())
        )
        if disconnected > len(docs) * 0.1:
            recommendations.append({
                "type": "disconnected_graph",
                "severity": "medium",
                "message": f"Graph has {disconnected} disconnected documents — add relationships",
                "count": disconnected,
            })

        # Embedding regen hint
        indexed = self._brain.stats().get("indexed_vectors", 0)
        if indexed < len(docs) * 0.9:
            recommendations.append({
                "type": "embedding_regen",
                "severity": "high",
                "message": "Embeddings should be regenerated — index coverage below 90%",
                "indexed": indexed,
                "documents": len(docs),
            })

        return {
            "engine": "curator",
            "status": "active",
            "recommendation_count": len(recommendations),
            "recommendations": recommendations[:50],
            "summary": {
                "merge_groups": sum(1 for r in recommendations if r["type"] == "merge"),
                "low_quality": sum(1 for r in recommendations if r["type"] == "low_quality"),
                "broken_references": broken,
                "disconnected_documents": disconnected,
            },
        }

    def stats(self) -> dict[str, Any]:
        result = self.recommend()
        return {
            "engine": "curator",
            "status": "active",
            "recommendation_count": result["recommendation_count"],
        }
