"""SQLite persistence for tenants, collections, documents, and jobs."""

from __future__ import annotations

import json
import secrets
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Tenant:
    id: str
    name: str
    email: str
    tier: str
    created_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ApiKey:
    id: str
    tenant_id: str
    key_hash: str
    prefix: str
    name: str
    created_at: str
    last_used_at: str | None = None
    scopes: list[str] = field(default_factory=lambda: ["read", "write"])


@dataclass
class Workspace:
    id: str
    tenant_id: str
    name: str
    slug: str
    created_at: str


@dataclass
class Collection:
    id: str
    workspace_id: str
    tenant_id: str
    name: str
    slug: str
    description: str
    document_count: int
    indexed_count: int
    status: str
    kb_path: str
    vector_path: str
    created_at: str
    updated_at: str


@dataclass
class DocumentRecord:
    id: str
    collection_id: str
    title: str
    source_type: str
    source_uri: str
    file_path: str
    status: str
    doc_type: str
    category: str
    created_at: str
    indexed_at: str | None = None


@dataclass
class JobRecord:
    id: str
    tenant_id: str
    collection_id: str
    job_type: str
    status: str
    progress: float
    message: str
    payload: dict[str, Any]
    result: dict[str, Any]
    created_at: str
    updated_at: str
    completed_at: str | None = None


class PlatformStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS tenants (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    tier TEXT NOT NULL DEFAULT 'free',
                    metadata_json TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS api_keys (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    key_hash TEXT NOT NULL UNIQUE,
                    prefix TEXT NOT NULL,
                    name TEXT NOT NULL,
                    scopes_json TEXT DEFAULT '["read","write"]',
                    created_at TEXT NOT NULL,
                    last_used_at TEXT,
                    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
                );
                CREATE TABLE IF NOT EXISTS workspaces (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(tenant_id, slug)
                );
                CREATE TABLE IF NOT EXISTS collections (
                    id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    document_count INTEGER DEFAULT 0,
                    indexed_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'ready',
                    kb_path TEXT NOT NULL,
                    vector_path TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(workspace_id, slug)
                );
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    collection_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_uri TEXT DEFAULT '',
                    file_path TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    doc_type TEXT DEFAULT 'documentation',
                    category TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    indexed_at TEXT,
                    FOREIGN KEY (collection_id) REFERENCES collections(id)
                );
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    collection_id TEXT NOT NULL,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress REAL DEFAULT 0,
                    message TEXT DEFAULT '',
                    payload_json TEXT DEFAULT '{}',
                    result_json TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    completed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS usage (
                    tenant_id TEXT NOT NULL,
                    day TEXT NOT NULL,
                    retrieve_count INTEGER DEFAULT 0,
                    chat_count INTEGER DEFAULT 0,
                    ingest_count INTEGER DEFAULT 0,
                    PRIMARY KEY (tenant_id, day)
                );
                """
            )

    def create_tenant(self, name: str, email: str, tier: str = "free") -> Tenant:
        tenant = Tenant(
            id=str(uuid.uuid4()),
            name=name,
            email=email.lower(),
            tier=tier,
            created_at=_utcnow(),
        )
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO tenants (id, name, email, tier, created_at) VALUES (?, ?, ?, ?, ?)",
                (tenant.id, tenant.name, tenant.email, tenant.tier, tenant.created_at),
            )
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,)).fetchone()
        return self._row_tenant(row) if row else None

    def get_tenant_by_email(self, email: str) -> Tenant | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM tenants WHERE email = ?", (email.lower(),)).fetchone()
        return self._row_tenant(row) if row else None

    def create_api_key(self, tenant_id: str, name: str, raw_key: str, prefix: str) -> ApiKey:
        import hashlib

        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        record = ApiKey(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            key_hash=key_hash,
            prefix=prefix,
            name=name,
            created_at=_utcnow(),
        )
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO api_keys (id, tenant_id, key_hash, prefix, name, scopes_json, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.id,
                    record.tenant_id,
                    record.key_hash,
                    record.prefix,
                    record.name,
                    json.dumps(record.scopes),
                    record.created_at,
                ),
            )
        return record

    def verify_api_key(self, raw_key: str) -> tuple[ApiKey, Tenant] | None:
        import hashlib

        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM api_keys WHERE key_hash = ?", (key_hash,)).fetchone()
            if not row:
                return None
            conn.execute(
                "UPDATE api_keys SET last_used_at = ? WHERE id = ?",
                (_utcnow(), row["id"]),
            )
            tenant_row = conn.execute("SELECT * FROM tenants WHERE id = ?", (row["tenant_id"],)).fetchone()
        if not tenant_row:
            return None
        return self._row_api_key(row), self._row_tenant(tenant_row)

    def list_api_keys(self, tenant_id: str) -> list[ApiKey]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM api_keys WHERE tenant_id = ? ORDER BY created_at DESC",
                (tenant_id,),
            ).fetchall()
        return [self._row_api_key(r) for r in rows]

    def create_workspace(self, tenant_id: str, name: str, slug: str) -> Workspace:
        ws = Workspace(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            created_at=_utcnow(),
        )
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO workspaces (id, tenant_id, name, slug, created_at) VALUES (?, ?, ?, ?, ?)",
                (ws.id, ws.tenant_id, ws.name, ws.slug, ws.created_at),
            )
        return ws

    def list_workspaces(self, tenant_id: str) -> list[Workspace]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM workspaces WHERE tenant_id = ? ORDER BY created_at",
                (tenant_id,),
            ).fetchall()
        return [self._row_workspace(r) for r in rows]

    def get_workspace(self, workspace_id: str, tenant_id: str) -> Workspace | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM workspaces WHERE id = ? AND tenant_id = ?",
                (workspace_id, tenant_id),
            ).fetchone()
        return self._row_workspace(row) if row else None

    def create_collection(
        self,
        workspace_id: str,
        tenant_id: str,
        name: str,
        slug: str,
        kb_path: str,
        vector_path: str,
        description: str = "",
    ) -> Collection:
        now = _utcnow()
        col = Collection(
            id=str(uuid.uuid4()),
            workspace_id=workspace_id,
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            description=description,
            document_count=0,
            indexed_count=0,
            status="ready",
            kb_path=kb_path,
            vector_path=vector_path,
            created_at=now,
            updated_at=now,
        )
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO collections
                   (id, workspace_id, tenant_id, name, slug, description, kb_path, vector_path,
                    created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    col.id,
                    col.workspace_id,
                    col.tenant_id,
                    col.name,
                    col.slug,
                    col.description,
                    col.kb_path,
                    col.vector_path,
                    col.created_at,
                    col.updated_at,
                ),
            )
        return col

    def list_collections(self, tenant_id: str, workspace_id: str | None = None) -> list[Collection]:
        with self._conn() as conn:
            if workspace_id:
                rows = conn.execute(
                    "SELECT * FROM collections WHERE tenant_id = ? AND workspace_id = ? ORDER BY name",
                    (tenant_id, workspace_id),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM collections WHERE tenant_id = ? ORDER BY name",
                    (tenant_id,),
                ).fetchall()
        return [self._row_collection(r) for r in rows]

    def get_collection(self, collection_id: str, tenant_id: str) -> Collection | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM collections WHERE id = ? AND tenant_id = ?",
                (collection_id, tenant_id),
            ).fetchone()
        return self._row_collection(row) if row else None

    def update_collection_counts(self, collection_id: str, document_count: int, indexed_count: int) -> None:
        with self._conn() as conn:
            conn.execute(
                """UPDATE collections SET document_count = ?, indexed_count = ?, updated_at = ?
                   WHERE id = ?""",
                (document_count, indexed_count, _utcnow(), collection_id),
            )

    def add_document(
        self,
        collection_id: str,
        title: str,
        file_path: str,
        source_type: str = "upload",
        source_uri: str = "",
        doc_type: str = "documentation",
        category: str = "",
    ) -> DocumentRecord:
        doc = DocumentRecord(
            id=str(uuid.uuid4()),
            collection_id=collection_id,
            title=title,
            source_type=source_type,
            source_uri=source_uri,
            file_path=file_path,
            status="pending",
            doc_type=doc_type,
            category=category,
            created_at=_utcnow(),
        )
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO documents
                   (id, collection_id, title, source_type, source_uri, file_path, status,
                    doc_type, category, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    doc.id,
                    doc.collection_id,
                    doc.title,
                    doc.source_type,
                    doc.source_uri,
                    doc.file_path,
                    doc.status,
                    doc.doc_type,
                    doc.category,
                    doc.created_at,
                ),
            )
        return doc

    def list_documents(self, collection_id: str) -> list[DocumentRecord]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM documents WHERE collection_id = ? ORDER BY created_at DESC",
                (collection_id,),
            ).fetchall()
        return [self._row_document(r) for r in rows]

    def get_document(self, document_id: str, collection_id: str) -> DocumentRecord | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM documents WHERE id = ? AND collection_id = ?",
                (document_id, collection_id),
            ).fetchone()
        return self._row_document(row) if row else None

    def mark_document_indexed(self, document_id: str) -> None:
        with self._conn() as conn:
            conn.execute(
                "UPDATE documents SET status = 'indexed', indexed_at = ? WHERE id = ?",
                (_utcnow(), document_id),
            )

    def create_job(
        self,
        tenant_id: str,
        collection_id: str,
        job_type: str,
        payload: dict[str, Any] | None = None,
    ) -> JobRecord:
        now = _utcnow()
        job = JobRecord(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            collection_id=collection_id,
            job_type=job_type,
            status="queued",
            progress=0.0,
            message="Queued",
            payload=payload or {},
            result={},
            created_at=now,
            updated_at=now,
        )
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO jobs
                   (id, tenant_id, collection_id, job_type, status, progress, message,
                    payload_json, result_json, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    job.id,
                    job.tenant_id,
                    job.collection_id,
                    job.job_type,
                    job.status,
                    job.progress,
                    job.message,
                    json.dumps(job.payload),
                    json.dumps(job.result),
                    job.created_at,
                    job.updated_at,
                ),
            )
        return job

    def update_job(
        self,
        job_id: str,
        status: str | None = None,
        progress: float | None = None,
        message: str | None = None,
        result: dict[str, Any] | None = None,
    ) -> JobRecord | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not row:
                return None
            updates: list[str] = ["updated_at = ?"]
            values: list[Any] = [_utcnow()]
            if status is not None:
                updates.append("status = ?")
                values.append(status)
                if status in ("completed", "failed"):
                    updates.append("completed_at = ?")
                    values.append(_utcnow())
            if progress is not None:
                updates.append("progress = ?")
                values.append(progress)
            if message is not None:
                updates.append("message = ?")
                values.append(message)
            if result is not None:
                updates.append("result_json = ?")
                values.append(json.dumps(result))
            values.append(job_id)
            conn.execute(f"UPDATE jobs SET {', '.join(updates)} WHERE id = ?", values)
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return self._row_job(row) if row else None

    def get_job(self, job_id: str, tenant_id: str) -> JobRecord | None:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM jobs WHERE id = ? AND tenant_id = ?",
                (job_id, tenant_id),
            ).fetchone()
        return self._row_job(row) if row else None

    def list_jobs(self, tenant_id: str, collection_id: str | None = None) -> list[JobRecord]:
        with self._conn() as conn:
            if collection_id:
                rows = conn.execute(
                    "SELECT * FROM jobs WHERE tenant_id = ? AND collection_id = ? ORDER BY created_at DESC",
                    (tenant_id, collection_id),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM jobs WHERE tenant_id = ? ORDER BY created_at DESC LIMIT 100",
                    (tenant_id,),
                ).fetchall()
        return [self._row_job(r) for r in rows]

    def increment_usage(self, tenant_id: str, metric: str) -> None:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        column = {
            "retrieve": "retrieve_count",
            "chat": "chat_count",
            "ingest": "ingest_count",
        }.get(metric)
        if not column:
            return
        with self._conn() as conn:
            conn.execute(
                f"""INSERT INTO usage (tenant_id, day, {column}) VALUES (?, ?, 1)
                    ON CONFLICT(tenant_id, day) DO UPDATE SET {column} = {column} + 1""",
                (tenant_id, day),
            )

    def get_usage_today(self, tenant_id: str) -> dict[str, int]:
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM usage WHERE tenant_id = ? AND day = ?",
                (tenant_id, day),
            ).fetchone()
        if not row:
            return {"retrieve": 0, "chat": 0, "ingest": 0}
        return {
            "retrieve": row["retrieve_count"],
            "chat": row["chat_count"],
            "ingest": row["ingest_count"],
        }

    @staticmethod
    def generate_api_key(prefix: str) -> str:
        return f"{prefix}{secrets.token_urlsafe(32)}"

    @staticmethod
    def _row_tenant(row: sqlite3.Row) -> Tenant:
        return Tenant(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            tier=row["tier"],
            created_at=row["created_at"],
            metadata=json.loads(row["metadata_json"] or "{}"),
        )

    @staticmethod
    def _row_api_key(row: sqlite3.Row) -> ApiKey:
        return ApiKey(
            id=row["id"],
            tenant_id=row["tenant_id"],
            key_hash=row["key_hash"],
            prefix=row["prefix"],
            name=row["name"],
            created_at=row["created_at"],
            last_used_at=row["last_used_at"],
            scopes=json.loads(row["scopes_json"] or '["read","write"]'),
        )

    @staticmethod
    def _row_workspace(row: sqlite3.Row) -> Workspace:
        return Workspace(
            id=row["id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            slug=row["slug"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _row_collection(row: sqlite3.Row) -> Collection:
        return Collection(
            id=row["id"],
            workspace_id=row["workspace_id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            slug=row["slug"],
            description=row["description"] or "",
            document_count=row["document_count"],
            indexed_count=row["indexed_count"],
            status=row["status"],
            kb_path=row["kb_path"],
            vector_path=row["vector_path"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _row_document(row: sqlite3.Row) -> DocumentRecord:
        return DocumentRecord(
            id=row["id"],
            collection_id=row["collection_id"],
            title=row["title"],
            source_type=row["source_type"],
            source_uri=row["source_uri"] or "",
            file_path=row["file_path"],
            status=row["status"],
            doc_type=row["doc_type"] or "documentation",
            category=row["category"] or "",
            created_at=row["created_at"],
            indexed_at=row["indexed_at"],
        )

    @staticmethod
    def _row_job(row: sqlite3.Row) -> JobRecord:
        return JobRecord(
            id=row["id"],
            tenant_id=row["tenant_id"],
            collection_id=row["collection_id"],
            job_type=row["job_type"],
            status=row["status"],
            progress=row["progress"],
            message=row["message"] or "",
            payload=json.loads(row["payload_json"] or "{}"),
            result=json.loads(row["result_json"] or "{}"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            completed_at=row["completed_at"],
        )
