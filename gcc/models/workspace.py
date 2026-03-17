from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class WorkspaceConfig:
    workspace_name: str
    current_branch: str

    def write(self, config_path: Path) -> None:
        lines = [
            f"workspace_name={self.workspace_name}",
            f"current_branch={self.current_branch}",
        ]
        config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @classmethod
    def read(cls, config_path: Path) -> WorkspaceConfig:
        data: dict[str, str] = {}
        for line in config_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
        return cls(
            workspace_name=data.get("workspace_name", "unknown"),
            current_branch=data.get("current_branch", "main"),
        )
