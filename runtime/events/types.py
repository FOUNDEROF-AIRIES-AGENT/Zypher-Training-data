"""Event types for the Coltex event bus."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class KnowledgeEvent:
    id: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = "coltex-runtime"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
