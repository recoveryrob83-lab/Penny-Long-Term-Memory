"""Strict Package E Worker result artifact contracts and deterministic paths."""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from hashlib import sha256
from importlib.resources import files
from pathlib import PurePosixPath
from typing import Literal

from .worker_runtime import WorkerRuntimeError

RESULT_CONTRACT_ID = "lifeos_worker_result"
RESULT_CONTRACT_VERSION = 1
RESULT_SUBMISSION_PROCEDURE_ID = "engineering_worker_result_submission"
RESULT_SUBMISSION_PROCEDURE_VERSION = 1

ArtifactKind = Literal["worker_report", "rejection", "hq_review", "rob_validation"]

_SCHEMA_FILES: dict[ArtifactKind, str] = {
    "worker_report": "worker-result-report.schema.json",
    "rejection": "worker-result-rejection.schema.json",
    "hq_review": "worker-hq-review.schema.json",
    "rob_validation": "worker-rob-validation.schema.json",
}
_ARTIFACT_PREFIXES: dict[ArtifactKind, str] = {
    "worker_report": "report",
    "rejection": "rejection",
    "hq_review": "hq-review",
    "rob_validation": "rob-validation",
}
_IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_RUN_ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9._-]*$")
_SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class WorkerResultContractError(WorkerRuntimeError):
    """Raised when a result contract or artifact fails deterministic validation."""

    def __init__(self, message: str, errors: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.errors = errors


@dataclass(frozen=True)
class ResultSubmissionContract:
    """Run-specific authority to create one immutable Worker report attempt."""

    contract_id: str
    contract_version: int
    submission_procedure_id: str
    submission_procedure_version: int
    owning_department: str
    worker_id: str
    run_id: str
    attempt: int
    result_path: str
    create_only: bool = True
    overwrite_allowed: bool = False
    work_reexecution_authorized: bool = False
    scope_expansion_authorized: bool = False

    def __post_init__(self) -> None:
        if self.contract_id != RESULT_CONTRACT_ID:
            raise WorkerResultContractError("Result Contract ID is unsupported.")
        if self.contract_version != RESULT_CONTRACT_VERSION:
            raise WorkerResultContractError("Result Contract Version is unsupported.")
        if self.submission_procedure_id != RESULT_SUBMISSION_PROCEDURE_ID:
            raise WorkerResultContractError("Result submission procedure ID is unsupported.")
        if self.submission_procedure_version != RESULT_SUBMISSION_PROCEDURE_VERSION:
            raise WorkerResultContractError("Result submission procedure version is unsupported.")
        _require_identifier(self.owning_department, "owning_department")
        _require_identifier(self.worker_id, "worker_id")
        _require_run_id(self.run_id)
        if isinstance(self.attempt, bool) or self.attempt < 1:
            raise WorkerResultContractError("Result attempt must be a positive integer.")
        if self.create_only is not True:
            raise WorkerResultContractError("Result reporting must be create-only.")
        if self.overwrite_allowed is not False:
            raise WorkerResultContractError("Result artifact overwrite is prohibited.")
        if self.work_reexecution_authorized is not False:
            raise WorkerResultContractError("Report submission cannot authorize work re-execution.")
        if self.scope_expansion_authorized is not False:
            raise WorkerResultContractError("Report submission cannot authorize scope expansion.")
        expected = artifact_path(
            self.owning_department,
            self.worker_id,
            self.run_id,
            "worker_report",
            self.attempt,
        )
        if self.result_path != expected:
            raise WorkerResultContractError(
                f"Result Path must equal the deterministic path {expected}."
            )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _require_identifier(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not _IDENTIFIER_PATTERN.fullmatch(clean):
        raise WorkerResultContractError(
            f"{field_name} must be a lowercase underscore-separated identifier."
        )
    return clean


def _require_run_id(value: str) -> str:
    clean = str(value or "").strip()
    if not _RUN_ID_PATTERN.fullmatch(clean):
        raise WorkerResultContractError("run_id contains unsupported characters.")
    return clean


def artifact_path(
    owning_department: str,
    worker_id: str,
    run_id: str,
    artifact_kind: ArtifactKind,
    attempt: int,
) -> str:
    """Return the one canonical immutable path for an artifact attempt."""

    department = _require_identifier(owning_department, "owning_department")
    worker = _require_identifier(worker_id, "worker_id")
    run = _require_run_id(run_id)
    if artifact_kind not in _ARTIFACT_PREFIXES:
        raise WorkerResultContractError(f"Unsupported artifact kind: {artifact_kind}")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
        raise WorkerResultContractError("Artifact attempt must be a positive integer.")
    filename = f"{_ARTIFACT_PREFIXES[artifact_kind]}-{attempt:03d}.json"
    return str(PurePosixPath("projects") / department / "worker-results" / worker / run / filename)


def build_result_submission_contract(
    owning_department: str,
    worker_id: str,
    run_id: str,
    *,
    attempt: int = 1,
) -> ResultSubmissionContract:
    """Build the exact create-only report contract for one run and attempt."""

    result_path = artifact_path(
        owning_department,
        worker_id,
        run_id,
        "worker_report",
        attempt,
    )
    return ResultSubmissionContract(
        contract_id=RESULT_CONTRACT_ID,
        contract_version=RESULT_CONTRACT_VERSION,
        submission_procedure_id=RESULT_SUBMISSION_PROCEDURE_ID,
        submission_procedure_version=RESULT_SUBMISSION_PROCEDURE_VERSION,
        owning_department=owning_department,
        worker_id=worker_id,
        run_id=run_id,
        attempt=attempt,
        result_path=result_path,
    )


def render_result_submission_instruction(contract: ResultSubmissionContract) -> str:
    """Render the display-only reporting reminder derived from one contract object."""

    return (
        "\n\nResult submission contract:\n"
        f"- Contract: {contract.contract_id} v{contract.contract_version}\n"
        f"- Procedure: {contract.submission_procedure_id} "
        f"v{contract.submission_procedure_version}\n"
        f"- Result path: `{contract.result_path}`\n"
        f"- Attempt: {contract.attempt}\n"
        "- Create the exact file once after completing, holding, or elevating the work.\n"
        "- Do not overwrite or delete an existing artifact.\n"
        "- Do not place the machine report only in chat.\n"
        "- This reporting authority does not authorize work re-execution, scope expansion, "
        "or advisory lifecycle change.\n"
        "- The report remains evidence pending the required Department HQ review."
    )


def load_artifact_schema(artifact_kind: ArtifactKind) -> dict[str, object]:
    """Load one packaged canonical schema."""

    try:
        filename = _SCHEMA_FILES[artifact_kind]
    except KeyError as exc:
        raise WorkerResultContractError(
            f"Unsupported artifact kind: {artifact_kind}"
        ) from exc
    path = files("lifeos_dashboard").joinpath("data", filename)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise WorkerResultContractError(f"Schema {filename} has the wrong shape.")
    return payload


def load_artifact_examples() -> dict[str, dict[str, object]]:
    """Load the canonical correctly typed example artifacts."""

    path = files("lifeos_dashboard").joinpath("data", "worker-result-examples.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not all(isinstance(value, dict) for value in payload.values()):
        raise WorkerResultContractError("Worker result examples have the wrong shape.")
    return payload


def canonical_artifact_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def artifact_checksum(payload: dict[str, object]) -> str:
    digest = sha256(canonical_artifact_json(payload).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _type_name(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _matches_type(value: object, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return False


def _validate_node(
    value: object,
    schema: dict[str, object],
    path: str,
    errors: list[str],
) -> None:
    expected_type = schema.get("type")
    if expected_type is not None:
        allowed = [expected_type] if isinstance(expected_type, str) else expected_type
        if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
            errors.append(f"{path}: schema type declaration is invalid")
            return
        if not any(_matches_type(value, item) for item in allowed):
            errors.append(
                f"{path}: expected {' or '.join(allowed)}, observed {_type_name(value)}"
            )
            return

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        errors.append(f"{path}: value is not in the allowed enum")

    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for field in required:
                if isinstance(field, str) and field not in value:
                    errors.append(f"{path}.{field}: required field is missing")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            if schema.get("additionalProperties") is False:
                extras = sorted(set(value) - set(properties))
                for field in extras:
                    errors.append(f"{path}.{field}: unknown field is prohibited")
            for field, child_schema in properties.items():
                if field in value and isinstance(child_schema, dict):
                    _validate_node(value[field], child_schema, f"{path}.{field}", errors)

    if isinstance(value, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(value) < minimum:
            errors.append(f"{path}: expected at least {minimum} items")
        if schema.get("uniqueItems") is True:
            fingerprints = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(fingerprints) != len(set(fingerprints)):
                errors.append(f"{path}: duplicate items are prohibited")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_node(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value) < minimum:
            errors.append(f"{path}: string is shorter than {minimum}")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: value does not match the required pattern")

    if isinstance(value, int) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, int) and value < minimum:
            errors.append(f"{path}: value must be at least {minimum}")


def validate_artifact(
    artifact_kind: ArtifactKind,
    payload: dict[str, object],
) -> dict[str, object]:
    """Validate one artifact strictly and return it unchanged when valid."""

    if not isinstance(payload, dict):
        raise WorkerResultContractError("Worker result artifact must be a JSON object.")
    errors: list[str] = []
    _validate_node(payload, load_artifact_schema(artifact_kind), "$", errors)
    if errors:
        raise WorkerResultContractError(
            f"{artifact_kind} artifact failed deterministic validation.", tuple(errors)
        )
    return payload


def validate_checksum(value: str) -> str:
    clean = str(value or "").strip()
    if not _SHA256_PATTERN.fullmatch(clean):
        raise WorkerResultContractError("Checksum must use sha256:<64 lowercase hex>.")
    return clean


__all__ = [
    "ArtifactKind",
    "RESULT_CONTRACT_ID",
    "RESULT_CONTRACT_VERSION",
    "RESULT_SUBMISSION_PROCEDURE_ID",
    "RESULT_SUBMISSION_PROCEDURE_VERSION",
    "ResultSubmissionContract",
    "WorkerResultContractError",
    "artifact_checksum",
    "artifact_path",
    "build_result_submission_contract",
    "canonical_artifact_json",
    "load_artifact_examples",
    "load_artifact_schema",
    "render_result_submission_instruction",
    "validate_artifact",
    "validate_checksum",
]
