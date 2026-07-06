"""Zypher Brain — permanent knowledge layer for Zypher."""

from brain.brain import ZypherBrain, BRAIN_SYSTEM_RULES
from brain.types import Document, RetrievalResult, ScoredDocument

__version__ = "1.0.0"
__all__ = [
    "ZypherBrain",
    "BRAIN_SYSTEM_RULES",
    "Document",
    "RetrievalResult",
    "ScoredDocument",
]
