"""Dispatch one bounded Worker wake through an existing one-tab Edge CDP session.

This module is transport infrastructure only. It does not create authority, interpret work,
wait for Worker completion, capture assistant responses, change advisory lifecycle, update
databases, or close records. It borrows one already-open ChatGPT tab, sends one explicitly
confirmed prompt to one exact Worker conversation, proves the correlated user turn exists,
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
    SEND_CONFIRMATION,
    SEND_SELECTOR,
    STOP_SELECTOR,
    TURN_XPATH,
    BrowserRoundTripError,
    BrowserRoundTripRequest,
    BrowserRoundTripUncertain,
    _composer_text,
    _require_single_chatgpt_page,
    _resolve_worker_url,
    _turn_for_role_marker,
    _verify_worker_identity,
    _visible,
    _wait_for_idle_composer,
    _wait_for_worker_conversation_ready,
    normalize_chatgpt_url,
)

RECEIPT_PREFIX = "LIFEOS_BROWSER_DISPATCH_RECEIPT="


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
    final_turns = 0
    sent = False
    submission_confirmed = False
    user_turn_id = ""

    try:
        browser = playwright.chromium.connect_over_cdp(request.cdp_endpoint)
        page = _require_single_chatgpt_page(browser)
        source_url = request.return_url or normalize_chatgpt_url(page.url)
        _wait_for_idle_composer(page, timeout_ms=min(timeout_ms, 60_000))
        worker_url = _resolve_worker_url(
            page,
            request,
            timeout_ms=min(timeout_ms, 120_000),
        )

        if normalize_chatgpt_url(page.url) != worker_url:
            page.goto(worker_url, wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_url(worker_url, timeout=timeout_ms)
        prompt, baseline_turns = _wait_for_worker_conversation_ready(
            page,
            request,
            worker_url=worker_url,
            timeout_ms=min(timeout_ms, 120_000),
        )

        turns = page.locator(TURN_XPATH)
        prompt.fill(request.prompt_text)
        if request.request_marker not in _composer_text(prompt):
            prompt.fill("")
            raise BrowserRoundTripError(
                "Composer witness did not contain the request marker. Draft was cleared."
            )

        time.sleep(0.75)
        if normalize_chatgpt_url(page.url) != worker_url:
            prompt.fill("")
            raise BrowserRoundTripError(
                "Worker conversation changed while preparing the prompt. Draft was cleared."
            )
        _verify_worker_identity(
            page,
            request,
            worker_url=worker_url,
            timeout_ms=min(timeout_ms, 10_000),
        )
        if turns.count() != baseline_turns:
            prompt.fill("")
            raise BrowserRoundTripError(
                "Worker conversation history changed before Send. Draft was cleared; nothing was sent."
            )
        if _visible(page.locator(STOP_SELECTOR)):
            prompt.fill("")
            raise BrowserRoundTripError(
                "Worker began generating before Send. Draft was cleared; nothing was sent."
            )
        if request.request_marker not in _composer_text(prompt):
            prompt.fill("")
            raise BrowserRoundTripError(
                "Composer witness changed before Send. Draft was cleared; nothing was sent."
            )

        send = page.locator(SEND_SELECTOR)
        send.wait_for(state="visible", timeout=min(timeout_ms, 15_000))
        if send.count() != 1 or not send.is_enabled():
            prompt.fill("")
            raise BrowserRoundTripError(
                "Unique enabled send button was not available. Draft was cleared."
            )
        send.click()
        sent = True

        remaining_ms = max(
            1,
            min(30_000, int((deadline - time.monotonic()) * 1000)),
        )
        user_turn = _turn_for_role_marker(
            page,
            role="user",
            marker=request.request_marker,
            timeout_ms=remaining_ms,
        )
        user_turn_id = str(user_turn.get_attribute("data-testid") or "")
        if not user_turn_id:
            raise BrowserRoundTripUncertain(
                "Submission occurred, but the correlated user turn had no stable turn ID. "
                "Inspect the Worker chat before any retry."
            )
        final_turns = turns.count()
        if final_turns < baseline_turns + 1:
            raise BrowserRoundTripUncertain(
                "Submission occurred, but the correlated user turn was not preserved in history. "
                "Inspect the Worker chat before any retry."
            )
        submission_confirmed = True

        try:
            if normalize_chatgpt_url(page.url) != source_url:
                page.goto(source_url, wait_until="domcontentloaded", timeout=timeout_ms)
                page.wait_for_url(source_url, timeout=timeout_ms)
            _wait_for_idle_composer(page, timeout_ms=min(timeout_ms, 120_000))
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
            # The correlated user turn is already confirmed. Preserve a successful send state
            # so idempotency blocks a duplicate, while recording the failed HQ return.
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
        if sent and not submission_confirmed:
            raise BrowserRoundTripUncertain(
                "Submission may have occurred, but the correlated user turn was not safely proven. "
                "Inspect the Worker chat before any retry. "
                f"Underlying error: {exc}"
            ) from exc
        raise BrowserRoundTripError(str(exc)) from exc
    finally:
        if page is not None and not sent and source_url:
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
