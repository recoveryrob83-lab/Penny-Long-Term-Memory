"""Convert canonical execution-ready advisories into reference-only Worker wake jobs.

The Advisory Index is the routing dashboard. Source boards remain authoritative. This module
checks only the minimum machine-readable wake schema, then passes a reference-only job to the
existing Worker Command Center. It does not interpret the assignment, create authority, update
advisory lifecycle, or close work.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

from .worker_command_center import WorkerCommandJob, WorkerExecutionResult
from .worker_runtime import ExecutionEnvelope, VerificationMode, WorkerRuntimeError

_INDEX_OPEN_PATTERN = re.compile(
    r"^- (?P<advisory_id>ADV-[A-Z0-9-]+) — OPEN — Posted Board: `(?P<board>[^`]+)` "
    r"— Target Department: (?P<department>.+?) — (?P<summary>.+)$"
)
_HEADING_PATTERN = re.compile(
    r"^### (?P<advisory_id>ADV-[A-Z0-9-]+)(?:\s+—\s+(?P<title>.*))?$",
    re.M,
)
_FIELD_PATTERN = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$", re.M)
_WORKER_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_ALLOWED_VERIFICATION_MODES = {"AUTOMATIC", "ROUTINE_BATCH", "IMMEDIATE_HQ"}
_ALLOWED_PRIORITIES = {"LOW", "NORMAL", "HIGH", "URGENT"}
_ALLOWED_AUTHORIZATION_CLASSES = {"READ_ONLY", "BOUNDED_WRITE", "APPROVAL_REQUIRED"}
_REQUIRED_FIELDS = (
    "Lifecycle State",
    "Priority",
    "Advisory Revision",
    "Verification Mode",
    "Target Department and Owner",
    "Task Class",
    "Authorization Class",
    "Procedure ID",
    "Procedure Version",
    "Authorization Source",
    "Parameters JSON",
    "Source References JSON",
    "Requested Read Scopes JSON",
    "Requested Write Scopes JSON",
    "Requested Tools JSON",
    "Completion Condition",
)


class WorkerCommandCenter(Protocol):
    def execute(
        self,
        job: WorkerCommandJob,
        *,
        trigger: str = "manual",
        timeout_seconds: int = 120,
    ) -> WorkerExecutionResult: ...


@dataclass(frozen=True)
class AdvisoryIndexRecord:
    advisory_id: str
    board_path: str
    target_department: str
    summary: str


@dataclass(frozen=True)
class ExecutionReadyAdvisory:
    advisory_id: str
    title: str
    board_path: str
    target_department: str
    target_worker_id: str
    advisory_revision: int
    task_class: str
    authorization_class: str
    procedure_id: str
    procedure_version: int
    authorization_source: str
    verification_mode: VerificationMode
    lifecycle_state: str
    priority: str

    @property
    def wrapper_id(self) -> str:
        return f"WAKE-{self.advisory_id}-R{self.advisory_revision}"

    @property
    def run_id(self) -> str:
        return f"RUN-{self.advisory_id}-R{self.advisory_revision}"

    def envelope(self) -> ExecutionEnvelope:
        return ExecutionEnvelope(
            wrapper_id=self.wrapper_id,
            run_id=self.run_id,
            worker_id=self.target_worker_id,
            task_id=self.advisory_id,
            task_revision=self.advisory_revision,
            procedure_id=self.procedure_id,
            procedure_version=self.procedure_version,
            authorization_source=self.authorization_source,
            verification_mode=self.verification_mode,
        )


@dataclass(frozen=True)
class AdvisoryWakeDispatch:
    advisory: ExecutionReadyAdvisory
    job: WorkerCommandJob
    result: WorkerExecutionResult


def _clean_inline(value: str) -> str:
    clean = value.strip()
    if len(clean) >= 2 and clean[0] == clean[-1] == "`":
        return clean[1:-1].strip()
    return clean


def _positive_int(value: str, field_name: str) -> int:
    try:
        parsed = int(_clean_inline(value))
    except (TypeError, ValueError) as exc:
        raise WorkerRuntimeError(f"{field_name} must be a positive integer.") from exc
    if parsed < 1:
        raise WorkerRuntimeError(f"{field_name} must be a positive integer.")
    return parsed


def _parse_json_field(value: str, field_name: str, expected_type: type) -> object:
    try:
        parsed = json.loads(_clean_inline(value))
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError(f"{field_name} must contain valid JSON.") from exc
    if not isinstance(parsed, expected_type):
        raise WorkerRuntimeError(f"{field_name} has the wrong JSON shape.")
    if expected_type is list and not all(isinstance(item, str) for item in parsed):
        raise WorkerRuntimeError(f"{field_name} must be a JSON array of strings.")
    return parsed


def parse_advisory_index(index_text: str) -> tuple[AdvisoryIndexRecord, ...]:
    """Return OPEN advisory routing records from the canonical Advisory Index."""

    records: list[AdvisoryIndexRecord] = []
    for raw_line in index_text.splitlines():
        match = _INDEX_OPEN_PATTERN.match(raw_line.strip())
        if not match:
            continue
        records.append(
            AdvisoryIndexRecord(
                advisory_id=match.group("advisory_id"),
                board_path=match.group("board"),
                target_department=match.group("department").strip(),
                summary=match.group("summary").strip(),
            )
        )
    return tuple(records)


def _advisory_section(board_text: str, advisory_id: str) -> tuple[str, str]:
    matches = list(_HEADING_PATTERN.finditer(board_text))
    for index, match in enumerate(matches):
        if match.group("advisory_id") != advisory_id:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(board_text)
        return (match.group("title") or "").strip(), board_text[start:end]
    raise WorkerRuntimeError(f"Advisory {advisory_id} was not found on its posted board.")


def _metadata(section: str) -> dict[str, str]:
    return {
        match.group("key").strip(): _clean_inline(match.group("value"))
        for match in _FIELD_PATTERN.finditer(section)
    }


def parse_execution_ready_advisory(
    board_text: str,
    index_record: AdvisoryIndexRecord,
) -> ExecutionReadyAdvisory | None:
    """Resolve one advisory. Return None when it is not targeted to a Worker."""

    title, section = _advisory_section(board_text, index_record.advisory_id)
    fields = _metadata(section)
    target_worker_id = fields.get("Target Worker ID", "").strip()
    if not target_worker_id:
        return None
    missing = [field for field in _REQUIRED_FIELDS if not fields.get(field, "").strip()]
    if missing:
        raise WorkerRuntimeError(
            f"Execution-ready advisory {index_record.advisory_id} is missing fields: {missing}"
        )

    lifecycle = fields["Lifecycle State"].strip().upper()
    if lifecycle != "OPEN":
        raise WorkerRuntimeError(
            f"Advisory {index_record.advisory_id} is indexed OPEN but its source "
            f"lifecycle is {lifecycle}."
        )
    source_department = fields["Target Department and Owner"].strip()
    if source_department != index_record.target_department:
        raise WorkerRuntimeError(
            f"Advisory {index_record.advisory_id} target department conflicts with "
            "the Advisory Index."
        )
    if not _WORKER_ID_PATTERN.fullmatch(target_worker_id):
        raise WorkerRuntimeError("Target Worker ID is invalid.")

    verification = fields["Verification Mode"].strip().upper()
    if verification not in _ALLOWED_VERIFICATION_MODES:
        raise WorkerRuntimeError("Verification Mode is invalid.")
    priority = fields["Priority"].strip().upper()
    if priority not in _ALLOWED_PRIORITIES:
        raise WorkerRuntimeError("Priority is invalid.")
    authorization_class = fields["Authorization Class"].strip().upper()
    if authorization_class not in _ALLOWED_AUTHORIZATION_CLASSES:
        raise WorkerRuntimeError("Authorization Class is invalid.")

    _parse_json_field(fields["Parameters JSON"], "Parameters JSON", dict)
    _parse_json_field(fields["Source References JSON"], "Source References JSON", list)
    _parse_json_field(fields["Requested Read Scopes JSON"], "Requested Read Scopes JSON", list)
    _parse_json_field(fields["Requested Write Scopes JSON"], "Requested Write Scopes JSON", list)
    _parse_json_field(fields["Requested Tools JSON"], "Requested Tools JSON", list)

    return ExecutionReadyAdvisory(
        advisory_id=index_record.advisory_id,
        title=title,
        board_path=index_record.board_path,
        target_department=source_department,
        target_worker_id=target_worker_id,
        advisory_revision=_positive_int(fields["Advisory Revision"], "Advisory Revision"),
        task_class=fields["Task Class"].strip(),
        authorization_class=authorization_class,
        procedure_id=fields["Procedure ID"].strip(),
        procedure_version=_positive_int(fields["Procedure Version"], "Procedure Version"),
        authorization_source=fields["Authorization Source"].strip(),
        verification_mode=cast(VerificationMode, verification),
        lifecycle_state=lifecycle,
        priority=priority,
    )


def render_reference_only_instruction(advisory: ExecutionReadyAdvisory) -> str:
    """Render a wake instruction that points to canonical truth without copying the task."""

    return (
        f"Wake for canonical advisory {advisory.advisory_id}, revision "
        f"{advisory.advisory_revision}, posted at `{advisory.board_path}`.\n\n"
        "Do not execute from this transport text. Load the canonical Worker boot path, your exact "
        "department-owned profile, and the named advisory revision. Validate caller authority, "
        "ownership, task class, procedure, parameters, scopes, tools, verification mode, "
        "pause state, and duplicate state before accepting it. If valid, consume only this "
        "revision, perform only the bounded work in the advisory, preserve run-linked evidence, "
        "update the same authoritative "
        "advisory or run record only as authorized, and return exactly one controlled outcome: "
        "IMPLEMENT, REPORT_AND_HOLD, or ELEVATE_FOR_APPROVAL. Do not close the advisory unless the "
        "canonical advisory explicitly delegates closure and its verification condition is "
        "satisfied."
    )


def build_wake_job(
    advisory: ExecutionReadyAdvisory,
    *,
    mode: str = "send",
    confirm_send: bool = True,
) -> WorkerCommandJob:
    return WorkerCommandJob(
        envelope=advisory.envelope(),
        instruction=render_reference_only_instruction(advisory),
        mode=mode,
        confirm_send=confirm_send,
    )


class AdvisoryWakePipeline:
    """Read canonical advisory routing state and dispatch reference-only Worker wakes."""

    def __init__(
        self,
        repository_root: Path,
        command_center: WorkerCommandCenter,
        *,
        advisory_index_path: str = "coordination/ADVISORY_INDEX.md",
    ) -> None:
        self.repository_root = repository_root.resolve()
        self.command_center = command_center
        self.advisory_index_path = advisory_index_path

    def _read(self, relative_path: str) -> str:
        candidate = (self.repository_root / relative_path).resolve()
        try:
            candidate.relative_to(self.repository_root)
        except ValueError as exc:
            raise WorkerRuntimeError("Advisory path escapes the repository root.") from exc
        if not candidate.is_file():
            raise WorkerRuntimeError(f"Required advisory source is missing: {relative_path}")
        return candidate.read_text(encoding="utf-8")

    def discover(self) -> tuple[ExecutionReadyAdvisory, ...]:
        records = parse_advisory_index(self._read(self.advisory_index_path))
        advisories: list[ExecutionReadyAdvisory] = []
        for record in records:
            resolved = parse_execution_ready_advisory(self._read(record.board_path), record)
            if resolved is not None:
                advisories.append(resolved)
        return tuple(advisories)

    def _dispatch_resolved(
        self,
        advisory: ExecutionReadyAdvisory,
        *,
        mode: str,
        confirm_send: bool,
        trigger: str,
        timeout_seconds: int,
    ) -> AdvisoryWakeDispatch:
        job = build_wake_job(advisory, mode=mode, confirm_send=confirm_send)
        result = self.command_center.execute(
            job,
            trigger=trigger,
            timeout_seconds=timeout_seconds,
        )
        return AdvisoryWakeDispatch(advisory=advisory, job=job, result=result)

    def dispatch(
        self,
        advisory_id: str,
        *,
        mode: str = "send",
        confirm_send: bool = True,
        trigger: str = "scheduled",
        timeout_seconds: int = 120,
    ) -> AdvisoryWakeDispatch:
        matches = [item for item in self.discover() if item.advisory_id == advisory_id]
        if not matches:
            raise WorkerRuntimeError(
                f"No OPEN execution-ready Worker advisory matches {advisory_id}."
            )
        if len(matches) > 1:
            raise WorkerRuntimeError(f"Advisory {advisory_id} resolved ambiguously.")
        return self._dispatch_resolved(
            matches[0],
            mode=mode,
            confirm_send=confirm_send,
            trigger=trigger,
            timeout_seconds=timeout_seconds,
        )

    def dispatch_all(
        self,
        *,
        mode: str = "send",
        confirm_send: bool = True,
        trigger: str = "scheduled",
        timeout_seconds: int = 120,
    ) -> tuple[AdvisoryWakeDispatch, ...]:
        advisories = self.discover()
        return tuple(
            self._dispatch_resolved(
                advisory,
                mode=mode,
                confirm_send=confirm_send,
                trigger=trigger,
                timeout_seconds=timeout_seconds,
            )
            for advisory in advisories
        )
