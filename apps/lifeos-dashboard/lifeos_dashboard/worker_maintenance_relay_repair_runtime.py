"""Repair cross-department Worker result validation and owning-HQ relay behavior.

This runtime layer keeps GitHub artifacts immutable while aligning broad path scopes,
Git evidence references, canonical department project roots, correction-attempt
recognition, and automatic HQ wakes with existing safety controls.
"""
from __future__ import annotations

import re
from collections.abc import Iterable

from . import worker_github_orchestrator_runtime
from .command_center_send_budget import BUDGET_RECOVERY_CONDITION
from .worker_github_orchestrator import WorkerGitHubOrchestrator
from .worker_result_contract import artifact_path
from .worker_result_ingester import WorkerResultIngester
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_maintenance_relay_repair_runtime_installed"
_INGESTER_FLAG = "_lifeos_cross_department_result_validation_installed"
_ORCHESTRATOR_FLAG = "_lifeos_cross_department_hq_relay_installed"
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_RESULT_TERMINAL_STATES = {
    "REPORT_VALIDATED",
    "HQ_VERIFIED",
    "HQ_REJECTED",
    "ROB_VALIDATION_REQUIRED",
    "ROB_VERIFIED",
    "ROB_REJECTED",
    "READY_FOR_COS",
}


def _normalized_scope(value: object) -> str:
    clean = str(value or "").strip().replace("\\", "/").strip("/")
    if " (" in clean:
        clean = clean.split(" (", 1)[0].rstrip()
    while "//" in clean:
        clean = clean.replace("//", "/")
    return clean


def _scope_allows(allowed: object, actual: object) -> bool:
    allowed_path = _normalized_scope(allowed)
    actual_path = _normalized_scope(actual)
    return bool(
        allowed_path
        and actual_path
        and (
            actual_path == allowed_path
            or actual_path.startswith(allowed_path + "/")
        )
    )


def _unauthorized_scopes(
    allowed_scopes: Iterable[object],
    actual_scopes: Iterable[object],
) -> list[str]:
    allowed = tuple(allowed_scopes)
    return sorted(
        str(actual)
        for actual in actual_scopes
        if not any(_scope_allows(candidate, actual) for candidate in allowed)
    )


def _uncovered_scopes(
    requested_scopes: Iterable[object],
    actual_scopes: Iterable[object],
) -> list[str]:
    actual = tuple(actual_scopes)
    return sorted(
        str(requested)
        for requested in requested_scopes
        if not any(_scope_allows(requested, observed) for observed in actual)
    )


def _parse_evidence_reference(
    reference: object,
) -> tuple[str, str | None, str | None]:
    text = str(reference or "").strip()
    path, separator, witness = text.partition("@")
    path = _normalized_scope(path)
    witness = witness.strip()
    if not separator or not path or not witness:
        raise WorkerRuntimeError(
            f"Evidence reference lacks path correlation: {text}"
        )
    if witness == "preflight:not-found":
        return path, None, None
    if _HEX40.fullmatch(witness):
        return path, None, witness
    if witness.startswith("blob:"):
        blob_sha = witness.removeprefix("blob:")
        if _HEX40.fullmatch(blob_sha):
            return path, None, blob_sha
    commit_token, marker, blob_token = witness.partition("@")
    if (
        marker
        and commit_token.startswith("commit:")
        and blob_token.startswith("blob:")
    ):
        commit_sha = commit_token.removeprefix("commit:")
        blob_sha = blob_token.removeprefix("blob:")
        if _HEX40.fullmatch(commit_sha) and _HEX40.fullmatch(blob_sha):
            return path, commit_sha, blob_sha
    raise WorkerRuntimeError(
        f"Evidence reference witness is invalid: {text}"
    )


def _verify_git_witness(
    ingester: WorkerResultIngester,
    *,
    reference: object,
    commit_sha: str | None,
    blob_sha: str | None,
) -> None:
    try:
        if commit_sha is not None:
            if ingester._git("cat-file", "-t", commit_sha) != "commit":
                raise WorkerRuntimeError(
                    f"Evidence witness is not a Git commit: {reference}"
                )
        if blob_sha is not None:
            if ingester._git("cat-file", "-t", blob_sha) != "blob":
                raise WorkerRuntimeError(
                    f"Evidence witness is not a Git blob: {reference}"
                )
    except WorkerRuntimeError as exc:
        if "is not a Git" in str(exc):
            raise
        raise WorkerRuntimeError(
            f"Evidence Git object is unavailable: {reference}"
        ) from exc


def _install_result_validation() -> None:
    ingester_class = WorkerResultIngester
    if getattr(ingester_class, _INGESTER_FLAG, False):
        return

    def validate_report_correlation(
        self: WorkerResultIngester,
        advisory,
        profile,
        payload: dict[str, object],
    ) -> None:
        contract = advisory.result_contract
        if contract is None:
            raise WorkerRuntimeError(
                "Canonical assignment has no Worker result contract."
            )

        errors: list[str] = []
        for field_name, expected in self._expected_identity(advisory).items():
            if payload.get(field_name) != expected:
                errors.append(
                    f"report {field_name} does not match the canonical assignment"
                )

        expected_profile = {
            "profile_version": profile.profile_version,
            "owning_department": profile.owning_department,
            "attempt": contract.attempt,
        }
        for field_name, expected in expected_profile.items():
            if payload.get(field_name) != expected:
                errors.append(
                    f"report {field_name} does not match canonical Worker state"
                )
        if profile.worker_id != advisory.target_worker_id:
            errors.append(
                "registered Worker does not match the canonical assignment"
            )

        actual_reads = tuple(payload.get("actual_read_scopes") or ())
        actual_writes = tuple(payload.get("actual_write_scopes") or ())
        actual_tools = {
            str(item) for item in payload.get("actual_tools") or ()
        }
        allowed_reads = (
            *advisory.requested_read_scopes,
            *advisory.requested_write_scopes,
        )

        unauthorized_reads = _unauthorized_scopes(
            allowed_reads,
            actual_reads,
        )
        unauthorized_writes = _unauthorized_scopes(
            advisory.requested_write_scopes,
            actual_writes,
        )
        unauthorized_tools = sorted(
            actual_tools - set(advisory.requested_tools)
        )
        if unauthorized_reads:
            errors.append(
                "actual read scopes exceed assignment: "
                + ", ".join(unauthorized_reads)
            )
        if unauthorized_writes:
            errors.append(
                "actual write scopes exceed assignment: "
                + ", ".join(unauthorized_writes)
            )
        if unauthorized_tools:
            errors.append(
                "actual tools exceed assignment: "
                + ", ".join(unauthorized_tools)
            )
        if contract.result_path not in actual_writes:
            errors.append(
                "actual write scopes do not include the exact report path"
            )

        if payload.get("controlled_outcome") == "IMPLEMENT":
            missing_reads = _uncovered_scopes(
                advisory.requested_read_scopes,
                actual_reads,
            )
            if missing_reads:
                errors.append(
                    "implemented report omits requested read scopes: "
                    + ", ".join(missing_reads)
                )
            if payload.get("completion_state") != "completed":
                errors.append(
                    "IMPLEMENT requires completion_state completed"
                )
            if payload.get("verification_state") != "pending":
                errors.append(
                    "IMPLEMENT requires pending Department HQ verification"
                )
            if payload.get("failure_reason") is not None:
                errors.append(
                    "IMPLEMENT report cannot contain a failure reason"
                )
        if (
            payload.get("controlled_outcome") == "REPORT_AND_HOLD"
            and not payload.get("failure_reason")
        ):
            errors.append(
                "REPORT_AND_HOLD requires a failure reason"
            )

        evidence_paths: set[str] = set()
        allowed_evidence_paths = (
            *advisory.source_references,
            *advisory.requested_read_scopes,
            *advisory.requested_write_scopes,
        )
        for reference in payload.get("evidence_references") or ():
            try:
                path, commit_sha, blob_sha = _parse_evidence_reference(
                    reference
                )
            except WorkerRuntimeError as exc:
                errors.append(str(exc))
                continue
            evidence_paths.add(path)
            if not any(
                _scope_allows(allowed, path)
                for allowed in allowed_evidence_paths
            ):
                errors.append(
                    f"evidence reference path is outside assignment: {path}"
                )
                continue
            if commit_sha is None and blob_sha is None:
                if path != _normalized_scope(contract.result_path):
                    errors.append(
                        "preflight:not-found is allowed only for the report path"
                    )
                continue
            try:
                _verify_git_witness(
                    self,
                    reference=reference,
                    commit_sha=commit_sha,
                    blob_sha=blob_sha,
                )
            except WorkerRuntimeError as exc:
                errors.append(str(exc))

        if payload.get("controlled_outcome") == "IMPLEMENT":
            missing_evidence = sorted(
                str(source)
                for source in advisory.source_references
                if not any(
                    _scope_allows(source, evidence_path)
                    for evidence_path in evidence_paths
                )
            )
            if missing_evidence:
                errors.append(
                    "implemented report omits source evidence: "
                    + ", ".join(missing_evidence)
                )

        if errors:
            raise WorkerRuntimeError(
                "Worker report correlation failed: "
                + "; ".join(errors)
                + "."
            )

    ingester_class._validate_report_correlation = (
        validate_report_correlation
    )
    setattr(ingester_class, _INGESTER_FLAG, True)


def _canonical_hq_review_path(row, run_id: str) -> str:
    return artifact_path(
        str(row["owning_department"]),
        str(row["worker_id"]),
        run_id,
        "hq_review",
        1,
    )


def _canonical_rob_validation_path(row, run_id: str) -> str:
    return artifact_path(
        str(row["owning_department"]),
        str(row["worker_id"]),
        run_id,
        "rob_validation",
        1,
    )


def _reserve_automatic_hq_wake_budget(
    orchestrator: WorkerGitHubOrchestrator,
    run_id: str,
):
    command_center = orchestrator.operations.command_center
    decision = command_center.reserve_send_budget(
        kind="hq_review_wake",
        run_id=run_id,
    )
    if not decision.reserved:
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
                "An automatic HQ review wake reserved a global send attempt, "
                "but the reservation could not be attached to the authoritative "
                "execution row. Nothing was sent."
            ),
            affected_run_id=run_id,
            trigger="send_budget_evidence",
            recovery_condition=BUDGET_RECOVERY_CONDITION,
        )
        raise WorkerRuntimeError(
            "Automatic HQ review send-budget evidence could not be persisted "
            "before transport."
        ) from exc
    return decision


def _trip_automatic_hq_wake(
    orchestrator: WorkerGitHubOrchestrator,
    run_id: str,
    reason: str,
) -> None:
    orchestrator.operations.command_center.trip_safety_pause(
        reason=reason,
        affected_run_id=run_id,
        trigger="hq_review_orchestrator",
    )


def _install_orchestrator_relay() -> None:
    orchestrator_class = WorkerGitHubOrchestrator
    if getattr(orchestrator_class, _ORCHESTRATOR_FLAG, False):
        return

    worker_github_orchestrator_runtime._hq_review_path = (
        _canonical_hq_review_path
    )
    guarded_send_hq_wake = orchestrator_class._send_hq_wake

    def ingest_result_if_present(
        self: WorkerGitHubOrchestrator,
        advisory,
    ) -> None:
        contract = advisory.result_contract
        if contract is None:
            return
        row = self._row(advisory.run_id)
        if row is None:
            return
        state = str(row["result_state"] or "")
        if state in _RESULT_TERMINAL_STATES:
            return

        if state == "REPORT_REJECTED":
            if str(row["repair_state"] or "") != "REPORT_REPAIR_PENDING":
                return
            wake = self.operations.result_repair.repair_wake(
                advisory.run_id
            )
            if wake is None:
                return
            candidate_path = wake.corrected_report_path
        else:
            candidate_path = contract.result_path

        if not self._artifact_exists(candidate_path):
            return
        payload = self.operations.ingest_result(advisory.run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "result_ingestion",
            "succeeded",
            "Worker result reached "
            f"{receipt.get('report_state') or receipt.get('result_state')}.",
            run_id=advisory.run_id,
            advisory_id=advisory.advisory_id,
        )

    def ingest_hq_review_if_present(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if (
            row is None
            or str(row["result_state"] or "") != "REPORT_VALIDATED"
        ):
            return
        if str(row["hq_review_state"] or ""):
            return
        review_path = _canonical_hq_review_path(row, run_id)
        if not self._artifact_exists(review_path):
            return
        payload = self.operations.ingest_hq_review(run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "hq_review_ingestion",
            "succeeded",
            "HQ review reached "
            f"{receipt.get('result_state') or receipt.get('review_state')}.",
            run_id=run_id,
            advisory_id=advisory_id,
        )

    def ingest_rob_validation_if_present(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if row is None or not bool(row["requires_rob_validation"]):
            return
        if str(row["rob_validation_state"] or ""):
            return
        validation_path = _canonical_rob_validation_path(row, run_id)
        if not self._artifact_exists(validation_path):
            return
        payload = self.operations.ingest_rob_validation(run_id)
        receipt = payload.get("receipt") or {}
        self._event(
            "rob_validation_ingestion",
            "succeeded",
            "Rob validation reached "
            f"{receipt.get('result_state') or receipt.get('validation_state')}.",
            run_id=run_id,
            advisory_id=advisory_id,
        )

    def send_hq_wake(
        self: WorkerGitHubOrchestrator,
        run_id: str,
        advisory_id: str,
    ) -> None:
        row = self._row(run_id)
        if (
            row is None
            or str(row["result_state"] or "") != "REPORT_VALIDATED"
        ):
            return
        review_path = _canonical_hq_review_path(row, run_id)
        if self._artifact_exists(review_path):
            guarded_send_hq_wake(self, run_id, advisory_id)
            return
        if str(row["hq_wake_state"] or ""):
            return
        if str(row["hq_review_state"] or ""):
            return
        if self.operations.command_center.paused:
            return
        run_lock = self.operations.command_center._run_lock
        if run_lock.locked():
            return

        claimed = (
            "hq_wake_claimed_at" in row.keys()
            and row["hq_wake_claimed_at"] is not None
        )
        if not claimed:
            _reserve_automatic_hq_wake_budget(self, run_id)

        try:
            guarded_send_hq_wake(self, run_id, advisory_id)
        except Exception:
            _trip_automatic_hq_wake(
                self,
                run_id,
                "Automatic owning-HQ wake failed or became uncertain after "
                "a send attempt was reserved or previously claimed. Manual "
                "review is required before retry.",
            )
            raise

        current = self._row(run_id)
        if current is None:
            _trip_automatic_hq_wake(
                self,
                run_id,
                "Automatic owning-HQ wake lost its authoritative execution "
                "row after transport. Automatic retry is prohibited.",
            )
            raise WorkerRuntimeError(
                "Automatic owning-HQ wake lost its execution row."
            )

        current_review_path = _canonical_hq_review_path(
            current,
            run_id,
        )
        durable_outcome = bool(
            str(current["hq_wake_state"] or "")
            or str(current["hq_review_state"] or "")
            or self._artifact_exists(current_review_path)
        )
        if not durable_outcome:
            _trip_automatic_hq_wake(
                self,
                run_id,
                "Automatic owning-HQ wake consumed or inherited a send claim "
                "without durable wake or review evidence. Automatic retry is "
                "prohibited.",
            )
            raise WorkerRuntimeError(
                "Automatic owning-HQ wake produced no durable outcome."
            )

        if (
            str(current["hq_wake_state"] or "") == "HQ_WAKE_SUBMITTED"
            and not bool(current["hq_wake_returned_to_source"])
        ):
            _trip_automatic_hq_wake(
                self,
                run_id,
                "Automatic owning-HQ wake did not verify return to the "
                "source chat. Automatic retry is prohibited.",
            )
            raise WorkerRuntimeError(
                "Automatic owning-HQ wake did not verify return to source."
            )

    orchestrator_class._ingest_result_if_present = (
        ingest_result_if_present
    )
    orchestrator_class._ingest_hq_review_if_present = (
        ingest_hq_review_if_present
    )
    orchestrator_class._ingest_rob_validation_if_present = (
        ingest_rob_validation_if_present
    )
    orchestrator_class._send_hq_wake = send_hq_wake
    setattr(orchestrator_class, _ORCHESTRATOR_FLAG, True)


def install_worker_maintenance_relay_repair_runtime() -> bool:
    """Install the bounded cross-department result and HQ relay repairs once."""

    if getattr(WorkerResultIngester, _INSTALL_FLAG, False):
        return False
    _install_result_validation()
    _install_orchestrator_relay()
    setattr(WorkerResultIngester, _INSTALL_FLAG, True)
    return True


install_worker_maintenance_relay_repair_runtime()


__all__ = [
    "_canonical_hq_review_path",
    "_canonical_rob_validation_path",
    "_normalized_scope",
    "_parse_evidence_reference",
    "_reserve_automatic_hq_wake_budget",
    "_scope_allows",
    "_unauthorized_scopes",
    "_uncovered_scopes",
    "install_worker_maintenance_relay_repair_runtime",
]
