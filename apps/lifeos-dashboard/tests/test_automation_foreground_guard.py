from types import ModuleType

import pytest

from lifeos_dashboard import automation_foreground_guard_runtime as runtime


class AutomationStopped(RuntimeError):
    pass


class FakeWin32Gui:
    def __init__(self) -> None:
        self.foreground = 0

    def GetForegroundWindow(self) -> int:
        return self.foreground


class FakeWindow:
    handle = 42

    def __init__(self, api: FakeWin32Gui, *, allow_focus: bool) -> None:
        self.api = api
        self.allow_focus = allow_focus
        self.focus_attempts = 0

    def is_minimized(self) -> bool:
        return False

    def set_focus(self) -> None:
        self.focus_attempts += 1
        if self.allow_focus:
            self.api.foreground = self.handle


def fake_base(window: FakeWindow, events: list[str]) -> tuple[ModuleType, dict[str, int]]:
    base = ModuleType("open_department_chat_group_test_double")
    base.AutomationStopped = AutomationStopped
    calls = {"window": 0}

    def get_chatgpt_window():
        calls["window"] += 1
        return window

    base.get_chatgpt_window = get_chatgpt_window
    base.focus_group_text_surface = lambda group: events.append(f"focus:{group}")
    base.send_keys = lambda keys, **kwargs: events.append(f"keys:{keys}")
    return base, calls


def test_guard_foregrounds_once_and_reuses_cached_handle_for_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = FakeWin32Gui()
    window = FakeWindow(api, allow_focus=True)
    events: list[str] = []
    base, calls = fake_base(window, events)
    monkeypatch.setattr(runtime, "win32gui", api)

    assert runtime.install_base_guard(base) is True
    base.focus_group_text_surface("composer")
    base.send_keys("^a")
    base.send_keys("^c")
    base.send_keys("^v")

    assert window.focus_attempts == 1
    assert calls["window"] == 1
    assert events == ["focus:composer", "keys:^a", "keys:^c", "keys:^v"]


def test_guard_does_not_refocus_when_chatgpt_is_already_foreground(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = FakeWin32Gui()
    api.foreground = 42
    window = FakeWindow(api, allow_focus=True)
    events: list[str] = []
    base, calls = fake_base(window, events)
    monkeypatch.setattr(runtime, "win32gui", api)

    runtime.install_base_guard(base)
    base.focus_group_text_surface("composer")
    base.send_keys("^v")

    assert window.focus_attempts == 0
    assert calls["window"] == 1
    assert events == ["focus:composer", "keys:^v"]


def test_guard_stops_before_keyboard_input_when_cached_foreground_is_lost(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = FakeWin32Gui()
    api.foreground = 42
    window = FakeWindow(api, allow_focus=True)
    events: list[str] = []
    base, calls = fake_base(window, events)
    monkeypatch.setattr(runtime, "win32gui", api)
    runtime.install_base_guard(base)
    base.focus_group_text_surface("composer")
    api.foreground = 99

    with pytest.raises(AutomationStopped, match="lost foreground focus"):
        base.send_keys("^a")

    assert calls["window"] == 1
    assert events == ["focus:composer"]


def test_guard_stops_before_click_when_foreground_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    api = FakeWin32Gui()
    window = FakeWindow(api, allow_focus=False)
    events: list[str] = []
    base, calls = fake_base(window, events)
    monkeypatch.setattr(runtime, "win32gui", api)
    monkeypatch.setattr(runtime, "FOREGROUND_TIMEOUT_SECONDS", 0.01)
    monkeypatch.setattr(runtime, "FOREGROUND_POLL_SECONDS", 0.001)
    runtime.install_base_guard(base)

    with pytest.raises(AutomationStopped, match="foreground window"):
        base.focus_group_text_surface("composer")

    assert calls["window"] == 1
    assert events == []


def test_foreground_failure_has_specific_dashboard_guidance() -> None:
    message = runtime.explain_failure(
        "",
        "STOPPED: ChatGPT Classic lost foreground focus before keyboard input. No keyboard input was sent.",
        1,
    )

    assert "bring ChatGPT Classic forward" in message
    assert "Nothing was pasted or sent" in message
