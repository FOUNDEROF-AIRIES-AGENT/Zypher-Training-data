# Coltex

**Enterprise RAG-as-a-Service** — multi-tenant API, hybrid retrieval engine, premium dataset export, and compliance tooling. Ship production knowledge AI in days, not months.

Coltex is the complete stack for building, selling, and operating retrieval-augmented generation:

| Product | Description |
|---------|-------------|
| **Coltex Platform** | REST API — ingest, index, retrieve, RAG chat |
| **Coltex Brain** | Hybrid retrieval — vector + metadata + GraphRAG |
| **Coltex Premium Dataset** | Distributable chunks, embeddings, graph, benchmarks |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COLTEX RAG-AS-A-SERVICE                         │
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐  │
│  │  Platform    │    │  Coltex      │    │  Dataset Product         │  │
│  │  API         │───▶│  Brain       │    │  Pipeline                │  │
│  │  (FastAPI)   │    │  (Retrieval) │    │  (Export & Audit)        │  │
│  └──────────────┘    └──────────────┘    └──────────────────────────┘  │
│         │                    │                        │                  │
│         ▼                    ▼                        ▼                  │
│   Multi-tenant          ChromaDB +              chunks.jsonl            │
│   Auth & Jobs           Graph + Metadata        embeddings.jsonl        │
│                                                 manifest.json           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Platform API (RAG-as-a-Service)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make platform
# API docs: http://localhost:8080/docs
# Demo key:  data/platform/DEMO_API_KEY.txt
```

**Docker:**
```bash
docker compose up -d
curl http://localhost:8080/health
```

### CLI Retrieval (Brain)

```bash
make index
python3 -m brain retrieve "What is retrieval-augmented generation?" --context
```

### Premium Dataset Build

```bash
make product-premium-smoke   # 25,000 documents — local validation
make product-premium         # Full premium pipeline
make evaluate                # Benchmark evidence report
```

---

## Platform API Highlights

| Feature | Endpoint |
|---------|----------|
| Tenant registration | `POST /v1/tenants` |
| API key auth | `X-API-Key` or Bearer token |
| Workspaces & collections | `/v1/workspaces`, `/v1/collections` |
| Ingest text / URL / file | `/v1/collections/{id}/documents/*` |
| Async indexing | `POST /v1/collections/{id}/index` |
| Hybrid retrieval | `POST /v1/collections/{id}/retrieve` |
| RAG chat | `POST /v1/chat/completions` |

Full guide: [docs/api/getting-started.md](docs/api/getting-started.md)

---

## Product Tiers

### Platform (SaaS)

| Tier | Collections | Documents | Queries/day |
|------|-------------|-----------|-------------|
| Free | 1 | 1,000 | 500 |
| Starter | 5 | 25,000 | 10,000 |
| Professional | 25 | 250,000 | 100,000 |
| Enterprise | Unlimited | Unlimited | Unlimited |

See [docs/sales/pricing.md](docs/sales/pricing.md)

### Dataset Export

| Tier | Command | Scope |
|------|---------|-------|
| Smoke | `make product-premium-smoke` | 25,000 documents |
| Premium | `make product-premium` | Full configuration |
| Hyper | `make product-hyper` | Uncapped streaming generation |

---

## Retrieval Engine

The `brain/` package implements hybrid RAG retrieval:

```
brain/
├── brain.py           # Coltex orchestrator
├── ingestion/         # Markdown + frontmatter parsing
├── embeddings/        # Sentence-transformer encoding
├── indexing/          # ChromaDB vector store
├── metadata/          # doc_type, category filtering
├── graph/             # Multi-hop GraphRAG traversal
├── reranking/         # Source-weighted merging
└── retrieval/         # End-to-end pipeline
```

Pipeline: **embed query → vector search → metadata filter → graph expand → rerank → context**

---

## Knowledge Base & Corpus

- **340+ curated CHUNK documents** — RAG, GraphRAG, K8s, security, vector stores, and more
- **Procedural expansion** — `make expand-curated-kb`, `make generate-mega`
- **Platform docs** — CHUNK-00500+ enterprise deployment and API reference
- **Compliance** — Apache-2.0 synthetic corpus, `PROVENANCE.md`, distribution audit

---

## Deployment

| Method | Guide |
|--------|-------|
| Docker Compose | [docs/deployment/docker.md](docs/deployment/docker.md) |
| Kubernetes + HPA | [deploy/kubernetes/coltex-platform.yaml](deploy/kubernetes/coltex-platform.yaml) |
| Architecture | [docs/architecture/platform-architecture.md](docs/architecture/platform-architecture.md) |

---

## Sales & Commercial

Ready-to-use materials for selling Coltex:

- [Sales overview](docs/sales/overview.md) — pitch, proof points, demo flow
- [Pricing & packaging](docs/sales/pricing.md) — platform tiers, dataset SKUs, reseller program
- [Feature matrix](docs/sales/feature-matrix.md) — competitive comparison by tier

---

## Quality & Compliance

```bash
make validate-product      # Metadata, chunk size, duplication checks
make audit-distribution    # License, provenance, content compliance
make evaluate              # Retrieval recall@k benchmark report
make test                  # Platform API tests
```

| Gate | Threshold |
|------|-----------|
| Maximum duplicate chunk ratio | ≤ 5% |
| Metadata accuracy | ≥ 90% |
| Retrieval recall@8 | ≥ 45–50% (tier-dependent) |

---

## Repository Structure

```
.
├── coltex_platform/        # RAG-as-a-Service API (FastAPI)
├── brain/                  # Hybrid retrieval engine + CLI
├── knowledge-base/         # Curated + generated document corpus
├── scripts/product/        # Dataset build, audit, export pipeline
├── deploy/kubernetes/      # Production K8s manifests
├── docs/
│   ├── api/                # API getting started
│   ├── architecture/       # Platform architecture
│   ├── deployment/         # Docker & K8s guides
│   └── sales/              # Pricing, features, pitch materials
├── examples/               # RAG query + platform client examples
├── benchmarks/             # Evaluation datasets and reports
├── Dockerfile
└── docker-compose.yml
```

---

## Documentation

- [Platform API guide](docs/api/getting-started.md)
- [Platform architecture](docs/architecture/platform-architecture.md)
- [Product setup](docs/product-setup.md)
- [Quality standards](docs/product-quality.md)
- [Evaluation guide](docs/product-evaluation.md)
- [Licensing](docs/product-licensing.md)
- [Content provenance](knowledge-base/PROVENANCE.md)

---

## License

Licensed under the [End User License Agreement](EULA). Third-party dependencies are listed in [NOTICE](NOTICE).
