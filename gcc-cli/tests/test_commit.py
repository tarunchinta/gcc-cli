import tempfile
from pathlib import Path

from gcc.core.init import run_init
from gcc.core.commit import run_commit
from gcc.core.utils import read_head
from gcc.models.commit import Commit


def test_commit_creates_snapshot():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)

        context_file = gcc_path / "branches" / "main" / "commit.md"
        context_file.write_text("# My first context\nHello world", encoding="utf-8")

        commit = run_commit("initial commit", gcc_root=gcc_path)

        assert len(commit.hash) == 8
        assert commit.message == "initial commit"
        assert commit.branch == "main"
        assert commit.parent is None

        snapshot = gcc_path / "snapshots" / commit.hash / "context.md"
        assert snapshot.exists()
        assert "Hello world" in snapshot.read_text(encoding="utf-8")

        commit_file = gcc_path / "commits" / f"{commit.hash}.json"
        assert commit_file.exists()
        loaded = Commit.from_file(commit_file)
        assert loaded.hash == commit.hash


def test_commit_chain():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)

        context_file = gcc_path / "branches" / "main" / "commit.md"

        context_file.write_text("context v1", encoding="utf-8")
        c1 = run_commit("first", gcc_root=gcc_path)

        context_file.write_text("context v2", encoding="utf-8")
        c2 = run_commit("second", gcc_root=gcc_path)

        assert c2.parent == c1.hash
        assert read_head(gcc_path) == c2.hash


def test_commit_updates_log():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        gcc_path = run_init(root)

        context_file = gcc_path / "branches" / "main" / "commit.md"
        context_file.write_text("some context", encoding="utf-8")
        run_commit("log test", gcc_root=gcc_path)

        log_content = (gcc_path / "branches" / "main" / "log.md").read_text(encoding="utf-8")
        assert "log test" in log_content
