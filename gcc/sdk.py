"""GCC Python SDK — programmatic access to GCC workspaces."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Optional

from gcc.core.commit import run_commit
from gcc.core.init import run_init
from gcc.core.utils import find_gcc_root, read_head, GCC_DIR
from gcc.models.commit import Commit
from gcc.models.workspace import WorkspaceConfig


class GCCClient:
    """High-level API for interacting with a GCC workspace."""

    def __init__(self, workspace_path: str = "."):
        self._workspace = Path(workspace_path).resolve()
        self._gcc_root = self._workspace / GCC_DIR
        if not self._gcc_root.is_dir():
            self._gcc_root = run_init(self._workspace)

    @property
    def root(self) -> Path:
        return self._gcc_root

    def commit(self, message: str, context: str) -> str:
        """Write *context* to the active branch's commit.md, then commit.

        Returns the commit hash.
        """
        config = WorkspaceConfig.read(self._gcc_root / "config")
        branch_dir = self._gcc_root / "branches" / config.current_branch
        branch_dir.mkdir(parents=True, exist_ok=True)
        (branch_dir / "commit.md").write_text(context, encoding="utf-8")

        c = run_commit(message, gcc_root=self._gcc_root)
        return c.hash

    def get_context(self, commit_hash: Optional[str] = None) -> str:
        """Return the context content for *commit_hash* (or HEAD if None)."""
        target = commit_hash or read_head(self._gcc_root)
        if not target:
            return ""
        snapshot = self._gcc_root / "snapshots" / target / "context.md"
        if not snapshot.exists():
            return ""
        return snapshot.read_text(encoding="utf-8")

    def get_log(self) -> list[dict]:
        """Return the commit chain from HEAD as a list of dicts."""
        current = read_head(self._gcc_root)
        result: list[dict] = []
        visited: set[str] = set()
        while current and current not in visited:
            visited.add(current)
            commit_file = self._gcc_root / "commits" / f"{current}.json"
            if not commit_file.exists():
                break
            c = Commit.from_file(commit_file)
            result.append(asdict(c))
            current = c.parent
        return result
