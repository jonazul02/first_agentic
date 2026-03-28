from __future__ import annotations

import subprocess
from pathlib import Path

from first_agentic.agents.sandbox_orchestrator import SandboxOrchestratorAgent
from first_agentic.core.sandbox_tasks import build_sandbox_task
from first_agentic.domain.enums import TaskStatus
from first_agentic.repo.adapter import RepoAdapter
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


def test_sandbox_orchestrator_runs_end_to_end(tmp_path: Path) -> None:
    repo_path = _init_git_repo(tmp_path)
    permissions = RepoPermissions(
        allowed_paths=["docs/sandbox"],
        allowed_commands=["python3"],
        max_files_changed=3,
    )
    repo = RepoAdapter(repo_root=repo_path, permissions=permissions)

    task = build_sandbox_task()
    orchestrator = SandboxOrchestratorAgent(max_review_rounds=1)
    result = orchestrator.run_task(task, repo)

    assert result.final_status in {TaskStatus.AWAITING_USER, TaskStatus.REJECTED}
    assert result.branch_name is not None
    assert result.changed_files
