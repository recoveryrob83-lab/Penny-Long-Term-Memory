import json
from pathlib import Path

import pytest

from lifeos_dashboard import automation_logs_runtime as runtime
from lifeos_dashboard import command_center


CONTEXT_PREFIX = "LIFEOS_RUN_CONTEXT="


def completed_result(job: command_center.CommandJob) -> command_center.ExecutionResult:
    return command_center.ExecutionResult(
        status="succeeded",
        destination=job.destination,
        mode=job.mode,
        prompt_type=job.prompt_type,
        exit_code=0,
        started_at=100.0,
        finished_at=101.25,
        stdout="worker output\n",
        stderr="",
        reason="Completed successfully.",
    )


def context_from_stdout(stdout: str) -> dict[str, object]:
    line = next(line for line in stdout.splitlines() if line.startswith(CONTEXT_PREFIX))
    return json.loads(line.removeprefix(CONTEXT_PREFIX))


def test_manual_run_gets_stable_safe_context_and_history_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = command_center.CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
        history_limit=1,
    )
    prompt = "Private diagnostic prompt body"
    job = command_center.CommandJob(
        destination="engineering",
        prompt_type="custom",
        custom_prompt=prompt,
    )
    monkeypatch.setattr(
        command_center,
        "run_job",
        lambda actual_job, app_root, timeout_seconds=120: completed_result(actual_job),
    )

    result = service.execute(job, timeout_seconds=45)
    context = context_from_stdout(result.stdout)
    stored = service.history()

    assert context["trigger"] == "manual"
    assert context["timeout_seconds"] == 45
    assert context["prompt_length"] == len(prompt)
    assert len(str(context["prompt_sha256"])) == 16
    assert prompt not in result.stdout
    assert context["duration_seconds"] == 1.25
    assert stored[0]["id"] == 1
    assert stored[0]["stdout"] == result.stdout


def test_history_surface_expands_to_diagnostic_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = command_center.CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
        history_limit=1,
    )
    monkeypatch.setattr(
        command_center,
        "run_job",
        lambda actual_job, app_root, timeout_seconds=120: completed_result(actual_job),
    )

    for destination in ("engineering", "business", "wellness"):
        service.execute(
            command_center.CommandJob(
                destination=destination,
                prompt_type="custom",
                custom_prompt=f"Prompt for {destination}",
            )
        )

    rows = service.history()

    assert len(rows) == 3
    assert [row["id"] for row in rows] == [3, 2, 1]


def test_scheduled_context_records_schedule_without_prompt_body() -> None:
    prompt = "Scheduled private prompt"
    job = command_center.CommandJob(
        destination="hub",
        prompt_type="custom",
        custom_prompt=prompt,
    )

    context = runtime._new_context(
        job,
        trigger="scheduled",
        timeout_seconds=120,
        schedule={"id": 7, "name": "Nightly check", "cadence": "daily"},
    )

    assert context["trigger"] == "scheduled"
    assert context["schedule_id"] == 7
    assert context["schedule_name"] == "Nightly check"
    assert context["cadence"] == "daily"
    assert prompt not in json.dumps(context)
