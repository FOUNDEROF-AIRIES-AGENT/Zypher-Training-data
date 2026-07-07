---
id: CHUNK-00502-coltex_enterprise_deployment_guide
title: Coltex Enterprise Deployment Guide
doc_type: guide
category: kubernetes
hub: coltex_platform
tags:
  - deployment
  - docker
  - kubernetes
  - enterprise
depends_on:
  - CHUNK-00500
  - CHUNK-00501
see_also:
  - CHUNK-00482
  - CHUNK-00488
---

# Coltex Enterprise Deployment Guide

## Deployment Options

| Option | Best For | Command |
|--------|----------|---------|
| Local dev | Engineers, demos | `python -m coltex_platform` |
| Docker Compose | Small prod, POC | `docker compose up -d` |
| Kubernetes | Enterprise scale | `kubectl apply -f deploy/kubernetes/` |
| Embedded | In-app RAG | `from brain.brain import Coltex` |

## Docker Compose Production

1. Set secrets: `OPENAI_API_KEY`, custom JWT secret in `config/platform.yaml`
2. Mount persistent volume for `coltex-data`
3. Place TLS-terminating reverse proxy in front
4. Restrict CORS to your application domain

```yaml
# docker-compose.yml excerpt
volumes:
  - coltex-data:/data
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## Kubernetes

Manifest: `deploy/kubernetes/coltex-platform.yaml`

Includes:
- Namespace `coltex`
- Deployment (2 replicas default)
- LoadBalancer Service
- PVC (50Gi)
- HPA (2–20 pods, 70% CPU target)

### Resource Requirements

| Component | Request | Limit |
|-----------|---------|-------|
| API pod | 2Gi RAM, 500m CPU | 8Gi RAM, 2 CPU |
| Index job (burst) | +4Gi RAM during embed | GPU optional |

## Security Hardening

1. **Rotate API keys** — Never commit `DEMO_API_KEY.txt`
2. **Network policies** — Restrict pod egress to LLM provider only
3. **Secrets management** — Use K8s Secrets or Vault for `OPENAI_API_KEY`
4. **Tenant isolation** — Each collection uses separate filesystem paths and Chroma collections

## Monitoring Checklist

- `/health` endpoint for liveness/readiness probes
- Track `GET /v1/me/usage` for quota alerting
- Index job failure rate via `GET /v1/collections/{id}/jobs`
- Disk usage on PVC (vector stores grow with documents)

## Scaling Path

1. **Phase 1**: Single-region K8s, 2–5 replicas
2. **Phase 2**: PostgreSQL for metadata (replace SQLite)
3. **Phase 3**: pgvector or dedicated vector DB per tenant tier
4. **Phase 4**: Multi-region with collection replication

## Sales Deployment Package

Enterprise customers receive:
- `docs/sales/` — Pitch deck content, pricing, feature matrix
- `deploy/kubernetes/` — Production manifests
- `docs/architecture/platform-architecture.md` — Technical deep dive
- Premium dataset bundle with manifest and audit report
