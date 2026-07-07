"""Per-collection Coltex brain instance management."""

from __future__ import annotations

import copy
import threading
from pathlib import Path
from typing import Any

import yaml

from brain.brain import Coltex
from coltex_platform.store import Collection, PlatformStore


class BrainManager:
    """Cache and lifecycle management for tenant-scoped Coltex instances."""

    def __init__(self, store: PlatformStore, base_config_path: str = "config/brain.yaml"):
        self.store = store
        self.base_config_path = Path(base_config_path)
        self._lock = threading.RLock()
        self._instances: dict[str, Coltex] = {}

    def _config_for_collection(self, collection: Collection) -> dict[str, Any]:
        with self.base_config_path.open(encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        cfg = copy.deepcopy(cfg)
        cfg["knowledge_base"] = {
            "paths": [collection.kb_path],
            "glob": "**/*.md",
            "exclude": ["**/_seed/**", "**/generated/**"],
        }
        cfg.setdefault("vector_store", {})
        cfg["vector_store"]["persist_dir"] = collection.vector_path
        cfg["vector_store"]["collection_name"] = f"coltex_{collection.id.replace('-', '')[:16]}"
        return cfg

    def get_brain(self, collection: Collection, refresh: bool = False) -> Coltex:
        with self._lock:
            if refresh or collection.id not in self._instances:
                cfg = self._config_for_collection(collection)
                self._instances[collection.id] = Coltex(config=cfg)
            return self._instances[collection.id]

    def invalidate(self, collection_id: str) -> None:
        with self._lock:
            self._instances.pop(collection_id, None)

    def index_collection(self, collection: Collection, force: bool = False) -> dict[str, Any]:
        brain = self.get_brain(collection, refresh=True)
        count = brain.index(force=force)
        docs = self.store.list_documents(collection.id)
        indexed = sum(1 for d in docs if d.status == "indexed")
        self.store.update_collection_counts(collection.id, len(docs), indexed)
        return {"indexed_vectors": count, **brain.stats()}

    def retrieve(self, collection: Collection, query: str) -> Any:
        brain = self.get_brain(collection)
        brain.index(force=False)
        return brain.retrieve(query)
