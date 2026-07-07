# Coltex SKU Matrix

Commercial tiers for the Coltex Enterprise RAG Vector Dataset.

---

## Tier comparison

| | **Enterprise Curated** | **Premium Standard** | **Premium Hyper** |
|---|------------------------|----------------------|-------------------|
| **SKU** | `coltex-enterprise-v3` | `coltex-premium-v2.1` | `coltex-premium-hyper-v2.1` |
| **Price guidance** | Contact | $1,000+ | $1,000+ (volume) |
| **Documents** | 12,993 curated CHUNK docs | 25,000 streamed | Uncapped (100B× procedural) |
| **Domains** | 63 full domains | 27 categories | 27+ categories |
| **Graph architecture** | Full (hubs, links, routes) | Streamed graph edges | Streamed graph edges |
| **Embeddings** | Optional (included in build) | Pre-computed (500k cap local) | Cluster-scale export |
| **Benchmarks** | 200+ pairs | 500+ pairs | 500+ pairs |
| **Audit report** | ✅ | ✅ | ✅ |
| **Build command** | `make product-enterprise` | `make product-premium-smoke` | `make product-hyper` |
| **Best for** | Production RAG pilots | Buyer validation / demos | Maximum scale deployment |

---

## What's in every tier

- Apache-2.0 license with full provenance documentation
- `manifest.json` with SHA-256 checksums
- `distribution_audit.json` compliance report
- Typed metadata on every document
- Quality gate validation (dedup, substance, license checks)
- Benchmark datasets for due diligence

---

## Enterprise Curated — recommended starting point

The **Enterprise Curated** tier combines the full knowledge-corpus architecture (63 domains, 18 hubs, graph links, domain routes, processing layers) with the standard product pipeline. This is the most polished, graph-rich deliverable.

```bash
make corpus-mega              # Expand to 10,000+ domain documents
make product-enterprise       # Chunk → embed → benchmark → manifest → audit
```

**Deliverables:** `data/product/` + `benchmarks/` + compliance files

---

## Premium Standard — validation & demos

25,000 procedurally streamed documents with audit samples on disk. Ideal for smoke-testing buyer pipelines before a hyper-scale run.

```bash
make product-premium-smoke
make audit-distribution
```

**Sample files:** `knowledge-base/distributable/_samples/` (1,000 audit markdown files)

---

## Premium Hyper — maximum scale

100-billion× procedural multiplier. Intended for cluster deployment (Vast.ai, cloud GPU). Uncapped document generation.

```bash
make product-hyper            # Requires cluster resources
```

Estimated procedural capacity: 600+ trillion unique document combinations.

---

## Add-ons (available on request)

| Add-on | Description |
|--------|-------------|
| Custom domain pack | Additional technology verticals |
| Re-embedding | Alternative embedding models (e.g. bge-small) |
| Evaluation report | Full recall@k report on buyer queries |
| White-label manifest | Buyer-branded `manifest.json` |

---

## Support & delivery

| Delivery method | Format |
|-----------------|--------|
| Git release tarball | `.tar.gz` with `data/product/` |
| Cloud storage | S3 / GCS signed URL |
| Hugging Face Dataset | Parquet or JSONL |

Contact: see repository maintainer for licensing and delivery options.
