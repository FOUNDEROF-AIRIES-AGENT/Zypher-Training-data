"""Scheduler engine — automated knowledge maintenance jobs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent


class SchedulerEngine:
    def __init__(self, config_path: str | Path = "config/scheduler.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = ROOT / self.config_path
        self._config = self._load()

    def _load(self) -> dict[str, Any]:
        if self.config_path.exists():
            with self.config_path.open(encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def list_jobs(self) -> list[dict[str, Any]]:
        return list(self._config.get("jobs", []))

    def stats(self) -> dict[str, Any]:
        jobs = self.list_jobs()
        return {
            "engine": "scheduler",
            "status": "active",
            "scheduled_jobs": len(jobs),
            "manual_jobs": len(self._config.get("manual_jobs", [])),
        }
