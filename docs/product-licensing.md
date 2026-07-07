# Coltex Product Licensing

## Knowledge base content

All distributable knowledge base content is **original synthetic documentation**
authored for Coltex. It was **not** copied from third-party documentation,
web scraping, or proprietary sources.

| Content | License | Included in product? |
|---------|---------|---------------------|
| Distributable `CHUNK-*.md` files | Coltex EULA | Yes |
| `knowledge-base/LICENSE` | Coltex EULA | Yes |
| `knowledge-base/_excluded_from_distribution/` | Coltex EULA | **No** — quarantined stubs |
| `knowledge-base/generated/` | Coltex EULA | **No** — stress-test corpus only |

See `knowledge-base/PROVENANCE.md` for full content origin documentation.

## Project license

The Coltex Dataset is governed by the **[End User License Agreement (EULA)](../EULA)**.

## NOTICE file

Third-party open-source runtime dependencies are listed in the root [`NOTICE`](../NOTICE) file.

## What is covered

| Component | License |
|-----------|---------|
| Curated knowledge base (distributable CHUNK docs) | Coltex EULA |
| Product artifacts (`data/product/`) | Coltex EULA |
| Benchmark datasets (`benchmarks/`) | Coltex EULA |
| Scripts and tooling (`scripts/product/`) | Coltex EULA |
| Examples (`examples/`) | Coltex EULA |

## Third-party dependencies (runtime)

These are **not bundled** in the knowledge package but are used when running
the RAG pipeline. Each dependency is subject to its own upstream license:

| Dependency | Notes |
|------------|-------|
| sentence-transformers | Embedding library |
| `all-MiniLM-L6-v2` model | Downloaded from Hugging Face |
| chromadb | Vector store |
| PyTorch | ML framework |
| transformers | Model loading |

See upstream repositories for license terms.

## Commercial use

Per the EULA, you **may**:

- Build and sell commercial software and AI applications using the Dataset
- Train or fine-tune models and deploy RAG systems commercially
- Create derivative works (embeddings, indexes, applications) for commercial use

Per the EULA, you **may not** (without written authorization):

- Resell or redistribute the Dataset itself
- Share the Dataset with third parties
- Sell the Dataset as a competing product

## Commercial distribution checklist

Before offering the package commercially:

```bash
make product              # Build with compliance gates
make audit-distribution   # Verify distribution rights
```

The audit checks for:

- Required `LICENSE`, `NOTICE`, and `PROVENANCE.md` files
- No excluded paths in product artifacts
- No forbidden third-party source patterns in content
- No placeholder boilerplate in distributable documents

## Disclaimer

This document summarizes the project's licensing approach. It is not legal advice.
Consult qualified counsel and read the full EULA before commercial use.
