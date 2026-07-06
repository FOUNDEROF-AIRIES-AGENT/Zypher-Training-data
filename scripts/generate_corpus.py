#!/usr/bin/env python3
"""Generate a massive, connected knowledge corpus with rich document relationships."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_schema import (
    DOC_TYPE_RELATIONSHIPS,
    DOCUMENT_TYPES,
    KNOWLEDGE_HUBS,
    LANGUAGE_CATEGORIES,
    RELATIONSHIP_TYPES,
)
from code_snippets import CODE_SNIPPETS, DEFAULT_CODE_LANGS
from corpus_templates import TOPICS, Topic
from mega_scale import (
    count_base_topics,
    count_expanded_topics,
    estimate_documents,
    iter_all_topics,
    resolve_mega_tier,
)

PARAPHRASE_OPENERS = [
    "In practice,",
    "For production systems,",
    "When scaling to enterprise workloads,",
    "From first principles,",
    "Under high load,",
    "During incident response,",
    "For security-sensitive deployments,",
    "When integrating with legacy systems,",
]

SECTION_TEMPLATES: dict[str, list[str]] = {
    "documentation": ["Summary", "Scope", "Key Concepts", "Usage", "References"],
    "guide": ["Overview", "Prerequisites", "Core Concepts", "Implementation Steps", "Validation", "Next Steps"],
    "tutorial": ["Goal", "Setup", "Step-by-Step", "Common Mistakes", "Exercise", "Solution Walkthrough"],
    "faq": ["Question", "Short Answer", "Detailed Explanation", "When To Use", "Related Topics"],
    "troubleshooting": ["Symptoms", "Diagnostic Steps", "Root Causes", "Fix", "Prevention"],
    "api_reference": ["Endpoint", "Authentication", "Request Schema", "Response Schema", "Error Codes"],
    "code_walkthrough": ["Problem", "Approach", "Code", "Walkthrough", "Tests"],
    "architecture_decision": ["Context", "Options Considered", "Decision", "Consequences", "Review Date"],
    "design_document": ["Goals", "Architecture", "Components", "Data Flow", "Open Questions"],
    "runbook": ["Trigger", "Severity", "Immediate Actions", "Escalation", "Recovery Verification"],
    "incident_report": ["Summary", "Timeline", "Root Cause", "Impact", "Resolution", "Lessons Learned"],
    "support_ticket": ["Problem", "Environment", "Steps Tried", "Resolution", "Related Docs"],
    "release_notes": ["Version", "Highlights", "Breaking Changes", "Migration", "Known Issues"],
    "migration_guide": ["Overview", "Prerequisites", "Step-by-Step", "Rollback", "Validation"],
    "meeting_notes": ["Attendees", "Agenda", "Decisions", "Action Items", "Follow-ups"],
    "code_review": ["Summary", "Strengths", "Issues", "Preferred Answer", "Suggested Changes"],
    "database_schema": ["Overview", "Tables", "Indexes", "Constraints", "Relationships"],
    "sql_example": ["Use Case", "Query", "Explanation", "Optimization", "Indexes"],
    "deep_dive": ["Background", "Internals", "Trade-offs", "Benchmarks", "Expert Notes"],
    "comparison": ["Criteria", "Option A", "Option B", "Recommendation", "Migration Path"],
    "best_practices": ["Principles", "Do", "Don't", "Checklist", "Examples"],
    "anti_patterns": ["Pattern", "Why It Fails", "Real Example", "Better Alternative", "Detection"],
    "cheat_sheet": ["Quick Reference", "Commands", "Configs", "Snippets", "Pitfalls"],
    "interview_prep": ["Concept", "Junior Answer", "Senior Answer", "Follow-up Questions", "Red Flags"],
    "case_study": ["Scenario", "Constraints", "Solution", "Outcome", "Lessons Learned"],
    "benchmark": ["Suite", "Methodology", "Dataset", "Metrics", "Results", "Comparison"],
    "evaluation": ["Rubric", "Good Answer", "Bad Answer", "Preferred Answer", "Scoring Guide"],
}

CODE_DOC_TYPES = frozenset({
    "code_walkthrough", "tutorial", "guide", "api_reference",
    "database_schema", "sql_example", "best_practices", "benchmark",
})

BENCHMARK_DOC_TYPES = frozenset({"benchmark", "evaluation", "comparison", "deep_dive"})


@dataclass
class GeneratedDoc:
    doc_id: str
    path: Path
    category: str
    doc_type: str
    topic: str
    difficulty: str
    variant: int
    word_count: int
    hub: str | None = None


def _pascal_case(text: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[_\s-]+", text) if part)


def _code_lang(topic: Topic) -> str:
    return LANGUAGE_CATEGORIES.get(topic.category, random.choice(DEFAULT_CODE_LANGS))


def _render_code(topic: Topic, variant: int, lang: str | None = None) -> str:
    lang = lang or _code_lang(topic)
    if lang not in CODE_SNIPPETS:
        lang = random.choice(list(CODE_SNIPPETS.keys()))
    template = CODE_SNIPPETS[lang]
    class_name = _pascal_case(topic.slug)
    return template.format(
        class_name=class_name,
        interface_name=class_name,
        function_name=f"handle{_pascal_case(topic.slug)}",
        table_name=f"{topic.category}_{variant % 1000}",
        service_name=f"{topic.category}-svc",
        docstring=topic.title,
        topic=topic.slug,
        variant=variant,
    )


def _section_body(section: str, topic: Topic, doc_type: str, variant: int) -> str:
    opener = PARAPHRASE_OPENERS[variant % len(PARAPHRASE_OPENERS)]
    keywords = ", ".join(topic.keywords)
    return (
        f"{opener} **{section}** for `{topic.title}` ({doc_type}). "
        f"This variant {variant} covers {keywords} at {topic.difficulty} level. "
        f"Key considerations include reliability, observability, latency budgets, and safe rollout. "
        f"Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. "
        f"Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data."
    )


def _benchmark_section(section: str, topic: Topic, variant: int) -> str:
    recall = 0.72 + (variant % 10) * 0.02
    p95 = 120 + variant * 15
    return (
        f"**{section}** — {topic.title} benchmark variant {variant}.\n\n"
        f"| Metric | Value |\n|--------|-------|\n"
        f"| recall@10 | {recall:.2f} |\n| p95 latency (ms) | {p95} |\n"
        f"| error rate | {0.001 * (variant + 1):.4f} |\n\n"
        f"**Good answer:** Grounded in measured results with trade-offs.\n"
        f"**Bad answer:** Claims without metrics or missing failure modes.\n"
        f"**Preferred answer:** Cites numbers, context, and next optimization steps."
    )


def _empty_relationships() -> dict[str, list[str]]:
    return {field: [] for field in RELATIONSHIP_TYPES}


def build_document(topic: Topic, doc_type: str, variant: int, scale: int) -> tuple[str, dict[str, Any]]:
    doc_id = hashlib.sha1(f"{topic.slug}:{doc_type}:{variant}:{scale}".encode()).hexdigest()[:12]
    title = f"{topic.title} — {doc_type.replace('_', ' ').title()} (v{variant})"
    sections = SECTION_TEMPLATES.get(doc_type, SECTION_TEMPLATES["guide"])

    body_parts = [f"# {title}\n"]
    for section in sections:
        if doc_type in BENCHMARK_DOC_TYPES and section in ("Benchmarks", "Results", "Metrics", "Rubric"):
            body_parts.append(f"\n## {section}\n\n{_benchmark_section(section, topic, variant)}")
        else:
            body_parts.append(f"\n## {section}\n\n{_section_body(section, topic, doc_type, variant)}")

    if doc_type in CODE_DOC_TYPES:
        lang = _code_lang(topic)
        body_parts.append(f"\n## Reference Implementation\n\n{_render_code(topic, variant, lang)}")

    if doc_type == "faq":
        body_parts.append(
            f"\n\n**Answer:** {topic.title} requires understanding {', '.join(topic.keywords)}. "
            f"Variant {variant} emphasizes operational excellence and measurable outcomes."
        )

    if doc_type == "evaluation":
        body_parts.append(
            "\n\n**Preferred answer:** Specific, actionable, cites trade-offs and metrics.\n"
            "**Bad answer:** Vague, hallucinated, or ignores provided context."
        )

    body = "".join(body_parts)
    metadata: dict[str, Any] = {
        "id": doc_id,
        "title": title,
        "category": topic.category,
        "doc_type": doc_type,
        "topic_slug": topic.slug,
        "difficulty": topic.difficulty,
        "tags": list(topic.keywords) + [doc_type, topic.category, f"variant_{variant}"],
        "variant": variant,
        "scale": scale,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "version": "3.0",
    }
    if topic.hub:
        metadata["hub"] = topic.hub
    metadata.update(_empty_relationships())
    return body, metadata


def write_document(output_dir: Path, topic: Topic, doc_type: str, variant: int, scale: int) -> GeneratedDoc:
    body, metadata = build_document(topic, doc_type, variant, scale)
    doc_id = metadata["id"]
    filename = f"{doc_id}_{topic.category}_{doc_type}_v{variant:04d}.md"
    path = output_dir / topic.category / doc_type / filename

    frontmatter = yaml.safe_dump(metadata, sort_keys=False).strip()
    content = f"---\n{frontmatter}\n---\n\n{body}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return GeneratedDoc(
        doc_id=doc_id,
        path=path,
        category=topic.category,
        doc_type=doc_type,
        topic=topic.slug,
        difficulty=topic.difficulty,
        variant=variant,
        word_count=len(body.split()),
        hub=topic.hub,
    )


def _generate_job(args: tuple) -> dict[str, Any]:
    topic_slug, topic_title, category, difficulty, keywords, variant, doc_type, scale_str, output_str, hub = args
    topic = Topic(topic_slug, topic_title, category, difficulty, tuple(keywords.split("|")), hub or None)
    scale = int(scale_str)
    output_dir = Path(output_str)
    doc = write_document(output_dir, topic, doc_type, variant, scale)
    return {
        "doc_id": doc.doc_id,
        "path": str(doc.path),
        "category": doc.category,
        "doc_type": doc.doc_type,
        "topic": doc.topic,
        "difficulty": doc.difficulty,
        "variant": doc.variant,
        "hub": doc.hub,
        "word_count": doc.word_count,
    }


def _lookup_id(index: dict[tuple[str, str, int], str], topic: str, doc_type: str, variant: int) -> str | None:
    return index.get((topic, doc_type, variant))


def wire_relationships(catalog: list[dict[str, Any]], output_dir: Path) -> int:
    """Populate typed relationship fields and rewrite frontmatter."""
    index: dict[tuple[str, str, int], str] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for row in catalog:
        key = (row["topic"], row["doc_type"], row["variant"])
        index[key] = row["doc_id"]
        by_id[row["doc_id"]] = row

    edge_count = 0
    hub_doc_types: dict[str, set[str]] = {}
    for hub in KNOWLEDGE_HUBS:
        hub_doc_types[hub.slug] = set(hub.doc_types)

    for row in catalog:
        path = Path(row["path"])
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        meta = yaml.safe_load(parts[1]) or {}
        rels = _empty_relationships()

        rules = DOC_TYPE_RELATIONSHIPS.get(row["doc_type"], {})
        for rel_type, target_types in rules.items():
            if rel_type not in RELATIONSHIP_TYPES:
                rel_type = "see_also"
            targets: list[str] = []
            for target_type in target_types:
                tid = _lookup_id(index, row["topic"], target_type, row["variant"])
                if tid:
                    targets.append(tid)
            rels[rel_type] = targets
            edge_count += len(targets)

        # Hub wiring: link to sibling doc types in same hub
        hub = row.get("hub") or meta.get("hub")
        if hub and hub in hub_doc_types:
            for sibling_type in hub_doc_types[hub]:
                if sibling_type == row["doc_type"]:
                    continue
                tid = _lookup_id(index, row["topic"], sibling_type, row["variant"])
                if tid and tid not in rels["see_also"]:
                    rels["see_also"].append(tid)
                    edge_count += 1

        # Cross-variant see_also
        if row["variant"] > 0:
            prev_id = _lookup_id(index, row["topic"], row["doc_type"], row["variant"] - 1)
            if prev_id:
                rels["replaces"].append(prev_id)
                edge_count += 1

        meta.update(rels)
        meta["related"] = list(dict.fromkeys(
            rels["see_also"] + rels["depends_on"] + rels["uses"] + rels["implements"]
        ))
        new_fm = yaml.safe_dump(meta, sort_keys=False).strip()
        body_part = parts[2].lstrip("\n")
        path.write_text(f"---\n{new_fm}\n---\n\n{body_part}", encoding="utf-8")
        row["relationships"] = {k: v for k, v in rels.items() if v}

    return edge_count


def copy_seed_corpus(seed_dir: Path, output_dir: Path) -> int:
    seed_out = output_dir / "_seed"
    seed_out.mkdir(parents=True, exist_ok=True)
    count = 0
    patterns = ["CHUNK-*.md", "configs/*", "schemas/*", "openapi/*", "kubernetes/*", "docker-compose/*"]
    for pattern in patterns:
        for path in seed_dir.glob(pattern):
            if "generated" in path.parts:
                continue
            rel = path.relative_to(seed_dir)
            dest = seed_out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                continue
            shutil.copy2(path, dest)
            count += 1
    return count


def iter_jobs(
    base_topics: list[Topic],
    categories: list[str],
    doc_types: list[str],
    variations: int,
    scale: int,
    output_dir: Path,
    mega_multiplier: int = 1,
):
    tier = resolve_mega_tier(mega_multiplier)
    effective_variants = max(1, int(variations * scale / 1000) * tier.variant_multiplier)
    for topic in iter_all_topics(base_topics, categories, mega_multiplier):
        for doc_type in doc_types:
            for variant in range(effective_variants):
                yield (
                    topic.slug,
                    topic.title,
                    topic.category,
                    topic.difficulty,
                    "|".join(topic.keywords),
                    variant,
                    doc_type,
                    str(scale),
                    str(output_dir),
                    topic.hub or "",
                )


def build_jobs(
    base_topics: list[Topic],
    categories: list[str],
    doc_types: list[str],
    variations: int,
    scale: int,
    output_dir: Path,
    mega_multiplier: int = 1,
) -> list[tuple]:
    return list(iter_jobs(base_topics, categories, doc_types, variations, scale, output_dir, mega_multiplier))


def _chunked(iterable, size: int):
    batch: list = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def run_streaming_generation(
    job_iter,
    workers: int,
    max_files: int,
    catalog_jsonl: Path,
    batch_size: int = 500,
) -> tuple[list[dict[str, Any]], int]:
    """Generate documents in batches; stream catalog to JSONL."""
    catalog: list[dict[str, Any]] = []
    completed = 0
    catalog_jsonl.parent.mkdir(parents=True, exist_ok=True)

    with catalog_jsonl.open("w", encoding="utf-8") as catalog_handle:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for batch in _chunked(job_iter, batch_size):
                if max_files and completed >= max_files:
                    break
                if max_files and completed + len(batch) > max_files:
                    batch = batch[: max_files - completed]
                futures = [executor.submit(_generate_job, job) for job in batch]
                for future in as_completed(futures):
                    row = future.result()
                    catalog.append(row)
                    catalog_handle.write(json.dumps(row) + "\n")
                    completed += 1
                    if completed % 10_000 == 0:
                        print(f"Generated {completed:,} files...")
                if max_files and completed >= max_files:
                    break
    return catalog, completed


def compute_brain_statistics(catalog: list[dict[str, Any]], edge_count: int, seed_count: int) -> dict[str, Any]:
    doc_types = [r["doc_type"] for r in catalog]
    return {
        "documents": len(catalog) + seed_count,
        "generated_documents": len(catalog),
        "seed_documents": seed_count,
        "code_examples": sum(1 for r in catalog if r["doc_type"] in CODE_DOC_TYPES),
        "apis": doc_types.count("api_reference"),
        "sql_queries": doc_types.count("sql_example") + doc_types.count("database_schema"),
        "runbooks": doc_types.count("runbook"),
        "incident_reports": doc_types.count("incident_report"),
        "adrs": doc_types.count("architecture_decision"),
        "benchmarks": doc_types.count("benchmark") + doc_types.count("evaluation"),
        "support_tickets": doc_types.count("support_ticket"),
        "relationships": edge_count,
        "knowledge_hubs": len(KNOWLEDGE_HUBS),
        "categories": len({r["category"] for r in catalog}),
        "document_types": len({r["doc_type"] for r in catalog}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate connected knowledge-base corpus at scale")
    parser.add_argument("--config", type=Path, default=Path("config/corpus_generation.yaml"))
    parser.add_argument("--scale", type=int, default=None)
    parser.add_argument("--variations", type=int, default=None)
    parser.add_argument("--mega-multiplier", type=int, default=None, help="Mega expansion (e.g. 100000000000)")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--seed-dir", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--max-files", type=int, default=0, help="Cap files (0=unlimited)")
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--skip-wiring", action="store_true", help="Skip graph wiring (fast mega runs)")
    parser.add_argument("--append", action="store_true", help="Append to existing corpus")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with args.config.open(encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)

    scale = args.scale if args.scale is not None else int(cfg.get("scale", 1000))
    variations = args.variations if args.variations is not None else int(cfg.get("variations_per_doc", 12))
    mega_multiplier = args.mega_multiplier if args.mega_multiplier is not None else int(cfg.get("mega_multiplier", 1))
    output_dir = args.output_dir or Path(cfg.get("output_dir", "knowledge-base/generated"))
    seed_dir = args.seed_dir or Path(cfg.get("seed_dir", "knowledge-base"))
    workers = args.workers or int(cfg.get("parallel_workers", 4))
    doc_types = cfg.get("document_types", DOCUMENT_TYPES)
    categories = list(cfg.get("categories", []))

    tier = resolve_mega_tier(mega_multiplier)
    base_count = count_base_topics(TOPICS, categories)
    expanded_count = count_expanded_topics(categories, mega_multiplier)
    estimated = estimate_documents(categories, len(doc_types), variations, scale, mega_multiplier, base_count)

    print(f"Tier: {tier.name} — {tier.description}")
    print(f"Base topics: {base_count:,} | Expanded topics: {expanded_count:,}")
    print(f"Total topics (virtual): {(base_count + expanded_count):,}")
    print(f"Document types: {len(doc_types)}")
    print(f"Scale: {scale}, variations: {variations}, mega_multiplier: {mega_multiplier:,}")
    print(f"Estimated documents: {estimated:,}")
    if args.max_files:
        print(f"Cap (max-files): {args.max_files:,}")

    if args.dry_run:
        return

    if not args.append and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    seed_count = 0
    if not args.append:
        seed_count = copy_seed_corpus(seed_dir, output_dir)
        print(f"Copied {seed_count} seed files to {output_dir / '_seed'}")

    job_iter = iter_jobs(TOPICS, categories, doc_types, variations, scale, output_dir, mega_multiplier)
    catalog_jsonl = output_dir / "catalog.jsonl"
    catalog, completed = run_streaming_generation(
        job_iter,
        workers=workers,
        max_files=args.max_files,
        catalog_jsonl=catalog_jsonl,
        batch_size=args.batch_size,
    )
    print(f"Generated {completed:,} files")

    skip_wiring = args.skip_wiring or completed > 50_000 or mega_multiplier > 1_000_000
    edge_count = 0
    if skip_wiring:
        print("Skipping relationship wiring (mega mode — use shard-local wiring for smaller batches)")
    else:
        print("Wiring document relationships...")
        edge_count = wire_relationships(catalog, output_dir)

    brain_stats = compute_brain_statistics(catalog, edge_count, seed_count)
    brain_stats["mega_tier"] = tier.name
    brain_stats["mega_multiplier"] = mega_multiplier
    brain_stats["estimated_capacity"] = estimated

    stats = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scale": scale,
        "mega_multiplier": mega_multiplier,
        "mega_tier": tier.name,
        "variations_per_doc": variations,
        "topics_base": base_count,
        "topics_expanded": expanded_count,
        "topics_total": base_count + expanded_count,
        "generated_files": completed,
        "brain_statistics": brain_stats,
        "by_category": {},
        "by_doc_type": {},
    }
    for row in catalog:
        stats["by_category"][row["category"]] = stats["by_category"].get(row["category"], 0) + 1
        stats["by_doc_type"][row["doc_type"]] = stats["by_doc_type"].get(row["doc_type"], 0) + 1

    catalog_path = output_dir / "catalog.json"
    catalog_path.write_text(
        json.dumps({"stats": stats, "files": catalog[:1000], "catalog_jsonl": str(catalog_jsonl)}, indent=2),
        encoding="utf-8",
    )
    (output_dir / "brain_statistics.json").write_text(json.dumps(brain_stats, indent=2), encoding="utf-8")
    print(json.dumps({**stats, "by_category": f"{len(stats['by_category'])} categories"}, indent=2))
    print(f"Catalog: {catalog_path} + {catalog_jsonl}")


if __name__ == "__main__":
    main()
