"""
Zypher backend — Zypher Brain (knowledge) + LLM (reasoning engine).

The language model never answers from internal knowledge alone when
relevant Zypher Brain documents exist.
"""

from __future__ import annotations

from brain import ZypherBrain
from zypher.config import ZypherConfig, load_config
from zypher.llm.provider import LLMProvider
from zypher.tools import ToolRegistry


class ZypherBackend:
    def __init__(self, config: ZypherConfig | None = None):
        self.config = config or load_config()
        self.brain = ZypherBrain(config=self.config.brain_cfg)
        self.llm = LLMProvider.from_config(self.config.llm_cfg)
        tools_cfg = self.config.brain_cfg.get("tools", {})
        self.tools = ToolRegistry.default(self.brain) if tools_cfg.get("enabled", True) else None

    @property
    def kb(self):
        """Backward-compatible access to knowledge base."""
        return self.brain.kb

    def index_knowledge_base(self, force: bool = False) -> int:
        return self.brain.index(force=force)

    def retrieve(self, query: str):
        return self.brain.retrieve(query)

    def chat(self, user_message: str) -> str:
        retrieval = self.brain.retrieve(user_message)
        messages = self.brain.build_messages(user_message, retrieval)
        reply = self.llm.generate(messages)
        self.brain.memory.add("user", user_message)
        self.brain.memory.add("assistant", reply)
        return reply
