#!/usr/bin/env python3
"""Zypher Platform CLI — serve API, run jobs, admin."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Zypher Platform")
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="Start REST API server")
    serve.add_argument("--host", default=None)
    serve.add_argument("--port", type=int, default=None)

    sub.add_parser("stats", help="Print platform stats")
    sub.add_parser("index", help="Index Zypher Brain")

    args = parser.parse_args()

    if args.command == "serve":
        import uvicorn
        from zypher_platform.core import ZypherPlatform

        cfg = ZypherPlatform().config.get("server", {})
        host = args.host or cfg.get("host", "0.0.0.0")
        port = args.port or int(cfg.get("port", 8080))
        uvicorn.run("zypher_platform.api.app:app", host=host, port=port, reload=cfg.get("reload", False))

    elif args.command == "stats":
        import json

        from zypher_platform.core import ZypherPlatform

        print(json.dumps(ZypherPlatform().stats(), indent=2))

    elif args.command == "index":
        from zypher_platform.core import ZypherPlatform

        p = ZypherPlatform()
        n = p.index_brain(force=True)
        print(f"Indexed {n} documents")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
