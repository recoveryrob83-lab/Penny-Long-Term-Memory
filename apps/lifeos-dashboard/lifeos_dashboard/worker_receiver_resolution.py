"""Resolve canonical advisory sources into one semantic receiver assignment."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, cast

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_procedure_resolution import load_canonical_procedure
from .worker_profile_resolution import load_worker_authority_profile
from .worker_source_resolution import clean_inline, read_relative
from .worker_receiver import (
    CanonicalProcedureSpec,
    ReceiverAssignment,
    WorkerAuthorityProfile,
)
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError

_HEADING_PATTERN = re.compile(
    r"^### (?P<advisory_id>ADV-[A-Z0-9-]+)(?:\s+—\s+.*)?$", re.MULTILINE
)
_FIELD_PATTERN = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$", re.MULTILINE)


@dataclass(frozen=True)
class ReceiverResolution:
    assignment: ReceiverAssignment
    profile: WorkerAuthorityProfile
    procedure: CanonicalProcedureSpec
    profile_path: str
    procedure_path: str


def _bool_field(fields: Mapping[str, str], key: str) -> bool:
    raw = fields.get(key, "false").strip().lower()
    if raw not in {"true", "false"}:
        raise WorkerRuntimeError(f"Advisory field {key} must be true or false.")
    return raw == "true"


def _json_advisory_field(
    fields: Mapping[str, str], key: str, expected_type: type
) -> object:
    raw = fields.get(key, "").strip()
    if not raw:
        raise WorkerRuntimeError(f"Execution-ready advisory is missing {key}.")
    try:
        value = json.loads(clean_inline(raw))
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError(f"Advisory field {key} is not valid JSON.") from exc
    if not isinstance(value, expected_type):
        raise WorkerRuntimeError(f"Advisory field {key} has the wrong JSON shape.")
    if expected_type is list and not all(isinstance(item, str) for item in value):
        raise WorkerRuntimeError(f"Advisory field {key} must be an array of strings.")
    return value


def _advisory_fields(board_text: str, advisory_id: str) -> dict[str, str]:
    matches = list(_HEADING_PATTERN.finditer(board_text))
    for index, match in enumerate(matches):
        if match.group("advisory_id") != advisory_id:
            continue
        start = match.end()
        end = (
            matches[index + 1].start() if index + 1 < len(matches) else len(board_text)
        )
        return {
            field.group("key").strip(): clean_inline(field.group("value"))
            for field in _FIELD_PATTERN.finditer(board_text[start:end])
        }
    raise WorkerRuntimeError(
        f"Advisory {advisory_id} is missing from its source board."
    )


def _assert_stable_advisory_fields(
    fields: Mapping[str, str], advisory: ExecutionReadyAdvisory
) -> None:
    if fields.get("Authorization Class", "").upper() != advisory.authorization_class:
        raise WorkerRuntimeError(
            "Advisory authorization class changed after dispatch resolution."
        )
    if fields.get("Procedure ID", "") != advisory.procedure_id:
        raise WorkerRuntimeError(
            "Advisory procedure ID changed after dispatch resolution."
        )
    try:
        procedure_version = int(fields.get("Procedure Version", "0"))
    except ValueError as exc:
        raise WorkerRuntimeError("Advisory procedure version is invalid.") from exc
    if procedure_version != advisory.procedure_version:
        raise WorkerRuntimeError(
            "Advisory procedure version changed after dispatch resolution."
        )
    if fields.get("Authorization Source", "") != advisory.authorization_source:
        raise WorkerRuntimeError(
            "Advisory authorization source changed after dispatch resolution."
        )


def resolve_receiver_assignment(
    repository_root: Path,
    advisory: ExecutionReadyAdvisory,
    entry: WorkerRegistryEntry,
) -> ReceiverResolution:
    repository_root = repository_root.resolve()
    profile, department_labels = load_worker_authority_profile(
        repository_root, entry, advisory
    )
    if advisory.target_department not in department_labels:
        raise WorkerRuntimeError(
            "Advisory target department is not an approved label for the Worker owner."
        )
    procedure, procedure_path = load_canonical_procedure(
        repository_root, entry, advisory
    )
    fields = _advisory_fields(
        read_relative(repository_root, advisory.board_path), advisory.advisory_id
    )
    _assert_stable_advisory_fields(fields, advisory)
    parameters = _json_advisory_field(fields, "Parameters JSON", dict)
    source_references = _json_advisory_field(fields, "Source References JSON", list)
    requested_read_scopes = _json_advisory_field(
        fields, "Requested Read Scopes JSON", list
    )
    requested_write_scopes = _json_advisory_field(
        fields, "Requested Write Scopes JSON", list
    )
    requested_tools = _json_advisory_field(fields, "Requested Tools JSON", list)
    procedure_checksum = fields.get("Procedure Checksum", "").strip()
    parameters_checksum = fields.get("Parameters Checksum", "").strip()
    if not procedure_checksum:
        raise WorkerRuntimeError(
            "Execution-ready advisory is missing Procedure Checksum."
        )
    if not parameters_checksum:
        raise WorkerRuntimeError(
            "Execution-ready advisory is missing Parameters Checksum."
        )

    assignment = ReceiverAssignment(
        envelope=advisory.envelope(),
        target_department=entry.owning_department,
        task_class=advisory.task_class,
        authorization_class=cast(str, advisory.authorization_class),
        procedure_checksum=procedure_checksum,
        parameters=cast(Mapping[str, object], parameters),
        parameters_checksum=parameters_checksum,
        source_references=tuple(cast(list[str], source_references)),
        requested_read_scopes=tuple(cast(list[str], requested_read_scopes)),
        requested_write_scopes=tuple(cast(list[str], requested_write_scopes)),
        requested_tools=tuple(cast(list[str], requested_tools)),
        approval_reference=fields.get("Approval Reference") or None,
        requests_new_authority=_bool_field(fields, "Requests New Authority"),
        requests_new_spending=_bool_field(fields, "Requests New Spending"),
        requests_new_connector=_bool_field(fields, "Requests New Connector"),
        requests_cross_department_authority=_bool_field(
            fields, "Requests Cross-Department Authority"
        ),
        requests_material_exception=_bool_field(fields, "Requests Material Exception"),
        transport_scope_change_detected=_bool_field(
            fields, "Transport Scope Change Detected"
        ),
    )
    return ReceiverResolution(
        assignment=assignment,
        profile=profile,
        procedure=procedure,
        profile_path=entry.profile_path,
        procedure_path=procedure_path,
    )


__all__ = ["ReceiverResolution", "resolve_receiver_assignment"]
