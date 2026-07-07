# Premium Distributable Corpus

Streaming-generated original synthetic documents for the **$1000+ Coltex Premium RAG Dataset**.

| Path | Purpose |
|------|---------|
| `_samples/` | Audit sample markdown files (first N from stream) |
| `data/product/catalog.jsonl` | Full document catalog metadata |
| `data/product/chunks/chunks.jsonl` | Vector-ready chunks (streaming output) |

## Generation

```bash
# Local smoke (10,000 documents)
make product-premium-smoke

# Full hyper tier (100B× multiplier, uncapped — run on Vast.ai)
make product-hyper
```

All content is **original synthetic** · governed by **Coltex EULA** · passes distribution audit.
