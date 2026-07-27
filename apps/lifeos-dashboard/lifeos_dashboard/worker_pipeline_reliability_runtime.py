"""Repair Worker result validation, continuation routing, and rejected-report recovery."""
from __future__ import annotations

import os
import re
import subprocess
import sys

from . import worker_operations
from .worker_github_orchestrator import WorkerGitHubOrchestrator
from .worker_github_orchestrator_runtime import (
    _claim_hq_wake,
    _ensure_hq_wake_claim_column,
)
from .worker_result_contract import artifact_path
from .worker_result_ingester import WorkerResultIngester
from .worker_result_repair import REPAIR_ACCEPTED, WorkerResultRepairCoordinator
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_pipeline_reliability_runtime_installed"
_SERVICE_FLAG = "_lifeos_worker_result_revalidation_service_installed"
_VALIDATOR_FLAG = "_lifeos_worker_result_scope_validator_installed"
_ORCHESTRATOR_FLAG = "_lifeos_worker_continuation_repair_installed"

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_COMMIT_BLOB_REFERENCE = re.compile(
    r"^(?P<path>.+)@commit:(?P<commit>[0-9a-f]{40})@blob:(?P<blob>[0-9a-f]{40})$"
)
_BLOB_REFERENCE = re.compile(r"^(?P<path>.+)@blob:(?P<blob>[0-9a-f]{40})$")
_BARE_BLOB_REFERENCE = re.compile(r"^(?P<path>.+)@(?P<blob>[0-9a-f]{40})$")
_PREFLIGHT_REFERENCE = re.compile(r"^(?P<path>.+)@preflight:not-found$")
_INTERNAL_VALIDATION_ACTIVITIES = {
    "local non-mutating json schema and checksum validation",
}


def _truthy_environment(name: str, *, default: bool = False) -> bool:
    raw = str(os.getenv(name) or "").strip().casefold()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


def _normalized_scope(value: object) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if text.endswith(")") and " (" in text:
        text = text.rsplit(" (", 1)[0].strip()
    while text.startswith("./"):
        text = text[2:]
    return text.rstrip("/")


def _scope_allows(allowed: object, actual: object) -> bool:
    allowed_path = _normalized_scope(allowed)
    actual_path = _normalized_scope(actual)
    if not allowed_path or not actual_path:
        return False
    return actual_path == allowed_path or actual_path.startswith(f"{allowed_path}/")


def _is_allowed_scope(allowed_scopes: tuple[str, ...], actual: object) -> bool:
    return any(_scope_allows(allowed, actual) for allowed in allowed_scopes)


def _parse_evidence_reference(
    value: object,
) -> tuple[str, str | None, str | None, bool]:
    text = str(value or "").strip()
    match = _COMMIT_BLOB_REFERENCE.fullmatch(text)
    if match:
        return match.group("path"), match.group("commit"), match.group("blob"), False
    match = _BLOB_REFERENCE.fullmatch(text)
    if match:
        return match.group("path"), None, match.group("blob"), False
    match = _BARE_BLOB_REFERENCE.fullmatch(text)
    if match:
        return match.group("path"), None, match.group("blob"), False
    match = _PREFLIGHT_REFERENCE.fullmatch(text)
    if match:
        return match.group("path"), None, None, True
    raise WorkerRuntimeError(f"evidence reference witness is invalid: {text}")


def _validate_report_correlation(
    self: WorkerResultIngester,
    advisory,
    profile,
    payload: dict[str, object],
) -> None:
    contract = advisory.result_contract
    if contract is None:
        raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
    errors: list[str] = []
    for field_name, expected in self._expected_identity(advisory).items():
        if payload.get(field_name) != expected:
            errors.append(f"report {field_name} does not match the canonical assignment")
    expected_profile = {
        "profile_version": profile.profile_version,
        "owning_department": profile.owning_department,
        "attempt": contract.attempt,
    }
    for field_name, expected in expected_profile.items():
        if payload.get(field_name) != expected:
            errors.append(f"report {field_name} does not match canonical Worker state")
    if profile.worker_id != advisory.target_worker_id:
        errors.append("registered Worker does not match the canonical assignment")

    actual_reads = tuple(str(item) for item in payload.get("actual_read_scopes") or ())
    actual_writes = tuple(str(item) for item in payload.get("actual_write_scopes") or ())
    actual_tools = tuple(str(item) for item in payload.get("actual_tools") or ())
    allowed_reads = tuple(
        dict.fromkeys((*advisory.requested_read_scopes, *advisory.requested_write_scopes))
    )
    unauthorized_reads = sorted(
        item for item in actual_reads if not _is_allowed_scope(allowed_reads, item)
    )
    unauthorized_writes = sorted(
        item
        for item in actual_writes
        if not _is_allowed_scope(advisory.requested_write_scopes, item)
    )
    requested_tools = set(advisory.requested_tools)
    unauthorized_tools = sorted(
        item
        for item in actual_tools
        if item not in requested_tools
        and item.casefold() not in _INTERNAL_VALIDATION_ACTIVITIES
    )
    if unauthorized_reads:
        errors.append(
            "actual read scopes exceed assignment: " + ", ".join(unauthorized_reads)
        )
    if unauthorized_writes:
        errors.append(
            "actual write scopes exceed assignment: " + ", ".join(unauthorized_writes)
        )
    if unauthorized_tools:
        errors.append("actual tools exceed assignment: " + ", ".join(unauthorized_tools))
    if contract.result_path not in actual_writes:
        errors.append("actual write scopes do not include the exact report path")

    if payload.get("controlled_outcome") == "IMPLEMENT":
        missing_reads = sorted(
            requested
            for requested in advisory.requested_read_scopes
            if not any(_scope_allows(requested, actual) for actual in actual_reads)
        )
        if missing_reads:
            errors.append(
                "implemented report omits requested read scopes: "
                + ", ".join(missing_reads)
            )
        if payload.get("completion_state") != "completed":
            errors.append("IMPLEMENT requires completion_state completed")
        if payload.get("verification_state") != "pending":
            errors.append("IMPLEMENT requires pending Department HQ verification")
        if payload.get("failure_reason") is not None:
            errors.append("IMPLEMENT report cannot contain a failure reason")
    if payload.get("controlled_outcome") == "REPORT_AND_HOLD" and not payload.get(
        "failure_reason"
    ):
        errors.append("REPORT_AND_HOLD requires a failure reason")

    evidence_paths: set[str] = set()
    allowed_evidence_scopes = tuple(
        dict.fromkeys(
            (
                *advisory.source_references,
                *advisory.requested_read_scopes,
                *advisory.requested_write_scopes,
            )
        )
    )
    for reference in payload.get("evidence_references") or ():
        text = str(reference)
        try:
            path, commit_sha, blob_sha, preflight = _parse_evidence_reference(text)
        except WorkerRuntimeError as exc:
            errors.append(str(exc))
            continue
        evidence_paths.add(_normalized_scope(path))
        if not _is_allowed_scope(allowed_evidence_scopes, path):
            errors.append(f"evidence reference path is outside assignment: {path}")
            continue
        if preflight:
            if _normalized_scope(path) != _normalized_scope(contract.result_path):
                errors.append("preflight:not-found is allowed only for the report path")
            continue
        if blob_sha is None or not _HEX40.fullmatch(blob_sha):
            errors.append(f"evidence reference witness is invalid: {text}")
            continue
        try:
            if self._git("cat-file", "-t", blob_sha) != "blob":
                errors.append(f"evidence witness is not a Git blob: {text}")
                continue
            if commit_sha is not None:
                if self._git("cat-file", "-t", commit_sha) != "commit":
                    errors.append(f"evidence commit witness is not a Git commit: {text}")
                    continue
                if self._git("rev-parse", f"{commit_sha}:{path}") != blob_sha:
                    errors.append(
                        f"evidence commit and blob do not resolve together: {text}"
                    )
        except WorkerRuntimeError:
            errors.append(f"evidence Git witness is unavailable: {text}")

    if payload.get("controlled_outcome") == "IMPLEMENT":
        missing_evidence = sorted(
            source
            for source in advisory.source_references
            if not any(_scope_allows(source, path) for path in evidence_paths)
        )
        if missing_evidence:
            errors.append(
                "implemented report omits source evidence: "
                + ", ".join(missing_evidence)
            )
    if errors:
        raise WorkerRuntimeError(
            "Worker report correlation failed: " + "; ".join(errors) + "."
        )


def _revalidate_rejected(self: WorkerResultRepairCoordinator, advisory):
    row = self._row(advisory.run_id)
    if str(row["result_state"] or "") != "REPORT_REJECTED":
        raise WorkerRuntimeError(
            "Same-artifact revalidation requires a REPORT_REJECTED result."
        )
    contract = advisory.result_contract
    if contract is None:
        raise WorkerRuntimeError("Canonical assignment has no Worker result contract.")
    rejected_attempt = int(row["report_attempt"] or 0)
    if rejected_attempt != contract.attempt:
        raise WorkerRuntimeError(
            "Rejected report attempt does not match the canonical assignment."
        )
    next_path = artifact_path(
        contract.owning_department,
        advisory.target_worker_id,
        advisory.run_id,
        "worker_report",
        rejected_attempt + 1,
    )
    if self.ingester._safe_path(next_path).exists():  # noqa: SLF001
        raise WorkerRuntimeError(
            "A later immutable report attempt already exists; same-artifact revalidation is unsafe."
        )
    receipt = self.ingester.ingest(advisory)
    with self._connect() as connection:
        connection.execute(
            """
            UPDATE execution_history
            SET repair_state = ?, next_report_attempt = NULL
            WHERE run_id = ? AND result_state = 'REPORT_VALIDATED'
            """,
            (REPAIR_ACCEPTED, advisory.run_id),
        )
    return receipt


def _matching_advisory(service, run_id: str):
    clean_run_id = str(run_id or "").strip()
    if not clean_run_id:
        raise WorkerRuntimeError("run_id cannot be empty.")
    matches = [
        advisory
        for advisory in service.pipeline.discover()
        if advisory.run_id == clean_run_id and advisory.result_contract is not None
    ]
    if not matches:
        raise WorkerRuntimeError(
            f"No OPEN execution-ready Worker result assignment matches {clean_run_id}."
        )
    if len(matches) > 1:
        raise WorkerRuntimeError(
            f"Worker result assignment {clean_run_id} is ambiguous."
        )
    return matches[0]


def _install_revalidation_service() -> None:
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _SERVICE_FLAG, False):
        return

    def revalidate_rejected_result(self, run_id: str) -> dict[str, object]:
        advisory = _matching_advisory(self, run_id)
        receipt = self.result_repair.revalidate_rejected(advisory)
        return {
            "status": "succeeded",
            "receipt": receipt.to_dict(),
            "result_ingestion": self.result_ingester.status(limit=100),
            "result_repair": self.result_repair.status(limit=100),
            "verification": self.verification.status(limit=100),
        }

    service_class.revalidate_rejected_result = revalidate_rejected_result
    setattr(service_class, _SERVICE_FLAG, True)


def _canonical_artifact_path(row, run_id: str, artifact_kind: str) -> str:
    return artifact_path(
        str(row["owning_department"]),
        str(row["worker_id"]),
        run_id,
        artifact_kind,
        1,
    )


def _ingest_hq_review_if_present(
    self: WorkerGitHubOrchestrator,
    run_id: str,
    advisory_id: str,
) -> None:
    row = self._row(run_id)
    if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
        return
    if str(row["hq_review_state"] or ""):
        return
    review_path = _canonical_artifact_path(row, run_id, "hq_review")
    if not self._artifact_exists(review_path):
        return
    payload = self.operations.ingest_hq_review(run_id)
    receipt = payload.get("receipt") or {}
    self._event(
        "hq_review_ingestion",
        "succeeded",
        f"HQ review reached {receipt.get('result_state') or receipt.get('review_state')}.",
        run_id=run_id,
        advisory_id=advisory_id,
    )


def _ingest_rob_validation_if_present(
    self: WorkerGitHubOrchestrator,
    run_id: str,
    advisory_id: str,
) -> None:
    row = self._row(run_id)
    if row is None or not bool(row["requires_rob_validation"]):
        return
    if str(row["rob_validation_state"] or ""):
        return
    validation_path = _canonical_artifact_path(row, run_id, "rob_validation")
    if not self._artifact_exists(validation_path):
        return
    payload = self.operations.ingest_rob_validation(run_id)
    receipt = payload.get("receipt") or {}
    self._event(
        "rob_validation_ingestion",
        "succeeded",
        f"Rob validation reached {receipt.get('result_state') or receipt.get('validation_state')}.",
        run_id=run_id,
        advisory_id=advisory_id,
    )


def _send_hq_wake(
    self: WorkerGitHubOrchestrator,
    run_id: str,
    advisory_id: str,
) -> None:
    row = self._row(run_id)
    if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
        return
    review_path = _canonical_artifact_path(row, run_id, "hq_review")
    if self._artifact_exists(review_path):
        self._ingest_hq_review_if_present(run_id, advisory_id)
        return
    if str(row["hq_wake_state"] or "") or str(row["hq_review_state"] or ""):
        return

    command_center = self.operations.command_center
    if command_center.paused:
        return
    run_lock = command_center._run_lock  # noqa: SLF001 - shared browser execution gate
    if not run_lock.acquire(blocking=False):
        return
    try:
        _ensure_hq_wake_claim_column(self)
        row = self._row(run_id)
        if row is None or str(row["result_state"] or "") != "REPORT_VALIDATED":
            return
        pending_review_path = _canonical_artifact_path(row, run_id, "hq_review")
        if self._artifact_exists(pending_review_path):
            self._ingest_hq_review_if_present(run_id, advisory_id)
            return
        if str(row["hq_wake_state"] or "") or str(row["hq_review_state"] or ""):
            return
        if row["hq_wake_claimed_at"] is not None or not _claim_hq_wake(self, row):
            self._event(
                "hq_review_wake",
                "suppressed",
                "A prior HQ wake claim exists; automatic duplicate dispatch was suppressed.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            return

        command = [
            sys.executable,
            str(self.app_root / "automation" / "run_worker_hq_review_wake.py"),
            "--run-id",
            run_id,
            "--repository-root",
            str(self.repository_root),
            "--database-path",
            str(self.database_path),
            "--cdp-endpoint",
            self.operations.cdp_endpoint,
            "--timeout-seconds",
            str(self.timeout_seconds),
            "--send",
            "--confirm-send",
            "HQ_REVIEW_SEND",
        ]
        try:
            completed = subprocess.run(
                command,
                cwd=self.app_root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds + 30,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            command_center.trip_safety_pause(
                reason=(
                    "Automatic HQ review wake timed out after its atomic claim; "
                    "submission could not be proven."
                ),
                affected_run_id=run_id,
                trigger="hq_review_orchestrator_transport",
            )
            self._event(
                "hq_review_wake",
                "held",
                (
                    "HQ wake transport timed out after the atomic claim; "
                    "automatic retry is suppressed."
                ),
                run_id=run_id,
                advisory_id=advisory_id,
            )
            raise WorkerRuntimeError("Automatic HQ review wake timed out.") from exc
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            self._event(
                "hq_review_wake",
                "held",
                detail or "Guarded HQ review wake stopped before verified completion.",
                run_id=run_id,
                advisory_id=advisory_id,
            )
            raise WorkerRuntimeError(detail or "Guarded HQ review wake failed.")
        current = self._row(run_id)
        if current is None or str(current["hq_wake_state"] or "") != "HQ_WAKE_SUBMITTED":
            command_center.trip_safety_pause(
                reason=(
                    "Guarded HQ review wake returned success without persisted submission evidence."
                ),
                affected_run_id=run_id,
                trigger="hq_review_orchestrator_persistence",
            )
            raise WorkerRuntimeError(
                "Guarded HQ review wake did not persist authoritative submission evidence."
            )
    finally:
        run_lock.release()
    self._event(
        "hq_review_wake",
        "succeeded",
        f"Owning HQ was woken for {run_id} through the guarded send path.",
        run_id=run_id,
        advisory_id=advisory_id,
    )


def _install_orchestrator_repairs() -> None:
    orchestrator_class = WorkerGitHubOrchestrator
    if getattr(orchestrator_class, _ORCHESTRATOR_FLAG, False):
        return
    original_dispatch_new = orchestrator_class._dispatch_new
    original_status = orchestrator_class.status

    def dispatch_new(self, advisories) -> None:
        if not _truthy_environment(
            "LIFEOS_WORKER_AUTO_DISPATCH_ENABLED",
            default=False,
        ):
            return
        original_dispatch_new(self, advisories)

    def status(self) -> dict[str, object]:
        payload = original_status(self)
        payload["auto_dispatch_enabled"] = _truthy_environment(
            "LIFEOS_WORKER_AUTO_DISPATCH_ENABLED",
            default=False,
        )
        payload["automatic_continuation_enabled"] = True
        return payload

    orchestrator_class._dispatch_new = dispatch_new
    orchestrator_class._send_hq_wake = _send_hq_wake
    orchestrator_class._ingest_hq_review_if_present = _ingest_hq_review_if_present
    orchestrator_class._ingest_rob_validation_if_present = _ingest_rob_validation_if_present
    orchestrator_class.status = status
    setattr(orchestrator_class, _ORCHESTRATOR_FLAG, True)


def install_worker_pipeline_reliability_runtime() -> bool:
    """Install the bounded Worker continuation repair once."""

    if getattr(worker_operations, _INSTALL_FLAG, False):
        return False
    if not getattr(WorkerResultIngester, _VALIDATOR_FLAG, False):
        WorkerResultIngester._validate_report_correlation = _validate_report_correlation
        setattr(WorkerResultIngester, _VALIDATOR_FLAG, True)
    WorkerResultRepairCoordinator.revalidate_rejected = _revalidate_rejected
    _install_revalidation_service()
    _install_orchestrator_repairs()
    setattr(worker_operations, _INSTALL_FLAG, True)
    return True


install_worker_pipeline_reliability_runtime()


__all__ = [
    "_canonical_artifact_path",
    "_normalized_scope",
    "_parse_evidence_reference",
    "_scope_allows",
    "_truthy_environment",
    "install_worker_pipeline_reliability_runtime",
]
