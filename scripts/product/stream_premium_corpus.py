#!/usr/bin/env python3
"""Stream premium distributable corpus — hyper-scale, compliance-safe, original synthetic."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import chunk_document, distribution_cfg, is_substantive_document, load_product_config, resolve_path
from premium_generator import (
    estimate_premium_documents,
    format_premium_markdown,
    iter_premium_documents,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mega_scale import resolve_mega_tier


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream premium distributable corpus")
    parser.add_argument("--config", type=Path, default=Path("config/product_hyper.yaml"))
    parser.add_argument("--max-files", type=int, default=None, help="Cap documents (0 = uncapped)")
    parser.add_argument("--sample-md", type=int, default=None, help="Write N sample .md files for audit")
    args = parser.parse_args()

    cfg = load_product_config(args.config)
    gen = cfg.get("generation", {})
    mega = int(gen.get("mega_multiplier", 100_000_000_000))
    scale = int(gen.get("scale", 10_000))
    variations = int(gen.get("variations_per_doc", 24))
    categories = gen.get("categories", [])
    max_docs = args.max_files if args.max_files is not None else int(gen.get("max_files", 0))
    sample_md = args.sample_md if args.sample_md is not None else int(gen.get("sample_md_files", 5000))
    dist_cfg = distribution_cfg(cfg)
    chunk_cfg = cfg["chunking"]
    license_name = cfg.get("license", "Coltex-EULA")

    out_cfg = cfg["output"]
    chunks_path = resolve_path(out_cfg["chunks"])
    catalog_path = resolve_path(out_cfg.get("catalog", "data/product/catalog.jsonl"))
    graph_path = resolve_path(out_cfg["graph"])
    stats_path = resolve_path(out_cfg.get("generation_stats", "data/product/generation_stats.json"))

    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.parent.mkdir(parents=True, exist_ok=True)

    sample_dir = resolve_path(gen.get("sample_dir", "knowledge-base/distributable/_samples"))
    if sample_md > 0:
        sample_dir.mkdir(parents=True, exist_ok=True)

    estimated_total = estimate_premium_documents(categories, mega, scale, variations)
    tier = resolve_mega_tier(mega)

    doc_count = 0
    chunk_count = 0
    edge_count = 0
    rejected = 0
    seen_hashes: set[str] = set()
    dupes = 0

    with chunks_path.open("w", encoding="utf-8") as cf, \
         catalog_path.open("w", encoding="utf-8") as catf, \
         graph_path.open("w", encoding="utf-8") as gf:

        for doc, meta in iter_premium_documents(
            categories, mega, scale, variations, max_documents=max_docs,
        ):
            ok, reason = is_substantive_document(doc, dist_cfg)
            if not ok:
                rejected += 1
                continue

            chunks = chunk_document(
                doc,
                max_chars=int(chunk_cfg["max_chunk_chars"]),
                overlap=int(chunk_cfg["overlap_chars"]),
                split_on=str(chunk_cfg.get("split_on", "## ")),
                license_name=license_name,
            )
            for chunk in chunks:
                h = chunk.get("content_hash", "")
                if h in seen_hashes:
                    dupes += 1
                    continue
                seen_hashes.add(h)
                cf.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                chunk_count += 1

            catalog_entry = {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "doc_type": doc.doc_type,
                "hub": doc.hub,
                "tags": doc.tags,
                "path": doc.path,
                "char_count": len(doc.content),
                "license": license_name,
                "origin": "coltex_premium_synthetic",
            }
            catf.write(json.dumps(catalog_entry, ensure_ascii=False) + "\n")

            for rel_id in doc.related:
                gf.write(json.dumps({
                    "source": doc.doc_id,
                    "target": rel_id,
                    "type": "see_also",
                    "source_path": doc.path,
                }, ensure_ascii=False) + "\n")
                edge_count += 1
            for rel_id in doc.relationships.get("depends_on", []):
                gf.write(json.dumps({
                    "source": doc.doc_id,
                    "target": rel_id,
                    "type": "depends_on",
                    "source_path": doc.path,
                }, ensure_ascii=False) + "\n")
                edge_count += 1

            if doc_count < sample_md:
                md_path = sample_dir / Path(doc.path).name
                md_path.write_text(format_premium_markdown(meta, doc.content), encoding="utf-8")

            doc_count += 1
            if doc_count % 10_000 == 0:
                print(f"  ... {doc_count:,} documents, {chunk_count:,} chunks", flush=True)

    dup_ratio = dupes / chunk_count if chunk_count else 0.0
    stats = {
        "tier": tier.name,
        "mega_multiplier": mega,
        "estimated_total_documents": estimated_total,
        "documents_generated": doc_count,
        "chunks_generated": chunk_count,
        "graph_edges": edge_count,
        "rejected_substance": rejected,
        "duplicate_chunks_skipped": dupes,
        "duplicate_ratio": round(dup_ratio, 6),
        "sample_md_files": min(doc_count, sample_md),
        "price_tier_usd": cfg.get("price_usd", 1000),
        "content_origin": "coltex_premium_synthetic",
        "third_party_docs_copied": False,
    }
    with stats_path.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
