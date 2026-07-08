"""Coltex Runtime CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from runtime.workspace.manager import WorkspaceManager


def _rt(args: argparse.Namespace):
    from runtime.runtime import ColtexRuntime
    return ColtexRuntime.from_active_workspace(config_path=args.config)


def cmd_new(args: argparse.Namespace) -> None:
    mgr = WorkspaceManager()
    ctx = mgr.create(args.name, base_dir=args.path)
    set_active = not args.no_open
    if set_active:
        mgr.open(ctx.manifest_path, activate=True)
        rt = ColtexRuntime_with_workspace(args.config, ctx)
        print(mgr.startup_message(ctx, rt))
    else:
        print(f"Created workspace: {ctx.manifest_path}")
        print(f"Open with: coltex open {ctx.manifest_path}")


def ColtexRuntime_with_workspace(config: str, ctx):
    from runtime.runtime import ColtexRuntime
    return ColtexRuntime(config_path=config, workspace=ctx)


def cmd_open(args: argparse.Namespace) -> None:
    mgr = WorkspaceManager()
    path = Path(args.workspace)
    ctx = mgr.open(path, activate=True)
    rt = ColtexRuntime_with_workspace(args.config, ctx)
    print(mgr.startup_message(ctx, rt))


def cmd_build(args: argparse.Namespace) -> None:
    rt = _rt(args)
    result = WorkspaceManager().build(rt)
    print(json.dumps(result, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    rt = _rt(args)
    if rt.workspace is not None:
        print(json.dumps(rt.workspace_status(), indent=2))
    else:
        print(json.dumps(rt.status(), indent=2))


def cmd_validate(args: argparse.Namespace) -> None:
    rt = _rt(args)
    result = WorkspaceManager().validate(rt)
    print(json.dumps(result, indent=2))
    if not result.get("passed", False):
        sys.exit(1)


def cmd_export(args: argparse.Namespace) -> None:
    rt = _rt(args)
    output = Path(args.output) if args.output else None
    result = WorkspaceManager().export(rt, output)
    print(json.dumps(result, indent=2))


def cmd_import(args: argparse.Namespace) -> None:
    mgr = WorkspaceManager()
    ctx = mgr.import_workspace(Path(args.archive), Path(args.dest) if args.dest else None)
    rt = ColtexRuntime_with_workspace(args.config, ctx)
    print(mgr.startup_message(ctx, rt))


def cmd_dashboard(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).v1.snapshot(), indent=2))


def cmd_health(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).analytics.health(), indent=2))


def cmd_curator(args: argparse.Namespace) -> None:
    rt = _rt(args)
    result = rt.curator.proactive_scan(save=not args.no_save)
    rt.sync_workspace_manifest()
    print(json.dumps(result, indent=2))


def cmd_monitor(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).monitor.snapshot(), indent=2))


def cmd_explain(args: argparse.Namespace) -> None:
    rt = _rt(args)
    rt.brain.index(force=False)
    print(json.dumps(rt.explain.explain(args.query), indent=2))


def cmd_ingest(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).ingest(args.document_id, source=args.source), indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).universal_search(args.query), indent=2))


def cmd_ask(args: argparse.Namespace) -> None:
    rt = _rt(args)
    result = rt.ask.ask(args.question)
    rt.sync_workspace_manifest()
    print(json.dumps(result, indent=2))


def cmd_upload(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).upload_and_process(args.path), indent=2))


def cmd_sources(args: argparse.Namespace) -> None:
    rt = _rt(args)
    print(json.dumps({
        "sources": rt.sources.list_sources(),
        "count": rt.sources.count(),
        "supported": [".pdf", ".docx", ".md", ".txt", ".html", ".json"],
    }, indent=2))


def cmd_settings(args: argparse.Namespace) -> None:
    rt = _rt(args)
    if args.set:
        key, _, value = args.set.partition("=")
        if not key:
            print(json.dumps({"error": "use --set key=value"}, indent=2))
            return
        current = rt.settings.load()
        current[key.strip()] = value.strip()
        result = rt.settings.save(current)
        rt.sync_workspace_manifest()
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(rt.settings.load(), indent=2))


def cmd_events(args: argparse.Namespace) -> None:
    rt = _rt(args)
    if args.simulate:
        rt.ingest(args.document_id or "SIM-DOC-001", source="simulation")
    print(json.dumps({"events": rt.event_bus.recent, "stats": rt.event_bus.stats()}, indent=2))


def cmd_knowledge(args: argparse.Namespace) -> None:
    rt = _rt(args)
    if args.document_id:
        print(json.dumps(rt.knowledge_dna(args.document_id), indent=2))
    else:
        print(json.dumps(rt.studio.explorer(limit=args.limit), indent=2))


def cmd_connector(args: argparse.Namespace) -> None:
    print(json.dumps(_rt(args).sync_connector(args.connector_id), indent=2))


def cmd_serve(args: argparse.Namespace) -> None:
    from runtime.studio.server import serve
    serve(host=args.host, port=args.port, open_browser=not args.no_browser)


def main(argv: list[str] | None = None) -> None:
    if argv is None and len(sys.argv) == 1:
        sys.argv.append("serve")
    parser = argparse.ArgumentParser(
        prog="coltex",
        description="Coltex — local AI knowledge workspaces (.ctex)",
    )
    parser.add_argument("--config", default="config/runtime.yaml")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Create a new .ctex workspace")
    p_new.add_argument("name", help="Workspace name")
    p_new.add_argument("--path", type=Path, default=Path.cwd(), help="Parent directory")
    p_new.add_argument("--no-open", action="store_true", help="Do not activate after create")
    p_new.set_defaults(func=cmd_new)

    p_open = sub.add_parser("open", help="Open an existing .ctex workspace")
    p_open.add_argument("workspace", help="Path to .ctex manifest")
    p_open.set_defaults(func=cmd_open)

    sub.add_parser("build", help="Build or rebuild the active workspace").set_defaults(func=cmd_build)
    sub.add_parser("status", help="Workspace or runtime status").set_defaults(func=cmd_status)
    sub.add_parser("validate", help="Validate workspace integrity").set_defaults(func=cmd_validate)

    p_export = sub.add_parser("export", help="Export workspace archive")
    p_export.add_argument("--output", default="", help="Output .ctex.zip path")
    p_export.set_defaults(func=cmd_export)

    p_import = sub.add_parser("import", help="Import a workspace archive")
    p_import.add_argument("archive", help="Path to .ctex.zip archive")
    p_import.add_argument("--dest", default="", help="Destination directory")
    p_import.set_defaults(func=cmd_import)

    sub.add_parser("dashboard", help="Dashboard metrics").set_defaults(func=cmd_dashboard)
    sub.add_parser("health", help="Knowledge Health scores").set_defaults(func=cmd_health)

    p_curator = sub.add_parser("curator", help="Proactive knowledge alerts")
    p_curator.add_argument("--no-save", action="store_true")
    p_curator.set_defaults(func=cmd_curator)

    sub.add_parser("monitor", help="Runtime monitoring data").set_defaults(func=cmd_monitor)

    p_explain = sub.add_parser("explain", help="Why did Coltex retrieve this?")
    p_explain.add_argument("query")
    p_explain.set_defaults(func=cmd_explain)

    p_ingest = sub.add_parser("ingest", help="Event-driven ingest pipeline")
    p_ingest.add_argument("document_id")
    p_ingest.add_argument("--source", default="upload")
    p_ingest.set_defaults(func=cmd_ingest)

    p_search = sub.add_parser("search", help="Universal search")
    p_search.add_argument("query")
    p_search.set_defaults(func=cmd_search)

    p_ask = sub.add_parser("ask", help="Ask Knowledge")
    p_ask.add_argument("question")
    p_ask.set_defaults(func=cmd_ask)

    p_upload = sub.add_parser("upload", help="Upload and process a source file")
    p_upload.add_argument("path")
    p_upload.set_defaults(func=cmd_upload)

    sub.add_parser("sources", help="List uploaded sources").set_defaults(func=cmd_sources)

    p_settings = sub.add_parser("settings", help="View or update workspace settings")
    p_settings.add_argument("--set", default="", help="Set a value, e.g. chunk_size=1500")
    p_settings.set_defaults(func=cmd_settings)

    p_events = sub.add_parser("events", help="Recent event bus activity")
    p_events.add_argument("--simulate", action="store_true")
    p_events.add_argument("--document-id", default="")
    p_events.set_defaults(func=cmd_events)

    p_knowledge = sub.add_parser("knowledge", help="Browse knowledge objects")
    p_knowledge.add_argument("--document-id", default="")
    p_knowledge.add_argument("--limit", type=int, default=20)
    p_knowledge.set_defaults(func=cmd_knowledge)

    p_conn = sub.add_parser("connector", help="Sync a connector")
    p_conn.add_argument("connector_id", choices=["filesystem", "github"])
    p_conn.set_defaults(func=cmd_connector)

    p_serve = sub.add_parser("serve", help="Start localhost web UI (default)")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8787)
    p_serve.add_argument("--no-browser", action="store_true")
    p_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
