# Knowledge Intelligence Engine

The heart of Coltex. The Intelligence Engine transforms Coltex from a storage and retrieval system into a system that **actively improves organizational knowledge**.

---

## Purpose

Traditional RAG tools index documents and answer questions. Coltex goes further:

| Storage-centric | Intelligence-centric |
|-----------------|-------------------|
| Index documents | Understand document meaning and role |
| Return chunks | Connect relationships across the corpus |
| Report search latency | Detect contradictions and staleness |
| Manual deduplication | Recommend merges automatically |
| Static graph | Evolve graph as knowledge changes |

---

## Core capabilities

### 1. Relationship discovery

Automatically infer edges not explicitly authored:

- Semantic similarity above threshold → `related`
- Shared hub/domain + cross-references → `see_also`
- API version chains → `supersedes` / `deprecated_by`
- Runbook → service dependency → `depends_on`

Feeds the knowledge graph without manual linking.

### 2. Contradiction detection

Compare documents on the same topic for conflicting claims:

```
Doc A: "API v2 uses OAuth2"
Doc B: "API v2 uses API keys only"
         │
         ▼
Contradiction flagged → notify owner → suggest resolution
```

### 3. Staleness & deprecation detection

Track document age, source sync timestamps, and explicit deprecation markers:

```
API v2 → status: Deprecated
         │
         ▼
Engine finds 18 documents referencing API v2
         │
         ├──► Suggest replacements
         ├──► Update graph (deprecated_by edges)
         └──► Emit knowledge.deprecation.detected event
```

### 4. Duplicate detection

Near-duplicate chunks and documents via content hash + embedding similarity:

- Flag duplicate risk percentage (Knowledge Health metric)
- Recommend merge or archive
- Preserve provenance of merged sources

### 5. Merge recommendations

When duplicates or overlapping docs are detected:

- Propose canonical document
- Show diff of unique content to preserve
- One-click merge with graph rewiring (Knowledge Studio)

### 6. Documentation improvement suggestions

Gap analysis driven by taxonomy and search logs:

- Missing doc types per domain (e.g., no runbook for Auth hub)
- Weak coverage areas (low graph density)
- Under-linked documents (orphan nodes)

---

## Architecture

```
                    ┌─────────────────────────────┐
                    │   Knowledge Intelligence    │
                    │         Engine              │
                    └─────────────┬───────────────┘
                                  │
        ┌────────────┬────────────┼────────────┬────────────┐
        ▼            ▼            ▼            ▼            ▼
   Discover     Detect        Detect       Recommend    Improve
   relations   contradictions  stale/       merges       docs
                              duplicate
        │            │            │            │            │
        └────────────┴────────────┴────────────┴────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │  Event Bus → Scheduler →    │
                    │  Health Dashboard → Notify  │
                    └─────────────────────────────┘
```

---

## Knowledge Health integration

The Intelligence Engine continuously feeds Knowledge Health scores:

| Metric | Engine contribution |
|--------|---------------------|
| Knowledge Score | Weighted composite of all sub-scores |
| Coverage | Taxonomy gap analysis |
| Duplicate Risk | Duplicate detector output |
| Outdated Docs | Staleness + deprecation scanner |
| Broken References | Graph integrity validator |
| Graph Integrity | Orphan and dangling edge detection |

Example dashboard target:

```
Knowledge Score     94%
Coverage            98%
Duplicate Risk       3%
Outdated Docs         12
Broken References      4
Graph Integrity     96%
```

Today's foundation: `make audit-distribution`, `make evaluate`, duplicate ratio checks in product config.

---

## Reasoning layer integration

The Intelligence Engine informs retrieval — not replaces it:

```
User question
      │
      ▼
Intent Detection ──► Intelligence context (contradictions, staleness flags)
      │
      ▼
Planner ──► selects retrieval strategy (graph expand vs. vector only)
      │
      ▼
Retriever + Re-ranker
      │
      ▼
Reasoning ──► resolves conflicts, prefers verified/published sources
      │
      ▼
Evidence Assembly ──► cites provenance per chunk
      │
      ▼
Answer
```

Today's `brain retrieve` + GraphRouter implements retrieval and partial graph reasoning. Full pipeline on roadmap.

---

## Event emissions

The engine emits events for downstream systems:

| Event | Trigger |
|-------|---------|
| `knowledge.contradiction.detected` | Conflicting documents found |
| `knowledge.duplicate.detected` | Near-duplicate above threshold |
| `knowledge.deprecation.detected` | Deprecated entity with dependents |
| `knowledge.merge.recommended` | Merge candidate pair identified |
| `knowledge.gap.detected` | Taxonomy or hub coverage gap |
| `knowledge.health.updated` | Health scores recalculated |

See [config/events.yaml](../../config/events.yaml).

---

## Extensibility

Third parties can register intelligence plugins:

```yaml
# Example plugin registration (roadmap SDK)
plugin:
  id: custom_compliance_checker
  type: intelligence
  hooks: [post_ingest, nightly_scan]
  handler: my_module.check_compliance
```

See [config/extensibility.yaml](../../config/extensibility.yaml).

---

## Implementation status

| Capability | Status |
|------------|--------|
| Distribution audit & substance checks | Available |
| Duplicate ratio gate (build time) | Available |
| GraphRouter relationship expansion | Available |
| Retrieval benchmarks | Available |
| Continuous intelligence scans | Roadmap |
| Contradiction & staleness detection | Roadmap |
| Merge recommendations | Roadmap |
| Health dashboard UI | Roadmap |

---

## Related documents

- [Knowledge OS](knowledge-os.md) — product vision
- [Platform roadmap](roadmap.md) — delivery phases
- [Extensibility manifest](../../config/extensibility.yaml)
