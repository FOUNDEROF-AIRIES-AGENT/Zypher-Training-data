"""Knowledge evolution states."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent


def load_evolution_config(path: str | Path = "config/knowledge-evolution.yaml") -> dict[str, Any]:
    cfg_path = Path(path)
    if not cfg_path.is_absolute():
        cfg_path = ROOT / cfg_path
    with cfg_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def allowed_transitions(state: str, config: dict[str, Any] | None = None) -> list[str]:
    cfg = config or load_evolution_config()
    return list(cfg.get("transitions", {}).get(state, []))
