from pathlib import Path


PACKAGE = Path(__file__).parents[1] / "lifeos_dashboard"
TEMPLATE = PACKAGE / "templates" / "index.html"
SCRIPT = PACKAGE / "static" / "worker-operations.js"
STYLE = PACKAGE / "static" / "worker-operations.css"


def test_worker_operations_replaces_legacy_automation_surface() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")

    assert "Worker Operations" in html
    assert 'id="wo-advisory-select"' in html
    assert 'id="wo-run"' in html
    assert 'id="wo-reviews"' in html
    assert 'id="wo-self-test"' in html
    assert 'id="wo-history"' in html
    assert "worker-operations.js" in html
    assert "worker-operations.css" in html
    assert 'id="cc-custom-prompt"' not in html
    assert 'id="cc-save-schedule"' not in html
    assert "command-center.js" not in html
    assert "command-scheduler.js" not in html


def test_worker_operations_assets_expose_bounded_controls() -> None:
    script = SCRIPT.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")

    assert "/api/worker-operations/run" in script
    assert "/api/worker-operations/review" in script
    assert "/api/worker-operations/self-test" in script
    assert "/api/command-center/pause" in script
    assert "confirm_send: true" in script
    assert "Receiver:" in script
    assert "Courier self-test succeeded." in script
    assert "No durable authority was created." in script
    assert ".worker-ops-layout" in style
    assert ".worker-history-item" in style
