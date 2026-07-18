from pathlib import Path

from lifeos_dashboard.canonical_prompt_catalog import CATALOG, catalog_metadata, render_prompt
from lifeos_dashboard.command_center import CommandCenterService, CommandJob, build_command


EXPECTED_KEYS = {
    "boot",
    "quick_boot",
    "full_boot",
    "sync",
    "nightly",
    "advisory",
    "sync_advisory",
    "read_advisory",
    "consume_advisory",
}


def test_catalog_exposes_protected_operational_families() -> None:
    assert {definition.key for definition in CATALOG} == EXPECTED_KEYS
    metadata = catalog_metadata()
    assert all(
        item["scope"] in {"department", "target_department", "current_department"}
        for item in metadata
    )
    consume = next(item for item in metadata if item["key"] == "consume_advisory")
    assert consume["read_only"] is False
    assert all(
        item["read_only"] is True
        for item in metadata
        if item["key"] != "consume_advisory"
    )


def test_rendered_prompts_preserve_command_boundaries() -> None:
    boot = "@GitHub boot and sync.\n\nYou are Engineering HQ.\n"

    assert render_prompt(
        "quick_boot", destination_label="Engineering HQ", boot_prompt=boot
    ).startswith("/BOOT @GitHub")
    assert "Remain read-only" in render_prompt(
        "sync", destination_label="Engineering HQ", boot_prompt=boot
    )
    advisory = render_prompt(
        "advisory", destination_label="Wellness HQ", boot_prompt=boot
    )
    assert "Target department: Wellness HQ" in advisory
    assert "Do not post" in advisory
    consume = render_prompt(
        "consume_advisory", destination_label="Engineering HQ", boot_prompt=boot
    )
    assert "Before changing durable state" in consume
    assert "statement authorizing" in consume


def test_rendered_canonical_snapshot_uses_verified_generic_engine(tmp_path: Path) -> None:
    job = CommandJob(
        destination="engineering",
        prompt_type="canonical",
        custom_prompt="/SYNC @GitHub\n\nRemain read-only.",
    )

    command = build_command(job, tmp_path)

    assert command[1].endswith("open_department_chat_group_verified.py")
    assert command[-2:] == ["--text", "/SYNC @GitHub\n\nRemain read-only."]


def test_legacy_boot_without_snapshot_keeps_existing_boot_engine(tmp_path: Path) -> None:
    command = build_command(
        CommandJob(destination="engineering", prompt_type="canonical"),
        tmp_path,
    )

    assert command[1].endswith("draft_department_boot.py")
    assert command[-1] == "engineering"


def test_catalog_is_exposed_in_command_center_status(tmp_path: Path) -> None:
    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )

    assert {item["key"] for item in service.status()["canonical_prompts"]} == EXPECTED_KEYS


def test_canonical_schedule_snapshots_text_and_preserves_catalog_key(tmp_path: Path) -> None:
    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )
    created = service.create_schedule(
        {
            "name": "Nightly Engineering",
            "destination": "engineering",
            "prompt_type": "canonical",
            "custom_prompt": "/NIGHTLY @GitHub\n\nCurrent HQ: Engineering HQ",
            "mode": "draft",
            "confirm_send": False,
            "default_destination": None,
            "confirm_destination": False,
            "source_type": "canonical:nightly",
            "source_prompt_id": None,
            "cadence": "daily",
            "schedule_date": "2099-01-01",
            "schedule_time": "19:00",
            "weekdays": [],
            "timezone": "America/Chicago",
            "enabled": True,
        }
    )

    assert created["source_type"] == "canonical:nightly"
    assert created["custom_prompt"].startswith("/NIGHTLY @GitHub")
