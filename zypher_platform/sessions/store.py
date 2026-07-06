"""Conversation session store for multi-user platform use."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Session:
    id: str
    messages: list[dict[str, str]] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()


class SessionStore:
    def __init__(self, persist_dir: str = "data/platform/sessions"):
        self.dir = Path(persist_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Session] = {}

    def create(self) -> Session:
        sid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        session = Session(id=sid, created_at=now, updated_at=now)
        self._cache[sid] = session
        self._save(session)
        return session

    def get(self, session_id: str) -> Session | None:
        if session_id in self._cache:
            return self._cache[session_id]
        path = self.dir / f"{session_id}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        session = Session(**data)
        self._cache[session_id] = session
        return session

    def add_message(self, session_id: str, role: str, content: str) -> Session:
        session = self.get(session_id) or self.create()
        session.messages.append({"role": role, "content": content})
        session.touch()
        self._save(session)
        return session

    def get_messages(self, session_id: str) -> list[dict[str, str]]:
        session = self.get(session_id)
        return session.messages if session else []

    def _save(self, session: Session) -> None:
        path = self.dir / f"{session.id}.json"
        path.write_text(
            json.dumps({
                "id": session.id,
                "messages": session.messages,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }, indent=2),
            encoding="utf-8",
        )

    def list_sessions(self, limit: int = 50) -> list[dict]:
        sessions = []
        for path in sorted(self.dir.glob("*.json"), reverse=True)[:limit]:
            data = json.loads(path.read_text(encoding="utf-8"))
            sessions.append({
                "id": data["id"],
                "messages": len(data.get("messages", [])),
                "updated_at": data.get("updated_at"),
            })
        return sessions
