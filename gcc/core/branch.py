from __future__ import annotations

import shutil
from pathlib import Path

from rich.console import Console

from gcc.core.utils import find_gcc_root, read_head, write_head
from gcc.models.workspace import WorkspaceConfig

console = Console()


def run_branch(name: str, gcc_root: Path | None = None) -> None:
    """Create a new branch named *name*, copying current branch state."""
    root = gcc_root or find_gcc_root()
    config = WorkspaceConfig.read(root / "config")

    new_branch_dir = root / "branches" / name
    if new_branch_dir.exists():
        console.print(f"[red bold]Error:[/] Branch [yellow]{name}[/] already exists.")
        raise SystemExit(1)

    current_branch_dir = root / "branches" / config.current_branch
    shutil.copytree(current_branch_dir, new_branch_dir)

    console.print(
        f"[green bold]Created branch:[/] [yellow]{name}[/] "
        f"(from [yellow]{config.current_branch}[/])"
    )


def run_checkout(name: str, gcc_root: Path | None = None) -> None:
    """Switch to branch *name*."""
    root = gcc_root or find_gcc_root()
    config = WorkspaceConfig.read(root / "config")

    branch_dir = root / "branches" / name
    if not branch_dir.exists():
        console.print(
            f"[red bold]Error:[/] Branch [yellow]{name}[/] does not exist.\n"
            f"Create it first with [cyan]gcc branch {name}[/]."
        )
        raise SystemExit(1)

    config.current_branch = name
    config.write(root / "config")

    head_hash = read_head(root)
    if head_hash:
        write_head(root, head_hash)

    console.print(
        f"[green bold]Switched to branch:[/] [yellow]{name}[/]"
    )


def list_branches(gcc_root: Path | None = None) -> list[str]:
    """Return a list of all branch names."""
    root = gcc_root or find_gcc_root()
    branches_dir = root / "branches"
    if not branches_dir.exists():
        return []
    return sorted(d.name for d in branches_dir.iterdir() if d.is_dir())
