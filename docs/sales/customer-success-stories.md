# Coltex Customer Success Stories

*Synthetic case studies for sales collateral. Adapt names and metrics for your prospects.*

---

## Case Study 1: NovaTech AI Consultancy

**Industry:** AI consulting · **Size:** 45 engineers · **Tier:** Professional + Premium Dataset

### Challenge
NovaTech needed to deliver RAG-powered internal search for three enterprise clients within 6 weeks. Each client required isolated knowledge bases, citation-backed answers, and compliance documentation for procurement.

### Solution
- Deployed Coltex Platform on Kubernetes (2 replicas, HPA)
- Imported Premium Dataset (25K docs) as starter corpus per client
- Custom collections per client workspace with API key isolation
- Integrated RAG chat into client portals via `/v1/chat/completions`

### Results
| Metric | Before | After |
|--------|--------|-------|
| Time to first production RAG | 8–12 weeks | **5 days** |
| Retrieval recall@8 | ~40% (vector-only POC) | **69%** (Coltex hybrid) |
| Revenue per engagement | $40K | **$85K** (platform + dataset upsell) |
| Client NPS | — | **72** |

> *"Coltex let us sell RAG as a product, not a science project."* — VP Engineering, NovaTech

---

## Case Study 2: FinServe Compliance Platform

**Industry:** FinTech · **Size:** 200 employees · **Tier:** Enterprise

### Challenge
FinServe's support team searched across 12,000 runbooks, ADRs, and incident reports. Existing keyword search missed semantic matches; an earlier RAG POC hallucinated without citations.

### Solution
- Coltex Enterprise VPC deployment with SSO
- Ingested 12,000 internal markdown docs via batch upload API
- GraphRAG linked incident reports → runbooks → ADRs
- Enabled OpenAI provider with strict context-only system prompt

### Results
| Metric | Before | After |
|--------|--------|-------|
| Mean time to resolve (L2) | 4.2 hours | **1.8 hours** |
| Escalations to L3 | 34/week | **11/week** |
| Citation accuracy (audit sample) | N/A | **94%** |
| Annual support cost savings | — | **$420K** |

---

## Case Study 3: DataMart Reseller

**Industry:** Data marketplace · **Size:** 12 employees · **Tier:** Reseller + Premium Dataset SKUs

### Challenge
DataMart sold generic "AI training data" bundles without differentiation. Buyers wanted RAG-ready packages with provenance and evaluation evidence.

### Solution
- White-labeled Coltex Premium Dataset as "DataMart RAG Pro Bundle"
- Included manifest.json, benchmarks, and distribution audit in every sale
- 40% reseller margin on $1,000 smoke tier

### Results
| Metric | Q1 | Q2 (with Coltex) |
|--------|-----|------------------|
| RAG bundle sales | 0 | **47 units** |
| Average deal size | $200 | **$1,400** |
| Refund rate | 8% | **<1%** (audit-backed quality) |
| Reseller revenue | — | **$65K** |

---

## Case Study 4: DevTools SaaS — Embedded RAG

**Industry:** Developer tools · **Size:** 80 employees · **Tier:** Professional

### Challenge
A documentation SaaS vendor wanted in-app "Ask AI" without building retrieval infrastructure from scratch.

### Solution
- Embedded Coltex Brain via Python SDK for low-latency retrieve
- Platform API for customer-managed collections (multi-tenant by workspace)
- Starter tier limits aligned with SaaS pricing tiers

### Results
- **Ask AI** feature shipped in **3 sprints** (vs 9 estimated)
- **23% increase** in Pro plan upgrades
- **<200ms p95** retrieve latency on Professional tier

---

## Metrics Summary (Across Customers)

| KPI | Typical Improvement |
|-----|---------------------|
| Time to production RAG | 70–85% reduction |
| Retrieval recall@8 | +20–30 points vs vector-only |
| Support ticket deflection | 25–40% |
| Deal size (with dataset SKU) | 2–4× |

## Use These in Proposals

Copy relevant case study into SOWs and pitch decks. Full technical evidence: `benchmarks/evaluation_report.json`, `docs/sales/feature-matrix.md`.
