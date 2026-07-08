"""V1 workspace settings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent


class SettingsStore:
    def __init__(self, path: str = "data/runtime/settings.json", defaults_path: str = "config/v1.yaml"):
        self.path = ROOT / path
        self.defaults_path = ROOT / defaults_path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        defaults = self._defaults()
        if self.path.exists():
            try:
                saved = json.loads(self.path.read_text(encoding="utf-8"))
                return {**defaults, **saved}
            except (json.JSONDecodeError, OSError):
                pass
        return defaults

    def save(self, updates: dict[str, Any]) -> dict[str, Any]:
        current = self.load()
        current.update(updates)
        self.path.write_text(json.dumps(current, indent=2), encoding="utf-8")
        return current

    def _defaults(self) -> dict[str, Any]:
        if self.defaults_path.exists():
            cfg = yaml.safe_load(self.defaults_path.read_text(encoding="utf-8"))
            return dict(cfg.get("settings", {}).get("defaults", {}))
        return {
            "workspace": "default",
            "ai_provider": "local",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chunk_size": 2000,
            "users": 1,
            "backup_enabled": False,
        }
