# Coltex V1

**Tagline:** The AI Knowledge Platform for Modern Organizations

**Goal:** Turn scattered business knowledge into AI-ready intelligence in under 10 minutes.

---

## Knowledge Studio — Home

The product opens here. Users open this every day.

| Module | Purpose |
|--------|---------|
| **Dashboard** | Documents, sources, searches, AI queries, last sync, health |
| **Knowledge** | Browse all knowledge objects |
| **Sources** | Upload and manage knowledge sources |
| **Search** | Universal search — one bar, all content |
| **Ask Knowledge** | Question → answer with sources, confidence, and why |
| **Analytics** | Knowledge Health and usage |
| **Settings** | Workspace, AI provider, embeddings, chunk size, users, backup |

Launch: `python3 -m runtime studio`

---

## Knowledge Sources

### Supported today (V1)

| Format | Extension |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx` |
| Markdown | `.md` |
| Text | `.txt` |
| HTML | `.html` |
| JSON | `.json` |

Upload via Knowledge Studio → **Sources**, or:

```bash
python3 -m runtime upload path/to/document.pdf
```

### Coming soon

GitHub · Notion · Google Drive · Confluence · Slack

---

## AI Processing (automatic)

Users never see technical steps unless they expand **Processing Details**.

```
Upload → Parse → Clean → Chunk → Metadata → Embeddings → Index → Done
```

Triggered automatically on every upload. Typical time: under 10 minutes for hundreds of documents.

---

## Universal Search

One search bar searches:

- Documents
- Metadata (type, hub, tags)
- Code references
- API documentation
- SQL examples

---

## Ask Knowledge

Not "Ask AI" — **Ask Knowledge**.

```
Question → Retrieve → Build Context → Answer → Sources + Confidence + Why
```

Each answer shows:

- **Sources** — linked documents
- **Confidence** — retrieval score
- **Why** — similarity, graph, metadata match (explainability)

CLI: `python3 -m runtime ask "How do we handle authentication?"`

---

## Knowledge Health

Simple, honest scores — nothing fake.

| Metric | Example |
|--------|---------|
| Knowledge Score | 94% |
| Documents | 483 |
| Embeddings | 14,832 |
| Duplicates | 2 |
| Outdated | 6 |

---

## V1 Architecture

```
Knowledge Sources
       ↓
   Processing
       ↓
  Knowledge Store
       ↓
     Search
       ↓
  Ask Knowledge
       ↓
   Analytics
```

Runtime implementation: `runtime/processing/`, `runtime/sources/`, `runtime/ask/`

Config: [config/v1.yaml](../../config/v1.yaml)

---

## Quick start (under 10 minutes)

```bash
pip install -r requirements.txt
python3 -m runtime studio

# Upload a document
python3 -m runtime upload docs/example.md

# Ask Knowledge
python3 -m runtime ask "What is in my knowledge base?"

# Check health
python3 -m runtime health
```
