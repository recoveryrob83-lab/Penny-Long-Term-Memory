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


def test_structured_write_failure_reports_possible_existing_draft() -> None:
    stdout = "1. Finding window: ChatGPT Classic\n5. Applying draft policy"
    stderr = (
        "STOPPED: Composer write verification timed out. Expected 341 normalized characters, "
        "last clipboard copy had 0, and the longest accessible composer value had 0. Nothing was sent.\n"
        "LIFEOS_RESULT_CODE=write_verification_failed"
    )

    reason = explain_failure(stdout, stderr, 1)

    assert "post-paste verification" in reason
    assert "draft may be present" in reason
    assert "Leave the composer untouched" in reason
    assert "Expected 341 normalized characters" in reason
    assert "Open the desktop app" not in reason


def test_structured_timeout_after_copy_reports_verification_stage() -> None:
    stdout = (
        "LIFEOS_STAGE=keyboard_paste_start\n"
        "LIFEOS_STAGE=keyboard_select_all_start\n"
        "LIFEOS_STAGE=keyboard_copy_start\n"
    )
    stderr = "LIFEOS_RESULT_CODE=timeout"

    reason = explain_failure(stdout, stderr, 1)

    assert "post-paste verification" in reason
    assert "draft may be present" in reason
    assert "Open Automation Logs" in reason
    assert "modal window" not in reason


def test_structured_readiness_timeout_is_not_mislabeled_as_write_failure() -> None:
    stdout = "Composer readiness timed out after 20.0s. Last state: composer geometry is still settling."
    stderr = "LIFEOS_RESULT_CODE=timeout"

    reason = explain_failure(stdout, stderr, 1)

    assert "composer never became stably ready" in reason
    assert "Nothing was pasted or sent" in reason


def test_unknown_failure_stays_safe() -> None:
    reason = explain_failure("", "Something entirely new", 7)
    assert "stopped safely" in reason
    assert "exit code 7" in reason
