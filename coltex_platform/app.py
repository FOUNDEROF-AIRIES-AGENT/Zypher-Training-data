"""Coltex RAG-as-a-Service FastAPI application."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from platform import __version__
from coltex_platform.api.collections import router as collections_router
from coltex_platform.api.health import router as health_router
from coltex_platform.api.ingestion import router as ingestion_router
from coltex_platform.api.rag import router as rag_router
from coltex_platform.api.tenants import router as tenants_router
from coltex_platform.config import load_config
from coltex_platform.services.brain_manager import BrainManager
from coltex_platform.services.ingestion import IngestionService
from coltex_platform.services.jobs import JobRunner
from coltex_platform.services.llm import LLMService
from coltex_platform.store import PlatformStore

_store: PlatformStore | None = None
_config: dict | None = None
_brain_manager: BrainManager | None = None
_ingestion: IngestionService | None = None
_job_runner: JobRunner | None = None
_llm: LLMService | None = None


def get_platform_config() -> dict:
    global _config
    if _config is None:
        _config = load_config()
    return _config


def get_platform_store() -> PlatformStore:
    global _store
    if _store is None:
        cfg = get_platform_config()
        db_path = cfg.get("storage", {}).get("sqlite_path", "data/platform/coltex.db")
        _store = PlatformStore(db_path)
    return _store


def get_brain_manager() -> BrainManager:
    global _brain_manager
    if _brain_manager is None:
        cfg = get_platform_config()
        _brain_manager = BrainManager(
            get_platform_store(),
            base_config_path=cfg.get("brain", {}).get("config_path", "config/brain.yaml"),
        )
    return _brain_manager


def get_ingestion_service() -> IngestionService:
    global _ingestion
    if _ingestion is None:
        cfg = get_platform_config()
        ing = cfg.get("ingestion", {})
        _ingestion = IngestionService(
            get_platform_store(),
            chunk_size=int(ing.get("chunk_size", 1200)),
            chunk_overlap=int(ing.get("chunk_overlap", 150)),
        )
    return _ingestion


def get_job_runner() -> JobRunner:
    global _job_runner
    if _job_runner is None:
        cfg = get_platform_config()
        jobs_cfg = cfg.get("jobs", {})
        _job_runner = JobRunner(
            get_platform_store(),
            get_brain_manager(),
            get_ingestion_service(),
            max_concurrent=int(jobs_cfg.get("max_concurrent", 4)),
            poll_interval=float(jobs_cfg.get("poll_interval_seconds", 2)),
        )
    return _job_runner


def get_llm_service() -> LLMService:
    global _llm
    if _llm is None:
        _llm = LLMService(get_platform_config())
    return _llm


def _seed_demo_tenant(store: PlatformStore, config: dict) -> None:
    """Create a demo tenant with API key on first boot (development only)."""
    if store.get_tenant_by_email("demo@coltex.ai"):
        return
    tenant = store.create_tenant("Coltex Demo", "demo@coltex.ai", "enterprise")
    store.create_workspace(tenant.id, "Default Workspace", "default")
    prefix = config.get("auth", {}).get("api_key_prefix", "ctx_")
    raw_key = store.generate_api_key(prefix)
    store.create_api_key(tenant.id, "Demo Key", raw_key, prefix[:4])
    key_file = Path(config.get("storage", {}).get("data_dir", "data/platform")) / "DEMO_API_KEY.txt"
    key_file.parent.mkdir(parents=True, exist_ok=True)
    key_file.write_text(
        f"Coltex Demo API Key (save this — shown once at bootstrap):\n\n{raw_key}\n",
        encoding="utf-8",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = get_platform_config()
    store = get_platform_store()
    _seed_demo_tenant(store, cfg)
    runner = get_job_runner()
    runner.start()
    yield
    runner.stop()


def create_app() -> FastAPI:
    cfg = get_platform_config()
    app = FastAPI(
        title="Coltex RAG-as-a-Service",
        description=(
            "Enterprise retrieval-augmented generation platform. "
            "Multi-tenant collections, hybrid retrieval, ingestion pipelines, and RAG chat."
        ),
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    origins = cfg.get("server", {}).get("cors_origins", ["*"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(tenants_router)
    app.include_router(collections_router)
    app.include_router(ingestion_router)
    app.include_router(rag_router)
    return app


app = create_app()
