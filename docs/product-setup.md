# Coltex — Setup Guide

Build, expand, and query the Coltex Enterprise RAG Vector Dataset.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Bootstrap the corpus

```bash
make corpus-advanced              # Architecture bootstrap (500 docs)
make corpus-mega                  # Expand to 10,000+ domain documents
make expand-curated-kb COUNT=500  # Additional curated growth
make corpus-report                # Rebuild catalog index
```

## Build commercial vector dataset

```bash
# Enterprise tier (recommended — full graph architecture, 13k+ docs)
make product-enterprise

# Fast build without embeddings (validation)
make product-enterprise-fast

# Premium smoke tier (25,000 streamed documents)
make product-premium-smoke

# Inspect deliverables
python3 examples/load_dataset.py
make audit-distribution
make evaluate
```

## Index and query

```bash
make index
python3 -m brain retrieve "How does GraphRAG work?" --context
python3 -m brain report
```

## Output artifacts

| Artifact | Path |
|----------|------|
| Chunks | `data/product/chunks/chunks.jsonl` |
| Catalog | `data/product/catalog.jsonl` |
| Embeddings | `data/product/embeddings/embeddings.jsonl` |
| Graph | `data/product/graph/edges.jsonl` |
| Manifest | `data/product/manifest.json` |
| Benchmarks | `benchmarks/` |
| Catalog index | `data/brain/catalog-index.json` |

## Commercial documentation

- [Product overview](commercial/product-overview.md)
- [Technical datasheet](commercial/datasheet.md)
- [SKU matrix](commercial/sku-matrix.md)
- [Product licensing](product-licensing.md)

## Corpus generation tiers

| Command | Approximate output |
|---------|-------------------|
| `make corpus-advanced` | 500+ domain-organized docs |
| `make corpus-mega` | 10,000+ documents |
| `make product-enterprise` | Full vector dataset package |
| `make product-premium-smoke` | 25,000 streamed documents |
| `make product-hyper` | Uncapped hyper tier (cluster) |

See [README](../README.md) and [architecture guide](architecture/knowledge-architecture.md).
