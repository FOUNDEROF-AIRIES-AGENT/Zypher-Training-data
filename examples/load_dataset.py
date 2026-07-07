#!/usr/bin/env python3
"""Load Coltex commercial RAG vector dataset artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterator


def load_jsonl(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect Coltex product dataset")
    parser.add_argument("--product-dir", type=Path, default=Path("data/product"))
    parser.add_argument("--sample", type=int, default=3, help="Print N sample records per file")
    args = parser.parse_args()

    base = args.product_dir
    manifest_path = base / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print("=== Manifest ===")
        summary = {k: manifest[k] for k in ("name", "version", "tier", "license", "documents", "documents_generated", "chunks_generated") if k in manifest}
        print(json.dumps(summary, indent=2))
        if "artifacts" in manifest:
            print("Artifacts:", json.dumps({k: v.get("records") for k, v in manifest["artifacts"].items()}, indent=2))

    files = {
        "chunks": base / "chunks" / "chunks.jsonl",
        "catalog": base / "catalog.jsonl",
        "embeddings": base / "embeddings" / "embeddings.jsonl",
        "graph": base / "graph" / "edges.jsonl",
    }

    for label, path in files.items():
        if not path.exists():
            print(f"\n[{label}] not found: {path}")
            continue
        records = list(load_jsonl(path))
        print(f"\n=== {label} ({len(records):,} records) ===")
        for rec in records[: args.sample]:
            preview = {k: (v[:80] + "…" if isinstance(v, str) and len(v) > 80 else v)
                       for k, v in rec.items() if k != "vector"}
            if "vector" in rec:
                preview["vector"] = f"[{len(rec['vector'])} dims]"
            print(json.dumps(preview, indent=2))


if __name__ == "__main__":
    main()
