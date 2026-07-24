from pathlib import Path


PACKAGE = Path(__file__).parents[1] / "lifeos_dashboard"
TEMPLATE = PACKAGE / "templates" / "index.html"
SCRIPT = PACKAGE / "static" / "worker-route-management.js"
STYLE = PACKAGE / "static" / "worker-route-management.css"
MAIN = PACKAGE / "main.py"


def test_route_management_surface_is_present() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")

    assert 'id="wo-route-management"' in html
    assert 'id="wo-route-worker"' in html
    assert 'id="wo-confirm-route-capture"' in html
    assert 'id="wo-capture-route"' in html
    assert "worker-route-management.js" in html
    assert "worker-route-management.css" in html
    assert "keep exactly one replacement Worker conversation open" in html


def test_route_management_ui_requires_pause_confirmation_and_revision() -> None:
    script = SCRIPT.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")

    assert "/api/worker-operations/routes/capture" in script
    assert "expected_route_revision" in script
    assert "confirm_capture: true" in script
    assert "!paused" in script
    assert "Capture active chat as route" in script
    assert "zero-authority courier test" in script
    assert ".worker-route-panel" in style
    assert '.worker-route-message[data-tone="bad"]' in style


def test_route_capture_api_is_bounded_to_worker_operations() -> None:
    source = MAIN.read_text(encoding="utf-8")

    assert 'class WorkerRouteCaptureRequest(BaseModel):' in source
    assert '@application.post("/api/worker-operations/routes/capture")' in source
    assert "worker_operations.routes.capture_active_route" in source
    assert "expected_route_revision=request.expected_route_revision" in source
    assert "confirm_capture=request.confirm_capture" in source
