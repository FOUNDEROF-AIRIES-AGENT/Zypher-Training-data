---
id: CHUNK-02905-RAG-RETRIEVAL-CORE-HYBRID-SEARCH-BENCHMARK-V701
title: "Chunk 02905 RAG Retrieval Core: Hybrid Search \u2014 Benchmark (v701)"
category: CHUNK-02905-rag_retrieval_core_hybrid_search_benchmark_v701.md
tags:
- rag_retrieval_core
- hybrid search
- rag
- benchmark
- rag
- variant_701
difficulty: intermediate
related:
- CHUNK-02904
- CHUNK-02903
- CHUNK-02902
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02905
title: "RAG Retrieval Core: Hybrid Search \u2014 Benchmark (v701)"
category: rag
doc_type: benchmark
tags:
- rag_retrieval_core
- hybrid search
- rag
- benchmark
- rag
- variant_701
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: rag_retrieval_core
---

# RAG Retrieval Core: Hybrid Search — Benchmark (v701)

## Suite

During incident response, **Suite** for `RAG Retrieval Core: Hybrid Search` (benchmark). This variant 701 covers rag_retrieval_core, hybrid search, rag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

During incident response, **Methodology** for `RAG Retrieval Core: Hybrid Search` (benchmark). This variant 701 covers rag_retrieval_core, hybrid search, rag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

During incident response, **Dataset** for `RAG Retrieval Core: Hybrid Search` (benchmark). This variant 701 covers rag_retrieval_core, hybrid search, rag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — RAG Retrieval Core: Hybrid Search benchmark variant 701.

| Metric | Value |
|--------|-------|
| recall@10 | 0.74 |
| p95 latency (ms) | 10635 |
| error rate | 0.7020 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — RAG Retrieval Core: Hybrid Search benchmark variant 701.

| Metric | Value |
|--------|-------|
| recall@10 | 0.74 |
| p95 latency (ms) | 10635 |
| error rate | 0.7020 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

During incident response, **Comparison** for `RAG Retrieval Core: Hybrid Search` (benchmark). This variant 701 covers rag_retrieval_core, hybrid search, rag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-svc
spec:
  replicas: 701
  template:
    spec:
      containers:
        - name: app
          image: coltex/rag-svc:701
          env:
            - name: TOPIC
              value: "rag_retrieval_core_hybrid_search"
```
