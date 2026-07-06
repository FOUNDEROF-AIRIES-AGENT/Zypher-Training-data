from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from brain import ZypherBrain
from zypher.llm.provider import LLMProvider


@dataclass
class ZypherConfig:
    brain_config_path: Path
    llm_config_path: Path
    brain_cfg: dict[str, Any]
    llm_cfg: dict[str, Any]
    brain: ZypherBrain | None = None
    llm: LLMProvider | None = None


def load_config(
    brain_path: Path | str = "config/brain.yaml",
    llm_path: Path | str = "config/llm.yaml",
) -> ZypherConfig:
    with Path(brain_path).open(encoding="utf-8") as f:
        brain_cfg = yaml.safe_load(f)
    with Path(llm_path).open(encoding="utf-8") as f:
        llm_cfg = yaml.safe_load(f)
    return ZypherConfig(Path(brain_path), Path(llm_path), brain_cfg, llm_cfg)


def create_backend(config: ZypherConfig | None = None) -> "ZypherBackend":
    from zypher.backend import ZypherBackend

    return ZypherBackend(config)
