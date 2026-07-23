import importlib.util
import sys
from pathlib import Path

import pytest


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

ROUNDTRIP_SCRIPT = AUTOMATION / "chatgpt_worker_browser_roundtrip.py"
ROUNDTRIP_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_roundtrip_readiness", ROUNDTRIP_SCRIPT
)
assert ROUNDTRIP_SPEC is not None and ROUNDTRIP_SPEC.loader is not None
hydration = importlib.util.module_from_spec(ROUNDTRIP_SPEC)
sys.modules[ROUNDTRIP_SPEC.name] = hydration
ROUNDTRIP_SPEC.loader.exec_module(hydration)

DISPATCH_SCRIPT = AUTOMATION / "chatgpt_worker_browser_dispatch.py"
DISPATCH_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_dispatch_readiness", DISPATCH_SCRIPT
)
assert DISPATCH_SPEC is not None and DISPATCH_SPEC.loader is not None
dispatch = importlib.util.module_from_spec(DISPATCH_SPEC)
sys.modules[DISPATCH_SPEC.name] = dispatch
DISPATCH_SPEC.loader.exec_module(dispatch)


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
        if selector == hydration.PROMPT_SELECTOR:
            return self.prompt
        if selector == hydration.STOP_SELECTOR:
            return EmptyLocator()
        if selector == hydration.TURN_XPATH:
            return self.turns
        raise AssertionError(f"Unexpected selector: {selector}")

    def evaluate(self, script: str) -> str:
        assert script == "document.readyState"
        return "complete"


class ReturnPrompt(FakePrompt):
    def evaluate(self, script: str) -> str:
        del script
        raise AssertionError("Return proof must not inspect or clear source draft text.")


class ReturnPage:
    def __init__(self, url: str) -> None:
        self.url = url
        self.prompt = ReturnPrompt()
        self.goto_calls: list[tuple[str, str, int]] = []

    def locator(self, selector: str):
        assert selector == hydration.PROMPT_SELECTOR
        return self.prompt

    def goto(self, url: str, *, wait_until: str, timeout: int) -> None:
        self.goto_calls.append((url, wait_until, timeout))
        self.url = f"{url}?model=gpt-5"


class TimeoutAfterCommitPage(ReturnPage):
    def goto(self, url: str, *, wait_until: str, timeout: int) -> None:
        self.goto_calls.append((url, wait_until, timeout))
        self.url = url
        raise RuntimeError("navigation timeout after commit")


class CorrelatedTurn:
    def get_attribute(self, name: str) -> str:
        assert name == "data-testid"
        return "conversation-turn-42"


class VirtualizedHistoryPage:
    def __init__(self, rendered_turns: int) -> None:
        self.turns = SequencedTurns([rendered_turns])

    def locator(self, selector: str):
        assert selector == hydration.TURN_XPATH
        return self.turns


def request(worker_url: str) -> object:
    return hydration.BrowserRoundTripRequest(
        worker_url=worker_url,
        worker_chat_title="Engineering_Worker",
        project_title="LifeOS",
        prompt_text="WAKE-ADV-TEST-R1",
        request_marker="WAKE-ADV-TEST-R1",
        response_marker="RUN-ADV-TEST-R1",
    )


def test_worker_readiness_waits_for_loaded_history(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worker_url = "https://chatgpt.com/g/project/c/worker"
    page = FakePage(worker_url, [0, 2, 2])
    monkeypatch.setattr(hydration, "_verify_worker_identity", lambda *args, **kwargs: None)
    monkeypatch.setattr(hydration.time, "sleep", lambda seconds: None)

    prompt, baseline_turns = hydration._wait_for_worker_conversation_ready(
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

    assert hydration._worker_history_snapshot(page) == (
        1,
        "conversation-turn-9",
        "Existing Worker history",
    )


def test_submission_witness_survives_rendered_history_virtualization() -> None:
    baseline_ids = ("conversation-turn-9",)

    # ChatGPT may replace rendered history nodes rather than increasing
    # their visible count. A genuinely new correlated turn still proves
    # that submission occurred.
    assert dispatch._submission_witness_valid(
        baseline_turns=1,
        final_turns=1,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-42",
        composer_text="",
    )

    # Normal non-virtualized history growth remains valid.
    assert dispatch._submission_witness_valid(
        baseline_turns=1,
        final_turns=2,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-42",
        composer_text="",
    )

    # An old turn cannot prove a new submission.
    assert not dispatch._submission_witness_valid(
        baseline_turns=1,
        final_turns=1,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-9",
        composer_text="",
    )

    # A nonempty composer means submission is not fully proven.
    assert not dispatch._submission_witness_valid(
        baseline_turns=1,
        final_turns=1,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-42",
        composer_text="unsent draft",
    )

    # No rendered history cannot prove submission.
    assert not dispatch._submission_witness_valid(
        baseline_turns=1,
        final_turns=0,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-42",
        composer_text="",
    )

def test_source_return_proves_exact_normalized_url_without_requiring_idle_composer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_url = "https://chatgpt.com/g/project/c/source"
    page = ReturnPage(f"{source_url}?model=gpt-5")
    monkeypatch.setattr(dispatch.time, "sleep", lambda seconds: None)

    dispatch._wait_for_source_conversation_ready(
        page,
        source_url=source_url,
        timeout_ms=1_000,
    )

    assert page.goto_calls == []


def test_source_return_accepts_late_success_after_navigation_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_url = "https://chatgpt.com/g/project/c/source"
    page = TimeoutAfterCommitPage("https://chatgpt.com/g/project/c/worker")
    monkeypatch.setattr(dispatch.time, "sleep", lambda seconds: None)

    dispatch._return_to_source_conversation(
        page,
        source_url=source_url,
        timeout_ms=1_000,
    )

    assert page.goto_calls == [(source_url, "commit", 1_000)]
    assert hydration.normalize_chatgpt_url(page.url) == source_url


def test_dispatch_gates_send_and_never_waits_for_assistant_response() -> None:
    script = DISPATCH_SCRIPT.read_text(encoding="utf-8")
    run_body = script.split("def run_dispatch", 1)[1]

    readiness = run_body.index("_wait_for_dispatch_ready(")
    fill = run_body.index("prompt.fill(request.prompt_text)")
    unchanged_history = run_body.index(
        "if turns.count() != baseline_turns or _turn_ids(page) != baseline_turn_ids:"
    )
    submit = run_body.index("user_turn_id, final_turns = _submit_and_confirm(")
    return_to_source = run_body.index("_return_to_source_conversation(")

    assert readiness < fill < unchanged_history < submit < return_to_source
    assert 'role="assistant"' not in run_body
    assert "_wait_for_stable_turn" not in run_body
    assert "without waiting for Worker output" in script
    assert "_wait_for_idle_composer(page" not in run_body[submit:]

    submit_body = script.split("def _submit_and_confirm", 1)[1].split(
        "def run_dispatch", 1
    )[0]

    assert "_try_confirm_user_turn(" in submit_body
    assert "draft_still_present" in submit_body
    assert "history_unchanged" in submit_body
    assert "BrowserRoundTripUncertain" in submit_body
    assert 'role="assistant"' not in submit_body