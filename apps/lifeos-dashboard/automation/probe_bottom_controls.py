"""Read-only probe for visible controls near the bottom of ChatGPT Classic.

This script does not click, focus, type, copy, alter, or send anything. It prints
control metadata only so Engineering can identify the current composer control type.
"""

from __future__ import annotations

from open_department_chat import APP_TITLE, get_chatgpt_window


def safe_text(control) -> str:
    try:
        return control.window_text().strip().replace("\n", " ")
    except Exception:
        return ""


def main() -> int:
    print(f"Finding window: {APP_TITLE}")
    window = get_chatgpt_window()
    rect = window.rectangle()
    cutoff = rect.top + int(rect.height() * 0.55)

    rows: list[tuple[int, int, int, int, str, str, str, bool, bool]] = []
    for control in window.descendants():
        try:
            crect = control.rectangle()
            if crect.top < cutoff:
                continue
            if crect.width() <= 0 or crect.height() <= 0:
                continue
            if crect.bottom > rect.bottom or crect.right > rect.right:
                continue
            control_type = control.element_info.control_type or ""
            name = safe_text(control)[:120]
            automation_id = str(control.element_info.automation_id or "")[:120]
            rows.append(
                (
                    crect.top,
                    crect.left,
                    crect.right,
                    crect.bottom,
                    control_type,
                    name,
                    automation_id,
                    bool(control.is_visible()),
                    bool(control.is_enabled()),
                )
            )
        except Exception:
            continue

    rows.sort(key=lambda row: (row[0], row[1]))
    print(f"Visible bottom-region controls: {len(rows)}")
    for top, left, right, bottom, control_type, name, automation_id, visible, enabled in rows:
        print(
            f"{control_type:<16} rect=({left},{top},{right},{bottom}) "
            f"visible={visible} enabled={enabled} name={name!r} automation_id={automation_id!r}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
