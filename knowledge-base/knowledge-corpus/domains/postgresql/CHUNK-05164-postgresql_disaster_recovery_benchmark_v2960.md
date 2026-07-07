---
id: CHUNK-05164-POSTGRESQL-DISASTER-RECOVERY-BENCHMARK-V2960
title: "Chunk 05164 PostgreSQL: Disaster Recovery \u2014 Benchmark (v2960)"
category: CHUNK-05164-postgresql_disaster_recovery_benchmark_v2960.md
tags:
- postgresql
- disaster_recovery
- postgresql
- benchmark
- postgresql
- variant_2960
difficulty: advanced
related:
- CHUNK-05163
- CHUNK-05162
- CHUNK-05161
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-05164
title: "PostgreSQL: Disaster Recovery \u2014 Benchmark (v2960)"
category: postgresql
doc_type: benchmark
tags:
- postgresql
- disaster_recovery
- postgresql
- benchmark
- postgresql
- variant_2960
difficulty: advanced
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_postgresql
---

# PostgreSQL: Disaster Recovery — Benchmark (v2960)

## Suite

In practice, **Suite** for `PostgreSQL: Disaster Recovery` (benchmark). This variant 2960 covers postgresql, disaster_recovery, postgresql at advanced level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

In practice, **Methodology** for `PostgreSQL: Disaster Recovery` (benchmark). This variant 2960 covers postgresql, disaster_recovery, postgresql at advanced level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

In practice, **Dataset** for `PostgreSQL: Disaster Recovery` (benchmark). This variant 2960 covers postgresql, disaster_recovery, postgresql at advanced level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — PostgreSQL: Disaster Recovery benchmark variant 2960.

| Metric | Value |
|--------|-------|
| recall@10 | 0.72 |
| p95 latency (ms) | 44520 |
| error rate | 2.9610 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — PostgreSQL: Disaster Recovery benchmark variant 2960.

| Metric | Value |
|--------|-------|
| recall@10 | 0.72 |
| p95 latency (ms) | 44520 |
| error rate | 2.9610 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

In practice, **Comparison** for `PostgreSQL: Disaster Recovery` (benchmark). This variant 2960 covers postgresql, disaster_recovery, postgresql at advanced level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS postgresql_960 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 2960,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_postgresql_960_topic ON postgresql_960 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM postgresql_960
WHERE topic = 'postgresql_disaster_recovery' ORDER BY created_at DESC LIMIT 50;
```
