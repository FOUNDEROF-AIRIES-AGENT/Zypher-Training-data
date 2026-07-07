---
id: CHUNK-02867-OBSERVABILITY-STACK-OPENTELEMETRY-BEST-PRACTICES-V663
title: "Chunk 02867 Observability Stack: OpenTelemetry \u2014 Best Practices (v663)"
category: CHUNK-02867-observability_stack_opentelemetry_best_practices_v663.md
tags:
- observability_stack
- opentelemetry
- observability
- best_practices
- observability
- variant_663
difficulty: intermediate
related:
- CHUNK-02866
- CHUNK-02865
- CHUNK-02864
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02867
title: "Observability Stack: OpenTelemetry \u2014 Best Practices (v663)"
category: observability
doc_type: best_practices
tags:
- observability_stack
- opentelemetry
- observability
- best_practices
- observability
- variant_663
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: observability_stack
---

# Observability Stack: OpenTelemetry — Best Practices (v663)

## Principles

When integrating with legacy systems, **Principles** for `Observability Stack: OpenTelemetry` (best_practices). This variant 663 covers observability_stack, opentelemetry, observability at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

When integrating with legacy systems, **Do** for `Observability Stack: OpenTelemetry` (best_practices). This variant 663 covers observability_stack, opentelemetry, observability at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

When integrating with legacy systems, **Don't** for `Observability Stack: OpenTelemetry` (best_practices). This variant 663 covers observability_stack, opentelemetry, observability at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

When integrating with legacy systems, **Checklist** for `Observability Stack: OpenTelemetry` (best_practices). This variant 663 covers observability_stack, opentelemetry, observability at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

When integrating with legacy systems, **Examples** for `Observability Stack: OpenTelemetry` (best_practices). This variant 663 covers observability_stack, opentelemetry, observability at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: observability-svc
spec:
  replicas: 663
  template:
    spec:
      containers:
        - name: app
          image: coltex/observability-svc:663
          env:
            - name: TOPIC
              value: "observability_stack_opentelemetry"
```
