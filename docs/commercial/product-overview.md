# Coltex — AI Knowledge Infrastructure Platform

**Enterprise knowledge infrastructure for RAG, AI agents, and governed organizational knowledge.**

Coltex unifies datasets, knowledge graphs, vector search, retrieval pipelines, and knowledge management. The enterprise RAG vector dataset is a core deliverable — alongside graph linking, hybrid retrieval, quality analytics, and a roadmap toward Knowledge Studio, live connectors, and automatic synchronization.

---

## Platform components

| Component | Status | Detail |
|-----------|--------|--------|
| Knowledge Dataset | Available | 13k+ docs · 83k+ chunks · 52k+ graph edges |
| Knowledge Graph | Available | Hubs, routes, 20 relationship types, GraphRAG |
| Search & Retrieval | Available | Hybrid RAG with GraphRouter |
| Quality & Audit | Available | Benchmarks, provenance, distribution audit |
| Knowledge Studio | Roadmap | Visual document, graph, and metadata management |
| Connectors & Sync | Roadmap | GitHub, Notion, Confluence, Drive, Slack, and more |
| AI Quality Dashboard | Roadmap | Retrieval accuracy, chunk health, coverage metrics |

Full vision: [Platform overview](../platform/overview.md) · [Roadmap](../platform/roadmap.md)

---

## License tiers

| Tier | Price | Document |
|------|-------|----------|
| **Personal** | $79 USD (one-time) | [licenses/personal.md](../../licenses/personal.md) |
| **Professional** | $399 USD (one-time) | [licenses/professional.md](../../licenses/professional.md) |
| **Enterprise** | Custom quote | [licenses/enterprise.md](../../licenses/enterprise.md) |

Full tier comparison: [licenses/README.md](../../licenses/README.md)

---

## Why Coltex

| Capability | Detail |
|------------|--------|
| **Platform scope** | Dataset + graph + search + governance — not a static export |
| **Scale** | 35,000+ deliverable documents; procedural capacity to billions+ |
| **Structure** | 63 domains · 18 hubs · 306 graph links · 90 domain routes |
| **Vector-ready** | Pre-chunked JSONL · optional embeddings (MiniLM-L6-v2) |
| **GraphRAG** | Typed edges · hub clustering · region-aware GraphRouter |
| **Compliance** | Tiered licensing · full provenance · audit pipeline |
| **Roadmap** | Knowledge Studio, connectors, sync, dashboards, multi-tenancy |

---

## Architecture

```
Connectors (roadmap)  →  L1–L6 Processing  →  Graph + Vectors  →  Search & Analytics
                              ↓
                    Knowledge Dataset (available today)
```

Six processing layers (L1 ingestion through L6 governance), ten functional clusters, and four memory tiers organize content for retrieval routing and enterprise governance.

---

## Ideal use cases

- **Enterprise RAG copilots** — domain coverage across cloud, security, data, and platform engineering
- **Agent toolchains** — graph-linked runbooks, ADRs, and API references for multi-hop reasoning
- **Living knowledge systems** — connector-driven sync from GitHub, Confluence, Notion (roadmap)
- **Vector database seeding** — load chunks and embeddings into Pinecone, Weaviate, Chroma, pgvector
- **Knowledge governance** — audit trail, quality dashboards, gap analytics (roadmap)

---

## What's included in a commercial build

| Artifact | Format | Purpose |
|----------|--------|---------|
| `catalog.jsonl` | JSONL | Full document metadata catalog |
| `chunks/chunks.jsonl` | JSONL | Vector-index-ready text chunks |
| `embeddings/embeddings.jsonl` | JSONL | Pre-computed 384-dim vectors |
| `graph/edges.jsonl` | JSONL | Typed relationship graph |
| `manifest.json` | JSON | SHA-256 checksums and build provenance |
| `benchmarks/` | JSONL | FAQ, retrieval gold, RAG eval sets |

Compliance: `licenses/`, `NOTICE`, `PROVENANCE.md`, `distribution_audit.json`

---

## Build commands

```bash
make product-enterprise       # Enterprise curated tier
make product-premium-smoke    # Premium validation build
make audit-distribution       # Compliance check
make evaluate                 # Retrieval benchmarks
```

See [SKU matrix](sku-matrix.md) · [Datasheet](datasheet.md) · [Platform roadmap](../platform/roadmap.md)

---

## License

See [licenses/README.md](../../licenses/README.md) for license tiers and terms.
