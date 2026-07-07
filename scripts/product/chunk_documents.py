#!/usr/bin/env python3
"""Build vector-ready chunks with accurate metadata from curated documents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import chunk_document, load_knowledge_base, load_product_config, resolve_path, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Build vector-ready chunks")
    parser.add_argument("--config", type=Path, default=Path("config/product.yaml"))
    args = parser.parse_args()

    cfg = load_product_config(args.config)
    kb = load_knowledge_base(cfg)
    chunk_cfg = cfg["chunking"]
    out_path = resolve_path(cfg["output"]["chunks"])

    all_chunks: list[dict] = []
    for doc in kb.documents:
        all_chunks.extend(
            chunk_document(
                doc,
                max_chars=int(chunk_cfg["max_chunk_chars"]),
                overlap=int(chunk_cfg["overlap_chars"]),
                split_on=str(chunk_cfg.get("split_on", "## ")),
                license_name=cfg.get("license", "Coltex-EULA"),
            )
        )

    write_jsonl(out_path, all_chunks)
    print(json.dumps({
        "chunks": len(all_chunks),
        "documents": len(kb.documents),
        "output": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
