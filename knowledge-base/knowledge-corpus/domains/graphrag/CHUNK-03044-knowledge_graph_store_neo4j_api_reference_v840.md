---
id: CHUNK-03044-KNOWLEDGE-GRAPH-STORE-NEO4J-API-REFERENCE-V840
title: "Chunk 03044 Knowledge Graph Store: Neo4j \u2014 Api Reference (v840)"
category: CHUNK-03044-knowledge_graph_store_neo4j_api_reference_v840.md
tags:
- knowledge_graph_store
- neo4j
- graphrag
- api_reference
- graphrag
- variant_840
difficulty: intermediate
related:
- CHUNK-03043
- CHUNK-03042
- CHUNK-03041
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-03044
title: "Knowledge Graph Store: Neo4j \u2014 Api Reference (v840)"
category: graphrag
doc_type: api_reference
tags:
- knowledge_graph_store
- neo4j
- graphrag
- api_reference
- graphrag
- variant_840
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Neo4j — Api Reference (v840)

## Endpoint

In practice, **Endpoint** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 840 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

In practice, **Authentication** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 840 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

In practice, **Request Schema** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 840 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

In practice, **Response Schema** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 840 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

In practice, **Error Codes** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 840 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS graphrag_840 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 840,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_graphrag_840_topic ON graphrag_840 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM graphrag_840
WHERE topic = 'knowledge_graph_store_neo4j' ORDER BY created_at DESC LIMIT 50;
```
