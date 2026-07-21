"""Shared fail-closed readers for canonical Worker receiver sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from .worker_runtime import WorkerRuntimeError


def clean_inline(value: str) -> str:
    clean = value.strip()
    if len(clean) >= 2 and clean[0] == clean[-1] == "`":
        return clean[1:-1].strip()
    return clean


def read_relative(repository_root: Path, relative_path: str) -> str:
    candidate = (repository_root / relative_path).resolve()
    try:
        candidate.relative_to(repository_root)
    except ValueError as exc:
        raise WorkerRuntimeError(
            "Receiver source path escapes the repository root."
        ) from exc
    if not candidate.is_file():
        raise WorkerRuntimeError(
            f"Required receiver source is missing: {relative_path}"
        )
    return candidate.read_text(encoding="utf-8").lstrip("\ufeff")


def front_matter(text: str) -> dict[str, str]:
    clean = text.lstrip("\ufeff")
    if not clean.startswith("---\n"):
        raise WorkerRuntimeError("Receiver source is missing YAML front matter.")
    end = clean.find("\n---", 4)
    if end < 0:
        raise WorkerRuntimeError("Receiver source front matter is unterminated.")
    values: dict[str, str] = {}
    for raw_line in clean[4:end].splitlines():
        if not raw_line.strip() or raw_line[:1].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        values[key.strip()] = clean_inline(value)
    return values


def json_value(metadata: Mapping[str, str], key: str, expected_type: type) -> object:
    raw = metadata.get(key, "").strip()
    if not raw:
        raise WorkerRuntimeError(f"Receiver contract field {key} is missing.")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError(
            f"Receiver contract field {key} is not valid JSON."
        ) from exc
    if not isinstance(value, expected_type):
        raise WorkerRuntimeError(f"Receiver contract field {key} has the wrong shape.")
    return value


def string_tuple_value(metadata: Mapping[str, str], key: str) -> tuple[str, ...]:
    value = json_value(metadata, key, list)
    assert isinstance(value, list)
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise WorkerRuntimeError(f"Receiver contract field {key} must contain strings.")
    return tuple(item.strip() for item in value)


def positive_int_value(metadata: Mapping[str, str], key: str) -> int:
    try:
        value = int(metadata.get(key, ""))
    except ValueError as exc:
        raise WorkerRuntimeError(
            f"Receiver contract field {key} must be a positive integer."
        ) from exc
    if value < 1:
        raise WorkerRuntimeError(
            f"Receiver contract field {key} must be a positive integer."
        )
    return value


def section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    start += len(marker)
    next_heading = text.find("\n## ", start)
    return text[start : next_heading if next_heading >= 0 else len(text)]


__all__ = [
    "clean_inline",
    "front_matter",
    "json_value",
    "positive_int_value",
    "read_relative",
    "section",
    "string_tuple_value",
]
