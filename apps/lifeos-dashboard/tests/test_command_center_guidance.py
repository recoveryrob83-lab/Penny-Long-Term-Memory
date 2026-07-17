from lifeos_dashboard.command_center import explain_failure


def test_explains_occupied_composer() -> None:
    reason = explain_failure("", "STOPPED: composer contains existing text", 2)
    assert "Clear or save that draft" in reason


def test_explains_missing_chatgpt_window() -> None:
    reason = explain_failure("", "ChatGPT Classic window not found", 2)
    assert "Open the desktop app" in reason


def test_explains_exact_chat_failure() -> None:
    reason = explain_failure("", "Exact chat link not found", 2)
    assert "Open the sidebar" in reason


def test_unknown_failure_stays_safe() -> None:
    reason = explain_failure("", "Something entirely new", 7)
    assert "stopped safely" in reason
    assert "exit code 7" in reason
