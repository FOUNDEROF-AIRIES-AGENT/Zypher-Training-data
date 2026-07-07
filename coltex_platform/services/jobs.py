"""Background job runner for indexing and bulk ingestion."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from coltex_platform.services.brain_manager import BrainManager
    from coltex_platform.services.ingestion import IngestionService
    from coltex_platform.store import PlatformStore


class JobRunner:
    def __init__(
        self,
        store: PlatformStore,
        brain_manager: BrainManager,
        ingestion: IngestionService,
        max_concurrent: int = 4,
        poll_interval: float = 2.0,
    ):
        self.store = store
        self.brain_manager = brain_manager
        self.ingestion = ingestion
        self.max_concurrent = max_concurrent
        self.poll_interval = poll_interval
        self._handlers: dict[str, Callable[[str], None]] = {
            "index": self._handle_index,
            "reindex": self._handle_index,
        }
        self._active = 0
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="coltex-jobs")
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    def enqueue_index(self, tenant_id: str, collection_id: str, force: bool = False) -> str:
        job = self.store.create_job(
            tenant_id,
            collection_id,
            "reindex" if force else "index",
            {"force": force},
        )
        return job.id

    def _loop(self) -> None:
        while not self._stop.is_set():
            if self._active >= self.max_concurrent:
                time.sleep(self.poll_interval)
                continue
            job = self._next_queued_job()
            if not job:
                time.sleep(self.poll_interval)
                continue
            handler = self._handlers.get(job.job_type)
            if not handler:
                self.store.update_job(job.id, status="failed", message=f"Unknown job type: {job.job_type}")
                continue
            threading.Thread(
                target=self._run_job,
                args=(job.id, handler),
                daemon=True,
            ).start()

    def _next_queued_job(self):
        jobs = []
        for tenant_jobs in [self.store.list_jobs(tid) for tid in self._tenant_ids()]:
            jobs.extend(tenant_jobs)
        for job in sorted(jobs, key=lambda j: j.created_at):
            if job.status == "queued":
                return job
        return None

    def _tenant_ids(self) -> list[str]:
        # Lightweight scan via jobs table would need a dedicated query; reuse list pattern
        import sqlite3
        from pathlib import Path

        db_path = self.store.db_path
        if not db_path.exists():
            return []
        conn = sqlite3.connect(db_path)
        try:
            rows = conn.execute("SELECT DISTINCT tenant_id FROM jobs WHERE status = 'queued'").fetchall()
            return [r[0] for r in rows]
        finally:
            conn.close()

    def _run_job(self, job_id: str, handler: Callable[[str], None]) -> None:
        with self._lock:
            self._active += 1
        try:
            self.store.update_job(job_id, status="running", progress=0.05, message="Starting")
            handler(job_id)
        except Exception as exc:
            self.store.update_job(job_id, status="failed", message=str(exc), progress=1.0)
        finally:
            with self._lock:
                self._active -= 1

    def _handle_index(self, job_id: str) -> None:
        job = self._get_job_any(job_id)
        if not job:
            return
        collection = self.store.get_collection(job.collection_id, job.tenant_id)
        if not collection:
            self.store.update_job(job_id, status="failed", message="Collection not found")
            return

        force = bool(job.payload.get("force"))
        self.store.update_job(job_id, progress=0.2, message="Loading documents")
        self.brain_manager.invalidate(collection.id)
        self.store.update_job(job_id, progress=0.5, message="Building vector index")
        stats = self.brain_manager.index_collection(collection, force=force)

        for doc in self.store.list_documents(collection.id):
            if doc.status == "pending":
                self.store.mark_document_indexed(doc.id)

        self.store.update_collection_counts(
            collection.id,
            len(self.store.list_documents(collection.id)),
            len(self.store.list_documents(collection.id)),
        )
        self.store.update_job(
            job_id,
            status="completed",
            progress=1.0,
            message="Index build complete",
            result=stats,
        )

    def _get_job_any(self, job_id: str):
        import sqlite3

        conn = sqlite3.connect(self.store.db_path)
        conn.row_factory = sqlite3.Row
        try:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not row:
                return None
            from coltex_platform.store import PlatformStore

            return PlatformStore._row_job(row)
        finally:
            conn.close()
