import pytest

from first_agentic.domain.enums import TaskStatus, TaskType
from first_agentic.domain.models import Task, TaskRequest
from first_agentic.orchestration.engine import OrchestrationEngine


def _task() -> Task:
    return Task(
        task_id="T-001",
        request=TaskRequest(
            title="agrega funcion suma",
            description="crear funcion suma con prueba",
            task_type=TaskType.FEATURE,
            requested_by="user",
            target_paths=["src/"],
        ),
    )


def test_happy_path_to_approved() -> None:
    engine = OrchestrationEngine()
    task = _task()

    engine.move_to(task, TaskStatus.PLANNED)
    engine.move_to(task, TaskStatus.CODING)
    engine.move_to(task, TaskStatus.REVIEWING)
    result = engine.move_to(task, TaskStatus.APPROVED)

    assert task.status == TaskStatus.APPROVED
    assert result.previous == TaskStatus.REVIEWING


def test_invalid_transition_raises_error() -> None:
    engine = OrchestrationEngine()
    task = _task()

    with pytest.raises(ValueError):
        engine.move_to(task, TaskStatus.APPROVED)


def test_review_round_increments_on_needs_changes() -> None:
    engine = OrchestrationEngine()
    task = _task()

    engine.move_to(task, TaskStatus.PLANNED)
    engine.move_to(task, TaskStatus.CODING)
    engine.move_to(task, TaskStatus.REVIEWING)
    engine.move_to(task, TaskStatus.NEEDS_CHANGES)

    assert task.review_round == 1
    assert task.status == TaskStatus.NEEDS_CHANGES
