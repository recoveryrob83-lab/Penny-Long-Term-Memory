from fastapi.testclient import TestClient

from lifeos_dashboard.main import create_app

client = TestClient(create_app())


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


def test_dashboard_home_renders_interface() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "LifeOS Dashboard" in response.text
    assert "Recent LifeOS activity" in response.text
    assert "Penny commands" in response.text
