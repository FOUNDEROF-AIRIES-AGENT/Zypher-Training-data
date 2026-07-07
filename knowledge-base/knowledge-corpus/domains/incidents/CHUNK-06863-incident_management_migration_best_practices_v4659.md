---
id: CHUNK-06863-INCIDENT-MANAGEMENT-MIGRATION-BEST-PRACTICES-V4659
title: "Chunk 06863 Incident Management: Migration \u2014 Best Practices (v4659)"
category: CHUNK-06863-incident_management_migration_best_practices_v4659.md
tags:
- incidents
- migration
- incident
- best_practices
- incidents
- variant_4659
difficulty: expert
related:
- CHUNK-06862
- CHUNK-06861
- CHUNK-06860
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-06863
title: "Incident Management: Migration \u2014 Best Practices (v4659)"
category: incidents
doc_type: best_practices
tags:
- incidents
- migration
- incident
- best_practices
- incidents
- variant_4659
difficulty: expert
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: domain_incidents
---

# Incident Management: Migration — Best Practices (v4659)

## Principles

From first principles, **Principles** for `Incident Management: Migration` (best_practices). This variant 4659 covers incidents, migration, incident at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Do

From first principles, **Do** for `Incident Management: Migration` (best_practices). This variant 4659 covers incidents, migration, incident at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Don't

From first principles, **Don't** for `Incident Management: Migration` (best_practices). This variant 4659 covers incidents, migration, incident at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Checklist

From first principles, **Checklist** for `Incident Management: Migration` (best_practices). This variant 4659 covers incidents, migration, incident at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Examples

From first principles, **Examples** for `Incident Management: Migration` (best_practices). This variant 4659 covers incidents, migration, incident at expert level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS incidents_659 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 4659,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incidents_659_topic ON incidents_659 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM incidents_659
WHERE topic = 'incidents_migration' ORDER BY created_at DESC LIMIT 50;
```
