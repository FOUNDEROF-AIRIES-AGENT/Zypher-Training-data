# Premium Distributable Corpus

Streaming-generated original synthetic documents for the **Coltex Premium RAG Vector Dataset**.

| Path | Purpose |
|------|---------|
| `_samples/` | Audit sample markdown files (first N from stream) |
| `DATASET.md` | Buyer orientation and load instructions |
| `data/product/catalog.jsonl` | Full document catalog metadata |
| `data/product/chunks/chunks.jsonl` | Vector-ready chunks |

## Generation

```bash
# Enterprise curated tier (recommended — full graph architecture)
make corpus-mega
make product-enterprise

# Premium smoke validation (25,000 documents)
make product-premium-smoke

# Full hyper tier (100B× multiplier, uncapped — run on cluster)
make product-hyper
```

All content is **original synthetic** · **Apache-2.0** · passes distribution audit.

See [commercial docs](../../docs/commercial/product-overview.md) for full product details.
