from pathlib import Path

from lifeos_dashboard.command_center import CommandCenterService


def test_command_center_status_exposes_worker_verification_view(tmp_path: Path) -> None:
    service = CommandCenterService(
        tmp_path,
        database_path=tmp_path / "command-center.sqlite3",
    )

    status = service.status()

    assert status["worker_verification"] == {
        "summary": {
            "total": 0,
            "pending": 0,
            "verified": 0,
            "rejected": 0,
            "routine_queue": 0,
            "wake_required": 0,
            "wake_suppressed": 0,
        },
        "records": [],
    }
