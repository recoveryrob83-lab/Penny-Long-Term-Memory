from fastapi.testclient import TestClient

from lifeos_dashboard.adapters import SampleDashboardSource
from lifeos_dashboard.main import PACKAGE_ROOT, create_app

sample_source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
client = TestClient(create_app(sample_source))


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "version": "0.1.0",
        "mode": "sample",
    }


def test_dashboard_endpoint_returns_eagle_eye_sections() -> None:
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["mode"] == "sample"
    assert payload["flow"]["now"]["title"]
    assert payload["today"]["next_event"]["title"]
    assert payload["notebooks"]
    assert payload["commands"]


def test_department_inspection_endpoint_exposes_contract() -> None:
    response = client.get("/api/department-inspection")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == 1
    assert payload["available"] is False
    assert len(payload["scopes"]) == 8
    assert payload["records"] == []


def test_dashboard_home_renders_interface() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "LifeOS Dashboard" in response.text
    assert "Recent LifeOS activity" in response.text
    assert "DURABLE SYSTEM PULSE" in response.text
    assert "Penny commands" in response.text
    assert "Department Inspection" in response.text
    assert "DURABLE STATE UNDER GLASS" in response.text
    assert "Worker Operations" in response.text
    assert "Courier self-test" in response.text


def test_worker_operations_requires_real_local_repository_mode() -> None:
    response = client.get("/api/worker-operations")

    assert response.status_code == 503
    assert "local LifeOS repository checkout" in response.json()["detail"]


def test_legacy_scheduler_is_dormant_by_default(monkeypatch) -> None:
    monkeypatch.delenv("LIFEOS_LEGACY_SCHEDULER_ENABLED", raising=False)
    application = create_app(sample_source)

    with TestClient(application):
        assert application.state.command_center.scheduler_running is False


def test_command_center_status_exposes_eight_destinations() -> None:
    response = client.get("/api/command-center")

    assert response.status_code == 200
    payload = response.json()
    assert payload["paused"] is False
    assert payload["running"] is False
    assert len(payload["destinations"]) == 8
    assert any(
        item["key"] == "hub" and item["label"] == "LifeOS_HQ"
        for item in payload["destinations"]
    )


def test_command_center_pause_round_trip() -> None:
    pause_response = client.post("/api/command-center/pause", json={"paused": True})

    assert pause_response.status_code == 200
    assert pause_response.json()["paused"] is True

    resume_response = client.post("/api/command-center/pause", json={"paused": False})

    assert resume_response.status_code == 200
    assert resume_response.json()["paused"] is False
