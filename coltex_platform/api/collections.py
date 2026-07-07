"""Workspace and collection management routes."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from coltex_platform.auth import AuthContext, require_auth
from coltex_platform.schemas import CollectionCreate, CollectionResponse, WorkspaceCreate, WorkspaceResponse
from coltex_platform.store import PlatformStore

router = APIRouter(prefix="/v1", tags=["Collections"])


def _store() -> PlatformStore:
    from coltex_platform.app import get_platform_store

    return get_platform_store()


def _config() -> dict:
    from coltex_platform.app import get_platform_config

    return get_platform_config()


def _check_collection_limit(ctx: AuthContext, store: PlatformStore, config: dict) -> None:
    limits = config.get("tiers", {}).get(ctx.tenant.tier, {})
    max_cols = limits.get("collections", 1)
    if max_cols < 0:
        return
    existing = store.list_collections(ctx.tenant.id)
    if len(existing) >= max_cols:
        raise HTTPException(
            status_code=403,
            detail=f"Collection limit reached for tier '{ctx.tenant.tier}' ({max_cols})",
        )


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    body: WorkspaceCreate,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> WorkspaceResponse:
    ws = store.create_workspace(ctx.tenant.id, body.name, body.slug)
    return WorkspaceResponse(id=ws.id, name=ws.name, slug=ws.slug, created_at=ws.created_at)


@router.get("/workspaces", response_model=list[WorkspaceResponse])
async def list_workspaces(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> list[WorkspaceResponse]:
    return [
        WorkspaceResponse(id=w.id, name=w.name, slug=w.slug, created_at=w.created_at)
        for w in store.list_workspaces(ctx.tenant.id)
    ]


@router.post(
    "/workspaces/{workspace_id}/collections",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_collection(
    workspace_id: str,
    body: CollectionCreate,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
) -> CollectionResponse:
    ws = store.get_workspace(workspace_id, ctx.tenant.id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    _check_collection_limit(ctx, store, config)

    data_dir = Path(config.get("storage", {}).get("data_dir", "data/platform"))
    kb_path = str(data_dir / "tenants" / ctx.tenant.id / "collections" / body.slug / "kb")
    vector_path = str(data_dir / "tenants" / ctx.tenant.id / "collections" / body.slug / "vectors")
    Path(kb_path).mkdir(parents=True, exist_ok=True)
    Path(vector_path).mkdir(parents=True, exist_ok=True)

    col = store.create_collection(
        workspace_id=ws.id,
        tenant_id=ctx.tenant.id,
        name=body.name,
        slug=body.slug,
        kb_path=kb_path,
        vector_path=vector_path,
        description=body.description,
    )
    return _collection_response(col)


@router.get("/collections", response_model=list[CollectionResponse])
async def list_collections(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    workspace_id: str | None = None,
) -> list[CollectionResponse]:
    return [_collection_response(c) for c in store.list_collections(ctx.tenant.id, workspace_id)]


@router.get("/collections/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: str,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> CollectionResponse:
    col = store.get_collection(collection_id, ctx.tenant.id)
    if not col:
        raise HTTPException(status_code=404, detail="Collection not found")
    return _collection_response(col)


def _collection_response(col) -> CollectionResponse:
    return CollectionResponse(
        id=col.id,
        workspace_id=col.workspace_id,
        name=col.name,
        slug=col.slug,
        description=col.description,
        document_count=col.document_count,
        indexed_count=col.indexed_count,
        status=col.status,
        created_at=col.created_at,
        updated_at=col.updated_at,
    )
