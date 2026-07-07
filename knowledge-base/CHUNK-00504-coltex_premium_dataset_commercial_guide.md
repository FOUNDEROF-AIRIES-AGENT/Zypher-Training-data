---
id: CHUNK-00504-coltex_premium_dataset_commercial_guide
title: Coltex Premium Dataset Commercial Guide
doc_type: guide
category: rag
hub: coltex_platform
tags:
  - sales
  - dataset
  - licensing
  - commercial
depends_on:
  - CHUNK-00500
see_also:
  - CHUNK-00502
related:
  - CHUNK-00000
---

# Coltex Premium Dataset Commercial Guide

## What You Are Selling

A **checksum-signed RAG dataset bundle** — not raw markdown dumps. Each build exports:

| Artifact | Buyer Value |
|----------|-------------|
| `chunks.jsonl` | Drop into any vector pipeline |
| `embeddings.jsonl` | Skip GPU embedding cost |
| `edges.jsonl` | Enable GraphRAG without manual linking |
| `catalog.jsonl` | Provenance and document index |
| `manifest.json` | SHA-256 integrity for procurement |
| `benchmarks/*.jsonl` | Proof of retrieval quality |

## SKU Positioning

| SKU | Price | Buyer Profile |
|-----|-------|---------------|
| Seed (500 docs) | $499 | Indie devs, hackathon sponsors |
| Premium Smoke (25K) | $1,000 | Startups, POC teams |
| Premium Full | $5,000 | Enterprise procurement |
| Hyper | Custom | Data marketplaces, ML platforms |

## Quality Evidence for Sales

Run before every deal close:

```bash
make product-premium-smoke
make evaluate
make audit-distribution
```

Share with buyer:
- `benchmarks/evaluation_report.json` — recall@k metrics
- `benchmarks/distribution_audit.json` — compliance pass/fail
- `knowledge-base/PROVENANCE.md` — content origin statement

## Licensing

- **Corpus content:** Apache-2.0 synthetic originals
- **Commercial redistribution:** Governed by `EULA`
- **Third-party deps:** Listed in `NOTICE`

## Upsell Path

1. Dataset-only buyer → Platform Starter ($299/mo) for live ingestion
2. Platform buyer → Premium Dataset for bootstrap corpus
3. Enterprise → White-label + hyper generation cluster

## Reseller Margin

- 40% on dataset SKUs
- 25% recurring on platform subscriptions
- Co-branded collateral in `docs/sales/`
