"""Knowledge Studio local web server — Coltex V1."""

from __future__ import annotations

import cgi
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

STATIC = Path(__file__).parent / "static"
ROOT = Path(__file__).resolve().parent.parent.parent


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

        routes = {
            "/": lambda: self._file(STATIC / "index.html", "text/html; charset=utf-8"),
            "/index.html": lambda: self._file(STATIC / "index.html", "text/html; charset=utf-8"),
            "/api/v1/dashboard": lambda: self._json(rt.v1.snapshot()),
            "/api/v1/health": lambda: self._json(rt.v1.snapshot()["dashboard"]["health"]),
            "/api/v1/sources": lambda: self._json({"sources": rt.sources.list_sources(), "supported": [".pdf", ".docx", ".md", ".txt", ".html", ".json"], "coming_soon": ["github", "notion", "google_drive"]}),
            "/api/v1/settings": lambda: self._json(rt.settings.load()),
            "/api/dashboard": lambda: self._json(studio.dashboard()),
            "/api/health": lambda: self._json(rt.analytics.health()),
            "/api/curator": lambda: self._json(rt.curator.proactive_scan()),
        }
        if path in routes:
            return routes[path]()

        if path == "/api/v1/knowledge":
            limit = int(qs.get("limit", ["20"])[0])
            return self._json(studio.explorer(limit=limit))

        if path in ("/api/v1/search", "/api/search"):
            q = qs.get("q", [""])[0]
            if not q:
                return self._json({"error": "missing q"}, 400)
            return self._json(rt.universal_search(q))

        if path == "/api/v1/ask":
            q = qs.get("q", [""])[0]
            if not q:
                return self._json({"error": "missing q"}, 400)
            return self._json(rt.ask.ask(q))

        if path == "/api/explain":
            q = qs.get("q", [""])[0]
            if not q:
                return self._json({"error": "missing q"}, 400)
            rt.brain.index(force=False)
            return self._json(rt.explain.explain(q))

        self.send_error(404)

    def do_POST(self):  # noqa: N802
        rt = self.runtime
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/v1/upload":
            return self._handle_upload()

        if parsed.path == "/api/v1/settings":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            return self._json(rt.settings.save(body))

        self.send_error(404)

    def _handle_upload(self) -> None:
        rt = self.runtime
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            return self._json({"error": "expected multipart upload"}, 400)

        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"})
        if "file" not in form:
            return self._json({"error": "missing file field"}, 400)

        item = form["file"]
        if not item.filename:
            return self._json({"error": "empty filename"}, 400)

        inbox = ROOT / "data/sources/inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        dest = inbox / Path(item.filename).name
        with dest.open("wb") as f:
            f.write(item.file.read())

        result = rt.processing.process(dest)
        return self._json(result)


def serve(runtime, host: str = "127.0.0.1", port: int = 8787) -> None:
    StudioHandler.runtime = runtime
    server = HTTPServer((host, port), StudioHandler)
    print("Coltex V1 — Knowledge Studio")
    print("The AI Knowledge Platform for Modern Organizations")
    print(f"Open http://{host}:{port}/")
    print("Dashboard · Knowledge · Sources · Search · Ask Knowledge · Analytics · Settings")
    server.serve_forever()
