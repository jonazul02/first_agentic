from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RepoPermissions:
    allowed_paths: list[str] = field(default_factory=list)
    allowed_commands: list[str] = field(default_factory=list)
    max_files_changed: int = 5


@dataclass(slots=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
