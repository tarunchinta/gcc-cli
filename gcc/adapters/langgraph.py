"""LangGraph-compatible checkpointer backed by GCC.

This provides a checkpointer interface that LangGraph agents can use
to persist and restore reasoning state through GCC's commit system.
"""
from __future__ import annotations

from typing import Any, Optional

from gcc.sdk import GCCClient


class GCCCheckpointer:
    """A LangGraph-style checkpointer that stores state in a GCC workspace.

    Usage with LangGraph::

        from gcc.adapters.langgraph import GCCCheckpointer

        checkpointer = GCCCheckpointer(workspace_path=".")
        # Use as your graph's checkpointer
    """

    def __init__(self, workspace_path: str = "."):
        self._client = GCCClient(workspace_path)

    def put(self, config: dict[str, Any], state: dict[str, Any], metadata: Optional[dict] = None) -> str:
        """Persist a LangGraph checkpoint.

        Parameters
        ----------
        config : dict
            LangGraph config dict, must contain ``configurable.thread_id``.
        state : dict
            The full graph state to checkpoint.
        metadata : dict, optional
            Extra metadata (ignored for now, reserved for future use).

        Returns
        -------
        str
            The GCC commit hash for this checkpoint.
        """
        import json

        thread_id = config.get("configurable", {}).get("thread_id", "default")
        context = json.dumps({"thread_id": thread_id, "state": state}, indent=2)
        message = f"checkpoint:{thread_id}"
        return self._client.commit(message, context)

    def get(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Retrieve the latest checkpoint for the given config.

        Returns the deserialized state dict, or None if no checkpoint exists.
        """
        import json

        content = self._client.get_context()
        if not content:
            return None
        try:
            data = json.loads(content)
            return data.get("state")
        except (json.JSONDecodeError, AttributeError):
            return None

    def list(self, config: dict[str, Any]) -> list[dict[str, Any]]:
        """Return all checkpoints as a list of commit metadata dicts."""
        return self._client.get_log()
