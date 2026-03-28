from __future__ import annotations

from first_agentic.domain.contracts import CoderOutput, ReviewFinding, ReviewReport
from first_agentic.domain.enums import Severity
from first_agentic.domain.models import Task


class ReviewerAgent:
    def review(self, task: Task, coder_output: CoderOutput) -> ReviewReport:
        title = task.request.title.lower()

        if "login" in title and task.review_round == 0:
            return ReviewReport(
                findings=[
                    ReviewFinding(
                        severity=Severity.CRITICAL,
                        title="Missing regression coverage",
                        detail="Login patch needs explicit regression test for invalid token path.",
                    )
                ],
                lint_status="passed",
                test_status="failed",
                recommendation="needs_changes",
                risk_level="high",
            )

        if "suma" in title and task.review_round == 0:
            return ReviewReport(
                findings=[
                    ReviewFinding(
                        severity=Severity.IMPORTANT,
                        title="Edge case missing",
                        detail="Add test for negative inputs and zero handling.",
                    )
                ],
                lint_status="passed",
                test_status="passed",
                recommendation="needs_changes",
                risk_level="medium",
            )

        return ReviewReport(
            findings=[],
            lint_status="passed",
            test_status="passed",
            recommendation="approve",
            risk_level="low",
        )
