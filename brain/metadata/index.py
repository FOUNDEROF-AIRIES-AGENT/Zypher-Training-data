"""Metadata filter search over Zypher Brain documents."""

from __future__ import annotations

import re

from brain.ingestion.loader import KnowledgeBase, SUPPORTED_DOC_TYPES
from brain.types import Document, ScoredDocument

DOC_TYPE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "api_reference": ("api", "endpoint", "rest", "graphql", "openapi"),
    "runbook": ("runbook", "oncall", "incident", "playbook", "escalation"),
    "architecture_decision": ("adr", "architecture decision", "trade-off", "decision"),
    "troubleshooting": ("troubleshoot", "debug", "fix", "error", "issue"),
    "faq": ("faq", "what is", "how do", "why"),
    "sql_example": ("sql", "query", "select", "postgres", "mysql"),
    "database_schema": ("schema", "table", "ddl", "migration"),
    "code_walkthrough": ("code", "example", "implementation", "snippet"),
    "incident_report": ("incident", "outage", "postmortem", "root cause"),
    "design_document": ("design", "spec", "proposal"),
    "migration_guide": ("migrate", "migration", "upgrade", "deploy"),
}


class MetadataIndex:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self._by_type: dict[str, list[Document]] = {}
        self._by_category: dict[str, list[Document]] = {}
        self._by_hub: dict[str, list[Document]] = {}
        self._build()

    def _build(self) -> None:
        for doc in self.kb.documents:
            if doc.doc_type:
                self._by_type.setdefault(doc.doc_type, []).append(doc)
            if doc.category:
                self._by_category.setdefault(doc.category, []).append(doc)
            if doc.hub:
                self._by_hub.setdefault(doc.hub, []).append(doc)

    def _infer_doc_types(self, query: str) -> list[str]:
        q = query.lower()
        matched = [dt for dt, kws in DOC_TYPE_KEYWORDS.items() if any(k in q for k in kws)]
        return matched or list(SUPPORTED_DOC_TYPES)[:5]

    def search(self, query: str, top_k: int = 8) -> list[ScoredDocument]:
        tokens = set(re.findall(r"[a-z0-9_]+", query.lower()))
        target_types = set(self._infer_doc_types(query))
        scored: list[ScoredDocument] = []

        for doc in self.kb.documents:
            score = 0.0
            if doc.doc_type in target_types:
                score += 0.4
            title_tokens = set(re.findall(r"[a-z0-9_]+", doc.title.lower()))
            tag_tokens = set(t.lower() for t in doc.tags)
            overlap = len(tokens & (title_tokens | tag_tokens))
            score += min(0.5, overlap * 0.1)
            if doc.category and doc.category.lower() in query.lower():
                score += 0.2
            if doc.hub and doc.hub.replace("_", " ") in query.lower():
                score += 0.3
            if score > 0.15:
                scored.append(ScoredDocument(document=doc, score=score, source="metadata"))

        scored.sort(key=lambda s: s.score, reverse=True)
        return scored[:top_k]
