from __future__ import annotations

from pathlib import Path
import subprocess
from datetime import datetime

from first_agentic.repo.models import CommandResult, RepoPermissions


class RepoPermissionError(PermissionError):
    pass


class RepoAdapter:
    def __init__(self, repo_root: str | Path, permissions: RepoPermissions) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.permissions = permissions

    def create_task_branch(self, task_id: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        branch_name = f"sandbox/{task_id.lower()}-{timestamp}"
        self._run_git(["checkout", "-b", branch_name])
        return branch_name

    def current_branch(self) -> str:
        result = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        return result.stdout.strip()

    def read_file(self, relative_path: str) -> str:
        file_path = self._resolve_allowed_path(relative_path)
        return file_path.read_text(encoding="utf-8")

    def write_file(self, relative_path: str, content: str) -> str:
        file_path = self._resolve_allowed_path(relative_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return str(file_path.relative_to(self.repo_root))

    def list_changed_files(self) -> list[str]:
        result = self._run_git(["status", "--porcelain"])
        changed_files: list[str] = []

        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue

            if len(line) < 4:
                continue

            changed_files.append(line[3:])

        return changed_files

    def generate_diff(self) -> str:
        result = self._run_git(["diff"])
        return result.stdout

    def run_allowed_command(self, command: list[str]) -> CommandResult:
        if not command:
            raise RepoPermissionError("Command cannot be empty.")

        executable = command[0]
        if executable not in self.permissions.allowed_commands:
            raise RepoPermissionError(
                f"Command '{executable}' is not permitted for sandbox execution."
            )

        completed = subprocess.run(
            command,
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            check=False,
        )

        return CommandResult(
            command=command,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    def ensure_change_limit(self) -> None:
        changed = self.list_changed_files()
        if len(changed) > self.permissions.max_files_changed:
            raise RepoPermissionError(
                "Changed files exceed configured limit: "
                f"{len(changed)} > {self.permissions.max_files_changed}"
            )

    def _resolve_allowed_path(self, relative_path: str) -> Path:
        rel = Path(relative_path)
        if rel.is_absolute():
            raise RepoPermissionError("Absolute paths are not allowed.")

        normalized = rel.as_posix().lstrip("./")
        if not self._is_path_allowed(normalized):
            raise RepoPermissionError(
                f"Path '{normalized}' is not inside allowed paths {self.permissions.allowed_paths}."
            )

        return (self.repo_root / normalized).resolve()

    def _is_path_allowed(self, normalized_path: str) -> bool:
        if not self.permissions.allowed_paths:
            return False

        for raw_prefix in self.permissions.allowed_paths:
            prefix = raw_prefix.strip("/")
            if not prefix:
                continue

            if normalized_path == prefix or normalized_path.startswith(f"{prefix}/"):
                return True

        return False

    def _run_git(self, args: list[str]) -> CommandResult:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.repo_root,
            text=True,
            capture_output=True,
            check=False,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                f"git {' '.join(args)} failed with code {completed.returncode}: "
                f"{completed.stderr.strip()}"
            )

        return CommandResult(
            command=["git", *args],
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
