import importlib.util
import json
import sys
from pathlib import Path

import pytest


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

TRANSPORT_SCRIPT = AUTOMATION / "chatgpt_worker_browser_roundtrip.py"
TRANSPORT_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_roundtrip", TRANSPORT_SCRIPT
)
assert TRANSPORT_SPEC is not None and TRANSPORT_SPEC.loader is not None
transport = importlib.util.module_from_spec(TRANSPORT_SPEC)
sys.modules[TRANSPORT_SPEC.name] = transport
TRANSPORT_SPEC.loader.exec_module(transport)

PILOT_SCRIPT = AUTOMATION / "run_synthetic_worker_browser_pilot.py"
PILOT_SPEC = importlib.util.spec_from_file_location(
    "synthetic_worker_browser_pilot", PILOT_SCRIPT
)
assert PILOT_SPEC is not None and PILOT_SPEC.loader is not None
pilot = importlib.util.module_from_spec(PILOT_SPEC)
sys.modules[PILOT_SPEC.name] = pilot
PILOT_SPEC.loader.exec_module(pilot)


def test_normalize_chatgpt_url_removes_query_fragment_and_trailing_slash() -> None:
    value = "https://chatgpt.com/g/project/c/chat-id/?model=x#fragment"

    assert transport.normalize_chatgpt_url(value) == (
        "https://chatgpt.com/g/project/c/chat-id"
    )


def test_normalize_chatgpt_url_rejects_non_chatgpt_or_non_conversation() -> None:
    with pytest.raises(transport.BrowserRoundTripError, match="chatgpt.com"):
        transport.normalize_chatgpt_url("https://example.com/c/chat-id")

    with pytest.raises(transport.BrowserRoundTripError, match="conversation"):
        transport.normalize_chatgpt_url("https://chatgpt.com/")


def test_request_requires_markers_and_bounded_timeout() -> None:
    with pytest.raises(transport.BrowserRoundTripError, match="request_marker"):
        transport.BrowserRoundTripRequest(
            worker_url="https://chatgpt.com/g/project/c/chat-id",
            worker_chat_title="Engineering_Worker",
            project_title="Life OS",
            prompt_text="prompt without marker",
            request_marker="WRAP-1",
            response_marker="ACK WRAP-1",
        )

    with pytest.raises(transport.BrowserRoundTripError, match="between 30 and 900"):
        transport.BrowserRoundTripRequest(
            worker_url="https://chatgpt.com/g/project/c/chat-id",
            worker_chat_title="Engineering_Worker",
            project_title="Life OS",
            prompt_text="WRAP-1",
            request_marker="WRAP-1",
            response_marker="ACK WRAP-1",
            timeout_seconds=10,
        )


def test_synthetic_plan_is_zero_authority_and_locked_to_engineering_worker() -> None:
    plan = pilot.build_plan(timestamp=1234567890, nonce="abc123")

    assert plan.envelope.wrapper_id == "SYNTH-BROWSER-WRAP-1234567890-abc123"
    assert plan.envelope.run_id == "SYNTH-BROWSER-RUN-1234567890-abc123"
    assert plan.envelope.worker_id == "engineering_worker"
    assert plan.envelope.authorization_source == pilot.AUTHORIZATION_SOURCE
    assert plan.request.worker_url == pilot.WORKER_URL
    assert plan.request.worker_chat_title == "Engineering_Worker"
    assert plan.request.request_marker == plan.envelope.wrapper_id
    assert plan.request.response_marker == plan.expected_ack
    assert "no real authority" in plan.prompt_text
    assert "Do not create or modify durable records" in plan.prompt_text


def test_synthetic_send_requires_exact_confirmation() -> None:
    wrong = pilot.parse_args(["--send", "--confirm-send", "wrong"])
    with pytest.raises(pilot.SyntheticBrowserPilotError, match="SYNTHETIC_SEND"):
        pilot.validate_args(wrong)

    valid = pilot.parse_args(["--send", "--confirm-send", "SYNTHETIC_SEND"])
    pilot.validate_args(valid)


def test_dry_run_emits_receipt_without_browser_transport(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def should_not_run(*args, **kwargs):
        raise AssertionError("dry run must not attach to a browser")

    monkeypatch.setattr(pilot, "run_round_trip", should_not_run)

    assert pilot.main(["--dry-run"]) == 0
    output = capsys.readouterr().out
    receipt_line = next(
        line for line in output.splitlines() if line.startswith(pilot.RECEIPT_PREFIX)
    )
    receipt = json.loads(receipt_line.removeprefix(pilot.RECEIPT_PREFIX))
    assert receipt["status"] == "dry_run"
    assert receipt["worker_chat_title"] == "Engineering_Worker"
    assert receipt["durable_authority_created"] is False


def test_successful_pilot_reports_capture_and_return(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run(request):
        return transport.BrowserRoundTripReceipt(
            status="succeeded",
            worker_url=request.worker_url,
            return_url="https://chatgpt.com/g/project/c/hq-chat",
            request_marker=request.request_marker,
            response_marker=request.response_marker,
            baseline_turns=5,
            final_turns=7,
            user_turn_id="conversation-turn-16",
            assistant_turn_id="conversation-turn-17",
            response_text=request.response_marker,
            returned_to_source=True,
            submission_uncertain=False,
        )

    monkeypatch.setattr(pilot, "run_round_trip", fake_run)

    assert pilot.main(["--send", "--confirm-send", "SYNTHETIC_SEND"]) == 0
    output = capsys.readouterr().out
    assert "SYNTHETIC_BROWSER_ROUNDTRIP_OK" in output
    receipt_line = next(
        line for line in output.splitlines() if line.startswith(pilot.RECEIPT_PREFIX)
    )
    receipt = json.loads(receipt_line.removeprefix(pilot.RECEIPT_PREFIX))
    assert receipt["returned_to_source"] is True
    assert receipt["assistant_turn_id"] == "conversation-turn-17"
    assert receipt["durable_authority_created"] is False
