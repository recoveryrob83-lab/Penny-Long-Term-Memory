"""Install Package E Slice 2 response reconciliation on Worker Operations."""

from __future__ import annotations

import json
from pathlib import Path

from . import worker_advisory_pipeline, worker_operations
from .worker_response_receiver import WORKER_REPORT_PREFIX, WorkerResponseReceiver
from .worker_runtime import WorkerRuntimeError

_INSTALL_FLAG = "_lifeos_worker_response_receiver_installed"
_SERVICE_ATTR = "_lifeos_worker_response_receiver_service"
_RENDER_FLAG = "_lifeos_worker_report_requirement_installed"


def _report_requirement(
    advisory: worker_advisory_pipeline.ExecutionReadyAdvisory,
) -> str:
    """Render a technical response schema without copying assignment authority."""

    template = {
        "wrapper_id": advisory.wrapper_id,
        "run_id": advisory.run_id,
        "worker_id": advisory.target_worker_id,
        "profile_version": "<positive integer>",
        "owning_department": "<canonical department id>",
        "task_id": advisory.advisory_id,
        "task_revision": advisory.advisory_revision,
        "procedure_id": advisory.procedure_id,
        "procedure_version": advisory.procedure_version,
        "authorization_source": advisory.authorization_source,
        "verification_mode": advisory.verification_mode,
        "controlled_outcome": "<IMPLEMENT|REPORT_AND_HOLD|ELEVATE_FOR_APPROVAL>",
        "completion_state": "<completed|partial|failed|not_attempted>",
        "evidence_references": ["<current evidence reference>"],
        "actual_read_scopes": ["<exact scope actually read>"],
        "actual_write_scopes": [],
        "actual_tools": ["<tool actually used>"],
        "verification_state": "<verified|pending|unavailable>",
        "external_actions_verified": True,
        "approval_required_discovered": False,
        "failure_reason": None,
    }
    return (
        "\n\nPackage E response contract: after the human-readable evidence report, emit "
        "exactly one final line beginning `LIFEOS_WORKER_REPORT=` followed by one JSON "
        "object. Replace every angle-bracket placeholder with truthful run evidence. Do not "
        "emit a second report marker and do not report `verified` when HQ review is still "
        "pending. The Worker-reported outcome is evidence only; the receiver decides the "
        "accepted controlled outcome. Template:\n"
        f"{WORKER_REPORT_PREFIX}{json.dumps(template, separators=(',', ':'))}"
    )


def _install_report_requirement() -> bool:
    if getattr(worker_advisory_pipeline, _RENDER_FLAG, False):
        return False
    original_render = worker_advisory_pipeline.render_reference_only_instruction

    def render_reference_only_instruction(
        advisory: worker_advisory_pipeline.ExecutionReadyAdvisory,
    ) -> str:
        return original_render(advisory) + _report_requirement(advisory)

    worker_advisory_pipeline.render_reference_only_instruction = (
        render_reference_only_instruction
    )
    setattr(worker_advisory_pipeline, _RENDER_FLAG, True)
    return True


def _receiver_message(payload: dict[str, object]) -> str:
    outcome = str(payload.get("controlled_outcome") or "REPORT_AND_HOLD")
    reason = str(payload.get("reason") or "No receiver reason was recorded.")
    if outcome == "IMPLEMENT":
        suffix = (
            " Immediate HQ review is pending."
            if payload.get("hq_review_required")
            else " Receiver verification requirements were satisfied."
        )
        return f"Receiver accepted IMPLEMENT on the existing run row.{suffix}"
    if outcome == "ELEVATE_FOR_APPROVAL":
        return (
            f"Receiver recorded ELEVATE_FOR_APPROVAL on the existing run row: {reason}"
        )
    return f"Receiver recorded REPORT_AND_HOLD on the existing run row: {reason}"


def install_worker_response_receiver() -> bool:
    """Wrap live advisory dispatch once and reconcile successful browser responses."""

    _install_report_requirement()
    service_class = worker_operations.WorkerOperationsService
    if getattr(service_class, _INSTALL_FLAG, False):
        return False
    original_run_advisory = service_class.run_advisory

    def run_advisory(
        self: worker_operations.WorkerOperationsService,
        advisory_id: str,
        *,
        confirm_send: bool,
        timeout_seconds: int = 600,
    ) -> dict[str, object]:
        clean_id = str(advisory_id or "").strip()
        matches = [
            item for item in self.pipeline.discover() if item.advisory_id == clean_id
        ]
        if len(matches) != 1:
            raise WorkerRuntimeError(
                f"Response reconciliation requires one execution-ready advisory for {clean_id}."
            )
        advisory = matches[0]
        payload = original_run_advisory(
            self,
            clean_id,
            confirm_send=confirm_send,
            timeout_seconds=timeout_seconds,
        )
        result = payload.get("result")
        if not isinstance(result, dict) or result.get("status") != "succeeded":
            return payload

        receiver = getattr(self, _SERVICE_ATTR, None)
        if not isinstance(receiver, WorkerResponseReceiver):
            receiver = WorkerResponseReceiver(
                Path(self.command_center.store.database_path), self.repository_root
            )
            setattr(self, _SERVICE_ATTR, receiver)
        entry = self.worker_center.runtime.worker(
            advisory.target_worker_id, require_enabled=True
        )
        reconciliation = receiver.reconcile(
            advisory, entry, str(result.get("stdout") or "")
        )
        receiver_payload = reconciliation.to_dict()
        payload["receiver"] = receiver_payload
        result["transport_status"] = result.get("status")
        result["status"] = {
            "IMPLEMENT": "succeeded",
            "ELEVATE_FOR_APPROVAL": "pending",
            "REPORT_AND_HOLD": "refused",
        }[reconciliation.controlled_outcome]
        result["reason"] = _receiver_message(receiver_payload)
        result["receiver_outcome"] = reconciliation.controlled_outcome
        result["hq_review_required"] = reconciliation.hq_review_required
        payload["status"] = self.status()
        return payload

    service_class.run_advisory = run_advisory
    setattr(service_class, _INSTALL_FLAG, True)
    return True


install_worker_response_receiver()


__all__ = ["install_worker_response_receiver"]
