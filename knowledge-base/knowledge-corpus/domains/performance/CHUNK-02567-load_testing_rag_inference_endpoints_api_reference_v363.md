---
id: CHUNK-02567-LOAD-TESTING-RAG-INFERENCE-ENDPOINTS-API-REFERENCE-V363
title: "Chunk 02567 Load Testing RAG Inference Endpoints \u2014 Api Reference (v363)"
category: CHUNK-02567-load_testing_rag_inference_endpoints_api_reference_v363.md
tags:
- k6
- locust
- throughput
- latency
- api_reference
- performance
- variant_363
difficulty: intermediate
related:
- CHUNK-02566
- CHUNK-02565
- CHUNK-02564
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02567
title: "Load Testing RAG Inference Endpoints \u2014 Api Reference (v363)"
category: performance
doc_type: api_reference
tags:
- k6
- locust
- throughput
- latency
- api_reference
- performance
- variant_363
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_performance
---

# Load Testing RAG Inference Endpoints — Api Reference (v363)

## Endpoint

From first principles, **Endpoint** for `Load Testing RAG Inference Endpoints` (api_reference). This variant 363 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

From first principles, **Authentication** for `Load Testing RAG Inference Endpoints` (api_reference). This variant 363 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

From first principles, **Request Schema** for `Load Testing RAG Inference Endpoints` (api_reference). This variant 363 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

From first principles, **Response Schema** for `Load Testing RAG Inference Endpoints` (api_reference). This variant 363 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

From first principles, **Error Codes** for `Load Testing RAG Inference Endpoints` (api_reference). This variant 363 covers k6, locust, throughput, latency at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: performance-svc
spec:
  replicas: 363
  template:
    spec:
      containers:
        - name: app
          image: coltex/performance-svc:363
          env:
            - name: TOPIC
              value: "load_testing"
```
