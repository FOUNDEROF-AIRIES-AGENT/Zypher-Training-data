"""
Zypher Brain — primary knowledge service for Zypher.

All documentation, APIs, code examples, ADRs, runbooks, and troubleshooting
live in Zypher Brain. The language model is a replaceable reasoning engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from brain.embeddings.encoder import EmbeddingEncoder
from brain.graph.relationships import GraphIndex
from brain.indexing.vector_index import VectorIndex
from brain.ingestion.loader import KnowledgeBase
from brain.memory.conversation import ConversationMemory
from brain.metadata.index import MetadataIndex
from brain.reranking.reranker import Reranker
from brain.retrieval.pipeline import RetrievalPipeline
from brain.types import RetrievalResult

BRAIN_SYSTEM_RULES = (
    "You are Zypher, an enterprise AI coding assistant.\n"
    "CRITICAL: Answer ONLY using the Zypher Brain context provided below.\n"
    "Do NOT rely on internal model knowledge when relevant context exists.\n"
    "If context is insufficient, say exactly what information is missing.\n"
    "Cite document titles when referencing specific facts."
)


class ZypherBrain:
    """
    Zypher Brain backend service:
    - Knowledge Base
    - Vector Database
    - Metadata Index
    - Graph Relationships
    - Conversation Memory
    - Retrieval Pipeline
    """

    def __init__(self, config: dict[str, Any] | None = None, config_path: str | Path = "config/brain.yaml"):
        self.config = config or self._load_config(config_path)
        self._init_components()

    @staticmethod
    def _load_config(path: str | Path) -> dict[str, Any]:
        with Path(path).open(encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _init_components(self) -> None:
        kb_cfg = self.config["knowledge_base"]
        self.kb = KnowledgeBase(
            paths=kb_cfg["paths"],
            glob_pattern=kb_cfg.get("glob", "**/*.md"),
            exclude=kb_cfg.get("exclude"),
        )

        emb_cfg = self.config.get("embeddings", {})
        self.encoder = EmbeddingEncoder(emb_cfg.get("model", "sentence-transformers/all-MiniLM-L6-v2"))

        vs_cfg = self.config.get("vector_store", {})
        self.vector_index = VectorIndex(
            self.kb,
            self.encoder,
            persist_dir=vs_cfg.get("persist_dir", "data/brain/vector_store"),
            collection_name=vs_cfg.get("collection_name", "zypher_brain"),
        )

        self.metadata_index = MetadataIndex(self.kb)

        gr_cfg = self.config.get("graph", {})
        self.graph_index = GraphIndex(
            self.kb,
            max_hops=int(gr_cfg.get("max_hops", 2)),
            max_extra=int(gr_cfg.get("max_extra_chunks", 8)),
        )

        ret_cfg = self.config.get("retrieval", {})
        self.retrieval = RetrievalPipeline(
            vector_index=self.vector_index,
            metadata_index=self.metadata_index,
            graph_index=self.graph_index,
            reranker=Reranker(ret_cfg.get("source_weights")),
            vector_top_k=int(ret_cfg.get("vector_top_k", 10)),
            metadata_top_k=int(ret_cfg.get("metadata_top_k", 8)),
            final_top_k=int(ret_cfg.get("final_top_k", 8)),
            max_context_chars=int(ret_cfg.get("max_context_chars", 14000)),
        )

        mem_cfg = self.config.get("memory", {})
        self.memory = ConversationMemory(max_turns=int(mem_cfg.get("max_turns", 20)))

        prompt = self.config.get("system_prompt", "").strip()
        base_prompt = f"{prompt}\n\n{BRAIN_SYSTEM_RULES}".strip() if prompt else BRAIN_SYSTEM_RULES
        if not self.memory.messages:
            self.memory.add("system", base_prompt)

    def index(self, force: bool = False) -> int:
        if force:
            import shutil
            if self.vector_index.persist_dir.exists():
                shutil.rmtree(self.vector_index.persist_dir)
            self.vector_index._collection = None
            self.vector_index._client = None
        if force or not self.vector_index.is_indexed:
            return self.vector_index.index()
        self.vector_index._connect()
        return self.vector_index._collection.count()

    def retrieve(self, query: str) -> RetrievalResult:
        return self.retrieval.retrieve(query)

    def build_messages(self, user_message: str, retrieval: RetrievalResult) -> list[dict[str, str]]:
        user_content = (
            f"<zypher_brain_context>\n{retrieval.context}\n</zypher_brain_context>\n\n"
            f"User question: {user_message}\n\n"
            "Answer using ONLY the Zypher Brain context above. "
            "If the context does not contain enough information, state what is missing."
        )
        return self.memory.as_list() + [{"role": "user", "content": user_content}]

    @property
    def document_count(self) -> int:
        return len(self.kb)
