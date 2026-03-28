from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from first_agentic.agents.sandbox_orchestrator import SandboxOrchestratorAgent
from first_agentic.core.sandbox_tasks import build_sandbox_task
from first_agentic.repo.adapter import RepoAdapter
from first_agentic.repo.models import RepoPermissions


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]

    permissions = RepoPermissions(
        allowed_paths=["docs/sandbox"],
        allowed_commands=["python3"],
        max_files_changed=3,
    )
    repo = RepoAdapter(repo_root=repo_root, permissions=permissions)

    task = build_sandbox_task()
    orchestrator = SandboxOrchestratorAgent(max_review_rounds=2)
    result = orchestrator.run_task(task, repo)

    payload = asdict(result)
    payload["final_status"] = result.final_status.value

    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
