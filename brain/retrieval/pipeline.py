"""Full retrieval pipeline for Zypher Brain."""

from __future__ import annotations

from brain.graph.relationships import GraphIndex
from brain.indexing.vector_index import VectorIndex
from brain.metadata.index import MetadataIndex
from brain.reranking.reranker import Reranker
from brain.types import RetrievalResult, ScoredDocument


def build_context(documents: list[ScoredDocument], max_chars: int = 14000) -> str:
    if not documents:
        return "No relevant documents found in Zypher Brain."

    blocks: list[str] = []
    used = 0
    for i, scored in enumerate(documents, start=1):
        doc = scored.document
        meta = f"doc_type={doc.doc_type or 'unknown'}, category={doc.category or 'unknown'}"
        if doc.hub:
            meta += f", hub={doc.hub}"
        block = (
            f"### [{i}] {doc.title}\n"
            f"Source: {doc.path}\n"
            f"Metadata: {meta}\n"
            f"Relevance: {scored.score:.2f} ({scored.source})\n\n"
            f"{doc.content[:2500]}"
        )
        if used + len(block) > max_chars:
            break
        blocks.append(block)
        used += len(block)
    return "\n\n---\n\n".join(blocks)


class RetrievalPipeline:
    """
    Retrieval flow:
    1. Embed query
    2. Vector search
    3. Metadata filter search
    4. Graph relationship expansion
    5. Merge and re-rank
    6. Build context window
    """

    def __init__(
        self,
        vector_index: VectorIndex,
        metadata_index: MetadataIndex,
        graph_index: GraphIndex,
        reranker: Reranker | None = None,
        vector_top_k: int = 10,
        metadata_top_k: int = 8,
        final_top_k: int = 8,
        max_context_chars: int = 14000,
    ):
        self.vector_index = vector_index
        self.metadata_index = metadata_index
        self.graph_index = graph_index
        self.reranker = reranker or Reranker()
        self.vector_top_k = vector_top_k
        self.metadata_top_k = metadata_top_k
        self.final_top_k = final_top_k
        self.max_context_chars = max_context_chars

    def retrieve(self, query: str) -> RetrievalResult:
        vector_hits = self.vector_index.search(query, top_k=self.vector_top_k)
        metadata_hits = self.metadata_index.search(query, top_k=self.metadata_top_k)
        graph_hits = self.graph_index.search_from_seeds(vector_hits + metadata_hits)

        merged = self.reranker.merge(vector_hits, metadata_hits, graph_hits, top_k=self.final_top_k)
        context = build_context(merged, max_chars=self.max_context_chars)
        return RetrievalResult(query=query, documents=merged, context=context)
