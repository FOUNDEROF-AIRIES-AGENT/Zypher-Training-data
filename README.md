# Coltex — AI Knowledge Infrastructure Platform

Enterprise-grade knowledge infrastructure for RAG, AI agents, and domain-specific copilots. Coltex unifies **datasets**, **knowledge graphs**, **vector search**, **retrieval pipelines**, and **knowledge management** into a single platform — not a static document dump.

[![Documents: 13k+](https://img.shields.io/badge/documents-13k%2B-green.svg)](docs/commercial/datasheet.md)
[![Graph edges: 52k+](https://img.shields.io/badge/graph%20edges-52k%2B-purple.svg)](docs/commercial/datasheet.md)
[![Domains: 63](https://img.shields.io/badge/domains-63-blue.svg)](docs/commercial/datasheet.md)
[![Platform](https://img.shields.io/badge/platform-knowledge%20infrastructure-blue.svg)](docs/platform/overview.md)

---

## Overview

Coltex is an **AI knowledge infrastructure platform** that helps organizations ingest, structure, connect, search, and govern knowledge at scale. The enterprise RAG vector dataset is one component — alongside graph linking, hybrid retrieval, quality analytics, and (on the roadmap) visual management, live connectors, and automatic synchronization.

**Platform components**

| Component | Description | Status |
|-----------|-------------|--------|
| **Knowledge Dataset** | Graph-linked, vector-ready corpus with typed metadata and provenance | Available |
| **Knowledge Graph** | Hub clusters, domain routes, typed relationship edges (GraphRAG) | Available |
| **Search & Retrieval** | Hybrid RAG pipeline with region-aware GraphRouter | Available |
| **Quality & Audit** | Distribution audit, benchmarks, compliance artifacts | Available |
| **Knowledge Studio** | Visual explorer for documents, graph, embeddings, and metadata | Roadmap |
| **Connectors & Sync** | GitHub, Notion, Confluence, Drive, Slack, and more — live sync | Roadmap |
| **Knowledge Timeline** | Version history, diff, and rollback per document | Roadmap |
| **AI Quality Dashboard** | Retrieval accuracy, chunk health, coverage, graph density | Roadmap |
| **Multi-tenancy** | Organization → Workspace → Project → Knowledge Base | Roadmap |
| **Plugin System** | Extensible connectors and custom integrations | Roadmap |

Full platform vision: [Platform overview](docs/platform/overview.md) · [Roadmap](docs/platform/roadmap.md)

---

## Why teams choose Coltex

- **Living knowledge, not static files** — graph-linked documents with cross-reference edges and cluster routing
- **Production-ready exports** — pre-chunked JSONL, optional embeddings, manifest checksums, benchmark evidence
- **Enterprise governance** — auditable provenance, tiered licensing, distribution compliance pipeline
- **Graph-aware retrieval** — GraphRouter expands context across hubs, domains, and relationship types
- **Built to grow** — connector ecosystem, sync, and Knowledge Studio on the roadmap ([details](docs/platform/roadmap.md))

---

## Architecture

```
  Connectors (roadmap)          Knowledge Studio (roadmap)
         │                              │
         ▼                              ▼
  ┌────────────── L6 Governance (Catalog & policy) ──────────────┐
  │  L5 Assembly   L4 Graph (GraphRAG)   L3 Integration         │
  │  L2 Metadata   L1 Ingestion                                  │
  └──────────────────────────┬───────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    63 Domains         18 Knowledge Hubs    4 Memory Tiers
         │                   │                   │
         └──────► Graph Links + Domain Routes ◄─┘
                             │
              Vector + Metadata + GraphRouter
                             │
                    Search · Retrieval · Analytics
```

| Layer | Path | Purpose |
|-------|------|---------|
| Processing stack | `knowledge-corpus/processing-layers/` | L1–L6 ingestion through governance |
| Functional clusters | `knowledge-corpus/clusters/` | Domain groupings by function |
| Domains | `knowledge-corpus/domains/` | 63 technology categories |
| Knowledge hubs | `knowledge-corpus/hubs/` | 18 service-level clusters |
| Graph links | `knowledge-corpus/graph-links/` | Hub-to-hub relationships |
| Domain routes | `knowledge-corpus/domain-routes/` | Inter-cluster routes |

Detailed architecture: [Knowledge architecture](docs/architecture/knowledge-architecture.md)

---

## Available today

### Dataset specifications

| Metric | Value |
|--------|-------|
| Curated documents | **12,993** |
| Vector chunks | **83,612** |
| Graph edges | **52,490** |
| Technology domains | **63** |
| Knowledge hubs | **18** |
| Benchmark FAQ pairs | **1,100+** |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) |

Full specifications: [Technical datasheet](docs/commercial/datasheet.md)

### Getting started

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make corpus-mega
make product-enterprise

python3 examples/load_dataset.py
make audit-distribution
```

### Retrieval engine

```bash
make index
python3 -m brain retrieve "How does GraphRAG routing work?" --context
python3 -m brain report
```

Build and deployment: [Product setup](docs/product-setup.md)

### Deliverables (`data/product/`)

| Artifact | Format | Description |
|----------|--------|-------------|
| `chunks/chunks.jsonl` | JSONL | Vector-index-ready text chunks |
| `embeddings/embeddings.jsonl` | JSONL | Pre-computed 384-dimensional vectors |
| `catalog.jsonl` | JSONL | Full document metadata catalog |
| `graph/edges.jsonl` | JSONL | Typed relationship graph |
| `manifest.json` | JSON | SHA-256 checksums and build provenance |
| `benchmarks/` | JSONL | FAQ, retrieval gold, and RAG evaluation sets |

---

## Platform roadmap

The highest-impact enterprise capabilities in development:

1. **[Knowledge Studio](docs/platform/roadmap.md#1-knowledge-studio)** — visual management of documents, graph, embeddings, search, and clusters
2. **[Automatic Connectors](docs/platform/roadmap.md#2-automatic-connectors)** — GitHub, GitLab, Notion, Confluence, Google Drive, SharePoint, Jira, Slack, and more
3. **[Automatic Synchronization](docs/platform/roadmap.md#3-automatic-synchronization)** — commit-triggered knowledge, graph, and vector updates
4. **[Knowledge Timeline](docs/platform/roadmap.md#4-knowledge-timeline)** — version history and rollback per document
5. **[AI Quality Dashboard](docs/platform/roadmap.md#5-ai-quality-dashboard)** — retrieval accuracy, chunk health, coverage, graph density
6. **[Knowledge Analytics](docs/platform/roadmap.md#6-knowledge-analytics)** — search trends, gaps, weak areas, broken links
7. **[Multi-tenancy](docs/platform/roadmap.md#7-multi-tenancy)** — Organization → Workspace → Project → Knowledge Base
8. **[Plugin System](docs/platform/roadmap.md#8-plugin-system)** — extensible connector and integration framework
9. **[AI Document Writer](docs/platform/roadmap.md#9-ai-document-writer)** — auto-generate API docs, FAQs, runbooks from uploads
10. **[Visual Knowledge Graph](docs/platform/roadmap.md#10-visual-knowledge-graph)** — interactive, clickable graph exploration

Connector manifest: [config/connectors.yaml](config/connectors.yaml)

---

## Package tiers

| Package | Build command | Documents | Intended use |
|---------|---------------|-----------|--------------|
| Personal | `make product-personal` | Full corpus | Non-commercial learning and research |
| Professional | `make product-professional` | Full corpus | Commercial applications — single entity |
| Enterprise Curated | `make product-enterprise` | 12,993 | Production RAG deployment |
| Premium Standard | `make product-premium-smoke` | 25,000 | Validation and evaluation |
| Premium Hyper | `make product-hyper` | Uncapped | Maximum-scale production |

Full comparison: [SKU matrix](docs/commercial/sku-matrix.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [Platform overview](docs/platform/overview.md) | AI knowledge infrastructure vision |
| [Platform roadmap](docs/platform/roadmap.md) | Enterprise features and timeline |
| [Licenses](licenses/README.md) | License tiers and terms |
| [Product overview](docs/commercial/product-overview.md) | Commercial positioning |
| [Technical datasheet](docs/commercial/datasheet.md) | Dataset specifications |
| [Knowledge architecture](docs/architecture/knowledge-architecture.md) | Corpus structure and design |
| [Product setup](docs/product-setup.md) | Build and deployment instructions |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.
