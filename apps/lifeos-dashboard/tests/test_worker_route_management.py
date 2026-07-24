import json
import sqlite3
import subprocess
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_route_management import (
    CapturedConversation,
    RouteAwareWorkerOperationsService,
    WorkerRouteManager,
    capture_chatgpt_conversation,
)
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService


CURRENT_URL = "https://chatgpt.com/g/project/c/engineering-worker"
NEXT_URL = "https://chatgpt.com/g/project/c/engineering-worker-next"


def route_fixture(
    tmp_path: Path,
    *,
    captured_url: str = NEXT_URL,
    captured_title: str = "Engineering_Worker",
) -> tuple[CommandCenterService, WorkerRuntimeService, WorkerRouteManager]:
    database = tmp_path / "command_center.sqlite3"
    command_center = CommandCenterService(tmp_path, database_path=database)
    runtime = WorkerRuntimeService(database)
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
            conversation_url=CURRENT_URL,
            route_revision=1,
        )
    )
    runtime.set_route_state(
        "engineering_worker",
        "available",
        last_seen_at=1.0,
        pause_reason=None,
    )
    manager = WorkerRouteManager(
        command_center,
        capture_conversation=lambda endpoint: CapturedConversation(
            url=captured_url,
            title=captured_title,
        ),
    )
    return command_center, runtime, manager


def test_capture_requires_paused_automation(tmp_path: Path) -> None:
    _, _, manager = route_fixture(tmp_path)

    with pytest.raises(WorkerRuntimeError, match="Pause automation"):
        manager.capture_active_route(
            "engineering_worker",
            expected_route_revision=1,
            confirm_capture=True,
        )


def test_capture_rolls_existing_row_and_holds_route_for_canary(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(tmp_path)
    command_center.set_paused(True)

    result = manager.capture_active_route(
        "engineering_worker",
        expected_route_revision=1,
        confirm_capture=True,
    )

    saved = runtime.worker("engineering_worker")
    route = runtime.store.route_state("engineering_worker")
    assert result["changed"] is True
    assert saved.conversation_url == NEXT_URL
    assert saved.route_revision == 2
    assert route is not None
    assert route.availability == "unknown"
    assert route.last_seen_at is None
    assert "revision 2 awaiting" in str(route.pause_reason)

    with sqlite3.connect(runtime.store.database_path) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM worker_registry WHERE worker_id = ?",
            ("engineering_worker",),
        ).fetchone()[0]
    assert count == 1


def test_capture_rejects_stale_dashboard_revision(tmp_path: Path) -> None:
    command_center, _, manager = route_fixture(tmp_path)
    command_center.set_paused(True)

    with pytest.raises(WorkerRuntimeError, match="Refresh before trying again"):
        manager.capture_active_route(
            "engineering_worker",
            expected_route_revision=0,
            confirm_capture=True,
        )


def test_capture_rejects_wrong_worker_title(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(
        tmp_path,
        captured_title="Chief_of_Staff_HQ",
    )
    command_center.set_paused(True)

    with pytest.raises(
        WorkerRuntimeError,
        match="does not match the selected Worker title",
    ):
        manager.capture_active_route(
            "engineering_worker",
            expected_route_revision=1,
            confirm_capture=True,
        )

    saved = runtime.worker("engineering_worker")
    assert saved.conversation_url == CURRENT_URL
    assert saved.route_revision == 1


def test_capture_same_url_is_no_write(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(
        tmp_path,
        captured_url=CURRENT_URL + "?model=gpt-5#fragment",
    )
    command_center.set_paused(True)

    result = manager.capture_active_route(
        "engineering_worker",
        expected_route_revision=1,
        confirm_capture=True,
    )

    saved = runtime.worker("engineering_worker")
    route = runtime.store.route_state("engineering_worker")
    assert result["changed"] is False
    assert saved.conversation_url == CURRENT_URL
    assert saved.route_revision == 1
    assert route is not None and route.availability == "available"


def test_capture_rejects_route_owned_by_another_worker(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(tmp_path)
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="second_worker",
            chat_title="Second_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/second_worker.md",
            profile_version=1,
            conversation_url=NEXT_URL,
            route_revision=1,
        )
    )
    command_center.set_paused(True)

    with pytest.raises(WorkerRuntimeError, match="already registered to another Worker"):
        manager.capture_active_route(
            "engineering_worker",
            expected_route_revision=1,
            confirm_capture=True,
        )

    saved = runtime.worker("engineering_worker")
    assert saved.conversation_url == CURRENT_URL
    assert saved.route_revision == 1


def test_successful_canary_promotes_only_the_witnessed_revision(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(tmp_path)
    command_center.set_paused(True)
    manager.capture_active_route(
        "engineering_worker",
        expected_route_revision=1,
        confirm_capture=True,
    )
    witness = manager.canary_witness()

    promoted = manager.promote_after_canary(
        witness,
        {
            "status": "succeeded",
            "durable_authority_created": False,
            "returned_to_source": True,
            "user_turn_id": "conversation-turn-44",
        },
    )

    route = runtime.store.route_state("engineering_worker")
    assert "verified and available" in promoted["message"]
    assert route is not None
    assert route.availability == "available"
    assert route.last_seen_at is not None
    assert route.pause_reason is None


def test_canary_promotion_rejects_route_drift(tmp_path: Path) -> None:
    command_center, runtime, manager = route_fixture(tmp_path)
    command_center.set_paused(True)
    manager.capture_active_route(
        "engineering_worker",
        expected_route_revision=1,
        confirm_capture=True,
    )
    witness = manager.canary_witness()
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
            conversation_url="https://chatgpt.com/g/project/c/third-route",
            route_revision=3,
        )
    )

    with pytest.raises(WorkerRuntimeError, match="changed during the canary"):
        manager.promote_after_canary(
            witness,
            {
                "status": "succeeded",
                "durable_authority_created": False,
                "returned_to_source": True,
                "user_turn_id": "conversation-turn-45",
            },
        )


def test_dashboard_canary_uses_authoritative_database_and_promotes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database = tmp_path / "custom-command-center.sqlite3"
    command_center = CommandCenterService(tmp_path, database_path=database)
    (tmp_path / ".git").mkdir()
    service = RouteAwareWorkerOperationsService(
        command_center,
        tmp_path,
        cdp_endpoint="http://127.0.0.1:9222",
    )
    service.worker_center.runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
            conversation_url=CURRENT_URL,
            route_revision=1,
        )
    )
    service.worker_center.runtime.set_route_state(
        "engineering_worker",
        "unknown",
        pause_reason="Awaiting canary.",
    )
    observed_command: list[str] = []
    receipt = {
        "status": "succeeded",
        "durable_authority_created": False,
        "returned_to_source": True,
        "user_turn_id": "conversation-turn-46",
    }
    stdout = (
        "SYNTHETIC_BROWSER_DISPATCH_OK\n"
        "LIFEOS_SYNTHETIC_BROWSER_RECEIPT=" + json.dumps(receipt)
    )

    def fake_run(command, **kwargs):
        del kwargs
        observed_command.extend(command)
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=stdout,
            stderr="",
        )

    monkeypatch.setattr(
        "lifeos_dashboard.worker_route_management.subprocess.run",
        fake_run,
    )

    result = service.courier_self_test(
        confirm_send=True,
        timeout_seconds=60,
    )

    database_index = observed_command.index("--database-path")
    assert Path(observed_command[database_index + 1]) == database
    assert "verified and available" in result["route_promotion"]["message"]
    route = service.routes.runtime.store.route_state("engineering_worker")
    assert route is not None
    assert route.availability == "available"
    assert route.pause_reason is None


class FakeResponse:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        del exc_type, exc, traceback

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_cdp_capture_requires_exactly_one_chatgpt_conversation(monkeypatch) -> None:
    payload = [
        {"type": "page", "url": "http://127.0.0.1:8000/", "title": "LifeOS Dashboard"},
        {
            "type": "page",
            "url": CURRENT_URL + "?model=gpt-5",
            "title": "Engineering_Worker",
        },
    ]
    monkeypatch.setattr(
        "lifeos_dashboard.worker_route_management.urllib.request.urlopen",
        lambda *args, **kwargs: FakeResponse(payload),
    )

    captured = capture_chatgpt_conversation("http://127.0.0.1:9222")
    assert captured.url == CURRENT_URL
    assert captured.title == "Engineering_Worker"

    payload.append(
        {
            "type": "page",
            "url": NEXT_URL,
            "title": "Engineering_Worker",
        }
    )
    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        capture_chatgpt_conversation("http://127.0.0.1:9222")
