---
id: CHUNK-03089-INCIDENT-COMMAND-SYSTEM-POSTMORTEM-API-REFERENCE-V885
title: "Chunk 03089 Incident Command System: Postmortem \u2014 Api Reference (v885)"
category: CHUNK-03089-incident_command_system_postmortem_api_reference_v885.md
tags:
- incident_command
- postmortem
- incidents
- api_reference
- incidents
- variant_885
difficulty: intermediate
related:
- CHUNK-03088
- CHUNK-03087
- CHUNK-03086
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-03089
title: "Incident Command System: Postmortem \u2014 Api Reference (v885)"
category: incidents
doc_type: api_reference
tags:
- incident_command
- postmortem
- incidents
- api_reference
- incidents
- variant_885
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: incident_command
---

# Incident Command System: Postmortem — Api Reference (v885)

## Endpoint

During incident response, **Endpoint** for `Incident Command System: Postmortem` (api_reference). This variant 885 covers incident_command, postmortem, incidents at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

During incident response, **Authentication** for `Incident Command System: Postmortem` (api_reference). This variant 885 covers incident_command, postmortem, incidents at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

During incident response, **Request Schema** for `Incident Command System: Postmortem` (api_reference). This variant 885 covers incident_command, postmortem, incidents at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

During incident response, **Response Schema** for `Incident Command System: Postmortem` (api_reference). This variant 885 covers incident_command, postmortem, incidents at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

During incident response, **Error Codes** for `Incident Command System: Postmortem` (api_reference). This variant 885 covers incident_command, postmortem, incidents at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```sql
CREATE TABLE IF NOT EXISTS incidents_885 (
    id          BIGSERIAL PRIMARY KEY,
    topic       TEXT NOT NULL,
    variant     INTEGER NOT NULL DEFAULT 885,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incidents_885_topic ON incidents_885 (topic);

EXPLAIN ANALYZE
SELECT id, topic, payload FROM incidents_885
WHERE topic = 'incident_command_postmortem' ORDER BY created_at DESC LIMIT 50;
```
