---
id: CHUNK-02347-AWS-LAMBDA-SERVERLESS-PATTERNS-BENCHMARK-V143
title: "Chunk 02347 AWS Lambda Serverless Patterns \u2014 Benchmark (v143)"
category: CHUNK-02347-aws_lambda_serverless_patterns_benchmark_v143.md
tags:
- lambda
- api_gateway
- iam
- cold_start
- benchmark
- aws
- variant_143
difficulty: intermediate
related:
- CHUNK-02346
- CHUNK-02345
- CHUNK-02344
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-02347
title: "AWS Lambda Serverless Patterns \u2014 Benchmark (v143)"
category: aws
doc_type: benchmark
tags:
- lambda
- api_gateway
- iam
- cold_start
- benchmark
- aws
- variant_143
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_aws
---

# AWS Lambda Serverless Patterns — Benchmark (v143)

## Suite

When integrating with legacy systems, **Suite** for `AWS Lambda Serverless Patterns` (benchmark). This variant 143 covers lambda, api_gateway, iam, cold_start at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

When integrating with legacy systems, **Methodology** for `AWS Lambda Serverless Patterns` (benchmark). This variant 143 covers lambda, api_gateway, iam, cold_start at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

When integrating with legacy systems, **Dataset** for `AWS Lambda Serverless Patterns` (benchmark). This variant 143 covers lambda, api_gateway, iam, cold_start at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — AWS Lambda Serverless Patterns benchmark variant 143.

| Metric | Value |
|--------|-------|
| recall@10 | 0.78 |
| p95 latency (ms) | 2265 |
| error rate | 0.1440 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — AWS Lambda Serverless Patterns benchmark variant 143.

| Metric | Value |
|--------|-------|
| recall@10 | 0.78 |
| p95 latency (ms) | 2265 |
| error rate | 0.1440 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

When integrating with legacy systems, **Comparison** for `AWS Lambda Serverless Patterns` (benchmark). This variant 143 covers lambda, api_gateway, iam, cold_start at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS aws_143 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 143,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_aws_143_topic ON aws_143 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM aws_143
WHERE topic = 'aws_lambda' ORDER BY created_at DESC LIMIT 50;
```
