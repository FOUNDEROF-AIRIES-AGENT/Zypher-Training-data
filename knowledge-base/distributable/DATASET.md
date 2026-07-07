# Coltex Distributable Dataset Package

This directory contains audit samples and documentation for the commercial Coltex RAG vector dataset.

## Contents

| Path | Description |
|------|-------------|
| `_samples/` | Audit sample markdown (first N from premium stream) |
| `DATASET.md` | This file — buyer orientation |
| `README.md` | Generation commands |

## Quick load (Python)

```python
import json

# Load vector-ready chunks
with open("data/product/chunks/chunks.jsonl") as f:
    chunks = [json.loads(line) for line in f]

# Load pre-computed embeddings
with open("data/product/embeddings/embeddings.jsonl") as f:
    vectors = [json.loads(line) for line in f]

# Load graph edges
with open("data/product/graph/edges.jsonl") as f:
    edges = [json.loads(line) for line in f]

print(f"{len(chunks)} chunks, {len(vectors)} vectors, {len(edges)} edges")
```

## Build from source

```bash
pip install -r requirements.txt
make product-enterprise       # Curated enterprise tier
make product-premium-smoke    # Premium 25k validation build
make audit-distribution     # Compliance check
```

## Compliance

- **License:** Apache-2.0 (`knowledge-base/LICENSE`)
- **Provenance:** `knowledge-base/PROVENANCE.md`
- **Audit:** `benchmarks/distribution_audit.json` (after build)

## Documentation

- [Product overview](../../docs/commercial/product-overview.md)
- [Technical datasheet](../../docs/commercial/datasheet.md)
- [SKU matrix](../../docs/commercial/sku-matrix.md)
