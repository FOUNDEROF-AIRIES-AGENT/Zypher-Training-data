"""Vector index for semantic search."""

from __future__ import annotations

import hashlib
from pathlib import Path

from brain.embeddings.encoder import EmbeddingEncoder
from brain.ingestion.loader import KnowledgeBase
from brain.types import Document, ScoredDocument


class VectorIndex:
    def __init__(
        self,
        kb: KnowledgeBase,
        encoder: EmbeddingEncoder,
        persist_dir: str = "data/brain/vector_store",
        collection_name: str = "zypher_brain",
    ):
        self.kb = kb
        self.encoder = encoder
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self._client = None
        self._collection = None

    def _connect(self) -> None:
        if self._collection is not None:
            return
        import chromadb

        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def is_indexed(self) -> bool:
        self._connect()
        return self._collection.count() > 0

    def _unique_id(self, doc: Document, used: set[str]) -> str:
        doc_id = doc.doc_id
        if doc_id not in used:
            used.add(doc_id)
            return doc_id
        fallback = hashlib.sha1(doc.path.encode()).hexdigest()[:12]
        used.add(fallback)
        return fallback

    def index(self, batch_size: int = 500) -> int:
        self._connect()
        total = 0
        used: set[str] = set()
        batch_ids, batch_texts, batch_metas = [], [], []

        def flush_batch() -> None:
            nonlocal total
            if not batch_ids:
                return
            embeddings = self.encoder.encode(batch_texts)
            self._collection.add(
                ids=batch_ids,
                documents=batch_texts,
                embeddings=embeddings,
                metadatas=batch_metas,
            )
            total += len(batch_ids)
            batch_ids.clear()
            batch_texts.clear()
            batch_metas.clear()

        for doc in self.kb.documents:
            doc_id = self._unique_id(doc, used)
            text = f"{doc.title}\n{doc.doc_type}\n{doc.content}"[:8000]
            batch_ids.append(doc_id)
            batch_texts.append(text)
            batch_metas.append({
                "title": doc.title,
                "path": doc.path,
                "category": doc.category,
                "doc_type": doc.doc_type,
                "hub": doc.hub,
                "original_id": doc.doc_id,
            })
            if len(batch_ids) >= batch_size:
                flush_batch()
                if total % 5000 == 0 and total > 0:
                    print(f"  Indexed {total:,} documents...")
        flush_batch()
        return total

    def index_document(self, doc: Document) -> None:
        """Index a single new document (no full rebuild)."""
        self._connect()
        used: set[str] = set()
        if self._collection.count() > 0:
            existing = self._collection.get(include=[])
            used = set(existing["ids"])
        doc_id = self._unique_id(doc, used)
        text = f"{doc.title}\n{doc.doc_type}\n{doc.content}"[:8000]
        embedding = self.encoder.encode([text])
        self._collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=embedding,
            metadatas=[{
                "title": doc.title,
                "path": doc.path,
                "category": doc.category,
                "doc_type": doc.doc_type,
                "hub": doc.hub,
                "original_id": doc.doc_id,
            }],
        )

    def search(self, query: str, top_k: int = 10) -> list[ScoredDocument]:
        self._connect()
        if self._collection.count() == 0:
            return []
        q_emb = self.encoder.encode_query(query)
        n = min(top_k, self._collection.count())
        results = self._collection.query(query_embeddings=[q_emb], n_results=n)
        scored: list[ScoredDocument] = []
        distances = results.get("distances", [[]])[0]
        paths = {d.path: d for d in self.kb.documents}
        for i, meta in enumerate(results["metadatas"][0]):
            path = meta.get("path", "")
            doc = paths.get(path)
            if not doc:
                doc_id = meta.get("original_id") or results["ids"][0][i]
                doc = self.kb.get(doc_id)
            if not doc:
                continue
            dist = distances[i] if i < len(distances) else 1.0
            score = max(0.0, 1.0 - dist)
            scored.append(ScoredDocument(document=doc, score=score, source="vector"))
        return scored
