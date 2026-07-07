# Coltex Platform Overview

**Coltex — AI Knowledge Infrastructure Platform**

Coltex is enterprise knowledge infrastructure: a unified platform for ingesting, structuring, connecting, searching, and governing organizational knowledge — not a one-time dataset export.

---

## The shift

| Dataset-only framing | Platform framing |
|---------------------|------------------|
| Static RAG vector corpus | Living knowledge system |
| Manual file imports | Connector-driven sync |
| CLI and JSONL exports | Knowledge Studio + APIs |
| GraphRAG as internal plumbing | Visual, explorable knowledge graph |
| Build-time quality checks | Continuous AI quality dashboard |

The **enterprise RAG vector dataset** remains a core deliverable — pre-chunked, graph-linked, audit-ready — but it is one layer in a broader stack.

---

## Platform stack

```
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Studio · Dashboards · Analytics · Multi-tenancy  │  ← Experience layer
├─────────────────────────────────────────────────────────────┤
│  Connectors · Sync · Plugins · AI Document Writer           │  ← Integration layer
├─────────────────────────────────────────────────────────────┤
│  Search · Retrieval · GraphRouter · Timeline                │  ← Intelligence layer
├─────────────────────────────────────────────────────────────┤
│  Graph · Embeddings · Chunks · Metadata · Clusters          │  ← Knowledge layer
├─────────────────────────────────────────────────────────────┤
│  Dataset · Provenance · Audit · Licensing                   │  ← Foundation (available)
└─────────────────────────────────────────────────────────────┘
```

---

## Core capabilities

### Available today

- **Knowledge dataset** — 13k+ curated documents, 83k+ chunks, 52k+ graph edges
- **Knowledge graph** — hubs, domain routes, 20 relationship types, GraphRAG expansion
- **Search & retrieval** — hybrid RAG with region-aware GraphRouter
- **Quality & compliance** — distribution audit, benchmarks, provenance, tiered licensing
- **Build pipeline** — `make product-enterprise`, manifest checksums, JSONL exports

### On the roadmap

See [Platform roadmap](roadmap.md) for detailed specifications of Knowledge Studio, connectors, sync, timeline, dashboards, analytics, multi-tenancy, plugins, AI document writer, and visual graph explorer.

---

## Target buyers

| Segment | Primary value |
|---------|---------------|
| **Platform engineering** | Graph-linked runbooks, ADRs, API refs for agent toolchains |
| **AI / ML teams** | Production RAG corpus with benchmark evidence |
| **Enterprise IT** | Governed knowledge with audit trail and tiered licensing |
| **DevOps / SRE** | Living docs synced from GitHub, Confluence, Notion (roadmap) |
| **Knowledge managers** | Visual studio, analytics, gap detection (roadmap) |

---

## Connector ecosystem

Planned first-party connectors are defined in [config/connectors.yaml](../../config/connectors.yaml):

GitHub · GitLab · Notion · Confluence · Google Drive · SharePoint · Dropbox · OneDrive · Jira · Slack · Discord

Each connector feeds the same pipeline: ingest → metadata → graph → vectors → search.

---

## Multi-tenancy model (planned)

```
Organization
  └── Workspace
        └── Project
              └── Knowledge Base
                    ├── Documents
                    ├── Graph
                    ├── Embeddings
                    └── Connectors
```

Isolation at the knowledge-base level with shared platform services (search, analytics, governance).

---

## Related documents

- [Platform roadmap](roadmap.md) — feature specifications
- [Product overview](../commercial/product-overview.md) — commercial packaging
- [Knowledge architecture](../architecture/knowledge-architecture.md) — corpus design
- [Technical datasheet](../commercial/datasheet.md) — dataset specifications
