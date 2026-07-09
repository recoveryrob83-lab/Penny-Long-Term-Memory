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

import tkinter as tk


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

class Prompt:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.title: str = data["title"]
        self.category: str = data["category"]
        self.mode: str = data["mode"]
        self.text: str = data["text"]

def copy_prompt(root: tk.Tk, prompt: Prompt) -> None:
    root.clipboard_clear()
    root.clipboard_append(prompt.text)
    root.update()

    print(f"Copied: {prompt.title}")

def button_clicked(title: str) -> None:
    print(f"You clicked: {title}")

def main() -> None:
    prompt_library = load_prompt_library()
    prompts = prompt_library.get("prompts", [])

    root = tk.Tk()
    root.title("Prompt Launcher")
    root.geometry("400x300")
    root.resizable(False, False)
    header = tk.Label(root, text="Prompt Launcher", font=("Segoe UI", 16, "bold")
)

    header.pack(pady=10)
    for prompt_data in prompts:
        prompt = Prompt(prompt_data)
        print(prompt.title)
        button = tk.Button(
        root,
        text=prompt.title,
        command=lambda p=prompt: copy_prompt(root, p),
    )
        button.pack()
    

    

    root.mainloop()
if __name__ == "__main__":
    main()
