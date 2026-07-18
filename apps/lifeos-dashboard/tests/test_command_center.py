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
    assert DESTINATIONS["main"].chat_title == "Chief of Staff HQ"
    assert DESTINATIONS["logistics"].chat_title == "Life OS Maintenance HQ"


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


def test_destination_mismatch_requires_explicit_confirmation() -> None:
    job = CommandJob(
        destination="logistics",
        prompt_type="custom",
        custom_prompt="Boot Engineering HQ.",
        default_destination="engineering",
        confirm_destination=False,
    )

    with pytest.raises(CommandCenterError, match="Destination mismatch requires explicit confirmation"):
        validate_job(job)


def test_confirmed_destination_mismatch_can_build_command() -> None:
    job = CommandJob(
        destination="logistics",
        prompt_type="custom",
        custom_prompt="Use this intentionally in Life OS Maintenance HQ.",
        default_destination="engineering",
        confirm_destination=True,
    )

    command = build_command(job, APP_ROOT)

    assert "Life OS Maintenance HQ" in command
    assert command[-2:] == ["--text", "Use this intentionally in Life OS Maintenance HQ."]


def test_unknown_default_destination_is_refused() -> None:
    job = CommandJob(
        destination="logistics",
        prompt_type="custom",
        custom_prompt="Do the thing.",
        default_destination="unknown",
        confirm_destination=True,
    )

    with pytest.raises(CommandCenterError, match="not recognized"):
        validate_job(job)


def test_summary_is_plain_language() -> None:
    job = CommandJob(destination="logistics", prompt_type="canonical")

    assert summarize_job(job) == (
        "Place as a verified draft the canonical boot prompt in Life OS Maintenance HQ."
    )
