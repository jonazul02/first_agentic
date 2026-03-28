from dataclasses import dataclass, field
from typing import List

from first_agentic.domain.enums import TaskStatus, TaskType


@dataclass(slots=True)
class TaskRequest:
    title: str
    description: str
    task_type: TaskType
    requested_by: str
    target_paths: List[str] = field(default_factory=list)


@dataclass(slots=True)
class Task:
    task_id: str
    request: TaskRequest
    status: TaskStatus = TaskStatus.CREATED
    review_round: int = 0


@dataclass(slots=True)
class TaskResult:
    task_id: str
    final_status: TaskStatus
    summary: str
    changed_files: List[str] = field(default_factory=list)
    test_status: str = "not_run"
    risk_level: str = "unknown"
    recommendation: str = "pending"
