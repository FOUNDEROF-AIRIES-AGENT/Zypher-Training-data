# Coltex V1

**The AI Knowledge Platform for Modern Organizations**

Turn scattered business knowledge into AI-ready intelligence in under 10 minutes.

```bash
pip install -r requirements.txt
python3 -m runtime studio
```

Open **Knowledge Studio** — your daily home for knowledge work.

---

## Use today

| Feature | How |
|---------|-----|
| **Knowledge Studio** | `python3 -m runtime studio` |
| **Upload sources** | Studio → Sources, or `python3 -m runtime upload file.pdf` |
| **Ask Knowledge** | Studio → Ask Knowledge, or `python3 -m runtime ask "question"` |
| **Universal Search** | Studio → Search, or `python3 -m runtime search "query"` |
| **Dashboard & Health** | Studio → Dashboard / Analytics |
| **Settings** | Studio → Settings |

Supported uploads: **PDF · DOCX · Markdown · TXT · HTML · JSON**

Coming soon: GitHub · Notion · Google Drive

---

## Knowledge Studio

| Module | Purpose |
|--------|---------|
| Dashboard | Documents, sources, searches, AI queries, last sync, health |
| Knowledge | Browse all knowledge objects |
| Sources | Upload and manage files |
| Search | One bar — documents, metadata, APIs, SQL |
| Ask Knowledge | Q&A with sources, confidence, and why |
| Analytics | Knowledge Health scores |
| Settings | Workspace, AI provider, embeddings, chunk size |

---

## AI Processing (automatic)

```
Upload → Parse → Clean → Chunk → Metadata → Embeddings → Index → Done
```

Users never see technical steps unless they expand processing details.

---

## V1 Architecture

```
Knowledge Sources → Processing → Knowledge Store → Search → Ask Knowledge → Analytics
```

Full spec: [docs/product/coltex-v1.md](docs/product/coltex-v1.md)

---

## Build dataset foundation (optional)

```bash
make product-enterprise
make runtime-health
```

---

## Documentation

| Doc | Description |
|-----|-------------|
| [Coltex V1 Product Spec](docs/product/coltex-v1.md) | Full V1 feature spec |
| [Runtime](docs/platform/runtime.md) | Runtime architecture |
| [Licenses](licenses/README.md) | License tiers |

---

## Copyright

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.
