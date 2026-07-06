#!/usr/bin/env python3
"""Zypher chatbot — Zypher Brain (knowledge) + LLM (reasoning engine)."""

from __future__ import annotations

import argparse

from zypher.backend import ZypherBackend
from zypher.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Zypher — Brain-first enterprise chatbot")
    parser.add_argument("--brain-config", default="config/brain.yaml")
    parser.add_argument("--llm-config", default="config/llm.yaml")
    parser.add_argument("--reindex", action="store_true", help="Rebuild Zypher Brain vector index")
    parser.add_argument("--index-only", action="store_true", help="Index and exit")
    parser.add_argument("--question", default=None, help="Single question (non-interactive)")
    args = parser.parse_args()

    config = load_config(args.brain_config, args.llm_config)
    backend = ZypherBackend(config)

    print(f"Zypher Brain: {backend.brain.document_count} documents")
    if args.reindex or args.index_only or not backend.brain.vector_index.is_indexed:
        n = backend.index_knowledge_base(force=args.reindex)
        print(f"Indexed {n} documents into Zypher Brain")

    if args.index_only:
        return

    adapter_note = " (fine-tuned adapter)" if getattr(backend.llm, "uses_adapter", False) else " (base model)"
    print(f"LLM reasoning engine{adapter_note}. Type 'quit' to exit.\n")

    if args.question:
        print(backend.chat(args.question))
        return

    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit"}:
            break
        print(f"Zypher: {backend.chat(user)}\n")


if __name__ == "__main__":
    main()
