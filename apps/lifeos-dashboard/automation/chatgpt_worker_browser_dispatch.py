"""Dispatch one bounded Worker wake through an existing one-tab Edge CDP session.

This module is transport infrastructure only. It does not create authority, interpret work,
wait for Worker completion, capture assistant responses, change advisory lifecycle, update
databases, or close records. It borrows one already-open ChatGPT tab, submits one explicitly
confirmed prompt to one exact Worker conversation, proves a new correlated user turn exists,
and returns the tab to its original conversation.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass

from chatgpt_worker_browser_roundtrip import (
    DEFAULT_CDP_ENDPOINT,
    PROMPT_SELECTOR,
    SEND_CONFIRMATION,
    STOP_SELECTOR,
    TURN_XPATH,
    WORKER_READY_POLL_SECONDS,
    BrowserRoundTripError,
    BrowserRoundTripRequest,
    BrowserRoundTripUncertain,
    _composer_text,
    _require_single_chatgpt_page,
    _resolve_worker_url,
    _verify_worker_identity,
    _visible,
    _wait_for_idle_composer,
    _worker_history_snapshot,
    normalize_chatgpt_url,
)

RECEIPT_PREFIX = "LIFEOS_BROWSER_DISPATCH_RECEIPT="
SOURCE_RETURN_POLL_SECONDS = 0.25
SUBMISSION_POLL_SECONDS = 0.25
SEND_SELECTOR = ", ".join(
    (
        'button[data-testid="send-button"]:visible',
        'button[aria-label="Send prompt"]:visible',
        'button[aria-label="Send message"]:visible',
        'button[aria-label="Send"]:visible',
    )
)


@dataclass(frozen=True)
class BrowserDispatchReceipt:
    """Run-linked proof that one Worker wake was submitted."""

    status: str
    worker_url: str
    return_url: str
    request_marker: str
    run_id: str
    baseline_turns: int
    final_turns: int
    user_turn_id: str
    submission_confirmed: bool
    returned_to_source: bool
    return_error: str | None
    submission_uncertain: bool

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)


def _receipt(
    request: BrowserRoundTripRequest,
    *,
    worker_url: str,
    source_url: str,
    baseline_turns: int,
    final_turns: int,
    user_turn_id: str,
    returned_to_source: bool,
    return_error: str | None,
) -> BrowserDispatchReceipt:
    return BrowserDispatchReceipt(
        status="submitted",
        worker_url=worker_url,
        return_url=source_url,
        request_marker=request.request_marker,
        run_id=request.response_marker,
        baseline_turns=baseline_turns,
        final_turns=final_turns,
        user_turn_id=user_turn_id,
        submission_confirmed=True,
        returned_to_source=returned_to_source,
        return_error=return_error,
        submission_uncertain=False,
    )


def _wait_for_source_conversation_ready(page, *, source_url: str, timeout_ms: int) -> None:
    deadline = time.monotonic() + (timeout_ms / 1000)
    last_observation = "Source conversation has not rendered."
    while time.monotonic() < deadline:
        try:
            observed_url = normalize_chatgpt_url(page.url)
            if observed_url != source_url:
                last_observation = f"Exact source conversation URL is not active yet: {observed_url}."
            else:
                prompt = page.locator(PROMPT_SELECTOR)
                count = prompt.count()
                if count == 1 and prompt.first.is_visible():
                    return
                last_observation = f"Source composer is not stably visible yet: count={count}."
        except Exception as exc:
            last_observation = str(exc)
        time.sleep(SOURCE_RETURN_POLL_SECONDS)
    raise BrowserRoundTripError(
        "Exact source conversation did not finish rendering before the return timeout. "
        f"Last observation: {last_observation}"
    )


def _return_to_source_conversation(page, *, source_url: str, timeout_ms: int) -> None:
    navigation_error: str | None = None
    if normalize_chatgpt_url(page.url) != source_url:
        try:
            page.goto(source_url, wait_until="commit", timeout=min(timeout_ms, 60_000))
        except Exception as exc:
            navigation_error = str(exc)
    try:
        _wait_for_source_conversation_ready(page, source_url=source_url, timeout_ms=timeout_ms)
    except BrowserRoundTripError as exc:
        if navigation_error:
            raise BrowserRoundTripError(
                f"{exc} Navigation attempt also reported: {navigation_error}"
            ) from exc
        raise



def _matching_draft(text: str, request: BrowserRoundTripRequest) -> bool:
    """Identify only the exact run-linked draft left by a prior pre-submit failure."""

    clean = str(text or "")
    return request.request_marker in clean and request.response_marker in clean


def _turn_ids(page) -> tuple[str, ...]:
    """Return stable IDs for all currently rendered conversation turns."""

    turns = page.locator(TURN_XPATH)
    values: list[str] = []
    for index in range(turns.count()):
        turn_id = str(turns.nth(index).get_attribute("data-testid") or "").strip()
        if turn_id:
            values.append(turn_id)
    return tuple(values)


def _wait_for_dispatch_ready(
    page,
    request: BrowserRoundTripRequest,
    *,
    worker_url: str,
    timeout_ms: int,
) -> tuple[object, int, tuple[str, ...], bool]:
    """Wait for stable Worker history and allow only this run's exact preserved draft."""

    deadline = time.monotonic() + (timeout_ms / 1000)
    last_snapshot: tuple[int, str, str] | None = None
    stable_since: float | None = None
    last_observation = "Worker conversation history has not loaded."
    while time.monotonic() < deadline:
        try:
            if normalize_chatgpt_url(page.url) != worker_url:
                raise BrowserRoundTripError("Exact Worker conversation URL is not active yet.")
            prompt = page.locator(PROMPT_SELECTOR)
            if prompt.count() != 1 or not prompt.first.is_visible():
                raise BrowserRoundTripError("Worker composer is not stably visible yet.")
            if _visible(page.locator(STOP_SELECTOR)):
                raise BrowserRoundTripError("Worker conversation is still generating.")

            draft = _composer_text(prompt)
            reused_draft = bool(draft)
            if reused_draft and not _matching_draft(draft, request):
                raise BrowserRoundTripError(
                    "Worker composer contains a different unsent draft. It was preserved."
                )

            ready_state = str(page.evaluate("document.readyState"))
            snapshot = _worker_history_snapshot(page)
            history_ready = snapshot[0] >= 1 and bool(snapshot[1] and snapshot[2])
            if ready_state == "complete" and history_ready:
                if snapshot == last_snapshot:
                    if stable_since is None:
                        stable_since = time.monotonic()
                  if time.monotonic() - stable_since >= 2.0:
                        _verify_worker_identity(
                            page,
                            request,
                            worker_url=worker_url,
                            timeout_ms=min(
                                10_000,
                                max(1, int((deadline - time.monotonic()) * 1000)),
                            ),
                          )
                        turn_ids = _turn_ids(page)
                        if len(turn_ids) != snapshot[0]:
                            raise BrowserRoundTripError(
                                "Worker turn IDs were incomplete at readiness."
                            )
                        return prompt, snapshot[0], turn_ids, reused_draft
                else:
                    last_snapshot = snapshot
                    stable_since = None
                last_observation = f"Worker history is present but not stable yet: {snapshot[0]} turns."
            else:
                last_snapshot = None
                stable_since = None
                last_observation = (
                    f"Worker room not hydrated: readyState={ready_state}, turns={snapshot[0]}."
                )
        except BrowserRoundTripError as exc:
            if "different unsent draft" in str(exc):
                raise
            last_snapshot = None
            stable_since = None
            last_observation = str(exc)
        except Exception as exc:
            last_snapshot = None
            stable_since = None
            last_observation = str(exc)
        time.sleep(WORKER_READY_POLL_SECONDS)

    raise BrowserRoundTripError(
        "Exact Worker conversation did not finish loading before the readiness timeout. "
        f"Nothing was sent. Last observation: {last_observation}"
    )


def _visible_enabled_send(page):
    locator = page.locator(SEND_SELECTOR)
    matches = []
    for index in range(locator.count()):
        candidate = locator.nth(index)
        if candidate.is_visible() and candidate.is_enabled():
            matches.append(candidate)
    return matches


def _new_matching_user_turn_id(
    page,
    *,
    marker: str,
    baseline_turn_ids: tuple[str, ...],
) -> str | None:
    """Return the newest marker-bearing user turn that did not exist before submit."""

    baseline = set(baseline_turn_ids)
    role_nodes = page.locator('[data-message-author-role="user"]').filter(has_text=marker)
    newest: str | None = None
    for index in range(role_nodes.count()):
        turn = role_nodes.nth(index).locator(
            "xpath=ancestor::*[starts-with(@data-testid,'conversation-turn-')][1]"
        )
        if turn.count() != 1:
            continue
        turn_id = str(turn.get_attribute("data-testid") or "").strip()
        if turn_id and turn_id not in baseline:
            newest = turn_id
    return newest


def _submission_witness_valid(
    *,
    baseline_turns: int,
    final_turns: int,
    baseline_turn_ids: tuple[str, ...],
    user_turn_id: str | None,
    composer_text: str,
) -> bool:
    """Reject paste-only and stale-turn false positives."""

    return bool(
        user_turn_id
        and user_turn_id not in set(baseline_turn_ids)
        and final_turns > baseline_turns
        and not str(composer_text or "").strip()
    )


def _try_confirm_user_turn(
    page,
    *,
    marker: str,
    prompt,
    baseline_turn_ids: tuple[str, ...],
    baseline_turns: int,
    timeout_ms: int,
) -> tuple[str, int] | None:
    """Prove a new marker-bearing user turn, an advanced history, and an empty composer."""

    deadline = time.monotonic() + (timeout_ms / 1000)
    while time.monotonic() < deadline:
        final_turns = page.locator(TURN_XPATH).count()
        user_turn_id = _new_matching_user_turn_id(
            page,
            marker=marker,
            baseline_turn_ids=baseline_turn_ids,
        )
        if _submission_witness_valid(
            baseline_turns=baseline_turns,
            final_turns=final_turns,
            baseline_turn_ids=baseline_turn_ids,
            user_turn_id=user_turn_id,
            composer_text=_composer_text(prompt),
        ):
            assert user_turn_id is not None
            return user_turn_id, final_turns
        time.sleep(SUBMISSION_POLL_SECONDS)
    return None


def _submit_and_confirm(
    page,
    prompt,
    request: BrowserRoundTripRequest,
    *,
    deadline: float,
    baseline_turn_ids: tuple[str, ...] = (),
    baseline_turns: int | None = None,
) -> tuple[str, int]:
    """Submit once, using a fallback only when the first action provably did nothing."""

    if not _matching_draft(_composer_text(prompt), request):
        raise BrowserRoundTripError("Composer no longer contains the exact run-linked draft.")
    if baseline_turns is None:
        baseline_turns = page.locator(TURN_XPATH).count()

    buttons = _visible_enabled_send(page)
    first_method = "button" if len(buttons) == 1 else "enter"
    if len(buttons) > 1:
        raise BrowserRoundTripError("Multiple enabled Send controls are visible; draft was preserved.")
    if first_method == "button":
        buttons[0].click()
    else:
        prompt.press("Enter")

    confirmed = _try_confirm_user_turn(
        page,
        marker=request.request_marker,
        prompt=prompt,
        baseline_turn_ids=baseline_turn_ids,
        baseline_turns=baseline_turns,
        timeout_ms=min(5_000, max(1, int((deadline - time.monotonic()) * 1000))),
    )
    if confirmed is not None:
        return confirmed

    draft_still_present = _matching_draft(_composer_text(prompt), request)
    generating = _visible(page.locator(STOP_SELECTOR))
    history_unchanged = page.locator(TURN_XPATH).count() == baseline_turns
    if not (draft_still_present and not generating and history_unchanged):
        raise BrowserRoundTripUncertain(
            "A submit action changed the composer, generation state, or conversation history, "
            "but no strict new-turn witness was proven. Inspect the Worker chat before any retry."
        )

    if first_method == "button":
        prompt.press("Enter")
    else:
        buttons = _visible_enabled_send(page)
        if len(buttons) != 1:
            raise BrowserRoundTripError(
                "No unique enabled Send control appeared after Enter did nothing. Exact draft preserved."
            )
        buttons[0].click()

    confirmed = _try_confirm_user_turn(
        page,
        marker=request.request_marker,
        prompt=prompt,
        baseline_turn_ids=baseline_turn_ids,
        baseline_turns=baseline_turns,
        timeout_ms=min(30_000, max(1, int((deadline - time.monotonic()) * 1000)),
    )
    if confirmed is not None:
        return confirmed

    draft_still_present = _matching_draft(_composer_text(prompt), request)
    generating = _visible(page.locator(STOP_SELECTOR))
    history_unchanged = page.locator(TURN_XPATH).count() == baseline_turns
    if draft_still_present and not generating and history_unchanged:
        raise BrowserRoundTripError(
            "Neither native submit mechanism activated. The exact draft was preserved."
        )
    raise BrowserRoundTripUncertain(
        "Submission state changed, but a new marker-bearing user turn, increased turn count, "
        "and empty composer were not all proven. Inspect the Worker chat before any retry."
    )


def run_dispatch(request: BrowserRoundTripRequest) -> BrowserDispatchReceipt:
    """Submit one exact Worker wake and return without waiting for Worker output."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise BrowserRoundTripError(
            "Playwright is not installed in this environment. Install the Python package first."
        ) from exc

    timeout_ms = request.timeout_seconds * 1000
    deadline = time.monotonic() + request.timeout_seconds
    playwright = sync_playwright().start()
    page = None
    source_url = ""
    worker_url = ""
    baseline_turns = 0
    baseline_turn_ids: tuple[str, ...] = ()
    submit_attempted = False
    submitted = False

    try:
        browser = playwright.chromium.connect_over_cdp(request.cdp_endpoint)
        page = _require_single_chatgpt_page(browser)
        source_url = request.return_url or normalize_chatgpt_url(page.url)
        worker_url = _resolve_worker_url(
            page,
            request,
            timeout_ms=min(
                timeout_ms,
                120_000,
            ),
        )
        if source_url != worker_url:
            _wait_for_idle_composer(page, timeout_ms=min(timeout_ms, 60_000))

        if normalize_chatgpt_url(page.url) != worker_url:
            page.goto(worker_url, wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_url(worker_url, timeout=timeout_ms)
        prompt, baseline_turns, baseline_turn_ids, reused_draft = _wait_for_dispatch_ready(
            page,
            request,
            worker_url=worker_url,
            timeout_ms=min(timeout_ms, 120_000),
        )

        turns = page.locator(TURN_XPATH)
        if not reused_draft:
            prompt.fill(request.prompt_text)
        if not _matching_draft(_composer_text(prompt), request):
            if not reused_draft:
                prompt.fill("")
            raise BrowserRoundTripError("Composer witness did not contain the exact run markers.")

        time.sleep(0.75)
        if normalize_chatgpt_url(page.url) != worker_url:
            raise BrowserRoundTripError("Worker conversation changed while preparing the prompt.")
        _verify_worker_identity(
            page,
            request,
            worker_url=worker_url,
            timeout_ms=min(timeout_ms, 10_000),
        )
        if turns.count() != baseline_turns or _turn_ids(page) != baseline_turn_ids:
            raise BrowserRoundTripError("Worker conversation history changed before Send. Exact draft preserved.")
        if _visible(page.locator(STOP_SELECTOR)):
            raise BrowserRoundTripError("Worker began generating before Send. Exact draft preserved.")

        submit_attempted = True
        user_turn_id, final_turns = _submit_and_confirm(
            page,
            prompt,
            request,
            deadline=deadline,
            baseline_turn_ids=baseline_turn_ids,
            baseline_turns=baseline_turns,
        )
        submitted = True

        try:
            _return_to_source_conversation(
                page,
                source_url=source_url,
                timeout_ms=min(timeout_ms, 120_000),
            )
            return _receipt(
                request,
                worker_url=worker_url,
                source_url=source_url,
                baseline_turns=baseline_turns,
                final_turns=final_turns,
                user_turn_id=user_turn_id,
                returned_to_source=True,
                return_error=None,
            )
        except Exception as exc:
            return _receipt(
                request,
                worker_url=worker_url,
                source_url=source_url,
                baseline_turns=baseline_turns,
                final_turns=final_turns,
                user_turn_id=user_turn_id,
                returned_to_source=False,
                return_error=str(exc),
            )
    except BrowserRoundTripError:
        raise
    except Exception as exc:
        if submit_attempted and not submitted:
            raise BrowserRoundTripUncertain(
                "A submit action was attempted, but strict dispatch evidence was incomplete. "
                "Inspect the Worker chat before any retry. "
                f"Underlying error: {exc}"
            ) from exc
        if submitted:
            raise BrowserRoundTripUncertain(
                "Submission occurred, but final dispatch evidence was incomplete. "
                "Inspect the Worker chat before any retry. "
                f"Underlying error: {exc}"
            ) from exc
        raise BrowserRoundTripError(str(exc)) from exc
    finally:
        if page is not None and not submit_attempted and source_url:
            try:
                if normalize_chatgpt_url(page.url) != source_url:
                    page.goto(source_url, wait_until="domcontentloaded", timeout=60_000)
            except Exception:
                pass
        playwright.stop()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-url")
    parser.add_argument("--worker-chat-title", required=True)
    parser.add_argument("--project-title", default="Life OS")
    parser.add_argument("--text", required=True)
    parser.add_argument("--request-marker", required=True)
    parser.add_argument("--response-marker", required=True, help="Canonical run ID.")
    parser.add_argument("--cdp-endpoint", default=DEFAULT_CDP_ENDPOINT)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--return-url")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--confirm-send", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.send or args.confirm_send != SEND_CONFIRMATION:
        print(
            f"STOPPED: browser dispatch requires --send --confirm-send {SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2
    try:
        request = BrowserRoundTripRequest(
            worker_url=args.worker_url,
            worker_chat_title=args.worker_chat_title,
            project_title=args.project_title,
            prompt_text=args.text,
            request_marker=args.request_marker,
            response_marker=args.response_marker,
            cdp_endpoint=args.cdp_endpoint,
            timeout_seconds=args.timeout_seconds,
            return_url=args.return_url,
        )
        receipt = run_dispatch(request)
    except BrowserRoundTripUncertain as exc:
        print(f"STOPPED_AFTER_SEND: {exc}", file=sys.stderr)
        return 3
    except BrowserRoundTripError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print("BROWSER_DISPATCH_OK")
    print(f"{RECEIPT_PREFIX}{receipt.to_json()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
