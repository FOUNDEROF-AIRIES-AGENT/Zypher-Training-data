# Coltex Runtime

The live centerpiece of the Knowledge Operating System — not a specification, not a repository layout.

```bash
python3 -m runtime status      # All engines
python3 -m runtime health      # Knowledge analytics
python3 -m runtime curator     # AI Curator recommendations
python3 -m runtime ingest DOC  # Event-driven pipeline
python3 -m runtime events --simulate
python3 -m runtime dna --limit 5
python3 -m runtime search "GraphRAG routing"
```

Makefile shortcuts: `make runtime-status`, `make runtime-health`, `make runtime-curator`, `make runtime-events`

---

## Runtime architecture

```
Coltex Runtime
├── Intelligence Engine    — relationship discovery, quality analysis
├── Search Engine          — hybrid knowledge object search
├── Memory Engine          — working → archive memory tiers
├── Scheduler              — automated maintenance jobs
├── Event Bus              — event-driven pipeline
├── Plugin Manager         — extensibility registry
├── Knowledge Studio       — explorer, graph, health, lifecycle (API)
├── Retrieval Engine       — intent-ready retrieval wrapper
├── Graph Engine           — topology and neighbors
├── AI Curator             — merge, staleness, regen recommendations
├── Analytics Engine       — knowledge quality metrics
├── API Gateway            — runtime status and health endpoints
└── Security               — access and audit gateway
```

Config: [config/runtime.yaml](../../config/runtime.yaml)

---

## Event-driven pipeline

Every ingest runs the full cascade:

```
Document Uploaded
       ↓
Chunk Created
       ↓
Embedding Generated
       ↓
Knowledge Graph Updated
       ↓
Search Index Updated
       ↓
Health Score Updated
       ↓
Analytics Updated
       ↓
Subscribers Notified
```

Events logged to `data/runtime/events.jsonl`. Manifest: [config/events.yaml](../../config/events.yaml)

---

## Knowledge DNA

Every knowledge object carries identity — AI retrieves **objects**, not files:

| Field | Purpose |
|-------|---------|
| `source` | Connector or origin |
| `parent` / `children` | Object hierarchy |
| `dependencies` | Required upstream knowledge |
| `confidence` | Extraction confidence |
| `freshness` | Recency score |
| `quality_score` | Composite health |
| `usage_count` | Retrieval frequency |
| `related_concepts` | Semantic + graph concepts |
| `evolution_state` | v1 → merged → deprecated → archived |

Schema: [config/knowledge-dna.yaml](../../config/knowledge-dna.yaml)

---

## Knowledge Evolution

Not just version history — governed evolution:

```
v1 → v2 → Merged → Expanded → Deprecated → Archived
```

Config: [config/knowledge-evolution.yaml](../../config/knowledge-evolution.yaml)

---

## AI Curator

Active recommendations:

- "These N documents should be merged"
- "This documentation is outdated / low quality"
- "Embeddings should be regenerated"
- "Graph is disconnected"
- "Broken references detected"

```bash
python3 -m runtime curator
```

---

## Knowledge Studio

Unified experience surface (API available today; UI roadmap):

Explorer · Search · Graph · Relationships · Analytics · Health · Lifecycle · Scheduler · Plugins · Connectors

---

## Connectors & Marketplace

Connectors feed the runtime event pipeline: GitHub → Confluence → Notion → Drive → Jira → Slack → SQL → **Coltex Runtime**

- Connectors: [config/connectors.yaml](../../config/connectors.yaml)
- Marketplace: [config/marketplace.yaml](../../config/marketplace.yaml)

---

## Related

- [Knowledge OS](knowledge-os.md)
- [Intelligence Engine](intelligence-engine.md)
- [Platform roadmap](roadmap.md)
