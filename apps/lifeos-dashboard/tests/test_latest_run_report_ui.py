from pathlib import Path

STATIC_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard" / "static"
TABS_PATH = STATIC_ROOT / "tabs.js"
REPORT_PATH = STATIC_ROOT / "latest-run-report.js"
CSS_PATH = STATIC_ROOT / "latest-run-report.css"


def test_automation_logs_loads_latest_run_report_surface() -> None:
    tabs_source = TABS_PATH.read_text(encoding="utf-8")
    source = REPORT_PATH.read_text(encoding="utf-8")

    assert '/static/latest-run-report.js' in tabs_source
    assert 'id = "automation-latest-run"' in source
    assert "Latest Run Report" in source
    assert "CURRENT OR LATEST WORKER EXECUTION" in source
    assert 'logPanel.insertBefore(root, verificationSummary' in source


def test_latest_run_report_reuses_authoritative_runtime_sources() -> None:
    source = REPORT_PATH.read_text(encoding="utf-8")

    assert 'fetch("/api/command-center"' in source
    assert 'fetch("/api/worker-operations"' in source
    assert "commandCenter.history" in source
    assert "commandCenter.worker_verification" in source
    assert "workerOperations.history" in source
    assert "workerOperations.orchestrator?.events" in source
    assert 'String(event.run_id || "") === runId' in source


def test_latest_run_report_exposes_durable_lifecycle_and_attempt_reasons() -> None:
    source = REPORT_PATH.read_text(encoding="utf-8")

    for field in (
        "dispatch_state",
        "result_state",
        "repair_state",
        "repair_dispatch_state",
        "hq_wake_state",
        "hq_review_state",
        "rob_validation_state",
        "ready_for_consumption",
    ):
        assert field in source

    assert "Durable lifecycle" in source
    assert "Attempt history" in source
    assert "event.detail" in source
    assert "hq_review_reason" in source
    assert "receiver_reason" in source
    assert "failure_reason" in source
    assert "The durable lifecycle above remains authoritative" in source


def test_latest_run_report_filters_existing_logs_instead_of_copying_them() -> None:
    source = REPORT_PATH.read_text(encoding="utf-8")

    assert "Filter full logs to this run" in source
    assert 'document.getElementById("automation-log-filter-search")' in source
    assert 'search.dispatchEvent(new Event("input"' in source
    assert "setInterval" in source


def test_latest_run_report_has_expandable_responsive_timeline_styles() -> None:
    source = CSS_PATH.read_text(encoding="utf-8")

    assert ".automation-latest-run > summary" in source
    assert ".latest-run-facts" in source
    assert ".latest-run-timeline" in source
    assert ".latest-run-stage" in source
    assert '[data-tone="good"]' in source
    assert '[data-tone="warn"]' in source
    assert '[data-tone="bad"]' in source
    assert "@media (max-width: 560px)" in source
