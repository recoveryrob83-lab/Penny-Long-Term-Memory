import ast
import re
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "automation"
    / "open_department_chat_group_verified.py"
)


def source() -> str:
    return SCRIPT_PATH.read_text(encoding="utf-8")


def load_function(name: str):
    tree = ast.parse(source())
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name
    )
    module = ast.Module(body=[function], type_ignores=[])
    namespace = {"re": re, "EXPAND_COLLAPSE_COLLAPSED": 0}
    exec(compile(module, str(SCRIPT_PATH), "exec"), namespace)
    return namespace[name]


def test_verified_automation_source_compiles() -> None:
    compile(source(), str(SCRIPT_PATH), "exec")


def test_collapsed_project_recovery_precedes_show_more_recovery() -> None:
    script = source()

    project_call = script.index("expand_collapsed_project_once(window, target)")
    show_more_call = script.index("show_more = find_sidebar_show_more(window)")

    assert project_call < show_more_call
    assert "project_chat_region_visible(window, target.project_title)" in script
    assert "Expanding {target.project_title!r} once" in script
    assert "Collapsed project expansion did not expose" in script


def test_project_detection_requires_exact_label_and_collapsed_state() -> None:
    script = source()

    assert "project_label_matches(control.window_text(), project_title)" in script
    assert "is_collapsed_state(expand_collapse_state(control))" in script
    assert "rect.left > right_limit" in script


def test_collapsed_state_recognition_rejects_partial_and_unknown_values() -> None:
    is_collapsed_state = load_function("is_collapsed_state")

    assert is_collapsed_state(0) is True
    assert is_collapsed_state("ExpandCollapseState_Collapsed") is True
    assert is_collapsed_state(1) is False
    assert is_collapsed_state("PartiallyExpanded") is False
    assert is_collapsed_state(None) is False


def test_project_labels_remain_exact() -> None:
    project_label_matches = load_function("project_label_matches")

    assert project_label_matches("Life OS", "Life OS") is True
    assert project_label_matches("Life OS, project", "Life OS") is True
    assert project_label_matches("Life OS, project, collapsed", "Life OS") is True
    assert project_label_matches("Life OS Archive", "Life OS") is False
    assert project_label_matches("Other Project", "Life OS") is False
