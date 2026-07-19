from pathlib import Path
import subprocess

import pytest

from lifeos_dashboard import command_center
from lifeos_dashboard import command_center_timeout_diagnostics_runtime as runtime


def job() -> command_center.CommandJob:
    return command_center.CommandJob(
        destination="engineering",
        prompt_type="custom",
        custom_prompt="Diagnostic prompt",
    )


def test_timeout_reports_last_physical_input_stage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd=["python", "worker.py"],
            timeout=120,
            output=b"",
            stderr=b"LIFEOS_STAGE=foreground_verified\nLIFEOS_STAGE=composer_activation_start\n",
        )

    monkeypatch.setattr(runtime.subprocess, "run", raise_timeout)
    result = runtime.run_job(job(), Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "failed"
    assert "exceeded 120s while activating the destination composer" in result.reason
    assert "Nothing was sent" in result.reason
    assert "Open Automation Logs" in result.reason
    assert "LIFEOS_STAGE=composer_activation_start" in result.stderr
    assert "LIFEOS_BACKEND=" in result.stdout
    assert '"event":"subprocess_timeout"' in result.stdout


def test_post_paste_verification_timeout_warns_that_draft_may_exist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd=["python", "worker.py"],
            timeout=120,
            output=(
                b"LIFEOS_STAGE=keyboard_paste_start\n"
                b"LIFEOS_STAGE=keyboard_select_all_start\n"
                b"LIFEOS_STAGE=keyboard_copy_start\n"
            ),
            stderr=b"",
        )

    monkeypatch.setattr(runtime.subprocess, "run", raise_timeout)
    result = runtime.run_job(job(), Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert "reached post-paste verification" in result.reason
    assert "draft may be present" in result.reason
    assert "copying composer text for verification" in result.reason
    assert "Nothing was sent" in result.reason


def test_timeout_without_stage_remains_safe_and_points_to_logs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=["python", "worker.py"], timeout=120)

    monkeypatch.setattr(runtime.subprocess, "run", raise_timeout)
    result = runtime.run_job(job(), Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "failed"
    assert "before reporting a physical-input stage" in result.reason
    assert "Nothing was sent" in result.reason
    assert "Open Automation Logs" in result.reason


def test_backend_command_trace_redacts_custom_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    secret_prompt = "Private prompt body that must not appear in diagnostic metadata"
    custom_job = command_center.CommandJob(
        destination="engineering",
        prompt_type="custom",
        custom_prompt=secret_prompt,
    )
    monkeypatch.setattr(
        command_center,
        "build_command",
        lambda job, app_root: ["python", "worker.py", "--text", secret_prompt],
    )
    monkeypatch.setattr(
        runtime.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=["python", "worker.py"],
            returncode=0,
            stdout="worker output\n",
            stderr="",
        ),
    )

    result = runtime.run_job(custom_job, Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "succeeded"
    assert secret_prompt not in result.stdout
    assert "<redacted prompt length=" in result.stdout
    assert "worker output" in result.stdout
    assert '"event":"subprocess_complete"' in result.stdout


def test_unexpected_subprocess_exception_becomes_a_logged_failed_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_os_error(*args, **kwargs):
        raise OSError("Windows refused to launch the child process")

    monkeypatch.setattr(runtime.subprocess, "run", raise_os_error)
    result = runtime.run_job(job(), Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "failed"
    assert "unexpected exception" in result.reason
    assert "Open Automation Logs" in result.reason
    assert "OSError" in result.stderr
    assert "Windows refused to launch" in result.stderr
    assert '"event":"subprocess_exception"' in result.stdout
