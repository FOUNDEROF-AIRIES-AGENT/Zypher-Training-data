# Coltex Feature Matrix

## Retrieval Engine

| Feature | Free | Starter | Pro | Enterprise | Notes |
|---------|:----:|:-------:|:---:|:----------:|-------|
| Vector search (MiniLM) | ✅ | ✅ | ✅ | ✅ | ChromaDB HNSW |
| Metadata filtering | ✅ | ✅ | ✅ | ✅ | doc_type, category, hub |
| GraphRAG expansion | ✅ | ✅ | ✅ | ✅ | Multi-hop frontmatter edges |
| Source-weighted reranking | ✅ | ✅ | ✅ | ✅ | vector 1.0 / metadata 0.85 / graph 0.65 |
| Custom embedding models | ❌ | ❌ | ✅ | ✅ | Bring your own encoder |
| Hybrid BM25 + dense | ❌ | ❌ | 🔜 | ✅ | Roadmap Q3 |
| Cross-encoder reranker | ❌ | ❌ | 🔜 | ✅ | Roadmap Q3 |

## Platform API

| Feature | Free | Starter | Pro | Enterprise |
|---------|:----:|:-------:|:---:|:----------:|
| REST API + OpenAPI | ✅ | ✅ | ✅ | ✅ |
| API key auth | ✅ | ✅ | ✅ | ✅ |
| Multi-tenant isolation | ✅ | ✅ | ✅ | ✅ |
| Workspaces & collections | ✅ | ✅ | ✅ | ✅ |
| Text / URL / file upload | ✅ | ✅ | ✅ | ✅ |
| Async indexing jobs | ✅ | ✅ | ✅ | ✅ |
| RAG chat completions | ✅ | ✅ | ✅ | ✅ |
| OpenAI provider | ✅ | ✅ | ✅ | ✅ |
| Webhooks | ❌ | ❌ | ✅ | ✅ |
| SSO | ❌ | ❌ | ❌ | ✅ |

## Ingestion Connectors

| Connector | Status | Tier |
|-----------|--------|------|
| Markdown / text | ✅ GA | All |
| File upload (md, txt, pdf, html) | ✅ GA | All |
| URL fetch | ✅ GA | All |
| Git repository | 🔜 Beta | Pro+ |
| S3 / GCS buckets | 🔜 Beta | Pro+ |
| Confluence | 📋 Planned | Enterprise |
| SharePoint | 📋 Planned | Enterprise |
| Slack export | 📋 Planned | Enterprise |

## Dataset Product

| Feature | Seed | Premium Smoke | Premium | Hyper |
|---------|:----:|:-------------:|:-------:|:-----:|
| Curated CHUNK documents | 500 | 25,000 | Full config | ∞ streaming |
| chunks.jsonl | ✅ | ✅ | ✅ | ✅ |
| embeddings.jsonl | ✅ | ✅ | ✅ | Optional |
| edges.jsonl (graph) | ✅ | ✅ | ✅ | ✅ |
| catalog.jsonl | ✅ | ✅ | ✅ | ✅ |
| manifest.json (SHA-256) | ✅ | ✅ | ✅ | ✅ |
| Benchmark suites (200+) | ✅ | ✅ | ✅ | ✅ |
| Distribution audit | ✅ | ✅ | ✅ | ✅ |
| EULA + provenance | ✅ | ✅ | ✅ | ✅ |

## Operations

| Feature | Self-hosted | Managed |
|---------|:-----------:|:-------:|
| Docker Compose | ✅ | — |
| Kubernetes + HPA | ✅ | ✅ |
| Health checks | ✅ | ✅ |
| Usage metering | ✅ | ✅ |
| OpenTelemetry | 🔜 | 🔜 |
| Multi-region | ❌ | Enterprise |

## Compliance

| Requirement | Coltex |
|-------------|--------|
| Synthetic/original corpus | ✅ PROVENANCE.md |
| No third-party doc copying | ✅ Audit script |
| Apache-2.0 dependencies | ✅ NOTICE |
| Commercial EULA | ✅ EULA |
| Checksum-signed artifacts | ✅ manifest.json |
