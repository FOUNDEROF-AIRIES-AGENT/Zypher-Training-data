"""Ask Knowledge — V1 Q&A workflow with sources, confidence, and explainability."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent


class AskKnowledge:
    def __init__(self, runtime):
        self._rt = runtime
        self._stats_path = runtime.data_dir / "usage.json"

    def ask(self, question: str) -> dict[str, Any]:
        self._rt.brain.index(force=False)
        explained = self._rt.explain.explain(question, top_k=5)
        retrieval = self._rt.brain.retrieve(question)

        sources = []
        for item in explained.get("results", []):
            confidence = min(99, max(1, int(item.get("final_score", 0) * 100)))
            sources.append({
                "document_id": item["document_id"],
                "title": item["title"],
                "confidence": confidence,
                "why": item.get("summary", ""),
                "factors": item.get("why", []),
            })

        answer = self._build_answer(question, retrieval.context, sources)

        self._record_query("ask")
        return {
            "product": "Ask Knowledge",
            "question": question,
            "answer": answer,
            "sources": sources,
            "confidence": sources[0]["confidence"] if sources else 0,
            "latency_ms": explained.get("latency_ms"),
        }

    @staticmethod
    def _build_answer(question: str, context: str, sources: list[dict]) -> str:
        if not sources or "No relevant documents" in context:
            return "I couldn't find relevant knowledge to answer that question. Try uploading sources or rephrasing your question."

        top = sources[0]
        intro = f"Based on **{top['title']}** and {len(sources) - 1} other source(s), here is what your knowledge base says:\n\n"
        excerpt = context.split("---")[0].strip()
        if len(excerpt) > 1200:
            excerpt = excerpt[:1200] + "..."
        return intro + excerpt

    def _record_query(self, kind: str) -> None:
        stats = self._load_stats()
        stats[kind] = stats.get(kind, 0) + 1
        stats["last_query_at"] = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat()
        self._stats_path.parent.mkdir(parents=True, exist_ok=True)
        self._stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    def record_search(self) -> None:
        self._record_query("searches")

    def _load_stats(self) -> dict:
        if self._stats_path.exists():
            try:
                return json.loads(self._stats_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {"searches": 0, "ask": 0}

    def usage_stats(self) -> dict[str, Any]:
        return self._load_stats()
