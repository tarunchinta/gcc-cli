"""Generic adapter — a thin wrapper any agent framework can use."""
from __future__ import annotations

from typing import Optional

from gcc.sdk import GCCClient


class GCCAdapter:
    """Minimal wrapper around GCCClient for easy agent integration."""

    def __init__(self, workspace_path: str = "."):
        self._client = GCCClient(workspace_path)

    def save(self, message: str, context: str) -> str:
        """Save agent context as a new commit. Returns the commit hash."""
        return self._client.commit(message, context)

    def load(self, commit_hash: Optional[str] = None) -> str:
        """Load context from a specific commit (or latest)."""
        return self._client.get_context(commit_hash)

    def history(self) -> list[dict]:
        """Return full commit history as list of dicts."""
        return self._client.get_log()
