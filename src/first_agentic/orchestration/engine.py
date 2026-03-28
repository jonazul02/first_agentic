from __future__ import annotations

from dataclasses import dataclass

from first_agentic.domain.enums import TaskStatus
from first_agentic.domain.models import Task


ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.CREATED: {TaskStatus.PLANNED},
    TaskStatus.PLANNED: {TaskStatus.CODING},
    TaskStatus.CODING: {TaskStatus.REVIEWING},
    TaskStatus.REVIEWING: {
        TaskStatus.NEEDS_CHANGES,
        TaskStatus.APPROVED,
        TaskStatus.REJECTED,
        TaskStatus.AWAITING_USER,
    },
    TaskStatus.NEEDS_CHANGES: {TaskStatus.CODING},
    TaskStatus.AWAITING_USER: {
        TaskStatus.APPROVED,
        TaskStatus.REJECTED,
        TaskStatus.NEEDS_CHANGES,
    },
    TaskStatus.APPROVED: set(),
    TaskStatus.REJECTED: set(),
}


@dataclass(slots=True)
class TransitionResult:
    previous: TaskStatus
    current: TaskStatus


class OrchestrationEngine:
    def move_to(self, task: Task, next_status: TaskStatus) -> TransitionResult:
        current = task.status
        allowed_next = ALLOWED_TRANSITIONS[current]

        if next_status not in allowed_next:
            raise ValueError(
                f"Invalid transition: {current.value} -> {next_status.value}"
            )

        if current == TaskStatus.REVIEWING and next_status == TaskStatus.NEEDS_CHANGES:
            task.review_round += 1

        task.status = next_status
        return TransitionResult(previous=current, current=next_status)
