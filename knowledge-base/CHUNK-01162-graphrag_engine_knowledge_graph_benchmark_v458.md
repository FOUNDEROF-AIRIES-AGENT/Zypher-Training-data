---
id: CHUNK-01162-GRAPHRAG-ENGINE-KNOWLEDGE-GRAPH-BENCHMARK-V458
title: "Chunk 01162 GraphRAG Engine: Knowledge Graph \u2014 Benchmark (v458)"
category: CHUNK-01162-graphrag_engine_knowledge_graph_benchmark_v458.md
tags:
- graphrag_engine
- knowledge graph
- graphrag
- benchmark
- graphrag
- variant_458
difficulty: intermediate
related:
- CHUNK-01154
- CHUNK-01155
- CHUNK-01156
- CHUNK-01157
- CHUNK-01158
- CHUNK-01159
- CHUNK-01160
- CHUNK-01161
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-01162
title: "GraphRAG Engine: Knowledge Graph \u2014 Benchmark (v458)"
category: graphrag
doc_type: benchmark
tags:
- graphrag_engine
- knowledge graph
- graphrag
- benchmark
- graphrag
- variant_458
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: graphrag_engine
---

# GraphRAG Engine: Knowledge Graph — Benchmark (v458)

## Suite

When scaling to enterprise workloads, **Suite** for `GraphRAG Engine: Knowledge Graph` (benchmark). This variant 458 covers graphrag_engine, knowledge graph, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

When scaling to enterprise workloads, **Methodology** for `GraphRAG Engine: Knowledge Graph` (benchmark). This variant 458 covers graphrag_engine, knowledge graph, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

When scaling to enterprise workloads, **Dataset** for `GraphRAG Engine: Knowledge Graph` (benchmark). This variant 458 covers graphrag_engine, knowledge graph, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — GraphRAG Engine: Knowledge Graph benchmark variant 458.

| Metric | Value |
|--------|-------|
| recall@10 | 0.88 |
| p95 latency (ms) | 6990 |
| error rate | 0.4590 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — GraphRAG Engine: Knowledge Graph benchmark variant 458.

| Metric | Value |
|--------|-------|
| recall@10 | 0.88 |
| p95 latency (ms) | 6990 |
| error rate | 0.4590 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

When scaling to enterprise workloads, **Comparison** for `GraphRAG Engine: Knowledge Graph` (benchmark). This variant 458 covers graphrag_engine, knowledge graph, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS graphrag_458 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 458,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_graphrag_458_topic ON graphrag_458 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM graphrag_458
WHERE topic = 'graphrag_engine_knowledge_graph' ORDER BY created_at DESC LIMIT 50;
```
