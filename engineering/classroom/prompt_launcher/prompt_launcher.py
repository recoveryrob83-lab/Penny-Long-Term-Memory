"""Local LifeOS prompt launcher.

Loads an editable JSON prompt library, builds department-aware prompts, and
copies the result to the clipboard. It uses only Python's standard library.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox
from typing import Any

import tkinter as tk
from tkinter import ttk


PROMPT_LIBRARY_PATH = Path(__file__).with_name("prompt_library.json")


@dataclass(frozen=True)
class Department:
    """A department that can be inserted into a department-aware prompt."""

    id: str
    label: str
    project_folder: str
    report_name: str
    boot_files: tuple[str, ...]


@dataclass(frozen=True)
class PromptDefinition:
    """A prompt template loaded from the JSON library."""

    id: str
    title: str
    category: str
    description: str
    mode: str
    template: str
    department_label: str = "Department"


@dataclass(frozen=True)
class PromptLibrary:
    """Validated local prompt library."""

    repository: str
    departments: tuple[Department, ...]
    prompts: tuple[PromptDefinition, ...]


def _required_text(record: dict[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must include a non-empty '{key}' value.")
    return value.strip()


def load_prompt_library(path: Path = PROMPT_LIBRARY_PATH) -> PromptLibrary:
    """Load and validate the editable JSON prompt library."""
    try:
        with path.open("r", encoding="utf-8") as source:
            raw = json.load(source)
    except FileNotFoundError as error:
        raise ValueError(f"Prompt library not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Prompt library JSON is invalid on line {error.lineno}: {error.msg}"
        ) from error

    if not isinstance(raw, dict):
        raise ValueError("Prompt library must contain a JSON object.")

    repository = _required_text(raw, "repository", "Prompt library")
    raw_departments = raw.get("departments")
    raw_prompts = raw.get("prompts")
    if not isinstance(raw_departments, list) or not raw_departments:
        raise ValueError("Prompt library must include at least one department.")
    if not isinstance(raw_prompts, list) or not raw_prompts:
        raise ValueError("Prompt library must include at least one prompt.")

    departments: list[Department] = []
    seen_department_ids: set[str] = set()
    for item in raw_departments:
        if not isinstance(item, dict):
            raise ValueError("Each department must be a JSON object.")
        raw_boot_files = item.get("boot_files")
        if not isinstance(raw_boot_files, list) or not raw_boot_files:
            raise ValueError("Department must include at least one boot file.")
        if not all(isinstance(name, str) and name.strip() for name in raw_boot_files):
            raise ValueError("Department boot files must be non-empty strings.")
        department = Department(
            id=_required_text(item, "id", "Department"),
            label=_required_text(item, "label", "Department"),
            project_folder=_required_text(item, "project_folder", "Department"),
            report_name=_required_text(item, "report_name", "Department"),
            boot_files=tuple(name.strip() for name in raw_boot_files),
        )
        if department.id in seen_department_ids:
            raise ValueError(f"Duplicate department id: {department.id}")
        seen_department_ids.add(department.id)
        departments.append(department)

    prompts: list[PromptDefinition] = []
    seen_prompt_ids: set[str] = set()
    valid_modes = {"simple", "department", "full_boot"}
    for item in raw_prompts:
        if not isinstance(item, dict):
            raise ValueError("Each prompt must be a JSON object.")
        prompt = PromptDefinition(
            id=_required_text(item, "id", "Prompt"),
            title=_required_text(item, "title", "Prompt"),
            category=_required_text(item, "category", "Prompt"),
            description=_required_text(item, "description", "Prompt"),
            mode=_required_text(item, "mode", "Prompt"),
            template=_required_text(item, "template", "Prompt"),
            department_label=str(item.get("department_label", "Department")).strip()
            or "Department",
        )
        if prompt.id in seen_prompt_ids:
            raise ValueError(f"Duplicate prompt id: {prompt.id}")
        if prompt.mode not in valid_modes:
            raise ValueError(
                f"Prompt '{prompt.id}' has unsupported mode '{prompt.mode}'."
            )
        seen_prompt_ids.add(prompt.id)
        prompts.append(prompt)

    return PromptLibrary(repository, tuple(departments), tuple(prompts))


def build_prompt(
    library: PromptLibrary,
    prompt: PromptDefinition,
    department: Department | None,
    custom_instructions: str,
) -> str:
    """Render one prompt using the selected department and optional instructions."""
    if prompt.mode in {"department", "full_boot"} and department is None:
        raise ValueError(f"'{prompt.title}' requires a department selection.")

    custom_text = custom_instructions.strip()
    custom_block = (
        f"\nAdditional instructions:\n{custom_text}\n" if custom_text else ""
    )
    values = {
        "repository": library.repository,
        "department": department.label if department else "",
        "project_folder": department.project_folder if department else "",
        "project_boot_files": (
            "\n".join(
                f"- {department.project_folder}/{name}" for name in department.boot_files
            )
            if department
            else ""
        ),
        "report_name": department.report_name if department else "",
        "custom_block": custom_block,
    }
    try:
        rendered = prompt.template.format(**values)
    except KeyError as error:
        raise ValueError(
            f"Prompt '{prompt.title}' uses an unknown template field: {error.args[0]}"
        ) from error

    return rendered.rstrip() + "\n"


class PromptLauncherApp:
    """Tkinter interface for selecting, previewing, and copying prompts."""

    def __init__(self, root: tk.Tk, library: PromptLibrary) -> None:
        self.root = root
        self.library = library
        self.prompts_by_title = {prompt.title: prompt for prompt in library.prompts}
        self.departments_by_label = {
            department.label: department for department in library.departments
        }

        self.prompt_choice = tk.StringVar(value=library.prompts[0].title)
        self.department_choice = tk.StringVar(value=library.departments[0].label)
        self.status_text = tk.StringVar(value="Ready. Choose a command, then copy it.")

        self.root.title("LifeOS Prompt Launcher")
        self.root.geometry("920x680")
        self.root.minsize(760, 560)
        self._build_layout()
        self._refresh_preview()

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(
            container,
            text="LifeOS Prompt Launcher",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(
            container,
            text="Select a command, add anything specific, then copy the ready-to-paste prompt.",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 14))

        ttk.Label(container, text="Command").grid(row=2, column=0, sticky="w")
        command_box = ttk.Combobox(
            container,
            textvariable=self.prompt_choice,
            values=list(self.prompts_by_title),
            state="readonly",
        )
        command_box.grid(row=2, column=1, sticky="ew", padx=(12, 0))
        command_box.bind("<<ComboboxSelected>>", lambda _event: self._refresh_preview())

        self.department_label = ttk.Label(container, text="Department")
        self.department_label.grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.department_box = ttk.Combobox(
            container,
            textvariable=self.department_choice,
            values=list(self.departments_by_label),
            state="readonly",
        )
        self.department_box.grid(row=3, column=1, sticky="ew", padx=(12, 0), pady=(10, 0))
        self.department_box.bind("<<ComboboxSelected>>", lambda _event: self._refresh_preview())

        ttk.Label(container, text="Custom instructions (optional)").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(14, 3)
        )
        self.custom_text = tk.Text(container, height=5, wrap="word")
        self.custom_text.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.custom_text.bind("<KeyRelease>", lambda _event: self._refresh_preview())

        ttk.Label(container, text="Prompt preview").grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(14, 3)
        )
        self.preview = tk.Text(container, height=12, wrap="word", state="disabled")
        self.preview.grid(row=7, column=0, columnspan=2, sticky="nsew")
        container.rowconfigure(7, weight=2)

        buttons = ttk.Frame(container)
        buttons.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Button(buttons, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(
            side="left"
        )
        ttk.Button(buttons, text="Refresh Preview", command=self._refresh_preview).pack(
            side="left", padx=(8, 0)
        )
        ttk.Label(buttons, textvariable=self.status_text).pack(side="right")

    def _selected_prompt(self) -> PromptDefinition:
        return self.prompts_by_title[self.prompt_choice.get()]

    def _selected_department(self) -> Department | None:
        prompt = self._selected_prompt()
        if prompt.mode == "simple":
            return None
        return self.departments_by_label[self.department_choice.get()]

    def _build_current_prompt(self) -> str:
        return build_prompt(
            self.library,
            self._selected_prompt(),
            self._selected_department(),
            self.custom_text.get("1.0", "end-1c"),
        )

    def _refresh_preview(self) -> None:
        prompt = self._selected_prompt()
        requires_department = prompt.mode != "simple"
        self.department_label.configure(text=prompt.department_label)
        self.department_box.configure(state="readonly" if requires_department else "disabled")

        try:
            rendered = self._build_current_prompt()
            self.status_text.set(prompt.description)
        except ValueError as error:
            rendered = ""
            self.status_text.set(str(error))

        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", rendered)
        self.preview.configure(state="disabled")

    def copy_to_clipboard(self) -> None:
        try:
            rendered = self._build_current_prompt()
        except ValueError as error:
            messagebox.showerror("Prompt Launcher", str(error), parent=self.root)
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(rendered)
        self.root.update_idletasks()
        self.status_text.set(f"Copied: {self._selected_prompt().title}")


def main() -> None:
    root = tk.Tk()
    try:
        library = load_prompt_library()
    except ValueError as error:
        root.withdraw()
        messagebox.showerror("LifeOS Prompt Launcher", str(error), parent=root)
        root.destroy()
        raise SystemExit(1) from error

    PromptLauncherApp(root, library)
    root.mainloop()


if __name__ == "__main__":
    main()
