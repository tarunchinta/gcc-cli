import os
import tempfile
from pathlib import Path

import pytest

from gcc.core.init import run_init
from gcc.models.workspace import WorkspaceConfig


def test_init_creates_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)

        assert gcc_path.exists()
        assert (gcc_path / "config").exists()
        assert (gcc_path / "HEAD").exists()
        assert (gcc_path / "main.md").exists()
        assert (gcc_path / "commits").is_dir()
        assert (gcc_path / "snapshots").is_dir()
        assert (gcc_path / "branches" / "main" / "commit.md").exists()
        assert (gcc_path / "branches" / "main" / "log.md").exists()
        assert (gcc_path / "branches" / "main" / "metadata.yaml").exists()


def test_init_config_values():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        run_init(root)
        config = WorkspaceConfig.read(root / ".GCC" / "config")
        assert config.current_branch == "main"
        assert config.workspace_name == root.name


def test_init_already_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        run_init(root)
        with pytest.raises(SystemExit):
            run_init(root)
