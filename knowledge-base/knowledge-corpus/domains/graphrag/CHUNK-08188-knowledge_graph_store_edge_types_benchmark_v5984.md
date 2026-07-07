---
id: CHUNK-08188-KNOWLEDGE-GRAPH-STORE-EDGE-TYPES-BENCHMARK-V5984
title: "Chunk 08188 Knowledge Graph Store: Edge Types \u2014 Benchmark (v5984)"
category: CHUNK-08188-knowledge_graph_store_edge_types_benchmark_v5984.md
tags:
- knowledge_graph_store
- edge types
- graphrag
- benchmark
- graphrag
- variant_5984
difficulty: intermediate
related:
- CHUNK-08187
- CHUNK-08186
- CHUNK-08185
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-08188
title: "Knowledge Graph Store: Edge Types \u2014 Benchmark (v5984)"
category: graphrag
doc_type: benchmark
tags:
- knowledge_graph_store
- edge types
- graphrag
- benchmark
- graphrag
- variant_5984
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Edge Types — Benchmark (v5984)

## Suite

In practice, **Suite** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 5984 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

In practice, **Methodology** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 5984 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

In practice, **Dataset** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 5984 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — Knowledge Graph Store: Edge Types benchmark variant 5984.

| Metric | Value |
|--------|-------|
| recall@10 | 0.80 |
| p95 latency (ms) | 89880 |
| error rate | 5.9850 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — Knowledge Graph Store: Edge Types benchmark variant 5984.

| Metric | Value |
|--------|-------|
| recall@10 | 0.80 |
| p95 latency (ms) | 89880 |
| error rate | 5.9850 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

In practice, **Comparison** for `Knowledge Graph Store: Edge Types` (benchmark). This variant 5984 covers knowledge_graph_store, edge types, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS graphrag_984 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 5984,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_graphrag_984_topic ON graphrag_984 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM graphrag_984
WHERE topic = 'knowledge_graph_store_edge_types' ORDER BY created_at DESC LIMIT 50;
```
