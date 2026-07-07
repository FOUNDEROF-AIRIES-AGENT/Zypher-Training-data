---
id: CHUNK-00935-OPENTELEMETRY-FOR-RAG-PIPELINES-BEST-PRACTICES-V231
title: "Chunk 00935 OpenTelemetry for RAG Pipelines \u2014 Best Practices (v231)"
category: CHUNK-00935-opentelemetry_for_rag_pipelines_best_practices_v231.md
tags:
- opentelemetry
- traces
- metrics
- spans
- best_practices
- observability
- variant_231
difficulty: intermediate
related:
- CHUNK-00927
- CHUNK-00928
- CHUNK-00929
- CHUNK-00930
- CHUNK-00931
- CHUNK-00932
- CHUNK-00933
- CHUNK-00934
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-00935
title: "OpenTelemetry for RAG Pipelines \u2014 Best Practices (v231)"
category: observability
doc_type: best_practices
tags:
- opentelemetry
- traces
- metrics
- spans
- best_practices
- observability
- variant_231
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
---

# OpenTelemetry for RAG Pipelines — Best Practices (v231)

## Principles

When integrating with legacy systems, **Principles** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 231 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

When integrating with legacy systems, **Do** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 231 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

When integrating with legacy systems, **Don't** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 231 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

When integrating with legacy systems, **Checklist** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 231 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

When integrating with legacy systems, **Examples** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 231 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS observability_231 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 231,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_observability_231_topic ON observability_231 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM observability_231
WHERE topic = 'otel_observability' ORDER BY created_at DESC LIMIT 50;
```
