from __future__ import annotations

from pathlib import Path

from rich.console import Console

from gcc.core.utils import find_gcc_root, read_head
from gcc.models.commit import Commit

console = Console()


def run_log(gcc_root: Path | None = None) -> list[Commit]:
    """Walk the commit chain from HEAD backwards and display each commit."""
    root = gcc_root or find_gcc_root()
    current_hash = read_head(root)

    if not current_hash:
        console.print("[yellow]No commits yet.[/]")
        return []

    commits: list[Commit] = []
    visited: set[str] = set()

    while current_hash and current_hash not in visited:
        visited.add(current_hash)
        commit_file = root / "commits" / f"{current_hash}.json"
        if not commit_file.exists():
            console.print(f"[red]Warning:[/] commit file for [cyan]{current_hash}[/] not found, stopping.")
            break
        commit = Commit.from_file(commit_file)
        commits.append(commit)
        current_hash = commit.parent

    for c in commits:
        ts_display = c.timestamp.replace("T", " ").replace("Z", "")
        console.print(f"[cyan bold]commit {c.hash}[/]")
        console.print(f"Branch: [yellow]{c.branch}[/]")
        console.print(f"Date:   {ts_display}")
        console.print(f"\n    {c.message}\n")

    return commits
