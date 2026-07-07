# Changelog

All notable changes to the Coltex product package are documented here.

## [4.0.0] - 2026-07-07

### Added — Coltex RAG-as-a-Service Platform

- **`coltex_platform/`** — Full multi-tenant FastAPI platform restored and rebranded
  - Tenant registration, API key authentication, usage metering
  - Workspaces, collections, document ingestion (text, URL, file upload)
  - Async indexing jobs with background worker
  - Hybrid retrieval API and RAG chat completions (mock + OpenAI providers)
- **Docker & Kubernetes** — `Dockerfile`, `docker-compose.yml`, `deploy/kubernetes/coltex-platform.yaml`
- **Sales & commercial docs** — `docs/sales/` (overview, pricing, feature matrix)
- **API & architecture docs** — `docs/api/`, `docs/architecture/`, `docs/deployment/`
- **Enterprise knowledge base** — CHUNK-00500+ platform overview, API reference, deployment guide
- **Platform tests** — `tests/test_platform.py`
- **Examples** — `examples/platform_client.py`
- Makefile targets: `make platform`, `make platform-dev`, `make docker-up`, `make test`

### Changed

- README repositioned as **enterprise RAG-as-a-Service** (platform + brain + dataset)
- `requirements.txt` expanded with FastAPI, uvicorn, httpx, pydantic, pytest

## [2.1.0] - 2026-07-07

### Added

- **Expanded curated seed knowledge-base** — 340+ new CHUNK documents via `make expand-curated-kb`
- 24 new corpus topic seeds (hybrid reranking, observability, vector stores, agentic patterns, and more)
- Doc-type-aware benchmark question templates with difficulty tiers and category stratification
- Multi-hop retrieval gold queries from knowledge hub graph links

### Changed

- Premium smoke build increased to **25,000 documents** (from 10,000) across **22 categories**
- Benchmark datasets increased to **200 FAQ pairs**, **220 retrieval gold**, **200 RAG eval** (from 20 each)
- Premium generator now round-robins topics for category diversity in bounded builds
- Premium document sections include concrete operational details and checklists
- Fixed Go/C++ code snippet template escaping for corpus generation
- Smoke builds skip embedding export by default (`--skip-embeddings`) for faster iteration

## [3.1.0] - 2026-07-06

### Changed

- Rebranded **Zypher** → **Coltex** across codebase, docs, and knowledge base
- Renamed `Zypher` class to `Coltex`; vector collection `zypher` → `coltex`

## [3.0.0] - 2026-07-06

### Removed (database-only focus)

- `zypher/` chatbot CLI and LLM provider
- `zypher_platform/` REST API, sessions, jobs, agents
- Fine-tuning scripts (`train.py`, `infer.py`, `prepare_advanced_dataset.py`)
- `config/llm.yaml`, `platform.yaml`, `zypher_xs.yaml`, `rag.yaml`
- Notebooks, Kubernetes/Docker hosting configs in knowledge-base
- Conversation memory module (chat-only)

### Changed

- Repository is now **Zypher** RAG database only (chatbot, API, and fine-tuning removed)
- Rebranded **Zypher Brain** → **Zypher** (`Zypher` class, `zypher` collection)
- Dropped **Mega** from product naming (README, NOTICE, CLI, docs)
- `python3 -m brain` CLI for index / retrieve / stats
- Slimmed `requirements.txt` to RAG dependencies only

## [2.0.0] - 2026-07-06

### Added

- **$1000+ Premium RAG Dataset** — hyper-scale distributable corpus
- `mega_multiplier: 100000000000` (100 billion× tier)
- Streaming generation: `scripts/product/stream_premium_corpus.py`
- Premium content generator with 6+ sections, code examples, graph edges per document
- `make product-premium-smoke`, `make product-premium`, `make product-hyper`
- Catalog.jsonl metadata index for billion-scale document tracking
- Estimated 604+ trillion unique document combinations (procedural)

## [1.1.0] - 2026-07-06

### Added

- Commercial distribution compliance: `NOTICE`, `knowledge-base/LICENSE`, `PROVENANCE.md`
- Distribution audit (`make audit-distribution`) — scans for third-party content, forbidden markers
- Quarantined 54 non-distributable placeholder stubs to `_excluded_from_distribution/`
- `.dockerignore` excludes generated and quarantined content from releases

### Changed

- Product build excludes `_excluded_from_distribution/` from commercial package
- Documentation updated with honest content origin and licensing requirements

## [1.0.0] - 2026-07-06

### Added

- **Product pipeline** (`make product`) — curated knowledge package build
- Vector-ready chunks with accurate metadata (`data/product/chunks/`)
- Embedding generation script (`scripts/product/export_embeddings.py`)
- Graph relationship export (`data/product/graph/edges.jsonl`)
- Deduplication pipeline (max 5% duplicate ratio)
- Quality validation gates (`scripts/product/validate_quality.py`)
- Benchmark datasets: FAQ pairs, retrieval gold, RAG eval (`benchmarks/`)
- RAG evaluation with evidence report (`benchmarks/evaluation_report.json`)
- Product manifest with SHA-256 checksums (`data/product/manifest.json`)
- Curated brain config (`config/brain_curated.yaml`) — CHUNK docs only
- Example applications (`examples/rag_query.py`, `brain_retrieve.py`, `api_client.py`)
- Documentation: setup guide, quality standards, evaluation guide, licensing
- Apache-2.0 license

### Design

- Value over volume: curated `CHUNK-*.md` documents, not synthetic mega corpus
- Quality gates enforce metadata accuracy, minimal duplication, and retrieval evidence
- Brain = knowledge; LLM = reasoning engine (unchanged architecture)
