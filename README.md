# Zypher — Enterprise AI Coding Assistant

**Zypher Brain** is the permanent source of knowledge. The language model is a **replaceable reasoning engine** only.

Add new documents to `knowledge-base/` anytime — no model retraining required.

## Architecture

```
User Message
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ZYPHER BRAIN                             │
│  Knowledge Base · Vector DB · Metadata · Graph · Memory          │
│                                                                 │
│  1. Save conversation                                           │
│  2. Embed query                                                 │
│  3. Vector search                                               │
│  4. Metadata filter search                                      │
│  5. Graph relationship traversal                                │
│  6. Merge + re-rank                                             │
│  7. Build context window                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LLM (Reasoning Engine)                        │
│  poolside/Laguna-XS-2.1 · optional adapter · swappable          │
│  Answers ONLY from Zypher Brain context                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                      Final Answer
```

| Component | Role |
|-----------|------|
| **Zypher Brain** | Primary knowledge — docs, APIs, code, ADRs, runbooks, SQL |
| **LLM** | Reasoning over retrieved context (not internal knowledge) |
| **Optional fine-tune** | Style/domain tuning — not required for knowledge |

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make generate-smoke     # expand knowledge corpus (optional)
make index              # build Zypher Brain vector index
make chat               # Brain retrieval + LLM reasoning
```

No fine-tuning required. To enable an optional adapter, set `adapter.enabled: true` in `config/llm.yaml`.

## Zypher Brain module

```
brain/
├── brain.py              # ZypherBrain service
├── ingestion/            # Load markdown documents
├── embeddings/           # Query/document embeddings
├── indexing/             # ChromaDB vector index
├── metadata/             # doc_type, category, tag filters
├── graph/                # Typed relationship traversal
├── reranking/            # Merge + score results
├── retrieval/            # Full retrieval pipeline
└── memory/               # Conversation memory
```

### Knowledge types supported

Documentation · FAQs · API References · ADRs · Runbooks · Troubleshooting · Code Examples · SQL Examples · Deployment Guides · Incident Reports · Design Documents · Code Reviews

### Retrieval flow

1. Save conversation
2. Generate embedding for user query
3. Search vector database
4. Search metadata filters
5. Search graph relationships
6. Merge and re-rank results
7. Build context window
8. Send context to LLM
9. Return generated answer

## Configuration

| File | Purpose |
|------|---------|
| `config/brain.yaml` | Knowledge paths, retrieval, graph, memory |
| `config/llm.yaml` | LLM provider, model, optional adapter |
| `config/corpus_generation.yaml` | Corpus generator settings |

## Add knowledge (no retraining)

```bash
# 1. Add markdown to knowledge-base/
echo "# My Runbook\n..." > knowledge-base/my-runbook.md

# 2. Re-index
make index

# 3. Chat — Brain retrieves the new doc automatically
make chat
```

## Optional: corpus generation + fine-tuning

```bash
make generate-smoke
make prepare
make train-xs          # optional — enable adapter in config/llm.yaml
```

## Project structure

```
.
├── brain/                    # Zypher Brain (primary knowledge service)
├── zypher/                   # Chatbot CLI + LLM provider
│   ├── backend.py
│   ├── chat.py
│   └── llm/provider.py       # Swappable reasoning engine
├── knowledge-base/           # Seed + generated documents
├── scripts/
│   ├── generate_corpus.py    # Expand brain corpus
│   └── prepare_advanced_dataset.py  # Optional training data
└── config/
    ├── brain.yaml
    └── llm.yaml
```

## Future compatibility

- Multiple language models (swap in `config/llm.yaml`)
- Model swapping without touching Brain
- Optional fine-tuning (adapter path)
- GraphRAG typed relationships
- Tool calling (`search_zypher_brain`)
- Multi-agent workflows
- Enterprise deployments

## Hardware

| Step | GPU | Notes |
|------|-----|-------|
| `make index` | CPU OK | Embeddings via sentence-transformers |
| `make chat` | 24 GB+ VRAM | 4-bit LLM inference |
| `make train-xs` | Optional | Not required for knowledge |
