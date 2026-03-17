"""GCC CLI — Git-style version control for AI agent context."""
from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console

import gcc

console = Console()

app = typer.Typer(
    name="gcc",
    help="Git-style version control for AI agent context.",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def init() -> None:
    """Initialize a .GCC/ workspace in the current directory."""
    from gcc.core.init import run_init

    run_init()


@app.command()
def commit(
    message: str = typer.Option(..., "-m", "--message", help="Commit message"),
) -> None:
    """Snapshot current context state with a message."""
    from gcc.core.commit import run_commit

    run_commit(message)


@app.command()
def log() -> None:
    """Show commit history (like git log)."""
    from gcc.core.log import run_log

    run_log()


@app.command()
def status() -> None:
    """Show current branch, last commit, and dirty state."""
    from gcc.core.status import run_status

    run_status()


@app.command()
def branch(name: str = typer.Argument(..., help="Name for the new branch")) -> None:
    """Create a new branch from the current branch."""
    from gcc.core.branch import run_branch

    run_branch(name)


@app.command()
def checkout(name: str = typer.Argument(..., help="Branch to switch to")) -> None:
    """Switch to an existing branch."""
    from gcc.core.branch import run_checkout

    run_checkout(name)


@app.command()
def diff(
    hash1: str = typer.Argument(..., help="First commit hash"),
    hash2: str = typer.Argument(..., help="Second commit hash"),
) -> None:
    """Show text diff between two commits."""
    from gcc.core.diff import run_diff

    run_diff(hash1, hash2)


@app.command()
def version() -> None:
    """Show GCC version."""
    console.print(f"[bold]GCC[/] version [cyan]{gcc.__version__}[/]")


if __name__ == "__main__":
    app()
