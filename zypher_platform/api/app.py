"""Zypher Platform REST API."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from zypher_platform.core import ZypherPlatform

platform = ZypherPlatform()
app = FastAPI(
    title="Zypher Platform",
    description="Brain-first enterprise AI platform — knowledge in Zypher Brain, LLM as reasoning engine",
    version="1.0.0",
)

if platform.config.get("cors", {}).get("enabled", True):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=platform.config.get("cors", {}).get("origins", ["*"]),
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- Request models ---

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 8


class DocumentRequest(BaseModel):
    title: str
    content: str
    doc_type: str = "documentation"
    category: str = "general"
    filename: str | None = None


class JobRequest(BaseModel):
    force: bool = False


class GenerateJobRequest(BaseModel):
    mega_multiplier: int = 1
    max_files: int = 10000


# --- Routes ---

@app.get("/health")
def health():
    return platform.health()


@app.get("/v1/stats")
def stats():
    return platform.stats()


@app.post("/v1/chat")
def chat(req: ChatRequest):
    return platform.chat(req.message, session_id=req.session_id)


@app.post("/v1/retrieve")
def retrieve(req: RetrieveRequest):
    result = platform.retrieve(req.query)
    return {
        "query": req.query,
        "documents": [
            {
                "title": s.document.title,
                "path": s.document.path,
                "doc_type": s.document.doc_type,
                "category": s.document.category,
                "score": s.score,
                "source": s.source,
                "preview": s.document.content[:500],
            }
            for s in result.documents[: req.top_k]
        ],
        "context": result.context,
    }


@app.post("/v1/documents")
def ingest_document(req: DocumentRequest):
    return platform.ingest_document(
        req.title, req.content, req.doc_type, req.category, req.filename
    )


@app.post("/v1/index")
def index_brain(req: JobRequest):
    job_id = platform.enqueue_index(force=req.force)
    return {"job_id": job_id, "status": "enqueued"}


@app.post("/v1/generate")
def generate_corpus(req: GenerateJobRequest):
    job_id = platform.enqueue_generate(req.mega_multiplier, req.max_files)
    return {"job_id": job_id, "status": "enqueued"}


@app.get("/v1/jobs/{job_id}")
def get_job(job_id: str):
    job = platform.jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "id": job.id,
        "type": job.type,
        "status": job.status.value,
        "result": job.result,
        "error": job.error,
    }


@app.post("/v1/jobs/{job_id}/run")
def run_job(job_id: str):
    return platform.run_job(job_id)


@app.post("/v1/sessions")
def create_session():
    session = platform.sessions.create()
    return {"session_id": session.id}


@app.get("/v1/sessions")
def list_sessions():
    return platform.sessions.list_sessions()


@app.get("/v1/sessions/{session_id}")
def get_session(session_id: str):
    session = platform.sessions.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return {"id": session.id, "messages": session.messages, "updated_at": session.updated_at}
