from __future__ import annotations

import difflib
from pathlib import Path

from rich.console import Console
from rich.text import Text

from gcc.core.utils import find_gcc_root

console = Console()


def run_diff(hash1: str, hash2: str, gcc_root: Path | None = None) -> str:
    """Show a unified diff of context.md between two commit snapshots."""
    root = gcc_root or find_gcc_root()

    snap1 = root / "snapshots" / hash1 / "context.md"
    snap2 = root / "snapshots" / hash2 / "context.md"

    if not snap1.exists():
        console.print(f"[red bold]Error:[/] Snapshot for [cyan]{hash1}[/] not found.")
        raise SystemExit(1)
    if not snap2.exists():
        console.print(f"[red bold]Error:[/] Snapshot for [cyan]{hash2}[/] not found.")
        raise SystemExit(1)

    lines1 = snap1.read_text(encoding="utf-8").splitlines(keepends=True)
    lines2 = snap2.read_text(encoding="utf-8").splitlines(keepends=True)

    diff_lines = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=f"{hash1}/context.md",
        tofile=f"{hash2}/context.md",
    ))

    if not diff_lines:
        console.print("[green]No differences found.[/]")
        return ""

    for line in diff_lines:
        stripped = line.rstrip("\n")
        if stripped.startswith("+++") or stripped.startswith("---"):
            console.print(Text(stripped, style="bold"))
        elif stripped.startswith("@@"):
            console.print(Text(stripped, style="cyan"))
        elif stripped.startswith("+"):
            console.print(Text(stripped, style="green"))
        elif stripped.startswith("-"):
            console.print(Text(stripped, style="red"))
        else:
            console.print(stripped)

    return "".join(diff_lines)
