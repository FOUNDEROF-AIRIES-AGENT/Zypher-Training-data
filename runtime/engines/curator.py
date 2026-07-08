"""AI Curator — proactive knowledge improvement."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from runtime.knowledge.dna import KnowledgeDNA


class CuratorEngine:
    """Proactively surfaces: duplicates, outdated docs, regen needs, poor quality, disconnects."""

    def __init__(self, brain, event_bus, data_dir: Path):
        self._brain = brain
        self._bus = event_bus
        self._alerts_path = data_dir / "curator" / "alerts.json"
        self._alerts_path.parent.mkdir(parents=True, exist_ok=True)

    def proactive_scan(self, *, save: bool = True) -> dict[str, Any]:
        alerts = self._build_alerts()
        if save:
            self._alerts_path.write_text(json.dumps({"alerts": alerts}, indent=2), encoding="utf-8")
            for alert in alerts[:5]:
                self._bus.emit(f"curator.{alert['type']}", alert)
        return {
            "engine": "curator",
            "status": "active",
            "mode": "proactive",
            "alert_count": len(alerts),
            "alerts": alerts,
        }

    def recommend(self) -> dict[str, Any]:
        return self.proactive_scan(save=True)

    def _build_alerts(self) -> list[dict[str, Any]]:
        docs = list(self._brain.kb.documents)
        ids = {d.doc_id for d in docs}
        alerts: list[dict[str, Any]] = []

        # Duplicate documents
        title_map: dict[str, list[str]] = {}
        for doc in docs:
            key = (doc.title or "").strip().lower()
            if key:
                title_map.setdefault(key, []).append(doc.doc_id)
        dup_groups = [ids for ids in title_map.values() if len(ids) > 1]
        if dup_groups:
            total = sum(len(g) for g in dup_groups)
            alerts.append({
                "type": "duplicate",
                "severity": "high",
                "title": "Duplicate documents detected",
                "message": f"{total} documents across {len(dup_groups)} duplicate groups should be merged.",
                "action": "Review merge candidates in Knowledge Studio → Curator",
                "groups": len(dup_groups),
            })

        # Low quality chunks
        low_q = [d.doc_id for d in docs if KnowledgeDNA.from_document(d).quality_score < 0.45]
        if low_q:
            alerts.append({
                "type": "low_quality",
                "severity": "high",
                "title": "Poor quality chunks",
                "message": f"{len(low_q)} documents have low quality scores — review or regenerate content.",
                "action": "Open affected documents in Explorer and improve or archive",
                "count": len(low_q),
            })

        # Outdated API documentation
        outdated_api = [
            d.doc_id for d in docs
            if d.doc_type == "api_reference" and len(d.content or "") < 120
        ]
        if outdated_api:
            alerts.append({
                "type": "outdated",
                "severity": "medium",
                "title": "API documentation may be outdated",
                "message": f"{len(outdated_api)} API reference documents are unusually short or incomplete.",
                "action": "Regenerate or expand API docs via AI Knowledge Builder",
                "count": len(outdated_api),
            })

        # Embedding regeneration
        indexed = self._brain.stats().get("indexed_vectors", 0)
        if indexed < len(docs) * 0.9:
            alerts.append({
                "type": "embedding_regen",
                "severity": "high",
                "title": "Embeddings should be regenerated",
                "message": f"Only {indexed}/{len(docs)} documents indexed — run `make index` to refresh vectors.",
                "action": "make index",
            })

        # Disconnected graph
        disconnected = sum(
            1 for d in docs if not d.related and not any(d.relationships.values())
        )
        if disconnected > 0:
            alerts.append({
                "type": "disconnected_graph",
                "severity": "medium",
                "title": "Disconnected graph nodes",
                "message": f"{disconnected} documents have no graph relationships — connect them to improve retrieval.",
                "action": "Add see_also / depends_on links in Knowledge Studio → Graph",
                "count": disconnected,
            })

        # Broken references
        broken = sum(
            1 for d in docs for ref in (d.related or [])
            if ref not in ids
        )
        if broken > 0:
            alerts.append({
                "type": "broken_reference",
                "severity": "high",
                "title": "Broken references",
                "message": f"{broken} broken see_also / related references found — fix or remove stale links.",
                "action": "Run scheduler broken_link_scan or fix in Explorer",
                "count": broken,
            })

        return alerts

    def stats(self) -> dict[str, Any]:
        alerts = self._build_alerts()
        return {
            "engine": "curator",
            "status": "active",
            "alert_count": len(alerts),
        }
