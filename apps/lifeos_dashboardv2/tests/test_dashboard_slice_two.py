from pathlib import Path

from fastapi.testclient import TestClient

from lifeos_v2.api import create_app


def source(root: Path) -> None:
    (root / "coordination/boards").mkdir(parents=True)
    (root / "coordination/ADVISORY_INDEX.md").write_text("# Index\n", encoding="utf-8")
    (root / "projects/engineering/notebook").mkdir(parents=True)
    (root / "projects/engineering/status.md").write_text("# Active\n", encoding="utf-8")
    (root / "projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md").write_text("# Design\n", encoding="utf-8")
    (root / "memory").mkdir()
    (root / "memory/STARTUP_BOOT.md").write_text("# Boot\n", encoding="utf-8")


def client(tmp_path: Path) -> TestClient:
    source(tmp_path)
    return TestClient(create_app(tmp_path, tmp_path / "runtime.json"))


def test_dashboard_shell_has_only_the_three_v2_tabs_and_read_models(tmp_path: Path) -> None:
    app = client(tmp_path)
    body = app.get("/").text
    assert all(label in body for label in ("Overview", "Department Inspector", "Automation"))
    assert "Worker Operations" not in body and "Automation Logs" not in body
    assert app.get("/dashboard/overview").status_code == 200
    assert app.get("/dashboard/inspector").json()["records"]


def test_dashboard_models_keep_partial_errors_and_inspector_is_bounded(tmp_path: Path) -> None:
    app = client(tmp_path)
    overview = app.get("/dashboard/overview").json()
    assert any(item["state"] == "unavailable" for item in overview["sources"])
    records = app.get("/dashboard/inspector").json()["records"]
    assert {record["source_path"] for record in records} == {
        "projects/engineering/status.md", "projects/engineering/notebook/NOTE-20260729-015-lifeos-v2-final-design.md", "coordination/ADVISORY_INDEX.md", "memory/STARTUP_BOOT.md"
    }


def test_automation_pause_resume_and_static_accessibility_contract() -> None:
    root = Path(__file__).parents[1]
    js = (root / "lifeos_v2/dashboard/dashboard.js").read_text(encoding="utf-8")
    css = (root / "lifeos_v2/dashboard/dashboard.css").read_text(encoding="utf-8")
    assert 'localStorage.setItem("lifeos-v2-tab"' in js and "ArrowRight" in js
    assert "/system/pause" in js and "/system/resume" in js
    assert "UNCERTAIN" in js and "cannot be replayed" in js
    assert "@media(max-width:1050px)" in css and "@media(max-width:720px)" in css
    assert "overflow:auto" in css and "min-width:320px" in css
