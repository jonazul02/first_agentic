from __future__ import annotations

from dataclasses import dataclass, field

from first_agentic.domain.enums import Severity


@dataclass(slots=True)
class CoderOutput:
    summary: str
    changed_files: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ReviewFinding:
    severity: Severity
    title: str
    detail: str


@dataclass(slots=True)
class ReviewReport:
    findings: list[ReviewFinding] = field(default_factory=list)
    lint_status: str = "not_run"
    test_status: str = "not_run"
    recommendation: str = "needs_changes"
    risk_level: str = "unknown"

    def has_critical(self) -> bool:
        return any(f.severity == Severity.CRITICAL for f in self.findings)

    def has_important(self) -> bool:
        return any(f.severity == Severity.IMPORTANT for f in self.findings)
