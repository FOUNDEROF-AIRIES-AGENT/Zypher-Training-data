"""Premium distributable document generator — original synthetic RAG corpus."""

from __future__ import annotations

import hashlib
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from brain.types import Document
from brain_schema import PREMIUM_DOC_TYPES
from code_snippets import CODE_SNIPPETS, DEFAULT_CODE_LANGS
from corpus_templates import TOPICS, Topic
from mega_scale import estimate_documents, iter_all_topics, resolve_mega_tier, count_base_topics

PREMIUM_SECTIONS: dict[str, list[str]] = {
    "documentation": ["Executive Summary", "Architecture", "Implementation", "Operations", "Security", "Metrics"],
    "guide": ["Overview", "Prerequisites", "Step-by-Step", "Validation", "Production Rollout", "Troubleshooting"],
    "tutorial": ["Learning Objectives", "Environment Setup", "Core Walkthrough", "Exercises", "Solution", "Next Steps"],
    "faq": ["Question", "Short Answer", "Detailed Explanation", "When To Apply", "Anti-Patterns", "References"],
    "api_reference": ["Endpoint Overview", "Authentication", "Request Schema", "Response Schema", "Error Codes", "Examples"],
    "runbook": ["Trigger Conditions", "Severity", "Immediate Actions", "Escalation", "Recovery", "Post-Incident"],
    "architecture_decision": ["Context", "Options", "Decision", "Consequences", "Review Schedule", "Stakeholders"],
    "code_walkthrough": ["Problem Statement", "Design", "Implementation", "Testing Strategy", "Deployment", "Monitoring"],
    "best_practices": ["Principles", "Recommended Patterns", "Common Mistakes", "Checklist", "Examples", "Metrics"],
    "benchmark": ["Methodology", "Dataset", "Metrics", "Results", "Comparison", "Recommendations"],
    "evaluation": ["Rubric", "Gold Answer", "Acceptable Answer", "Poor Answer", "Scoring", "Calibration"],
    "troubleshooting": ["Symptoms", "Diagnostics", "Root Causes", "Resolution", "Prevention", "Verification"],
    "incident_report": ["Summary", "Timeline", "Root Cause", "Impact", "Resolution", "Lessons Learned"],
    "design_document": ["Goals", "Architecture", "Components", "Data Flow", "Trade-offs", "Open Questions"],
    "migration_guide": ["Overview", "Prerequisites", "Migration Steps", "Rollback", "Validation", "Post-Migration"],
    "release_notes": ["Version", "Highlights", "Breaking Changes", "Migration", "Known Issues", "Upgrade Path"],
    "database_schema": ["Overview", "Tables", "Indexes", "Constraints", "Relationships", "Migration Notes"],
    "deep_dive": ["Background", "Internals", "Trade-offs", "Benchmarks", "Expert Notes", "Further Reading"],
    "comparison": ["Criteria", "Option A", "Option B", "Recommendation", "Migration Path", "Decision Matrix"],
    "case_study": ["Scenario", "Constraints", "Solution", "Outcome", "Metrics", "Lessons Learned"],
}

OPENERS = (
    "In enterprise Coltex deployments,",
    "For production-grade RAG systems,",
    "When scaling to multi-tenant workloads,",
    "Under strict latency and compliance requirements,",
    "During platform modernization initiatives,",
    "For security-sensitive code intelligence pipelines,",
    "When onboarding a new engineering team to Coltex,",
    "During a quarterly architecture review,",
    "For regulated industries requiring audit trails,",
    "When migrating legacy documentation into Coltex,",
)

CONCRETE_DETAILS = (
    "Configure circuit breakers with a 30-second half-open window and exponential backoff.",
    "Use idempotency keys on all write endpoints to prevent duplicate side effects.",
    "Partition data by tenant_id and enforce row-level security at the database layer.",
    "Deploy canary releases at 5% traffic before full rollout with automated rollback.",
    "Index metadata fields (doc_type, category, hub) alongside dense vectors for hybrid search.",
    "Run weekly chaos drills that simulate vector store failover and embedding service outage.",
    "Cache hot queries in Redis with a 15-minute TTL and stale-while-revalidate policy.",
    "Emit OpenTelemetry spans on every retrieval hop for end-to-end latency attribution.",
)

LANGUAGE_MAP = {
    "python": "python", "java": "java", "javascript": "javascript", "typescript": "typescript",
    "go": "go", "rust": "rust", "sql": "sql", "postgresql": "sql", "mysql": "sql",
    "csharp": "csharp", "bash": "bash", "mongodb": "javascript", "redis": "bash",
}


def estimate_premium_documents(
    categories: list[str],
    mega_multiplier: int,
    scale: int = 10_000,
    variations: int = 24,
    doc_types: int | None = None,
    base_topics: int | None = None,
) -> int:
    dt = doc_types or len(PREMIUM_DOC_TYPES)
    base = base_topics if base_topics is not None else len([t for t in TOPICS if t.category in categories])
    return estimate_documents(categories, dt, variations, scale, mega_multiplier, base)


def _pascal(text: str) -> str:
    return "".join(p.capitalize() for p in text.replace("-", "_").split("_") if p)


def _render_code(topic: Topic, variant: int) -> str:
    lang = LANGUAGE_MAP.get(topic.category, "python")
    if lang not in CODE_SNIPPETS:
        lang = DEFAULT_CODE_LANGS[variant % len(DEFAULT_CODE_LANGS)]
    template = CODE_SNIPPETS[lang]
    name = _pascal(topic.slug[:40])
    return template.format(
        class_name=name,
        interface_name=name,
        function_name=f"handle{name}",
        table_name=f"{topic.category}_{variant % 10_000}",
        service_name=f"{topic.category}-svc",
        docstring=topic.title[:120],
        topic=topic.slug,
        variant=variant,
    )


def _section_body(section: str, topic: Topic, doc_type: str, variant: int) -> str:
    opener = OPENERS[variant % len(OPENERS)]
    kw = ", ".join(topic.keywords[:5])
    recall = 0.68 + (variant % 20) * 0.015
    p95 = 85 + (variant % 50) * 8
    detail = CONCRETE_DETAILS[(variant + hash(section)) % len(CONCRETE_DETAILS)]
    shard_note = f"shard-{variant % 1000:03d}" if "shard" in topic.slug else f"hub-{topic.hub or topic.category}"
    return (
        f"{opener} the **{section}** layer for `{topic.title}` requires explicit engineering "
        f"for {kw} at **{topic.difficulty}** complexity (variant {variant}, {shard_note}).\n\n"
        f"**Design requirements:**\n"
        f"- Define SLOs: p95 latency ≤ {p95}ms, availability ≥ 99.9%, retrieval recall@10 ≥ {recall:.2f}\n"
        f"- Add structured logging, distributed tracing, and audit trails for all write paths\n"
        f"- Version schemas; use feature flags for rollout; document rollback procedures\n"
        f"- Validate with integration tests and chaos drills before production promotion\n"
        f"- {detail}\n\n"
        f"**Operational checklist:**\n"
        f"1. Verify graph edges link `{topic.category}` documents to related hubs\n"
        f"2. Confirm chunk overlap preserves context across section boundaries\n"
        f"3. Run retrieval gold benchmarks after each corpus update\n"
        f"4. Monitor duplicate chunk ratio stays below 5%"
    )
    )


def build_premium_body(topic: Topic, doc_type: str, variant: int) -> str:
    title = f"{topic.title} — {doc_type.replace('_', ' ').title()} (v{variant:04d})"
    sections = PREMIUM_SECTIONS.get(doc_type, PREMIUM_SECTIONS["guide"])
    parts = [f"# {title}\n"]
    for section in sections:
        parts.append(f"\n## {section}\n\n{_section_body(section, topic, doc_type, variant)}")
    code_doc_types = (
        "code_walkthrough", "tutorial", "api_reference", "guide", "best_practices",
        "database_schema", "migration_guide", "design_document",
    )
    if doc_type in code_doc_types:
        parts.append(f"\n## Reference Implementation\n\n```\n{_render_code(topic, variant)}\n```")
    if doc_type == "faq":
        parts.append(
            f"\n\n**Answer:** {topic.title} in Coltex requires rigorous indexing, graph linking, "
            f"and evaluation. Variant {variant} targets {topic.hub or topic.category} with "
            f"measurable recall and faithfulness thresholds."
        )
    if doc_type == "benchmark":
        parts.append(
            f"\n\n| Metric | Target |\n|--------|--------|\n"
            f"| recall@10 | ≥ {0.68 + (variant % 20) * 0.015:.2f} |\n"
            f"| faithfulness | ≥ 0.85 |\n| p95 (ms) | ≤ {85 + (variant % 50) * 8} |"
        )
    return "\n".join(parts)


def build_premium_metadata(
    topic: Topic,
    doc_type: str,
    variant: int,
    scale: int,
    related_ids: list[str] | None = None,
) -> dict[str, Any]:
    doc_id = hashlib.sha1(f"premium:{topic.slug}:{doc_type}:{variant}:{scale}".encode()).hexdigest()[:16]
    doc_id = f"DIST-{doc_id.upper()}"
    return {
        "id": doc_id,
        "title": f"{topic.title} — {doc_type.replace('_', ' ').title()} (v{variant:04d})",
        "category": topic.category,
        "doc_type": doc_type,
        "hub": topic.hub or topic.category,
        "tags": list(dict.fromkeys([topic.category, doc_type, topic.difficulty, "premium", "distributable"])),
        "difficulty": topic.difficulty,
        "related": related_ids or [],
        "origin": "coltex_premium_synthetic",
        "variant": variant,
    }


def format_premium_markdown(meta: dict[str, Any], body: str) -> str:
    import yaml
    front = yaml.safe_dump(meta, sort_keys=False).strip()
    return f"---\n{front}\n---\n\n{body}"


@dataclass
class PremiumGenerationStats:
    documents: int = 0
    chunks: int = 0
    edges: int = 0
    bytes_written: int = 0


def iter_premium_documents(
    categories: list[str],
    mega_multiplier: int,
    scale: int = 10_000,
    variations: int = 24,
    max_documents: int = 0,
    seed_multiplier: int = 1,
) -> Iterator[tuple[Document, dict[str, Any]]]:
    """Yield premium Document objects procedurally — never loads all into memory."""
    tier = resolve_mega_tier(mega_multiplier)
    # Bounded builds use base topics only for category diversity (not hyper shards)
    topic_mega = 1 if max_documents else mega_multiplier
    topic_count = count_base_topics(TOPICS, categories) if topic_mega == 1 else None
    jobs_per_round = (topic_count or 1) * len(PREMIUM_DOC_TYPES)

    raw_variants = max(1, int(variations * scale / 1000) * tier.variant_multiplier * seed_multiplier)
    if max_documents and topic_count:
        max_rounds = max(1, (max_documents + jobs_per_round - 1) // jobs_per_round)
        effective_variants = min(raw_variants, max_rounds)
    else:
        effective_variants = raw_variants

    hub_recent: dict[str, list[str]] = {}
    count = 0

    for variant in range(effective_variants):
        for topic in iter_all_topics(TOPICS, categories, topic_mega):
            for doc_type in PREMIUM_DOC_TYPES:
                if max_documents and count >= max_documents:
                    return
                hub = topic.hub or topic.category
                related = hub_recent.get(hub, [])[-5:]
                meta = build_premium_metadata(topic, doc_type, variant, scale, related)
                body = build_premium_body(topic, doc_type, variant)
                path = (
                    f"knowledge-base/distributable/{topic.category}/{doc_type}/"
                    f"{meta['id'].lower()}_{topic.slug[:48]}_v{variant:04d}.md"
                )
                doc = Document(
                    doc_id=meta["id"],
                    title=meta["title"],
                    path=path,
                    content=body,
                    category=topic.category,
                    doc_type=doc_type,
                    hub=hub,
                    tags=meta["tags"],
                    related=related,
                    relationships={"see_also": related, "depends_on": related[:2]},
                )
                hub_recent.setdefault(hub, []).append(meta["id"])
                if len(hub_recent[hub]) > 20:
                    hub_recent[hub] = hub_recent[hub][-20:]
                yield doc, meta
                count += 1
