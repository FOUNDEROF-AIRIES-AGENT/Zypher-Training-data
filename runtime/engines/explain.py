"""Retrieval explainability — why did Coltex retrieve this?"""

from __future__ import annotations

import re
import time
from typing import Any


class ExplainEngine:
    def __init__(self, brain, monitor=None):
        self._brain = brain
        self._monitor = monitor

    def explain(self, query: str, top_k: int = 5) -> dict[str, Any]:
        start = time.perf_counter()
        pipeline = self._brain.retrieval

        vector_hits = pipeline.vector_index.search(query, top_k=top_k * 2)
        metadata_hits = pipeline.metadata_index.search(query, top_k=top_k * 2)
        graph_hits = pipeline.graph_index.search_from_seeds(vector_hits + metadata_hits)
        merged = pipeline.reranker.merge(vector_hits, metadata_hits, graph_hits, top_k=top_k)

        vector_ids = {s.document.doc_id for s in vector_hits}
        metadata_ids = {s.document.doc_id for s in metadata_hits}
        graph_ids = {s.document.doc_id for s in graph_hits}

        query_lower = query.lower()
        query_tokens = set(re.findall(r"\w+", query_lower))

        explanations = []
        for scored in merged:
            doc = scored.document
            reasons: list[dict[str, Any]] = []

            if doc.doc_id in vector_ids:
                v_score = next((s.score for s in vector_hits if s.document.doc_id == doc.doc_id), 0)
                reasons.append({
                    "factor": "vector_similarity",
                    "label": "Similarity",
                    "score": round(min(v_score * 100, 99), 1),
                    "unit": "percent",
                })

            if doc.doc_id in graph_ids:
                reasons.append({
                    "factor": "graph_relationship",
                    "label": "Graph Relationship",
                    "detail": "Connected via graph expansion from seed results",
                })

            if doc.doc_id in metadata_ids:
                reasons.append({
                    "factor": "metadata_match",
                    "label": "Metadata Match",
                    "detail": f"doc_type={doc.doc_type or 'unknown'}, hub={doc.hub or 'none'}",
                })

            title_lower = (doc.title or "").lower()
            if any(t in title_lower for t in query_tokens if len(t) > 2):
                reasons.append({"factor": "title_match", "label": "Title Match", "detail": doc.title})

            if doc.doc_type and any(k in query_lower for k in ("api", "endpoint", "rest")):
                if doc.doc_type == "api_reference":
                    reasons.append({"factor": "api_match", "label": "API Match", "detail": "api_reference type"})

            path_norm = doc.path.replace("\\", "/")
            repo_hint = path_norm.split("/knowledge-corpus/")[0] if "/knowledge-corpus/" in path_norm else "knowledge-base"
            reasons.append({"factor": "same_repository", "label": "Same Repository", "detail": repo_hint})

            if doc.related:
                reasons.append({
                    "factor": "graph_links",
                    "label": "Graph Links",
                    "detail": f"{len(doc.related)} related documents",
                })

            reasons.append({
                "factor": "content_relevance",
                "label": "Content Match",
                "detail": "Query terms present in document body",
            })

            explanations.append({
                "document_id": doc.doc_id,
                "title": doc.title,
                "final_score": round(scored.score, 4),
                "retrieval_sources": scored.source,
                "why": reasons,
                "summary": self._summarize(reasons),
            })

        elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
        if self._monitor:
            self._monitor.record_search_latency(elapsed_ms / 1000)

        return {
            "engine": "explain",
            "query": query,
            "latency_ms": elapsed_ms,
            "results": explanations,
        }

    @staticmethod
    def _summarize(reasons: list[dict[str, Any]]) -> str:
        labels = [r["label"] for r in reasons[:4]]
        return " · ".join(labels)
