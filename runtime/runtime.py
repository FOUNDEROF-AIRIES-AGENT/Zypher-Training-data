"""
Coltex Runtime — the live Knowledge Operating System.

Orchestrates intelligence, search, memory, graph, retrieval, events,
scheduler, plugins, curator, analytics, security, and API gateway.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from brain.brain import Coltex
from runtime.api.gateway import APIGateway
from runtime.engines.analytics import AnalyticsEngine
from runtime.engines.curator import CuratorEngine
from runtime.engines.graph import GraphEngine
from runtime.engines.intelligence import IntelligenceEngine
from runtime.engines.memory import MemoryEngine
from runtime.engines.retrieval import RetrievalEngine
from runtime.engines.scheduler import SchedulerEngine
from runtime.engines.search import SearchEngine
from runtime.events.bus import EventBus
from runtime.knowledge.dna import KnowledgeDNA
from runtime.plugins.manager import PluginManager
from runtime.security.gateway import SecurityGateway

ROOT = Path(__file__).resolve().parent.parent


class ColtexRuntime:
    """
    Coltex Runtime — platform centerpiece.

    ├── Intelligence Engine
    ├── Search Engine
    ├── Memory Engine
    ├── Scheduler
    ├── Event Bus
    ├── Plugin Manager
    ├── Knowledge Studio (API)
    ├── Retrieval Engine
    ├── Graph Engine
    ├── AI Curator
    ├── Analytics Engine
    ├── API Gateway
    └── Security
    """

    def __init__(self, config_path: str | Path = "config/runtime.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = ROOT / self.config_path
        self.config = self._load_config()
        self.data_dir = ROOT / self.config.get("runtime", {}).get("data_dir", "data/runtime")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        brain_cfg = self.config.get("brain_config", "config/brain.yaml")
        self.brain = Coltex(config_path=brain_cfg)

        log_path = self.config.get("runtime", {}).get("event_log", "data/runtime/events.jsonl")
        self.event_bus = EventBus(log_path=log_path)

        self.intelligence = IntelligenceEngine(self.brain, self.event_bus)
        self.search = SearchEngine(self.brain)
        self.memory = MemoryEngine(self.brain)
        self.scheduler = SchedulerEngine()
        self.plugins = PluginManager()
        self.retrieval = RetrievalEngine(self.brain)
        self.graph = GraphEngine(self.brain)
        self.curator = CuratorEngine(self.brain, self.event_bus)
        self.analytics = AnalyticsEngine(self.brain)
        self.security = SecurityGateway()
        self.api = APIGateway(self)

        self._wire_default_subscribers()

    @staticmethod
    def _load_config(path: Path | None = None) -> dict[str, Any]:
        cfg_path = path or ROOT / "config/runtime.yaml"
        with cfg_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _wire_default_subscribers(self) -> None:
        self.event_bus.subscribe("health.rescored", lambda _: None)
        self.event_bus.subscribe("analytics.updated", lambda _: None)

    def status(self) -> dict[str, Any]:
        return {
            "runtime": "coltex-runtime",
            "version": self.config.get("version", "1.0.0"),
            "platform": "Knowledge Operating System for AI",
            "engines": {
                "intelligence": self.intelligence.stats(),
                "search": self.search.stats(),
                "memory": self.memory.stats(),
                "scheduler": self.scheduler.stats(),
                "event_bus": self.event_bus.stats(),
                "plugins": self.plugins.stats(),
                "retrieval": self.retrieval.stats(),
                "graph": self.graph.stats(),
                "curator": self.curator.stats(),
                "analytics": self.analytics.stats(),
                "security": self.security.stats(),
            },
            "knowledge_studio": self.config.get("knowledge_studio", {}),
        }

    def ingest(self, document_id: str, source: str = "upload") -> dict[str, Any]:
        """Run event-driven ingest pipeline for a knowledge object."""
        if not self.security.authorize("ingest"):
            return {"error": "unauthorized"}
        payload = {"document_id": document_id, "source": source}
        events = self.event_bus.run_pipeline(payload)
        return {
            "document_id": document_id,
            "pipeline_events": [e.id for e in events],
            "subscribers_notified": True,
        }

    def knowledge_dna(self, document_id: str) -> dict[str, Any]:
        for doc in self.brain.kb.documents:
            if doc.doc_id == document_id:
                return KnowledgeDNA.from_document(doc).to_dict()
        return {"error": "not_found", "document_id": document_id}

    def knowledge_objects(self, limit: int = 10) -> list[dict[str, Any]]:
        return [
            KnowledgeDNA.from_document(d).to_dict()
            for d in self.brain.kb.documents[:limit]
        ]
