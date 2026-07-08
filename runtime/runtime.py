"""
Coltex Runtime — the live Knowledge Operating System.

Orchestrates intelligence, search, memory, graph, retrieval, events,
scheduler, plugins, curator, analytics, security, studio, and monitoring.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from brain.brain import Coltex
from runtime.api.gateway import APIGateway
from runtime.connectors.base import ConnectorRegistry
from runtime.connectors.filesystem import FilesystemConnector
from runtime.connectors.github import GitHubConnector
from runtime.engines.analytics import AnalyticsEngine
from runtime.engines.curator import CuratorEngine
from runtime.engines.explain import ExplainEngine
from runtime.engines.graph import GraphEngine
from runtime.engines.intelligence import IntelligenceEngine
from runtime.engines.memory import MemoryEngine
from runtime.engines.retrieval import RetrievalEngine
from runtime.engines.scheduler import SchedulerEngine
from runtime.engines.search import SearchEngine
from runtime.events.bus import EventBus
from runtime.knowledge.dna import KnowledgeDNA
from runtime.monitoring.metrics import RuntimeMonitor
from runtime.plugins import sdk as plugin_sdk
from runtime.plugins.manager import PluginManager
from runtime.security.gateway import SecurityGateway
from runtime.studio.studio import KnowledgeStudio

ROOT = Path(__file__).resolve().parent.parent


class ColtexRuntime:
    """Coltex Runtime — platform centerpiece with Knowledge Studio."""

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

        self.monitor = RuntimeMonitor(self)
        self.intelligence = IntelligenceEngine(self.brain, self.event_bus)
        self.search = SearchEngine(self.brain)
        self.memory = MemoryEngine(self.brain)
        self.scheduler = SchedulerEngine()
        self.plugins = PluginManager()
        plugin_sdk.init(self.plugins)
        self.retrieval = RetrievalEngine(self.brain)
        self.graph = GraphEngine(self.brain)
        self.curator = CuratorEngine(self.brain, self.event_bus, self.data_dir)
        self.analytics = AnalyticsEngine(self.brain)
        self.explain = ExplainEngine(self.brain, self.monitor)
        self.security = SecurityGateway()
        self.api = APIGateway(self)
        self.studio = KnowledgeStudio(self)

        self.connectors = ConnectorRegistry()
        self.connectors.register(FilesystemConnector())
        self.connectors.register(GitHubConnector())

        self._wire_default_subscribers()

    @staticmethod
    def _load_config(path: Path | None = None) -> dict[str, Any]:
        cfg_path = path or ROOT / "config/runtime.yaml"
        with cfg_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _wire_default_subscribers(self) -> None:
        def on_pipeline_complete(event):
            if event.id == "analytics.updated":
                self.curator.proactive_scan(save=True)

        self.event_bus.subscribe("analytics.updated", on_pipeline_complete)

    def status(self) -> dict[str, Any]:
        return {
            "runtime": "coltex-runtime",
            "version": self.config.get("version", "1.0.0"),
            "platform": "Knowledge Operating System for AI",
            "use_today": {
                "knowledge_studio": "python3 -m runtime studio",
                "health_dashboard": "python3 -m runtime health",
                "ai_curator": "python3 -m runtime curator",
                "monitoring": "python3 -m runtime monitor",
                "explainability": "python3 -m runtime explain \"query\"",
                "connectors": "python3 -m runtime connector filesystem",
                "search": "python3 -m runtime search \"query\"",
            },
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
                "monitor": {"status": "active"},
                "explain": {"status": "active"},
                "security": self.security.stats(),
            },
            "knowledge_studio": {
                **self.config.get("knowledge_studio", {}),
                "status": "active",
                "command": "python3 -m runtime studio",
            },
        }

    def ingest(self, document_id: str, source: str = "upload") -> dict[str, Any]:
        if not self.security.authorize("ingest"):
            return {"error": "unauthorized"}
        payload = {"document_id": document_id, "source": source}
        events = self.event_bus.run_pipeline(payload)
        curator = self.curator.proactive_scan(save=True)
        return {
            "document_id": document_id,
            "pipeline_events": [e.id for e in events],
            "subscribers_notified": True,
            "curator_alerts": curator.get("alert_count", 0),
        }

    def sync_connector(self, connector_id: str) -> dict[str, Any]:
        result = self.connectors.sync(connector_id)
        if "ingest_payloads" in result:
            for item in result["ingest_payloads"][:5]:
                self.ingest(item["document_id"], source=connector_id)
        return result

    def knowledge_dna(self, document_id: str) -> dict[str, Any]:
        for doc in self.brain.kb.documents:
            if doc.doc_id == document_id:
                dna = KnowledgeDNA.from_document(doc)
                data = dna.to_dict()
                data["memory_tier"] = self.memory.resolve_tier(doc)
                data["evolution_state"] = self.memory.evolution_state(doc)
                return data
        return {"error": "not_found", "document_id": document_id}

    def knowledge_objects(self, limit: int = 10) -> list[dict[str, Any]]:
        return [self.knowledge_dna(d.doc_id) for d in self.brain.kb.documents[:limit]]
