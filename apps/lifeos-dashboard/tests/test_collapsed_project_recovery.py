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


def function_node(name: str) -> ast.FunctionDef:
    tree = ast.parse(source())
    return next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name
    )


def function_source(name: str) -> str:
    segment = ast.get_source_segment(source(), function_node(name))
    assert segment is not None
    return segment


def load_function(name: str):
    function = function_node(name)
    module = ast.Module(body=[function], type_ignores=[])
    namespace = {
        "re": re,
        "EXPAND_COLLAPSE_COLLAPSED": 0,
        "EXPAND_COLLAPSE_EXPANDED": 1,
    }
    exec(compile(module, str(SCRIPT_PATH), "exec"), namespace)
    return namespace[name]


def test_verified_automation_source_compiles() -> None:
    compile(source(), str(SCRIPT_PATH), "exec")


def test_collapsed_project_recovery_precedes_show_more_recovery() -> None:
    script = function_source("open_exact_chat_with_bounded_sidebar_expansion")

    project_call = script.index(
        "project_expanded = expand_collapsed_project_once(window, target)"
    )
    exact_wait = script.index("wait_for_exact_sidebar_link(")
    show_more_call = script.index("show_more = find_sidebar_show_more(window)")

    assert project_call < exact_wait < show_more_call
    assert "PROJECT_EXPANSION_TIMEOUT_SECONDS" in script
    assert "return _original_open_exact_chat(window, target)" in script


def test_project_expansion_never_invokes_the_project_row() -> None:
    script = function_source("expand_project_control_once")

    assert "control.invoke()" not in script
    assert "no explicit UIA expansion action was available" in script
    assert "navigate to the wrong chat" in script


def test_project_expansion_requires_exact_target_wait_after_unfolding() -> None:
    script = function_source("expand_collapsed_project_once")

    assert "exact_link.exists(timeout=0.1)" in script
    assert "is_expanded_state(expand_collapse_state(project))" in script
    assert "project_chat_region_visible(" in script
    assert "Exact target link became visible after project expansion." in script


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


def test_expanded_state_recognition_rejects_partial_and_unknown_values() -> None:
    is_expanded_state = load_function("is_expanded_state")

    assert is_expanded_state(1) is True
    assert is_expanded_state("ExpandCollapseState_Expanded") is True
    assert is_expanded_state(0) is False
    assert is_expanded_state("PartiallyExpanded") is False
    assert is_expanded_state(None) is False


def test_project_labels_remain_exact() -> None:
    project_label_matches = load_function("project_label_matches")

    assert project_label_matches("LifeOS", "LifeOS") is True
    assert project_label_matches("LifeOS, project", "LifeOS") is True
    assert project_label_matches("LifeOS, project, collapsed", "LifeOS") is True
    assert project_label_matches("LifeOS Archive", "LifeOS") is False
    assert project_label_matches("Other Project", "LifeOS") is False


def test_composer_state_requires_two_matching_fresh_reads() -> None:
    script = function_source("read_stable_composer_state")

    assert "base.current_document_title(window) != expected_document_title" in script
    assert "fresh_group = base.find_composer_group(window)" in script
    assert "observed = base.normalize_text(base.copy_group_text(fresh_group))" in script
    assert "if previous is not None and observed == previous" in script
    assert "Composer readiness timed out while confirming stable content" in script


def test_place_text_discards_pre_navigation_group_wrapper() -> None:
    script = function_source("place_text_with_stable_clipboard")

    assert "del group" in script
    assert "read_stable_composer_state(window, expected_document_title)" in script
    assert "base.copy_group_text(group)" not in script


def test_paste_reacquires_and_focuses_current_destination_composer() -> None:
    script = function_source("place_text_with_stable_clipboard")

    reacquire = script.index("paste_group = base.find_composer_group(window)")
    focus = script.index("base.focus_group_text_surface(paste_group)")
    paste = script.index('base.send_keys("^v", pause=0.10)')

    assert reacquire < focus < paste
    assert "Active destination changed before paste" in script
