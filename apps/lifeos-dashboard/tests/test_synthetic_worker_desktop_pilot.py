import importlib.util
import json
import subprocess
from pathlib import Path

import pytest


SCRIPT = (
    Path(__file__).parents[1]
    / "automation"
    / "run_synthetic_worker_desktop_pilot.py"
)
SPEC = importlib.util.spec_from_file_location("synthetic_worker_desktop_pilot", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)

APP_ROOT = Path("C:/LifeOS/apps/lifeos-dashboard")


def test_envelope_is_synthetic_unique_and_non_authoritative() -> None:
    envelope = pilot.build_envelope(timestamp=1234567890, nonce="abc123")

    assert envelope.wrapper_id == "SYNTH-DESKTOP-WRAP-1234567890-abc123"
    assert envelope.run_id == "SYNTH-DESKTOP-RUN-1234567890-abc123"
    assert envelope.task_id == "SYNTH-DESKTOP-TASK-1234567890-abc123"
    assert envelope.worker_id == "synthetic_desktop_worker"
    assert envelope.authorization_source == (
        "ROB-BOUNDED-SYNTHETIC-DESKTOP-PILOT-20260719"
    )
    assert envelope.verification_mode == "IMMEDIATE_HQ"


def test_instruction_forbids_durable_or_external_action() -> None:
    envelope = pilot.build_envelope(timestamp=1, nonce="safe1")
    instruction = pilot.build_instruction(envelope)

    assert "no real authority" in instruction
    assert "Do not create or modify durable records" in instruction
    assert f"SYNTHETIC_WRAPPER_RECEIVED {envelope.wrapper_id}" in instruction


def test_draft_plan_is_locked_to_disposable_title_and_wrapper_marker() -> None:
    plan = pilot.build_plan(APP_ROOT, send=False, timestamp=1, nonce="draft1")
    command = list(plan.command)

    assert plan.mode == "draft"
    assert pilot.SYNTHETIC_CHAT_TITLE == "Synthetic_Worker_Pilot"
    assert command[2] == "Synthetic_Worker_Pilot"
    project_index = command.index("--project")
    assert command[project_index + 1] == "Life OS"
    marker_index = command.index("--verify-marker")
    assert command[marker_index + 1] == plan.envelope.wrapper_id
    assert "--send" not in command
    assert "LIFEOS_EXECUTION_WRAPPER=" in command[command.index("--text") + 1]


def test_send_plan_adds_only_base_transport_confirmation() -> None:
    plan = pilot.build_plan(APP_ROOT, send=True, timestamp=1, nonce="send1")
    command = list(plan.command)

    assert plan.mode == "send"
    assert command[-3:] == ["--send", "--confirm-send", "SEND"]


def test_send_requires_exact_synthetic_confirmation() -> None:
    args = pilot.parse_args(["--send", "--confirm-send", "wrong"])

    with pytest.raises(pilot.SyntheticDesktopPilotError, match="SYNTHETIC_SEND"):
        pilot.validate_args(args)

    valid = pilot.parse_args(["--send", "--confirm-send", "SYNTHETIC_SEND"])
    pilot.validate_args(valid)


def test_confirmation_without_send_is_refused() -> None:
    args = pilot.parse_args(["--confirm-send", "SYNTHETIC_SEND"])

    with pytest.raises(pilot.SyntheticDesktopPilotError, match="only when --send"):
        pilot.validate_args(args)


def test_dry_run_emits_non_authoritative_receipt_without_subprocess(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def should_not_run(*args, **kwargs):
        raise AssertionError("dry run must not open ChatGPT Classic")

    monkeypatch.setattr(pilot.subprocess, "run", should_not_run)
    monkeypatch.setattr(
        pilot,
        "build_envelope",
        lambda **kwargs: pilot.ExecutionEnvelope(
            wrapper_id="WRAP-DRY",
            run_id="RUN-DRY",
            worker_id="synthetic_desktop_worker",
            task_id="TASK-DRY",
            task_revision=1,
            procedure_id="synthetic_desktop_transport",
            procedure_version=1,
            authorization_source=pilot.SYNTHETIC_AUTHORIZATION_SOURCE,
            verification_mode="IMMEDIATE_HQ",
        ),
    )

    assert pilot.main(["--dry-run"]) == 0
    output = capsys.readouterr().out
    receipt_line = next(
        line for line in output.splitlines() if line.startswith(pilot.RECEIPT_PREFIX)
    )
    receipt = json.loads(receipt_line.removeprefix(pilot.RECEIPT_PREFIX))
    assert receipt["status"] == "dry_run"
    assert receipt["chat_title"] == "Synthetic_Worker_Pilot"
    assert receipt["durable_authority_created"] is False


def test_successful_transport_emits_success_receipt(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        pilot.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0], returncode=0, stdout="Message submitted.\n", stderr=""
        ),
    )
    plan = pilot.build_plan(APP_ROOT, send=True, timestamp=1, nonce="ok1")

    assert pilot.run_plan(plan, APP_ROOT, timeout_seconds=90) == 0
    output = capsys.readouterr().out
    assert "Message submitted." in output
    assert '"status": "succeeded"' in output
    assert '"durable_authority_created": false' in output


def test_failed_transport_returns_failure_without_claiming_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        pilot.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args[0], returncode=1, stdout="", stderr="STOPPED: destination mismatch\n"
        ),
    )
    plan = pilot.build_plan(APP_ROOT, send=False, timestamp=1, nonce="fail1")

    assert pilot.run_plan(plan, APP_ROOT, timeout_seconds=90) == 1
    captured = capsys.readouterr()
    assert "destination mismatch" in captured.err
    assert '"status": "failed"' in captured.out


def test_timeout_is_bounded_and_emits_timeout_receipt(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def timed_out(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])

    monkeypatch.setattr(pilot.subprocess, "run", timed_out)
    plan = pilot.build_plan(APP_ROOT, send=False, timestamp=1, nonce="time1")

    assert pilot.run_plan(plan, APP_ROOT, timeout_seconds=90) == 1
    output = capsys.readouterr().out
    assert '"status": "timed_out"' in output
