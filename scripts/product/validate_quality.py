#!/usr/bin/env python3
"""Validate product quality gates from config/product.yaml."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import ROOT, iter_jsonl, load_knowledge_base, load_product_config, resolve_path


def validate_chunks(cfg: dict, chunks_path: Path) -> dict:
    min_chars = int(cfg["quality"]["min_chunk_chars"])
    required_fields = cfg["quality"]["require_metadata_fields"]
    issues: list[str] = []
    total = 0
    short = 0
    missing_meta = 0

    if not chunks_path.exists():
        return {"passed": False, "issues": [f"Missing chunks file: {chunks_path}"]}

    for chunk in iter_jsonl(chunks_path):
        total += 1
        if chunk.get("char_count", 0) < min_chars:
            short += 1
        for field in required_fields:
            if not chunk.get(field):
                missing_meta += 1
                break

    if short:
        issues.append(f"{short}/{total} chunks below min_chunk_chars ({min_chars})")
    if missing_meta:
        issues.append(f"{missing_meta}/{total} chunks missing required metadata fields")

    return {
        "passed": not issues,
        "total_chunks": total,
        "short_chunks": short,
        "missing_metadata": missing_meta,
        "issues": issues,
    }


def validate_documents(cfg: dict, kb) -> dict:
    required_fields = ("id", "title")  # documents use id in frontmatter
    issues: list[str] = []
    missing = 0

    for doc in kb.documents:
        meta = {"id": doc.doc_id, "title": doc.title}
        if any(not meta.get(f) for f in required_fields):
            missing += 1

    if missing:
        issues.append(f"{missing}/{len(kb.documents)} documents missing required metadata")

    return {
        "passed": not issues,
        "total_documents": len(kb.documents),
        "missing_metadata": missing,
        "issues": issues,
    }


def validate_license_files(cfg: dict) -> dict:
    dist_cfg = cfg.get("distribution", {})
    issues: list[str] = []

    if dist_cfg.get("require_kb_license", True):
        if not (ROOT / "knowledge-base" / "LICENSE").exists():
            issues.append("Missing knowledge-base/LICENSE")
    if dist_cfg.get("require_provenance", True):
        if not (ROOT / "knowledge-base" / "PROVENANCE").exists() and not (ROOT / "knowledge-base" / "PROVENANCE.md").exists():
            issues.append("Missing knowledge-base/PROVENANCE.md")
    if dist_cfg.get("require_notice", True):
        if not (ROOT / "NOTICE").exists():
            issues.append("Missing root NOTICE file")

    return {"passed": not issues, "issues": issues}


def validate_distribution(cfg: dict, kb) -> dict:
    from common import distribution_cfg, is_substantive_document

    dist_cfg = distribution_cfg(cfg)
    issues: list[str] = []

    for doc in kb.documents:
        ok, reason = is_substantive_document(doc, dist_cfg)
        if not ok:
            issues.append(f"{doc.doc_id}: {reason}")

    max_rejection_ratio = float(dist_cfg.get("max_rejection_ratio", 0.0))
    rejection_ratio = len(issues) / len(kb.documents) if kb.documents else 0.0
    passed = not issues if max_rejection_ratio <= 0 else rejection_ratio <= max_rejection_ratio

    return {
        "passed": passed,
        "rejected_documents": len(issues),
        "rejection_ratio": round(rejection_ratio, 4),
        "max_rejection_ratio": max_rejection_ratio,
        "issues": issues[:15],
    }


def validate_duplicates(cfg: dict, chunks_path: Path) -> dict:
    max_ratio = float(cfg["quality"]["max_duplicate_ratio"])
    seen: set[str] = set()
    total = 0
    dupes = 0

    for chunk in iter_jsonl(chunks_path):
        total += 1
        h = chunk.get("content_hash", "")
        if h in seen:
            dupes += 1
        else:
            seen.add(h)

    ratio = dupes / total if total else 0.0
    issues = []
    if ratio > max_ratio:
        issues.append(f"Duplicate ratio {ratio:.2%} exceeds max {max_ratio:.2%}")

    return {
        "passed": ratio <= max_ratio,
        "duplicate_ratio": round(ratio, 4),
        "max_allowed": max_ratio,
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate product quality gates")
    parser.add_argument("--config", type=Path, default=Path("config/product.yaml"))
    args = parser.parse_args()

    cfg = load_product_config(args.config)
    kb = load_knowledge_base(cfg)
    chunks_path = resolve_path(cfg["output"]["chunks"])
    streaming = cfg.get("quality", {}).get("streaming_mode", False)

    results = {
        "license_files": validate_license_files(cfg),
        "documents": validate_documents(cfg, kb),
        "chunks": validate_chunks(cfg, chunks_path),
        "duplicates": validate_duplicates(cfg, chunks_path) if chunks_path.exists() else {"passed": True},
    }
    if not streaming:
        results["distribution"] = validate_distribution(cfg, kb)
    else:
        results["distribution"] = {"passed": True, "streaming_mode": True, "note": "Validated during stream generation"}
    results["passed"] = all(r.get("passed", False) for r in results.values())

    print(json.dumps(results, indent=2))
    if not results["passed"]:
        raise SystemExit("Quality validation failed")


if __name__ == "__main__":
    main()
