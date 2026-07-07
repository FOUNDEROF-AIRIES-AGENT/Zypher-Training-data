# Coltex

**Enterprise RAG Vector Dataset** — production-grade, graph-linked, vector-ready knowledge corpus for commercial AI deployment.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/documents-13k%2B-green.svg)](docs/commercial/datasheet.md)
[![Chunks](https://img.shields.io/badge/chunks-83k%2B-orange.svg)](docs/commercial/datasheet.md)
[![Graph edges](https://img.shields.io/badge/edges-57k%2B-purple.svg)](docs/commercial/datasheet.md)
[![Domains](https://img.shields.io/badge/domains-63-blue.svg)](docs/commercial/datasheet.md)
[![Compliance](https://img.shields.io/badge/audit-passing-brightgreen.svg)](docs/product-licensing.md)

Coltex delivers a fully auditable RAG dataset: 63 technology domains, 18 knowledge hubs, typed graph edges, pre-chunked JSONL exports, optional pre-computed embeddings, and benchmark evidence — ready to load into any vector database.

**Commercial documentation:** [Product overview](docs/commercial/product-overview.md) · [Datasheet](docs/commercial/datasheet.md) · [SKU matrix](docs/commercial/sku-matrix.md)

---

## Dataset at a glance

| Metric | Value |
|--------|-------|
| Curated documents | **12,993** |
| Vector chunks | **83,612** |
| Graph edges | **52,490** |
| Benchmark FAQ pairs | **1,100+** |
| Premium stream capacity | **25,000+** smoke · **uncapped** hyper |
| Technology domains | **63** |
| Knowledge hubs | **18** |
| Graph links | **306** hub-to-hub edges |
| Domain routes | **90** inter-cluster routes |
| Document types | **22** typed classifications |
| Graph edge types | **20** relationship types |
| Embedding model | `all-MiniLM-L6-v2` (384-dim) |
| License | **Apache-2.0** with full provenance |

---

## Architecture

```
                    ┌─── L6 Governance (Catalog & policy) ───┐
                    │   L5 Assembly (Context assembly)       │
                    │   L4 Graph (GraphRAG)                  │
                    │   L3 Integration (Cluster assignment)    │
                    │   L2 Metadata (Tagging & linking)      │
                    │   L1 Ingestion (Document intake)       │
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
                        brain retrieve / report
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

---

## Quick start — build the commercial package

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Expand corpus + build enterprise vector dataset
make corpus-mega
make product-enterprise

# Inspect deliverables
python3 examples/load_dataset.py
make audit-distribution
```

---

## Commercial tiers

| Tier | Command | Documents | Best for |
|------|---------|-----------|----------|
| **Enterprise Curated** | `make product-enterprise` | 12,993 | Production RAG deployment |
| **Premium Smoke** | `make product-premium-smoke` | 25,000 | Buyer validation / demos |
| **Premium Hyper** | `make product-hyper` | Uncapped | Maximum scale (cluster) |

Full comparison: [SKU matrix](docs/commercial/sku-matrix.md)

---

## Deliverables (`data/product/`)

| Artifact | Format | Description |
|----------|--------|-------------|
| `chunks/chunks.jsonl` | JSONL | Vector-index-ready text chunks |
| `embeddings/embeddings.jsonl` | JSONL | Pre-computed 384-dim vectors |
| `catalog.jsonl` | JSONL | Full document metadata |
| `graph/edges.jsonl` | JSONL | Typed relationship graph |
| `manifest.json` | JSON | SHA-256 checksums + build provenance |
| `benchmarks/` | JSONL | FAQ, retrieval gold, RAG eval |

---

## Retrieval engine

Hybrid RAG pipeline with **GraphRouter** (region-aware graph expansion):

```bash
make index
python3 -m brain retrieve "How does GraphRAG routing work?" --context
python3 -m brain report
```

---

## Expand the corpus

| Command | Output |
|---------|--------|
| `make corpus-advanced` | Architecture bootstrap (500 docs + routes + hubs) |
| `make corpus-mega` | **10,000** domain documents |
| `make corpus-grow COUNT=5000` | Incremental expansion |
| `make expand-curated-kb COUNT=500` | Curated KB growth |

Catalog index: `data/brain/catalog-index.json` · Architecture manifest: `data/brain/architecture-manifest.json`

---

## Documentation

| Document | Description |
|----------|-------------|
| [Product overview](docs/commercial/product-overview.md) | Commercial positioning |
| [Technical datasheet](docs/commercial/datasheet.md) | Specifications |
| [SKU matrix](docs/commercial/sku-matrix.md) | Tier comparison |
| [Knowledge architecture](docs/architecture/knowledge-architecture.md) | Corpus structure |
| [Product licensing](docs/product-licensing.md) | Apache-2.0 compliance |
| [Product setup](docs/product-setup.md) | Build instructions |

---

## License

Apache-2.0. Original synthetic content with full provenance. See [PROVENANCE.md](knowledge-base/PROVENANCE.md).
