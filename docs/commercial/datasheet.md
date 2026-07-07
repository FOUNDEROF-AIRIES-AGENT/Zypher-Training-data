# Coltex Dataset — Technical Datasheet

**Version:** 3.0.0 · **Updated:** 2026-07-07 · **License:** Apache-2.0

---

## Dataset specifications

| Metric | Enterprise | Premium Smoke | Premium Hyper |
|--------|------------|---------------|---------------|
| Documents | 12,993 curated | 25,000 streamed | Uncapped |
| Domains | 63 | 27 categories | 27+ categories |
| Knowledge hubs | 18 | 18 | 18 |
| Graph links | 306 | Generated | Generated |
| Domain routes | 90 | — | — |
| Chunk max size | 2,000 chars | 2,000 chars | 2,000 chars |
| Chunk overlap | 200 chars | 200 chars | 200 chars |
| Embedding model | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 |
| Embedding dimensions | 384 | 384 | 384 |
| Max duplicate ratio | ≤ 5% | ≤ 5% | ≤ 5% |
| Min chunk chars | 40 | 40 | 40 |

---

## Document types (20)

`documentation`, `faq`, `api_reference`, `architecture_decision`, `design_document`, `runbook`, `troubleshooting`, `code_walkthrough`, `sql_example`, `database_schema`, `migration_guide`, `incident_report`, `code_review`, `guide`, `tutorial`, `benchmark`, `evaluation`, `best_practices`, `deep_dive`, `anti_patterns`, `case_study`, `domain_route`, `graph_link_map`

---

## Metadata schema (per document)

| Field | Type | Description |
|-------|------|-------------|
| `doc_id` | string | Unique identifier (e.g. `CHUNK-01234`) |
| `title` | string | Human-readable title |
| `doc_type` | string | Typed classification |
| `category` | string | Technology domain |
| `hub` | string | Knowledge cluster assignment |
| `tags` | list | Searchable tags |
| `related` | list | Cross-reference document IDs |
| `see_also` | list | GraphRAG edge targets |
| `depends_on` | list | Dependency edges |

Chunk records add: `chunk_id`, `content`, `content_hash`, `source_doc_id`, `char_count`

Embedding records add: `chunk_id`, `vector` (384 floats), `model`

---

## Graph relationship types (20)

**Core:** `related`, `depends_on`, `uses`, `implements`, `calls`, `see_also`

**Advanced:** `extends`, `validates`, `synthesizes`, `triggers`, `derived_from`, `tested_by`, `deployed_via`, `contradicts`, `inhibits`, `supersedes`

---

## Quality gates (build fails if unmet)

| Gate | Threshold |
|------|-----------|
| Duplicate chunk ratio | ≤ 5% |
| Metadata completeness | `doc_id`, `title` required |
| License header | Required on all distributable docs |
| Substantive content | ≥ 200 chars body (premium) |
| Forbidden sources | No Wikipedia, StackOverflow, official doc URLs |
| Distribution audit | LICENSE + PROVENANCE + NOTICE present |

---

## Benchmark datasets

| Dataset | Minimum pairs | Purpose |
|---------|---------------|---------|
| FAQ pairs | 200–500 | Q&A retrieval baseline |
| Retrieval gold | 200+ | Ground-truth chunk matching |
| RAG eval | 200+ | End-to-end context quality |

Evaluation targets: recall@8 ≥ 40–50%, metadata accuracy ≥ 90%

---

## File formats

All deliverables use **JSONL** (one JSON object per line) for streaming ingestion:

```json
{"chunk_id": "CHUNK-01234-0", "doc_id": "CHUNK-01234", "content": "...", "char_count": 847}
```

```json
{"chunk_id": "CHUNK-01234-0", "vector": [0.012, -0.034, ...], "model": "all-MiniLM-L6-v2"}
```

---

## System requirements (build)

| Component | Version |
|-----------|---------|
| Python | 3.10+ |
| sentence-transformers | ≥ 3.0 |
| chromadb | ≥ 0.5 |
| Disk (Enterprise build) | ~2 GB |
| Disk (Premium 25k + embeddings) | ~5 GB |
| RAM (embedding export) | 8 GB recommended |

---

## Provenance

100% original synthetic content. No web scraping. No third-party doc reproduction. See `knowledge-base/PROVENANCE.md`.
