"""Guarded registration of already-approved canonical Worker profiles.

This module creates one route-less SQLite registry row from one canonical department-owned
Worker profile. It does not create a ChatGPT room, capture a route, run a canary, dispatch work,
change advisory lifecycle, or create activation authority.
"""

from __future__ import annotations

import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath

from .command_center import CommandCenterService
from .room_titles import CANONICAL_WORKER_TITLES
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_runtime_service import WorkerRuntimeService
from .worker_source_resolution import front_matter, positive_int_value, read_relative


@dataclass(frozen=True)
class CanonicalWorkerProfile:
    """Machine-readable identity resolved from one canonical Worker profile."""

    worker_id: str
    chat_title: str
    owning_department: str
    profile_path: str
    profile_version: int
    specialization: str
    role: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class WorkerRegistrationService:
    """Register one approved canonical profile without creating a route or authority."""

    def __init__(
        self,
        command_center: CommandCenterService,
        repository_root: Path,
    ) -> None:
        self.command_center = command_center
        self.repository_root = repository_root.resolve()
        self.database_path = Path(command_center.store.database_path)
        self.runtime = WorkerRuntimeService(self.database_path)

    @staticmethod
    def _required(metadata: dict[str, str], key: str) -> str:
        value = str(metadata.get(key) or "").strip()
        if not value:
            raise WorkerRuntimeError(f"Worker profile field {key} is missing.")
        return value

    def _normalized_profile_path(self, profile_path: str) -> str:
        normalized = str(profile_path or "").strip().replace("\\", "/")
        path = PurePosixPath(normalized)
        if (
            path.is_absolute()
            or len(path.parts) < 4
            or path.parts[0] != "projects"
            or path.parts[-2] != "workers"
            or path.suffix.casefold() != ".md"
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise WorkerRuntimeError(
                "Worker registration requires one safe canonical profile path under "
                "projects/<department>/workers/*.md."
            )
        candidate = (self.repository_root / path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError(
                "Worker profile path escapes the repository root."
            ) from exc
        return path.as_posix()

    def load_profile(self, profile_path: str) -> CanonicalWorkerProfile:
        """Resolve and validate one canonical profile without mutating runtime state."""

        normalized = self._normalized_profile_path(profile_path)
        text = read_relative(self.repository_root, normalized)
        metadata = front_matter(text)
        worker_id = self._required(metadata, "worker_id")
        chat_title = self._required(metadata, "chat_title")
        owning_department = self._required(metadata, "owning_department")
        role = self._required(metadata, "role")
        specialization = self._required(metadata, "specialization")
        profile_version = positive_int_value(metadata, "profile_version")

        if role != "worker":
            raise WorkerRuntimeError("Worker profile role must be worker.")
        expected_title = CANONICAL_WORKER_TITLES.get(worker_id)
        if expected_title is None:
            raise WorkerRuntimeError(
                f"Worker {worker_id!r} is not present in the executable canonical title map."
            )
        if chat_title != expected_title:
            raise WorkerRuntimeError(
                f"Worker profile title must equal canonical exact title {expected_title!r}."
            )

        entry = WorkerRegistryEntry(
            worker_id=worker_id,
            chat_title=chat_title,
            owning_department=owning_department,
            profile_path=normalized,
            profile_version=profile_version,
            conversation_url=None,
            route_revision=0,
            specialization=specialization,
            role=role,
            deployment_state="enabled",
        )
        return CanonicalWorkerProfile(
            worker_id=entry.worker_id,
            chat_title=entry.chat_title,
            owning_department=entry.owning_department,
            profile_path=entry.profile_path,
            profile_version=entry.profile_version,
            specialization=entry.specialization,
            role=entry.role,
        )

    def _profile_paths(self) -> tuple[str, ...]:
        paths = []
        for candidate in self.repository_root.glob("projects/*/workers/*.md"):
            if candidate.is_file():
                paths.append(candidate.relative_to(self.repository_root).as_posix())
        return tuple(sorted(paths))

    def status(self) -> dict[str, object]:
        """List canonical unregistered profiles plus any fail-closed discovery errors."""

        existing = self.runtime.workers()
        by_id = {entry.worker_id: entry for entry in existing}
        by_title = {entry.chat_title: entry for entry in existing}
        by_path = {entry.profile_path: entry for entry in existing}
        candidates: list[dict[str, object]] = []
        errors: list[dict[str, str]] = []

        for profile_path in self._profile_paths():
            try:
                profile = self.load_profile(profile_path)
            except (OSError, WorkerRuntimeError) as exc:
                errors.append({"profile_path": profile_path, "reason": str(exc)})
                continue

            current = by_id.get(profile.worker_id)
            if current is not None:
                continue
            conflict = by_title.get(profile.chat_title) or by_path.get(profile.profile_path)
            if conflict is not None:
                errors.append(
                    {
                        "profile_path": profile.profile_path,
                        "reason": (
                            "Canonical profile conflicts with an existing registry title or path "
                            f"owned by {conflict.worker_id!r}."
                        ),
                    }
                )
                continue
            candidates.append(profile.to_dict())

        return {
            "paused": self.command_center.paused,
            "running": self.command_center.running,
            "candidates": candidates,
            "errors": errors,
        }

    @staticmethod
    def _same_identity(row: sqlite3.Row, profile: CanonicalWorkerProfile) -> bool:
        return all(
            (
                str(row["worker_id"]) == profile.worker_id,
                str(row["chat_title"]) == profile.chat_title,
                str(row["owning_department"]) == profile.owning_department,
                str(row["profile_path"]) == profile.profile_path,
                int(row["profile_version"]) == profile.profile_version,
                str(row["specialization"]) == profile.specialization,
                str(row["role"]) == profile.role,
            )
        )

    def register_profile(
        self,
        profile_path: str,
        *,
        confirm_registration: bool,
    ) -> dict[str, object]:
        """Atomically create one route-less registry row from one canonical profile."""

        if not confirm_registration:
            raise WorkerRuntimeError("Worker registration requires explicit confirmation.")
        if not self.command_center.paused:
            raise WorkerRuntimeError(
                "Pause automation before registering a Worker. Nothing was changed."
            )
        if self.command_center.running:
            raise WorkerRuntimeError(
                "Another automation job is running. Nothing was changed."
            )

        profile = self.load_profile(profile_path)
        run_lock = self.command_center._run_lock  # noqa: SLF001 - shared runtime write gate
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError(
                "Another automation job is running. Nothing was changed."
            )

        changed = False
        try:
            now = time.time()
            with sqlite3.connect(self.database_path) as connection:
                connection.row_factory = sqlite3.Row
                connection.execute("PRAGMA foreign_keys = ON")
                connection.execute("BEGIN IMMEDIATE")
                rows = connection.execute(
                    """
                    SELECT * FROM worker_registry
                    WHERE worker_id = ? OR chat_title = ? OR profile_path = ?
                    """,
                    (
                        profile.worker_id,
                        profile.chat_title,
                        profile.profile_path,
                    ),
                ).fetchall()
                if rows:
                    if len(rows) == 1 and self._same_identity(rows[0], profile):
                        message = "This canonical Worker identity is already registered."
                    else:
                        raise WorkerRuntimeError(
                            "Worker registration conflicts with an existing ID, title, or profile "
                            "path. Nothing was changed."
                        )
                else:
                    connection.execute(
                        """
                        INSERT INTO worker_registry(
                            worker_id, chat_title, owning_department, profile_path,
                            profile_version, conversation_url, route_revision,
                            specialization, role, deployment_state,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, NULL, 0, ?, 'worker', 'enabled', ?, ?)
                        """,
                        (
                            profile.worker_id,
                            profile.chat_title,
                            profile.owning_department,
                            profile.profile_path,
                            profile.profile_version,
                            profile.specialization,
                            now,
                            now,
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO worker_route_state(
                            worker_id, availability, last_seen_at, pause_reason, updated_at
                        ) VALUES (?, 'unknown', NULL, ?, ?)
                        """,
                        (
                            profile.worker_id,
                            "Registered from canonical profile; exact route not yet linked.",
                            now,
                        ),
                    )
                    changed = True
                    message = (
                        f"Registered {profile.chat_title} without a route. "
                        "Guarded route capture remains required."
                    )
        except sqlite3.IntegrityError as exc:
            raise WorkerRuntimeError(
                "Worker registration could not preserve registry uniqueness. Nothing was changed."
            ) from exc
        finally:
            run_lock.release()

        entry = self.runtime.worker(profile.worker_id)
        route = self.runtime.store.route_state(profile.worker_id)
        return {
            "changed": changed,
            "message": message,
            "worker": {
                **entry.to_dict(),
                "route": asdict(route) if route is not None else None,
            },
            "activation_authorized": False,
        }


__all__ = [
    "CanonicalWorkerProfile",
    "WorkerRegistrationService",
]
