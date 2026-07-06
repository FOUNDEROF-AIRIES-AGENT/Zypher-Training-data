"""Backward-compatible re-exports — use brain.ingestion.loader instead."""

from brain.ingestion.loader import KnowledgeBase, parse_markdown
from brain.types import Document

__all__ = ["Document", "KnowledgeBase", "parse_markdown"]
