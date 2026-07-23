import importlib.util
import sys
from pathlib import Path


AUTOMATION = Path(__file__).parents[1] / "automation"
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))

SCRIPT = AUTOMATION / "chatgpt_worker_browser_dispatch.py"
SPEC = importlib.util.spec_from_file_location("chatgpt_worker_browser_dispatch_recovery", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
dispatch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dispatch
SPEC.loader.exec_module(dispatch)


class FakeLocator:
    def __init__(self, *, count=0, visible=False, enabled=False):
        self._count = count
        self._visible = visible
        self._enabled = enabled
        self.clicked = 0

    def count(self):
        return self._count

    def nth(self, _index):
        return self

    def is_visible(self):
        return self._visible

    def is_enabled(self):
        return self._enabled

    def click(self):
        self.clicked += 1


class FakePrompt:
    def __init__(self, text):
        self.text = text
        self.pressed = []

    def evaluate(self, _script):
        return self.text

    def press(self, key):
        self.pressed.append(key)


class FakePage:
    def __init__(self):
        self.stop = FakeLocator()
        self.turns = FakeLocator(count=6)

    def locator(self, selector):
        if selector == dispatch.STOP_SELECTOR:
            return self.stop
        if selector == dispatch.TURN_XPATH:
            return self.turns
        return FakeLocator()


def request():
    return dispatch.BrowserRoundTripRequest(
        worker_url="https://chatgpt.com/g/project/c/worker",
        worker_chat_title="Engineering_Worker",
        project_title="Life OS",
        prompt_text="WAKE-ADV-050 RUN-ADV-050",
        request_marker="WAKE-ADV-050",
        response_marker="RUN-ADV-050",
    )


def test_matching_draft_requires_both_run_markers():
    item = request()

    assert dispatch._matching_draft("WAKE-ADV-050 RUN-ADV-050", item)
    assert not dispatch._matching_draft("WAKE-ADV-050", item)
    assert not dispatch._matching_draft("RUN-ADV-050", item)


def test_submission_witness_rejects_adv050_paste_only_false_positive():
    assert not dispatch._submission_witness_valid(
        baseline_turns=6,
        final_turns=6,
        baseline_turn_ids=("conversation-turn-40",),
        user_turn_id="conversation-turn-40",
        composer_text="WAKE-ADV-050 RUN-ADV-050",
    )


def test_submission_witness_requires_all_three_postconditions():
    baseline_ids = ("conversation-turn-40",)

    assert dispatch._submission_witness_valid(
        baseline_turns=6,
        final_turns=7,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-41",
        composer_text="",
    )
    assert not dispatch._submission_witness_valid(
        baseline_turns=6,
        final_turns=6,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-41",
        composer_text="",
    )
    assert not dispatch._submission_witness_valid(
        baseline_turns=6,
        final_turns=7,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-40",
        composer_text="",
    )
    assert not dispatch._submission_witness_valid(
        baseline_turns=6,
        final_turns=7,
        baseline_turn_ids=baseline_ids,
        user_turn_id="conversation-turn-41",
        composer_text="still pasted",
    )


def test_button_noop_falls_back_to_enter_only_after_draft_remains(monkeypatch):
    item = request()
    prompt = FakePrompt(item.prompt_text)
    page = FakePage()
    button = FakeLocator(count=1, visible=True, enabled=True)
    confirmations = iter([None, ("conversation-turn-41", 7)])

    monkeypatch.setattr(dispatch, "_visible_enabled_send", lambda _page: [button])
    monkeypatch.setattr(
        dispatch,
        "_try_confirm_user_turn",
        lambda *_args, **_kwargs: next(confirmations),
    )

    result = dispatch._submit_and_confirm(
        page,
        prompt,
        item,
        deadline=dispatch.time.monotonic() + 30,
    )

    assert result == ("conversation-turn-41", 7)
    assert button.clicked == 1
    assert prompt.pressed == ["Enter"]


def test_enter_is_used_when_no_visible_send_control(monkeypatch):
    item = request()
    prompt = FakePrompt(item.prompt_text)
    page = FakePage()

    monkeypatch.setattr(dispatch, "_visible_enabled_send", lambda _page: [])
    monkeypatch.setattr(
        dispatch,
        "_try_confirm_user_turn",
        lambda *_args, **_kwargs: ("conversation-turn-41", 7),
    )

    result = dispatch._submit_and_confirm(
        page,
        prompt,
        item,
        deadline=dispatch.time.monotonic() + 30,
    )

    assert result == ("conversation-turn-41", 7)
    assert prompt.pressed == ["Enter"]
