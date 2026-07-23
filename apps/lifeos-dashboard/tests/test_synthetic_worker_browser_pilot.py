import importlib.util
import json
import sys
from pathlib import Path

from lifeos_dashboard.worker_runtime import WorkerRegistryEntry
from lifeos_dashboard.worker_runtime_service import WorkerRuntimeService

import pytest


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

DISPATCH_SCRIPT = AUTOMATION / "chatgpt_worker_browser_dispatch.py"
DISPATCH_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_dispatch", DISPATCH_SCRIPT
)
assert DISPATCH_SPEC is not None and DISPATCH_SPEC.loader is not None
dispatch = importlib.util.module_from_spec(DISPATCH_SPEC)
sys.modules[DISPATCH_SPEC.name] = dispatch
DISPATCH_SPEC.loader.exec_module(dispatch)

PILOT_SCRIPT = AUTOMATION / "run_synthetic_worker_browser_pilot.py"
PILOT_SPEC = importlib.util.spec_from_file_location(
    "synthetic_worker_browser_pilot", PILOT_SCRIPT
)
assert PILOT_SPEC is not None and PILOT_SPEC.loader is not None
pilot = importlib.util.module_from_spec(PILOT_SPEC)
sys.modules[PILOT_SPEC.name] = pilot
PILOT_SPEC.loader.exec_module(pilot)


def registered_database(
    tmp_path: Path,
    *,
    url: str | None = "https://chatgpt.com/g/project/c/engineering-worker",
    revision: int = 1,
    availability: str = "unknown",
) -> Path:
    database = tmp_path / "command_center.sqlite3"
    runtime = WorkerRuntimeService(database)
    runtime.register_worker(
        WorkerRegistryEntry(
            worker_id="engineering_worker",
            chat_title="Engineering_Worker",
            owning_department="engineering",
            profile_path="projects/engineering/workers/engineering_worker.md",
            profile_version=1,
            conversation_url=url,
            route_revision=revision,
        )
    )
    runtime.set_route_state(
        "engineering_worker",
        availability,
        pause_reason="Synthetic test route.",
    )
    return database


def test_normalize_chatgpt_url_removes_query_fragment_and_trailing_slash() -> None:
    value = "https://chatgpt.com/g/project/c/chat-id/?model=x#fragment"

    assert dispatch.normalize_chatgpt_url(value) == (
        "https://chatgpt.com/g/project/c/chat-id"
    )


def test_normalize_chatgpt_url_rejects_non_chatgpt_or_non_conversation() -> None:
    with pytest.raises(dispatch.BrowserRoundTripError, match="chatgpt.com"):
        dispatch.normalize_chatgpt_url("https://example.com/c/chat-id")

    with pytest.raises(dispatch.BrowserRoundTripError, match="conversation"):
        dispatch.normalize_chatgpt_url("https://chatgpt.com/")


def test_request_requires_markers_and_bounded_timeout() -> None:
    with pytest.raises(dispatch.BrowserRoundTripError, match="request_marker"):
        dispatch.BrowserRoundTripRequest(
            worker_url="https://chatgpt.com/g/project/c/chat-id",
            worker_chat_title="Engineering_Worker",
            project_title="LifeOS",
            prompt_text="prompt without marker",
            request_marker="WRAP-1",
            response_marker="RUN-1",
        )

    with pytest.raises(dispatch.BrowserRoundTripError, match="between 30 and 900"):
        dispatch.BrowserRoundTripRequest(
            worker_url="https://chatgpt.com/g/project/c/chat-id",
            worker_chat_title="Engineering_Worker",
            project_title="LifeOS",
            prompt_text="WRAP-1",
            request_marker="WRAP-1",
            response_marker="RUN-1",
            timeout_seconds=10,
        )


def test_synthetic_plan_is_zero_authority_and_locked_to_engineering_worker(
    tmp_path: Path,
) -> None:
    database = registered_database(tmp_path)
    plan = pilot.build_plan(
        database_path=database,
        timestamp=1234567890,
        nonce="abc123",
    )

    assert plan.envelope.wrapper_id == "SYNTH-BROWSER-WRAP-1234567890-abc123"
    assert plan.envelope.run_id == "SYNTH-BROWSER-RUN-1234567890-abc123"
    assert plan.envelope.worker_id == "engineering_worker"
    assert plan.envelope.authorization_source == pilot.AUTHORIZATION_SOURCE
    assert plan.request.worker_url == (
        "https://chatgpt.com/g/project/c/engineering-worker"
    )
    assert plan.route_revision == 1
    assert plan.request.worker_chat_title == "Engineering_Worker"
    assert plan.request.request_marker == plan.envelope.wrapper_id
    assert plan.request.response_marker == plan.envelope.run_id
    assert "no real authority" in plan.prompt_text
    assert "Do not create or modify durable records" in plan.prompt_text


def test_synthetic_send_requires_exact_confirmation() -> None:
    wrong = pilot.parse_args(["--send", "--confirm-send", "wrong"])
    with pytest.raises(pilot.SyntheticBrowserPilotError, match="SYNTHETIC_SEND"):
        pilot.validate_args(wrong)

    valid = pilot.parse_args(["--send", "--confirm-send", "SYNTHETIC_SEND"])
    pilot.validate_args(valid)


def test_dry_run_emits_receipt_without_browser_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def should_not_run(*args, **kwargs):
        raise AssertionError("dry run must not attach to a browser")

    monkeypatch.setattr(pilot, "run_dispatch", should_not_run)
    database = registered_database(tmp_path)

    assert pilot.main([
        "--dry-run",
        "--database-path",
        str(database),
    ]) == 0
    output = capsys.readouterr().out
    receipt_line = next(
        line for line in output.splitlines() if line.startswith(pilot.RECEIPT_PREFIX)
    )
    receipt = json.loads(receipt_line.removeprefix(pilot.RECEIPT_PREFIX))
    assert receipt["status"] == "dry_run"
    assert receipt["worker_chat_title"] == "Engineering_Worker"
    assert receipt["route_revision"] == 1
    assert receipt["durable_authority_created"] is False


def test_successful_pilot_reports_dispatch_and_return(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(request):
        return dispatch.BrowserDispatchReceipt(
            status="submitted",
            worker_url=request.worker_url,
            return_url="https://chatgpt.com/g/project/c/hq-chat",
            request_marker=request.request_marker,
            run_id=request.response_marker,
            baseline_turns=5,
            final_turns=6,
            user_turn_id="conversation-turn-16",
            submission_confirmed=True,
            returned_to_source=True,
            return_error=None,
            submission_uncertain=False,
        )

    monkeypatch.setattr(pilot, "run_dispatch", fake_run)
    database = registered_database(tmp_path)

    assert pilot.main([
        "--send",
        "--confirm-send",
        "SYNTHETIC_SEND",
        "--database-path",
        str(database),
    ]) == 0
    output = capsys.readouterr().out
    assert "SYNTHETIC_BROWSER_DISPATCH_OK" in output
    receipt_line = next(
        line for line in output.splitlines() if line.startswith(pilot.RECEIPT_PREFIX)
    )
    receipt = json.loads(receipt_line.removeprefix(pilot.RECEIPT_PREFIX))
    assert receipt["dispatch_state"] == "DISPATCH_SUBMITTED"
    assert receipt["returned_to_source"] is True
    assert receipt["user_turn_id"] == "conversation-turn-16"
    assert receipt["durable_authority_created"] is False


def test_pilot_refuses_missing_registered_url(tmp_path: Path) -> None:
    database = registered_database(tmp_path, url=None, revision=0)

    with pytest.raises(
        pilot.SyntheticBrowserPilotError,
        match="no registered exact conversation URL",
    ):
        pilot.build_plan(database_path=database)


@pytest.mark.parametrize("availability", ["unavailable", "ambiguous"])
def test_pilot_refuses_unsafe_route_state(
    tmp_path: Path,
    availability: str,
) -> None:
    database = registered_database(
        tmp_path,
        availability=availability,
    )

    with pytest.raises(
        pilot.SyntheticBrowserPilotError,
        match=f"route is {availability}",
    ):
        pilot.build_plan(database_path=database)
