"""Health and platform status routes."""

from __future__ import annotations

from fastapi import APIRouter

from platform import __version__
from coltex_platform.schemas import HealthResponse, PlatformStatsResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get("/v1/status", response_model=PlatformStatsResponse)
async def platform_status() -> PlatformStatsResponse:
    from coltex_platform.app import get_platform_store

    store = get_platform_store()
    import sqlite3

    conn = sqlite3.connect(store.db_path)
    try:
        tenants = conn.execute("SELECT COUNT(*) FROM tenants").fetchone()[0]
        collections = conn.execute("SELECT COUNT(*) FROM collections").fetchone()[0]
        documents = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE status = 'completed'").fetchone()[0]
    finally:
        conn.close()
    return PlatformStatsResponse(
        tenants=tenants,
        collections=collections,
        documents=documents,
        jobs_completed=jobs,
    )
