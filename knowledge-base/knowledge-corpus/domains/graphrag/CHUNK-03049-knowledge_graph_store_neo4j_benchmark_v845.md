---
id: CHUNK-03049-KNOWLEDGE-GRAPH-STORE-NEO4J-BENCHMARK-V845
title: "Chunk 03049 Knowledge Graph Store: Neo4j \u2014 Benchmark (v845)"
category: CHUNK-03049-knowledge_graph_store_neo4j_benchmark_v845.md
tags:
- knowledge_graph_store
- neo4j
- graphrag
- benchmark
- graphrag
- variant_845
difficulty: intermediate
related:
- CHUNK-03048
- CHUNK-03047
- CHUNK-03046
last_updated: '2026-07-07'
version: '2.0'
---

---
id: CHUNK-03049
title: "Knowledge Graph Store: Neo4j \u2014 Benchmark (v845)"
category: graphrag
doc_type: benchmark
tags:
- knowledge_graph_store
- neo4j
- graphrag
- benchmark
- graphrag
- variant_845
difficulty: intermediate
related: []
last_updated: '2026-07-07'
version: '2.0'
hub: knowledge_graph_store
---

# Knowledge Graph Store: Neo4j — Benchmark (v845)

## Suite

During incident response, **Suite** for `Knowledge Graph Store: Neo4j` (benchmark). This variant 845 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Methodology

During incident response, **Methodology** for `Knowledge Graph Store: Neo4j` (benchmark). This variant 845 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Dataset

During incident response, **Dataset** for `Knowledge Graph Store: Neo4j` (benchmark). This variant 845 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Metrics

**Metrics** — Knowledge Graph Store: Neo4j benchmark variant 845.

| Metric | Value |
|--------|-------|
| recall@10 | 0.82 |
| p95 latency (ms) | 12795 |
| error rate | 0.8460 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Results

**Results** — Knowledge Graph Store: Neo4j benchmark variant 845.

| Metric | Value |
|--------|-------|
| recall@10 | 0.82 |
| p95 latency (ms) | 12795 |
| error rate | 0.8460 |

**Good answer:** Grounded in measured results with trade-offs.
**Bad answer:** Claims without metrics or missing failure modes.
**Preferred answer:** Cites numbers, context, and next optimization steps.
## Comparison

During incident response, **Comparison** for `Knowledge Graph Store: Neo4j` (benchmark). This variant 845 covers knowledge_graph_store, neo4j, graphrag at intermediate level. Key considerations include reliability, observability, latency budgets, and safe rollout. Teams should validate assumptions with benchmarks, add tracing spans, and document failure modes. Recommended metrics: p95 latency, error rate, recall@k (if retrieval), and freshness of indexed data.
## Reference Implementation

```python
from typing import Any

class KnowledgeGraphStoreNeo4j:
    """Knowledge Graph Store: Neo4j"""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "topic": "knowledge_graph_store_neo4j", "variant": 845}
```
