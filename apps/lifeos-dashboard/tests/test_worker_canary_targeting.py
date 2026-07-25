import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from lifeos_dashboard.command_center import CommandCenterService
from lifeos_dashboard.worker_route_management import (
    RouteAwareWorkerOperationsService,
    WorkerRouteManager,
)
from lifeos_dashboard.worker_runtime import WorkerRegistryEntry, WorkerRuntimeError
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

PILOT_SCRIPT = AUTOMATION / "run_synthetic_worker_browser_pilot.py"
PILOT_SPEC = importlib.util.spec_from_file_location(
    "dynamic_synthetic_worker_browser_pilot",
    PILOT_SCRIPT,
)
assert PILOT_SPEC is not None and PILOT_SPEC.loader is not None
pilot = importlib.util.module_from_spec(PILOT_SPEC)
sys.modules[PILOT_SPEC.name] = pilot
PILOT_SPEC.loader.exec_module(pilot)


def register_worker(
    runtime: WorkerRuntimeService,
    *,
    worker_id: str,
    chat_title: str,
    owning_department: str,
    profile_path: str,
    url: str,
    revision: int,
    availability: str,
) -> None:
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id=worker_id,
            chat_title=chat_title,
            owning_department=owning_department,
            profile_path=profile_path,
            profile_version=1,
            conversation_url=url,
            route_revision=revision,
        )
    )
    runtime.set_route_state(
        worker_id,
        availability,
        pause_reason=(
            f"Direct URL route revision {revision} awaiting zero-authority browser canary."
            if availability == "unknown"
            else None
        ),
    )


def runtime_with_maintenance_pending(
    tmp_path: Path,
) -> tuple[CommandCenterService, WorkerRuntimeService]:
    database = tmp_path / "command-center.sqlite3"
    command_center = CommandCenterService(tmp_path, database_path=database)
    runtime = WorkerRuntimeService(database)
    register_worker(
        runtime,
        worker_id="engineering_worker",
        chat_title="Engineering_Worker",
        owning_department="engineering",
        profile_path="projects/engineering/workers/engineering_worker.md",
        url="https://chatgpt.com/g/project/c/engineering-worker",
        revision=1,
        availability="available",
    )
    register_worker(
        runtime,
        worker_id="maintenance_worker",
        chat_title="Maintenance_Worker",
        owning_department="maintenance",
        profile_path="projects/life-logistics-hq/workers/maintenance_worker.md",
        url="https://chatgpt.com/g/project/c/maintenance-worker",
        revision=1,
        availability="unknown",
    )
    return command_center, runtime


def test_pending_canary_witness_selects_sole_unknown_routed_worker(tmp_path: Path) -> None:
    command_center, _ = runtime_with_maintenance_pending(tmp_path)
    manager = WorkerRouteManager(command_center)

    witness = manager.pending_canary_witness()

    assert witness.worker_id == "maintenance_worker"
    assert witness.route_revision == 1
    assert witness.conversation_url.endswith("/maintenance-worker")


def test_pending_canary_witness_refuses_multiple_unknown_routes(tmp_path: Path) -> None:
    command_center, runtime = runtime_with_maintenance_pending(tmp_path)
    runtime.set_route_state(
        "engineering_worker",
        "unknown",
        pause_reason="Awaiting canary.",
    )
    manager = WorkerRouteManager(command_center)

    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        manager.pending_canary_witness()


def test_dashboard_canary_targets_maintenance_and_promotes_only_that_route(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command_center, runtime = runtime_with_maintenance_pending(tmp_path)
    (tmp_path / ".git").mkdir()
    service = RouteAwareWorkerOperationsService(
        command_center,
        tmp_path,
        cdp_endpoint="http://127.0.0.1:9222",
    )
    observed_command: list[str] = []
    receipt = {
        "status": "succeeded",
        "durable_authority_created": False,
        "returned_to_source": True,
        "user_turn_id": "conversation-turn-maintenance-canary",
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

    worker_index = observed_command.index("--worker-id")
    revision_index = observed_command.index("--expected-route-revision")
    assert observed_command[worker_index + 1] == "maintenance_worker"
    assert observed_command[revision_index + 1] == "1"
    assert result["route_promotion"]["worker"]["worker_id"] == "maintenance_worker"

    maintenance_route = runtime.store.route_state("maintenance_worker")
    engineering_route = runtime.store.route_state("engineering_worker")
    assert maintenance_route is not None
    assert maintenance_route.availability == "available"
    assert maintenance_route.pause_reason is None
    assert engineering_route is not None
    assert engineering_route.availability == "available"


def test_synthetic_plan_accepts_maintenance_worker_and_exact_revision(
    tmp_path: Path,
) -> None:
    _, runtime = runtime_with_maintenance_pending(tmp_path)

    plan = pilot.build_plan(
        database_path=runtime.store.database_path,
        worker_id="maintenance_worker",
        expected_route_revision=1,
        timestamp=1234567890,
        nonce="maint123",
    )

    assert plan.envelope.worker_id == "maintenance_worker"
    assert plan.request.worker_chat_title == "Maintenance_Worker"
    assert plan.request.worker_url.endswith("/maintenance-worker")
    assert plan.route_revision == 1
    assert "no real authority" in plan.prompt_text


def test_synthetic_plan_refuses_stale_expected_revision(tmp_path: Path) -> None:
    _, runtime = runtime_with_maintenance_pending(tmp_path)

    with pytest.raises(pilot.SyntheticBrowserPilotError, match="changed from expected"):
        pilot.build_plan(
            database_path=runtime.store.database_path,
            worker_id="maintenance_worker",
            expected_route_revision=2,
        )
