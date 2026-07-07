"""Retrieval and RAG chat routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from coltex_platform.auth import AuthContext, require_auth
from coltex_platform.schemas import (
    ChatCitation,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    RetrieveRequest,
    RetrieveResponse,
    RetrievedDocument,
)
from coltex_platform.store import PlatformStore

router = APIRouter(prefix="/v1", tags=["RAG"])


def _store() -> PlatformStore:
    from coltex_platform.app import get_platform_store

    return get_platform_store()


def _config() -> dict:
    from coltex_platform.app import get_platform_config

    return get_platform_config()


def _brain():
    from coltex_platform.app import get_brain_manager

    return get_brain_manager()


def _llm():
    from coltex_platform.app import get_llm_service

    return get_llm_service()


def _check_query_limit(ctx: AuthContext, store: PlatformStore, config: dict, metric: str) -> None:
    limits = config.get("tiers", {}).get(ctx.tenant.tier, {})
    max_q = limits.get("queries_per_day", 500)
    if max_q < 0:
        return
    usage = store.get_usage_today(ctx.tenant.id)
    total = usage.get("retrieve", 0) + usage.get("chat", 0)
    if total >= max_q:
        raise HTTPException(status_code=429, detail="Daily query limit exceeded for your tier")


def _resolve_collection_id(
    collection_id: str | None,
    ctx: AuthContext,
    store: PlatformStore,
    config: dict,
) -> str:
    if collection_id:
        col = store.get_collection(collection_id, ctx.tenant.id)
        if not col:
            raise HTTPException(status_code=404, detail="Collection not found")
        return col.id
    cols = store.list_collections(ctx.tenant.id)
    if not cols:
        default_slug = config.get("brain", {}).get("default_collection", "default")
        raise HTTPException(
            status_code=404,
            detail=f"No collections found. Create a collection or use the bundled '{default_slug}' knowledge base via CLI.",
        )
    return cols[0].id


@router.post("/collections/{collection_id}/retrieve", response_model=RetrieveResponse)
async def retrieve(
    collection_id: str,
    body: RetrieveRequest,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
    brain=Depends(_brain),
) -> RetrieveResponse:
    _check_query_limit(ctx, store, config, "retrieve")
    col = store.get_collection(collection_id, ctx.tenant.id)
    if not col:
        raise HTTPException(status_code=404, detail="Collection not found")

    result = brain.retrieve(col, body.query)
    store.increment_usage(ctx.tenant.id, "retrieve")

    docs = [
        RetrievedDocument(
            id=scored.document.doc_id,
            title=scored.document.title,
            score=scored.score,
            source=scored.source,
            doc_type=scored.document.doc_type,
            category=scored.document.category,
            snippet=scored.document.content[:500],
        )
        for scored in result.documents[: body.top_k]
    ]
    return RetrieveResponse(
        query=body.query,
        collection_id=collection_id,
        documents=docs,
        context=result.context if body.include_context else None,
    )


@router.post("/chat/completions", response_model=ChatResponse)
async def chat_completions(
    body: ChatRequest,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    store: Annotated[PlatformStore, Depends(_store)],
    config: Annotated[dict, Depends(_config)],
    brain=Depends(_brain),
    llm=Depends(_llm),
) -> ChatResponse:
    _check_query_limit(ctx, store, config, "chat")
    collection_id = _resolve_collection_id(body.collection_id, ctx, store, config)
    col = store.get_collection(collection_id, ctx.tenant.id)
    if not col:
        raise HTTPException(status_code=404, detail="Collection not found")

    user_messages = [m.content for m in body.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="At least one user message required")
    query = user_messages[-1]

    retrieval = brain.retrieve(col, query)
    history = [{"role": m.role, "content": m.content} for m in body.messages[:-1]]
    answer, usage = llm.generate(
        query,
        retrieval=retrieval,
        history=history,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )
    store.increment_usage(ctx.tenant.id, "chat")

    citations = [
        ChatCitation(
            document_id=scored.document.doc_id,
            title=scored.document.title,
            score=scored.score,
            source=scored.source,
        )
        for scored in retrieval.documents[: body.top_k]
    ]
    return ChatResponse(
        id=llm.new_chat_id(),
        model=llm.model,
        message=ChatMessage(role="assistant", content=answer),
        citations=citations,
        usage=usage,
    )
