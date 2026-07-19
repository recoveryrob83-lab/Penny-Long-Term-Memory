from pathlib import Path


STATIC_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard" / "static"
TABS_PATH = STATIC_ROOT / "tabs.js"
LOGS_PATH = STATIC_ROOT / "automation-logs.js"
CSS_PATH = STATIC_ROOT / "automation-logs.css"


def test_tabs_create_a_dedicated_automation_logs_surface() -> None:
    source = TABS_PATH.read_text(encoding="utf-8")

    assert 'data-tab-target="automation-logs"' in source
    assert 'data-tab-panel="automation-logs"' in source
    assert "Automation Logs" in source
    assert "/static/automation-logs.js" in source
    assert "/static/automation-logs.css" in source
    assert "Prompt bodies and environment secrets are not copied" in source


def test_logs_ui_exposes_complete_stdout_stderr_and_copyable_run_record() -> None:
    source = LOGS_PATH.read_text(encoding="utf-8")

    assert 'fetch("/api/command-center"' in source
    assert "Complete stdout" in source
    assert "Complete stderr" in source
    assert "Copy complete run log" in source
    assert "LIFEOS_RUN_CONTEXT=" in source
    assert "LIFEOS_BACKEND=" in source
    assert "setInterval" in source


def test_logs_ui_has_filters_and_readable_stream_layout() -> None:
    tabs_source = TABS_PATH.read_text(encoding="utf-8")
    css_source = CSS_PATH.read_text(encoding="utf-8")

    for element_id in (
        "automation-log-filter-result",
        "automation-log-filter-destination",
        "automation-log-filter-trigger",
        "automation-log-filter-sort",
        "automation-log-filter-search",
        "automation-log-refresh",
        "automation-log-expand",
    ):
        assert element_id in tabs_source

    assert ".automation-log-stream pre" in css_source
    assert "max-height: 32rem" in css_source
    assert "white-space: pre-wrap" in css_source


def test_logs_ui_preserves_open_details_and_avoids_unchanged_rerenders() -> None:
    source = LOGS_PATH.read_text(encoding="utf-8")

    assert "function captureDetailState()" in source
    assert 'details[data-detail-key]' in source
    assert "function detailOpen(" in source
    assert "historySignature" in source
    assert "const changed = nextSignature !== historySignature" in source
    assert "if (changed || showLoading) render();" in source
