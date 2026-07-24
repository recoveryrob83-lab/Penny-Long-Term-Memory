from fastapi.testclient import TestClient

from lifeos_dashboard.adapters import SampleDashboardSource
from lifeos_dashboard.main import PACKAGE_ROOT, create_app


sample_source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
client = TestClient(create_app(sample_source))


def test_dashboard_renders_browser_bridge_reconnect_control() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'id="wo-reconnect-browser"' in response.text
    assert "Reconnect bridge" in response.text
    assert "browser-bridge.js" in response.text
    assert "browser-bridge.css" in response.text


def test_browser_bridge_reconnect_requires_local_repository_mode() -> None:
    response = client.post(
        "/api/worker-operations/browser/reconnect",
        json={"confirm_launch": True, "timeout_seconds": 20},
    )

    assert response.status_code == 503
    assert "local LifeOS repository checkout" in response.json()["detail"]
