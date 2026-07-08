"""Prompt Launcher v0.1 learning project.

A small desktop utility for loading a JSON prompt library, displaying prompt
buttons, and copying selected prompt text to the clipboard.

This file is intentionally a placeholder for Engineering Classroom work.
It is not part of Life OS production automation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROMPT_LIBRARY_PATH = Path(__file__).with_name("prompt_library.json")


def load_prompt_library(path: Path = PROMPT_LIBRARY_PATH) -> dict[str, Any]:
    """Load the prompt library JSON file.

    v0.1 classroom goal:
    - Read prompt_library.json.
    - Return parsed JSON data.
    - Later: validate schema and feed data into a simple desktop UI.
    """
    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)

    return data


def main() -> None:
    """Placeholder entrypoint for Rob to build in Engineering Classroom."""
    prompt_library = load_prompt_library()
    prompts = prompt_library.get("prompts", [])

    print("Prompt Launcher v0.1 placeholder")
    print(f"Loaded {len(prompts)} prompt(s) from {PROMPT_LIBRARY_PATH.name}.")
    print("Next classroom step: add a simple desktop UI and clipboard copy behavior.")


if __name__ == "__main__":
    main()
