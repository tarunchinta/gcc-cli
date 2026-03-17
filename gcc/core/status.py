from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from gcc.core.utils import find_gcc_root, read_head
from gcc.models.commit import Commit
from gcc.models.workspace import WorkspaceConfig

console = Console()


def run_status(gcc_root: Path | None = None) -> None:
    """Display current branch, HEAD commit, and dirty state."""
    root = gcc_root or find_gcc_root()
    config = WorkspaceConfig.read(root / "config")
    branch = config.current_branch
    head_hash = read_head(root)

    dirty = _is_dirty(root, branch, head_hash)

    status_icon = "[red bold]* modified[/]" if dirty else "[green bold]clean[/]"

    commit_display = f"[cyan bold]{head_hash}[/]" if head_hash else "[dim]none[/]"
    message_display = ""
    if head_hash:
        commit_file = root / "commits" / f"{head_hash}.json"
        if commit_file.exists():
            commit = Commit.from_file(commit_file)
            message_display = f'\n  Message : "{commit.message}"'

    console.print(
        Panel(
            f"  Branch  : [yellow]{branch}[/]\n"
            f"  HEAD    : {commit_display}{message_display}\n"
            f"  Status  : {status_icon}",
            title="[bold]GCC Status[/]",
            border_style="blue",
        )
    )


def _is_dirty(root: Path, branch: str, head_hash: str | None) -> bool:
    """Check if commit.md has changed since the last commit."""
    context_file = root / "branches" / branch / "commit.md"
    if not context_file.exists():
        return False
    if not head_hash:
        return True

    snapshot_file = root / "snapshots" / head_hash / "context.md"
    if not snapshot_file.exists():
        return True

    current = context_file.read_text(encoding="utf-8")
    snapped = snapshot_file.read_text(encoding="utf-8")
    return current != snapped
