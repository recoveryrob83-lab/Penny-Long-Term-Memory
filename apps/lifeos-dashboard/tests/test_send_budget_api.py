from pathlib import Path

from fastapi.testclient import TestClient

from lifeos_dashboard.adapters import SampleDashboardSource
from lifeos_dashboard.main import PACKAGE_ROOT, create_app


def _client(tmp_path: Path, monkeypatch) -> TestClient:
    monkeypatch.setenv(
        "COMMAND_CENTER_DATABASE_PATH",
        str(tmp_path / "command-center.sqlite3"),
    )
    monkeypatch.setenv("LIFEOS_GLOBAL_SEND_BUDGET_LIMIT", "2")
    source = SampleDashboardSource(PACKAGE_ROOT / "data" / "sample_dashboard.json")
    return TestClient(create_app(source))


def test_command_center_status_exposes_send_budget(tmp_path: Path, monkeypatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        response = client.get("/api/command-center")

    assert response.status_code == 200
    budget = response.json()["send_budget"]
    assert budget["limit"] == 2
    assert budget["used"] == 0
    assert budget["remaining"] == 2
    assert budget["held_operations"] == {"count": 0, "last": None}


def test_send_budget_reset_requires_pause_and_confirmation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    with _client(tmp_path, monkeypatch) as client:
        unpaused = client.post(
            "/api/command-center/send-budget/reset",
            json={"confirm_reset": True},
        )
        client.post("/api/command-center/pause", json={"paused": True})
        unconfirmed = client.post(
            "/api/command-center/send-budget/reset",
            json={"confirm_reset": False},
        )
        reset = client.post(
            "/api/command-center/send-budget/reset",
            json={"confirm_reset": True},
        )

    assert unpaused.status_code == 400
    assert "Pause automation" in unpaused.json()["detail"]
    assert unconfirmed.status_code == 400
    assert "explicit confirmation" in unconfirmed.json()["detail"]
    assert reset.status_code == 200
    assert reset.json()["paused"] is True
    assert reset.json()["send_budget"]["epoch"] == 2
    assert reset.json()["send_budget"]["used"] == 0


def test_worker_operations_home_exposes_send_budget_controls(
    tmp_path: Path,
    monkeypatch,
) -> None:
    with _client(tmp_path, monkeypatch) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Send budget" in response.text
    assert 'id="wo-budget-state"' in response.text
    assert 'id="wo-reset-budget"' in response.text
