---
id: CHUNK-07495-GOOGLE-CLOUD-RUN-SERVICES-BENCHMARK-V5291
title: "Chunk 07495 Google Cloud Run Services \u2014 Benchmark (v5291)"
category: CHUNK-07495-google_cloud_run_services_benchmark_v5291.md
tags:
- cloud_run
- gke
- iam
- autoscaling
- benchmark
- gcp
- variant_5291
difficulty: intermediate
related:
- CHUNK-07494
- CHUNK-07493
- CHUNK-07492
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-07495
title: "Google Cloud Run Services \u2014 Benchmark (v5291)"
category: gcp
doc_type: benchmark
tags:
- cloud_run
- gke
- iam
- autoscaling
- benchmark
- gcp
- variant_5291
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_gcp
---

# Google Cloud Run Services — Benchmark (v5291)

## Suite

From first principles, **Suite** for `Google Cloud Run Services` (benchmark). This variant 5291 covers cloud_run, gke, iam, autoscaling at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

From first principles, **Methodology** for `Google Cloud Run Services` (benchmark). This variant 5291 covers cloud_run, gke, iam, autoscaling at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

From first principles, **Dataset** for `Google Cloud Run Services` (benchmark). This variant 5291 covers cloud_run, gke, iam, autoscaling at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — Google Cloud Run Services benchmark variant 5291.

| Metric | Value |
|--------|-------|
| recall@10 | 0.74 |
| p95 latency (ms) | 79485 |
| error rate | 5.2920 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — Google Cloud Run Services benchmark variant 5291.

| Metric | Value |
|--------|-------|
| recall@10 | 0.74 |
| p95 latency (ms) | 79485 |
| error rate | 5.2920 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

From first principles, **Comparison** for `Google Cloud Run Services` (benchmark). This variant 5291 covers cloud_run, gke, iam, autoscaling at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS gcp_291 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 5291,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_gcp_291_topic ON gcp_291 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM gcp_291
WHERE topic = 'gcp_cloud_run' ORDER BY created_at DESC LIMIT 50;
```
