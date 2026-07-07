#!/usr/bin/env python3
"""Example Coltex Platform API client."""

from __future__ import annotations

import json
import os
import sys

try:
    import httpx
except ImportError:
    print("pip install httpx")
    sys.exit(1)

BASE = os.environ.get("COLTEX_API_URL", "http://localhost:8080")
KEY = os.environ.get("COLTEX_API_KEY", "")


def main() -> None:
    if not KEY:
        key_file = "data/platform/DEMO_API_KEY.txt"
        if os.path.exists(key_file):
            for line in open(key_file):
                if line.startswith("ctx_"):
                    KEY = line.strip()
                    break
        if not KEY:
            print("Set COLTEX_API_KEY or start platform to generate demo key")
            sys.exit(1)

    headers = {"X-API-Key": KEY, "Content-Type": "application/json"}
    client = httpx.Client(base_url=BASE, headers=headers, timeout=60.0)

    me = client.get("/v1/me").json()
    print("Tenant:", json.dumps(me, indent=2))

    workspaces = client.get("/v1/workspaces").json()
    if not workspaces:
        ws = client.post("/v1/workspaces", json={"name": "Demo", "slug": "demo"}).json()
        workspaces = [ws]
    ws_id = workspaces[0]["id"]

    collections = client.get("/v1/collections").json()
    if not collections:
        col = client.post(
            f"/v1/workspaces/{ws_id}/collections",
            json={"name": "Knowledge", "slug": "knowledge", "description": "Demo collection"},
        ).json()
        collections = [col]

        client.post(
            f"/v1/collections/{col['id']}/documents/text",
            json={
                "title": "Coltex RAG Overview",
                "content": "Coltex is an enterprise RAG-as-a-Service platform with hybrid retrieval.",
                "doc_type": "documentation",
                "category": "rag",
            },
        )
        job = client.post(f"/v1/collections/{col['id']}/index", json={"force_reindex": True}).json()
        print("Index job:", job["id"], job["status"])

    col_id = collections[0]["id"]
    result = client.post(
        f"/v1/collections/{col_id}/retrieve",
        json={"query": "What is Coltex RAG?", "top_k": 5, "include_context": True},
    ).json()
    print("\nRetrieve results:")
    for doc in result.get("documents", []):
        print(f"  - {doc['title']} ({doc['score']:.2f})")

    chat = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "What is Coltex?"}],
            "collection_id": col_id,
        },
    ).json()
    print("\nChat:", chat["message"]["content"][:500])


if __name__ == "__main__":
    main()
