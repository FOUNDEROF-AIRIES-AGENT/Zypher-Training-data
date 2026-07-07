# Coltex Platform Overview

**Coltex — The Knowledge Operating System for AI**

Coltex is enterprise knowledge intelligence: a unified OS for understanding, connecting, reasoning over, retrieving from, and improving organizational knowledge — not a vector database with a file browser.

---

## The shift

| Storage-centric | Intelligence-centric |
|-----------------|---------------------|
| Store → Retrieve | Understand → Connect → Reason → Retrieve → Improve |
| Index documents | Intelligence Engine improves the corpus |
| Search metrics | Knowledge Health operational scores |
| Static corpus | Knowledge Lifecycle (Created → Published → Archived) |
| Monolithic codebase | Extensible plugins, hooks, and event subscribers |

The **enterprise RAG vector dataset** remains a foundation deliverable. The **Knowledge Intelligence Engine** is the heart.

---

## Platform stack

```
┌─────────────────────────────────────────────────────────────────┐
│  Knowledge Studio · Governance · Lifecycle · Extensibility      │
├─────────────────────────────────────────────────────────────────┤
│  ★ Knowledge Intelligence Engine · Knowledge Health · AI Memory   │
├─────────────────────────────────────────────────────────────────┤
│  Reasoning Layer (intent → plan → retrieve → rank → evidence)   │
├─────────────────────────────────────────────────────────────────┤
│  Event Bus · Scheduler · Connectors · Plugins                   │
├─────────────────────────────────────────────────────────────────┤
│  Graph · Embeddings · Chunks · Trust & Provenance               │
├─────────────────────────────────────────────────────────────────┤
│  Dataset · Audit · Licensing  (available today)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core capabilities

### Available today

- **Knowledge dataset** — 13k+ documents, 83k+ chunks, 52k+ graph edges
- **Knowledge graph** — hubs, routes, 20 relationship types, GraphRAG
- **Search & retrieval** — hybrid RAG with GraphRouter
- **Quality & audit** — distribution audit, benchmarks, provenance
- **Memory tier model** — working, episodic, semantic, procedural (corpus)

### On the roadmap

- **Knowledge Intelligence Engine** — discover, detect, recommend, improve
- **Knowledge Health** — operational dashboard scores
- **Event system & scheduler** — event-driven pipeline, automated jobs
- **Reasoning layer** — full intent-to-evidence pipeline
- **Knowledge lifecycle & AI governance** — state machine, retention, audit
- **Extensibility** — plugins, hooks, SDK
- **Knowledge Studio, connectors, sync** — experience and integration layer

See [Knowledge OS](knowledge-os.md) · [Intelligence Engine](intelligence-engine.md) · [Roadmap](roadmap.md)

---

## Config manifests

| Manifest | Purpose |
|----------|---------|
| [events.yaml](../../config/events.yaml) | Event-driven pipeline |
| [knowledge-lifecycle.yaml](../../config/knowledge-lifecycle.yaml) | Document state machine |
| [scheduler.yaml](../../config/scheduler.yaml) | Automated maintenance jobs |
| [governance.yaml](../../config/governance.yaml) | Retention, access, audit |
| [extensibility.yaml](../../config/extensibility.yaml) | Plugins and hooks |
| [connectors.yaml](../../config/connectors.yaml) | Source connectors |

---

## Target buyers

| Segment | Primary value |
|---------|---------------|
| **Enterprise IT / Knowledge managers** | Knowledge OS with health, lifecycle, governance |
| **AI / ML teams** | Reasoning layer + intelligence over RAG corpus |
| **Platform engineering** | Event-driven, extensible knowledge infrastructure |
| **Compliance / Legal** | Provenance, audit trail, retention policies |
| **DevOps / SRE** | Living docs, scheduler, connector sync (roadmap) |

---

## Related documents

- [Knowledge OS](knowledge-os.md) — product vision
- [Intelligence Engine](intelligence-engine.md) — core intelligence architecture
- [Platform roadmap](roadmap.md) — feature specifications
- [Product overview](../commercial/product-overview.md) — commercial packaging
