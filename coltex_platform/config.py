"""Platform configuration loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "config" / "platform.yaml"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_CONFIG
    if not cfg_path.exists():
        return _defaults()
    with cfg_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    merged = _defaults()
    _deep_merge(merged, data)
    return merged


def _defaults() -> dict[str, Any]:
    return {
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "workers": 1,
            "cors_origins": ["*"],
            "public_url": "http://localhost:8080",
        },
        "auth": {
            "jwt_secret": "coltex-dev-secret-change-in-production",
            "jwt_expiry_hours": 24,
            "api_key_prefix": "ctx_",
        },
        "storage": {
            "data_dir": "data/platform",
            "sqlite_path": "data/platform/coltex.db",
        },
        "brain": {
            "config_path": "config/brain.yaml",
            "default_collection": "default",
        },
        "llm": {
            "provider": "mock",
            "model": "coltex-rag-v1",
            "openai_base_url": "https://api.openai.com/v1",
            "openai_api_key_env": "OPENAI_API_KEY",
            "max_tokens": 2048,
            "temperature": 0.2,
        },
        "ingestion": {
            "max_upload_bytes": 52_428_800,
            "allowed_extensions": [".md", ".txt", ".json", ".csv", ".html", ".pdf"],
            "chunk_size": 1200,
            "chunk_overlap": 150,
        },
        "jobs": {
            "max_concurrent": 4,
            "poll_interval_seconds": 2,
        },
        "rate_limits": {
            "requests_per_minute": 120,
            "retrieve_per_minute": 60,
            "chat_per_minute": 30,
        },
        "tiers": {
            "free": {"collections": 1, "documents": 1000, "queries_per_day": 500},
            "starter": {"collections": 5, "documents": 25_000, "queries_per_day": 10_000},
            "professional": {"collections": 25, "documents": 250_000, "queries_per_day": 100_000},
            "enterprise": {"collections": -1, "documents": -1, "queries_per_day": -1},
        },
    }


def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
