"""Document ingestion and indexing routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from coltex_platform.auth import AuthContext, require_auth
from coltex_platform.schemas import (
    DocumentResponse,
    IndexRequest,
    JobResponse,
    TextIngestRequest,
    UrlIngestRequest,
)
from coltex_platform.store import PlatformStore

router = APIRouter(prefix="/v1/collections/{collection_id}", tags=["Ingestion"])


def _store() -> PlatformStore:
    from coltex_platform.app import get_platform_store

    return get_platform_store()


def _config() -> dict:
    from coltex_platform.app import get_platform_config

    return get_platform_config()


def _ingestion():
    from coltex_platform.app import get_ingestion_service

    return get_ingestion_service()


def _jobs():
    from coltex_platform.app import get_job_runner

    return get_job_runner()


def _get_collection_or_404(collection_id: str, ctx: AuthContext, store: PlatformStore):
    col = store.get_collection(collection_id, ctx.tenant.id)
    if not col:
        raise HTTPException(status_code=404, detail="Collection not found")
    return col


@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents(
    collection_id: str,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> list[DocumentResponse]:
    _get_collection_or_404(collection_id, ctx, store)
    return [_doc_response(d) for d in store.list_documents(collection_id)]


@router.post("/documents/text", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def ingest_text(
    collection_id: str,
    body: TextIngestRequest,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    ingestion=Depends(_ingestion),
) -> DocumentResponse:
    col = _get_collection_or_404(collection_id, ctx, store)
    record = ingestion.ingest_text(
        col, body.title, body.content, body.doc_type, body.category, body.tags
    )
    store.increment_usage(ctx.tenant.id, "ingest")
    store.update_collection_counts(collection_id, len(store.list_documents(collection_id)), col.indexed_count)
    return _doc_response(record)


@router.post("/documents/url", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def ingest_url(
    collection_id: str,
    body: UrlIngestRequest,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    ingestion=Depends(_ingestion),
) -> DocumentResponse:
    col = _get_collection_or_404(collection_id, ctx, store)
    try:
        record = ingestion.ingest_url(col, body.url, body.title, body.doc_type, body.category)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    store.increment_usage(ctx.tenant.id, "ingest")
    store.update_collection_counts(collection_id, len(store.list_documents(collection_id)), col.indexed_count)
    return _doc_response(record)


@router.post("/documents/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    collection_id: str,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
    ingestion=Depends(_ingestion),
    file: UploadFile = File(...),
    doc_type: str = "documentation",
    category: str = "",
) -> DocumentResponse:
    col = _get_collection_or_404(collection_id, ctx, store)
    max_bytes = int(config.get("ingestion", {}).get("max_upload_bytes", 52_428_800))
    data = await file.read()
    if len(data) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds {max_bytes} bytes")
    allowed = config.get("ingestion", {}).get("allowed_extensions", [".md", ".txt"])
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ".txt"
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Extension {ext} not allowed")
    record = ingestion.ingest_file(col, file.filename or "upload.txt", data, doc_type=doc_type, category=category)
    store.increment_usage(ctx.tenant.id, "ingest")
    store.update_collection_counts(collection_id, len(store.list_documents(collection_id)), col.indexed_count)
    return _doc_response(record)


@router.post("/index", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_index(
    collection_id: str,
    body: IndexRequest,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    job_runner=Depends(_jobs),
) -> JobResponse:
    _get_collection_or_404(collection_id, ctx, store)
    job_id = job_runner.enqueue_index(ctx.tenant.id, collection_id, force=body.force_reindex)
    job = store.get_job(job_id, ctx.tenant.id)
    return _job_response(job)


@router.get("/jobs", response_model=list[JobResponse])
async def list_jobs(
    collection_id: str,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> list[JobResponse]:
    _get_collection_or_404(collection_id, ctx, store)
    return [_job_response(j) for j in store.list_jobs(ctx.tenant.id, collection_id)]


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    collection_id: str,
    job_id: str,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> JobResponse:
    _get_collection_or_404(collection_id, ctx, store)
    job = store.get_job(job_id, ctx.tenant.id)
    if not job or job.collection_id != collection_id:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_response(job)


def _doc_response(doc) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        collection_id=doc.collection_id,
        title=doc.title,
        source_type=doc.source_type,
        source_uri=doc.source_uri,
        status=doc.status,
        doc_type=doc.doc_type,
        category=doc.category,
        created_at=doc.created_at,
        indexed_at=doc.indexed_at,
    )


def _job_response(job) -> JobResponse:
    return JobResponse(
        id=job.id,
        collection_id=job.collection_id,
        job_type=job.job_type,
        status=job.status,
        progress=job.progress,
        message=job.message,
        result=job.result,
        created_at=job.created_at,
        updated_at=job.updated_at,
        completed_at=job.completed_at,
    )
