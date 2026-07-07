# Coltex — The Knowledge Operating System for AI

**Enterprise knowledge intelligence — not a vector database.**

Coltex is a Knowledge OS that **understands**, **connects**, **reasons over**, **retrieves from**, and **improves** organizational knowledge. The dataset and graph are foundation layers; the **Knowledge Intelligence Engine** is the heart.

---

## Intelligence loop

```
Understand  →  Connect  →  Reason  →  Retrieve  →  Improve
```

Full vision: [Knowledge OS](../platform/knowledge-os.md) · [Intelligence Engine](../platform/intelligence-engine.md) · [Roadmap](../platform/roadmap.md)

---

## Platform components

| Component | Status | Detail |
|-----------|--------|--------|
| Knowledge Intelligence Engine | Roadmap | Discover, detect contradictions, recommend merges |
| Knowledge Health | Roadmap | Score, coverage, duplicates, staleness, graph integrity |
| AI Memory | Partial | Working → Project → Org → Long-term → Archive |
| Reasoning Layer | Partial | Intent → Planner → Retrieve → Rank → Evidence |
| Event System & Scheduler | Roadmap | Event-driven pipeline, automated jobs |
| Trust & Provenance | Partial | Source, author, version, verification per chunk |
| Knowledge Lifecycle | Roadmap | Created → Verified → Published → Deprecated |
| AI Governance | Partial | Retention, access, audit, compliance reports |
| Extensibility | Roadmap | Plugins, hooks, SDK |
| Dataset & Graph | Available | 13k+ docs, GraphRouter, audit pipeline |

Config manifests: [events.yaml](../../config/events.yaml) · [lifecycle.yaml](../../config/knowledge-lifecycle.yaml) · [scheduler.yaml](../../config/scheduler.yaml) · [governance.yaml](../../config/governance.yaml) · [extensibility.yaml](../../config/extensibility.yaml)

---

## License tiers

| Tier | Price | Document |
|------|-------|----------|
| **Personal** | $79 USD (one-time) | [licenses/personal.md](../../licenses/personal.md) |
| **Professional** | $399 USD (one-time) | [licenses/professional.md](../../licenses/professional.md) |
| **Enterprise** | Custom quote | [licenses/enterprise.md](../../licenses/enterprise.md) |

Full tier comparison: [licenses/README.md](../../licenses/README.md)

---

## Available today

- **Knowledge dataset** — graph-linked, vector-ready, audit-ready exports
- **GraphRouter retrieval** — region-aware hybrid RAG
- **Distribution audit** — compliance gates, benchmark evidence
- **Memory tier model** — corpus-level working / episodic / semantic / procedural

---

## Build commands

```bash
make product-enterprise
make audit-distribution
make evaluate
```

See [SKU matrix](sku-matrix.md) · [Datasheet](datasheet.md)

---

## License

See [licenses/README.md](../../licenses/README.md) for license tiers and terms.
