"""Pydantic request/response schemas for Coltex Platform API."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    code: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str = "coltex-platform"


class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    tier: Literal["free", "starter", "professional", "enterprise"] = "free"


class TenantResponse(BaseModel):
    id: str
    name: str
    email: str
    tier: str
    created_at: str


class ApiKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class ApiKeyResponse(BaseModel):
    id: str
    name: str
    prefix: str
    created_at: str
    last_used_at: str | None = None
    scopes: list[str]


class ApiKeyCreatedResponse(ApiKeyResponse):
    key: str


class WorkspaceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    created_at: str


class CollectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=80, pattern=r"^[a-z0-9-]+$")
    description: str = ""


class CollectionResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    slug: str
    description: str
    document_count: int
    indexed_count: int
    status: str
    created_at: str
    updated_at: str


class DocumentResponse(BaseModel):
    id: str
    collection_id: str
    title: str
    source_type: str
    source_uri: str
    status: str
    doc_type: str
    category: str
    created_at: str
    indexed_at: str | None = None


class TextIngestRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    doc_type: str = "documentation"
    category: str = ""
    tags: list[str] = Field(default_factory=list)


class UrlIngestRequest(BaseModel):
    url: str = Field(..., min_length=8)
    title: str | None = None
    doc_type: str = "documentation"
    category: str = ""


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    top_k: int = Field(default=8, ge=1, le=50)
    include_context: bool = True
    filters: dict[str, Any] = Field(default_factory=dict)


class RetrievedDocument(BaseModel):
    id: str
    title: str
    score: float
    source: str
    doc_type: str
    category: str
    snippet: str


class RetrieveResponse(BaseModel):
    query: str
    collection_id: str
    documents: list[RetrievedDocument]
    context: str | None = None


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)
    collection_id: str | None = None
    stream: bool = False
    top_k: int = Field(default=8, ge=1, le=50)
    temperature: float | None = None
    max_tokens: int | None = None


class ChatCitation(BaseModel):
    document_id: str
    title: str
    score: float
    source: str


class ChatResponse(BaseModel):
    id: str
    model: str
    message: ChatMessage
    citations: list[ChatCitation]
    usage: dict[str, int]


class JobResponse(BaseModel):
    id: str
    collection_id: str
    job_type: str
    status: str
    progress: float
    message: str
    result: dict[str, Any]
    created_at: str
    updated_at: str
    completed_at: str | None = None


class IndexRequest(BaseModel):
    force_reindex: bool = False


class UsageResponse(BaseModel):
    tier: str
    today: dict[str, int]
    limits: dict[str, int]


class PlatformStatsResponse(BaseModel):
    tenants: int
    collections: int
    documents: int
    jobs_completed: int
