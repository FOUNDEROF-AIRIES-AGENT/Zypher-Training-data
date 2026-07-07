"""Run Coltex Platform API server."""

from __future__ import annotations

import argparse

import uvicorn

from coltex_platform.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Coltex RAG-as-a-Service")
    parser.add_argument("--host", default=None)
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    host = args.host or cfg.get("server", {}).get("host", "0.0.0.0")
    port = args.port or int(cfg.get("server", {}).get("port", 8080))
    uvicorn.run(
        "coltex_platform.app:app",
        host=host,
        port=port,
        reload=args.reload,
        workers=1 if args.reload else int(cfg.get("server", {}).get("workers", 1)),
    )


if __name__ == "__main__":
    main()
