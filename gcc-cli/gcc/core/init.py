from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from gcc.core.utils import GCC_DIR
from gcc.models.workspace import WorkspaceConfig

console = Console()

MAIN_MD_TEMPLATE = """\
# Project Roadmap

## Goals
- [ ] Define project objectives
- [ ] Outline key milestones

## Notes
_Use this file to track high-level project goals and roadmap._
"""

COMMIT_MD_TEMPLATE = """\
# Commit Summary

_No commits yet. Use `gcc commit -m "message"` to create your first commit._
"""

LOG_MD_TEMPLATE = """\
# Execution Log

_No entries yet._
"""

METADATA_YAML_TEMPLATE = """\
model: unknown
tokens: 0
task: initial
"""


def run_init(directory: Path | None = None) -> Path:
    """Initialize a .GCC/ workspace in *directory* (default: cwd).

    Returns the path to the created .GCC/ folder.
    """
    root = (directory or Path.cwd()).resolve()
    gcc_path = root / GCC_DIR

    if gcc_path.exists():
        console.print(
            f"[yellow bold]Warning:[/] .GCC/ already exists at [cyan]{gcc_path}[/]\n"
            "Nothing to do."
        )
        raise SystemExit(0)

    workspace_name = root.name

    gcc_path.mkdir(parents=True)
    (gcc_path / "commits").mkdir()
    (gcc_path / "snapshots").mkdir()
    branches_dir = gcc_path / "branches" / "main"
    branches_dir.mkdir(parents=True)

    config = WorkspaceConfig(workspace_name=workspace_name, current_branch="main")
    config.write(gcc_path / "config")

    (gcc_path / "HEAD").write_text("\n", encoding="utf-8")

    (gcc_path / "main.md").write_text(MAIN_MD_TEMPLATE, encoding="utf-8")

    (branches_dir / "commit.md").write_text(COMMIT_MD_TEMPLATE, encoding="utf-8")
    (branches_dir / "log.md").write_text(LOG_MD_TEMPLATE, encoding="utf-8")
    (branches_dir / "metadata.yaml").write_text(METADATA_YAML_TEMPLATE, encoding="utf-8")

    console.print(
        Panel(
            f"[green bold]Initialized GCC workspace[/] in [cyan]{gcc_path}[/]\n\n"
            f"  Workspace : [bold]{workspace_name}[/]\n"
            f"  Branch    : [yellow]main[/]\n\n"
            "Next steps:\n"
            '  1. Edit [cyan].GCC/branches/main/commit.md[/] with your context\n'
            '  2. Run [cyan]gcc commit -m "initial context"[/]',
            title="[bold]GCC[/]",
            border_style="green",
        )
    )

    return gcc_path
