# Coltex

Enterprise-grade retrieval-augmented generation (RAG) dataset and indexing engine. Coltex delivers curated knowledge artifacts—vector-ready chunks, embeddings, graph relationships, metadata, benchmarks, and compliance tooling—designed for production RAG pipelines.

This repository contains the **knowledge layer only**: document corpus, export pipeline, and retrieval engine. It does not include chat interfaces, model hosting, fine-tuning workflows, or API servers.

---

## Overview

Coltex is a modular RAG database composed of:

| Layer | Description |
|-------|-------------|
| **Knowledge base** | Original synthetic documents with typed metadata and graph links |
| **Export pipeline** | Chunking, deduplication, embedding generation, and manifest signing |
| **Retrieval engine** | Vector search, metadata filtering, graph traversal, and re-ranking |
| **Quality assurance** | Benchmark datasets, evaluation reports, and distribution audits |

```
┌──────────────────────────────────────────────────────────────────┐
│                            COLTEX                                │
│                                                                  │
│   Knowledge Base  →  Chunks  →  Embeddings  →  Vector Index      │
│        │              │            │              │              │
│        └──────── Graph Relationships · Metadata · Catalog ──────┘
└──────────────────────────────────────────────────────────────────┘
```

---

## Dataset Deliverables

Each product build exports a versioned, checksum-signed artifact set:

| Artifact | Path | Description |
|----------|------|-------------|
| Chunks | `data/product/chunks/chunks.jsonl` | Vector-ready text segments with metadata |
| Catalog | `data/product/catalog.jsonl` | Per-document index and provenance |
| Embeddings | `data/product/embeddings/embeddings.jsonl` | Pre-computed sentence-transformer vectors |
| Graph | `data/product/graph/edges.jsonl` | Typed relationship edges (`depends_on`, `see_also`, …) |
| Metadata | `data/product/metadata/documents.json` | Document-level schema index |
| Benchmarks | `benchmarks/*.jsonl` | FAQ pairs, retrieval gold, and RAG evaluation sets |
| Manifest | `data/product/manifest.json` | SHA-256 checksums, version, and build metadata |

All distributable content is original synthetic material governed by the **Coltex EULA**. See `knowledge-base/PROVENANCE.md` and `NOTICE` for provenance and third-party attribution.

---

## Getting Started

### Prerequisites

- Python 3.10+
- 4 GB RAM minimum (embedding generation benefits from additional memory)

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Build a dataset (smoke test)

```bash
make product-premium-smoke
```

This generates 25,000 premium documents with full pipeline validation. Artifacts are written to `data/product/`.

### Index and query

```bash
make index
python3 -m brain retrieve "What is retrieval-augmented generation for code?" --context
```

---

## Product Tiers

Coltex supports three build tiers for the premium RAG dataset. Configuration is defined in `config/product_hyper.yaml`.

| Tier | Command | Scope |
|------|---------|-------|
| Smoke | `make product-premium-smoke` | 25,000 documents — local validation |
| Premium | `make product-premium` | Full premium pipeline per configuration |
| Hyper | `make product-hyper` | Uncapped streaming generation for cluster deployment |

The hyper tier uses a `mega_multiplier` of 100,000,000,000, enabling procedural expansion to hundreds of trillions of unique document combinations via streaming generation. Hyper builds are intended for distributed execution (e.g., Vast.ai or equivalent compute clusters).

```bash
# Cluster deployment
make product-hyper
```

---

## Retrieval Engine

The `brain/` package implements the full retrieval stack:

```
brain/
├── brain.py           # Orchestrator and public API
├── ingestion/         # Markdown document loading and parsing
├── embeddings/        # Sentence-transformer encoding
├── indexing/          # ChromaDB persistent vector store
├── metadata/          # doc_type, category, and tag filtering
├── graph/             # Multi-hop relationship traversal
├── reranking/         # Source-weighted result merging
└── retrieval/         # End-to-end retrieval pipeline
```

### CLI reference

```bash
python3 -m brain index --reindex     # Rebuild the vector index
python3 -m brain stats                 # Report document and index counts
python3 -m brain retrieve "<query>"   # Retrieve ranked documents
python3 -m brain retrieve "<query>" --context   # Include assembled context window
```

### Retrieval pipeline

1. Encode the query embedding
2. Search the vector index
3. Apply metadata filters
4. Expand results via graph relationships
5. Merge and re-rank by source weight
6. Assemble the context window for downstream consumption

---

## Corpus Generation

Raw markdown corpus expansion is available for seed document generation prior to product export:

| Command | Approximate output |
|---------|-------------------|
| `make generate-smoke` | 2,000 documents |
| `make generate-mega` | 100,000 documents |
| `make generate-ultra` | 1,000,000 documents |
| `make generate-hyper` | Uncapped (streaming) |

Generated markdown under `knowledge-base/generated/` is excluded from commercial distribution builds.

---

## Quality and Compliance

The product pipeline enforces quality gates and distribution audits on every build:

```bash
make validate-product      # Metadata, chunk size, and duplication checks
make audit-distribution    # License files, provenance, and content compliance
make evaluate              # Retrieval recall@k and benchmark evidence report
```

| Gate | Threshold |
|------|-----------|
| Maximum duplicate chunk ratio | ≤ 5% |
| Metadata accuracy | ≥ 90% |
| Retrieval recall@8 | ≥ 45–50% (tier-dependent) |
| Third-party content | None (`third_party_docs_copied: false`) |

Reports are written to `benchmarks/evaluation_report.json` and `benchmarks/distribution_audit.json`.

---

## Configuration

| File | Purpose |
|------|---------|
| `config/product_hyper.yaml` | Premium hyper-tier dataset build |
| `config/product_hyper_smoke.yaml` | Local smoke-test configuration |
| `config/product.yaml` | Seed corpus product build |
| `config/brain.yaml` | Vector index and retrieval settings |
| `config/corpus_mega.yaml` | Mega-scale corpus generation |

---

## Repository Structure

```
.
├── brain/                  # Retrieval engine and CLI
├── knowledge-base/         # Source documents and audit samples
├── data/product/           # Exported dataset artifacts (build output)
├── benchmarks/             # Evaluation and compliance reports
├── scripts/
│   ├── product/            # Dataset build, audit, and export pipeline
│   ├── generate_corpus.py  # Markdown corpus generator
│   └── mega_scale.py       # Hyper-scale procedural topic expansion
├── docs/                   # Setup, quality, evaluation, and licensing guides
└── examples/               # Retrieval usage examples
```

---

## Documentation

- [Product setup](docs/product-setup.md)
- [Quality standards](docs/product-quality.md)
- [Evaluation guide](docs/product-evaluation.md)
- [Licensing](docs/product-licensing.md)
- [Content provenance](knowledge-base/PROVENANCE.md)

---

## License

Licensed under the [End User License Agreement](EULA). Third-party dependencies are listed in [NOTICE](NOTICE).
