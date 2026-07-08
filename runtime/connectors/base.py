"""Connector base and registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent


class Connector(ABC):
    id: str = "base"
    name: str = "Base Connector"

    @abstractmethod
    def sync(self) -> dict[str, Any]:
        """Pull from source and return ingest payloads."""


class ConnectorRegistry:
    def __init__(self):
        self._connectors: dict[str, Connector] = {}

    def register(self, connector: Connector) -> None:
        self._connectors[connector.id] = connector

    def list_connectors(self) -> list[dict[str, str]]:
        return [{"id": c.id, "name": c.name} for c in self._connectors.values()]

    def sync(self, connector_id: str) -> dict[str, Any]:
        if connector_id not in self._connectors:
            return {"error": f"unknown connector: {connector_id}"}
        return self._connectors[connector_id].sync()
