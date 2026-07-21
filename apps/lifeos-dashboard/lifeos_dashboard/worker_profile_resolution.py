"""Resolve one department-owned Worker profile into receiver authority."""

from __future__ import annotations

import re
from pathlib import Path
from typing import cast

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_receiver import WorkerAuthorityProfile
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from .worker_source_resolution import (
    front_matter,
    json_value,
    positive_int_value,
    read_relative,
    section,
    string_tuple_value,
)


def _prose_scope_prefixes(text: str, heading: str) -> tuple[str, ...]:
    active = section(text, heading)
    if heading == "Write scope":
        active = active.split("All writes must", 1)[0]
        active = active.split("The Worker has no standing authority", 1)[0]
    values: list[str] = []
    for value in re.findall(r"`([^`]+)`", active):
        clean = value.strip().rstrip(";")
        if clean.startswith(
            ("projects/", "apps/", "memory/", "coordination/")
        ) or clean.endswith(":"):
            values.append(clean.rstrip("/"))
    if heading == "Read scope" and (
        "canonical shared operating contracts named by the task" in active
        or "required Boot path" in active
    ):
        values.extend(("memory", "coordination"))
    return tuple(dict.fromkeys(values))


def _task_class_allowed_by_prose(task_class: str, text: str) -> bool:
    normalized = task_class.lower().replace("-", "_")
    prose = text.lower()
    checks = (
        (
            "read_only" in normalized and "verification" in normalized,
            "read-only verification",
        ),
        ("maintenance" in normalized, "bounded maintenance"),
        (
            "implementation" in normalized or "repair" in normalized,
            "bounded implementation or repair",
        ),
        (
            "debug" in normalized or "test" in normalized or "regression" in normalized,
            "focused debugging, test execution, regression verification",
        ),
        ("evidence" in normalized, "evidence collection"),
    )
    return any(condition and phrase in prose for condition, phrase in checks)


def _calling_source_allowed_by_prose(source: str, text: str) -> bool:
    normalized = source.strip().upper().replace(" ", "_")
    prose = text.lower()
    if normalized.startswith("ROB"):
        return "rob" in prose
    if normalized.startswith("ENGINEERING_HQ"):
        return "engineering hq" in prose
    if normalized.startswith("CHIEF_OF_STAFF_HQ"):
        return "chief of staff hq" in prose
    return False


def _approved_tools_from_prose(text: str) -> tuple[str, ...]:
    active = section(text, "Approved connectors and tools").lower()
    tools: list[str] = []
    if "github read operations" in active or "github write operations" in active:
        tools.append("GitHub")
    if "local file" in active:
        tools.append("local_file")
    if "terminal" in active:
        tools.append("terminal")
    if "test tools" in active:
        tools.append("tests")
    if "runtime evidence" in active:
        tools.append("runtime_evidence")
    return tuple(tools)


def load_worker_authority_profile(
    repository_root: Path,
    entry: WorkerRegistryEntry,
    advisory: ExecutionReadyAdvisory,
) -> tuple[WorkerAuthorityProfile, tuple[str, ...]]:
    text = read_relative(repository_root, entry.profile_path)
    metadata = front_matter(text)
    if metadata.get("worker_id") != entry.worker_id:
        raise WorkerRuntimeError("Worker profile ID conflicts with the registry.")
    if metadata.get("owning_department") != entry.owning_department:
        raise WorkerRuntimeError(
            "Worker profile department conflicts with the registry."
        )
    if positive_int_value(metadata, "profile_version") != entry.profile_version:
        raise WorkerRuntimeError("Worker profile version conflicts with the registry.")

    if metadata.get("receiver_allowed_task_classes_json"):
        calling_raw = json_value(
            metadata, "receiver_calling_source_task_classes_json", dict
        )
        assert isinstance(calling_raw, dict)
        calling: dict[str, tuple[str, ...]] = {}
        for source, task_classes in calling_raw.items():
            if (
                not isinstance(source, str)
                or not source.strip()
                or not isinstance(task_classes, list)
            ):
                raise WorkerRuntimeError(
                    "Worker calling-source receiver contract is invalid."
                )
            if not all(isinstance(item, str) and item.strip() for item in task_classes):
                raise WorkerRuntimeError(
                    "Worker calling-source task classes must be strings."
                )
            calling[source.strip()] = tuple(item.strip() for item in task_classes)
        allowed_task_classes = string_tuple_value(
            metadata, "receiver_allowed_task_classes_json"
        )
        read_scope_prefixes = string_tuple_value(
            metadata, "receiver_read_scope_prefixes_json"
        )
        write_scope_prefixes = string_tuple_value(
            metadata, "receiver_write_scope_prefixes_json"
        )
        approved_tools = string_tuple_value(metadata, "receiver_approved_tools_json")
        allowed_verification_modes = cast(
            tuple,
            string_tuple_value(metadata, "receiver_allowed_verification_modes_json"),
        )
        prohibited_task_classes = string_tuple_value(
            metadata, "receiver_prohibited_task_classes_json"
        )
        labels = string_tuple_value(metadata, "receiver_department_labels_json")
    else:
        if not _task_class_allowed_by_prose(advisory.task_class, text):
            raise WorkerRuntimeError(
                "Worker profile prose does not authorize the advisory task class."
            )
        if not _calling_source_allowed_by_prose(advisory.authorization_source, text):
            raise WorkerRuntimeError(
                "Worker profile prose does not authorize the advisory calling source."
            )
        if f"`{advisory.verification_mode}`" not in text:
            raise WorkerRuntimeError(
                "Worker profile prose does not authorize the verification mode."
            )
        allowed_task_classes = (advisory.task_class,)
        read_scope_prefixes = _prose_scope_prefixes(text, "Read scope")
        write_scope_prefixes = _prose_scope_prefixes(text, "Write scope")
        approved_tools = _approved_tools_from_prose(text)
        calling = {advisory.authorization_source: (advisory.task_class,)}
        allowed_verification_modes = cast(tuple, (advisory.verification_mode,))
        prohibited_task_classes = ()
        labels = (
            entry.owning_department,
            f"{entry.owning_department.replace('-', ' ').title()} HQ",
        )

    profile = WorkerAuthorityProfile(
        worker_id=entry.worker_id,
        owning_department=entry.owning_department,
        profile_version=entry.profile_version,
        allowed_task_classes=allowed_task_classes,
        read_scope_prefixes=read_scope_prefixes,
        write_scope_prefixes=write_scope_prefixes,
        approved_tools=approved_tools,
        calling_source_task_classes=calling,
        allowed_verification_modes=allowed_verification_modes,
        prohibited_task_classes=prohibited_task_classes,
    )
    return profile, labels


__all__ = [
    "load_worker_authority_profile",
]
