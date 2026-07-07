# Coltex End User License Agreement (EULA)

**Effective date:** July 7, 2026  
**Version:** 1.0  
**Licensor:** Elijah Maxwell / Coltex ("Licensor", "we", "us")

---

## 1. Agreement

This End User License Agreement ("Agreement") is a legal contract between you ("Licensee", "you") and the Licensor governing your access to and use of the Coltex Enterprise RAG Vector Dataset, including all associated knowledge base content, vector chunks, embeddings, graph edges, metadata, benchmark datasets, manifests, and documentation (collectively, the "Dataset").

By downloading, accessing, installing, copying, or using the Dataset under an **enterprise agreement**, you agree to be bound by this Agreement in conjunction with the [Coltex Enterprise License](ENTERPRISE-LICENSE.md). For other tiers, see the [Personal License](PERSONAL-LICENSE.md) ($79) or [Professional License](PROFESSIONAL-LICENSE.md) ($399).

---

## 2. Definitions

- **"Authorized Users"** — Your employees, contractors, and agents who access the Dataset solely on your behalf and under your control.
- **"Derivative Work"** — Any modification, adaptation, translation, fine-tuned model, index, or product that incorporates or is substantially based on the Dataset.
- **"Permitted Use"** — Use of the Dataset as described in Section 3.
- **"Product Artifacts"** — Files produced by the Coltex build pipeline, including `chunks.jsonl`, `embeddings.jsonl`, `edges.jsonl`, `catalog.jsonl`, `manifest.json`, and benchmark files.

---

## 3. License Grant

Subject to your compliance with this Agreement and payment of applicable fees (if any), Licensor grants you a **limited, non-exclusive, non-transferable, non-sublicensable, revocable** license to:

(a) Use the Dataset and Product Artifacts internally for research, development, testing, and production of retrieval-augmented generation (RAG) systems, AI agents, and related applications;

(b) Load Dataset content into vector databases, search indexes, and RAG pipelines operated by you or on your behalf;

(c) Create Derivative Works for internal use and for products or services you offer to end customers, provided such offerings do not redistribute the Dataset itself in raw or substantially unmodified form;

(d) Make a reasonable number of backup copies for disaster recovery purposes.

This license does **not** transfer ownership of the Dataset to you.

---

## 4. Restrictions

You may **not**, without prior written consent from Licensor:

(a) Sell, resell, license, sublicense, distribute, publish, or otherwise make the Dataset or Product Artifacts available to third parties as a standalone dataset, data product, or competing corpus;

(b) Share, upload, or publish the Dataset (or substantial portions) to public repositories, model hubs, torrents, or file-sharing platforms;

(c) Remove, alter, or obscure copyright notices, provenance metadata, license headers, or manifest checksums;

(d) Use the Dataset to train or fine-tune models for the primary purpose of redistributing the Dataset content itself;

(e) Represent the Dataset as your own original work without attribution to Coltex;

(f) Use the Dataset in violation of applicable law, including to generate unlawful, harmful, or infringing content;

(g) Exceed the document volume, tier, or scope specified in your purchase order or SKU (e.g., Enterprise, Premium Smoke, Premium Hyper).

---

## 5. Ownership

The Dataset, including all content, structure, metadata schemas, graph topology, and compilation, is and remains the exclusive property of Licensor. All rights not expressly granted are reserved.

Trademarks, service marks, and product names including **"Coltex"** are the property of Licensor. This Agreement does not grant any trademark rights.

---

## 6. Fees and Payment

Access to commercial tiers of the Dataset may require payment of fees as specified at the time of purchase. Fees are non-refundable except where required by applicable law or expressly stated in your order.

Evaluation, smoke, or trial builds provided for validation purposes remain subject to this Agreement and may not be used in production without a commercial license.

---

## 7. Third-Party Components

The Coltex **engine tooling** (scripts, retrieval pipeline) may incorporate open-source software listed in the `NOTICE` file. Those components remain governed by their respective licenses.

Runtime dependencies (e.g., embedding models such as `all-MiniLM-L6-v2`) are subject to their own license terms on download. You are responsible for compliance with third-party licenses when using those components.

The Dataset **content** itself is proprietary and governed solely by this EULA, not by Apache-2.0 or other open-source licenses.

---

## 8. Provenance and Compliance

The Dataset consists of **original synthetic content** authored for Coltex. It was not copied from third-party documentation or scraped from the web. See `knowledge-base/PROVENANCE.md` for content origin details.

You agree to retain `PROVENANCE.md`, this EULA, and applicable manifest files with any Product Artifacts you deploy internally.

---

## 9. Term and Termination

This Agreement is effective upon your first access to the Dataset and continues until terminated.

Licensor may terminate this Agreement immediately if you breach any term. Upon termination, you must cease all use, destroy all copies of the Dataset in your possession, and certify destruction upon request.

Sections 5, 9–13 survive termination.

---

## 10. Disclaimer of Warranties

THE DATASET IS PROVIDED **"AS IS"** AND **"AS AVAILABLE"** WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, COMPLETENESS, NON-INFRINGEMENT, OR THAT THE DATASET WILL MEET YOUR REQUIREMENTS.

Licensor does not warrant that retrieval quality, benchmark scores, or metadata accuracy will meet any particular threshold in your production environment.

---

## 11. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, LICENSOR SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS, DATA, REVENUE, OR BUSINESS OPPORTUNITY, ARISING FROM OR RELATED TO THIS AGREEMENT OR THE DATASET, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

LICENSOR'S TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE AMOUNT YOU PAID FOR THE DATASET IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM, OR ONE HUNDRED U.S. DOLLARS (USD $100), WHICHEVER IS GREATER.

---

## 12. Indemnification

You agree to indemnify, defend, and hold harmless Licensor from any claims, damages, losses, or expenses (including reasonable attorneys' fees) arising from your use of the Dataset, your Derivative Works, or your violation of this Agreement.

---

## 13. Governing Law

This Agreement shall be governed by and construed in accordance with the laws of the jurisdiction in which Licensor is established, without regard to conflict-of-law principles. Disputes shall be resolved in the courts of that jurisdiction, unless otherwise required by mandatory local law.

---

## 14. General

- **Entire agreement.** This EULA, together with your purchase order and SKU documentation, constitutes the entire agreement regarding the Dataset.
- **Amendment.** Licensor may update this EULA for new versions of the Dataset. Continued use after notice constitutes acceptance.
- **Severability.** If any provision is unenforceable, the remainder remains in effect.
- **No waiver.** Failure to enforce any right is not a waiver of that right.

---

## 15. Contact

For licensing inquiries, enterprise agreements, or written consent requests:

**Coltex** — see repository maintainer contact or your purchase channel.

---

*This document is provided for product licensing purposes. It is not legal advice. Consult qualified counsel before commercial use.*
