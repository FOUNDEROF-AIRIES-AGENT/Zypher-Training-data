# Coltex — The Knowledge Operating System for AI

Enterprise knowledge intelligence for organizations that need more than a vector database. Coltex is a **Knowledge OS** — it understands, connects, reasons over, retrieves from, and continuously improves organizational knowledge.

[![Knowledge Score](https://img.shields.io/badge/knowledge%20health-audit%20ready-green.svg)](docs/platform/intelligence-engine.md)
[![Graph edges: 52k+](https://img.shields.io/badge/graph%20edges-52k%2B-purple.svg)](docs/commercial/datasheet.md)
[![Domains: 63](https://img.shields.io/badge/domains-63-blue.svg)](docs/commercial/datasheet.md)
[![Knowledge OS](https://img.shields.io/badge/product-knowledge%20OS-blue.svg)](docs/platform/knowledge-os.md)

---

## Overview

Customers aren't buying vectors. They're buying an **operating system that manages organizational knowledge** — with intelligence at the center, not storage.

Coltex runs a continuous intelligence loop:

```
Understand  →  Connect  →  Reason  →  Retrieve  →  Improve
     │            │           │           │            │
  ingest &     graph &     planner &    hybrid      health,
  classify     relate      evidence     search      merges,
                                                      alerts
```

The enterprise RAG dataset, graph, and retrieval engine are **foundation layers**. The **Knowledge Intelligence Engine** is the heart — actively discovering relationships, detecting contradictions, scoring health, and recommending improvements.

Platform vision: [Knowledge OS](docs/platform/knowledge-os.md) · [Intelligence Engine](docs/platform/intelligence-engine.md) · [Roadmap](docs/platform/roadmap.md)

---

## Platform stack

Intelligence-first — not storage-first.

```
┌─────────────────────────────────────────────────────────────────┐
│  Knowledge Studio · Governance · Lifecycle · Extensibility      │
├─────────────────────────────────────────────────────────────────┤
│  ★ Knowledge Intelligence Engine · Knowledge Health · Memory    │
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

| Layer | Role | Status |
|-------|------|--------|
| **Knowledge Intelligence Engine** | Discover, detect, recommend, improve | Roadmap |
| **Knowledge Health** | Operational scores: coverage, duplicates, staleness | Roadmap |
| **AI Memory** | Working → Project → Org → Long-term → Archive | Partial |
| **Reasoning Layer** | Intent, planner, re-rank, evidence assembly | Partial |
| **Event System** | Event-driven pipeline propagation | Roadmap |
| **Knowledge Scheduler** | Nightly re-index, link scan, quality jobs | Roadmap |
| **Trust & Provenance** | Source, author, confidence, verification per chunk | Partial |
| **Knowledge Lifecycle** | Created → Reviewed → Verified → Published → Deprecated | Roadmap |
| **AI Governance** | Retention, access, audit, compliance reports | Roadmap |
| **Extensibility** | Plugins, hooks, custom connectors, SDK | Roadmap |
| **Dataset & Graph** | Corpus, edges, GraphRouter retrieval | Available |

Config manifests: [events](config/events.yaml) · [lifecycle](config/knowledge-lifecycle.yaml) · [scheduler](config/scheduler.yaml) · [governance](config/governance.yaml) · [extensibility](config/extensibility.yaml)

---

## Knowledge Intelligence Engine

The heart of Coltex. Not just indexing — **actively improving** the knowledge base.

```
API v2 marked Deprecated
         │
         ▼
Intelligence Engine detects 18 related documents
         │
         ├──► Suggest replacements & merges
         ├──► Update graph edges
         └──► Notify owner via event
```

Capabilities: relationship discovery · contradiction detection · stale doc alerts · duplicate detection · merge recommendations · documentation improvement suggestions.

Details: [Intelligence Engine](docs/platform/intelligence-engine.md)

---

## Knowledge Health

Enterprise operational insight — not just search metrics.

| Metric | Example | Meaning |
|--------|---------|---------|
| **Knowledge Score** | 94% | Overall corpus health |
| **Coverage** | 98% | Taxonomy completeness |
| **Duplicate Risk** | 3% | Near-duplicate chunk ratio |
| **Outdated Docs** | 12 | Stale or deprecated count |
| **Broken References** | 4 | Invalid see_also / related targets |
| **Graph Integrity** | 96% | Documents with valid edges |

Built on today's audit pipeline; continuous monitoring on the roadmap.

---

## Reasoning layer

Retrieval is not the answer. Reasoning is.

```
Question
    │
    ▼
Intent Detection
    │
    ▼
Planner
    │
    ▼
Retriever (vector + graph)
    │
    ▼
Re-ranking
    │
    ▼
Reasoning
    │
    ▼
Evidence Assembly
    │
    ▼
Answer
```

Today's `brain retrieve` + GraphRouter is the retrieval foundation. Full reasoning pipeline on the roadmap.

---

## Available today

| Capability | Detail |
|------------|--------|
| Curated documents | **12,993** |
| Vector chunks | **83,612** |
| Graph edges | **52,490** |
| Technology domains | **63** |
| GraphRouter retrieval | Region-aware hybrid RAG |
| Distribution audit | Compliance and quality gates |
| Memory tier model | Working, episodic, semantic, procedural (corpus) |

### Getting started

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make corpus-mega
make product-enterprise
make audit-distribution
make evaluate
```

```bash
make index
python3 -m brain retrieve "How does GraphRAG routing work?" --context
python3 -m brain report
```

Full specifications: [Technical datasheet](docs/commercial/datasheet.md) · [Product setup](docs/product-setup.md)

---

## Platform roadmap

### Intelligence & operations

1. [Knowledge Intelligence Engine](docs/platform/roadmap.md#knowledge-intelligence-engine) — discover, detect, recommend, improve
2. [Knowledge Health](docs/platform/roadmap.md#knowledge-health) — operational health dashboard
3. [AI Memory](docs/platform/roadmap.md#ai-memory) — working → org → archive tiers
4. [Event System](docs/platform/roadmap.md#event-system) — event-driven architecture
5. [Knowledge Scheduler](docs/platform/roadmap.md#knowledge-scheduler) — automated maintenance jobs
6. [Reasoning Layer](docs/platform/roadmap.md#reasoning-layer) — intent through evidence assembly
7. [Knowledge Lifecycle](docs/platform/roadmap.md#knowledge-lifecycle) — created through archived
8. [AI Governance](docs/platform/roadmap.md#ai-governance) — retention, access, compliance
9. [Extensibility](docs/platform/roadmap.md#extensibility) — plugins, hooks, SDK

### Experience & integration

10. [Knowledge Studio](docs/platform/roadmap.md#1-knowledge-studio) — visual knowledge management
11. [Connectors & Sync](docs/platform/roadmap.md#2-automatic-connectors) — living knowledge from GitHub, Notion, etc.

Connector manifest: [config/connectors.yaml](config/connectors.yaml)

---

## Documentation

| Document | Description |
|----------|-------------|
| [Knowledge OS](docs/platform/knowledge-os.md) | Product vision and mental model |
| [Intelligence Engine](docs/platform/intelligence-engine.md) | Core intelligence architecture |
| [Platform roadmap](docs/platform/roadmap.md) | Feature specifications |
| [Licenses](licenses/README.md) | License tiers and terms |
| [Technical datasheet](docs/commercial/datasheet.md) | Dataset specifications |
| [Knowledge architecture](docs/architecture/knowledge-architecture.md) | Corpus structure |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.
