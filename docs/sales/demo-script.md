# Coltex Demo Script (15 minutes)

Use this script for sales calls, investor demos, and conference booths.

## Setup (before the call)

```bash
docker compose up -d --build
export KEY=$(grep ctx_ data/platform/DEMO_API_KEY.txt)
export API=http://localhost:8080
```

## Act 1: The Problem (2 min)

> "Most RAG projects stall at the POC stage. Teams bolt together a vector DB and an LLM, but they lack hybrid retrieval, multi-tenancy, compliance evidence, and a path to production."

Pain points to mention:
- Vector-only search misses structured metadata
- No graph relationships between docs
- No benchmark proof for buyers
- No API for product integration

## Act 2: Platform Live Demo (8 min)

### Health & tenant
```bash
curl -s $API/health | jq
curl -s -H "X-API-Key: $KEY" $API/v1/me | jq
```

> "Every customer gets isolated workspaces and collections with tier-based quotas."

### Create collection & ingest
```bash
WS=$(curl -s -H "X-API-Key: $KEY" $API/v1/workspaces | jq -r '.[0].id')
COL=$(curl -s -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"name":"Sales Demo","slug":"demo-'$(date +%s)'"}' \
  $API/v1/workspaces/$WS/collections | jq -r '.id')

curl -s -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"title":"Acme Deploy Runbook","content":"# Deploy\n\n1. Run terraform apply\n2. Verify health checks\n3. Roll out via ArgoCD","doc_type":"runbook","category":"kubernetes"}' \
  $API/v1/collections/$COL/documents/text | jq
```

### Index & retrieve
```bash
JOB=$(curl -s -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"force_reindex":true}' $API/v1/collections/$COL/index | jq -r '.id')
sleep 5
curl -s -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"query":"How do I deploy to production?","include_context":true}' \
  $API/v1/collections/$COL/retrieve | jq '.documents[:3]'
```

> "Notice hybrid scoring — vector, metadata, and graph sources merged with weighted reranking."

### RAG chat
```bash
curl -s -X POST -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Walk me through the deployment steps"}],"collection_id":"'$COL'"}' \
  $API/v1/chat/completions | jq '.message.content, .citations'
```

## Act 3: Dataset Product (3 min)

```bash
make product-premium-smoke  # if pre-built, show artifacts
ls -la data/product/
cat data/product/manifest.json | jq '.checksums | keys[:5]'
cat benchmarks/evaluation_report.json | jq '.recall_at_k'
```

> "Buyers get checksum-signed artifacts, 200+ benchmark pairs, and a distribution audit — not a zip of random PDFs."

## Act 4: Close (2 min)

Offer paths:
1. **Starter Platform** — $299/mo, self-hosted Docker
2. **Premium Dataset** — $1,000 one-time, 25K docs + benchmarks
3. **Enterprise** — Custom VPC, SSO, professional services

Leave-behind: `docs/sales/overview.md`, `docs/sales/pricing.md`

## Objection Handling

| Objection | Response |
|-----------|----------|
| "We use Pinecone" | Coltex is retrieval + dataset + compliance; export embeddings to any vector DB |
| "We built our own" | Show recall@8 benchmarks and GraphRAG — most POCs are vector-only |
| "Content licensing?" | 100% synthetic Apache-2.0 corpus with PROVENANCE.md and audit script |
| "Scale?" | Hyper tier: 604T+ procedural combinations; K8s HPA to 20 pods |
