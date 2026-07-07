#!/usr/bin/env python3
"""Build product manifest with checksums and metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from common import iter_jsonl, load_knowledge_base, load_product_config, resolve_path


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in iter_jsonl(path))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build product manifest")
    parser.add_argument("--config", type=Path, default=Path("config/product.yaml"))
    args = parser.parse_args()

    cfg = load_product_config(args.config)
    kb = load_knowledge_base(cfg)
    out_cfg = cfg["output"]
    gen_stats_path_str = out_cfg.get("generation_stats", "")
    gen_stats_path = resolve_path(gen_stats_path_str) if gen_stats_path_str else None
    streaming = cfg.get("quality", {}).get("streaming_mode", False)

    gen_stats: dict = {}
    if gen_stats_path and gen_stats_path.is_file():
        gen_stats = json.loads(gen_stats_path.read_text(encoding="utf-8"))

    catalog_path = resolve_path(out_cfg.get("catalog", "data/product/catalog.jsonl"))

    artifacts = {
        "chunks": resolve_path(out_cfg["chunks"]),
        "graph": resolve_path(out_cfg["graph"]),
        "metadata": resolve_path(out_cfg["metadata"]),
        "catalog": catalog_path,
        "embeddings": resolve_path(cfg["embeddings"]["output_dir"]) / "embeddings.jsonl",
    }

    files: dict[str, dict] = {}
    for name, path in artifacts.items():
        if path.exists():
            files[name] = {
                "path": str(path.relative_to(resolve_path("."))),
                "sha256": file_sha256(path),
                "records": count_jsonl(path) if path.suffix == ".jsonl" else None,
                "bytes": path.stat().st_size,
            }

    meta_path = resolve_path(out_cfg["metadata"])
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    documents = []
    if streaming and catalog_path.exists():
        for i, rec in enumerate(iter_jsonl(catalog_path)):
            if i >= 10_000:
                break
            documents.append({
                "doc_id": rec.get("doc_id"),
                "title": rec.get("title"),
                "category": rec.get("category"),
                "doc_type": rec.get("doc_type"),
                "tags": rec.get("tags", []),
                "hub": rec.get("hub", ""),
                "source_path": rec.get("path"),
                "license": cfg.get("license", "Coltex-EULA"),
            })
    else:
        for doc in kb.documents:
            documents.append({
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "doc_type": doc.doc_type,
                "tags": doc.tags,
                "hub": doc.hub,
                "related_count": len(doc.related),
                "relationship_types": list(doc.relationships.keys()),
                "source_path": doc.path,
                "license": cfg.get("license", "Coltex-EULA"),
            })

    catalog_count = count_jsonl(catalog_path) if catalog_path.exists() else len(kb.documents)
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump({
            "documents": documents,
            "count": catalog_count,
            "metadata_sample_size": len(documents),
        }, f, indent=2)

    files["metadata"] = {
        "path": str(meta_path.relative_to(resolve_path("."))),
        "sha256": file_sha256(meta_path),
        "records": catalog_count,
        "bytes": meta_path.stat().st_size,
    }

    manifest = {
        "name": cfg.get("name", "Coltex Product"),
        "version": str(cfg.get("version", "1.0.0")),
        "tier": cfg.get("tier", "standard"),
        "price_usd": cfg.get("price_usd"),
        "license": cfg.get("license", "Coltex-EULA"),
        "updated": str(cfg.get("updated", datetime.now(timezone.utc).strftime("%Y-%m-%d"))),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "curated_only": cfg["quality"].get("curated_only", True),
        "streaming_mode": streaming,
        "content_origin": gen_stats.get("content_origin", "original_synthetic"),
        "third_party_docs_copied": gen_stats.get("third_party_docs_copied", False),
        "mega_multiplier": gen_stats.get("mega_multiplier"),
        "estimated_total_documents": gen_stats.get("estimated_total_documents"),
        "documents_generated": gen_stats.get("documents_generated", catalog_count),
        "chunks_generated": gen_stats.get("chunks_generated", files.get("chunks", {}).get("records")),
        "excluded_paths": [
            "knowledge-base/_excluded_from_distribution/",
            "knowledge-base/generated/",
            "knowledge-base/_seed/",
        ],
        "documents": catalog_count,
        "artifacts": files,
        "benchmarks_dir": cfg["benchmarks"]["output_dir"],
        "generation_stats": gen_stats,
    }

    manifest_path = resolve_path(out_cfg["manifest"])
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
