---
id: CHUNK-08174-KNOWLEDGE-GRAPH-STORE-NEO4J-API-REFERENCE-V5970
title: "Chunk 08174 Knowledge Graph Store: Neo4j \u2014 Api Reference (v5970)"
category: CHUNK-08174-knowledge_graph_store_neo4j_api_reference_v5970.md
tags:
- knowledge_graph_store
- neo4j
- graphrag
- api_reference
- graphrag
- variant_5970
difficulty: intermediate
related:
- CHUNK-08173
- CHUNK-08172
- CHUNK-08171
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-08174
title: "Knowledge Graph Store: Neo4j \u2014 Api Reference (v5970)"
category: graphrag
doc_type: api_reference
tags:
- knowledge_graph_store
- neo4j
- graphrag
- api_reference
- graphrag
- variant_5970
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Neo4j — Api Reference (v5970)

## Endpoint

When scaling to enterprise workloads, **Endpoint** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 5970 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Authentication

When scaling to enterprise workloads, **Authentication** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 5970 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Request Schema

When scaling to enterprise workloads, **Request Schema** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 5970 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Response Schema

When scaling to enterprise workloads, **Response Schema** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 5970 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Error Codes

When scaling to enterprise workloads, **Error Codes** for `Knowledge Graph Store: Neo4j` (api_reference). This variant 5970 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```python
from typing import Any

class KnowledgeGraphStoreNeo4j:
    """Knowledge Graph Store: Neo4j"""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "topic": "knowledge_graph_store_neo4j", "variant": 5970}
```
