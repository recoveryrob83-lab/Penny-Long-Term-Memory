from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "lifeos_dashboard"
STATIC_ROOT = PACKAGE_ROOT / "static"
TEMPLATE_ROOT = PACKAGE_ROOT / "templates"


def test_server_guard_loads_before_dashboard_clients() -> None:
    template = (TEMPLATE_ROOT / "index.html").read_text(encoding="utf-8")

    guard_index = template.index("server-availability.js")
    assert guard_index < template.index("app.js")
    assert guard_index < template.index("worker-operations.js")
    assert guard_index < template.index("department-inspection.js")


def test_server_guard_wraps_fetch_and_surfaces_actionable_message() -> None:
    script = (STATIC_ROOT / "server-availability.js").read_text(encoding="utf-8")

    assert "window.fetch = async" in script
    assert "LifeOSServerUnavailableError" in script
    assert "Dashboard server is unavailable. Restart the server, then reload this page." in script
    assert 'setText("wo-status", "Server offline")' in script
    assert 'setText("wo-browser-state", "Unavailable")' in script
    assert 'setText("wo-run-state", SERVER_UNAVAILABLE_MESSAGE)' in script
    assert 'toast.classList.add("visible")' in script
