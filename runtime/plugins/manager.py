"""Plugin manager — extensibility registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent


class PluginManager:
    def __init__(self, config_path: str | Path = "config/extensibility.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.is_absolute():
            self.config_path = ROOT / self.config_path
        self._config = self._load()
        self._registered: dict[str, Callable] = {}

    def _load(self) -> dict[str, Any]:
        if self.config_path.exists():
            with self.config_path.open(encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def register(self, plugin_id: str, handler: Callable) -> None:
        self._registered[plugin_id] = handler

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "plugins",
            "status": "active",
            "plugin_types": len(self._config.get("plugin_types", [])),
            "registered": list(self._registered.keys()),
            "hook_points": self._config.get("hook_points", []),
        }
