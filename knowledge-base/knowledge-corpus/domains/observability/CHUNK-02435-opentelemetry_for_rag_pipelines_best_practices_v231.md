---
id: CHUNK-02435-OPENTELEMETRY-FOR-RAG-PIPELINES-BEST-PRACTICES-V231
title: "Chunk 02435 OpenTelemetry for RAG Pipelines \u2014 Best Practices (v231)"
category: CHUNK-02435-opentelemetry_for_rag_pipelines_best_practices_v231.md
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
- CHUNK-02434
- CHUNK-02433
- CHUNK-02432
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02435
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
hub: domain_observability
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

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: observability-svc
spec:
  replicas: 231
  template:
    spec:
      containers:
        - name: app
          image: coltex/observability-svc:231
          env:
            - name: TOPIC
              value: "otel_observability"
```
