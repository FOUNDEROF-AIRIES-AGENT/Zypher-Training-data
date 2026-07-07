"""Improved platform API tests with isolated store."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from coltex_platform.app import create_app
from coltex_platform.store import PlatformStore


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    import coltex_platform.app as app_module
    import coltex_platform.config as cfg_module

    store = PlatformStore(db_path)
    tenant = store.create_tenant("Test", "pytest@coltex.test", "enterprise")
    ws = store.create_workspace(tenant.id, "Test WS", "test")
    raw_key = store.generate_api_key("ctx_")
    store.create_api_key(tenant.id, "test", raw_key, "ctx_")

    app_module._store = store
    app_module._config = cfg_module.load_config()
    app_module._brain_manager = None
    app_module._ingestion = None
    app_module._job_runner = None
    app_module._llm = None

    yield create_app(), raw_key, tenant.id, ws.id


@pytest.fixture
def client(app_env):
    app, _, _, _ = app_env
    return TestClient(app)


@pytest.fixture
def auth_headers(app_env):
    _, key, _, _ = app_env
    return {"X-API-Key": key}


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_me(client, auth_headers):
    resp = client.get("/v1/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "pytest@coltex.test"


def test_collection_lifecycle(client, auth_headers, app_env):
    _, _, _, ws_id = app_env
    resp = client.post(
        f"/v1/workspaces/{ws_id}/collections",
        headers=auth_headers,
        json={"name": "Docs", "slug": "docs", "description": "Test"},
    )
    assert resp.status_code == 201
    col_id = resp.json()["id"]

    resp = client.post(
        f"/v1/collections/{col_id}/documents/text",
        headers=auth_headers,
        json={"title": "Hello", "content": "Coltex RAG platform test document about retrieval."},
    )
    assert resp.status_code == 201

    resp = client.post(
        f"/v1/collections/{col_id}/index",
        headers=auth_headers,
        json={"force_reindex": True},
    )
    assert resp.status_code == 202
