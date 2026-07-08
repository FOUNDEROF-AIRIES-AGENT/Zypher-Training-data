"""GitHub connector — scan repository metadata (sync stub, ready for webhooks)."""

from __future__ import annotations

from typing import Any

from runtime.connectors.base import Connector


class GitHubConnector(Connector):
    id = "github"
    name = "GitHub"

    def __init__(self, repo: str = "", branch: str = "main"):
        self.repo = repo
        self.branch = branch

    def sync(self) -> dict[str, Any]:
        return {
            "connector": self.id,
            "status": "ready",
            "repo": self.repo or "(configure GITHUB_REPO)",
            "branch": self.branch,
            "message": "GitHub webhook sync available — set repo and enable webhook to runtime ingest",
            "webhook_event": "push",
            "pipeline": [
                "github.push",
                "document.uploaded",
                "chunk.created",
                "embedding.generated",
                "graph.updated",
            ],
        }
