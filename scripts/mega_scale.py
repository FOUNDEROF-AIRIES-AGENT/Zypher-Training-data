"""Mega-scale topic expansion for Coltex corpus generation."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from corpus_templates import Topic

SERVICE_PREFIXES = (
    "auth", "billing", "catalog", "checkout", "search", "indexer", "ingestion",
    "notification", "payment", "profile", "recommendation", "analytics", "audit",
    "gateway", "scheduler", "workflow", "inventory", "shipping", "support",
    "telemetry", "config", "secrets", "cache", "queue", "stream", "ml", "rag",
)

COMPONENT_SUFFIXES = (
    "api", "worker", "scheduler", "database", "cache", "queue", "gateway",
    "controller", "service", "pipeline", "processor", "store", "index",
    "connector", "adapter", "broker", "proxy", "agent", "engine", "runtime",
)

MEGA_ASPECTS = (
    "fundamentals", "patterns", "pitfalls", "scaling", "monitoring", "security",
    "testing", "migration", "integration", "optimization", "troubleshooting",
    "benchmarks", "cost_analysis", "team_workflows", "enterprise_rollout",
    "edge_cases", "versioning", "compliance", "disaster_recovery", "multi_tenant",
    "observability", "reliability", "performance", "capacity", "onboarding",
    "deprecation", "governance", "automation", "orchestration", "resilience",
)

from brain_schema import PREMIUM_CATEGORY_PHRASES

CATEGORY_PHRASES: dict[str, str] = PREMIUM_CATEGORY_PHRASES


@dataclass(frozen=True)
class MegaTier:
    name: str
    shards: int
    services_per_category: int
    aspects: int
    variant_multiplier: int
    description: str


def resolve_mega_tier(mega_multiplier: int) -> MegaTier:
    if mega_multiplier >= 100_000_000_000:
        return MegaTier("hyper", 10_000, 1_000, len(MEGA_ASPECTS), 100,
                        "Hyper — billions of documents (Vast.ai cluster)")
    if mega_multiplier >= 1_000_000_000:
        return MegaTier("ultra", 1_000, 500, len(MEGA_ASPECTS), 50,
                        "Ultra — hundreds of millions")
    if mega_multiplier >= 1_000_000:
        return MegaTier("mega", 100, 100, 20, 24, "Mega — tens of millions")
    if mega_multiplier >= 10_000:
        return MegaTier("large", 20, 50, 15, 12, "Large — millions")
    return MegaTier("standard", 1, 1, 10, 1, "Standard")


def count_expanded_topics(categories: list[str], mega_multiplier: int) -> int:
    if mega_multiplier <= 1:
        return 0
    tier = resolve_mega_tier(mega_multiplier)
    return len(categories) * tier.shards * tier.services_per_category * tier.aspects


def estimate_documents(
    categories: list[str],
    doc_types: int,
    variations: int,
    scale: int,
    mega_multiplier: int,
    base_topic_count: int,
) -> int:
    tier = resolve_mega_tier(mega_multiplier)
    total_topics = base_topic_count + count_expanded_topics(categories, mega_multiplier)
    effective_variants = max(1, int(variations * scale / 1000) * tier.variant_multiplier)
    return total_topics * doc_types * effective_variants


def iter_expanded_topics(categories: list[str], mega_multiplier: int) -> Iterator[Topic]:
    """Yield topics procedurally — never loads all into memory."""
    if mega_multiplier <= 1:
        return
    tier = resolve_mega_tier(mega_multiplier)
    aspects = MEGA_ASPECTS[: tier.aspects]
    for category in categories:
        phrase = CATEGORY_PHRASES.get(category, category.replace("_", " ").title())
        for shard in range(tier.shards):
            for svc_idx in range(tier.services_per_category):
                service = SERVICE_PREFIXES[svc_idx % len(SERVICE_PREFIXES)]
                component = COMPONENT_SUFFIXES[(svc_idx + shard) % len(COMPONENT_SUFFIXES)]
                for aspect in aspects:
                    slug = f"{category}_s{shard:05d}_{service}_{component}_{aspect}"
                    title = (
                        f"{phrase} / {service}-{component} (shard {shard}): "
                        f"{aspect.replace('_', ' ').title()}"
                    )
                    yield Topic(
                        slug=slug,
                        title=title,
                        category=category,
                        difficulty=["beginner", "intermediate", "advanced", "expert"][svc_idx % 4],
                        keywords=(category, service, component, aspect, f"shard_{shard}"),
                        hub=f"{service}_{component}_{category}",
                    )


def iter_all_topics(
    base_topics: list[Topic],
    categories: list[str],
    mega_multiplier: int,
) -> Iterator[Topic]:
    cat_set = set(categories)
    for topic in base_topics:
        if topic.category in cat_set:
            yield topic
    yield from iter_expanded_topics(categories, mega_multiplier)


def count_base_topics(base_topics: list[Topic], categories: list[str]) -> int:
    cat_set = set(categories)
    return sum(1 for t in base_topics if t.category in cat_set)
