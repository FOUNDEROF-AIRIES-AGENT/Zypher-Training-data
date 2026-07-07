"""Coltex schema — document types, categories, relationships, and knowledge hubs."""

from __future__ import annotations

from dataclasses import dataclass

# Rich relationship types (GraphRAG edges)
RELATIONSHIP_TYPES = (
    "related",
    "depends_on",
    "uses",
    "implements",
    "calls",
    "owned_by",
    "documents",
    "fixes",
    "replaces",
    "see_also",
    # Advanced neural edge types
    "extends",
    "validates",
    "contradicts",
    "synthesizes",
    "triggers",
    "inhibits",
    "supersedes",
    "derived_from",
    "tested_by",
    "deployed_via",
)

# Premium dataset tier — 50 categories × 20 doc types (single source of truth)
PREMIUM_CATEGORIES: tuple[str, ...] = (
    # RAG & AI (13)
    "rag", "graphrag", "agentic", "chunking", "embeddings", "vector_stores",
    "vector_search", "retrieval", "indexing", "fine_tuning", "prompt_engineering",
    "tool_use", "memory",
    # Languages (8)
    "python", "java", "javascript", "typescript", "go", "rust", "sql", "csharp",
    # Databases (4)
    "postgresql", "mongodb", "redis", "mysql",
    # Cloud & DevOps (8)
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ci_cd", "linux",
    # Architecture (5)
    "microservices", "event_driven", "architecture", "api_design", "domain_driven_design",
    # Engineering practice (8)
    "security", "observability", "testing", "performance", "code_review", "incidents",
    "data_quality", "mlops",
    # Tools (4)
    "git", "github_actions", "nginx", "bash",
)

PREMIUM_DOC_TYPES: tuple[str, ...] = (
    "documentation", "guide", "tutorial", "faq", "api_reference", "runbook",
    "architecture_decision", "code_walkthrough", "best_practices", "benchmark",
    "evaluation", "troubleshooting", "incident_report", "design_document",
    "migration_guide", "release_notes", "database_schema", "deep_dive",
    "comparison", "case_study",
)

PREMIUM_CATEGORY_PHRASES: dict[str, str] = {
    "rag": "RAG Systems",
    "graphrag": "GraphRAG",
    "agentic": "Agentic AI",
    "chunking": "Document Chunking",
    "embeddings": "Embedding Models",
    "vector_stores": "Vector Stores",
    "vector_search": "Vector Search",
    "retrieval": "Retrieval Pipelines",
    "indexing": "Indexing Pipelines",
    "fine_tuning": "Fine-Tuning",
    "prompt_engineering": "Prompt Engineering",
    "tool_use": "Tool Use",
    "memory": "Agent Memory",
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "go": "Go",
    "rust": "Rust",
    "sql": "SQL",
    "csharp": "C#",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "mysql": "MySQL",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "Google Cloud",
    "terraform": "Terraform",
    "ci_cd": "CI/CD",
    "linux": "Linux",
    "microservices": "Microservices",
    "event_driven": "Event-Driven Architecture",
    "architecture": "System Architecture",
    "api_design": "API Design",
    "domain_driven_design": "Domain-Driven Design",
    "security": "Security",
    "observability": "Observability",
    "testing": "Testing",
    "performance": "Performance",
    "code_review": "Code Review",
    "incidents": "Incident Management",
    "data_quality": "Data Quality",
    "mlops": "MLOps",
    "git": "Git",
    "github_actions": "GitHub Actions",
    "nginx": "Nginx",
    "bash": "Bash",
}

# Document types the brain can generate and index
DOCUMENT_TYPES = [
    # Core documentation
    "documentation",
    "guide",
    "tutorial",
    "faq",
    "troubleshooting",
    # Operations
    "runbook",
    "incident_report",
    "support_ticket",
    "release_notes",
    "migration_guide",
    # Engineering
    "api_reference",
    "architecture_decision",
    "design_document",
    "code_walkthrough",
    "code_review",
    "meeting_notes",
    # Data & SQL
    "database_schema",
    "sql_example",
    # Learning & reference
    "deep_dive",
    "comparison",
    "best_practices",
    "anti_patterns",
    "cheat_sheet",
    "interview_prep",
    "case_study",
    # Evaluation
    "benchmark",
    "evaluation",
]

# How doc types link within the same knowledge hub / topic
DOC_TYPE_RELATIONSHIPS: dict[str, dict[str, list[str]]] = {
    "api_reference": {
        "see_also": ["runbook", "faq", "troubleshooting"],
        "documents": ["architecture_decision"],
        "uses": ["database_schema"],
        "calls": ["code_walkthrough"],
    },
    "runbook": {
        "fixes": ["incident_report"],
        "uses": ["api_reference"],
        "depends_on": ["architecture_decision"],
        "see_also": ["troubleshooting"],
    },
    "architecture_decision": {
        "documents": ["design_document"],
        "see_also": ["api_reference", "runbook"],
        "replaces": ["meeting_notes"],
    },
    "incident_report": {
        "fixes": ["troubleshooting"],
        "see_also": ["runbook", "incident_report"],
        "owned_by": ["runbook"],
    },
    "code_walkthrough": {
        "implements": ["architecture_decision", "design_document"],
        "calls": ["api_reference"],
        "see_also": ["best_practices"],
    },
    "database_schema": {
        "documents": ["sql_example"],
        "used_by": ["api_reference"],  # mapped to see_also at wire time
    },
    "sql_example": {
        "uses": ["database_schema"],
        "see_also": ["best_practices", "troubleshooting"],
    },
    "benchmark": {
        "documents": ["evaluation"],
        "see_also": ["comparison", "deep_dive"],
    },
    "evaluation": {
        "see_also": ["benchmark", "code_review"],
    },
    "support_ticket": {
        "fixes": ["troubleshooting"],
        "see_also": ["runbook", "faq"],
    },
    "migration_guide": {
        "replaces": ["documentation"],
        "depends_on": ["architecture_decision"],
        "see_also": ["release_notes"],
    },
    "design_document": {
        "documents": ["api_reference", "code_walkthrough"],
        "see_also": ["architecture_decision"],
    },
}

CATEGORIES = [
    # RAG & AI
    "rag",
    "graphrag",
    "agentic",
    "chunking",
    "embeddings",
    "vector_stores",
    "vector_search",
    "retrieval",
    "indexing",
    "fine_tuning",
    "prompt_engineering",
    "tool_use",
    "memory",
    # Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "csharp",
    "cpp",
    "go",
    "rust",
    "sql",
    "html_css",
    "bash",
    "powershell",
    # Databases
    "postgresql",
    "mysql",
    "sqlite",
    "mongodb",
    "redis",
    # Cloud & DevOps
    "docker",
    "kubernetes",
    "github_actions",
    "gitlab_ci",
    "aws",
    "azure",
    "gcp",
    "linux",
    "nginx",
    "terraform",
    "ci_cd",
  # Architecture
    "microservices",
    "event_driven",
    "cqrs",
    "architecture",
    "clean_architecture",
    "domain_driven_design",
    # Engineering practice
    "api_design",
    "security",
    "observability",
    "testing",
    "debugging",
    "performance",
    "code_review",
    "incidents",
    "data_quality",
    "mlops",
    # Tools
    "git",
    "github",
    "package_managers",
    "build_tools",
    "terminal",
]

# Category → preferred code snippet language
LANGUAGE_CATEGORIES: dict[str, str] = {
    "python": "python",
    "java": "java",
    "javascript": "javascript",
    "typescript": "typescript",
    "csharp": "csharp",
    "cpp": "cpp",
    "go": "go",
    "rust": "rust",
    "sql": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "sqlite": "sql",
    "html_css": "html_css",
    "bash": "bash",
    "powershell": "powershell",
    "docker": "dockerfile",
    "kubernetes": "yaml",
    "terraform": "hcl",
    "nginx": "nginx",
    "github_actions": "yaml",
    "gitlab_ci": "yaml",
    "mongodb": "javascript",
    "redis": "bash",
}

# Example brain scale statistics (grow with corpus generation)
BRAIN_STATISTICS_EXAMPLES = {
    "documents": 250_000,
    "code_examples": 75_000,
    "apis": 30_000,
    "sql_queries": 20_000,
    "runbooks": 15_000,
    "incident_reports": 10_000,
    "adrs": 5_000,
    "relationships": 1_000_000,
}


@dataclass(frozen=True)
class KnowledgeHub:
    """Connected document cluster — e.g. Authentication Service."""

    slug: str
    title: str
    category: str
    components: tuple[str, ...]
    doc_types: tuple[str, ...]


KNOWLEDGE_HUBS: list[KnowledgeHub] = [
    KnowledgeHub(
        "auth_service",
        "Authentication Service",
        "security",
        ("JWT", "PostgreSQL", "OAuth", "RBAC", "Session Management"),
        (
            "api_reference",
            "runbook",
            "architecture_decision",
            "incident_report",
            "code_walkthrough",
            "database_schema",
            "sql_example",
            "best_practices",
            "troubleshooting",
            "benchmark",
        ),
    ),
    KnowledgeHub(
        "indexing_pipeline",
        "Document Indexing Pipeline",
        "indexing",
        ("Embeddings", "Vector Store", "Chunking", "HNSW", "Kafka"),
        (
            "api_reference",
            "runbook",
            "architecture_decision",
            "code_walkthrough",
            "troubleshooting",
            "benchmark",
            "design_document",
        ),
    ),
    KnowledgeHub(
        "graphrag_engine",
        "GraphRAG Engine",
        "graphrag",
        ("Knowledge Graph", "AST Parser", "Traversal", "Vector Search"),
        (
            "api_reference",
            "architecture_decision",
            "deep_dive",
            "code_walkthrough",
            "benchmark",
            "evaluation",
        ),
    ),
    KnowledgeHub(
        "payment_service",
        "Payment Processing Service",
        "microservices",
        ("Stripe API", "PostgreSQL", "Idempotency", "Webhooks", "PCI"),
        (
            "api_reference",
            "runbook",
            "incident_report",
            "database_schema",
            "sql_example",
            "architecture_decision",
            "migration_guide",
        ),
    ),
    KnowledgeHub(
        "ci_cd_platform",
        "CI/CD Platform",
        "ci_cd",
        ("GitHub Actions", "Docker", "Kubernetes", "Terraform", "Canary Deploy"),
        (
            "runbook",
            "troubleshooting",
            "release_notes",
            "migration_guide",
            "best_practices",
            "incident_report",
        ),
    ),
    KnowledgeHub(
        "vector_store_cluster",
        "Vector Store Cluster",
        "vector_stores",
        ("ChromaDB", "HNSW", "pgvector", "Sharding", "Replication"),
        (
            "architecture_decision",
            "benchmark",
            "runbook",
            "api_reference",
            "deep_dive",
            "troubleshooting",
        ),
    ),
    KnowledgeHub(
        "embedding_service",
        "Embedding Service",
        "embeddings",
        ("MiniLM", "Batch Encoding", "GPU Pipeline", "Model Registry"),
        (
            "api_reference",
            "architecture_decision",
            "benchmark",
            "code_walkthrough",
            "best_practices",
        ),
    ),
    KnowledgeHub(
        "agent_orchestrator",
        "Agent Orchestrator",
        "agentic",
        ("ReAct", "Tool Registry", "Memory Buffer", "Planning Loop"),
        (
            "architecture_decision",
            "deep_dive",
            "code_walkthrough",
            "evaluation",
            "benchmark",
        ),
    ),
    KnowledgeHub(
        "observability_stack",
        "Observability Stack",
        "observability",
        ("OpenTelemetry", "Prometheus", "Grafana", "Structured Logging"),
        (
            "runbook",
            "architecture_decision",
            "troubleshooting",
            "benchmark",
            "best_practices",
        ),
    ),
    KnowledgeHub(
        "rag_retrieval_core",
        "RAG Retrieval Core",
        "rag",
        ("Hybrid Search", "Reranking", "Context Window", "Citation Tracking"),
        (
            "deep_dive",
            "benchmark",
            "evaluation",
            "architecture_decision",
            "api_reference",
        ),
    ),
    KnowledgeHub(
        "security_operations",
        "Security Operations Center",
        "security",
        ("SIEM", "Threat Detection", "Zero Trust", "Secrets Management"),
        (
            "runbook",
            "incident_report",
            "architecture_decision",
            "troubleshooting",
            "best_practices",
        ),
    ),
    KnowledgeHub(
        "data_pipeline",
        "Data Ingestion Pipeline",
        "data_quality",
        ("ETL", "CDC", "Schema Validation", "Deduplication"),
        (
            "architecture_decision",
            "runbook",
            "code_walkthrough",
            "benchmark",
            "migration_guide",
        ),
    ),
    KnowledgeHub(
        "llm_inference_gateway",
        "LLM Inference Gateway",
        "rag",
        ("OpenAI API", "Streaming", "Rate Limiting", "Token Budget"),
        (
            "api_reference",
            "architecture_decision",
            "runbook",
            "benchmark",
            "troubleshooting",
        ),
    ),
    KnowledgeHub(
        "knowledge_graph_store",
        "Knowledge Graph Store",
        "graphrag",
        ("Neo4j", "Edge Types", "PageRank", "Community Detection"),
        (
            "deep_dive",
            "architecture_decision",
            "benchmark",
            "code_walkthrough",
            "evaluation",
        ),
    ),
    KnowledgeHub(
        "incident_command",
        "Incident Command System",
        "incidents",
        ("PagerDuty", "Postmortem", "SLA Tracking", "War Room"),
        (
            "runbook",
            "incident_report",
            "troubleshooting",
            "best_practices",
            "meeting_notes",
        ),
    ),
    KnowledgeHub(
        "ml_training_pipeline",
        "ML Training Pipeline",
        "mlops",
        ("LoRA", "Dataset Curation", "Eval Harness", "Model Registry"),
        (
            "architecture_decision",
            "benchmark",
            "code_walkthrough",
            "evaluation",
            "migration_guide",
        ),
    ),
    KnowledgeHub(
        "api_gateway",
        "API Gateway",
        "api_design",
        ("Kong", "Rate Limits", "JWT Validation", "Route Tables"),
        (
            "api_reference",
            "architecture_decision",
            "runbook",
            "troubleshooting",
            "best_practices",
        ),
    ),
    KnowledgeHub(
        "coltex_knowledge_core",
        "Coltex Knowledge Core",
        "rag",
        ("Catalog Index", "Corpus Report", "Graph Links", "Processing Layers", "Memory Tiers"),
        (
            "deep_dive",
            "architecture_decision",
            "guide",
            "benchmark",
            "evaluation",
        ),
    ),
]
