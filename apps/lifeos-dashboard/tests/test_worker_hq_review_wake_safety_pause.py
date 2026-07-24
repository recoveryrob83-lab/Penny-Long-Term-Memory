import importlib.util
from pathlib import Path
from types import ModuleType

import lifeos_dashboard.command_center_safety_pause_runtime  # noqa: F401
from lifeos_dashboard.command_center import CommandCenterService


def _wake_module() -> ModuleType:
    script = (
        Path(__file__).resolve().parents[1]
        / "automation"
        / "run_worker_hq_review_wake.py"
    )
    spec = importlib.util.spec_from_file_location("test_run_worker_hq_review_wake", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _service(tmp_path: Path) -> CommandCenterService:
    return CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )


def test_hq_wake_uncertain_send_trips_shared_pause(tmp_path: Path) -> None:
    module = _wake_module()
    service = _service(tmp_path)

    module._trip_for_transport(
        service,
        run_id="RUN-HQ-WAKE-SAFETY-1",
        exit_code=3,
        stderr="STOPPED_AFTER_SEND: strict witness missing",
        reason="HQ wake submission state is uncertain.",
    )

    assert service.paused is True
    assert service.pause_state()["affected_run_id"] == "RUN-HQ-WAKE-SAFETY-1"
    assert service.pause_state()["trigger"] == "hq_review_browser_transport"


def test_hq_wake_deterministic_presend_stop_does_not_pause(tmp_path: Path) -> None:
    module = _wake_module()
    service = _service(tmp_path)

    module._trip_for_transport(
        service,
        run_id="RUN-HQ-WAKE-SAFETY-2",
        exit_code=2,
        stderr="STOPPED: exact destination was unavailable; nothing was sent.",
        reason="Safe pre-send stop.",
    )

    assert service.paused is False
    assert service.pause_state()["pause_kind"] == "none"
