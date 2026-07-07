# Coltex Enterprise RAG Vector Dataset

Production-grade, graph-linked knowledge corpus for retrieval-augmented generation (RAG), AI agents, and domain-specific copilots. Coltex delivers pre-chunked vector exports, typed relationship graphs, optional embeddings, benchmark evidence, and a full compliance audit trail — ready for commercial deployment.

[![Documents: 13k+](https://img.shields.io/badge/documents-13k%2B-green.svg)](docs/commercial/datasheet.md)
[![Chunks: 83k+](https://img.shields.io/badge/chunks-83k%2B-orange.svg)](docs/commercial/datasheet.md)
[![Graph edges: 52k+](https://img.shields.io/badge/edges-52k%2B-purple.svg)](docs/commercial/datasheet.md)
[![Domains: 63](https://img.shields.io/badge/domains-63-blue.svg)](docs/commercial/datasheet.md)
[![Audit: Passing](https://img.shields.io/badge/audit-passing-brightgreen.svg)](docs/commercial/datasheet.md)

---

## Overview

Coltex is a structured knowledge dataset designed for teams that require auditable provenance, consistent metadata, and graph-aware retrieval — not ad-hoc document dumps. Each document carries typed classification, domain assignment, hub clustering, and cross-reference edges suitable for GraphRAG and hybrid search pipelines.

**Primary applications**

- Enterprise RAG copilots with pre-built coverage across cloud, security, data, and platform engineering
- Agent toolchains requiring multi-hop reasoning over runbooks, ADRs, and API references
- Vector database seeding (Pinecone, Weaviate, Chroma, pgvector, and others)
- Benchmark baselines for retrieval recall, metadata accuracy, and buyer due diligence
- Fine-tuning and domain adaptation from structured Q&A and retrieval gold pairs

---

## Specifications

| Metric | Value |
|--------|-------|
| Curated documents | **12,993** |
| Vector chunks | **83,612** |
| Graph edges | **52,490** |
| Benchmark FAQ pairs | **1,100+** |
| Technology domains | **63** |
| Knowledge hubs | **18** |
| Graph links (hub-to-hub) | **306** |
| Domain routes (inter-cluster) | **90** |
| Document types | **22** typed classifications |
| Graph edge types | **20** relationship types |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) |
| Premium stream capacity | 25,000+ (validation) · uncapped (production) |

Full technical specifications: [Technical datasheet](docs/commercial/datasheet.md)

---

## Architecture

Coltex organizes content through six processing layers (L1 ingestion through L6 governance), ten functional clusters, and four memory tiers. Documents flow from intake through metadata enrichment, cluster assignment, graph linking, and context assembly before export.

```
                    ┌─── L6 Governance (Catalog & policy) ───┐
                    │   L5 Assembly (Context assembly)       │
                    │   L4 Graph (GraphRAG)                  │
                    │   L3 Integration (Cluster assignment)  │
                    │   L2 Metadata (Tagging & linking)    │
                    │   L1 Ingestion (Document intake)     │
                    └─────────────────┬──────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
         63 Domains             18 Knowledge Hubs       4 Memory Tiers
              │                       │                       │
              └──────────► Graph Links + Domain Routes ◄──────┘
                                   │
                    Vector + Metadata + GraphRouter
                                   │
                          Retrieval & evaluation
```

| Region | Path | Purpose |
|--------|------|---------|
| Processing layers | `knowledge-corpus/processing-layers/` | L1–L6 document processing stack |
| Functional clusters | `knowledge-corpus/clusters/` | Domain groupings by function |
| Domains | `knowledge-corpus/domains/` | 63 technology categories |
| Knowledge hubs | `knowledge-corpus/hubs/` | 18 service-level clusters |
| Graph links | `knowledge-corpus/graph-links/` | Hub-to-hub relationships |
| Domain routes | `knowledge-corpus/domain-routes/` | Inter-cluster routes |
| Memory tiers | `knowledge-corpus/memory/` | Working, episodic, semantic, procedural |
| Quick reference | `knowledge-corpus/quick-reference/` | FAQ index |

Detailed architecture: [Knowledge architecture](docs/architecture/knowledge-architecture.md)

---

## Getting started

### Prerequisites

- Python 3.10+
- 8 GB RAM recommended for full enterprise build

### Build the enterprise dataset package

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make corpus-mega
make product-enterprise

python3 examples/load_dataset.py
make audit-distribution
```

Additional build targets and configuration options: [Product setup](docs/product-setup.md)

### Query the retrieval engine

Hybrid RAG pipeline with region-aware **GraphRouter** expansion:

```bash
make index
python3 -m brain retrieve "How does GraphRAG routing work?" --context
python3 -m brain report
```

---

## Deliverables

Commercial builds output to `data/product/`:

| Artifact | Format | Description |
|----------|--------|-------------|
| `chunks/chunks.jsonl` | JSONL | Vector-index-ready text chunks |
| `embeddings/embeddings.jsonl` | JSONL | Pre-computed 384-dimensional vectors |
| `catalog.jsonl` | JSONL | Full document metadata catalog |
| `graph/edges.jsonl` | JSONL | Typed relationship graph |
| `manifest.json` | JSON | SHA-256 checksums and build provenance |
| `benchmarks/` | JSONL | FAQ, retrieval gold, and RAG evaluation sets |

Compliance artifacts include `NOTICE`, `PROVENANCE.md`, and `distribution_audit.json`. Terms of use: [LICENSING.md](LICENSING.md).

---

## Package tiers

| Package | Build command | Documents | Intended use |
|---------|---------------|-----------|--------------|
| Personal | `make product-personal` | Full corpus | Non-commercial learning and research |
| Professional | `make product-professional` | Full corpus | Commercial applications — single entity |
| Enterprise Curated | `make product-enterprise` | 12,993 | Production RAG deployment |
| Premium Standard | `make product-premium-smoke` | 25,000 | Validation and evaluation |
| Premium Hyper | `make product-hyper` | Uncapped | Maximum-scale production |

Package and license comparison: [SKU matrix](docs/commercial/sku-matrix.md)

---

## Corpus expansion

| Command | Output |
|---------|--------|
| `make corpus-advanced` | Architecture bootstrap (500 documents, routes, hubs) |
| `make corpus-mega` | 10,000 domain documents |
| `make corpus-grow COUNT=5000` | Incremental expansion |
| `make expand-curated-kb COUNT=500` | Curated knowledge base growth |

Catalog index: `data/brain/catalog-index.json`  
Architecture manifest: `data/brain/architecture-manifest.json`

---

## Documentation

| Document | Description |
|----------|-------------|
| [Licensing](LICENSING.md) | License tiers, terms, and build commands |
| [Product overview](docs/commercial/product-overview.md) | Commercial positioning and use cases |
| [Technical datasheet](docs/commercial/datasheet.md) | Dataset specifications |
| [SKU matrix](docs/commercial/sku-matrix.md) | Package comparison |
| [Knowledge architecture](docs/architecture/knowledge-architecture.md) | Corpus structure and design |
| [Product setup](docs/product-setup.md) | Build and deployment instructions |
| [Provenance](knowledge-base/PROVENANCE.md) | Content origin and compliance |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved. See [LICENSING.md](LICENSING.md) for terms of use.
