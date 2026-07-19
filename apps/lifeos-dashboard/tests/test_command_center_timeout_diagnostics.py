from pathlib import Path
import subprocess

import pytest

from lifeos_dashboard import command_center
from lifeos_dashboard import command_center_timeout_diagnostics_runtime as runtime


def test_timeout_reports_last_physical_input_stage(monkeypatch: pytest.MonkeyPatch) -> None:
    job = command_center.CommandJob(
        destination="engineering",
        prompt_type="custom",
        custom_prompt="Diagnostic prompt",
    )
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd=["python", "worker.py"],
            timeout=120,
            output=b"",
            stderr=b"LIFEOS_STAGE=foreground_verified\nLIFEOS_STAGE=composer_activation_start\n",
        )

    monkeypatch.setattr(runtime.subprocess, "run", raise_timeout)

    result = runtime.run_job(job, Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "failed"
    assert "activating the destination composer" in result.reason
    assert "Nothing was sent" in result.reason
    assert "LIFEOS_STAGE=composer_activation_start" in result.stderr


def test_timeout_without_stage_remains_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    job = command_center.CommandJob(
        destination="engineering",
        prompt_type="custom",
        custom_prompt="Diagnostic prompt",
    )
    monkeypatch.setattr(command_center, "build_command", lambda job, app_root: ["python", "worker.py"])

    def raise_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=["python", "worker.py"], timeout=120)

    monkeypatch.setattr(runtime.subprocess, "run", raise_timeout)

    result = runtime.run_job(job, Path("C:/LifeOS/apps/lifeos-dashboard"))

    assert result.status == "failed"
    assert "before it reported a physical-input stage" in result.reason
    assert "Nothing was sent" in result.reason
