"""Conversation memory for Zypher Brain."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ConversationMemory:
    max_turns: int = 20
    messages: list[dict[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_turns * 2 + 1:
            system = [m for m in self.messages if m["role"] == "system"]
            rest = [m for m in self.messages if m["role"] != "system"]
            self.messages = (system[:1] if system else []) + rest[-(self.max_turns * 2) :]

    def as_list(self) -> list[dict[str, str]]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()
