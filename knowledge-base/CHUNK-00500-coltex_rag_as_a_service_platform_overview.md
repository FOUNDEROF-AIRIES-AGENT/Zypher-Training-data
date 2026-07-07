---
id: CHUNK-00500-coltex_rag_as_a_service_platform_overview
title: Coltex RAG-as-a-Service Platform Overview
doc_type: documentation
category: rag
hub: coltex_platform
tags:
  - coltex
  - rag-as-a-service
  - enterprise
  - saas
related:
  - CHUNK-00000
  - CHUNK-00001
see_also:
  - CHUNK-00501
  - CHUNK-00502
---

# Coltex RAG-as-a-Service Platform Overview

Coltex is a production-grade **Retrieval-Augmented Generation as a Service (RaaS)** platform that combines:

1. **Multi-tenant REST API** — workspaces, collections, API keys, usage metering
2. **Hybrid retrieval engine** — vector search + metadata filtering + GraphRAG expansion
3. **Ingestion pipelines** — text, URL, and file upload with async indexing jobs
4. **RAG chat completions** — OpenAI-compatible generation with citation tracking
5. **Premium dataset export** — distributable chunks, embeddings, graph edges, and benchmarks

## Architecture Layers

| Layer | Package | Purpose |
|-------|---------|---------|
| Platform API | `coltex_platform/` | FastAPI gateway, auth, tenancy, jobs |
| Brain | `brain/` | Coltex retrieval orchestrator |
| Product | `scripts/product/` | Dataset build, audit, manifest signing |

## Key Differentiators

- **Graph-aware retrieval**: Documents link via typed frontmatter edges (`depends_on`, `see_also`, `implements`)
- **Tier-based SaaS limits**: Free through Enterprise with collection and query quotas
- **Compliance-ready corpus**: Synthetic Apache-2.0 content with PROVENANCE.md and distribution audit
- **Deploy anywhere**: Docker Compose, Kubernetes with HPA, or embedded via Python SDK

## Getting Started

```bash
pip install -r requirements.txt
python -m coltex_platform
curl http://localhost:8080/docs
```

See `docs/api/getting-started.md` for the full API walkthrough.
