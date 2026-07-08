"""Filesystem connector — sync markdown from a directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime.connectors.base import Connector, ROOT


class FilesystemConnector(Connector):
    id = "filesystem"
    name = "Filesystem"

    def __init__(self, watch_path: str | Path = "knowledge-base", glob: str = "**/*.md"):
        self.watch_path = Path(watch_path)
        if not self.watch_path.is_absolute():
            self.watch_path = ROOT / self.watch_path
        self.glob = glob

    def sync(self) -> dict[str, Any]:
        if not self.watch_path.exists():
            return {"connector": self.id, "error": "path not found", "path": str(self.watch_path)}

        files = list(self.watch_path.glob(self.glob))[:500]
        payloads = []
        for f in files:
            if "_excluded_from_distribution" in str(f) or "/generated/" in str(f).replace("\\", "/"):
                continue
            doc_id = f.stem.upper().replace("-", "_")[:64]
            payloads.append({
                "document_id": doc_id,
                "source": "filesystem",
                "path": str(f.relative_to(ROOT)),
            })

        return {
            "connector": self.id,
            "status": "synced",
            "files_found": len(files),
            "ingest_payloads": payloads[:20],
            "total_ready": len(payloads),
        }
