from __future__ import annotations

from first_agentic.domain.enums import TaskType
from first_agentic.domain.models import Task, TaskRequest


def build_sandbox_task() -> Task:
    return Task(
        task_id="S-001",
        request=TaskRequest(
            title="validar flujo repo sandbox",
            description="probar branch temporal, cambios limitados y diff real",
            task_type=TaskType.FEATURE,
            requested_by="user",
            target_paths=["docs/sandbox"],
        ),
    )
