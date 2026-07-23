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
EXPECTED_TITLES = {
    "hub": "LifeOS_HQ",
    "logistics": "Maintenance_HQ",
    "engineering": "Engineering_HQ",
    "business": "Business_HQ",
    "office-leaks": "Office_Leaks_HQ",
    "finance": "Finance_HQ",
    "main": "Chief_of_Staff_HQ",
    "wellness": "Wellness_HQ",
}


def test_phase_one_exposes_eight_exact_destinations() -> None:
    assert set(DESTINATIONS) == set(EXPECTED_TITLES)
    assert {key: value.chat_title for key, value in DESTINATIONS.items()} == EXPECTED_TITLES


@pytest.mark.parametrize("destination", EXPECTED_TITLES)
def test_all_hq_destinations_build_draft_only_commands(destination: str) -> None:
    command = build_command(CommandJob(destination=destination, prompt_type="canonical"), APP_ROOT)
    assert command[-1] == destination
    assert "--send" not in command
    assert "--confirm-send" not in command


def test_draft_is_default_and_does_not_add_send_flags() -> None:
    command = build_command(CommandJob(destination="main", prompt_type="canonical"), APP_ROOT)
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
    assert "Office_Leaks_HQ" in command
    assert command[-2:] == ["--text", "Review the active lead-loss campaign."]


def test_custom_prompt_cannot_be_blank() -> None:
    job = CommandJob(destination="wellness", prompt_type="custom", custom_prompt="   ")
    with pytest.raises(CommandCenterError, match="cannot be empty"):
        validate_job(job)


def test_destination_mismatch_requires_explicit_confirmation() -> None:
    job = CommandJob(
        destination="logistics",
        prompt_type="custom",
        custom_prompt="Boot Engineering_HQ.",
        default_destination="engineering",
        confirm_destination=False,
    )
    with pytest.raises(CommandCenterError, match="Destination mismatch requires explicit confirmation"):
        validate_job(job)


def test_confirmed_destination_mismatch_can_build_command() -> None:
    job = CommandJob(
        destination="logistics",
        prompt_type="custom",
        custom_prompt="Use this intentionally in Maintenance_HQ.",
        default_destination="engineering",
        confirm_destination=True,
    )
    command = build_command(job, APP_ROOT)
    assert "Maintenance_HQ" in command
    assert command[-2:] == ["--text", "Use this intentionally in Maintenance_HQ."]


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
        "Place as a verified draft the canonical boot prompt in Maintenance_HQ."
    )
