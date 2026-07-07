#!/usr/bin/env python3
"""Build Coltex Enterprise curated RAG vector dataset."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ENTERPRISE_STEPS = [
    ("chunk_documents", "Chunk knowledge base into vector-ready segments"),
    ("deduplicate", "Remove duplicate chunks"),
    ("validate_quality", "Validate quality gates"),
    ("export_graph", "Export graph relationship edges"),
    ("build_benchmarks", "Build benchmark datasets"),
    ("build_manifest", "Build product manifest with checksums"),
    ("audit_distribution", "Audit distribution compliance"),
]


def run_step(script: str, config: Path, extra: list[str] | None = None) -> None:
    cmd = [sys.executable, str(Path(__file__).parent / f"{script}.py"), "--config", str(config)]
    if extra:
        cmd.extend(extra)
    print(f"\n=== {script} ===")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Coltex Enterprise RAG vector dataset")
    parser.add_argument("--config", type=Path, default=Path("config/product_enterprise.yaml"))
    parser.add_argument("--skip-embeddings", action="store_true")
    parser.add_argument("--skip-eval", action="store_true")
    args = parser.parse_args()

    for script, _ in ENTERPRISE_STEPS:
        run_step(script, args.config)

    if not args.skip_embeddings:
        run_step("export_embeddings", args.config)

    if not args.skip_eval:
        run_step("evaluate_rag", args.config)

    print("\nColtex Enterprise RAG vector dataset build complete.")
    print("Artifacts: data/product/ · Benchmarks: benchmarks/")
    print("Inspect: python3 examples/load_dataset.py")


if __name__ == "__main__":
    main()
