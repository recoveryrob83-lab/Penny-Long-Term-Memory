"""Enable one guarded later Maintenance HQ review attempt on the existing run row.

Authority remains in ``coordination/boards/engineering.md``. This compatibility
layer reads revision 2 of ADV-20260728-054, verifies every referenced Git object,
and permits only the authorized attempt-2 wake and immutable receipt. It never
reruns the Worker, edits an earlier artifact, closes an advisory, or creates a
second ledger.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .command_center_send_budget import BUDGET_RECOVERY_CONDITION
from .worker_dispatch_runtime import parse_browser_dispatch_receipt
from .worker_github_orchestrator import WorkerGitHubOrchestrator
from .worker_hq_review import (
    WorkerHqReviewIngestionReceipt,
    WorkerHqReviewService,
)
from .worker_result_contract import artifact_checksum, artifact_path, validate_artifact
from .worker_runtime import WorkerRuntimeError

_ADVISORY_ID = "ADV-20260728-054"
_BOARD_PATH = "coordination/boards/engineering.md"
_EXPECTED_REVISION = 2
_EXPECTED_RUN_ID = "RUN-ADV-20260726-053-R1"
_EXPECTED_OWNER = "engineering"
_EXPECTED_PHASE = "PHASE_2_ENGINEERING_RUNTIME_ENABLEMENT"
_EXPECTED_APPROVAL = "ROB-DIRECT-HQ-REVIEW-RESUME-RUNTIME-20260728"
_EXPECTED_WRITE_SCOPES = {
    "apps/lifeos-dashboard/lifeos_dashboard/worker_hq_review_resume_runtime.py",
    "apps/lifeos-dashboard/lifeos_dashboard/__init__.py",
    "apps/lifeos-dashboard/tests/test_worker_hq_review_resume_runtime.py",
}
_INSTALL_FLAG = "_lifeos_hq_review_resume_runtime_installed"
_SERVICE_FLAG = "_lifeos_hq_review_resume_service_installed"
_ORCHESTRATOR_FLAG = "_lifeos_hq_review_resume_orchestrator_installed"
_HEADING_PATTERN = re.compile(
    r"^### (?P<advisory_id>ADV-[A-Z0-9-]+)(?:\s+—\s+.*)?$",
    re.MULTILINE,
)
_FIELD_PATTERN = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$", re.MULTILINE)
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_REPAIR_PENDING = "REPORT_REPAIR_PENDING"
_REPAIR_REQUIRED = "REPAIR_REQUIRED"
_RESUME_WAKE_CLAIMED = "CLAIMED"
_RESUME_WAKE_SUBMITTED = "SUBMITTED"

_RESUME_COLUMNS = {
    "hq_review_resume_attempt": "INTEGER",
    "hq_review_resume_state": "TEXT",
    "hq_review_resume_claimed_at": "REAL",
    "hq_review_resume_wake_target": "TEXT",
    "hq_review_resume_wake_marker": "TEXT",
    "hq_review_resume_wake_user_turn_id": "TEXT",
    "hq_review_resume_wake_receipt_json": "TEXT",
    "hq_review_resume_wake_returned_to_source": "INTEGER",
    "hq_review_resume_wake_sent_at": "REAL",
    "hq_review_resume_review_path": "TEXT",
    "hq_review_resume_review_checksum": "TEXT",
    "hq_review_resume_review_commit_sha": "TEXT",
    "hq_review_resume_review_blob_sha": "TEXT",
    "hq_review_resume_review_state": "TEXT",
    "hq_review_resume_review_reason": "TEXT",
    "hq_review_resume_review_evidence_json": "TEXT",
    "hq_review_resume_review_ingested_at": "REAL",
    "hq_review_prior_evidence_json": "TEXT",
}


@dataclass(frozen=True)
class HqReviewResumeAuthorization:
    """Exact source-board authority for one later immutable HQ review attempt."""

    advisory_id: str
    advisory_revision: int
    owner: str
    phase: str
    approval_reference: str
    run_id: str
    attempt: int
    review_path: str
    procedure_path: str
    procedure_version: int
    procedure_checksum: str
    procedure_commit_sha: str
    procedure_blob_sha: str
    report_path: str
    report_checksum: str
    report_commit_sha: str
    report_blob_sha: str
    prior_review_path: str
    prior_review_state: str
    prior_review_checksum: str
    prior_review_commit_sha: str
    prior_review_blob_sha: str
    write_scopes: tuple[str, ...]


@dataclass(frozen=True)
class WorkerHqReviewResumeWake:
    """Pointer-only Maintenance HQ wake for the authorized later attempt."""

    advisory_id: str
    advisory_revision: int
    run_id: str
    worker_id: str
    owning_department: str
    hq_chat_title: str
    marker: str
    report_path: str
    report_checksum: str
    prior_review_path: str
    prior_review_checksum: str
    procedure_path: str
    procedure_checksum: str
    review_attempt: int
    review_path: str
    instruction: str

    @property
    def idempotency_key(self) -> str:
        return (
            f"hq-review-resume:{self.owning_department}:{self.run_id}:"
            f"{self.review_attempt}"
        )

    def to_dict(self) -> dict[str, object]:
        values = asdict(self)
        values["idempotency_key"] = self.idempotency_key
        return values


def _clean_inline(value: str) -> str:
    clean = str(value or "").strip()
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


def _json_strings(value: str, field_name: str) -> tuple[str, ...]:
    try:
        payload = json.loads(_clean_inline(value))
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError(f"{field_name} must contain valid JSON.") from exc
    if not isinstance(payload, list) or not all(isinstance(item, str) for item in payload):
        raise WorkerRuntimeError(f"{field_name} must be a JSON array of strings.")
    return tuple(payload)


def _advisory_fields(board_text: str, advisory_id: str = _ADVISORY_ID) -> dict[str, str]:
    matches = list(_HEADING_PATTERN.finditer(board_text))
    for index, match in enumerate(matches):
        if match.group("advisory_id") != advisory_id:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(board_text)
        section = board_text[start:end]
        return {
            item.group("key").strip(): _clean_inline(item.group("value"))
            for item in _FIELD_PATTERN.finditer(section)
        }
    raise WorkerRuntimeError(f"Source advisory {advisory_id} was not found.")


def _required(fields: dict[str, str], key: str) -> str:
    value = str(fields.get(key) or "").strip()
    if not value:
        raise WorkerRuntimeError(f"Source advisory is missing {key}.")
    return value


def parse_resume_authorization(board_text: str) -> HqReviewResumeAuthorization:
    """Parse and fail closed on any drift in the exact revision-2 authority."""

    fields = _advisory_fields(board_text)
    lifecycle = _required(fields, "Lifecycle State").upper()
    if lifecycle != "OPEN":
        raise WorkerRuntimeError("HQ review resume advisory is not OPEN.")
    revision = _positive_int(_required(fields, "Advisory Revision"), "Advisory Revision")
    if revision != _EXPECTED_REVISION:
        raise WorkerRuntimeError("HQ review resume advisory revision is not authorized.")
    owner = _required(fields, "Current Target Department and Owner").casefold()
    if owner != _EXPECTED_OWNER:
        raise WorkerRuntimeError("HQ review resume owner is not Engineering.")
    phase = _required(fields, "Current Phase")
    if phase != _EXPECTED_PHASE:
        raise WorkerRuntimeError("HQ review resume phase is not active.")
    approval = _required(fields, "Approval Reference")
    if approval != _EXPECTED_APPROVAL:
        raise WorkerRuntimeError("HQ review resume approval reference does not match.")
    if _required(fields, "Execution-Ready Worker Task").casefold() != "false":
        raise WorkerRuntimeError("HQ review resume must not become a Worker task.")

    run_id = _required(fields, "Related Run")
    attempt = _positive_int(
        _required(fields, "Authorized Later Review Attempt"),
        "Authorized Later Review Attempt",
    )
    review_path = _required(fields, "Authorized Later Review Path")
    procedure_version = _positive_int(
        _required(fields, "Phase 1 Procedure Version"),
        "Phase 1 Procedure Version",
    )
    write_scopes = _json_strings(
        _required(fields, "Requested Write Scopes JSON"),
        "Requested Write Scopes JSON",
    )
    if run_id != _EXPECTED_RUN_ID or attempt != 2:
        raise WorkerRuntimeError("HQ review resume run or attempt is not authorized.")
    if set(write_scopes) != _EXPECTED_WRITE_SCOPES:
        raise WorkerRuntimeError("HQ review resume write scopes have drifted.")

    expected_review_path = artifact_path(
        "maintenance",
        "maintenance_worker",
        run_id,
        "hq_review",
        attempt,
    )
    if review_path != expected_review_path:
        raise WorkerRuntimeError("Authorized later HQ review path is not deterministic.")

    authorization = HqReviewResumeAuthorization(
        advisory_id=_ADVISORY_ID,
        advisory_revision=revision,
        owner=owner,
        phase=phase,
        approval_reference=approval,
        run_id=run_id,
        attempt=attempt,
        review_path=review_path,
        procedure_path=_required(fields, "Phase 1 Procedure Path"),
        procedure_version=procedure_version,
        procedure_checksum=_required(fields, "Phase 1 Procedure Checksum").lower(),
        procedure_commit_sha=_required(fields, "Phase 1 Procedure Commit SHA"),
        procedure_blob_sha=_required(fields, "Phase 1 Procedure Blob SHA"),
        report_path=_required(fields, "Validated Worker Report Path"),
        report_checksum=_required(fields, "Validated Worker Report Checksum").lower(),
        report_commit_sha=_required(fields, "Validated Worker Report Commit SHA"),
        report_blob_sha=_required(fields, "Validated Worker Report Blob SHA"),
        prior_review_path=_required(fields, "Earlier HQ Review Path"),
        prior_review_state=_required(fields, "Earlier HQ Review State"),
        prior_review_checksum=_required(fields, "Earlier HQ Review Checksum").lower(),
        prior_review_commit_sha=_required(fields, "Earlier HQ Review Commit SHA"),
        prior_review_blob_sha=_required(fields, "Earlier HQ Review Blob SHA"),
        write_scopes=write_scopes,
    )
    if authorization.procedure_version != 2:
        raise WorkerRuntimeError("Maintenance HQ review procedure version 2 is required.")
    if authorization.prior_review_state != _REPAIR_REQUIRED:
        raise WorkerRuntimeError("Earlier HQ review is not the authorized procedural hold.")
    for value in (
        authorization.procedure_commit_sha,
        authorization.procedure_blob_sha,
        authorization.report_commit_sha,
        authorization.report_blob_sha,
        authorization.prior_review_commit_sha,
        authorization.prior_review_blob_sha,
    ):
        if not _HEX40.fullmatch(value):
            raise WorkerRuntimeError("HQ review resume authority contains an invalid Git SHA.")
    return authorization


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path, description: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WorkerRuntimeError(f"{description} is not readable valid UTF-8 JSON.") from exc
    if not isinstance(payload, dict):
        raise WorkerRuntimeError(f"{description} must be a JSON object.")
    return payload


def _verify_git_path(
    service: WorkerHqReviewService,
    *,
    path: str,
    commit_sha: str,
    blob_sha: str,
    require_only_path: bool,
) -> Path:
    candidate = service._safe_path(path)  # noqa: SLF001 - same service safety boundary
    if not candidate.is_file():
        raise WorkerRuntimeError(f"Authorized Git evidence is missing: {path}")
    if service._git("status", "--porcelain", "--", path):  # noqa: SLF001
        raise WorkerRuntimeError(f"Authorized Git evidence has uncommitted changes: {path}")
    if service._git("cat-file", "-t", commit_sha) != "commit":  # noqa: SLF001
        raise WorkerRuntimeError(f"Authorized Git commit is unavailable: {commit_sha}")
    if service._git("cat-file", "-t", blob_sha) != "blob":  # noqa: SLF001
        raise WorkerRuntimeError(f"Authorized Git blob is unavailable: {blob_sha}")
    if service._git("rev-parse", f"{commit_sha}:{path}") != blob_sha:  # noqa: SLF001
        raise WorkerRuntimeError(f"Authorized commit and blob do not match: {path}")
    if service._git("rev-parse", f"HEAD:{path}") != blob_sha:  # noqa: SLF001
        raise WorkerRuntimeError(f"Authorized Git evidence changed after publication: {path}")
    if require_only_path:
        changed = {
            item.strip()
            for item in service._git(  # noqa: SLF001
                "diff-tree",
                "--root",
                "--no-commit-id",
                "--name-only",
                "-r",
                commit_sha,
            ).splitlines()
            if item.strip()
        }
        if changed != {path}:
            raise WorkerRuntimeError(
                f"Authorized evidence commit must contain only its exact path: {path}"
            )
    return candidate


def _authorization(service: WorkerHqReviewService) -> HqReviewResumeAuthorization:
    board = service._safe_path(_BOARD_PATH)  # noqa: SLF001
    if not board.is_file():
        raise WorkerRuntimeError("Engineering advisory board is missing.")
    authorization = parse_resume_authorization(board.read_text(encoding="utf-8"))

    procedure_file = _verify_git_path(
        service,
        path=authorization.procedure_path,
        commit_sha=authorization.procedure_commit_sha,
        blob_sha=authorization.procedure_blob_sha,
        require_only_path=True,
    )
    if _sha256_file(procedure_file) != authorization.procedure_checksum:
        raise WorkerRuntimeError("Maintenance procedure v2 checksum does not match authority.")
    procedure_text = procedure_file.read_text(encoding="utf-8")
    if (
        f"Procedure Version: {authorization.procedure_version}" not in procedure_text
        or "hq-review-002.json" not in procedure_text
    ):
        raise WorkerRuntimeError("Maintenance procedure v2 content is incompatible.")

    report_file = _verify_git_path(
        service,
        path=authorization.report_path,
        commit_sha=authorization.report_commit_sha,
        blob_sha=authorization.report_blob_sha,
        require_only_path=True,
    )
    report = _load_json(report_file, "Validated Worker report")
    validate_artifact("worker_report", report)
    if artifact_checksum(report) != authorization.report_checksum:
        raise WorkerRuntimeError("Validated Worker report checksum does not match authority.")

    prior_file = _verify_git_path(
        service,
        path=authorization.prior_review_path,
        commit_sha=authorization.prior_review_commit_sha,
        blob_sha=authorization.prior_review_blob_sha,
        require_only_path=True,
    )
    prior = _load_json(prior_file, "Earlier HQ review")
    validate_artifact("hq_review", prior)
    if artifact_checksum(prior) != authorization.prior_review_checksum:
        raise WorkerRuntimeError("Earlier HQ review checksum does not match authority.")
    if (
        prior.get("attempt") != 1
        or prior.get("run_id") != authorization.run_id
        or prior.get("review_state") != authorization.prior_review_state
        or prior.get("report_path") != authorization.report_path
    ):
        raise WorkerRuntimeError("Earlier HQ review does not match the authorized hold.")
    return authorization


def _row_matches_authority(row, authorization: HqReviewResumeAuthorization) -> None:
    expected = {
        "run_id": authorization.run_id,
        "worker_id": "maintenance_worker",
        "owning_department": "maintenance",
        "result_state": _REPAIR_PENDING,
        "report_path": authorization.report_path,
        "report_checksum": authorization.report_checksum,
        "report_commit_sha": authorization.report_commit_sha,
        "report_blob_sha": authorization.report_blob_sha,
        "hq_review_path": authorization.prior_review_path,
        "hq_review_checksum": authorization.prior_review_checksum,
        "hq_review_commit_sha": authorization.prior_review_commit_sha,
        "hq_review_blob_sha": authorization.prior_review_blob_sha,
        "hq_review_state": authorization.prior_review_state,
    }
    mismatches = [
        key
        for key, expected_value in expected.items()
        if str(row[key] or "") != str(expected_value)
    ]
    if mismatches:
        raise WorkerRuntimeError(
            "Runtime row does not match authorized review-resume evidence: "
            + ", ".join(mismatches)
        )


def _ensure_resume_columns(service: WorkerHqReviewService) -> None:
    with service._connect() as connection:  # noqa: SLF001 - additive same-row extension
        existing = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(execution_history)").fetchall()
        }
        for name, column_type in _RESUME_COLUMNS.items():
            if name not in existing:
                connection.execute(
                    f"ALTER TABLE execution_history ADD COLUMN {name} {column_type}"
                )


def _claim_resume_wake(
    service: WorkerHqReviewService,
    row,
    authorization: HqReviewResumeAuthorization,
) -> float | None:
    claimed_at = time.time()
    with service._connect() as connection:  # noqa: SLF001 - atomic same-row claim
        updated = connection.execute(
            """
            UPDATE execution_history SET
                hq_review_resume_attempt = ?,
                hq_review_resume_state = ?,
                hq_review_resume_claimed_at = ?
            WHERE id = ?
              AND result_state = ?
              AND hq_review_state = ?
              AND hq_review_path = ?
              AND hq_review_checksum = ?
              AND hq_review_commit_sha = ?
              AND hq_review_blob_sha = ?
              AND hq_review_resume_claimed_at IS NULL
              AND COALESCE(hq_review_resume_state, '') = ''
              AND COALESCE(hq_review_resume_review_path, '') = ''
            """,
            (
                authorization.attempt,
                _RESUME_WAKE_CLAIMED,
                claimed_at,
                int(row["id"]),
                _REPAIR_PENDING,
                _REPAIR_REQUIRED,
                authorization.prior_review_path,
                authorization.prior_review_checksum,
                authorization.prior_review_commit_sha,
                authorization.prior_review_blob_sha,
            ),
        )
    return claimed_at if updated.rowcount == 1 else None


def _release_pretransport_claim(
    service: WorkerHqReviewService,
    row_id: int,
    claimed_at: float,
) -> None:
    with service._connect() as connection:  # noqa: SLF001 - safe pre-send claim release
        connection.execute(
            """
            UPDATE execution_history SET
                hq_review_resume_attempt = NULL,
                hq_review_resume_state = NULL,
                hq_review_resume_claimed_at = NULL
            WHERE id = ?
              AND hq_review_resume_state = ?
              AND hq_review_resume_claimed_at = ?
              AND COALESCE(hq_review_resume_wake_user_turn_id, '') = ''
              AND COALESCE(hq_review_resume_wake_receipt_json, '') = ''
            """,
            (row_id, _RESUME_WAKE_CLAIMED, claimed_at),
        )


def _resume_wake_from_row(
    service: WorkerHqReviewService,
    row,
    authorization: HqReviewResumeAuthorization,
) -> WorkerHqReviewResumeWake:
    hq_title = service._hq_chat_title(str(row["owning_department"]))  # noqa: SLF001
    marker = f"HQ-REVIEW-RESUME-{authorization.run_id}-A{authorization.attempt}"
    instruction = (
        f"{marker}\n\n"
        f"Authorized later Maintenance HQ review for existing run "
        f"`{authorization.run_id}`. Follow `{authorization.procedure_path}` version "
        f"{authorization.procedure_version}. Inspect validated report "
        f"`{authorization.report_path}` and preserve earlier review "
        f"`{authorization.prior_review_path}`. Create exactly one immutable "
        f"attempt-{authorization.attempt} receipt at `{authorization.review_path}`. "
        "Do not rerun, replace immutable evidence, broaden scope, change runtime "
        "state, close advisories, wake Chief of Staff, or perform Rob validation."
    )
    return WorkerHqReviewResumeWake(
        advisory_id=authorization.advisory_id,
        advisory_revision=authorization.advisory_revision,
        run_id=authorization.run_id,
        worker_id=str(row["worker_id"]),
        owning_department=str(row["owning_department"]),
        hq_chat_title=hq_title,
        marker=marker,
        report_path=authorization.report_path,
        report_checksum=authorization.report_checksum,
        prior_review_path=authorization.prior_review_path,
        prior_review_checksum=authorization.prior_review_checksum,
        procedure_path=authorization.procedure_path,
        procedure_checksum=authorization.procedure_checksum,
        review_attempt=authorization.attempt,
        review_path=authorization.review_path,
        instruction=instruction,
    )


def _build_resume_wake(
    service: WorkerHqReviewService,
    run_id: str,
) -> WorkerHqReviewResumeWake:
    authorization = _authorization(service)
    if run_id != authorization.run_id:
        raise WorkerRuntimeError("Run is not authorized for HQ review resume.")
    _ensure_resume_columns(service)
    row = service._row(run_id)  # noqa: SLF001 - same service row
    _row_matches_authority(row, authorization)
    if service._safe_path(authorization.review_path).exists():  # noqa: SLF001
        raise WorkerRuntimeError(
            "Authorized attempt-2 review already exists; ingest it instead of waking HQ."
        )
    if str(row["hq_review_resume_state"] or ""):
        raise WorkerRuntimeError("HQ review resume is already claimed or submitted.")
    return _resume_wake_from_row(service, row, authorization)


def _record_resume_wake(
    service: WorkerHqReviewService,
    run_id: str,
    browser_receipt: dict[str, object],
) -> WorkerHqReviewResumeWake:
    authorization = _authorization(service)
    _ensure_resume_columns(service)
    row = service._row(run_id)  # noqa: SLF001
    _row_matches_authority(row, authorization)
    wake = _resume_wake_from_row(service, row, authorization)
    if browser_receipt.get("status") != "submitted":
        raise WorkerRuntimeError("HQ review resume courier did not report submission.")
    if browser_receipt.get("submission_confirmed") is not True:
        raise WorkerRuntimeError("HQ review resume courier did not confirm submission.")
    if str(browser_receipt.get("request_marker") or "") != wake.marker:
        raise WorkerRuntimeError("HQ review resume courier marker does not match.")
    if str(browser_receipt.get("run_id") or "") != wake.run_id:
        raise WorkerRuntimeError("HQ review resume courier run ID does not match.")
    user_turn_id = str(browser_receipt.get("user_turn_id") or "").strip()
    if not user_turn_id:
        raise WorkerRuntimeError("HQ review resume courier has no correlated user turn.")
    if browser_receipt.get("returned_to_source") is not True:
        raise WorkerRuntimeError("HQ review resume courier did not verify return to source.")

    with service._connect() as connection:  # noqa: SLF001 - exact claim persistence
        updated = connection.execute(
            """
            UPDATE execution_history SET
                hq_review_resume_state = ?,
                hq_review_resume_wake_target = ?,
                hq_review_resume_wake_marker = ?,
                hq_review_resume_wake_user_turn_id = ?,
                hq_review_resume_wake_receipt_json = ?,
                hq_review_resume_wake_returned_to_source = 1,
                hq_review_resume_wake_sent_at = ?
            WHERE id = ?
              AND hq_review_resume_attempt = ?
              AND hq_review_resume_state = ?
              AND hq_review_resume_claimed_at IS NOT NULL
              AND COALESCE(hq_review_resume_wake_user_turn_id, '') = ''
            """,
            (
                _RESUME_WAKE_SUBMITTED,
                wake.hq_chat_title,
                wake.marker,
                user_turn_id,
                json.dumps(browser_receipt, sort_keys=True, ensure_ascii=False),
                time.time(),
                int(row["id"]),
                authorization.attempt,
                _RESUME_WAKE_CLAIMED,
            ),
        )
        if updated.rowcount != 1:
            current = connection.execute(
                "SELECT * FROM execution_history WHERE id = ?",
                (int(row["id"]),),
            ).fetchone()
            if (
                current is not None
                and str(current["hq_review_resume_state"] or "")
                == _RESUME_WAKE_SUBMITTED
                and str(current["hq_review_resume_wake_user_turn_id"] or "")
                == user_turn_id
                and str(current["hq_review_resume_wake_marker"] or "") == wake.marker
            ):
                return wake
            raise WorkerRuntimeError(
                "HQ review resume claim changed before wake evidence was persisted."
            )
    return wake


def _required_evidence(
    payload: dict[str, object],
    authorization: HqReviewResumeAuthorization,
) -> None:
    evidence = [str(item) for item in payload.get("evidence_checked") or ()]
    required_tokens = (
        authorization.advisory_id,
        authorization.procedure_path,
        authorization.report_path,
        authorization.prior_review_path,
    )
    missing = [token for token in required_tokens if not any(token in item for item in evidence)]
    if missing:
        raise WorkerRuntimeError(
            "Attempt-2 HQ review lacks required correlation evidence: "
            + ", ".join(missing)
        )


def _prior_snapshot(row) -> dict[str, object]:
    keys = (
        "hq_wake_state",
        "hq_wake_target",
        "hq_wake_marker",
        "hq_wake_user_turn_id",
        "hq_wake_returned_to_source",
        "hq_wake_sent_at",
        "hq_review_path",
        "hq_review_checksum",
        "hq_review_commit_sha",
        "hq_review_blob_sha",
        "hq_review_state",
        "hq_review_reason",
        "hq_review_evidence_json",
        "hq_review_ingested_at",
        "ready_for_consumption",
        "requires_rob_validation",
    )
    return {key: row[key] for key in keys if key in row.keys()}


def _ingest_resume_review(
    service: WorkerHqReviewService,
    run_id: str,
) -> WorkerHqReviewIngestionReceipt:
    authorization = _authorization(service)
    if run_id != authorization.run_id:
        raise WorkerRuntimeError("Run is not authorized for attempt-2 HQ review.")
    _ensure_resume_columns(service)
    row = service._row(run_id)  # noqa: SLF001

    review_file = service._safe_path(authorization.review_path)  # noqa: SLF001
    if not review_file.is_file():
        raise WorkerRuntimeError(
            f"Immutable attempt-2 HQ review is missing: {authorization.review_path}"
        )
    payload = _load_json(review_file, "Attempt-2 HQ review")
    validate_artifact("hq_review", payload)
    service._validate_review_semantics(payload)  # noqa: SLF001
    expected = {
        "attempt": authorization.attempt,
        "run_id": authorization.run_id,
        "worker_id": str(row["worker_id"]),
        "reviewing_hq": service._hq_chat_title(  # noqa: SLF001
            str(row["owning_department"])
        ),
        "report_path": authorization.report_path,
    }
    mismatches = [key for key, value in expected.items() if payload.get(key) != value]
    if mismatches:
        raise WorkerRuntimeError(
            "Attempt-2 HQ review does not match authorized identity: "
            + ", ".join(mismatches)
        )
    _required_evidence(payload, authorization)
    commit_sha, blob_sha, checksum = service._git_review_evidence(  # noqa: SLF001
        authorization.review_path,
        payload,
    )

    existing_path = str(row["hq_review_resume_review_path"] or "")
    if existing_path:
        if (
            existing_path == authorization.review_path
            and str(row["hq_review_resume_review_checksum"] or "") == checksum
            and str(row["hq_review_resume_review_commit_sha"] or "") == commit_sha
            and str(row["hq_review_resume_review_blob_sha"] or "") == blob_sha
            and str(row["hq_review_resume_review_state"] or "")
            == str(payload["review_state"])
            and str(row["hq_review_path"] or "") == authorization.review_path
            and str(row["hq_review_checksum"] or "") == checksum
        ):
            return WorkerHqReviewIngestionReceipt(
                status="succeeded",
                run_id=authorization.run_id,
                worker_id=str(row["worker_id"]),
                review_state=str(payload["review_state"]),
                review_path=authorization.review_path,
                review_checksum=checksum,
                review_commit_sha=commit_sha,
                review_blob_sha=blob_sha,
                result_state=str(row["result_state"]),
                ready_for_consumption=bool(row["ready_for_consumption"]),
                requires_rob_validation=bool(row["requires_rob_validation"]),
                duplicate_suppressed=True,
            )
        raise WorkerRuntimeError("A conflicting attempt-2 HQ review is already ingested.")

    _row_matches_authority(row, authorization)
    if (
        str(row["hq_review_resume_state"] or "") != _RESUME_WAKE_SUBMITTED
        or not bool(row["hq_review_resume_wake_returned_to_source"])
    ):
        raise WorkerRuntimeError(
            "Attempt-2 HQ review cannot be ingested before a proven resume wake."
        )

    review_state = str(payload["review_state"])
    runtime_state = service._runtime_state(review_state)  # noqa: SLF001
    prior_json = json.dumps(_prior_snapshot(row), sort_keys=True, ensure_ascii=False)
    now = time.time()
    with service._connect() as connection:  # noqa: SLF001 - exact CAS same-row update
        updated = connection.execute(
            """
            UPDATE execution_history SET
                result_state = ?,
                hq_review_path = ?,
                hq_review_checksum = ?,
                hq_review_commit_sha = ?,
                hq_review_blob_sha = ?,
                hq_review_state = ?,
                hq_review_reason = ?,
                hq_review_evidence_json = ?,
                hq_review_ingested_at = ?,
                ready_for_consumption = ?,
                requires_rob_validation = ?,
                hq_review_resume_review_path = ?,
                hq_review_resume_review_checksum = ?,
                hq_review_resume_review_commit_sha = ?,
                hq_review_resume_review_blob_sha = ?,
                hq_review_resume_review_state = ?,
                hq_review_resume_review_reason = ?,
                hq_review_resume_review_evidence_json = ?,
                hq_review_resume_review_ingested_at = ?,
                hq_review_prior_evidence_json = ?
            WHERE id = ?
              AND result_state = ?
              AND hq_review_state = ?
              AND hq_review_path = ?
              AND hq_review_checksum = ?
              AND hq_review_commit_sha = ?
              AND hq_review_blob_sha = ?
              AND hq_review_resume_attempt = ?
              AND hq_review_resume_state = ?
              AND hq_review_resume_wake_returned_to_source = 1
              AND COALESCE(hq_review_resume_review_path, '') = ''
            """,
            (
                runtime_state,
                authorization.review_path,
                checksum,
                commit_sha,
                blob_sha,
                review_state,
                str(payload["reason"]),
                json.dumps(payload["evidence_checked"], sort_keys=True, ensure_ascii=False),
                now,
                int(bool(payload["ready_for_consumption"])),
                int(bool(payload["requires_rob_validation"])),
                authorization.review_path,
                checksum,
                commit_sha,
                blob_sha,
                review_state,
                str(payload["reason"]),
                json.dumps(payload["evidence_checked"], sort_keys=True, ensure_ascii=False),
                now,
                prior_json,
                int(row["id"]),
                _REPAIR_PENDING,
                _REPAIR_REQUIRED,
                authorization.prior_review_path,
                authorization.prior_review_checksum,
                authorization.prior_review_commit_sha,
                authorization.prior_review_blob_sha,
                authorization.attempt,
                _RESUME_WAKE_SUBMITTED,
            ),
        )
        if updated.rowcount != 1:
            raise WorkerRuntimeError(
                "Attempt-2 HQ review found changed or conflicting runtime evidence. "
                "Nothing was overwritten."
            )

    return WorkerHqReviewIngestionReceipt(
        status="succeeded",
        run_id=authorization.run_id,
        worker_id=str(row["worker_id"]),
        review_state=review_state,
        review_path=authorization.review_path,
        review_checksum=checksum,
        review_commit_sha=commit_sha,
        review_blob_sha=blob_sha,
        result_state=runtime_state,
        ready_for_consumption=bool(payload["ready_for_consumption"]),
        requires_rob_validation=bool(payload["requires_rob_validation"]),
    )


def _install_service() -> None:
    service_class = WorkerHqReviewService
    if getattr(service_class, _SERVICE_FLAG, False):
        return
    original_initialize = service_class._initialize

    def initialize(self: WorkerHqReviewService) -> None:
        original_initialize(self)
        _ensure_resume_columns(self)

    def build_resume_wake(
        self: WorkerHqReviewService,
        run_id: str,
    ) -> WorkerHqReviewResumeWake:
        return _build_resume_wake(self, run_id)

    def record_resume_wake(
        self: WorkerHqReviewService,
        run_id: str,
        browser_receipt: dict[str, object],
    ) -> WorkerHqReviewResumeWake:
        return _record_resume_wake(self, run_id, browser_receipt)

    def ingest_resume_review(
        self: WorkerHqReviewService,
        run_id: str,
    ) -> WorkerHqReviewIngestionReceipt:
        return _ingest_resume_review(self, run_id)

    service_class._initialize = initialize
    service_class.build_resume_wake = build_resume_wake
    service_class.record_resume_wake = record_resume_wake
    service_class.ingest_resume_review = ingest_resume_review
    setattr(service_class, _SERVICE_FLAG, True)


def _send_resume_wake(
    orchestrator: WorkerGitHubOrchestrator,
    run_id: str,
    advisory_id: str,
) -> None:
    service = orchestrator.operations.hq_review
    authorization = _authorization(service)
    if run_id != authorization.run_id:
        return
    _ensure_resume_columns(service)
    row = orchestrator._row(run_id)  # noqa: SLF001
    if row is None:
        return
    _row_matches_authority(row, authorization)

    if orchestrator._artifact_exists(authorization.review_path):  # noqa: SLF001
        _ingest_resume_if_present(orchestrator, run_id, advisory_id)
        return
    resume_state = str(row["hq_review_resume_state"] or "")
    if resume_state in {_RESUME_WAKE_CLAIMED, _RESUME_WAKE_SUBMITTED}:
        return
    command_center = orchestrator.operations.command_center
    if command_center.paused:
        return
    run_lock = command_center._run_lock  # noqa: SLF001 - shared browser gate
    if not run_lock.acquire(blocking=False):
        return

    claimed_at: float | None = None
    try:
        wake = _build_resume_wake(service, run_id)
        row = orchestrator._row(run_id)  # noqa: SLF001
        if row is None:
            raise WorkerRuntimeError("HQ review resume execution row disappeared.")
        claimed_at = _claim_resume_wake(service, row, authorization)
        if claimed_at is None:
            orchestrator._event(  # noqa: SLF001
                "hq_review_resume_wake",
                "suppressed",
                "A prior attempt-2 wake claim or review exists.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            return

        decision = command_center.reserve_send_budget(
            kind="hq_review_wake",
            run_id=run_id,
        )
        if not decision.reserved:
            _release_pretransport_claim(service, int(row["id"]), claimed_at)
            command_center.trip_safety_pause(
                reason=decision.reason,
                affected_run_id=run_id,
                trigger="send_budget",
                recovery_condition=BUDGET_RECOVERY_CONDITION,
            )
            raise WorkerRuntimeError(
                f"{decision.reason} Reset the budget explicitly while paused "
                "before another send."
            )
        try:
            command_center.append_send_budget_evidence(
                run_id=run_id,
                decision=decision,
            )
        except Exception as exc:
            command_center.trip_safety_pause(
                reason=(
                    "Attempt-2 HQ review wake reserved a send attempt, but its "
                    "evidence could not be attached before transport. Nothing was sent."
                ),
                affected_run_id=run_id,
                trigger="send_budget_evidence",
                recovery_condition=BUDGET_RECOVERY_CONDITION,
            )
            raise WorkerRuntimeError(
                "Attempt-2 send-budget evidence could not be persisted."
            ) from exc

        command = [
            sys.executable,
            str(
                orchestrator.app_root
                / "automation"
                / "chatgpt_worker_browser_dispatch.py"
            ),
            "--worker-chat-title",
            wake.hq_chat_title,
            "--project-title",
            str(__import__("os").getenv("LIFEOS_CHATGPT_PROJECT_TITLE", "LifeOS")),
            "--text",
            wake.instruction,
            "--request-marker",
            wake.marker,
            "--response-marker",
            wake.run_id,
            "--cdp-endpoint",
            orchestrator.operations.cdp_endpoint,
            "--timeout-seconds",
            str(orchestrator.timeout_seconds),
            "--send",
            "--confirm-send",
            "SEND",
        ]
        completed = subprocess.run(
            command,
            cwd=orchestrator.app_root,
            env=__import__("os").environ.copy(),
            capture_output=True,
            text=True,
            timeout=orchestrator.timeout_seconds + 30,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise WorkerRuntimeError(
                detail or "Attempt-2 Maintenance HQ wake failed or became uncertain."
            )
        receipt = parse_browser_dispatch_receipt(completed.stdout)
        _record_resume_wake(service, run_id, receipt)
    except Exception:
        current = orchestrator._row(run_id)  # noqa: SLF001
        submitted = bool(
            current is not None
            and str(current["hq_review_resume_state"] or "") == _RESUME_WAKE_SUBMITTED
        )
        if claimed_at is not None and not submitted:
            command_center.trip_safety_pause(
                reason=(
                    "Attempt-2 Maintenance HQ wake failed or became uncertain after "
                    "a claim or send reservation. Inspect the HQ conversation before "
                    "any retry."
                ),
                affected_run_id=run_id,
                trigger="hq_review_resume",
            )
        orchestrator._event(  # noqa: SLF001
            "hq_review_resume_wake",
            "held",
            "Attempt-2 wake is held for inspection; automatic retry is suppressed.",
            run_id=run_id,
            advisory_id=advisory_id,
        )
        raise
    finally:
        run_lock.release()

    orchestrator._event(  # noqa: SLF001
        "hq_review_resume_wake",
        "succeeded",
        "Maintenance HQ received the authorized attempt-2 review pointer.",
        run_id=run_id,
        advisory_id=advisory_id,
    )


def _ingest_resume_if_present(
    orchestrator: WorkerGitHubOrchestrator,
    run_id: str,
    advisory_id: str,
) -> None:
    service = orchestrator.operations.hq_review
    authorization = _authorization(service)
    if run_id != authorization.run_id:
        return
    if not orchestrator._artifact_exists(authorization.review_path):  # noqa: SLF001
        return
    row = orchestrator._row(run_id)  # noqa: SLF001
    if row is None:
        return
    receipt = _ingest_resume_review(service, run_id)
    status = "suppressed" if receipt.duplicate_suppressed else "succeeded"
    orchestrator._event(  # noqa: SLF001
        "hq_review_resume_ingestion",
        status,
        "Identical attempt-2 HQ review was already ingested."
        if receipt.duplicate_suppressed
        else f"Attempt-2 HQ review reached {receipt.result_state}.",
        run_id=run_id,
        advisory_id=advisory_id,
    )


def _install_orchestrator() -> None:
    orchestrator_class = WorkerGitHubOrchestrator
    if getattr(orchestrator_class, _ORCHESTRATOR_FLAG, False):
        return
    original_send = orchestrator_class._send_hq_wake
    original_ingest = orchestrator_class._ingest_hq_review_if_present

    def send_hq_wake(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if (
            run_id == _EXPECTED_RUN_ID
            and row is not None
            and str(row["result_state"] or "") == _REPAIR_PENDING
            and str(row["hq_review_state"] or "") == _REPAIR_REQUIRED
        ):
            _send_resume_wake(self, run_id, advisory_id)
            return
        original_send(self, run_id, advisory_id)

    def ingest_hq_review_if_present(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if (
            run_id == _EXPECTED_RUN_ID
            and row is not None
            and (
                str(row["result_state"] or "") == _REPAIR_PENDING
                or str(row["hq_review_resume_review_path"] or "")
            )
        ):
            _ingest_resume_if_present(self, run_id, advisory_id)
            return
        original_ingest(self, run_id, advisory_id)

    orchestrator_class._send_hq_wake = send_hq_wake
    orchestrator_class._ingest_hq_review_if_present = ingest_hq_review_if_present
    setattr(orchestrator_class, _ORCHESTRATOR_FLAG, True)


def install_worker_hq_review_resume_runtime() -> bool:
    """Install the authorized same-row attempt-2 HQ review path once."""

    if getattr(WorkerHqReviewService, _INSTALL_FLAG, False):
        return False
    _install_service()
    _install_orchestrator()
    setattr(WorkerHqReviewService, _INSTALL_FLAG, True)
    return True


install_worker_hq_review_resume_runtime()


__all__ = [
    "HqReviewResumeAuthorization",
    "WorkerHqReviewResumeWake",
    "_claim_resume_wake",
    "_ensure_resume_columns",
    "_ingest_resume_review",
    "_release_pretransport_claim",
    "install_worker_hq_review_resume_runtime",
    "parse_resume_authorization",
]
