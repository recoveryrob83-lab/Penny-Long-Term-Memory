import importlib.util
import sys
from pathlib import Path

import pytest


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))
TRANSPORT_SCRIPT = AUTOMATION / "chatgpt_worker_browser_dispatch.py"
TRANSPORT_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_dispatch_readiness", TRANSPORT_SCRIPT
)
assert TRANSPORT_SPEC is not None and TRANSPORT_SPEC.loader is not None
transport = importlib.util.module_from_spec(TRANSPORT_SPEC)
sys.modules[TRANSPORT_SPEC.name] = transport
TRANSPORT_SPEC.loader.exec_module(transport)


class FakePrompt:
    @property
    def first(self):
        return self

    def count(self) -> int:
        return 1

    def is_visible(self) -> bool:
        return True

    def evaluate(self, script: str) -> str:
        del script
        return ""


class EmptyLocator:
    @property
    def first(self):
        return self

    def count(self) -> int:
        return 0

    def is_visible(self) -> bool:
        return False


class FakeTurn:
    def is_visible(self) -> bool:
        return True

    def get_attribute(self, name: str) -> str:
        assert name == "data-testid"
        return "conversation-turn-9"

    def inner_text(self) -> str:
        return "Existing Worker history"


class SequencedTurns:
    def __init__(self, counts: list[int]) -> None:
        self.counts = counts
        self.index = 0
        self.last_count = 0
        self.last = FakeTurn()

    def count(self) -> int:
        position = min(self.index, len(self.counts) - 1)
        self.last_count = self.counts[position]
        self.index += 1
        return self.last_count


class FakePage:
    def __init__(self, worker_url: str, counts: list[int]) -> None:
        self.url = worker_url
        self.prompt = FakePrompt()
        self.turns = SequencedTurns(counts)

    def locator(self, selector: str):
        if selector == transport.PROMPT_SELECTOR:
            return self.prompt
        if selector == transport.STOP_SELECTOR:
            return EmptyLocator()
        if selector == transport.TURN_XPATH:
            return self.turns
        raise AssertionError(f"Unexpected selector: {selector}")

    def evaluate(self, script: str) -> str:
        assert script == "document.readyState"
        return "complete"


def request(worker_url: str) -> object:
    return transport.BrowserRoundTripRequest(
        worker_url=worker_url,
        worker_chat_title="Engineering_Worker",
        project_title="Life OS",
        prompt_text="WAKE-ADV-TEST-R1",
        request_marker="WAKE-ADV-TEST-R1",
        response_marker="RUN-ADV-TEST-R1",
    )


def test_worker_readiness_waits_for_loaded_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worker_url = "https://chatgpt.com/g/project/c/worker"
    page = FakePage(worker_url, [0, 2, 2])
    monkeypatch.setattr(transport, "_verify_worker_identity", lambda *args, **kwargs: None)
    monkeypatch.setattr(transport.time, "sleep", lambda seconds: None)

    prompt, baseline_turns = transport._wait_for_worker_conversation_ready(
        page,
        request(worker_url),
        worker_url=worker_url,
        timeout_ms=5_000,
        stable_seconds=-1.0,
    )

    assert prompt is page.prompt
    assert baseline_turns == 2
    assert page.turns.index >= 3


def test_worker_history_snapshot_requires_visible_nonempty_turn() -> None:
    worker_url = "https://chatgpt.com/g/project/c/worker"
    page = FakePage(worker_url, [1])

    assert transport._worker_history_snapshot(page) == (
        1,
        "conversation-turn-9",
        "Existing Worker history",
    )


def test_dispatch_gates_send_and_never_waits_for_assistant_response() -> None:
    script = TRANSPORT_SCRIPT.read_text(encoding="utf-8")
    run_body = script.split("def run_dispatch", 1)[1]

    readiness = run_body.index("prompt, baseline_turns = _wait_for_worker_conversation_ready")
    fill = run_body.index("prompt.fill(request.prompt_text)")
    unchanged_history = run_body.index("if turns.count() != baseline_turns")
    click = run_body.index("send.click()")
    user_turn = run_body.index('role="user"')
    return_to_source = run_body.index("page.goto(source_url")

    assert readiness < fill < unchanged_history < click < user_turn < return_to_source
    assert 'role="assistant"' not in run_body
    assert "_wait_for_stable_turn" not in run_body
    assert "without waiting for Worker output" in script
