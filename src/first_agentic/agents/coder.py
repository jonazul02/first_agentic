from __future__ import annotations

from first_agentic.domain.contracts import CoderOutput
from first_agentic.domain.models import Task


class CoderAgent:
    def implement(self, task: Task) -> CoderOutput:
        title = task.request.title.lower()

        if "suma" in title:
            return CoderOutput(
                summary="Implement suma utility and unit test.",
                changed_files=[
                    "src/math/suma.py",
                    "tests/unit/test_suma.py",
                ],
                notes=["Added initial implementation aligned with request."],
            )

        if "login" in title:
            return CoderOutput(
                summary="Patch login validation and update related tests.",
                changed_files=[
                    "src/auth/login.py",
                    "tests/unit/test_login.py",
                ],
                notes=["Hardened input validation for auth flow."],
            )

        if "test" in title:
            return CoderOutput(
                summary="Add missing tests for existing module.",
                changed_files=["tests/unit/test_feature_existing.py"],
                notes=["Focused only on test coverage increase."],
            )

        return CoderOutput(
            summary="Generic implementation based on task request.",
            changed_files=["src/app/placeholder.py"],
            notes=["Fallback implementation path used."],
        )
