# Changelog

All notable changes to the Coltex product package are documented here.

## [4.3.0] - 2026-07-07

### Added — Enterprise RAG Vector Dataset (commercial tier)

- **`config/product_enterprise.yaml`** — Enterprise tier v3.0.0 (13,000+ documents)
- **`scripts/product/build_enterprise_product.py`** — Full enterprise build orchestrator
- **`make product-enterprise`** / **`make product-enterprise-fast`** — Commercial build targets
- **Commercial documentation** — `docs/commercial/product-overview.md`, `datasheet.md`, `sku-matrix.md`
- **`examples/load_dataset.py`** — Buyer inspection script
- **`knowledge-base/distributable/DATASET.md`** — Distributable package orientation

### Changed — Scale & polish

- Corpus expanded to **12,993 documents** across 63 domains (`make corpus-mega`)
- Enterprise build produces **83,612 vector chunks**, **52,490 graph edges**, **1,100+ benchmark pairs**
- Chunk deduplication scoped per document (preserves cross-doc coverage)
- Distribution validation allows ≤1% thin documents on large corpora
- Fixed manifest/audit crash when `generation_stats` path absent
- README repositioned as commercial **Enterprise RAG Vector Dataset** with SKU matrix

## [4.2.2] - 2026-07-07

### Changed — Enterprise terminology (Phase 4)

- Renamed corpus regions: `lobes/` → `clusters/`, `synapses/` → `graph-links/`, `pathways/` → `domain-routes/`, `reflexes/` → `quick-reference/`, `cortex/` → `processing-layers/`
- Renamed standalone regions: `hippocampus/` → `retention/`, `cerebellum/` → `automation/`, `brainstem/` → `operations/`, `thalamus/` → `routing/`, `amygdala/` → `priority/`
- Functional cluster slugs: `frontal` → `architecture`, `temporal` → `retrieval`, `parietal` → `data`, `occipital` → `observability`, `limbic` → `security`
- Processing layer slugs: `L1_sensory` → `L1_ingestion`, `L2_association` → `L2_metadata`, `L4_reasoning` → `L4_graph`, `L5_executive` → `L5_assembly`, `L6_meta` → `L6_governance`
- `brain/graph/neural_router.py` → `graph_router.py` (`NeuralRouter` → `GraphRouter`)
- `data/brain/neural-map.json` → `catalog-index.json`
- Generated artifact prefixes: `SYNAPSE-*` → `LINK-*`, `REFLEX-*` → `FAQ-*`, `PATHWAY-*` → `ROUTE-*`
- Doc types: `neural_pathway` → `domain_route`, `synapse_map` → `graph_link_map`
- Removed deprecated `brain pulse` CLI alias
- Makefile: `corpus-synapses` → `corpus-links`

## [4.2.1] - 2026-07-07

### Changed — Professional terminology

- Renamed `living-brain/` → `knowledge-corpus/`
- Renamed `scripts/living_brain.py` → `scripts/knowledge_corpus.py`
- Replaced "Living Brain" / "Hypercortex" wording with **Knowledge Corpus** / **Knowledge Architecture**
- Hub `coltex_living_brain` → `coltex_knowledge_core`
- CLI `brain pulse` → `brain report`
- Makefile targets: `corpus`, `corpus-advanced`, `corpus-grow`, `corpus-report`

## [4.2.0] - 2026-07-07

### Added — Knowledge Architecture v2

- **`config/brain_architecture.yaml`** — Master spec: 6 cortical layers, 10 lobes, 4 memory tiers, 18 hubs
- **`scripts/brain_architecture.py`** — Architecture loader and domain-to-lobe mapping
- **`brain/graph/neural_router.py`** — Region-aware GraphRAG with pathway/synapse score boosts
- **10 brain lobes** — frontal, temporal, parietal, occipital, limbic, cerebellum, hippocampus, thalamus, amygdala, brainstem
- **6 cortical layers** — L1-sensory through L6-meta
- **4 memory tiers** — working, episodic, semantic, procedural
- **Inter-lobe pathways** — excitatory, inhibitory, modulatory, associative, commissural
- **13 new neural hubs** — vector_store_cluster, agent_orchestrator, llm_inference_gateway, etc.
- **10 advanced GraphRAG edge types** — extends, validates, synthesizes, triggers, etc.
- **`data/brain/architecture-manifest.json`** — Live architecture registry
- **`docs/architecture/knowledge-architecture.md`** — Full architecture reference
- **`make corpus-advanced`** — Full architecture bootstrap command
- Enhanced `brain report` — architecture metrics (domains, clusters, pathways)

### Changed

- Graph routing: 4 hops, 16 max chunks, advanced_routing enabled by default
- `KNOWLEDGE_HUBS` expanded from 5 → 18
- `RELATIONSHIP_TYPES` expanded from 10 → 20

## [4.1.0] - 2026-07-07

### Added — Coltex Knowledge Corpus

- **`knowledge-base/knowledge-corpus/`** — Domain-organized folder tree
- **`scripts/knowledge_corpus.py`** — Bootstrap, grow, wire graph links, build catalog
- Makefile targets: `corpus`, `corpus-grow`, `corpus-mega`, `corpus-report`

### Changed

- README repositioned as **enterprise knowledge corpus** (not RAG-as-a-Service)
- `config/brain.yaml` indexes `knowledge-corpus/` paths

### Removed

- `coltex_platform/` RAG-as-a-Service API (out of scope)
- Docker/Kubernetes platform deployment, sales/API docs, platform tests

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
