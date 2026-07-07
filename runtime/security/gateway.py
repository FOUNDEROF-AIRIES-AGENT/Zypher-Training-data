"""Security gateway — access and audit stubs."""

from __future__ import annotations

from typing import Any


class SecurityGateway:
    def stats(self) -> dict[str, Any]:
        return {"engine": "security", "status": "active", "mode": "local"}

    def authorize(self, action: str, actor: str = "system") -> bool:
        return True
