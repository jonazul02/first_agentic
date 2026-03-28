from __future__ import annotations

from first_agentic.agents.coder import CoderAgent
from first_agentic.agents.reviewer import ReviewerAgent
from first_agentic.domain.contracts import CoderOutput, ReviewReport
from first_agentic.domain.enums import TaskStatus
from first_agentic.domain.models import Task, TaskResult
from first_agentic.orchestration.engine import OrchestrationEngine


class OrchestratorAgent:
    def __init__(self, max_review_rounds: int = 3) -> None:
        self.max_review_rounds = max_review_rounds
        self.engine = OrchestrationEngine()
        self.coder = CoderAgent()
        self.reviewer = ReviewerAgent()

    def run_task(self, task: Task) -> TaskResult:
        self.engine.move_to(task, TaskStatus.PLANNED)

        latest_code: CoderOutput | None = None
        latest_review: ReviewReport | None = None

        while True:
            self.engine.move_to(task, TaskStatus.CODING)
            latest_code = self.coder.implement(task)

            self.engine.move_to(task, TaskStatus.REVIEWING)
            latest_review = self.reviewer.review(task, latest_code)

            if latest_review.has_critical() or latest_review.has_important():
                if task.review_round >= self.max_review_rounds:
                    self.engine.move_to(task, TaskStatus.REJECTED)
                    break

                self.engine.move_to(task, TaskStatus.NEEDS_CHANGES)
                continue

            self.engine.move_to(task, TaskStatus.AWAITING_USER)
            break

        return TaskResult(
            task_id=task.task_id,
            final_status=task.status,
            summary=(latest_code.summary if latest_code else "No work executed."),
            changed_files=(latest_code.changed_files if latest_code else []),
            test_status=(latest_review.test_status if latest_review else "not_run"),
            risk_level=(latest_review.risk_level if latest_review else "unknown"),
            recommendation=(latest_review.recommendation if latest_review else "pending"),
        )
