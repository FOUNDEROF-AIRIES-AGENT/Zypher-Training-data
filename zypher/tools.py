from __future__ import annotations

import json
from typing import Any, Callable

from brain import ZypherBrain

ToolFn = Callable[[dict[str, Any]], str]


class ToolRegistry:
    """Tool-calling registry — delegates knowledge search to Zypher Brain."""

    def __init__(self) -> None:
        self._tools: dict[str, tuple[str, ToolFn]] = {}

    def register(self, name: str, description: str, fn: ToolFn) -> None:
        self._tools[name] = (description, fn)

    def list_tools(self) -> list[dict[str, str]]:
        return [{"name": n, "description": d} for n, (d, _) in self._tools.items()]

    def run(self, name: str, arguments: dict[str, Any]) -> str:
        if name not in self._tools:
            return json.dumps({"error": f"Unknown tool: {name}"})
        _, fn = self._tools[name]
        return fn(arguments)

    @staticmethod
    def default(brain: ZypherBrain) -> "ToolRegistry":
        reg = ToolRegistry()

        def search_docs(args: dict[str, Any]) -> str:
            query = args.get("query", "")
            result = brain.retrieve(query)
            return json.dumps({
                "status": "ok",
                "documents": len(result.documents),
                "context_preview": result.context[:2000],
            })

        reg.register(
            "search_zypher_brain",
            "Search Zypher Brain for documentation, APIs, runbooks, and code examples",
            search_docs,
        )
        return reg
