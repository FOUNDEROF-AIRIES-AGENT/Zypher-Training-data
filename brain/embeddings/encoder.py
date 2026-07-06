"""Embedding generation for Zypher Brain."""

from __future__ import annotations


class EmbeddingEncoder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _ensure(self) -> None:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)

    def encode(self, texts: list[str]) -> list[list[float]]:
        self._ensure()
        return self._model.encode(texts, show_progress_bar=len(texts) > 32).tolist()

    def encode_query(self, query: str) -> list[float]:
        return self.encode([query])[0]
