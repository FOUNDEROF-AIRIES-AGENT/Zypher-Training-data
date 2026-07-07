---
id: CHUNK-07565-OPENTELEMETRY-FOR-RAG-PIPELINES-BEST-PRACTICES-V5361
title: "Chunk 07565 OpenTelemetry for RAG Pipelines \u2014 Best Practices (v5361)"
category: CHUNK-07565-opentelemetry_for_rag_pipelines_best_practices_v5361.md
tags:
- opentelemetry
- traces
- metrics
- spans
- best_practices
- observability
- variant_5361
difficulty: intermediate
related:
- CHUNK-07564
- CHUNK-07563
- CHUNK-07562
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-07565
title: "OpenTelemetry for RAG Pipelines \u2014 Best Practices (v5361)"
category: observability
doc_type: best_practices
tags:
- opentelemetry
- traces
- metrics
- spans
- best_practices
- observability
- variant_5361
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_observability
---

# OpenTelemetry for RAG Pipelines — Best Practices (v5361)

## Principles

For production systems, **Principles** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 5361 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

For production systems, **Do** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 5361 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

For production systems, **Don't** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 5361 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

For production systems, **Checklist** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 5361 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

For production systems, **Examples** for `OpenTelemetry for RAG Pipelines` (best_practices). This variant 5361 covers opentelemetry, traces, metrics, spans at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```typescript
interface OtelObservabilityConfig {
  topic: string;
  variant: number;
}

export async function handleOtelObservability(config: OtelObservabilityConfig): Promise<Record<string, unknown>> {
  return { status: "ok", topic: config.topic, variant: config.variant };
}
```
