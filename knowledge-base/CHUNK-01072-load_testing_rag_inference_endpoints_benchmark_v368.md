---
id: CHUNK-01072-LOAD-TESTING-RAG-INFERENCE-ENDPOINTS-BENCHMARK-V368
title: "Chunk 01072 Load Testing RAG Inference Endpoints \u2014 Benchmark (v368)"
category: CHUNK-01072-load_testing_rag_inference_endpoints_benchmark_v368.md
tags:
- k6
- locust
- throughput
- latency
- benchmark
- performance
- variant_368
difficulty: intermediate
related:
- CHUNK-01064
- CHUNK-01065
- CHUNK-01066
- CHUNK-01067
- CHUNK-01068
- CHUNK-01069
- CHUNK-01070
- CHUNK-01071
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-01072
title: "Load Testing RAG Inference Endpoints \u2014 Benchmark (v368)"
category: performance
doc_type: benchmark
tags:
- k6
- locust
- throughput
- latency
- benchmark
- performance
- variant_368
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
---

# Load Testing RAG Inference Endpoints — Benchmark (v368)

## Suite

In practice, **Suite** for `Load Testing RAG Inference Endpoints` (benchmark). This variant 368 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

In practice, **Methodology** for `Load Testing RAG Inference Endpoints` (benchmark). This variant 368 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

In practice, **Dataset** for `Load Testing RAG Inference Endpoints` (benchmark). This variant 368 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — Load Testing RAG Inference Endpoints benchmark variant 368.

| Metric | Value |
|--------|-------|
| recall@10 | 0.88 |
| p95 latency (ms) | 5640 |
| error rate | 0.3690 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — Load Testing RAG Inference Endpoints benchmark variant 368.

| Metric | Value |
|--------|-------|
| recall@10 | 0.88 |
| p95 latency (ms) | 5640 |
| error rate | 0.3690 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

In practice, **Comparison** for `Load Testing RAG Inference Endpoints` (benchmark). This variant 368 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS performance_368 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 368,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_performance_368_topic ON performance_368 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM performance_368
WHERE topic = 'load_testing' ORDER BY created_at DESC LIMIT 50;
```
