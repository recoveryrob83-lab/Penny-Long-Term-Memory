"""Resolve one canonical Worker procedure into receiver semantics."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping, cast

from .worker_advisory_pipeline import ExecutionReadyAdvisory
from .worker_source_resolution import (
    front_matter,
    json_value,
    positive_int_value,
    read_relative,
    section,
    string_tuple_value,
)
from .worker_receiver import CanonicalProcedureSpec
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError


def _parameter_schema_from_prose(text: str) -> dict[str, str]:
    active = section(text, "Required Parameters")
    schema: dict[str, str] = {}
    for name, description in re.findall(r"- `([^`]+)`:([^\n]+)", active):
        lower = description.lower()
        if "json array" in lower:
            expected = "array"
        elif "json object" in lower:
            expected = "object"
        elif "boolean" in lower:
            expected = "boolean"
        elif "integer" in lower:
            expected = "integer"
        elif "number" in lower:
            expected = "number"
        else:
            expected = "string"
        schema[name.strip()] = expected
    if not schema:
        raise WorkerRuntimeError(
            "Canonical procedure does not expose a receiver parameter schema."
        )
    return schema


def _authorization_classes(text: str, metadata: Mapping[str, str]) -> tuple[str, ...]:
    if metadata.get("receiver_allowed_authorization_classes_json"):
        return string_tuple_value(
            metadata, "receiver_allowed_authorization_classes_json"
        )
    match = re.search(
        r"^authorization_classes:\s*$((?:\n\s+-\s+[^\n]+)+)",
        text,
        re.MULTILINE,
    )
    if not match:
        raise WorkerRuntimeError(
            "Canonical procedure is missing authorization_classes."
        )
    return tuple(
        item.strip()
        for item in re.findall(r"^\s+-\s+([^\n]+)$", match.group(1), re.MULTILINE)
    )


def load_canonical_procedure(
    repository_root: Path,
    entry: WorkerRegistryEntry,
    advisory: ExecutionReadyAdvisory,
) -> tuple[CanonicalProcedureSpec, str]:
    relative_path = (
        f"projects/{entry.owning_department}/procedures/{advisory.procedure_id}.md"
    )
    text = read_relative(repository_root, relative_path)
    metadata = front_matter(text)
    if metadata.get("procedure_id") != advisory.procedure_id:
        raise WorkerRuntimeError("Canonical procedure ID conflicts with the advisory.")
    if positive_int_value(metadata, "procedure_version") != advisory.procedure_version:
        raise WorkerRuntimeError(
            "Canonical procedure version conflicts with the advisory."
        )
    if metadata.get("owning_department") != entry.owning_department:
        raise WorkerRuntimeError(
            "Canonical procedure department conflicts with the Worker."
        )
    if metadata.get("task_class") != advisory.task_class:
        raise WorkerRuntimeError(
            "Canonical procedure task class conflicts with the advisory."
        )

    if metadata.get("receiver_parameter_schema_json"):
        schema_raw = json_value(metadata, "receiver_parameter_schema_json", dict)
        assert isinstance(schema_raw, dict)
        if not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in schema_raw.items()
        ):
            raise WorkerRuntimeError("Procedure receiver parameter schema is invalid.")
        parameter_schema = {str(key): str(value) for key, value in schema_raw.items()}
        required_parameters = string_tuple_value(
            metadata, "receiver_required_parameters_json"
        )
        approved_tools = string_tuple_value(metadata, "receiver_approved_tools_json")
        source_required = metadata.get(
            "receiver_source_references_required", "true"
        ).lower()
    else:
        parameter_schema = _parameter_schema_from_prose(text)
        required_parameters = tuple(parameter_schema)
        approved_tools = ("GitHub",) if "GitHub" in text else ()
        source_required = "true"
    if source_required not in {"true", "false"}:
        raise WorkerRuntimeError(
            "Procedure receiver_source_references_required must be true or false."
        )
    procedure = CanonicalProcedureSpec(
        procedure_id=advisory.procedure_id,
        procedure_version=advisory.procedure_version,
        task_class=advisory.task_class,
        canonical_text=text,
        parameter_schema=parameter_schema,
        required_parameters=required_parameters,
        allowed_authorization_classes=cast(
            tuple, _authorization_classes(text, metadata)
        ),
        required_verification_mode=cast(
            str, metadata.get("required_verification_mode", "").strip()
        ),
        approved_tools=approved_tools,
        source_references_required=source_required == "true",
    )
    return procedure, relative_path


__all__ = ["load_canonical_procedure"]
