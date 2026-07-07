---
id: CHUNK-08249-API-GATEWAY-KONG-BEST-PRACTICES-V6045
title: "Chunk 08249 API Gateway: Kong \u2014 Best Practices (v6045)"
category: CHUNK-08249-api_gateway_kong_best_practices_v6045.md
tags:
- api_gateway
- kong
- api_design
- best_practices
- api_design
- variant_6045
difficulty: intermediate
related:
- CHUNK-08248
- CHUNK-08247
- CHUNK-08246
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-08249
title: "API Gateway: Kong \u2014 Best Practices (v6045)"
category: api_design
doc_type: best_practices
tags:
- api_gateway
- kong
- api_design
- best_practices
- api_design
- variant_6045
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: api_gateway
---

# API Gateway: Kong — Best Practices (v6045)

## Principles

During incident response, **Principles** for `API Gateway: Kong` (best_practices). This variant 6045 covers api_gateway, kong, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

During incident response, **Do** for `API Gateway: Kong` (best_practices). This variant 6045 covers api_gateway, kong, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

During incident response, **Don't** for `API Gateway: Kong` (best_practices). This variant 6045 covers api_gateway, kong, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

During incident response, **Checklist** for `API Gateway: Kong` (best_practices). This variant 6045 covers api_gateway, kong, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

During incident response, **Examples** for `API Gateway: Kong` (best_practices). This variant 6045 covers api_gateway, kong, api_design at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```typescript
interface ApiGatewayKongConfig {
  topic: string;
  variant: number;
}

export async function handleApiGatewayKong(config: ApiGatewayKongConfig): Promise<Record<string, unknown>> {
  return { status: "ok", topic: config.topic, variant: config.variant };
}
```
