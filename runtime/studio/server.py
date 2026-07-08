"""Knowledge Studio local web server."""

from __future__ import annotations

import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

STATIC = Path(__file__).parent / "static"


class StudioHandler(BaseHTTPRequestHandler):
    runtime = None

    def log_message(self, format, *args):  # noqa: A003
        pass

    def _json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(404)
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        rt = self.runtime
        studio = rt.studio
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            return self._file(STATIC / "index.html", "text/html; charset=utf-8")

        if path == "/api/dashboard":
            return self._json(studio.dashboard())

        if path == "/api/health":
            return self._json(rt.analytics.health())

        if path == "/api/monitor":
            return self._json(rt.monitor.snapshot())

        if path == "/api/curator":
            return self._json(rt.curator.proactive_scan())

        if path == "/api/explorer":
            limit = int(qs.get("limit", ["20"])[0])
            offset = int(qs.get("offset", ["0"])[0])
            return self._json(studio.explorer(limit=limit, offset=offset))

        if path == "/api/search":
            q = qs.get("q", [""])[0]
            if not q:
                return self._json({"error": "missing q"}, 400)
            rt.brain.index(force=False)
            return self._json(rt.search.search(q))

        if path == "/api/explain":
            q = qs.get("q", [""])[0]
            if not q:
                return self._json({"error": "missing q"}, 400)
            rt.brain.index(force=False)
            return self._json(rt.explain.explain(q))

        if path == "/api/connectors":
            return self._json({"connectors": rt.connectors.list_connectors()})

        if path == "/api/lifecycle":
            doc_id = qs.get("id", [None])[0]
            return self._json(studio.lifecycle(doc_id))

        if path == "/api/plugins":
            return self._json(rt.plugins.stats())

        self.send_error(404)


def serve(runtime, host: str = "127.0.0.1", port: int = 8787) -> None:
    StudioHandler.runtime = runtime
    server = HTTPServer((host, port), StudioHandler)
    print(f"Knowledge Studio running at http://{host}:{port}/")
    print("Modules: Explorer · Search · Graph · Analytics · Curator · Lifecycle · Plugins · Monitor")
    server.serve_forever()
