---
id: CHUNK-02603-API-CONTRACT-TESTING-WITH-PACT-API-REFERENCE-V399
title: "Chunk 02603 API Contract Testing with Pact \u2014 Api Reference (v399)"
category: CHUNK-02603-api_contract_testing_with_pact_api_reference_v399.md
tags:
- pact
- contracts
- consumer
- provider
- api_reference
- testing
- variant_399
difficulty: intermediate
related:
- CHUNK-02602
- CHUNK-02601
- CHUNK-02600
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02603
title: "API Contract Testing with Pact \u2014 Api Reference (v399)"
category: testing
doc_type: api_reference
tags:
- pact
- contracts
- consumer
- provider
- api_reference
- testing
- variant_399
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_testing
---

# API Contract Testing with Pact — Api Reference (v399)

## Endpoint

When integrating with legacy systems, **Endpoint** for `API Contract Testing with Pact` (api_reference). This variant 399 covers pact, contracts, consumer, provider at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

When integrating with legacy systems, **Authentication** for `API Contract Testing with Pact` (api_reference). This variant 399 covers pact, contracts, consumer, provider at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

When integrating with legacy systems, **Request Schema** for `API Contract Testing with Pact` (api_reference). This variant 399 covers pact, contracts, consumer, provider at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

When integrating with legacy systems, **Response Schema** for `API Contract Testing with Pact` (api_reference). This variant 399 covers pact, contracts, consumer, provider at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

When integrating with legacy systems, **Error Codes** for `API Contract Testing with Pact` (api_reference). This variant 399 covers pact, contracts, consumer, provider at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testing-svc
spec:
  replicas: 399
  template:
    spec:
      containers:
        - name: app
          image: coltex/testing-svc:399
          env:
            - name: TOPIC
              value: "contract_testing"
```
