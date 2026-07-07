# Coltex — The Knowledge Operating System for AI

**Coltex Runtime** is the platform centerpiece — a live, event-driven knowledge operating system. Not a repository. Not a specification. A runtime.

```bash
python3 -m runtime status       # All engines online
python3 -m runtime health       # Knowledge analytics
python3 -m runtime curator      # AI Curator recommendations
python3 -m runtime ingest DOC   # Event-driven pipeline
```

[![Runtime](https://img.shields.io/badge/runtime-active-brightgreen.svg)](docs/platform/runtime.md)
[![Knowledge Score](https://img.shields.io/badge/knowledge%20OS-live-blue.svg)](docs/platform/knowledge-os.md)
[![Documents: 13k+](https://img.shields.io/badge/documents-13k%2B-green.svg)](docs/commercial/datasheet.md)
[![Graph edges: 52k+](https://img.shields.io/badge/graph%20edges-52k%2B-purple.svg)](docs/commercial/datasheet.md)

---

## Coltex Runtime

```
Coltex Runtime
├── Intelligence Engine      ├── Event Bus
├── Search Engine            ├── Plugin Manager
├── Memory Engine            ├── Knowledge Studio
├── Scheduler                ├── Retrieval Engine
├── Graph Engine             ├── AI Curator
├── Analytics Engine         ├── API Gateway
└── Security
```

| Command | Purpose |
|---------|---------|
| `python3 -m runtime status` | Engine status and platform health |
| `python3 -m runtime health` | Knowledge Quality, Coverage, Graph Integrity |
| `python3 -m runtime curator` | Merge, regen, disconnect, quality recommendations |
| `python3 -m runtime ingest <id>` | Full event pipeline |
| `python3 -m runtime dna` | Knowledge DNA for objects |
| `python3 -m runtime search "<query>"` | Search knowledge objects |

Full runtime docs: [docs/platform/runtime.md](docs/platform/runtime.md)

---

## Intelligence loop

```
Understand  →  Connect  →  Reason  →  Retrieve  →  Improve
```

The runtime executes this loop continuously — powered by the **Knowledge Intelligence Engine** and **AI Curator**.

---

## Event-driven — Coltex stays alive

```
Document Uploaded → Chunk Created → Embedding Generated → Graph Updated
    → Search Index Updated → Health Score Updated → Analytics Updated → Subscribers Notified
```

Every change propagates through the event bus. Log: `data/runtime/events.jsonl`

---

## Knowledge DNA

AI retrieves **knowledge objects**, not files. Every object stores:

`source` · `parent` · `children` · `dependencies` · `confidence` · `freshness` · `quality_score` · `usage_count` · `related_concepts` · `evolution_state`

---

## Knowledge Evolution

```
v1 → v2 → Merged → Expanded → Deprecated → Archived
```

---

## Knowledge Studio

Unified surface for: **Explorer · Search · Graph · Relationships · Analytics · Health · Lifecycle · Scheduler · Plugins · Connectors**

Runtime API available today. Visual UI on roadmap.

---

## Connectors → Runtime

```
GitHub → Confluence → Notion → Google Drive → Jira → Slack → SharePoint → SQL → Coltex Runtime
```

Everything synchronized through the event pipeline. [Connector manifest](config/connectors.yaml) · [Marketplace](config/marketplace.yaml)

---

## Platform components

| Component | Status |
|-----------|--------|
| **Coltex Runtime** | **Available** |
| Event Bus & ingest pipeline | Available |
| Knowledge DNA schema | Available |
| AI Curator | Available |
| Knowledge Analytics | Available |
| Intelligence / Search / Graph / Memory engines | Available |
| Knowledge Studio UI | Roadmap |
| Connector sync | Roadmap |
| Marketplace | Roadmap |
| AI Knowledge Builder | Roadmap |

Vision: [Knowledge OS](docs/platform/knowledge-os.md) · [Intelligence Engine](docs/platform/intelligence-engine.md) · [Roadmap](docs/platform/roadmap.md)

---

## Build the knowledge dataset

The enterprise RAG vector dataset is the foundation layer the runtime operates on:

```bash
pip install -r requirements.txt
make corpus-mega
make product-enterprise
make audit-distribution
make runtime-status
```

| Metric | Value |
|--------|-------|
| Curated documents | **12,993** |
| Vector chunks | **83,612** |
| Graph edges | **52,490** |
| Technology domains | **63** |

[Technical datasheet](docs/commercial/datasheet.md) · [Product setup](docs/product-setup.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [**Coltex Runtime**](docs/platform/runtime.md) | **Runtime architecture and CLI** |
| [Knowledge OS](docs/platform/knowledge-os.md) | Platform vision |
| [Intelligence Engine](docs/platform/intelligence-engine.md) | Core intelligence |
| [Platform roadmap](docs/platform/roadmap.md) | Feature specifications |
| [Licenses](licenses/README.md) | License tiers |
| [SKU matrix](docs/commercial/sku-matrix.md) | Package comparison |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.
