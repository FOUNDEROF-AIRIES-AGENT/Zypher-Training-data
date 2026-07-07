---
id: CHUNK-08183-KNOWLEDGE-GRAPH-STORE-EDGE-TYPES-API-REFERENCE-V5979
title: "Chunk 08183 Knowledge Graph Store: Edge Types \u2014 Api Reference (v5979)"
category: CHUNK-08183-knowledge_graph_store_edge_types_api_reference_v5979.md
tags:
- knowledge_graph_store
- edge types
- graphrag
- api_reference
- graphrag
- variant_5979
difficulty: intermediate
related:
- CHUNK-08182
- CHUNK-08181
- CHUNK-08180
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-08183
title: "Knowledge Graph Store: Edge Types \u2014 Api Reference (v5979)"
category: graphrag
doc_type: api_reference
tags:
- knowledge_graph_store
- edge types
- graphrag
- api_reference
- graphrag
- variant_5979
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Edge Types — Api Reference (v5979)

## Endpoint

From first principles, **Endpoint** for `Knowledge Graph Store: Edge Types` (api_reference). This variant 5979 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

From first principles, **Authentication** for `Knowledge Graph Store: Edge Types` (api_reference). This variant 5979 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

From first principles, **Request Schema** for `Knowledge Graph Store: Edge Types` (api_reference). This variant 5979 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

From first principles, **Response Schema** for `Knowledge Graph Store: Edge Types` (api_reference). This variant 5979 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

From first principles, **Error Codes** for `Knowledge Graph Store: Edge Types` (api_reference). This variant 5979 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS graphrag_979 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 5979,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_graphrag_979_topic ON graphrag_979 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM graphrag_979
WHERE topic = 'knowledge_graph_store_edge_types' ORDER BY created_at DESC LIMIT 50;
```
