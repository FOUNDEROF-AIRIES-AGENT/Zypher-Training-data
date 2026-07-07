# Coltex Product Licensing

## Knowledge base content

All distributable knowledge base content is **original synthetic documentation**
authored for Coltex. It was **not** copied from third-party documentation,
web scraping, or proprietary sources.

| Content | Included in product? |
|---------|---------------------|
| Distributable `CHUNK-*.md` files | Yes |
| `knowledge-base/LICENSE` | Yes |
| `knowledge-base/_excluded_from_distribution/` | **No** — quarantined stubs |
| `knowledge-base/generated/` | **No** — stress-test corpus only |

See `knowledge-base/PROVENANCE.md` for full content origin documentation.

## Purchaser rights

When you buy the Coltex Dataset, you receive a **perpetual commercial license** to:

- Use the Dataset for any lawful purpose
- Build and sell commercial software, AI applications, and RAG services
- Modify the Dataset and create derivative works
- Generate embeddings, indexes, and graph databases
- Share derivative outputs with your customers

See the [EULA](../EULA) and `knowledge-base/LICENSE` for full terms.

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

## Commercial distribution checklist

```bash
make product-premium-smoke   # Build with compliance gates
make audit-distribution      # Verify distribution rights
```

## Disclaimer

This document summarizes the project's licensing approach. It is not legal advice.
