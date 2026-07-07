"""Event-driven knowledge pipeline."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable

import yaml

from runtime.events.types import KnowledgeEvent

ROOT = Path(__file__).resolve().parent.parent.parent

Handler = Callable[[KnowledgeEvent], None]

# Pipeline cascade: each event triggers the next
PIPELINE_CHAIN = [
    "document.uploaded",
    "chunk.created",
    "embedding.generated",
    "graph.updated",
    "search.index.updated",
    "health.rescored",
    "analytics.updated",
]


class EventBus:
    """In-process event bus with pipeline propagation and subscriber notification."""

    def __init__(self, config_path: str | Path = "config/events.yaml", log_path: str | Path | None = None):
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = ROOT / self.config_path
        self.log_path = Path(log_path or ROOT / "data/runtime/events.jsonl")
        self._subscribers: dict[str, list[Handler]] = defaultdict(list)
        self._history: list[KnowledgeEvent] = []
        self._config = self._load_config()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict[str, Any]:
        if self.config_path.exists():
            with self.config_path.open(encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def subscribe(self, event_id: str, handler: Handler) -> None:
        self._subscribers[event_id].append(handler)

    def emit(self, event_id: str, payload: dict[str, Any] | None = None, *, cascade: bool = False) -> KnowledgeEvent:
        event = KnowledgeEvent(id=event_id, payload=payload or {})
        self._history.append(event)
        self._append_log(event)
        for handler in self._subscribers[event_id]:
            handler(event)
        for handler in self._subscribers["*"]:
            handler(event)
        if cascade and event_id in PIPELINE_CHAIN:
            idx = PIPELINE_CHAIN.index(event_id)
            if idx + 1 < len(PIPELINE_CHAIN):
                next_id = PIPELINE_CHAIN[idx + 1]
                self.emit(next_id, {**event.payload, "triggered_by": event_id}, cascade=True)
        return event

    def run_pipeline(self, payload: dict[str, Any] | None = None) -> list[KnowledgeEvent]:
        """Run full ingest pipeline from document.uploaded through analytics.updated."""
        events: list[KnowledgeEvent] = []
        data = payload or {}
        for event_id in PIPELINE_CHAIN:
            events.append(self.emit(event_id, {**data, "pipeline_step": event_id}, cascade=False))
        self._notify_subscribers(events[-1])
        return events

    def _notify_subscribers(self, final_event: KnowledgeEvent) -> None:
        notify = KnowledgeEvent(
            id="subscribers.notified",
            payload={"last_event": final_event.id, "count": len(self._history)},
        )
        self._history.append(notify)
        self._append_log(notify)
        for handler in self._subscribers["subscribers.notified"]:
            handler(notify)

    def _append_log(self, event: KnowledgeEvent) -> None:
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

    @property
    def recent(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self._history[-20:]]

    def stats(self) -> dict[str, Any]:
        counts: dict[str, int] = defaultdict(int)
        for e in self._history:
            counts[e.id] += 1
        return {
            "total_events": len(self._history),
            "by_type": dict(counts),
            "subscribers": {k: len(v) for k, v in self._subscribers.items()},
            "log_path": str(self.log_path),
        }
