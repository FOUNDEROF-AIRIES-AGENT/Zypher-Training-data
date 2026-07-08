"""Knowledge source upload and registration."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent

SUPPORTED = {".pdf", ".docx", ".md", ".markdown", ".txt", ".html", ".htm", ".json"}


class SourceManager:
    def __init__(self, inbox_dir: str = "data/sources/inbox", processed_dir: str = "knowledge-base/uploads"):
        self.inbox = ROOT / inbox_dir
        self.processed = ROOT / processed_dir
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.processed.mkdir(parents=True, exist_ok=True)

    def list_sources(self) -> list[dict[str, Any]]:
        sources = []
        for directory in (self.inbox, self.processed):
            for path in sorted(directory.rglob("*")):
                if path.is_file() and path.suffix.lower() in SUPPORTED:
                    sources.append({
                        "name": path.name,
                        "format": path.suffix.lstrip(".").lower(),
                        "path": str(path.relative_to(ROOT)),
                        "size_bytes": path.stat().st_size,
                        "status": "inbox" if "inbox" in str(path) else "processed",
                    })
        return sources

    def upload(self, source_path: Path) -> dict[str, Any]:
        source_path = Path(source_path)
        if not source_path.exists():
            return {"error": "file not found", "path": str(source_path)}
        if source_path.suffix.lower() not in SUPPORTED:
            return {"error": "unsupported format", "supported": sorted(SUPPORTED)}

        dest = self.inbox / source_path.name
        if source_path.resolve() != dest.resolve():
            shutil.copy2(source_path, dest)

        return {
            "status": "uploaded",
            "name": dest.name,
            "format": dest.suffix.lstrip(".").lower(),
            "path": str(dest.relative_to(ROOT)),
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }

    def count(self) -> int:
        return len(self.list_sources())
