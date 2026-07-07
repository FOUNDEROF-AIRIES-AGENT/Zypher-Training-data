"""API gateway — runtime status and engine endpoints."""

from __future__ import annotations

from typing import Any


class APIGateway:
    def __init__(self, runtime):
        self._runtime = runtime

    def status(self) -> dict[str, Any]:
        return self._runtime.status()

    def health(self) -> dict[str, Any]:
        return self._runtime.analytics.health()
