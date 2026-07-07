#!/usr/bin/env python3
"""Build curated benchmark datasets from seed knowledge base or product catalog."""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from common import (
    extract_faq_question,
    iter_jsonl,
    load_knowledge_base,
    load_product_config,
    normalize_doc_id,
    normalize_id_list,
    resolve_path,
    write_jsonl,
)

# Doc-type aware question templates for diverse, realistic evaluation queries
QUESTION_TEMPLATES: dict[str, list[str]] = {
    "faq": [
        "{title}",
        "Can you explain {topic}?",
        "What is {topic}?",
    ],
    "documentation": [
        "What does the documentation say about {topic}?",
        "Summarize the key points of {topic}.",
        "How is {topic} documented in Coltex?",
    ],
    "guide": [
        "How do I implement {topic}?",
        "Walk me through {topic} step by step.",
        "What are the prerequisites for {topic}?",
    ],
    "tutorial": [
        "Teach me about {topic}.",
        "How do I get started with {topic}?",
        "What exercises cover {topic}?",
    ],
    "runbook": [
        "What is the runbook for {topic}?",
        "How do I respond to an incident involving {topic}?",
        "What are the escalation steps for {topic}?",
    ],
    "troubleshooting": [
        "How do I troubleshoot {topic}?",
        "What are common symptoms of {topic} issues?",
        "How do I diagnose problems with {topic}?",
    ],
    "api_reference": [
        "What is the API for {topic}?",
        "How do I authenticate requests to {topic}?",
        "What are the error codes for {topic}?",
    ],
    "architecture_decision": [
        "Why was {topic} chosen?",
        "What are the trade-offs of {topic}?",
        "What is the architecture decision for {topic}?",
    ],
    "code_walkthrough": [
        "Walk me through the code for {topic}.",
        "How is {topic} implemented?",
        "What is the testing strategy for {topic}?",
    ],
    "best_practices": [
        "What are the best practices for {topic}?",
        "What common mistakes should I avoid with {topic}?",
        "What checklist applies to {topic}?",
    ],
    "benchmark": [
        "What metrics should I use to evaluate {topic}?",
        "How do I benchmark {topic}?",
        "What recall targets apply to {topic}?",
    ],
    "evaluation": [
        "How should I score answers about {topic}?",
        "What makes a good answer for {topic}?",
        "What rubric applies to {topic}?",
    ],
    "incident_report": [
        "What happened during the {topic} incident?",
        "What was the root cause of {topic}?",
        "How was {topic} resolved?",
    ],
    "design_document": [
        "What is the design for {topic}?",
        "What components make up {topic}?",
        "What are the data flows in {topic}?",
    ],
    "migration_guide": [
        "How do I migrate to {topic}?",
        "What are the rollback steps for {topic} migration?",
        "What prerequisites are needed before migrating {topic}?",
    ],
    "release_notes": [
        "What changed in the latest {topic} release?",
        "Are there breaking changes in {topic}?",
        "What migration steps are required for {topic}?",
    ],
    "database_schema": [
        "What is the database schema for {topic}?",
        "What indexes should {topic} use?",
        "How are tables related in {topic}?",
    ],
    "deep_dive": [
        "Explain the internals of {topic}.",
        "What are the trade-offs of {topic}?",
        "How does {topic} work under the hood?",
    ],
    "comparison": [
        "How does {topic} compare to alternatives?",
        "What criteria should I use to evaluate {topic}?",
        "Which option is recommended for {topic}?",
    ],
    "case_study": [
        "What is a real-world example of {topic}?",
        "What outcomes were achieved with {topic}?",
        "What lessons were learned from {topic}?",
    ],
}

PARAPHRASE_PREFIXES = (
    "In Coltex,",
    "For production RAG systems,",
    "When working with enterprise codebases,",
    "From an architecture perspective,",
    "During incident response,",
)


def _clean_topic(title: str) -> str:
    """Extract a concise topic phrase from a document title."""
    topic = title.split("—")[0].split(" - ")[0].strip()
    topic = re.sub(r"\s*\(v\d+\)\s*$", "", topic, flags=re.IGNORECASE)
    topic = re.sub(r"\s*\(Unique \d+\)\s*$", "", topic, flags=re.IGNORECASE)
    if topic.lower().startswith("chunk "):
        topic = re.sub(r"^chunk\s+\d+\s+", "", topic, flags=re.IGNORECASE)
    return topic


def _question_for_record(
    title: str,
    doc_type: str,
    variant: int = 0,
    *,
    paraphrase: bool = False,
    doc_id: str = "",
) -> str:
    topic = _clean_topic(title)
    templates = QUESTION_TEMPLATES.get(doc_type, QUESTION_TEMPLATES["documentation"])
    template = templates[variant % len(templates)]
    question = template.format(title=title, topic=topic)
    if "?" not in question and doc_type == "faq":
        question = question if question.endswith("?") else f"{question}?"
    # Disambiguate when titles repeat across variants (common in premium corpus)
    if doc_id and "(v" in title.lower():
        short_id = doc_id.split("-")[-1][:8] if "-" in doc_id else doc_id[:8]
        question = f"{question.rstrip('?')} (document {short_id})?"
    if paraphrase:
        prefix = PARAPHRASE_PREFIXES[variant % len(PARAPHRASE_PREFIXES)]
        question = f"{prefix} {question[0].lower()}{question[1:]}" if question else question
    return question


def _answer_keywords(doc) -> list[str]:
    """Extract key terms from document body for faithfulness checks."""
    text = doc.content.lower()
    words = re.findall(r"[a-z]{5,}", text)
    freq: dict[str, int] = {}
    priority = {
        "coltex", "retrieval", "graphrag", "chunking", "embedding", "vector",
        "knowledge", "rag", "agentic", "indexing", "kubernetes", "security",
    }
    for w in words:
        boost = 3 if w in priority else 1
        freq[w] = freq.get(w, 0) + boost
    for tag in doc.tags:
        if isinstance(tag, str) and len(tag) >= 4:
            freq[tag.lower()] = freq.get(tag.lower(), 0) + 2
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:10]]


def _keywords_from_record(rec: dict) -> list[str]:
    tags = [t for t in rec.get("tags", []) if isinstance(t, str) and len(t) >= 3]
    category = str(rec.get("category", ""))
    if category and category not in tags:
        tags.insert(0, category)
    doc_type = str(rec.get("doc_type", ""))
    if doc_type and doc_type not in tags:
        tags.append(doc_type)
    return tags[:10]


def build_faq_benchmark(kb, min_pairs: int) -> list[dict]:
    pairs: list[dict] = []
    seen_ids: set[str] = set()
    seen_questions: set[str] = set()

    for doc in kb.documents:
        question = extract_faq_question(doc)
        if not question or doc.doc_id in seen_ids:
            continue
        qnorm = question.lower().strip()
        if qnorm in seen_questions:
            continue
        seen_ids.add(doc.doc_id)
        seen_questions.add(qnorm)
        pairs.append({
            "id": f"faq-{normalize_doc_id(doc.doc_id)}",
            "question": question,
            "expected_doc_ids": [normalize_doc_id(doc.doc_id)],
            "expected_keywords": _answer_keywords(doc),
            "category": doc.category,
            "doc_type": doc.doc_type or "faq",
            "tags": doc.tags,
            "difficulty": "easy",
            "source_path": doc.path,
        })

    if len(pairs) < min_pairs:
        by_category: dict[str, list] = defaultdict(list)
        for doc in kb.documents:
            if doc.doc_id in seen_ids:
                continue
            title = doc.title.strip()
            if len(title) < 12 or title.lower().startswith("chunk "):
                continue
            if title.lower() in ("context", "decision", "consequences", "description", "resolution"):
                continue
            by_category[doc.category or "general"].append(doc)

        categories = sorted(by_category.keys())
        idx = 0
        while len(pairs) < min_pairs and categories:
            cat = categories[idx % len(categories)]
            docs = by_category[cat]
            if not docs:
                categories.remove(cat)
                continue
            doc = docs.pop(0)
            if doc.doc_id in seen_ids:
                idx += 1
                continue
            doc_type = doc.doc_type or "documentation"
            variant = len(pairs)
            question = _question_for_record(doc.title, doc_type, variant)
            qnorm = question.lower().strip()
            if qnorm in seen_questions:
                idx += 1
                continue
            seen_ids.add(doc.doc_id)
            seen_questions.add(qnorm)
            pairs.append({
                "id": f"faq-{doc.doc_id}",
                "question": question,
                "expected_doc_ids": [doc.doc_id],
                "expected_keywords": _answer_keywords(doc),
                "category": doc.category,
                "doc_type": doc_type,
                "tags": doc.tags,
                "difficulty": "medium",
                "source_path": doc.path,
                "supplemental": True,
            })
            idx += 1

    if len(pairs) < min_pairs:
        raise SystemExit(f"Only {len(pairs)} benchmark pairs found; need {min_pairs}")
    return pairs


def build_faq_from_catalog(
    catalog_path: Path,
    min_pairs: int,
    sample_size: int,
    *,
    seed: int = 42,
) -> list[dict]:
    rng = random.Random(seed)
    records = list(iter_jsonl(catalog_path))
    if sample_size and len(records) > sample_size:
        records = rng.sample(records, sample_size)

    by_category: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        by_category[str(rec.get("category", "general"))].append(rec)

    pairs: list[dict] = []
    seen_ids: set[str] = set()
    seen_questions: set[str] = set()
    categories = sorted(by_category.keys())
    idx = 0

    while len(pairs) < min_pairs and categories:
        cat = categories[idx % len(categories)]
        pool = by_category[cat]
        if not pool:
            categories.remove(cat)
            continue
        rec = pool.pop(rng.randrange(len(pool)))
        doc_id = rec.get("doc_id", "")
        if doc_id in seen_ids:
            idx += 1
            continue

        title = str(rec.get("title", "")).strip()
        doc_type = str(rec.get("doc_type", "documentation"))
        variant = len(pairs)
        if doc_type == "faq" and "?" in title:
            question = title.split("—")[0].strip()
        else:
            question = _question_for_record(title, doc_type, variant, doc_id=doc_id)

        qnorm = question.lower().strip()
        if qnorm in seen_questions:
            idx += 1
            continue

        seen_ids.add(doc_id)
        seen_questions.add(qnorm)
        pairs.append({
            "id": f"faq-{doc_id}",
            "question": question,
            "expected_doc_ids": [doc_id],
            "expected_keywords": _keywords_from_record(rec),
            "category": rec.get("category", ""),
            "doc_type": doc_type,
            "tags": rec.get("tags", []),
            "difficulty": ["easy", "medium", "hard"][variant % 3],
            "source_path": rec.get("path", ""),
            "from_catalog": True,
        })
        idx += 1

    if len(pairs) < min_pairs:
        raise SystemExit(f"Only {len(pairs)} catalog benchmark pairs; need {min_pairs}")
    return pairs


def build_retrieval_gold_catalog(faq_pairs: list[dict], catalog_path: Path | None = None) -> list[dict]:
    gold: list[dict] = []
    for pair in faq_pairs:
        gold.append({
            "query": pair["question"],
            "relevant_doc_ids": pair["expected_doc_ids"],
            "relevant_chunk_ids": [],
            "difficulty": pair.get("difficulty", "medium"),
            "category": pair.get("category", ""),
            "doc_type": pair.get("doc_type", ""),
        })

    if catalog_path and catalog_path.exists():
        by_hub: dict[str, list[str]] = defaultdict(list)
        for rec in iter_jsonl(catalog_path):
            hub = str(rec.get("hub", rec.get("category", "")))
            doc_id = rec.get("doc_id", "")
            if hub and doc_id:
                by_hub[hub].append(doc_id)

        hubs = sorted((h for h, ids in by_hub.items() if len(ids) >= 3), key=lambda h: -len(by_hub[h]))
        for hub in hubs[: min(20, len(hubs))]:
            ids = by_hub[hub][:8]
            gold.append({
                "query": f"What documents cover the {hub.replace('_', ' ')} knowledge hub?",
                "relevant_doc_ids": ids,
                "relevant_chunk_ids": [],
                "difficulty": "hard",
                "category": hub,
                "multi_hop": True,
            })
    return gold


def build_retrieval_gold(faq_pairs: list[dict], kb) -> list[dict]:
    gold: list[dict] = []
    for pair in faq_pairs:
        gold.append({
            "query": pair["question"],
            "relevant_doc_ids": pair["expected_doc_ids"],
            "relevant_chunk_ids": [],
            "difficulty": pair.get("difficulty", "easy"),
            "category": pair.get("category", ""),
        })

    hub_docs = sorted(kb.documents, key=lambda d: len(d.related), reverse=True)[:10]
    for doc in hub_docs:
        if len(doc.related) < 3:
            continue
        gold.append({
            "query": f"What documents are related to {doc.title}?",
            "relevant_doc_ids": normalize_id_list([doc.doc_id] + doc.related[:8]),
            "relevant_chunk_ids": [],
            "difficulty": "hard",
            "category": doc.category,
            "multi_hop": True,
        })

    for pair in faq_pairs[: min(10, len(faq_pairs))]:
        if pair.get("difficulty") == "easy":
            paraphrased = _question_for_record(
                pair["question"],
                pair.get("doc_type", "documentation"),
                len(gold),
                paraphrase=True,
            )
            gold.append({
                "query": paraphrased,
                "relevant_doc_ids": pair["expected_doc_ids"],
                "relevant_chunk_ids": [],
                "difficulty": "medium",
                "category": pair.get("category", ""),
                "paraphrase": True,
            })
    return gold


def build_rag_eval(faq_pairs: list[dict]) -> list[dict]:
    eval_set: list[dict] = []
    for pair in faq_pairs:
        eval_set.append({
            "id": pair["id"],
            "question": pair["question"],
            "expected_doc_ids": pair["expected_doc_ids"],
            "expected_keywords": pair["expected_keywords"],
            "category": pair.get("category", ""),
            "doc_type": pair.get("doc_type", ""),
            "difficulty": pair.get("difficulty", "medium"),
            "rubric": (
                "Answer must cite facts from expected documents only. "
                "Include at least two expected keywords when present in source material."
            ),
        })
    return eval_set


def main() -> None:
    parser = argparse.ArgumentParser(description="Build benchmark datasets")
    parser.add_argument("--config", type=Path, default=Path("config/product.yaml"))
    args = parser.parse_args()

    cfg = load_product_config(args.config)
    bench_cfg = cfg["benchmarks"]
    out_dir = resolve_path(bench_cfg["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    kb = load_knowledge_base(cfg)
    min_faq = int(bench_cfg.get("min_faq_pairs", 10))
    catalog_path = resolve_path(cfg["output"].get("catalog", "data/product/catalog.jsonl"))

    if bench_cfg.get("sample_from_catalog") and catalog_path.exists():
        sample = int(bench_cfg["sample_from_catalog"])
        faq_pairs = build_faq_from_catalog(catalog_path, min_faq, sample)
        gold = build_retrieval_gold_catalog(faq_pairs, catalog_path)
    else:
        faq_pairs = build_faq_benchmark(kb, min_faq)
        gold = build_retrieval_gold(faq_pairs, kb)

    write_jsonl(out_dir / "faq_pairs.jsonl", faq_pairs)

    rag_eval: list[dict] = []

    if bench_cfg.get("include_retrieval_gold", True):
        write_jsonl(out_dir / "retrieval_gold.jsonl", gold)

    if bench_cfg.get("include_rag_eval", True):
        rag_eval = build_rag_eval(faq_pairs)
        write_jsonl(out_dir / "rag_eval.jsonl", rag_eval)

    categories = sorted({p.get("category", "") for p in faq_pairs if p.get("category")})
    doc_types = sorted({p.get("doc_type", "") for p in faq_pairs if p.get("doc_type")})
    summary = {
        "faq_pairs": len(faq_pairs),
        "retrieval_gold": len(gold) if bench_cfg.get("include_retrieval_gold", True) else 0,
        "rag_eval": len(rag_eval) if bench_cfg.get("include_rag_eval", True) else 0,
        "categories_covered": len(categories),
        "doc_types_covered": len(doc_types),
        "difficulty_distribution": {
            d: sum(1 for p in faq_pairs if p.get("difficulty") == d)
            for d in ("easy", "medium", "hard")
        },
        "output_dir": str(out_dir),
    }
    with (out_dir / "benchmark_manifest.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
