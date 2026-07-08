"""Runtime operational metrics — enterprise monitoring view."""

from __future__ import annotations

import os
import resource
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent


class RuntimeMonitor:
    def __init__(self, runtime):
        self._rt = runtime
        self._search_latencies: list[float] = []

    def record_search_latency(self, seconds: float) -> None:
        self._search_latencies.append(seconds)
        if len(self._search_latencies) > 100:
            self._search_latencies = self._search_latencies[-100:]

    def snapshot(self) -> dict[str, Any]:
        mem_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        if os.name != "darwin":
            mem_mb = mem_mb / 1024  # Linux reports KB

        brain_stats = self._rt.brain.stats()
        graph_stats = self._rt.graph.stats()
        event_stats = self._rt.event_bus.stats()
        health = self._rt.analytics.health()

        events_per_sec = 0.0
        log_path = Path(event_stats.get("log_path", ""))
        if log_path.exists():
            try:
                age = max(time.time() - log_path.stat().st_mtime, 1)
                events_per_sec = round(event_stats.get("total_events", 0) / age, 2)
            except OSError:
                pass

        latencies = self._search_latencies
        avg_latency = round(sum(latencies) / len(latencies) * 1000, 1) if latencies else None

        return {
            "engine": "monitor",
            "status": "active",
            "runtime": {
                "memory_mb": round(mem_mb, 1),
                "pid": os.getpid(),
                "uptime_events": event_stats.get("total_events", 0),
            },
            "knowledge": {
                "documents": brain_stats.get("documents", 0),
                "embeddings": brain_stats.get("indexed_vectors", 0),
                "graph_edges": graph_stats.get("graph_edges", 0),
                "graph_size_mb": self._dir_size_mb(ROOT / "data/product/graph"),
            },
            "pipeline": {
                "queue_depth": 0,
                "events_per_sec": events_per_sec,
                "search_latency_ms": avg_latency,
            },
            "health": {
                "knowledge_score": health.get("knowledge_score"),
                "status": health.get("status", "unknown"),
            },
        }

    @staticmethod
    def _dir_size_mb(path: Path) -> float:
        if not path.exists():
            return 0.0
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        return round(total / (1024 * 1024), 2)
