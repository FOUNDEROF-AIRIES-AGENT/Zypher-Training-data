# Coltex — The Knowledge Operating System for AI

**Start here:** `python3 -m runtime studio` — Knowledge Studio is the product.

```bash
pip install -r requirements.txt
python3 -m runtime studio          # Knowledge Studio (web UI)
python3 -m runtime health          # Knowledge Health dashboard
python3 -m runtime curator         # AI Curator proactive alerts
python3 -m runtime monitor         # Runtime monitoring
python3 -m runtime explain "query" # Retrieval explainability
```

---

## Use today

| Capability | Command | Status |
|------------|---------|--------|
| **Knowledge Studio** | `python3 -m runtime studio` | **Available** — Explorer, Health, Curator, Monitor, Search, Explain |
| **Knowledge Health** | `python3 -m runtime health` | **Available** — Score, Coverage, Duplicate Risk, Broken Refs |
| **AI Curator** | `python3 -m runtime curator` | **Available** — Proactive merge, quality, regen alerts |
| **Runtime Monitor** | `python3 -m runtime monitor` | **Available** — Memory, docs, embeddings, events, latency |
| **Explainability** | `python3 -m runtime explain "..."` | **Available** — Why each result was retrieved |
| **Event pipeline** | `python3 -m runtime ingest DOC` | **Available** — Full cascade + auto-curator |
| **Filesystem connector** | `python3 -m runtime connector filesystem` | **Available** |
| **Knowledge DNA** | `python3 -m runtime dna` | **Available** |
| **Plugin SDK** | `runtime/plugins/sdk.py` | **Available** — register connectors, curators, processors |
| GitHub / Notion / Slack sync | — | Roadmap |
| Marketplace | — | Roadmap |
| AI Knowledge Builder | — | Roadmap |

---

## Coltex Runtime

```
Coltex Runtime
├── Intelligence Engine    ├── Event Bus
├── Search Engine          ├── Plugin Manager
├── Memory Engine          ├── Knowledge Studio ★
├── Scheduler              ├── Retrieval Engine
├── Graph Engine           ├── AI Curator
├── Analytics Engine       ├── Explain Engine
├── API Gateway            └── Security
└── Runtime Monitor
```

---

## Knowledge Studio

Everything lives in one place:

**Explorer · Search · Graph · Analytics · Health · Curator · Lifecycle · Plugins · Connectors · Monitor · Explain**

Launch: `python3 -m runtime studio` → http://127.0.0.1:8787

---

## Knowledge Health

Metrics about **knowledge**, not users:

| Metric | What it means |
|--------|---------------|
| Knowledge Score | Composite corpus health |
| Coverage | Domain/taxonomy completeness |
| Freshness | Recency and connectivity |
| Duplicate Risk | Near-duplicate document ratio |
| Disconnected Graphs | Orphan documents |
| Broken References | Invalid graph links |
| Graph Integrity | Documents with valid edges |

```bash
python3 -m runtime health
```

---

## AI Curator (proactive)

Coltex tells you what to fix — you don't go looking:

- "24 documents should be merged"
- "Embeddings should be regenerated"
- "API documentation may be outdated"
- "These chunks have poor quality"
- "Graph has disconnected nodes"

Runs automatically after every ingest. Manual scan: `python3 -m runtime curator`

---

## Explainability

Ask why Coltex retrieved a result:

```bash
python3 -m runtime explain "JWT authentication flow"
```

Returns: Similarity · Graph Relationship · Metadata Match · API Match · Same Repository · Content Match

---

## Event-driven pipeline

```
Document Uploaded → Chunk Created → Embedding Generated → Graph Updated
  → Search Updated → Health Rescored → Analytics Updated → Curator Scan → Subscribers Notified
```

---

## Memory tiers

```
Working Memory → Project Memory → Organization Memory → Historical Memory → Archive
```

---

## Knowledge Evolution

```
Created → Reviewed → Verified → Published → Deprecated → Archived → Deleted
```

Also: Merged · Expanded evolution paths.

---

## Connectors & Plugin SDK

```bash
python3 -m runtime connector filesystem
python3 -m runtime connector github    # ready for webhook wiring
```

Extend via `runtime/plugins/sdk.py`:

```python
from runtime.plugins import sdk
sdk.register_connector("my_source", my_ingest_fn)
sdk.register_curator("my_curator", my_scan_fn)
```

---

## Build the dataset (foundation layer)

```bash
make product-enterprise
make audit-distribution
make runtime-health
```

| Documents | Chunks | Graph edges |
|-----------|--------|-------------|
| 12,993 | 83,612 | 52,490 |

[Technical datasheet](docs/commercial/datasheet.md) · [Runtime docs](docs/platform/runtime.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [**Knowledge Studio / Runtime**](docs/platform/runtime.md) | Runtime CLI and architecture |
| [Knowledge OS vision](docs/platform/knowledge-os.md) | Platform vision |
| [Intelligence Engine](docs/platform/intelligence-engine.md) | Intelligence architecture |
| [Roadmap](docs/platform/roadmap.md) | What's next |
| [Licenses](licenses/README.md) | License tiers |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.
