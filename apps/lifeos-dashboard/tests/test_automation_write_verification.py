from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from lifeos_dashboard import automation_write_verification_runtime as runtime


PROBE_PATH = (
    Path(__file__).resolve().parents[1]
    / "automation"
    / "probe_composer_group_clipboard.py"
)


class AutomationStopped(RuntimeError):
    pass


class FakeControl:
    def __init__(self, control_type: str, value: str = "", *, visible: bool = True) -> None:
        self.element_info = SimpleNamespace(control_type=control_type)
        self._value = value
        self._visible = visible
        self.iface_value = SimpleNamespace(CurrentValue=value)
        self.iface_text = SimpleNamespace(
            DocumentRange=SimpleNamespace(GetText=lambda _: value)
        )

    def get_value(self) -> str:
        return self._value

    def window_text(self) -> str:
        return self._value

    def is_visible(self) -> bool:
        return self._visible


class FakeGroup(FakeControl):
    def __init__(self, children: list[FakeControl]) -> None:
        super().__init__("Group")
        self._children = children

    def descendants(self) -> list[FakeControl]:
        return self._children


class FakeRect:
    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def width(self) -> int:
        return self.right - self.left

    def height(self) -> int:
        return self.bottom - self.top


class FakeCandidate:
    def __init__(
        self,
        control_type: str,
        rect: FakeRect,
        *,
        visible: bool = True,
        enabled: bool = True,
    ) -> None:
        self.element_info = SimpleNamespace(control_type=control_type)
        self._rect = rect
        self._visible = visible
        self._enabled = enabled

    def rectangle(self) -> FakeRect:
        return self._rect

    def is_visible(self) -> bool:
        return self._visible

    def is_enabled(self) -> bool:
        return self._enabled


class FakeAnchorLookup:
    def __init__(self, rect: FakeRect) -> None:
        self._wrapper = FakeCandidate("Button", rect)

    def exists(self, timeout: float) -> bool:
        return True

    def wrapper_object(self) -> FakeCandidate:
        return self._wrapper


class FakeWindow:
    def __init__(self, anchor_rect: FakeRect, candidates: list[FakeCandidate]) -> None:
        self._anchor = FakeAnchorLookup(anchor_rect)
        self._candidates = candidates

    def child_window(self, **kwargs):
        assert kwargs == {"auto_id": "composer-plus-btn", "control_type": "Button"}
        return self._anchor

    def descendants(self) -> list[FakeCandidate]:
        return self._candidates


def fake_base(group: FakeGroup, clipboard_values: list[str]) -> tuple[ModuleType, dict[str, int]]:
    base = ModuleType("open_department_chat_group_test_double")
    base.AutomationStopped = AutomationStopped
    base.POLL_SECONDS = 0.001
    base.current_document_title = lambda window: "LifeOS - Engineering_HQ"
    base.find_composer_group = lambda window: group
    base.normalize_text = lambda value: " ".join(str(value).split())
    base.text_matches_expected = lambda observed, expected: base.normalize_text(observed) == base.normalize_text(expected)
    calls = {"clipboard": 0}

    def copy_group_text(_group):
        calls["clipboard"] += 1
        return clipboard_values.pop(0) if clipboard_values else ""

    base.copy_group_text = copy_group_text
    return base, calls


def selector_base() -> ModuleType:
    base = ModuleType("open_department_chat_group_selector_test_double")
    base.AutomationStopped = AutomationStopped
    return base


def test_accessible_composer_text_verifies_without_clipboard_copy() -> None:
    expected = "Complete canonical prompt"
    group = FakeGroup([FakeControl("Edit", expected)])
    base, calls = fake_base(group, [""])

    assert runtime.install_base_write_verification(base) is True
    result = base.wait_for_written_text(
        object(),
        expected_document_title="LifeOS - Engineering_HQ",
        expected_text=expected,
        timeout_seconds=0.02,
    )

    assert result is group
    assert calls["clipboard"] == 0


def test_clipboard_remains_fallback_when_uia_value_is_empty() -> None:
    expected = "Complete canonical prompt"
    group = FakeGroup([FakeControl("Edit", "")])
    base, calls = fake_base(group, [expected])

    runtime.install_base_write_verification(base)
    result = base.wait_for_written_text(
        object(),
        expected_document_title="LifeOS - Engineering_HQ",
        expected_text=expected,
        timeout_seconds=0.02,
    )

    assert result is group
    assert calls["clipboard"] == 1


def test_unrelated_visible_text_cannot_verify_the_draft() -> None:
    group = FakeGroup([
        FakeControl("Button", "Complete canonical prompt"),
        FakeControl("Edit", "Different text"),
    ])
    base, _ = fake_base(group, ["Still different"])

    runtime.install_base_write_verification(base)
    with pytest.raises(AutomationStopped, match="longest accessible composer value"):
        base.wait_for_written_text(
            object(),
            expected_document_title="LifeOS - Engineering_HQ",
            expected_text="Complete canonical prompt",
            timeout_seconds=0.005,
        )


def test_write_verification_install_is_idempotent() -> None:
    group = FakeGroup([FakeControl("Edit", "Prompt")])
    base, _ = fake_base(group, [])

    assert runtime.install_base_write_verification(base) is True
    assert runtime.install_base_write_verification(base) is False


def test_strict_selector_rejects_partial_overlap_and_returns_smallest_full_container() -> None:
    anchor = FakeRect(10, 10, 20, 20)
    partial_overlap = FakeCandidate("Group", FakeRect(0, 0, 10, 10))
    smallest_full_container = FakeCandidate("Group", FakeRect(0, 0, 30, 30))
    larger_full_container = FakeCandidate("Group", FakeRect(-10, -10, 40, 40))
    window = FakeWindow(
        anchor,
        [partial_overlap, larger_full_container, smallest_full_container],
    )

    selected = runtime.strict_composer_group(selector_base(), window)

    assert selected is smallest_full_container


def test_strict_selector_refuses_when_no_group_contains_the_full_anchor() -> None:
    anchor = FakeRect(10, 10, 20, 20)
    partial_overlap = FakeCandidate("Group", FakeRect(0, 0, 10, 10))
    window = FakeWindow(anchor, [partial_overlap])

    with pytest.raises(AutomationStopped, match="fully enclosing"):
        runtime.strict_composer_group(selector_base(), window)


def test_composer_selector_install_is_idempotent() -> None:
    anchor = FakeRect(10, 10, 20, 20)
    expected = FakeCandidate("Group", FakeRect(0, 0, 30, 30))
    window = FakeWindow(anchor, [expected])
    base = selector_base()
    base.find_composer_group = lambda window: None

    assert runtime.install_base_composer_group_selector(base) is True
    assert base.find_composer_group(window) is expected
    assert runtime.install_base_composer_group_selector(base) is False


def test_read_only_probe_reuses_the_installed_production_selector() -> None:
    probe_source = PROBE_PATH.read_text(encoding="utf-8")

    assert "import open_department_chat_group as production_group" in probe_source
    assert "automation_write_verification_runtime" in probe_source
    assert "return production_group.find_composer_group(window)" in probe_source
    assert "rect.left <= anchor_rect.left" not in probe_source
