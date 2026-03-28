from __future__ import annotations

from first_agentic.domain.enums import TaskType
from first_agentic.domain.models import Task, TaskRequest


def build_demo_tasks() -> list[Task]:
    return [
        Task(
            task_id="D-001",
            request=TaskRequest(
                title="agrega funcion suma",
                description="crear funcion suma con tests unitarios",
                task_type=TaskType.FEATURE,
                requested_by="user",
                target_paths=["src/", "tests/"],
            ),
        ),
        Task(
            task_id="D-002",
            request=TaskRequest(
                title="corrige bug de login",
                description="corregir validacion de autenticacion",
                task_type=TaskType.BUGFIX,
                requested_by="user",
                target_paths=["src/auth/", "tests/unit/"],
            ),
        ),
        Task(
            task_id="D-003",
            request=TaskRequest(
                title="anade test",
                description="incrementar cobertura sobre modulo existente",
                task_type=TaskType.TEST,
                requested_by="user",
                target_paths=["tests/"],
            ),
        ),
    ]
