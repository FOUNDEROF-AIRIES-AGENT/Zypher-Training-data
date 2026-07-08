"""Coltex localhost server — web UI for .ctex workspaces."""

from __future__ import annotations

import json
import mimetypes
import re
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

STATIC = Path(__file__).parent / "static"
ROOT = Path(__file__).resolve().parent.parent.parent


class StudioState:
    """Shared runtime state for the web server."""

    def __init__(self):
        self.manager = None
        self.runtime = None
        self._init()

    def _init(self) -> None:
        from runtime.runtime import ColtexRuntime
        from runtime.workspace.manager import WorkspaceManager

        self.manager = WorkspaceManager()
        self.runtime = ColtexRuntime.from_active_workspace()

    def reload(self, manifest_path: Path | None = None) -> None:
        from runtime.runtime import ColtexRuntime

        if manifest_path:
            ctx = self.manager.open(manifest_path, activate=True)
            self.runtime = ColtexRuntime(workspace=ctx)
        else:
            self.runtime = ColtexRuntime.from_active_workspace()


STATE = StudioState()


def _parse_multipart(body: bytes, content_type: str) -> dict[str, tuple[str, bytes]]:
    """Minimal multipart/form-data parser (no cgi — Windows/Python 3.13 safe)."""
    match = re.search(r"boundary=(.+)", content_type)
    if not match:
        return {}
    boundary = match.group(1).strip('"').encode()
    parts = body.split(b"--" + boundary)
    fields: dict[str, tuple[str, bytes]] = {}
    for part in parts:
        if b"Content-Disposition" not in part:
            continue
        header, _, rest = part.partition(b"\r\n\r\n")
        if not rest:
            continue
        content = rest.rstrip(b"\r\n--")
        name_match = re.search(rb'name="([^"]+)"', header)
        file_match = re.search(rb'filename="([^"]*)"', header)
        if not name_match:
            continue
        name = name_match.group(1).decode("utf-8", errors="replace")
        filename = file_match.group(1).decode("utf-8", errors="replace") if file_match else ""
        fields[name] = (filename, content)
    return fields


class StudioHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A003
        pass

    def _json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path) -> None:
        if not path.exists():
            self.send_error(404)
            return
        content_type, _ = mimetypes.guess_type(str(path))
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)
        rt = STATE.runtime

        if path in ("/", "/index.html"):
            return self._file(STATIC / "index.html")

        if path.startswith("/static/"):
            rel = path.removeprefix("/static/")
            target = (STATIC / rel).resolve()
            if str(target).startswith(str(STATIC.resolve())):
                return self._file(target)
            return self.send_error(403)

        try:
            if path == "/api/status":
                if rt.workspace:
                    return self._json(rt.workspace_status())
                return self._json({"workspace": None, "runtime": rt.status()})

            if path == "/api/dashboard":
                return self._json(rt.v1.snapshot())

            if path == "/api/health":
                return self._json(rt.analytics.health())

            if path == "/api/knowledge":
                limit = int(qs.get("limit", ["25"])[0])
                return self._json(rt.studio.explorer(limit=limit))

            if path == "/api/sources":
                return self._json({
                    "sources": rt.sources.list_sources(),
                    "supported": [".pdf", ".docx", ".md", ".txt", ".html", ".json"],
                })

            if path == "/api/settings":
                return self._json(rt.settings.load())

            if path == "/api/curator":
                return self._json(rt.curator.proactive_scan())

            if path == "/api/search":
                q = qs.get("q", [""])[0]
                if not q:
                    return self._json({"error": "missing q"}, 400)
                return self._json(rt.universal_search(q))

            if path == "/api/ask":
                q = qs.get("q", [""])[0]
                if not q:
                    return self._json({"error": "missing q"}, 400)
                return self._json(rt.ask.ask(q))

            self.send_error(404)
        except Exception as exc:
            self._json({"error": str(exc)}, 500)

    def do_POST(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        content_type = self.headers.get("Content-Type", "")

        try:
            if path == "/api/workspace/new":
                data = json.loads(body.decode("utf-8"))
                name = data.get("name", "").strip()
                if not name:
                    return self._json({"error": "name required"}, 400)
                base = Path(data.get("path") or ROOT / "workspaces")
                ctx = STATE.manager.create(name, base_dir=base)
                STATE.reload(ctx.manifest_path)
                return self._json({
                    "status": "created",
                    "name": ctx.name,
                    "manifest": str(ctx.manifest_path),
                })

            if path == "/api/workspace/open":
                data = json.loads(body.decode("utf-8"))
                manifest = Path(data.get("manifest", "")).expanduser()
                if not manifest.exists():
                    return self._json({"error": "workspace not found"}, 404)
                STATE.reload(manifest)
                return self._json({
                    "status": "opened",
                    "workspace": STATE.runtime.workspace_status(),
                })

            if path == "/api/build":
                result = STATE.manager.build(STATE.runtime)
                return self._json(result)

            if path == "/api/validate":
                result = STATE.manager.validate(STATE.runtime)
                return self._json(result)

            if path == "/api/upload":
                return self._handle_upload(content_type, body)

            if path == "/api/settings":
                data = json.loads(body.decode("utf-8"))
                return self._json(STATE.runtime.settings.save(data))

            self.send_error(404)
        except Exception as exc:
            self._json({"error": str(exc)}, 500)

    def _handle_upload(self, content_type: str, body: bytes) -> None:
        rt = STATE.runtime
        if rt.workspace is None:
            return self._json({"error": "open or create a workspace first"}, 400)

        fields = _parse_multipart(body, content_type)
        if "file" not in fields:
            return self._json({"error": "missing file field"}, 400)

        filename, content = fields["file"]
        if not filename:
            return self._json({"error": "empty filename"}, 400)

        inbox = rt.workspace.documents_inbox
        inbox.mkdir(parents=True, exist_ok=True)
        dest = inbox / Path(filename).name
        dest.write_bytes(content)
        result = rt.processing.process(dest)
        return self._json(result)


def serve(
    host: str = "127.0.0.1",
    port: int = 8787,
    open_browser: bool = True,
) -> None:
    """Start Coltex localhost server."""
    (ROOT / "workspaces").mkdir(exist_ok=True)
    server = ThreadingHTTPServer((host, port), StudioHandler)
    url = f"http://{host}:{port}/"

    print("")
    print("  ┌─────────────────────────────────────────────┐")
    print("  │  Coltex — The AI Knowledge Platform         │")
    print("  └─────────────────────────────────────────────┘")
    print("")
    print(f"  Localhost  {url}")
    print("")
    print("  Press Ctrl+C to stop")
    print("")

    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.shutdown()
