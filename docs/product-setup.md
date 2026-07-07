# Coltex — Setup Guide

Build the RAG-as-a-Service platform, export premium dataset artifacts, or query via CLI.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run Platform API

```bash
make platform
# Docs: http://localhost:8080/docs
# Demo API key: data/platform/DEMO_API_KEY.txt
```

See [Platform API guide](api/getting-started.md) and [Docker deployment](deployment/docker.md).

## Build dataset

```bash
# Premium smoke (25,000 documents)
make product-premium-smoke

# Full hyper tier (100B× — run on cluster)
make product-hyper

# Compliance audit
make audit-distribution
```

## Output artifacts

| Artifact | Path |
|----------|------|
| Chunks | `data/product/chunks/chunks.jsonl` |
| Catalog | `data/product/catalog.jsonl` |
| Embeddings | `data/product/embeddings/embeddings.jsonl` |
| Graph | `data/product/graph/edges.jsonl` |
| Manifest | `data/product/manifest.json` |

## Query the database

```bash
make index
python3 -m brain retrieve "How does GraphRAG work?" --context
python3 examples/rag_query.py "chunking strategies"
python3 examples/brain_retrieve.py "RAG principles"
```

## Configuration

- `config/product_hyper.yaml` — $1000+ premium hyper dataset
- `config/product_hyper_smoke.yaml` — local smoke test
- `config/brain.yaml` — vector index + retrieval

See also: [Quality Standards](product-quality.md) · [Licensing](product-licensing.md) · [Evaluation](product-evaluation.md)
