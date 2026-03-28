from __future__ import annotations

from first_agentic.domain.contracts import CoderOutput, ReviewReport
from first_agentic.domain.models import Task
from first_agentic.repo.adapter import RepoAdapter, RepoPermissionError


class SandboxReviewerAgent:
    def review(self, task: Task, coder_output: CoderOutput, repo: RepoAdapter) -> ReviewReport:
        del task
        del coder_output

        lint_status = "skipped"
        test_status = "not_run"

        try:
            test_result = repo.run_allowed_command(["python3", "-m", "pytest", "-q"])
            test_status = "passed" if test_result.returncode == 0 else "failed"
        except RepoPermissionError:
            test_status = "blocked"

        recommendation = "approve" if test_status == "passed" else "needs_changes"
        risk_level = "low" if recommendation == "approve" else "medium"

        return ReviewReport(
            findings=[],
            lint_status=lint_status,
            test_status=test_status,
            recommendation=recommendation,
            risk_level=risk_level,
        )
