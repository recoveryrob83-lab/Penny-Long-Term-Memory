from types import ModuleType, SimpleNamespace

import pytest

from lifeos_dashboard import automation_write_verification_runtime as runtime


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


def fake_base(group: FakeGroup, clipboard_values: list[str]) -> tuple[ModuleType, dict[str, int]]:
    base = ModuleType("open_department_chat_group_test_double")
    base.AutomationStopped = AutomationStopped
    base.POLL_SECONDS = 0.001
    base.current_document_title = lambda window: "Life OS - Engineering HQ"
    base.find_composer_group = lambda window: group
    base.normalize_text = lambda value: " ".join(str(value).split())
    base.text_matches_expected = lambda observed, expected: base.normalize_text(observed) == base.normalize_text(expected)
    calls = {"clipboard": 0}

    def copy_group_text(_group):
        calls["clipboard"] += 1
        return clipboard_values.pop(0) if clipboard_values else ""

    base.copy_group_text = copy_group_text
    return base, calls


def test_accessible_composer_text_verifies_without_clipboard_copy() -> None:
    expected = "Complete canonical prompt"
    group = FakeGroup([FakeControl("Edit", expected)])
    base, calls = fake_base(group, [""])

    assert runtime.install_base_write_verification(base) is True
    result = base.wait_for_written_text(
        object(),
        expected_document_title="Life OS - Engineering HQ",
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
        expected_document_title="Life OS - Engineering HQ",
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
            expected_document_title="Life OS - Engineering HQ",
            expected_text="Complete canonical prompt",
            timeout_seconds=0.005,
        )


def test_write_verification_install_is_idempotent() -> None:
    group = FakeGroup([FakeControl("Edit", "Prompt")])
    base, _ = fake_base(group, [])

    assert runtime.install_base_write_verification(base) is True
    assert runtime.install_base_write_verification(base) is False
