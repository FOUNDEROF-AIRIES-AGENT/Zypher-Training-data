# Coltex RAG-as-a-Service — Sales Overview

Coltex is the **enterprise RAG platform** that turns your documents into production-ready AI knowledge — with hybrid retrieval, multi-tenant APIs, and a distributable dataset product you can sell or white-label.

## Why Coltex Wins Deals

| Capability | Coltex | Typical RAG POC |
|------------|--------|-----------------|
| Hybrid retrieval (vector + metadata + graph) | ✅ Built-in | ❌ Vector-only |
| Multi-tenant SaaS API | ✅ REST + OpenAPI | ❌ Single-tenant script |
| Pre-built enterprise corpus (25K–∞ docs) | ✅ Premium tiers | ❌ Empty index |
| Compliance & provenance | ✅ Apache-2.0 synthetic corpus | ⚠️ Unknown sources |
| Benchmark evidence | ✅ recall@8, FAQ gold sets | ❌ No eval harness |
| Docker + Kubernetes | ✅ Production manifests | ❌ Notebook only |

## Product Lines

### 1. Coltex Platform (RaaS)
Hosted or self-managed API for:
- Document ingestion (upload, URL, text)
- Async indexing jobs
- Hybrid retrieval with citations
- RAG chat completions (OpenAI-compatible)

### 2. Coltex Premium Dataset
Checksum-signed export bundle:
- `chunks.jsonl`, `embeddings.jsonl`, `edges.jsonl`
- 200+ benchmark pairs per tier
- Distribution audit & EULA

### 3. Coltex Enterprise
- Unlimited tenants/collections
- Dedicated vector stores
- Custom SLAs, SSO, VPC deployment
- Professional services for corpus curation

## Target Buyers

- **AI consultancies** — White-label RAG for clients in days, not months
- **SaaS vendors** — Embed knowledge search into existing products
- **Enterprise IT** — Internal docs, runbooks, ADRs with graph-aware retrieval
- **Data marketplaces** — Resell premium RAG datasets with provenance

## Proof Points

- **340+ curated seed documents** across 30+ technology categories
- **25,000-document smoke build** validated locally (`make product-premium-smoke`)
- **~69% recall@8** on curated evaluation set
- **604T+ procedural combinations** in hyper tier for infinite scale demos

## Demo Flow (5 minutes)

```bash
docker compose up -d
curl http://localhost:8080/health
# Use demo API key from data/platform/DEMO_API_KEY.txt
curl -H "X-API-Key: $KEY" http://localhost:8080/v1/me
curl -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"query":"What is GraphRAG?","include_context":true}' \
  http://localhost:8080/v1/collections/{id}/retrieve
```

## Contact & Licensing

- Platform code: Apache-2.0 compatible stack
- Premium dataset: Commercial EULA (`EULA`)
- Enterprise: Custom MSAs available

See [Pricing](pricing.md) and [Feature Matrix](feature-matrix.md).
