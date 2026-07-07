---
id: CHUNK-00503-coltex_multi_tenant_security_model
title: Coltex Multi-Tenant Security Model
doc_type: best_practices
category: security
hub: coltex_platform
tags:
  - security
  - multi-tenancy
  - api-keys
depends_on:
  - CHUNK-00500
  - CHUNK-00501
related:
  - CHUNK-00502
---

# Coltex Multi-Tenant Security Model

## Isolation Layers

1. **Tenant boundary** — All store queries filter by `tenant_id`
2. **Collection filesystem** — Separate `kb/` and `vectors/` paths per collection
3. **ChromaDB collection** — Unique collection name per collection UUID
4. **API key scoping** — SHA-256 hashed keys with optional scope lists

## Authentication Flow

```
Client → X-API-Key header → SHA-256 lookup → tenant_id → authorize resource
```

- Keys never stored in plaintext
- `last_used_at` tracked for rotation audits
- Demo keys written once to `DEMO_API_KEY.txt` at bootstrap (disable in production)

## Tier Enforcement

| Limit | Enforcement Point |
|-------|-------------------|
| Collections | `POST /workspaces/{id}/collections` |
| Documents | Ingestion (roadmap: pre-check count) |
| Queries/day | `/retrieve` and `/chat/completions` → 429 |

## Production Hardening

- Rotate `auth.jwt_secret` in `config/platform.yaml`
- Restrict `cors_origins` to known domains
- Run behind TLS-terminating reverse proxy
- Use Kubernetes Secrets for `OPENAI_API_KEY`
- Enable network policies limiting egress to LLM provider

## Compliance Alignment

- Synthetic corpus — no PII in default knowledge base
- Customer-uploaded content stays in tenant-scoped paths
- Distribution audit script for commercial dataset exports
- EULA governs premium dataset redistribution
