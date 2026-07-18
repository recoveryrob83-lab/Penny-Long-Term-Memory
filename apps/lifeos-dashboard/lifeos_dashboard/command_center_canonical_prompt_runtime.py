"""Attach the protected canonical prompt catalog to the Command Center."""
from __future__ import annotations

import sys
from pathlib import Path

from . import command_center
from .canonical_prompt_catalog import catalog_metadata, definition_for, render_prompt

_original_build_command = command_center.build_command
_original_canonical_prompt = command_center.CommandCenterService.canonical_prompt
_original_prepare_schedule = command_center.CommandCenterService._prepare_schedule
_original_status = command_center.CommandCenterService.status


def _split_destination_token(value: str) -> tuple[str, str]:
    destination, separator, prompt_key = value.partition("~")
    return destination, prompt_key if separator else "boot"


def build_command(job: command_center.CommandJob, app_root: Path) -> list[str]:
    """Execute rendered canonical snapshots through the verified generic engine."""
    destination = command_center.validate_job(job)
    if job.prompt_type != "canonical" or not job.custom_prompt.strip():
        return _original_build_command(job, app_root)

    command = [
        sys.executable,
        str(app_root / "automation" / "open_department_chat_group_verified.py"),
        destination.chat_title,
        "--text",
        job.custom_prompt,
    ]
    if job.mode == "send":
        command.extend(["--send", "--confirm-send", "SEND"])
    return command


def canonical_prompt(
    self: command_center.CommandCenterService,
    destination_token: str,
) -> dict[str, str]:
    destination_key, prompt_key = _split_destination_token(destination_token)
    destination = command_center.DESTINATIONS.get(destination_key)
    if destination is None:
        raise command_center.CommandCenterError(
            "Unknown destination. Exact LifeOS destination required."
        )
    try:
        definition = definition_for(prompt_key)
    except ValueError as exc:
        raise command_center.CommandCenterError(str(exc)) from exc

    boot = _original_canonical_prompt(self, destination_key)
    prompt = render_prompt(
        prompt_key,
        destination_label=destination.label,
        boot_prompt=boot["prompt"],
    )
    return {
        "key": definition.key,
        "name": f"{destination.label} {definition.label}",
        "prompt": prompt,
    }


def prepare_schedule(
    self: command_center.CommandCenterService,
    values: dict[str, object],
) -> dict[str, object]:
    """Preserve a canonical key in source_type while snapshotting rendered text."""
    source_type = str(values.get("source_type") or "")
    if not source_type.startswith("canonical:"):
        return _original_prepare_schedule(self, values)

    prompt_key = source_type.split(":", 1)[1]
    try:
        definition_for(prompt_key)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc

    normalized = dict(values)
    normalized["source_type"] = "canonical"
    prepared = _original_prepare_schedule(self, normalized)
    if not str(prepared.get("custom_prompt") or "").strip():
        raise ValueError("Canonical schedules must snapshot the rendered prompt text.")
    prepared["source_type"] = source_type
    return prepared


def status(self: command_center.CommandCenterService) -> dict[str, object]:
    current = _original_status(self)
    current["canonical_prompts"] = catalog_metadata()
    return current


command_center.build_command = build_command
command_center.CommandCenterService.canonical_prompt = canonical_prompt
command_center.CommandCenterService._prepare_schedule = prepare_schedule
command_center.CommandCenterService.status = status
