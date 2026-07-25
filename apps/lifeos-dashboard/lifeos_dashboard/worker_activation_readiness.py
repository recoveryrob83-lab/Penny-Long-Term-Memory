"""Read-only contract-derived Worker activation prerequisite reports.

The report recomputes current prerequisites from canonical repository files and the existing
Command Center SQLite database. It never creates or updates a Worker, route, procedure,
deployment state, permission, schedule, advisory, or activation record.
"""
from __future__ import annotations

import re
import sqlite3
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Literal, cast

from .department_hq_routing import (
    DepartmentHqRoute,
    DepartmentHqRoutingError,
    resolve_department_hq_route,
)
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError

FindingState = Literal["PASS", "HOLD", "NOT_APPLICABLE"]
ReadinessState = Literal["READY_FOR_AUTHORITY_REVIEW", "HOLD"]

_WORKER_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_FRONT_MATTER_PATTERN = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
_PROCEDURE_FIELD_PATTERN = re.compile(
    r"^(?P<name>Procedure ID|Procedure Version|Owner|Lifecycle State):\s*(?P<value>.+?)\s*$",
    re.MULTILINE,
)

_REQUIRED_PROFILE_METADATA = (
    "worker_id",
    "chat_title",
    "owning_department",
    "role",
    "specialization",
    "profile_version",
)
_REQUIRED_PROFILE_SECTIONS = (
    "purpose",
    "allowed task classes",
    "explicitly prohibited work",
    "read scope",
    "write scope",
    "approved connectors and tools",
    "required procedures",
    "required evidence",
    "hold conditions",
    "elevation conditions",
    "verification and completion path",
    "owning department hq",
)
_REQUIRED_REVIEW_SECTIONS = (
    "purpose",
    "authority",
    "required inputs",
    "deterministic receipt path",
    "allowed review states",
    "ingestion",
    "completion condition",
)
_FORBIDDEN_PROFILE_METADATA = {
    "active",
    "deployment_state",
    "lifecycle_state",
    "pause_state",
    "retired",
    "route_availability",
}
_UNRESOLVED_RESULT_STATES = {
    "REPORT_REPAIR_PENDING",
    "ROB_VALIDATION_REQUIRED",
}
_UNRESOLVED_REVIEW_STATES = {
    "REPAIR_REQUIRED",
    "ROB_VALIDATION_REQUIRED",
}


@dataclass(frozen=True)
class ActivationFinding:
    """One explicit prerequisite result plus its authoritative source pointer."""

    code: str
    state: FindingState
    summary: str
    source: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class WorkerActivationReadinessReport:
    """Ephemeral technical-readiness report that never grants activation authority."""

    report_version: int
    worker_id: str
    state: ReadinessState
    technical_ready: bool
    activation_authorized: bool
    findings: tuple[ActivationFinding, ...]
    registry: dict[str, object] | None = None
    hq_route: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["findings"] = [finding.to_dict() for finding in self.findings]
        values["summary"] = {
            "pass": sum(finding.state == "PASS" for finding in self.findings),
            "hold": sum(finding.state == "HOLD" for finding in self.findings),
            "not_applicable": sum(
                finding.state == "NOT_APPLICABLE" for finding in self.findings
            ),
        }
        return values


class WorkerActivationReadinessService:
    """Read canonical files and runtime state through fail-closed, read-only paths."""

    def __init__(
        self,
        repository_root: Path,
        database_path: Path,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self.repository_root = repository_root.resolve()
        self.database_path = database_path.resolve()
        self.environment = dict(environment) if environment is not None else None

    @staticmethod
    def _finding(
        code: str,
        state: FindingState,
        summary: str,
        source: str,
    ) -> ActivationFinding:
        return ActivationFinding(code=code, state=state, summary=summary, source=source)

    def _connect_read_only(self) -> sqlite3.Connection:
        if not self.database_path.is_file():
            raise WorkerRuntimeError("Command Center database does not exist.")
        uri = self.database_path.as_uri() + "?mode=ro"
        try:
            connection = sqlite3.connect(uri, uri=True)
        except sqlite3.Error as exc:
            raise WorkerRuntimeError(
                "Command Center database could not be opened read-only."
            ) from exc
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
        row = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        ).fetchone()
        return row is not None

    @staticmethod
    def _table_columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
        return {
            str(row["name"])
            for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        }

    def _safe_repository_path(self, relative_path: str, label: str) -> Path:
        normalized = str(relative_path or "").strip().replace("\\", "/")
        path = PurePosixPath(normalized)
        if (
            path.is_absolute()
            or not path.parts
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise WorkerRuntimeError(f"{label} is not one safe repository-relative path.")
        candidate = (self.repository_root / Path(*path.parts)).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError(f"{label} escapes the repository root.") from exc
        return candidate

    @staticmethod
    def _normalize_heading(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()

    @classmethod
    def _sections(cls, text: str) -> dict[str, str]:
        matches = list(_HEADING_PATTERN.finditer(text))
        sections: dict[str, str] = {}
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            sections[cls._normalize_heading(match.group(1))] = text[start:end].strip()
        return sections

    @staticmethod
    def _front_matter(text: str) -> dict[str, str]:
        match = _FRONT_MATTER_PATTERN.search(text)
        if match is None:
            raise WorkerRuntimeError("Worker profile has no valid top-level front matter.")
        values: dict[str, str] = {}
        for raw_line in match.group("body").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise WorkerRuntimeError("Worker profile front matter contains an invalid line.")
            key, value = line.split(":", 1)
            clean_key = key.strip()
            clean_value = value.strip().strip("\"").strip("'")
            if not clean_key or not clean_value or clean_key in values:
                raise WorkerRuntimeError(
                    "Worker profile front matter contains an empty or duplicate field."
                )
            values[clean_key] = clean_value
        return values

    @staticmethod
    def _procedure_fields(text: str) -> dict[str, str]:
        return {
            match.group("name").casefold().replace(" ", "_"): match.group("value").strip()
            for match in _PROCEDURE_FIELD_PATTERN.finditer(text)
        }

    @staticmethod
    def _normalized_owner(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())

    @staticmethod
    def _expected_worker_title(route: DepartmentHqRoute) -> str:
        if not route.hq_chat_title.endswith("_HQ"):
            raise WorkerRuntimeError("Owning-HQ title cannot derive a canonical Worker title.")
        return route.hq_chat_title.removesuffix("_HQ") + "_Worker"

    def _runtime_rows(
        self,
        worker_id: str,
    ) -> tuple[
        dict[str, object] | None,
        dict[str, object] | None,
        dict[str, object] | None,
        list[dict[str, object]],
        list[ActivationFinding],
    ]:
        findings: list[ActivationFinding] = []
        registry: dict[str, object] | None = None
        route: dict[str, object] | None = None
        control: dict[str, object] | None = None
        unresolved_rows: list[dict[str, object]] = []
        try:
            connection = self._connect_read_only()
        except WorkerRuntimeError as exc:
            findings.append(
                self._finding(
                    "runtime.database",
                    "HOLD",
                    str(exc),
                    "SQLite Command Center runtime state",
                )
            )
            return registry, route, control, unresolved_rows, findings

        with connection:
            required_tables = {
                "worker_registry",
                "worker_route_state",
                "command_center_control",
            }
            missing_tables = [
                name for name in sorted(required_tables) if not self._table_exists(connection, name)
            ]
            if missing_tables:
                findings.append(
                    self._finding(
                        "runtime.tables",
                        "HOLD",
                        "Required runtime tables are missing: " + ", ".join(missing_tables),
                        "SQLite Command Center runtime state",
                    )
                )
                return registry, route, control, unresolved_rows, findings

            registry_rows = connection.execute(
                "SELECT * FROM worker_registry WHERE worker_id = ?",
                (worker_id,),
            ).fetchall()
            if len(registry_rows) != 1:
                findings.append(
                    self._finding(
                        "runtime.registry",
                        "HOLD",
                        (
                            "Worker registry entry is missing."
                            if not registry_rows
                            else "Worker registry contains ambiguous duplicate entries."
                        ),
                        "worker_registry",
                    )
                )
                return registry, route, control, unresolved_rows, findings
            registry = dict(registry_rows[0])

            duplicate_row = connection.execute(
                """
                SELECT
                    SUM(CASE WHEN chat_title = ? THEN 1 ELSE 0 END) AS title_count,
                    SUM(CASE WHEN profile_path = ? THEN 1 ELSE 0 END) AS profile_count
                FROM worker_registry
                """,
                (registry["chat_title"], registry["profile_path"]),
            ).fetchone()
            if (
                duplicate_row is None
                or int(duplicate_row["title_count"] or 0) != 1
                or int(duplicate_row["profile_count"] or 0) != 1
            ):
                findings.append(
                    self._finding(
                        "runtime.registry_uniqueness",
                        "HOLD",
                        "Worker title or profile path is not globally unique in the registry.",
                        "worker_registry",
                    )
                )
            else:
                findings.append(
                    self._finding(
                        "runtime.registry_uniqueness",
                        "PASS",
                        "Worker ID, visible title, and profile path resolve uniquely.",
                        "worker_registry",
                    )
                )

            route_rows = connection.execute(
                "SELECT * FROM worker_route_state WHERE worker_id = ?",
                (worker_id,),
            ).fetchall()
            if len(route_rows) == 1:
                route = dict(route_rows[0])
            else:
                findings.append(
                    self._finding(
                        "runtime.route_row",
                        "HOLD",
                        "Exactly one Worker route-state row is required.",
                        "worker_route_state",
                    )
                )

            control_rows = connection.execute(
                "SELECT * FROM command_center_control WHERE control_key = 'shared_pause'",
            ).fetchall()
            if len(control_rows) == 1:
                control = dict(control_rows[0])
            else:
                findings.append(
                    self._finding(
                        "runtime.control_row",
                        "HOLD",
                        "Exactly one shared Command Center control row is required.",
                        "command_center_control",
                    )
                )

            if self._table_exists(connection, "execution_history"):
                columns = self._table_columns(connection, "execution_history")
                selected = [
                    column
                    for column in (
                        "run_id",
                        "result_state",
                        "hq_review_state",
                        "requires_rob_validation",
                        "ready_for_consumption",
                    )
                    if column in columns
                ]
                if "run_id" in selected:
                    rows = connection.execute(
                        "SELECT " + ", ".join(selected) + " FROM execution_history "
                        "WHERE worker_id = ? ORDER BY id DESC LIMIT 100",
                        (worker_id,),
                    ).fetchall()
                    for row in rows:
                        values = dict(row)
                        result_state = str(values.get("result_state") or "")
                        review_state = str(values.get("hq_review_state") or "")
                        requires_rob = bool(values.get("requires_rob_validation") or 0)
                        ready = bool(values.get("ready_for_consumption") or 0)
                        if (
                            result_state in _UNRESOLVED_RESULT_STATES
                            or review_state in _UNRESOLVED_REVIEW_STATES
                            or (requires_rob and not ready)
                        ):
                            unresolved_rows.append(values)

        findings.append(
            self._finding(
                "runtime.database",
                "PASS",
                "Command Center state was read through a SQLite read-only connection.",
                "SQLite Command Center runtime state",
            )
        )
        return registry, route, control, unresolved_rows, findings

    def _profile_findings(
        self,
        entry: WorkerRegistryEntry,
    ) -> tuple[list[ActivationFinding], dict[str, str] | None]:
        findings: list[ActivationFinding] = []
        source = entry.profile_path
        try:
            profile_path = self._safe_repository_path(source, "Worker profile path")
        except WorkerRuntimeError as exc:
            return [self._finding("profile.path", "HOLD", str(exc), source)], None
        if not profile_path.is_file():
            return [
                self._finding(
                    "profile.path",
                    "HOLD",
                    "Worker profile does not exist at the registered path.",
                    source,
                )
            ], None
        try:
            text = profile_path.read_text(encoding="utf-8")
            metadata = self._front_matter(text)
        except (OSError, UnicodeDecodeError, WorkerRuntimeError) as exc:
            return [self._finding("profile.read", "HOLD", str(exc), source)], None

        missing_metadata = [key for key in _REQUIRED_PROFILE_METADATA if key not in metadata]
        forbidden = sorted(_FORBIDDEN_PROFILE_METADATA.intersection(metadata))
        expected = {
            "worker_id": entry.worker_id,
            "chat_title": entry.chat_title,
            "owning_department": entry.owning_department,
            "role": entry.role,
            "specialization": entry.specialization,
            "profile_version": str(entry.profile_version),
        }
        mismatched = [key for key, value in expected.items() if metadata.get(key) != value]
        if missing_metadata or forbidden or mismatched:
            detail: list[str] = []
            if missing_metadata:
                detail.append("missing " + ", ".join(missing_metadata))
            if forbidden:
                detail.append("forbidden " + ", ".join(forbidden))
            if mismatched:
                detail.append("registry mismatch " + ", ".join(mismatched))
            findings.append(
                self._finding(
                    "profile.metadata",
                    "HOLD",
                    "Worker profile metadata failed: " + "; ".join(detail) + ".",
                    source,
                )
            )
        else:
            findings.append(
                self._finding(
                    "profile.metadata",
                    "PASS",
                    "Required stable metadata matches the unique runtime registry entry.",
                    source,
                )
            )

        sections = self._sections(text)
        missing_sections = [
            heading
            for heading in _REQUIRED_PROFILE_SECTIONS
            if not sections.get(heading, "").strip()
        ]
        if missing_sections:
            findings.append(
                self._finding(
                    "profile.sections",
                    "HOLD",
                    "Required profile sections are missing or empty: "
                    + ", ".join(missing_sections)
                    + ".",
                    source,
                )
            )
        else:
            findings.append(
                self._finding(
                    "profile.sections",
                    "PASS",
                    "All contract-required profile authority and evidence sections are present.",
                    source,
                )
            )

        lower_text = text.casefold()
        retirement_ready = (
            "must not" in lower_text
            and "retire" in lower_text
            and "retires this profile" in lower_text
        )
        findings.append(
            self._finding(
                "profile.retirement",
                "PASS" if retirement_ready else "HOLD",
                (
                    "Profile reserves retirement and profile changes to the owning Department HQ."
                    if retirement_ready
                    else "Profile does not state both self-retirement prohibition and HQ retirement."
                ),
                source,
            )
        )
        return findings, metadata

    def _review_path_findings(
        self,
        entry: WorkerRegistryEntry,
    ) -> tuple[list[ActivationFinding], DepartmentHqRoute | None]:
        findings: list[ActivationFinding] = []
        try:
            route = resolve_department_hq_route(
                entry.owning_department,
                environment=self.environment,
            )
        except DepartmentHqRoutingError as exc:
            return [
                self._finding(
                    "review.route",
                    "HOLD",
                    str(exc),
                    "department_hq_routing.py",
                )
            ], None

        expected_title = self._expected_worker_title(route)
        findings.append(
            self._finding(
                "review.worker_title",
                "PASS" if entry.chat_title == expected_title else "HOLD",
                (
                    "Worker title matches the canonical owning-department Worker title."
                    if entry.chat_title == expected_title
                    else f"Worker title must be {expected_title!r}."
                ),
                "memory/HQ_NAMING_STANDARD.md",
            )
        )

        source = route.review_procedure_path
        try:
            procedure_path = self._safe_repository_path(source, "HQ review procedure path")
        except WorkerRuntimeError as exc:
            findings.append(self._finding("review.procedure_path", "HOLD", str(exc), source))
            return findings, route
        if not procedure_path.is_file():
            findings.append(
                self._finding(
                    "review.procedure_path",
                    "HOLD",
                    "Owning-HQ review procedure does not exist.",
                    source,
                )
            )
            return findings, route
        try:
            text = procedure_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(self._finding("review.procedure_read", "HOLD", str(exc), source))
            return findings, route

        fields = self._procedure_fields(text)
        required_fields = {
            "procedure_id",
            "procedure_version",
            "owner",
            "lifecycle_state",
        }
        missing_fields = sorted(required_fields.difference(fields))
        field_errors: list[str] = []
        if missing_fields:
            field_errors.append("missing " + ", ".join(missing_fields))
        try:
            if int(fields.get("procedure_version", "0")) < 1:
                field_errors.append("procedure version must be positive")
        except ValueError:
            field_errors.append("procedure version must be an integer")
        expected_owner = self._normalized_owner(route.hq_chat_title)
        if self._normalized_owner(fields.get("owner", "")) != expected_owner:
            field_errors.append("owner does not match the owning HQ")
        if fields.get("lifecycle_state", "").casefold() != "active":
            field_errors.append("lifecycle state is not Active")
        findings.append(
            self._finding(
                "review.procedure_metadata",
                "HOLD" if field_errors else "PASS",
                (
                    "HQ review procedure metadata failed: " + "; ".join(field_errors) + "."
                    if field_errors
                    else "HQ review procedure has an active owner-bound ID and version."
                ),
                source,
            )
        )

        sections = self._sections(text)
        missing_sections = [
            heading
            for heading in _REQUIRED_REVIEW_SECTIONS
            if not sections.get(heading, "").strip()
        ]
        findings.append(
            self._finding(
                "review.procedure_sections",
                "HOLD" if missing_sections else "PASS",
                (
                    "Required HQ review sections are missing or empty: "
                    + ", ".join(missing_sections)
                    + "."
                    if missing_sections
                    else "HQ review procedure defines authority, inputs, receipt, states, and ingestion."
                ),
                source,
            )
        )
        return findings, route

    def report(self, worker_id: str) -> WorkerActivationReadinessReport:
        clean_worker_id = str(worker_id or "").strip()
        findings: list[ActivationFinding] = []
        registry_values, route_values, control, unresolved, runtime_findings = self._runtime_rows(
            clean_worker_id
        )
        findings.extend(runtime_findings)

        if not _WORKER_ID_PATTERN.fullmatch(clean_worker_id):
            findings.append(
                self._finding(
                    "worker_id",
                    "HOLD",
                    "Worker ID must use lowercase letters, numbers, and underscores only.",
                    "coordination/WORKER_EXECUTION_CONTRACT.md",
                )
            )
            return self._report(clean_worker_id, findings, registry_values, None)

        entry: WorkerRegistryEntry | None = None
        if registry_values is not None:
            try:
                entry = WorkerRegistryEntry.from_dict(registry_values)
            except WorkerRuntimeError as exc:
                findings.append(
                    self._finding(
                        "runtime.registry_contract",
                        "HOLD",
                        str(exc),
                        "worker_registry",
                    )
                )
            else:
                findings.append(
                    self._finding(
                        "runtime.registry_contract",
                        "PASS",
                        "Registry entry satisfies the stable Worker runtime contract.",
                        "worker_registry",
                    )
                )
                findings.append(
                    self._finding(
                        "runtime.deployment_state",
                        "HOLD" if entry.deployment_state == "retired" else "PASS",
                        (
                            "Retired Workers require owning-department reactivation authority."
                            if entry.deployment_state == "retired"
                            else (
                                "Deployment state is registered and not retired: "
                                f"{entry.deployment_state}."
                            )
                        ),
                        "worker_registry",
                    )
                )

        hq_route: DepartmentHqRoute | None = None
        if entry is not None:
            profile_findings, _ = self._profile_findings(entry)
            findings.extend(profile_findings)
            review_findings, hq_route = self._review_path_findings(entry)
            findings.extend(review_findings)

            if not entry.conversation_url or entry.route_revision < 1:
                findings.append(
                    self._finding(
                        "runtime.route_identity",
                        "HOLD",
                        "One registered exact conversation URL and positive route revision are required.",
                        "worker_registry",
                    )
                )
            else:
                findings.append(
                    self._finding(
                        "runtime.route_identity",
                        "PASS",
                        "An exact ChatGPT conversation URL and positive route revision are registered.",
                        "worker_registry",
                    )
                )

            if route_values is not None:
                availability = str(route_values.get("availability") or "unknown")
                pause_reason = str(route_values.get("pause_reason") or "").strip()
                ready_route = availability == "available" and not pause_reason
                findings.append(
                    self._finding(
                        "runtime.route_availability",
                        "PASS" if ready_route else "HOLD",
                        (
                            "Route is available with no route-specific hold."
                            if ready_route
                            else (
                                f"Route is {availability}."
                                + (f" Hold: {pause_reason}" if pause_reason else "")
                            )
                        ),
                        "worker_route_state",
                    )
                )

        if control is not None:
            paused = bool(control.get("paused") or 0)
            findings.append(
                self._finding(
                    "runtime.shared_pause",
                    "HOLD" if paused else "PASS",
                    (
                        "Shared automation pause is active."
                        if paused
                        else "Shared automation pause is clear."
                    ),
                    "command_center_control",
                )
            )
            budget_fields = {
                "send_budget_limit",
                "send_budget_used",
                "send_budget_epoch",
            }
            missing_budget = sorted(budget_fields.difference(control))
            if missing_budget:
                findings.append(
                    self._finding(
                        "runtime.send_budget",
                        "HOLD",
                        "Send-budget fields are missing: " + ", ".join(missing_budget) + ".",
                        "command_center_control",
                    )
                )
            else:
                try:
                    limit = int(control["send_budget_limit"])
                    used = int(control["send_budget_used"])
                    epoch = int(control["send_budget_epoch"])
                    remaining = limit - used
                    valid_budget = limit >= 1 and epoch >= 1 and 0 <= used < limit
                except (TypeError, ValueError):
                    valid_budget = False
                    limit = used = remaining = epoch = 0
                findings.append(
                    self._finding(
                        "runtime.send_budget",
                        "PASS" if valid_budget else "HOLD",
                        (
                            f"Send-budget epoch {epoch} has {remaining} of {limit} attempts remaining."
                            if valid_budget
                            else "Send-budget state is malformed or exhausted."
                        ),
                        "command_center_control",
                    )
                )

        findings.append(
            self._finding(
                "runtime.unresolved_holds",
                "HOLD" if unresolved else "PASS",
                (
                    "Unresolved Worker verification or repair runs remain: "
                    + ", ".join(str(row.get("run_id") or "unknown") for row in unresolved)
                    + "."
                    if unresolved
                    else "No unresolved repair or Rob-validation rows were found."
                ),
                "execution_history",
            )
        )

        findings.extend(
            (
                self._finding(
                    "authority.owning_department",
                    "NOT_APPLICABLE",
                    "Technical readiness does not prove owning-department activation authority.",
                    "coordination/WORKER_EXECUTION_CONTRACT.md §6",
                ),
                self._finding(
                    "authority.maintenance",
                    "NOT_APPLICABLE",
                    "Technical readiness does not prove Maintenance shared-governance review.",
                    "coordination/WORKER_EXECUTION_CONTRACT.md §17",
                ),
                self._finding(
                    "authority.rob",
                    "NOT_APPLICABLE",
                    "Technical readiness never substitutes for Rob approval when §6 requires it.",
                    "coordination/WORKER_EXECUTION_CONTRACT.md §6",
                ),
            )
        )
        return self._report(clean_worker_id, findings, registry_values, hq_route)

    @staticmethod
    def _report(
        worker_id: str,
        findings: list[ActivationFinding],
        registry: dict[str, object] | None,
        hq_route: DepartmentHqRoute | None,
    ) -> WorkerActivationReadinessReport:
        technical_ready = not any(finding.state == "HOLD" for finding in findings)
        state: ReadinessState = (
            "READY_FOR_AUTHORITY_REVIEW" if technical_ready else "HOLD"
        )
        return WorkerActivationReadinessReport(
            report_version=1,
            worker_id=worker_id,
            state=state,
            technical_ready=technical_ready,
            activation_authorized=False,
            findings=tuple(findings),
            registry=registry,
            hq_route=asdict(hq_route) if hq_route is not None else None,
        )


__all__ = [
    "ActivationFinding",
    "FindingState",
    "ReadinessState",
    "WorkerActivationReadinessReport",
    "WorkerActivationReadinessService",
]
