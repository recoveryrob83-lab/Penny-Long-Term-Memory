import importlib.util
import json
import sys
from pathlib import Path

import pytest

AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

SCRIPT = AUTOMATION / "chatgpt_worker_browser_dispatch.py"
SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_dispatch_residue",
    SCRIPT,
)
assert SPEC is not None and SPEC.loader is not None
dispatch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dispatch
SPEC.loader.exec_module(dispatch)


class FakePrompt:
    def __init__(self, text: str) -> None:
        self.text = text
        self.fill_calls: list[str] = []

    def evaluate(self, _script: str) -> str:
        return self.text

    def fill(self, value: str) -> None:
        self.fill_calls.append(value)
        self.text = value


class FakeUserNode:
    def __init__(self, text: str) -> None:
        self.text = text

    def evaluate(self, _script: str) -> str:
        return self.text


class FakeUserNodes:
    def __init__(self, texts: list[str]) -> None:
        self.nodes = [FakeUserNode(text) for text in texts]

    def filter(self, *, has_text: str):
        return FakeUserNodes([node.text for node in self.nodes if has_text in node.text])

    def count(self) -> int:
        return len(self.nodes)

    def nth(self, index: int) -> FakeUserNode:
        return self.nodes[index]


class FakePage:
    def __init__(self, user_turns: list[str]) -> None:
        self.user_turns = user_turns

    def locator(self, selector: str):
        assert selector == dispatch.USER_MESSAGE_SELECTOR
        return FakeUserNodes(self.user_turns)


def request():
    return dispatch.BrowserRoundTripRequest(
        worker_url="https://chatgpt.com/g/project/c/worker",
        worker_chat_title="Maintenance_Worker",
        project_title="LifeOS",
        prompt_text="CURRENT-WRAP CURRENT-RUN",
        request_marker="CURRENT-WRAP",
        response_marker="CURRENT-RUN",
    )


def lifeos_draft(wrapper_id: str = "OLD-WRAP", run_id: str = "OLD-RUN") -> str:
    payload = json.dumps(
        {
            "wrapper_id": wrapper_id,
            "run_id": run_id,
            "worker_id": "maintenance_worker",
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"LIFEOS_EXECUTION_WRAPPER={payload}\n\nOld bounded instruction"


def test_lifeos_draft_markers_extract_wrapper_and_run_ids() -> None:
    assert dispatch._lifeos_draft_markers(lifeos_draft()) == (
        "OLD-WRAP",
        "OLD-RUN",
    )
    assert dispatch._lifeos_draft_markers("ordinary user draft") is None
    assert dispatch._lifeos_draft_markers("LIFEOS_EXECUTION_WRAPPER={bad json}") is None


def test_current_run_draft_is_reused_without_clearing() -> None:
    prompt = FakePrompt("CURRENT-WRAP CURRENT-RUN")

    assert dispatch._prepare_existing_draft(FakePage([]), prompt, request()) is True
    assert prompt.fill_calls == []


def test_unrelated_user_draft_is_preserved_and_blocks_dispatch() -> None:
    prompt = FakePrompt("Rob's unrelated unsent note")

    with pytest.raises(dispatch.BrowserRoundTripError, match="different unsent draft"):
        dispatch._prepare_existing_draft(FakePage([]), prompt, request())

    assert prompt.text == "Rob's unrelated unsent note"
    assert prompt.fill_calls == []


def test_proven_stale_lifeos_residue_is_cleared_before_new_fill() -> None:
    stale = lifeos_draft()
    prompt = FakePrompt(stale)
    page = FakePage([f"Submitted message containing {stale}"])

    assert dispatch._prepare_existing_draft(page, prompt, request()) is False
    assert prompt.text == ""
    assert prompt.fill_calls == [""]


def test_unproven_lifeos_draft_is_preserved() -> None:
    stale = lifeos_draft()
    prompt = FakePrompt(stale)

    assert dispatch._prepare_existing_draft(FakePage([]), prompt, request()) is None
    assert prompt.text == stale
    assert prompt.fill_calls == []


def test_wrapper_and_run_ids_must_appear_in_same_submitted_turn() -> None:
    stale = lifeos_draft()
    prompt = FakePrompt(stale)
    page = FakePage(["OLD-WRAP only", "OLD-RUN only"])

    assert dispatch._prepare_existing_draft(page, prompt, request()) is None
    assert prompt.text == stale
    assert prompt.fill_calls == []
