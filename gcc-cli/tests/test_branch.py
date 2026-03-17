import tempfile
from pathlib import Path

import pytest

from gcc.core.init import run_init
from gcc.core.branch import run_branch, run_checkout, list_branches
from gcc.models.workspace import WorkspaceConfig


def test_create_branch():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)

        run_branch("feature", gcc_root=gcc_path)

        assert (gcc_path / "branches" / "feature").is_dir()
        assert (gcc_path / "branches" / "feature" / "commit.md").exists()
        assert (gcc_path / "branches" / "feature" / "log.md").exists()

        branches = list_branches(gcc_root=gcc_path)
        assert "main" in branches
        assert "feature" in branches


def test_branch_already_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)
        run_branch("feature", gcc_root=gcc_path)
        with pytest.raises(SystemExit):
            run_branch("feature", gcc_root=gcc_path)


def test_checkout():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)
        run_branch("dev", gcc_root=gcc_path)
        run_checkout("dev", gcc_root=gcc_path)

        config = WorkspaceConfig.read(gcc_path / "config")
        assert config.current_branch == "dev"


def test_checkout_nonexistent():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)
        with pytest.raises(SystemExit):
            run_checkout("nope", gcc_root=gcc_path)
