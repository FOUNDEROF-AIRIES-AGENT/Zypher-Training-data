"""Authentication dependencies for Coltex Platform."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from coltex_platform.store import ApiKey, PlatformStore, Tenant

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@dataclass
class AuthContext:
    tenant: Tenant
    api_key: ApiKey | None = None
    auth_method: str = "api_key"


def get_store() -> PlatformStore:
    from coltex_platform.app import get_platform_store

    return get_platform_store()


async def require_auth(
    store: Annotated[PlatformStore, Depends(get_store)],
    bearer: Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)] = None,
    api_key: Annotated[str | None, Security(api_key_header)] = None,
) -> AuthContext:
    raw_key = api_key
    if bearer and bearer.credentials:
        raw_key = bearer.credentials

    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Pass X-API-Key header or Bearer token.",
        )

    verified = store.verify_api_key(raw_key)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key.",
        )

    api_key_record, tenant = verified
    return AuthContext(tenant=tenant, api_key=api_key_record, auth_method="api_key")


def require_scope(scope: str):
    async def _check(ctx: Annotated[AuthContext, Depends(require_auth)]) -> AuthContext:
        if ctx.api_key and scope not in ctx.api_key.scopes and "admin" not in ctx.api_key.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API key missing required scope: {scope}",
            )
        return ctx

    return _check
