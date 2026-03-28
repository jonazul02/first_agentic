from __future__ import annotations

from first_agentic.agents.sandbox_coder import SandboxCoderAgent
from first_agentic.agents.sandbox_reviewer import SandboxReviewerAgent
from first_agentic.domain.contracts import CoderOutput, ReviewReport
from first_agentic.domain.enums import TaskStatus
from first_agentic.domain.models import Task, TaskResult
from first_agentic.orchestration.engine import OrchestrationEngine
from first_agentic.repo.adapter import RepoAdapter, RepoPermissionError


class SandboxOrchestratorAgent:
    def __init__(self, max_review_rounds: int = 3) -> None:
        self.max_review_rounds = max_review_rounds
        self.engine = OrchestrationEngine()
        self.coder = SandboxCoderAgent()
        self.reviewer = SandboxReviewerAgent()

    def run_task(self, task: Task, repo: RepoAdapter) -> TaskResult:
        self.engine.move_to(task, TaskStatus.PLANNED)
        branch_name = repo.create_task_branch(task.task_id)

        latest_code: CoderOutput | None = None
        latest_review: ReviewReport | None = None

        while True:
            self.engine.move_to(task, TaskStatus.CODING)
            latest_code = self.coder.implement(task, repo)

            try:
                repo.ensure_change_limit()
            except RepoPermissionError:
                self.engine.move_to(task, TaskStatus.REJECTED)
                break

            self.engine.move_to(task, TaskStatus.REVIEWING)
            latest_review = self.reviewer.review(task, latest_code, repo)

            if latest_review.recommendation != "approve":
                if task.review_round >= self.max_review_rounds:
                    self.engine.move_to(task, TaskStatus.REJECTED)
                    break

                self.engine.move_to(task, TaskStatus.NEEDS_CHANGES)
                continue

            self.engine.move_to(task, TaskStatus.AWAITING_USER)
            break

        diff_content = repo.generate_diff()

        return TaskResult(
            task_id=task.task_id,
            final_status=task.status,
            summary=(latest_code.summary if latest_code else "No work executed."),
            changed_files=repo.list_changed_files(),
            test_status=(latest_review.test_status if latest_review else "not_run"),
            risk_level=(latest_review.risk_level if latest_review else "unknown"),
            recommendation=(latest_review.recommendation if latest_review else "pending"),
            branch_name=branch_name,
            diff_excerpt=diff_content[:1200],
        )
