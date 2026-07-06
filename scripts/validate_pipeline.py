#!/usr/bin/env python3
"""Validate Zypher Brain and optional training pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def check(name: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Zypher setup")
    parser.add_argument("--require-adapter", action="store_true")
    args = parser.parse_args()

    root = ROOT
    all_ok = True

    for pkg in ("yaml", "chromadb"):
        try:
            __import__(pkg)
            check(f"import {pkg}", True)
        except ImportError:
            all_ok = check(f"import {pkg}", False, "pip install -r requirements.txt")

    for path in (
        "config/brain.yaml",
        "config/llm.yaml",
        "config/corpus_generation.yaml",
        "brain/brain.py",
        "requirements.txt",
    ):
        all_ok = check(f"file {path}", (root / path).exists()) and all_ok

    try:
        from brain import ZypherBrain

        brain = ZypherBrain()
        all_ok = check("Zypher Brain", brain.document_count > 0, f"{brain.document_count} docs") and all_ok
    except Exception as exc:
        all_ok = check("Zypher Brain", False, str(exc))

    adapter = root / "outputs/zypher-xs/final/adapter_config.json"
    if args.require_adapter:
        all_ok = check("optional adapter", adapter.exists(), str(adapter)) and all_ok
    else:
        check("optional adapter", adapter.exists(), "enable in config/llm.yaml if trained")

    if not all_ok:
        print("\nValidation failed.")
        sys.exit(1)
    print("\nValidation passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
