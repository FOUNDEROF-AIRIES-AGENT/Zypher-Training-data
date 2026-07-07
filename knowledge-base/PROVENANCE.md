# Knowledge Base Provenance

This document records the origin of content in the Coltex knowledge base for
commercial distribution compliance.

## Content origin

| Category | Origin | Third-party sources |
|----------|--------|---------------------|
| FAQ documents (`CHUNK-00000`–`00004`) | Originally authored for Coltex | None |
| Graph relationship nodes | Synthetically generated fictional architecture | None |
| Architecture decision records (ADRs) | Synthetically generated | None |
| Incident reports & runbooks | Synthetically generated | None |
| Code review examples | Original minimal Python examples | None |
| OpenAPI / Kubernetes / SQL configs | Original minimal stubs | None |

## What is NOT included in commercial distribution

| Path | Reason |
|------|--------|
| `knowledge-base/_excluded_from_distribution/` | Placeholder stubs — insufficient substance for distribution |
| `knowledge-base/generated/` | Procedural mega-corpus for stress testing only |
| `knowledge-base/_seed/` | Internal seed copies |

## Generation method

- **No web scraping** of third-party documentation
- **No copying** from HuggingFace, LangChain, Kubernetes, Python, or other official docs
- **No LLM API generation** from external sources in the corpus pipeline
- Corpus expansion scripts (`scripts/generate_corpus.py`) use in-repo string templates only

## Technology references

Documents may reference technologies by name (e.g., Kafka, Kubernetes, tree-sitter,
ChromaDB) in descriptive context. These are **nominative references**, not reproduced
documentation from those projects.

## Runtime dependencies (not bundled)

The following are downloaded at runtime and subject to their own licenses:

| Component | License | Notes |
|-----------|---------|-------|
| `sentence-transformers/all-MiniLM-L6-v2` | Upstream HF license | Embedding model |
| `poolside/Laguna-XS-2.1` | Custom HF license | LLM — accept terms on Hugging Face before use |
| PyTorch, transformers, chromadb | Various open source | See root `NOTICE` |

## Premium distributable corpus

Streaming-generated documents in `knowledge-base/distributable/` are **original synthetic**
content for the $1000+ premium RAG dataset. Generation uses in-repo templates only.

| Tier | Multiplier | Command |
|------|------------|---------|
| Hyper | 100,000,000,000× | `make product-hyper` |

Estimated document capacity exceeds 600 trillion unique combinations (procedural).
Run on Vast.ai for uncapped generation.
