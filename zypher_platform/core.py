"""Zypher Platform core — orchestrates Brain, LLM, sessions, jobs, agents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from brain import ZypherBrain
from brain.ingestion.ingest import ingest_file, write_document
from zypher_platform.agents.orchestrator import AgentOrchestrator
from zypher_platform.jobs.queue import JobQueue, JobStatus
from zypher_platform.sessions.store import SessionStore


class ZypherPlatform:
    """
    Complete Zypher platform:

    - Zypher Brain (knowledge)
    - LLM reasoning engine (optional)
    - Session management
    - Job queue (index, generate)
    - Agent orchestration
    """

    def __init__(self, config_path: str | Path = "config/platform.yaml"):
        with Path(config_path).open(encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        brain_cfg_path = self.config["brain"]["config"]
        with Path(brain_cfg_path).open(encoding="utf-8") as f:
            brain_cfg = yaml.safe_load(f)

        self.brain = ZypherBrain(config=brain_cfg, config_path=brain_cfg_path)
        self._llm_cfg = None
        self.llm = None
        self.tools = None

        if self.config.get("llm", {}).get("enabled", True):
            with Path(self.config["llm"]["config"]).open(encoding="utf-8") as f:
                self._llm_cfg = yaml.safe_load(f)

        sess_cfg = self.config.get("sessions", {})
        self.sessions = SessionStore(sess_cfg.get("persist_dir", "data/platform/sessions"))

        jobs_cfg = self.config.get("jobs", {})
        self.jobs = JobQueue(jobs_cfg.get("queue_dir", "data/platform/jobs"))

        agent_cfg = self.config.get("agents", {})
        self.agents = AgentOrchestrator(
            self.brain,
            tools=self.tools,
            max_rounds=int(agent_cfg.get("max_tool_rounds", 3)),
        )

    def _ensure_llm(self) -> None:
        if self.llm is None and self._llm_cfg:
            from zypher.llm.provider import LLMProvider
            from zypher.tools import ToolRegistry

            self.llm = LLMProvider.from_config(self._llm_cfg)
            self.tools = ToolRegistry.default(self.brain)
            self.agents.tools = self.tools

    # --- Brain operations ---

    def index_brain(self, force: bool = False) -> int:
        return self.brain.index(force=force)

    def retrieve(self, query: str):
        return self.brain.retrieve(query)

    def ingest_document(
        self,
        title: str,
        content: str,
        doc_type: str = "documentation",
        category: str = "general",
        filename: str | None = None,
    ) -> dict[str, Any]:
        """Add a document to the brain without retraining."""
        safe_name = (filename or title.lower().replace(" ", "_")[:60]) + ".md"
        path = Path("knowledge-base/custom") / safe_name
        doc = write_document(path, title, content, doc_type=doc_type, category=category)
        ingest_file(self.brain, path, reindex=True)
        return {"id": doc.doc_id, "path": doc.path, "title": doc.title}

    # --- Chat ---

    def chat(self, message: str, session_id: str | None = None) -> dict[str, Any]:
        if session_id:
            history = self.sessions.get_messages(session_id)
            for msg in history:
                if msg not in self.brain.memory.messages:
                    self.brain.memory.messages.append(msg)

        if self._llm_cfg:
            self._ensure_llm()

        if self.llm is None:
            retrieval = self.brain.retrieve(message)
            answer = (
                retrieval.context[:4000]
                if retrieval.has_context
                else "LLM disabled. Use POST /v1/retrieve for brain search."
            )
            sources = [
                {"title": s.document.title, "path": s.document.path, "score": s.score}
                for s in retrieval.documents
            ]
        else:
            result = self.agents.run(message, self.llm.generate)
            answer = result["answer"]
            sources = result["sources"]

        if session_id:
            self.sessions.add_message(session_id, "user", message)
            self.sessions.add_message(session_id, "assistant", answer)

        return {"answer": answer, "session_id": session_id, "sources": sources}

    # --- Jobs ---

    def enqueue_index(self, force: bool = False) -> str:
        job = self.jobs.enqueue("index", {"force": force})
        return job.id

    def enqueue_generate(self, mega_multiplier: int = 1, max_files: int = 10000) -> str:
        job = self.jobs.enqueue("generate", {
            "mega_multiplier": mega_multiplier,
            "max_files": max_files,
        })
        return job.id

    def run_job(self, job_id: str) -> dict[str, Any]:
        job = self.jobs.get(job_id)
        if not job:
            return {"error": "Job not found"}
        self.jobs.update(job, JobStatus.RUNNING)
        try:
            if job.type == "index":
                count = self.index_brain(force=job.params.get("force", False))
                result = {"indexed": count}
            elif job.type == "generate":
                import subprocess
                cmd = [
                    "python3", "scripts/generate_corpus.py",
                    "--mega-multiplier", str(job.params.get("mega_multiplier", 1)),
                    "--max-files", str(job.params.get("max_files", 10000)),
                    "--skip-wiring",
                ]
                subprocess.run(cmd, check=True, cwd=Path.cwd())
                result = {"status": "generated"}
            else:
                raise ValueError(f"Unknown job type: {job.type}")
            self.jobs.update(job, JobStatus.COMPLETED, result=result)
            return {"job_id": job_id, "status": "completed", **result}
        except Exception as exc:
            self.jobs.update(job, JobStatus.FAILED, error=str(exc))
            return {"job_id": job_id, "status": "failed", "error": str(exc)}

    # --- Admin ---

    def stats(self) -> dict[str, Any]:
        admin = self.config.get("admin", {})
        stats: dict[str, Any] = {
            "platform": self.config.get("name", "Zypher Platform"),
            "version": self.config.get("version", "1.0.0"),
            "brain_documents": self.brain.document_count,
            "indexed": self.brain.vector_index.is_indexed,
            "llm_enabled": self._llm_cfg is not None,
            "sessions": len(list(self.sessions.dir.glob("*.json"))),
            "jobs": len(list(self.jobs.dir.glob("*.json"))),
        }
        stats_path = Path(admin.get("stats_path", "knowledge-base/generated/brain_statistics.json"))
        if stats_path.exists():
            stats["brain_statistics"] = json.loads(stats_path.read_text(encoding="utf-8"))
        return stats

    def health(self) -> dict[str, str]:
        return {
            "status": "ok",
            "brain": "ready",
            "llm": "ready" if self.llm else "disabled",
        }
