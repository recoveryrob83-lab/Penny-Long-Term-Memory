from lifeos_dashboard import command_center_failure_precision_runtime as runtime


def test_foreground_failure_is_not_misreported_as_unavailable() -> None:
    message = runtime.explain_failure(
        "",
        "STOPPED: ChatGPT Classic could not become the foreground window. No keyboard input was sent.",
        1,
    )

    assert "retain foreground focus" in message
    assert "Nothing was pasted or sent" in message
    assert "Open the desktop app" not in message


def test_exact_missing_window_still_reports_unavailable() -> None:
    message = runtime.explain_failure(
        "",
        "STOPPED: ChatGPT window not found: 'ChatGPT Classic'",
        1,
    )

    assert "was not available" in message
    assert "Open the desktop app" in message
