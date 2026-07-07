"""Coltex Runtime CLI."""

from __future__ import annotations

import argparse
import json
import sys


def cmd_status(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    print(json.dumps(rt.status(), indent=2))


def cmd_health(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    print(json.dumps(rt.analytics.health(), indent=2))


def cmd_curator(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    print(json.dumps(rt.curator.recommend(), indent=2))


def cmd_ingest(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    print(json.dumps(rt.ingest(args.document_id, source=args.source), indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    rt.brain.index(force=False)
    print(json.dumps(rt.search.search(args.query), indent=2))


def cmd_events(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    if args.simulate:
        rt.ingest(args.document_id or "SIM-DOC-001", source="simulation")
    print(json.dumps({"events": rt.event_bus.recent, "stats": rt.event_bus.stats()}, indent=2))


def cmd_dna(args: argparse.Namespace) -> None:
    from runtime.runtime import ColtexRuntime

    rt = ColtexRuntime(config_path=args.config)
    if args.document_id:
        print(json.dumps(rt.knowledge_dna(args.document_id), indent=2))
    else:
        print(json.dumps(rt.knowledge_objects(limit=args.limit), indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Coltex Runtime — Knowledge Operating System")
    parser.add_argument("--config", default="config/runtime.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Runtime and engine status").set_defaults(func=cmd_status)

    sub.add_parser("health", help="Knowledge analytics health scores").set_defaults(func=cmd_health)

    sub.add_parser("curator", help="AI Curator recommendations").set_defaults(func=cmd_curator)

    p_ingest = sub.add_parser("ingest", help="Run event-driven ingest pipeline")
    p_ingest.add_argument("document_id")
    p_ingest.add_argument("--source", default="upload")
    p_ingest.set_defaults(func=cmd_ingest)

    p_search = sub.add_parser("search", help="Search knowledge objects")
    p_search.add_argument("query")
    p_search.set_defaults(func=cmd_search)

    p_events = sub.add_parser("events", help="Recent event bus activity")
    p_events.add_argument("--simulate", action="store_true")
    p_events.add_argument("--document-id", default="")
    p_events.set_defaults(func=cmd_events)

    p_dna = sub.add_parser("dna", help="Knowledge DNA for objects")
    p_dna.add_argument("--document-id", default="")
    p_dna.add_argument("--limit", type=int, default=5)
    p_dna.set_defaults(func=cmd_dna)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
