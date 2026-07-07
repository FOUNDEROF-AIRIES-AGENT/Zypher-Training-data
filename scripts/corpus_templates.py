"""Topic and template definitions for scalable knowledge-base generation."""

from __future__ import annotations

from dataclasses import dataclass

from brain_schema import KNOWLEDGE_HUBS, PREMIUM_CATEGORY_PHRASES

ADVANCED_TASK_TYPES = [
    "single_turn_qa",
    "multi_turn_dialogue",
    "chain_of_thought",
    "tool_calling",
    "rag_with_context",
    "code_generation",
    "code_review",
    "debugging_session",
    "architecture_consultation",
    "incident_triage",
    "refactoring",
    "unit_test_generation",
    "api_design_review",
    "security_audit",
    "performance_analysis",
    "graph_traversal",
    "benchmark_interpretation",
    "evaluation_rubric",
]


@dataclass(frozen=True)
class Topic:
    slug: str
    title: str
    category: str
    difficulty: str
    keywords: tuple[str, ...]
    hub: str | None = None


def _hub_topics() -> list[Topic]:
    topics: list[Topic] = []
    for hub in KNOWLEDGE_HUBS:
        for component in hub.components:
            slug = f"{hub.slug}_{component.lower().replace(' ', '_')}"
            topics.append(
                Topic(
                    slug=slug,
                    title=f"{hub.title}: {component}",
                    category=hub.category,
                    difficulty="intermediate",
                    keywords=(hub.slug, component.lower(), hub.category),
                    hub=hub.slug,
                )
            )
    return topics


def _topics() -> list[Topic]:
    topics: list[Topic] = []
    seeds = [
        ("hybrid_search", "Hybrid Search with BM25 and Dense Retrieval", "retrieval", "advanced",
         ("bm25", "dense", "fusion", "reranking")),
        ("graph_traversal", "Graph Traversal for Dependency Analysis", "graphrag", "advanced",
         ("bfs", "dfs", "pagerank", "communities")),
        ("agent_memory", "Long-Horizon Agent Memory Systems", "agentic", "expert",
         ("episodic", "semantic", "working_memory", "summarization")),
        ("jwt_auth", "JWT Authentication for Internal APIs", "security", "intermediate",
         ("jwt", "oauth", "rbac", "tokens")),
        ("async_python", "Async Python for High-Throughput Pipelines", "python", "advanced",
         ("asyncio", "aiohttp", "concurrency", "queues")),
        ("java_spring", "Spring Boot Service Patterns", "java", "intermediate",
         ("spring", "dependency_injection", "rest", "testing")),
        ("js_promises", "JavaScript Async Patterns", "javascript", "intermediate",
         ("promises", "async_await", "event_loop", "fetch")),
        ("ts_generics", "Advanced TypeScript Generics", "typescript", "advanced",
         ("generics", "utility_types", "inference", "constraints")),
        ("csharp_linq", "C# LINQ and EF Core", "csharp", "intermediate",
         ("linq", "ef_core", "async", "migrations")),
        ("cpp_memory", "C++ RAII and Smart Pointers", "cpp", "advanced",
         ("raii", "unique_ptr", "shared_ptr", "move_semantics")),
        ("go_concurrency", "Go Concurrency Patterns", "go", "intermediate",
         ("goroutines", "channels", "select", "worker_pools")),
        ("rust_ownership", "Rust Ownership in Systems Programming", "rust", "advanced",
         ("ownership", "borrowing", "lifetimes", "safety")),
        ("sql_optimization", "SQL Query Optimization", "sql", "advanced",
         ("indexes", "explain", "joins", "partitioning")),
        ("postgres_indexing", "PostgreSQL Index Strategies", "postgresql", "advanced",
         ("btree", "gin", "partial_index", "vacuum")),
        ("mongodb_aggregation", "MongoDB Aggregation Pipelines", "mongodb", "intermediate",
         ("aggregation", "sharding", "indexes", "schema_design")),
        ("redis_caching", "Redis Caching Patterns", "redis", "intermediate",
         ("cache_aside", "ttl", "pub_sub", "lua")),
        ("docker_compose", "Docker Compose for Local Dev", "docker", "beginner",
         ("compose", "volumes", "networks", "healthchecks")),
        ("k8s_hpa", "Kubernetes HPA for Inference Services", "kubernetes", "intermediate",
         ("hpa", "autoscaling", "gpu", "serving")),
        ("github_actions_ci", "GitHub Actions CI Pipelines", "github_actions", "intermediate",
         ("workflows", "matrix", "caching", "secrets")),
        ("gitlab_ci_cd", "GitLab CI/CD Pipelines", "gitlab_ci", "intermediate",
         ("stages", "runners", "artifacts", "environments")),
        ("aws_lambda", "AWS Lambda Serverless Patterns", "aws", "intermediate",
         ("lambda", "api_gateway", "iam", "cold_start")),
        ("azure_functions", "Azure Functions Architecture", "azure", "intermediate",
         ("functions", "app_service", "monitoring", "scaling")),
        ("gcp_cloud_run", "Google Cloud Run Services", "gcp", "intermediate",
         ("cloud_run", "gke", "iam", "autoscaling")),
        ("linux_systemd", "Linux systemd Service Management", "linux", "intermediate",
         ("systemd", "journalctl", "permissions", "security")),
        ("nginx_reverse_proxy", "Nginx Reverse Proxy Configuration", "nginx", "intermediate",
         ("proxy_pass", "ssl", "rate_limiting", "caching")),
        ("terraform_modules", "Terraform Module Design", "terraform", "advanced",
         ("modules", "state", "workspaces", "drift")),
        ("microservices_saga", "Microservices Saga Pattern", "microservices", "expert",
         ("saga", "compensation", "orchestration", "choreography")),
        ("event_driven_kafka", "Event-Driven Architecture with Kafka", "event_driven", "advanced",
         ("kafka", "events", "idempotency", "ordering")),
        ("cqrs_read_models", "CQRS Read Model Projections", "cqrs", "expert",
         ("cqrs", "projections", "event_sourcing", "consistency")),
        ("ddd_bounded_contexts", "Domain-Driven Design Bounded Contexts", "domain_driven_design", "expert",
         ("bounded_context", "ubiquitous_language", "aggregates", "context_map")),
        ("clean_arch_layers", "Clean Architecture Layers", "clean_architecture", "advanced",
         ("entities", "use_cases", "adapters", "dependency_rule")),
        ("git_branching", "Git Branching Strategies", "git", "intermediate",
         ("gitflow", "trunk", "rebase", "merge")),
        ("github_pr_workflow", "GitHub Pull Request Workflow", "github", "intermediate",
         ("pull_request", "reviews", "checks", "merge_queue")),
        ("npm_packages", "npm Package Management", "package_managers", "beginner",
         ("npm", "semver", "lockfile", "workspaces")),
        ("bash_scripting", "Bash Scripting Best Practices", "bash", "intermediate",
         ("set_euo", "functions", "trap", "logging")),
        ("powershell_automation", "PowerShell Automation Scripts", "powershell", "intermediate",
         ("cmdlets", "modules", "remoting", "error_handling")),
        ("rag_eval", "RAG Evaluation Frameworks", "rag", "advanced",
         ("faithfulness", "relevance", "ragas", "benchmarks")),
        ("postmortem", "Blameless Postmortem Writing", "incidents", "intermediate",
         ("timeline", "root_cause", "action_items", "lessons")),
        ("pr_review", "High-Quality Pull Request Reviews", "code_review", "intermediate",
         ("feedback", "nits", "architecture", "tests")),
        ("lora_sft", "LoRA Supervised Fine-Tuning", "fine_tuning", "advanced",
         ("lora", "qlora", "peft", "sft")),
        ("hybrid_reranking", "Cross-Encoder Reranking for RAG", "rag", "advanced",
         ("cross_encoder", "reranking", "bi_encoder", "fusion")),
        ("context_window", "Context Window Budget Management", "rag", "intermediate",
         ("token_budget", "truncation", "priority", "compression")),
        ("multimodal_rag", "Multimodal RAG for Diagrams and Code", "rag", "expert",
         ("vision", "diagrams", "screenshots", "multimodal")),
        ("otel_observability", "OpenTelemetry for RAG Pipelines", "observability", "intermediate",
         ("opentelemetry", "traces", "metrics", "spans")),
        ("prometheus_alerts", "Prometheus Alerting for Retrieval SLOs", "observability", "intermediate",
         ("prometheus", "alertmanager", "slo", "burn_rate")),
        ("grafana_dashboards", "Grafana Dashboards for RAG Metrics", "observability", "beginner",
         ("grafana", "dashboards", "latency", "recall")),
        ("vault_secrets", "HashiCorp Vault for API Keys", "security", "advanced",
         ("vault", "secrets", "rotation", "policies")),
        ("mtls_internal", "mTLS for Internal Service Mesh", "security", "advanced",
         ("mtls", "istio", "certificates", "mesh")),
        ("canary_deploy", "Canary Deployment Strategies", "ci_cd", "intermediate",
         ("canary", "rollout", "traffic_split", "rollback")),
        ("feature_flags", "Feature Flag Rollout Patterns", "ci_cd", "intermediate",
         ("feature_flags", "launchdarkly", "rollout", "kill_switch")),
        ("elasticsearch_hybrid", "Elasticsearch Hybrid Search", "vector_search", "advanced",
         ("elasticsearch", "bm25", "knn", "hybrid")),
        ("pinecone_indexing", "Pinecone Vector Index Management", "vector_stores", "intermediate",
         ("pinecone", "namespaces", "metadata", "upsert")),
        ("chromadb_persistence", "ChromaDB Persistent Collections", "vector_stores", "intermediate",
         ("chromadb", "collections", "persistence", "embedding")),
        ("weaviate_schema", "Weaviate Schema Design", "vector_stores", "advanced",
         ("weaviate", "schema", "multi_tenancy", "hybrid")),
        ("langchain_retrieval", "LangChain Retrieval Chain Patterns", "agentic", "intermediate",
         ("langchain", "retriever", "chain", "callbacks")),
        ("crewai_agents", "Multi-Agent Orchestration with CrewAI", "agentic", "expert",
         ("crewai", "agents", "tasks", "delegation")),
        ("react_pattern", "ReAct Agent Pattern for Tool Use", "agentic", "advanced",
         ("react", "reasoning", "acting", "tools")),
        ("ast_parsing", "AST Parsing with Tree-sitter", "graphrag", "advanced",
         ("tree_sitter", "ast", "parsing", "symbols")),
        ("pagerank_deps", "PageRank for Code Dependency Ranking", "graphrag", "expert",
         ("pagerank", "dependencies", "ranking", "impact")),
        ("load_testing", "Load Testing RAG Inference Endpoints", "performance", "intermediate",
         ("k6", "locust", "throughput", "latency")),
        ("cost_optimization", "Cost Optimization for Embedding Pipelines", "performance", "intermediate",
         ("batching", "caching", "gpu", "cost")),
        ("data_lineage", "Data Lineage for RAG Corpora", "data_quality", "advanced",
         ("lineage", "provenance", "audit", "versioning")),
        ("pii_detection", "PII Detection in Code Repositories", "security", "advanced",
         ("pii", "redaction", "scanning", "compliance")),
        ("contract_testing", "API Contract Testing with Pact", "testing", "intermediate",
         ("pact", "contracts", "consumer", "provider")),
    ]

    for slug, title, category, difficulty, keywords in seeds:
        topics.append(Topic(slug, title, category, difficulty, keywords))

    topics.extend(_hub_topics())

    category_phrases = PREMIUM_CATEGORY_PHRASES

    aspects = [
        "fundamentals", "patterns", "pitfalls", "scaling", "monitoring",
        "security", "testing", "migration", "integration", "optimization",
        "troubleshooting", "benchmarks", "cost_analysis", "team_workflows",
        "enterprise_rollout", "edge_cases", "versioning", "compliance",
        "disaster_recovery", "multi_tenant",
    ]

    for category, phrase in category_phrases.items():
        for i, aspect in enumerate(aspects):
            slug = f"{category}_{aspect}"
            title = f"{phrase}: {aspect.replace('_', ' ').title()}"
            difficulty = ["beginner", "intermediate", "advanced", "expert"][i % 4]
            keywords = (category, aspect, phrase.lower().split()[0])
            topics.append(Topic(slug, title, category, difficulty, keywords))

    return topics


TOPICS: list[Topic] = _topics()
