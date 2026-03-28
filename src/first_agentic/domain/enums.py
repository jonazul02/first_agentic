from enum import Enum


class TaskStatus(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    CODING = "coding"
    REVIEWING = "reviewing"
    NEEDS_CHANGES = "needs_changes"
    APPROVED = "approved"
    REJECTED = "rejected"
    AWAITING_USER = "awaiting_user"


class TaskType(str, Enum):
    FEATURE = "feature"
    BUGFIX = "bugfix"
    TEST = "test"
    REFACTOR = "refactor"
    DOCS = "docs"


class Severity(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    SUGGESTION = "suggestion"
