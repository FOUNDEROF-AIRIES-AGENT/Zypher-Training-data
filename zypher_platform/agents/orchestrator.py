"""Multi-agent orchestration over Zypher Brain (tool-calling ready)."""

from __future__ import annotations

from typing import Any, Callable


class AgentOrchestrator:
    """
    Orchestrates reasoning + tool use against Zypher Brain.

    Future: multi-agent workflows, specialist agents, handoffs.
    """

    def __init__(self, brain, tools=None, max_rounds: int = 3):
        self.brain = brain
        self.tools = tools
        self.max_rounds = max_rounds

    def run(self, query: str, generate_fn: Callable[[list[dict[str, str]]], str]) -> dict[str, Any]:
        retrieval = self.brain.retrieve(query)
        messages = self.brain.build_messages(query, retrieval)
        tool_results: list[dict] = []

        if self.tools and "search" in query.lower():
            result = self.tools.run("search_zypher_brain", {"query": query})
            tool_results.append({"tool": "search_zypher_brain", "result": result})

        if retrieval.has_context:
            answer = generate_fn(messages)
        else:
            answer = (
                "No relevant Zypher Brain documents found. "
                "Ingest documentation via POST /v1/documents first."
            )

        return {
            "answer": answer,
            "sources": [
                {
                    "title": s.document.title,
                    "path": s.document.path,
                    "score": s.score,
                    "source": s.source,
                }
                for s in retrieval.documents
            ],
            "tool_results": tool_results,
            "agent": "zypher-primary",
        }
