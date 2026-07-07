# Coltex Platform API — Getting Started

## Quick Start

### 1. Start the platform

```bash
pip install -r requirements.txt
python -m coltex_platform
# Or: docker compose up -d
```

API docs: http://localhost:8080/docs

### 2. Get your API key

On first boot, a demo tenant is created. Find the key at:

```
data/platform/DEMO_API_KEY.txt
```

Or register a new tenant (no auth required):

```bash
curl -X POST http://localhost:8080/v1/tenants \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Corp","email":"admin@acme.com","tier":"starter"}'

curl -X POST http://localhost:8080/v1/api-keys \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Production"}'
```

### 3. Create a workspace and collection

```bash
export COLTEX_KEY="ctx_..."

curl -X POST http://localhost:8080/v1/workspaces \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Engineering","slug":"engineering"}'

curl -X POST http://localhost:8080/v1/workspaces/{workspace_id}/collections \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Runbooks","slug":"runbooks","description":"Ops documentation"}'
```

### 4. Ingest documents

**Text:**
```bash
curl -X POST http://localhost:8080/v1/collections/{collection_id}/documents/text \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Deploy Guide","content":"# Deploy\n\nRun make deploy...","doc_type":"runbook"}'
```

**File upload:**
```bash
curl -X POST http://localhost:8080/v1/collections/{collection_id}/documents/upload \
  -H "X-API-Key: $COLTEX_KEY" \
  -F "file=@docs/runbook.md"
```

**URL:**
```bash
curl -X POST http://localhost:8080/v1/collections/{collection_id}/documents/url \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/docs"}'
```

### 5. Index and query

```bash
# Trigger async index job
curl -X POST http://localhost:8080/v1/collections/{collection_id}/index \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'

# Poll job status
curl http://localhost:8080/v1/collections/{collection_id}/jobs/{job_id} \
  -H "X-API-Key: $COLTEX_KEY"

# Retrieve
curl -X POST http://localhost:8080/v1/collections/{collection_id}/retrieve \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I deploy?","top_k":5,"include_context":true}'

# RAG chat
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "X-API-Key: $COLTEX_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages":[{"role":"user","content":"Explain our deployment process"}],
    "collection_id": "{collection_id}",
    "top_k": 8
  }'
```

## Authentication

Pass your API key via:
- Header: `X-API-Key: ctx_...`
- Bearer: `Authorization: Bearer ctx_...`

## OpenAI Integration

Set `OPENAI_API_KEY` and update `config/platform.yaml`:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
```

## Rate Limits

| Tier | Queries/day |
|------|-------------|
| free | 500 |
| starter | 10,000 |
| professional | 100,000 |
| enterprise | unlimited |

Check usage: `GET /v1/me/usage`

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Invalid/missing API key |
| 403 | Tier limit exceeded |
| 404 | Resource not found |
| 413 | Upload too large |
| 429 | Daily query limit |
| 202 | Index job accepted |

Full OpenAPI spec: http://localhost:8080/openapi.json
