"""Coltex Runtime CLI."""

from __future__ import annotations

import argparse
import json


def _rt(config: str):
    from runtime.runtime import ColtexRuntime
    return ColtexRuntime(config_path=config)


def cmd_status(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).status(), indent=2))


def cmd_health(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).analytics.health(), indent=2))


def cmd_curator(args: argparse.Namespace) -> None:
    rt = _rt(args.config)
    result = rt.curator.proactive_scan(save=not args.no_save)
    print(json.dumps(result, indent=2))


def cmd_monitor(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).monitor.snapshot(), indent=2))


def cmd_explain(args: argparse.Namespace) -> None:
    rt = _rt(args.config)
    rt.brain.index(force=False)
    print(json.dumps(rt.explain.explain(args.query), indent=2))


def cmd_studio(args: argparse.Namespace) -> None:
    from runtime.studio.server import serve
    rt = _rt(args.config)
    serve(rt, host=args.host, port=args.port)


def cmd_ingest(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).ingest(args.document_id, source=args.source), indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    rt = _rt(args.config)
    rt.brain.index(force=False)
    print(json.dumps(rt.search.search(args.query), indent=2))


def cmd_events(args: argparse.Namespace) -> None:
    rt = _rt(args.config)
    if args.simulate:
        rt.ingest(args.document_id or "SIM-DOC-001", source="simulation")
    print(json.dumps({"events": rt.event_bus.recent, "stats": rt.event_bus.stats()}, indent=2))


def cmd_dna(args: argparse.Namespace) -> None:
    rt = _rt(args.config)
    if args.document_id:
        print(json.dumps(rt.knowledge_dna(args.document_id), indent=2))
    else:
        print(json.dumps(rt.knowledge_objects(limit=args.limit), indent=2))


def cmd_connector(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).sync_connector(args.connector_id), indent=2))


def cmd_explorer(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args.config).studio.explorer(limit=args.limit), indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Coltex Runtime — Knowledge Operating System")
    parser.add_argument("--config", default="config/runtime.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Runtime and engine status").set_defaults(func=cmd_status)
    sub.add_parser("health", help="Knowledge Health scores").set_defaults(func=cmd_health)

    p_curator = sub.add_parser("curator", help="AI Curator proactive alerts")
    p_curator.add_argument("--no-save", action="store_true")
    p_curator.set_defaults(func=cmd_curator)

    sub.add_parser("monitor", help="Runtime monitoring dashboard data").set_defaults(func=cmd_monitor)

    p_explain = sub.add_parser("explain", help="Why did Coltex retrieve this?")
    p_explain.add_argument("query")
    p_explain.set_defaults(func=cmd_explain)

    p_studio = sub.add_parser("studio", help="Launch Knowledge Studio web UI")
    p_studio.add_argument("--host", default="127.0.0.1")
    p_studio.add_argument("--port", type=int, default=8787)
    p_studio.set_defaults(func=cmd_studio)

    p_ingest = sub.add_parser("ingest", help="Event-driven ingest pipeline")
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

    p_dna = sub.add_parser("dna", help="Knowledge DNA")
    p_dna.add_argument("--document-id", default="")
    p_dna.add_argument("--limit", type=int, default=5)
    p_dna.set_defaults(func=cmd_dna)

    p_conn = sub.add_parser("connector", help="Sync a connector")
    p_conn.add_argument("connector_id", choices=["filesystem", "github"])
    p_conn.set_defaults(func=cmd_connector)

    p_exp = sub.add_parser("explorer", help="Knowledge Studio explorer")
    p_exp.add_argument("--limit", type=int, default=20)
    p_exp.set_defaults(func=cmd_explorer)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
