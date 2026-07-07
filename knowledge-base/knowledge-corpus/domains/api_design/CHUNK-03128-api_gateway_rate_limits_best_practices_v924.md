---
id: CHUNK-03128-API-GATEWAY-RATE-LIMITS-BEST-PRACTICES-V924
title: "Chunk 03128 API Gateway: Rate Limits \u2014 Best Practices (v924)"
category: CHUNK-03128-api_gateway_rate_limits_best_practices_v924.md
tags:
- api_gateway
- rate limits
- api_design
- best_practices
- api_design
- variant_924
difficulty: intermediate
related:
- CHUNK-03127
- CHUNK-03126
- CHUNK-03125
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-03128
title: "API Gateway: Rate Limits \u2014 Best Practices (v924)"
category: api_design
doc_type: best_practices
tags:
- api_gateway
- rate limits
- api_design
- best_practices
- api_design
- variant_924
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: api_gateway
---

# API Gateway: Rate Limits — Best Practices (v924)

## Principles

Under high load, **Principles** for `API Gateway: Rate Limits` (best_practices). This variant 924 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

Under high load, **Do** for `API Gateway: Rate Limits` (best_practices). This variant 924 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

Under high load, **Don't** for `API Gateway: Rate Limits` (best_practices). This variant 924 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

Under high load, **Checklist** for `API Gateway: Rate Limits` (best_practices). This variant 924 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

Under high load, **Examples** for `API Gateway: Rate Limits` (best_practices). This variant 924 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```typescript
interface ApiGatewayRateLimitsConfig {
  topic: string;
  variant: number;
}

export async function handleApiGatewayRateLimits(config: ApiGatewayRateLimitsConfig): Promise<Record<string, unknown>> {
  return { status: "ok", topic: config.topic, variant: config.variant };
}
```
