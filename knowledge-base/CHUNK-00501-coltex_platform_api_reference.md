---
id: CHUNK-00501-coltex_platform_api_reference
title: Coltex Platform API Reference
doc_type: api_reference
category: rag
hub: coltex_platform
tags:
  - api
  - rest
  - openapi
depends_on:
  - CHUNK-00500
related:
  - CHUNK-00502
---

# Coltex Platform API Reference

Base URL: `http://localhost:8080` (configurable via `config/platform.yaml`)

## Authentication

All authenticated endpoints require an API key:

```
X-API-Key: ctx_<token>
Authorization: Bearer ctx_<token>
```

## Core Endpoints

### Tenants & Keys

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/tenants` | Register tenant (public) |
| GET | `/v1/me` | Current tenant profile |
| GET | `/v1/me/usage` | Daily usage vs tier limits |
| POST | `/v1/api-keys` | Create API key |
| GET | `/v1/api-keys` | List keys (prefix only) |

### Workspaces & Collections

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/workspaces` | Create workspace |
| GET | `/v1/workspaces` | List workspaces |
| POST | `/v1/workspaces/{id}/collections` | Create collection |
| GET | `/v1/collections` | List collections |
| GET | `/v1/collections/{id}` | Get collection |

### Ingestion & Indexing

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/collections/{id}/documents/text` | Ingest raw text |
| POST | `/v1/collections/{id}/documents/url` | Fetch and ingest URL |
| POST | `/v1/collections/{id}/documents/upload` | Upload file (multipart) |
| GET | `/v1/collections/{id}/documents` | List documents |
| POST | `/v1/collections/{id}/index` | Trigger index job (202) |
| GET | `/v1/collections/{id}/jobs/{job_id}` | Poll job status |

### RAG

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/collections/{id}/retrieve` | Hybrid retrieval + context |
| POST | `/v1/chat/completions` | RAG chat with citations |

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/v1/status` | Platform statistics |
| GET | `/openapi.json` | OpenAPI 3.1 spec |
| GET | `/docs` | Swagger UI |

## Response Codes

- `201` — Resource created
- `202` — Index job accepted
- `401` — Invalid API key
- `403` — Tier limit exceeded
- `429` — Daily query quota exceeded

## Example: Retrieve

```json
POST /v1/collections/{id}/retrieve
{
  "query": "How does GraphRAG work?",
  "top_k": 8,
  "include_context": true
}
```

Response includes ranked documents with scores, sources (vector/metadata/graph), and assembled context window.
