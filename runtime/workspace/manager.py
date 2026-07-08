"""Workspace lifecycle: create, open, build, validate, export, import."""

from __future__ import annotations

import json
import shutil
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from runtime.workspace.context import COLTEX_VERSION, WorkspaceContext
from runtime.workspace.manifest import (
    default_manifest,
    export_metadata_snapshot,
    load_manifest,
    save_manifest,
    sync_manifest_from_runtime,
)
from runtime.workspace.session import set_active_workspace


class WorkspaceManager:
    def create(self, name: str, base_dir: Path | None = None) -> WorkspaceContext:
        base = Path(base_dir or Path.cwd())
        root = (base / name).resolve()
        if root.exists() and any(root.iterdir()):
            raise FileExistsError(f"Directory already exists and is not empty: {root}")

        root.mkdir(parents=True, exist_ok=True)
        ctx = WorkspaceContext(
            root=root,
            manifest_path=root / f"{name}.ctex",
            name=name,
        )
        ctx.ensure_layout()
        manifest = default_manifest(name)
        save_manifest(ctx.manifest_path, manifest)
        ctx.write_brain_config(manifest.get("settings", {}))
        settings_path = ctx.settings_json_path
        settings_path.write_text(
            json.dumps(manifest.get("settings", {}), indent=2),
            encoding="utf-8",
        )
        return ctx

    def open(self, manifest_path: Path, activate: bool = True) -> WorkspaceContext:
        manifest_path = Path(manifest_path).expanduser().resolve()
        if manifest_path.is_dir():
            matches = list(manifest_path.glob("*.ctex"))
            if not matches:
                raise FileNotFoundError(f"No .ctex manifest in directory: {manifest_path}")
            manifest_path = matches[0]
        if not manifest_path.exists():
            raise FileNotFoundError(f"Workspace not found: {manifest_path}")
        ctx = WorkspaceContext.from_manifest(manifest_path)
        ctx.ensure_layout()
        if activate:
            set_active_workspace(ctx.manifest_path)
        return ctx

    def build(self, runtime) -> dict[str, Any]:
        ctx = runtime.workspace
        if ctx is None:
            return {"error": "no active workspace"}

        steps: list[str] = []
        inbox_files = list(ctx.documents_inbox.rglob("*"))
        for path in inbox_files:
            if path.is_file():
                runtime.upload_and_process(path)
        steps.append("process_documents")

        runtime.brain.metadata_index.refresh()
        steps.append("extract_metadata")

        indexed = runtime.brain.index(force=True)
        steps.append("generate_embeddings")

        export_metadata_snapshot(ctx, runtime)
        steps.append("update_graph")

        runtime.curator.proactive_scan(save=True)
        steps.append("validate")

        data = load_manifest(ctx.manifest_path)
        data["statistics"]["last_build_at"] = datetime.now(timezone.utc).isoformat()
        save_manifest(ctx.manifest_path, data)
        sync_manifest_from_runtime(ctx, runtime)
        steps.append("save_manifest")

        return {
            "status": "built",
            "workspace": ctx.name,
            "indexed_vectors": indexed,
            "steps": steps,
        }

    def validate(self, runtime) -> dict[str, Any]:
        ctx = runtime.workspace
        if ctx is None:
            return {"passed": False, "issues": ["no active workspace"]}

        issues: list[str] = []
        warnings: list[str] = []

        if not ctx.manifest_path.exists():
            issues.append("Missing .ctex manifest")
        else:
            try:
                load_manifest(ctx.manifest_path)
            except ValueError as exc:
                issues.append(str(exc))

        for dirname in (
            "knowledge", "documents", "embeddings", "graph", "metadata",
            "settings", "runtime",
        ):
            if not (ctx.root / dirname).is_dir():
                issues.append(f"Missing directory: {dirname}/")

        if not ctx.brain_config_path.exists():
            issues.append("Missing settings/brain.yaml")

        settings = runtime.settings.load()
        if not settings.get("embedding_model"):
            warnings.append("embedding_model not configured")

        doc_ids = {d.doc_id for d in runtime.brain.kb.documents}
        broken = 0
        for doc in runtime.brain.kb.documents:
            path = Path(doc.path)
            if not path.exists():
                broken += 1
            for rel_id in doc.related or []:
                if rel_id not in doc_ids:
                    broken += 1
        if broken:
            warnings.append(f"{broken} broken document references")

        if not ctx.vector_store.exists():
            warnings.append("Vector index not initialized — run `coltex build`")

        sync_manifest_from_runtime(ctx, runtime)

        return {
            "passed": not issues,
            "workspace": ctx.name,
            "issues": issues,
            "warnings": warnings,
        }

    def export(self, runtime, output: Path | None = None) -> dict[str, Any]:
        ctx = runtime.workspace
        if ctx is None:
            return {"error": "no active workspace"}

        sync_manifest_from_runtime(ctx, runtime)
        archive = output or (Path.cwd() / f"{ctx.name}.ctex.zip")
        archive = archive.resolve()

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in ctx.root.rglob("*"):
                if path.is_file() and "cache" not in path.parts:
                    arcname = path.relative_to(ctx.root.parent)
                    zf.write(path, arcname)

        return {
            "status": "exported",
            "workspace": ctx.name,
            "archive": str(archive),
            "size_bytes": archive.stat().st_size,
        }

    def import_workspace(self, archive_path: Path, dest: Path | None = None) -> WorkspaceContext:
        archive_path = Path(archive_path).expanduser().resolve()
        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        if archive_path.suffix == ".zip" or str(archive_path).endswith(".ctex.zip"):
            return self._import_zip(archive_path, dest)
        if archive_path.suffix in {".tar", ".gz", ".tgz"} or archive_path.name.endswith(".tar.gz"):
            return self._import_tar(archive_path, dest)
        raise ValueError(f"Unsupported archive format: {archive_path}")

    def _import_zip(self, archive_path: Path, dest: Path | None) -> WorkspaceContext:
        with zipfile.ZipFile(archive_path, "r") as zf:
            names = zf.namelist()
            if not names:
                raise ValueError("Empty archive")
            top = names[0].split("/")[0]
            target = Path(dest or Path.cwd()) / top
            target.mkdir(parents=True, exist_ok=True)
            zf.extractall(target.parent)

        manifest = next(target.glob("*.ctex"), None)
        if manifest is None:
            raise ValueError(f"No .ctex manifest found in imported workspace: {target}")
        return self.open(manifest, activate=True)

    def _import_tar(self, archive_path: Path, dest: Path | None) -> WorkspaceContext:
        target_parent = Path(dest or Path.cwd())
        with tarfile.open(archive_path, "r:*") as tf:
            tf.extractall(target_parent)
        dirs = [p for p in target_parent.iterdir() if p.is_dir()]
        if not dirs:
            raise ValueError("Archive contained no workspace directory")
        target = dirs[0]
        manifest = next(target.glob("*.ctex"), None)
        if manifest is None:
            raise ValueError(f"No .ctex manifest found in imported workspace: {target}")
        return self.open(manifest, activate=True)

    def startup_message(self, ctx: WorkspaceContext, runtime) -> str:
        data = sync_manifest_from_runtime(ctx, runtime)
        stats = data.get("statistics", {})
        health = data.get("health", {})
        last_build = stats.get("last_build_at")
        last_build_human = _human_ago(last_build) if last_build else "never"

        lines = [
            "Opening Workspace...",
            "",
            f"Workspace: {ctx.name}",
            f"Coltex Version: {COLTEX_VERSION}",
            f"Knowledge Health: {health.get('knowledge_score', 0)}%",
            f"Documents: {stats.get('documents', 0):,}",
            f"Embeddings: {stats.get('embeddings', 0):,}",
            f"Graph Nodes: {stats.get('graph_nodes', 0):,}",
            f"Last Build: {last_build_human}",
            "",
            "Workspace Ready.",
        ]
        return "\n".join(lines)


def _human_ago(iso_ts: str) -> str:
    try:
        ts = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - ts
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        if seconds < 3600:
            return f"{seconds // 60} minutes ago"
        if seconds < 86400:
            return f"{seconds // 3600} hours ago"
        return f"{seconds // 86400} days ago"
    except (ValueError, TypeError):
        return iso_ts
