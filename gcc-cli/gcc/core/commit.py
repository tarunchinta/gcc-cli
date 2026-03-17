from __future__ import annotations

from pathlib import Path

from rich.console import Console

from gcc.core.utils import find_gcc_root, generate_hash, now_iso, read_head, write_head
from gcc.models.commit import Commit
from gcc.models.workspace import WorkspaceConfig

console = Console()


def run_commit(message: str, gcc_root: Path | None = None) -> Commit:
    """Create a new commit with *message*.

    Reads the current context from the active branch's commit.md, snapshots it,
    writes the commit JSON, updates the log and HEAD.
    """
    root = gcc_root or find_gcc_root()
    config = WorkspaceConfig.read(root / "config")
    branch = config.current_branch

    branch_dir = root / "branches" / branch
    context_file = branch_dir / "commit.md"

    if not context_file.exists():
        console.print(
            f"[red bold]Error:[/] No context file found at [cyan]{context_file}[/].\n"
            f"Create [cyan].GCC/branches/{branch}/commit.md[/] with your context first."
        )
        raise SystemExit(1)

    content = context_file.read_text(encoding="utf-8")
    timestamp = now_iso()
    parent = read_head(root)

    commit_hash = generate_hash(timestamp, message, content)

    snapshot_dir = root / "snapshots" / commit_hash
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    (snapshot_dir / "context.md").write_text(content, encoding="utf-8")
    metadata_yaml = (
        f"timestamp: {timestamp}\n"
        f"message: \"{message}\"\n"
        f"parent: {parent or 'null'}\n"
        f"branch: {branch}\n"
    )
    (snapshot_dir / "metadata.yaml").write_text(metadata_yaml, encoding="utf-8")

    commit = Commit(
        hash=commit_hash,
        parent=parent if parent else None,
        message=message,
        branch=branch,
        timestamp=timestamp,
        snapshot_ref=commit_hash,
    )
    (root / "commits" / f"{commit_hash}.json").write_text(
        commit.to_json() + "\n", encoding="utf-8"
    )

    _append_log(branch_dir / "log.md", commit)

    write_head(root, commit_hash)

    console.print(
        f"[green bold]Committed:[/] [cyan bold]{commit_hash}[/] — {message}\n"
        f"  Branch: [yellow]{branch}[/]  |  "
        f"Time: {timestamp}"
    )

    return commit


def _append_log(log_path: Path, commit: Commit) -> None:
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else ""

    if existing.strip() == "# Execution Log\n\n_No entries yet._".strip():
        existing = "# Execution Log\n"

    entry = (
        f"\n## {commit.hash}\n"
        f"- **Date:** {commit.timestamp}\n"
        f"- **Branch:** {commit.branch}\n"
        f"- **Message:** {commit.message}\n"
    )
    if commit.parent:
        entry += f"- **Parent:** {commit.parent}\n"

    log_path.write_text(existing + entry, encoding="utf-8")
