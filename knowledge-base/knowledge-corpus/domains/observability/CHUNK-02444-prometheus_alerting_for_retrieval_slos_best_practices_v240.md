---
id: CHUNK-02444-PROMETHEUS-ALERTING-FOR-RETRIEVAL-SLOS-BEST-PRACTICES-V240
title: "Chunk 02444 Prometheus Alerting for Retrieval SLOs \u2014 Best Practices (v240)"
category: CHUNK-02444-prometheus_alerting_for_retrieval_slos_best_practices_v240.md
tags:
- prometheus
- alertmanager
- slo
- burn_rate
- best_practices
- observability
- variant_240
difficulty: intermediate
related:
- CHUNK-02443
- CHUNK-02442
- CHUNK-02441
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02444
title: "Prometheus Alerting for Retrieval SLOs \u2014 Best Practices (v240)"
category: observability
doc_type: best_practices
tags:
- prometheus
- alertmanager
- slo
- burn_rate
- best_practices
- observability
- variant_240
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_observability
---

# Prometheus Alerting for Retrieval SLOs — Best Practices (v240)

## Principles

In practice, **Principles** for `Prometheus Alerting for Retrieval SLOs` (best_practices). This variant 240 covers prometheus, alertmanager, slo, burn_rate at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

In practice, **Do** for `Prometheus Alerting for Retrieval SLOs` (best_practices). This variant 240 covers prometheus, alertmanager, slo, burn_rate at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

In practice, **Don't** for `Prometheus Alerting for Retrieval SLOs` (best_practices). This variant 240 covers prometheus, alertmanager, slo, burn_rate at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

In practice, **Checklist** for `Prometheus Alerting for Retrieval SLOs` (best_practices). This variant 240 covers prometheus, alertmanager, slo, burn_rate at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

In practice, **Examples** for `Prometheus Alerting for Retrieval SLOs` (best_practices). This variant 240 covers prometheus, alertmanager, slo, burn_rate at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```typescript
interface PrometheusAlertsConfig {
  topic: string;
  variant: number;
}

export async function handlePrometheusAlerts(config: PrometheusAlertsConfig): Promise<Record<string, unknown>> {
  return { status: "ok", topic: config.topic, variant: config.variant };
}
```
