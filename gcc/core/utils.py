from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from rich.console import Console

GCC_DIR = ".GCC"

err_console = Console(stderr=True)


def generate_hash(timestamp: str, message: str, content: str) -> str:
    """Generate a truncated SHA-256 hash (8 hex chars) from timestamp + message + content."""
    raw = f"{timestamp}{message}{content}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_gcc_root(start: Optional[Path] = None) -> Path:
    """Walk up from *start* (default: cwd) looking for a .GCC/ directory.

    Returns the Path to the .GCC folder, or raises SystemExit with a
    helpful error message if none is found.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        candidate = current / GCC_DIR
        if candidate.is_dir():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    err_console.print(
        "[red bold]Error:[/] No .GCC/ directory found.\n"
        "Run [cyan]gcc init[/] first to initialize a workspace."
    )
    raise SystemExit(1)


def read_head(gcc_root: Path) -> Optional[str]:
    head_file = gcc_root / "HEAD"
    if not head_file.exists():
        return None
    content = head_file.read_text(encoding="utf-8").strip()
    return content if content else None


def write_head(gcc_root: Path, commit_hash: str) -> None:
    (gcc_root / "HEAD").write_text(commit_hash + "\n", encoding="utf-8")
