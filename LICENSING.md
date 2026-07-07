# Coltex Licensing

Copyright © 2026 Elijah Maxwell / Coltex. All rights reserved.

Use of the Coltex Enterprise RAG Vector Dataset is governed by a commercial license agreement. Select the tier that matches your deployment scope and intended use.

---

## License tiers

| Tier | Price | License | Best for |
|------|-------|---------|----------|
| **Personal** | **$79 USD** (one-time) | [PERSONAL-LICENSE.md](PERSONAL-LICENSE.md) | Students, hobbyists, researchers — non-commercial |
| **Professional** | **$399 USD** (one-time) | [PROFESSIONAL-LICENSE.md](PROFESSIONAL-LICENSE.md) | Freelancers, startups, commercial developers — one entity |
| **Enterprise** | **Custom quote** | [ENTERPRISE-LICENSE.md](ENTERPRISE-LICENSE.md) | Organization-wide deployment, multiple teams, on-prem / private cloud |
| **Dataset EULA** | Per agreement | [EULA.md](EULA.md) | Supplemental terms for enterprise RAG vector dataset packages |

---

## Personal License — $79 USD

**Intended users:** Students, hobbyists, researchers, and individuals using Coltex for non-commercial purposes.

**You may:** Install on personal devices, learn and experiment, create private AI projects, modify for personal use, receive updates (if offered).

**You may not:** Commercial use, sell services, offer SaaS/hosted Coltex, redistribute or resell, share license keys, remove copyright notices.

Full terms: [PERSONAL-LICENSE.md](PERSONAL-LICENSE.md)

---

## Professional License — $399 USD

**Intended users:** Freelancers, consultants, startups, software companies, and commercial developers.

**Includes everything in the Personal License, plus:**

- Use Coltex in commercial products
- Build AI applications and generate revenue
- Deploy Coltex within your business
- Fine-tune AI models using Coltex-processed data (where applicable)
- Integrate Coltex into customer-facing software

**Restrictions:** No reselling original Coltex software, no competing hosted service without permission, no selling copies, no sharing across organizations, no removing notices.

**Scope:** One company or one legal entity (additional seats available). Priority email support may be included if offered.

Full terms: [PROFESSIONAL-LICENSE.md](PROFESSIONAL-LICENSE.md) · Summary: [knowledge-base/PROFESSIONAL-LICENSE.md](knowledge-base/PROFESSIONAL-LICENSE.md)

---

## Enterprise License — Custom Quote

**Intended users:** Medium and large businesses, government organizations, educational institutions, and enterprises.

**Includes everything in the Professional License, plus:**

### Enterprise rights

- Organization-wide deployment
- Multiple users and teams
- Private cloud deployment
- Customer-owned cloud deployment (AWS, Azure, GCP, VPS, Kubernetes, etc.)
- On-premises deployment
- Internal production use across multiple departments

### Enterprise services (per agreement)

- Deployment assistance
- Administrator onboarding
- Technical training sessions
- Architecture consultation
- Priority support
- Custom licensing agreements
- Volume licensing
- Optional support and maintenance agreements
- Optional custom integrations and professional services

### Restrictions

The Enterprise License does not permit redistribution, resale, sublicensing, or public distribution of the Coltex software unless explicitly authorized in writing.

Each Enterprise agreement may include custom terms based on deployment size, support requirements, and organizational needs.

Enterprise customers receive a dedicated commercial license agreement that supersedes standard license terms where applicable.

Full terms: [ENTERPRISE-LICENSE.md](ENTERPRISE-LICENSE.md) · Summary: [knowledge-base/ENTERPRISE-LICENSE.md](knowledge-base/ENTERPRISE-LICENSE.md)

---

## Dataset EULA (Enterprise packages)

Enterprise RAG vector dataset packages are governed by the **Coltex End User License Agreement (EULA)** in addition to the Enterprise License. The EULA covers dataset content, vector chunks, embeddings, graph edges, metadata, benchmarks, and product artifacts.

| Document | Purpose |
|----------|---------|
| [EULA.md](EULA.md) | Full End User License Agreement for dataset delivery |
| [knowledge-base/EULA.md](knowledge-base/EULA.md) | Dataset scope summary |
| [PROVENANCE.md](knowledge-base/PROVENANCE.md) | Content origin and compliance |
| [NOTICE](NOTICE) | Third-party open-source dependencies (engine tooling only) |

See [EULA.md](EULA.md) for complete terms. Package comparison: [docs/commercial/sku-matrix.md](docs/commercial/sku-matrix.md).

---

## Build commands by tier

```bash
# Personal ($79 — non-commercial)
make product-personal

# Professional ($399 — commercial, one entity)
make product-professional

# Enterprise (organization-wide + dataset packages)
make product-enterprise
make product-premium-smoke

# Compliance audit
make audit-distribution
```

---

## Disclaimer

This document summarizes the licensing approach. It is not legal advice. Consult qualified counsel before commercial use.

For enterprise agreements, custom quotes, volume licensing, or tier upgrades: contact the repository maintainer.
