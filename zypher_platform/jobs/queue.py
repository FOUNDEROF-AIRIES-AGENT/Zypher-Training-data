"""Background job queue for indexing and corpus generation."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    id: str
    type: str
    params: dict[str, Any] = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    result: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    created_at: str = ""
    updated_at: str = ""


class JobQueue:
    def __init__(self, queue_dir: str = "data/platform/jobs"):
        self.dir = Path(queue_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, job_type: str, params: dict[str, Any] | None = None) -> Job:
        job = Job(
            id=str(uuid.uuid4()),
            type=job_type,
            params=params or {},
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._write(job)
        return job

    def get(self, job_id: str) -> Job | None:
        path = self.dir / f"{job_id}.json"
        if not path.exists():
            return None
        return self._read(json.loads(path.read_text(encoding="utf-8")))

    def update(self, job: Job, status: JobStatus, result: dict | None = None, error: str = "") -> Job:
        job.status = status
        job.updated_at = datetime.now(timezone.utc).isoformat()
        if result:
            job.result = result
        if error:
            job.error = error
        self._write(job)
        return job

    def list_jobs(self, limit: int = 50) -> list[Job]:
        jobs = []
        for path in sorted(self.dir.glob("*.json"), reverse=True)[:limit]:
            jobs.append(self._read(json.loads(path.read_text(encoding="utf-8"))))
        return jobs

    def _write(self, job: Job) -> None:
        (self.dir / f"{job.id}.json").write_text(
            json.dumps({
                "id": job.id,
                "type": job.type,
                "params": job.params,
                "status": job.status.value,
                "result": job.result,
                "error": job.error,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
            }, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _read(data: dict) -> Job:
        return Job(
            id=data["id"],
            type=data["type"],
            params=data.get("params", {}),
            status=JobStatus(data.get("status", "pending")),
            result=data.get("result", {}),
            error=data.get("error", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )
