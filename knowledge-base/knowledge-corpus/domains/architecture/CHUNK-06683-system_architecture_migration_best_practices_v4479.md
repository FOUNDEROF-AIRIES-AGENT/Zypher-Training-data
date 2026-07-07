---
id: CHUNK-06683-SYSTEM-ARCHITECTURE-MIGRATION-BEST-PRACTICES-V4479
title: "Chunk 06683 System Architecture: Migration \u2014 Best Practices (v4479)"
category: CHUNK-06683-system_architecture_migration_best_practices_v4479.md
tags:
- architecture
- migration
- system
- best_practices
- architecture
- variant_4479
difficulty: expert
related:
- CHUNK-06682
- CHUNK-06681
- CHUNK-06680
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-06683
title: "System Architecture: Migration \u2014 Best Practices (v4479)"
category: architecture
doc_type: best_practices
tags:
- architecture
- migration
- system
- best_practices
- architecture
- variant_4479
difficulty: expert
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_architecture
---

# System Architecture: Migration — Best Practices (v4479)

## Principles

When integrating with legacy systems, **Principles** for `System Architecture: Migration` (best_practices). This variant 4479 covers architecture, migration, system at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

When integrating with legacy systems, **Do** for `System Architecture: Migration` (best_practices). This variant 4479 covers architecture, migration, system at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

When integrating with legacy systems, **Don't** for `System Architecture: Migration` (best_practices). This variant 4479 covers architecture, migration, system at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

When integrating with legacy systems, **Checklist** for `System Architecture: Migration` (best_practices). This variant 4479 covers architecture, migration, system at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

When integrating with legacy systems, **Examples** for `System Architecture: Migration` (best_practices). This variant 4479 covers architecture, migration, system at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS architecture_479 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 4479,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_architecture_479_topic ON architecture_479 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM architecture_479
WHERE topic = 'architecture_migration' ORDER BY created_at DESC LIMIT 50;
```
