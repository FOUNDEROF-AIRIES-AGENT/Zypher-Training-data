"""Tenant and API key management routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from coltex_platform.auth import AuthContext, require_auth
from coltex_platform.schemas import (
    ApiKeyCreate,
    ApiKeyCreatedResponse,
    ApiKeyResponse,
    TenantCreate,
    TenantResponse,
    UsageResponse,
)
from coltex_platform.store import PlatformStore

router = APIRouter(prefix="/v1", tags=["Tenants"])


def _store() -> PlatformStore:
    from coltex_platform.app import get_platform_store

    return get_platform_store()


def _config() -> dict:
    from coltex_platform.app import get_platform_config

    return get_platform_config()


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(body: TenantCreate, store: Annotated[PlatformStore, Depends(_store)]) -> TenantResponse:
    if store.get_tenant_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    tenant = store.create_tenant(body.name, body.email, body.tier)
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        email=tenant.email,
        tier=tenant.tier,
        created_at=tenant.created_at,
    )


@router.get("/me", response_model=TenantResponse)
async def get_me(ctx: Annotated[AuthContext, Depends(require_auth)]) -> TenantResponse:
    t = ctx.tenant
    return TenantResponse(id=t.id, name=t.name, email=t.email, tier=t.tier, created_at=t.created_at)


@router.get("/me/usage", response_model=UsageResponse)
async def get_usage(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
) -> UsageResponse:
    tier_limits = config.get("tiers", {}).get(ctx.tenant.tier, {})
    return UsageResponse(
        tier=ctx.tenant.tier,
        today=store.get_usage_today(ctx.tenant.id),
        limits={
            "queries_per_day": tier_limits.get("queries_per_day", 500),
            "documents": tier_limits.get("documents", 1000),
            "collections": tier_limits.get("collections", 1),
        },
    )


@router.post("/api-keys", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    body: ApiKeyCreate,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
) -> ApiKeyCreatedResponse:
    prefix = config.get("auth", {}).get("api_key_prefix", "ctx_")
    raw = store.generate_api_key(prefix)
    record = store.create_api_key(ctx.tenant.id, body.name, raw, prefix[:4])
    return ApiKeyCreatedResponse(
        id=record.id,
        name=record.name,
        prefix=record.prefix,
        created_at=record.created_at,
        scopes=record.scopes,
        key=raw,
    )


@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
) -> list[ApiKeyResponse]:
    return [
        ApiKeyResponse(
            id=k.id,
            name=k.name,
            prefix=k.prefix,
            created_at=k.created_at,
            last_used_at=k.last_used_at,
            scopes=k.scopes,
        )
        for k in store.list_api_keys(ctx.tenant.id)
    ]
