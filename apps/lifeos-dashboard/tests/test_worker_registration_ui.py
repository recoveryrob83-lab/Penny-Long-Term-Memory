from pathlib import Path

PACKAGE = Path(__file__).parents[1] / "lifeos_dashboard"
TEMPLATE = PACKAGE / "templates" / "index.html"
SCRIPT = PACKAGE / "static" / "worker-route-management.js"
MAIN = PACKAGE / "main.py"
ROOM_TITLES = PACKAGE / "room_titles.py"


def test_registration_surface_is_present_and_separate_from_route_capture() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")

    assert 'id="wo-worker-registration"' in html
    assert 'id="wo-registration-profile"' in html
    assert 'id="wo-confirm-registration"' in html
    assert 'id="wo-register-worker"' in html
    assert "creates one route-less row at revision 0" in html
    assert "grants no activation or assignment authority" in html
    assert html.index('id="wo-worker-registration"') < html.index(
        'id="wo-route-management"'
    )


def test_registration_ui_requires_pause_profile_and_confirmation() -> None:
    script = SCRIPT.read_text(encoding="utf-8")

    assert 'fetch("/api/worker-operations/registration"' in script
    assert "profile_path: profile.profile_path" in script
    assert "confirm_registration: true" in script
    assert "!paused" in script
    assert "Register approved Worker" in script
    assert "Registration created no route and no activation authority" in script


def test_registration_api_is_bounded_and_profile_derived() -> None:
    source = MAIN.read_text(encoding="utf-8")

    assert "class WorkerRegistrationRequest(BaseModel):" in source
    assert '@application.get("/api/worker-operations/registration")' in source
    assert '@application.post("/api/worker-operations/registration")' in source
    assert "worker_registration.register_profile" in source
    assert "confirm_registration=request.confirm_registration" in source


def test_maintenance_worker_title_is_in_executable_canonical_map() -> None:
    source = ROOM_TITLES.read_text(encoding="utf-8")

    assert '"maintenance_worker": "Maintenance_Worker"' in source
