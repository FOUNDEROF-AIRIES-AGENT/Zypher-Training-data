"""Knowledge Studio — unified product surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent


class KnowledgeStudio:
    """
    Knowledge Studio modules (all available via API/CLI today):

    Explorer · Search · Graph · Analytics · Curator · Lifecycle · Plugins · Settings
    """

    MODULES = [
        "explorer", "search", "graph", "analytics", "curator",
        "lifecycle", "plugins", "settings", "monitor", "explain",
    ]

    def __init__(self, runtime):
        self._rt = runtime
        self._alerts_path = runtime.data_dir / "curator" / "alerts.json"
        self._alerts_path.parent.mkdir(parents=True, exist_ok=True)

    def dashboard(self) -> dict[str, Any]:
        health = self._rt.analytics.health()
        curator = self._rt.curator.proactive_scan(save=False)
        monitor = self._rt.monitor.snapshot()
        return {
            "studio": "Knowledge Studio",
            "status": "active",
            "modules": self.MODULES,
            "health": health,
            "curator_alerts": curator.get("alerts", [])[:10],
            "monitor": monitor,
            "connectors": self._rt.connectors.list_connectors(),
            "memory": self._rt.memory.stats(),
        }

    def explorer(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        docs = self._rt.brain.kb.documents[offset : offset + limit]
        return {
            "module": "explorer",
            "total": len(self._rt.brain.kb.documents),
            "offset": offset,
            "limit": limit,
            "objects": [
                {
                    **self._rt.knowledge_dna(d.doc_id),
                    "title": d.title,
                    "memory_tier": self._rt.memory.resolve_tier(d),
                    "evolution": self._rt.memory.evolution_state(d),
                }
                for d in docs
            ],
        }

    def lifecycle(self, document_id: str | None = None) -> dict[str, Any]:
        from runtime.knowledge.evolution import load_evolution_config

        cfg = load_evolution_config()
        if document_id:
            dna = self._rt.knowledge_dna(document_id)
            return {"module": "lifecycle", "document": dna, "allowed_transitions": cfg.get("transitions", {}).get(dna.get("evolution_state", "v1"), [])}
        return {"module": "lifecycle", "states": cfg.get("states", []), "transitions": cfg.get("transitions", {})}

    def settings(self) -> dict[str, Any]:
        return {
            "module": "settings",
            "runtime_config": str(self._rt.config_path),
            "brain_config": self._rt.config.get("brain_config"),
            "event_log": self._rt.config.get("runtime", {}).get("event_log"),
            "plugins": self._rt.plugins.stats(),
        }

    def save_alerts(self, alerts: list[dict[str, Any]]) -> None:
        self._alerts_path.write_text(json.dumps({"alerts": alerts}, indent=2), encoding="utf-8")

    def load_alerts(self) -> list[dict[str, Any]]:
        if not self._alerts_path.exists():
            return []
        try:
            return json.loads(self._alerts_path.read_text(encoding="utf-8")).get("alerts", [])
        except (json.JSONDecodeError, OSError):
            return []
