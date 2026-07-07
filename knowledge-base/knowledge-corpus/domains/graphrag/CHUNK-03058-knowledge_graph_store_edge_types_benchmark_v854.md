---
id: CHUNK-03058-KNOWLEDGE-GRAPH-STORE-EDGE-TYPES-BENCHMARK-V854
title: "Chunk 03058 Knowledge Graph Store: Edge Types \u2014 Benchmark (v854)"
category: CHUNK-03058-knowledge_graph_store_edge_types_benchmark_v854.md
tags:
- knowledge_graph_store
- edge types
- graphrag
- benchmark
- graphrag
- variant_854
difficulty: intermediate
related:
- CHUNK-03057
- CHUNK-03056
- CHUNK-03055
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-03058
title: "Knowledge Graph Store: Edge Types \u2014 Benchmark (v854)"
category: graphrag
doc_type: benchmark
tags:
- knowledge_graph_store
- edge types
- graphrag
- benchmark
- graphrag
- variant_854
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Edge Types — Benchmark (v854)

## Suite

For security-sensitive deployments, **Suite** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 854 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

For security-sensitive deployments, **Methodology** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 854 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

For security-sensitive deployments, **Dataset** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 854 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — Knowledge Graph Store: Edge Types benchmark variant 854.

| Metric | Value |
|--------|-------|
| recall@10 | 0.80 |
| p95 latency (ms) | 12930 |
| error rate | 0.8550 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — Knowledge Graph Store: Edge Types benchmark variant 854.

| Metric | Value |
|--------|-------|
| recall@10 | 0.80 |
| p95 latency (ms) | 12930 |
| error rate | 0.8550 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

For security-sensitive deployments, **Comparison** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 854 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS graphrag_854 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 854,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_graphrag_854_topic ON graphrag_854 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM graphrag_854
WHERE topic = 'knowledge_graph_store_edge_types' ORDER BY created_at DESC LIMIT 50;
```
