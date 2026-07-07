---
id: CHUNK-08258-API-GATEWAY-RATE-LIMITS-BEST-PRACTICES-V6054
title: "Chunk 08258 API Gateway: Rate Limits \u2014 Best Practices (v6054)"
category: CHUNK-08258-api_gateway_rate_limits_best_practices_v6054.md
tags:
- api_gateway
- rate limits
- api_design
- best_practices
- api_design
- variant_6054
difficulty: intermediate
related:
- CHUNK-08257
- CHUNK-08256
- CHUNK-08255
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-08258
title: "API Gateway: Rate Limits \u2014 Best Practices (v6054)"
category: api_design
doc_type: best_practices
tags:
- api_gateway
- rate limits
- api_design
- best_practices
- api_design
- variant_6054
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: api_gateway
---

# API Gateway: Rate Limits — Best Practices (v6054)

## Principles

For security-sensitive deployments, **Principles** for `API Gateway: Rate Limits` (best_practices). This variant 6054 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

For security-sensitive deployments, **Do** for `API Gateway: Rate Limits` (best_practices). This variant 6054 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

For security-sensitive deployments, **Don't** for `API Gateway: Rate Limits` (best_practices). This variant 6054 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

For security-sensitive deployments, **Checklist** for `API Gateway: Rate Limits` (best_practices). This variant 6054 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

For security-sensitive deployments, **Examples** for `API Gateway: Rate Limits` (best_practices). This variant 6054 covers api_gateway, rate limits, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
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
