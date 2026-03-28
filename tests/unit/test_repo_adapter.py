from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from first_agentic.repo.adapter import RepoAdapter, RepoPermissionError
from first_agentic.repo.models import RepoPermissions


def _init_git_repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    (tmp_path / "README.md").write_text("seed\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"], cwd=tmp_path, check=True, capture_output=True
    )
    return tmp_path


def test_write_file_allows_configured_path(tmp_path: Path) -> None:
    repo_path = _init_git_repo(tmp_path)
    permissions = RepoPermissions(allowed_paths=["docs/sandbox"], allowed_commands=["python3"])
    adapter = RepoAdapter(repo_root=repo_path, permissions=permissions)

    written = adapter.write_file("docs/sandbox/result.md", "ok")
    assert written == "docs/sandbox/result.md"


def test_write_file_rejects_disallowed_path(tmp_path: Path) -> None:
    repo_path = _init_git_repo(tmp_path)
    permissions = RepoPermissions(allowed_paths=["docs/sandbox"], allowed_commands=["python3"])
    adapter = RepoAdapter(repo_root=repo_path, permissions=permissions)

    with pytest.raises(RepoPermissionError):
        adapter.write_file("src/app.py", "print('x')")


def test_run_command_respects_allowlist(tmp_path: Path) -> None:
    repo_path = _init_git_repo(tmp_path)
    permissions = RepoPermissions(allowed_paths=["docs/sandbox"], allowed_commands=["python3"])
    adapter = RepoAdapter(repo_root=repo_path, permissions=permissions)

    result = adapter.run_allowed_command(["python3", "-c", "print('ok')"])
    assert result.returncode == 0
    assert "ok" in result.stdout

    with pytest.raises(RepoPermissionError):
        adapter.run_allowed_command(["git", "status"])
