from pathlib import Path

import pytest

from lifeos_dashboard.command_center import (
    CommandCenterError,
    CommandJob,
    DESTINATIONS,
    build_command,
    summarize_job,
    validate_job,
)


APP_ROOT = Path("C:/LifeOS/apps/lifeos-dashboard")


def test_phase_one_exposes_eight_exact_destinations() -> None:
    assert set(DESTINATIONS) == {
        "hub",
        "main",
        "engineering",
        "logistics",
        "business",
        "office-leaks",
        "finance",
        "wellness",
    }
    assert DESTINATIONS["hub"].chat_title == "LifeOS HQ"


def test_draft_is_default_and_does_not_add_send_flags() -> None:
    job = CommandJob(destination="main", prompt_type="canonical")

    command = build_command(job, APP_ROOT)

    assert command[-1] == "main"
    assert "--send" not in command
    assert "--confirm-send" not in command


def test_send_requires_explicit_confirmation() -> None:
    job = CommandJob(
        destination="main",
        prompt_type="canonical",
        mode="send",
        confirm_send=False,
    )

    with pytest.raises(CommandCenterError, match="explicit confirmation"):
        validate_job(job)


def test_confirmed_send_adds_existing_engine_gate() -> None:
    job = CommandJob(
        destination="hub",
        prompt_type="canonical",
        mode="send",
        confirm_send=True,
    )

    command = build_command(job, APP_ROOT)

    assert command[-3:] == ["--send", "--confirm-send", "SEND"]


def test_custom_prompt_uses_exact_chat_title() -> None:
    job = CommandJob(
        destination="office-leaks",
        prompt_type="custom",
        custom_prompt="Review the active lead-loss campaign.",
    )

    command = build_command(job, APP_ROOT)

    assert "Office Leaks HQ" in command
    assert command[-2:] == ["--text", "Review the active lead-loss campaign."]


def test_custom_prompt_cannot_be_blank() -> None:
    job = CommandJob(destination="wellness", prompt_type="custom", custom_prompt="   ")

    with pytest.raises(CommandCenterError, match="cannot be empty"):
        validate_job(job)


def test_summary_is_plain_language() -> None:
    job = CommandJob(destination="logistics", prompt_type="canonical")

    assert summarize_job(job) == (
        "Place as a verified draft the canonical boot prompt in Logistics HQ."
    )
