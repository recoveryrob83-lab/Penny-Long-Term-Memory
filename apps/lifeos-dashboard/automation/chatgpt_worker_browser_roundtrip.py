"""Bounded one-tab ChatGPT Worker round-trip transport over an existing Edge CDP session.

This module is transport infrastructure only. It does not create authority, interpret work,
change advisory lifecycle, update databases, or close records. It borrows one already-open
ChatGPT tab, sends one explicitly confirmed prompt to one exact Worker conversation, captures
one run-correlated assistant response, and returns the tab to its original conversation.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from urllib.parse import urlsplit, urlunsplit

DEFAULT_CDP_ENDPOINT = "http://127.0.0.1:9222"
SEND_CONFIRMATION = "SEND"
RECEIPT_PREFIX = "LIFEOS_BROWSER_ROUNDTRIP_RECEIPT="
PROMPT_SELECTOR = "#prompt-textarea"
SEND_SELECTOR = 'button[data-testid="send-button"]'
STOP_SELECTOR = 'button[data-testid="stop-button"]'
TURN_XPATH = "xpath=//*[@data-testid and starts-with(@data-testid,'conversation-turn-')]"
WORKER_READY_STABLE_SECONDS = 4.0
WORKER_READY_POLL_SECONDS = 0.5


class BrowserRoundTripError(RuntimeError):
    """Raised when the browser transport cannot prove a safe, exact round trip."""


class BrowserRoundTripUncertain(BrowserRoundTripError):
    """Raised after submission when response capture is uncertain and retry is unsafe."""


@dataclass(frozen=True)
class BrowserRoundTripRequest:
    worker_chat_title: str
    project_title: str
    prompt_text: str
    request_marker: str
    response_marker: str
    worker_url: str | None = None
    cdp_endpoint: str = DEFAULT_CDP_ENDPOINT
    timeout_seconds: int = 300
    return_url: str | None = None

    def __post_init__(self) -> None:
        if self.worker_url is not None:
            object.__setattr__(self, "worker_url", normalize_chatgpt_url(self.worker_url))
        if self.return_url is not None:
            object.__setattr__(self, "return_url", normalize_chatgpt_url(self.return_url))
        for field_name in (
            "worker_chat_title",
            "project_title",
            "prompt_text",
            "request_marker",
            "response_marker",
            "cdp_endpoint",
        ):
            if not str(getattr(self, field_name)).strip():
                raise BrowserRoundTripError(f"{field_name} cannot be empty.")
        if self.request_marker not in self.prompt_text:
            raise BrowserRoundTripError("request_marker must appear in prompt_text.")
        if self.timeout_seconds < 30 or self.timeout_seconds > 900:
            raise BrowserRoundTripError("timeout_seconds must be between 30 and 900.")


@dataclass(frozen=True)
class BrowserRoundTripReceipt:
    status: str
    worker_url: str
    return_url: str
    request_marker: str
    response_marker: str
    baseline_turns: int
    final_turns: int | None
    user_turn_id: str | None
    assistant_turn_id: str | None
    response_text: str
    returned_to_source: bool
    submission_uncertain: bool

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)


def normalize_chatgpt_url(value: str) -> str:
    """Return one canonical absolute ChatGPT conversation URL."""

    clean = value.strip()
    parsed = urlsplit(clean)
    if parsed.scheme != "https" or parsed.hostname != "chatgpt.com":
        raise BrowserRoundTripError("Only https://chatgpt.com conversation URLs are allowed.")
    path = parsed.path.rstrip("/")
    if "/c/" not in path:
        raise BrowserRoundTripError("URL must identify one ChatGPT conversation.")
    return urlunsplit(("https", "chatgpt.com", path, "", ""))


def _visible(locator) -> bool:
    try:
        return locator.count() > 0 and locator.first.is_visible()
    except Exception:
        return False


def _composer_text(prompt) -> str:
    return str(
        prompt.evaluate(
            "element => ('value' in element ? element.value : "
            "element.innerText || element.textContent || '')"
        )
    ).strip()


def _chatgpt_pages(browser) -> list:
    pages = [page for context in browser.contexts for page in context.pages]
    return [page for page in pages if urlsplit(page.url).hostname == "chatgpt.com"]


def _require_single_chatgpt_page(browser):
    pages = _chatgpt_pages(browser)
    if len(pages) != 1:
        raise BrowserRoundTripError(
            "Expected exactly one attached ChatGPT tab; "
            f"found {len(pages)}. Close extra ChatGPT tabs before retrying."
        )
    return pages[0]


def _wait_for_idle_composer(page, *, timeout_ms: int):
    prompt = page.locator(PROMPT_SELECTOR)
    prompt.wait_for(state="visible", timeout=timeout_ms)
    if prompt.count() != 1:
        raise BrowserRoundTripError(f"Expected one composer; found {prompt.count()}.")
    if _visible(page.locator(STOP_SELECTOR)):
        raise BrowserRoundTripError("ChatGPT is generating. Wait for it to finish before running.")
    if _composer_text(prompt):
        raise BrowserRoundTripError("Composer contains an unsent draft. It was preserved.")
    return prompt


def _worker_link(page, request: BrowserRoundTripRequest, *, timeout_ms: int):
    label = f"{request.worker_chat_title}, chat in project {request.project_title}"
    worker_link = page.locator(f'a[aria-label={json.dumps(label)}]')
    worker_link.wait_for(state="attached", timeout=timeout_ms)
    if worker_link.count() != 1:
        raise BrowserRoundTripError(
            "Expected exactly one exact Worker sidebar link; "
            f"found {worker_link.count()}."
        )
    return worker_link


def _resolve_worker_url(page, request: BrowserRoundTripRequest, *, timeout_ms: int) -> str:
    worker_link = _worker_link(page, request, timeout_ms=timeout_ms)
    observed = normalize_chatgpt_url(str(worker_link.evaluate("element => element.href")))
    if request.worker_url is not None and observed != request.worker_url:
        raise BrowserRoundTripError("Worker sidebar link points to an unexpected conversation.")
    return request.worker_url or observed


def _verify_worker_identity(
    page,
    request: BrowserRoundTripRequest,
    *,
    worker_url: str,
    timeout_ms: int,
) -> None:
    if normalize_chatgpt_url(page.url) != worker_url:
        raise BrowserRoundTripError("Exact Worker conversation URL was not reached.")
    worker_link = _worker_link(page, request, timeout_ms=timeout_ms)
    absolute_href = normalize_chatgpt_url(str(worker_link.evaluate("element => element.href")))
    if absolute_href != worker_url:
        raise BrowserRoundTripError("Worker sidebar link points to an unexpected conversation.")


def _worker_history_snapshot(page) -> tuple[int, str, str]:
    """Return a stable identity witness for the currently rendered conversation history."""

    try:
        turns = page.locator(TURN_XPATH)
        count = turns.count()
        if count < 1:
            return (count, "", "")
        last_turn = turns.last
        if not last_turn.is_visible():
            return (count, "", "")
        turn_id = str(last_turn.get_attribute("data-testid") or "")
        text = " ".join(last_turn.inner_text().split())
        return (count, turn_id, text)
    except Exception:
        return (0, "", "")


def _wait_for_worker_conversation_ready(
    page,
    request: BrowserRoundTripRequest,
    *,
    worker_url: str,
    timeout_ms: int,
    stable_seconds: float = WORKER_READY_STABLE_SECONDS,
):
    """Wait for the exact Worker room, history, and composer to finish hydrating."""

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
            if _composer_text(prompt):
                raise BrowserRoundTripError(
                    "Worker composer contains an unsent draft. It was preserved."
                )

            ready_state = str(page.evaluate("document.readyState"))
            snapshot = _worker_history_snapshot(page)
            history_ready = snapshot[0] >= 1 and bool(snapshot[1] and snapshot[2])
            if ready_state == "complete" and history_ready:
                if snapshot == last_snapshot:
                    if stable_since is None:
                        stable_since = time.monotonic()
                    if time.monotonic() - stable_since >= stable_seconds:
                        remaining_ms = max(
                            1, min(10_000, int((deadline - time.monotonic()) * 1000))
                        )
                        _verify_worker_identity(
                            page,
                            request,
                            worker_url=worker_url,
                            timeout_ms=remaining_ms,
                        )
                        return prompt, snapshot[0]
                else:
                    last_snapshot = snapshot
                    stable_since = None
                last_observation = (
                    f"Worker history is present but not stable yet: {snapshot[0]} turns."
                )
            else:
                last_snapshot = None
                stable_since = None
                last_observation = (
                    f"Worker room not hydrated: readyState={ready_state}, "
                    f"turns={snapshot[0]}."
                )
        except BrowserRoundTripError as exc:
            if "unsent draft" in str(exc):
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


def _turn_for_role_marker(page, *, role: str, marker: str, timeout_ms: int):
    role_node = page.locator(f'[data-message-author-role="{role}"]').filter(has_text=marker).last
    role_node.wait_for(state="visible", timeout=timeout_ms)
    turn = role_node.locator(
        "xpath=ancestor::*[starts-with(@data-testid,'conversation-turn-')][1]"
    )
    turn.wait_for(state="visible", timeout=timeout_ms)
    return turn


def _wait_for_stable_turn(page, turn, *, deadline: float, stable_seconds: float = 2.0) -> str:
    last_text = ""
    stable_since: float | None = None
    while time.monotonic() < deadline:
        text = " ".join(turn.inner_text().split())
        if text and text == last_text:
            if stable_since is None:
                stable_since = time.monotonic()
            if time.monotonic() - stable_since >= stable_seconds and not _visible(
                page.locator(STOP_SELECTOR)
            ):
                return text
        else:
            last_text = text
            stable_since = None
        time.sleep(0.5)
    raise BrowserRoundTripUncertain(
        "Worker response appeared but did not become stably capturable before timeout. "
        "The Worker tab was left open; inspect it before any retry."
    )


def run_round_trip(request: BrowserRoundTripRequest) -> BrowserRoundTripReceipt:
    """Execute one confirmed one-tab browser round trip and return run-linked evidence."""

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
    sent = False
    captured = False
    returned = False
    user_turn_id: str | None = None
    assistant_turn_id: str | None = None
    response_text = ""
    final_turns: int | None = None

    try:
        browser = playwright.chromium.connect_over_cdp(request.cdp_endpoint)
        page = _require_single_chatgpt_page(browser)
        source_url = request.return_url or normalize_chatgpt_url(page.url)
        source_prompt = _wait_for_idle_composer(page, timeout_ms=min(timeout_ms, 60_000))
        del source_prompt
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

        remaining_ms = max(1, int((deadline - time.monotonic()) * 1000))
        user_turn = _turn_for_role_marker(
            page,
            role="user",
            marker=request.request_marker,
            timeout_ms=remaining_ms,
        )
        user_turn_id = user_turn.get_attribute("data-testid")

        remaining_ms = max(1, int((deadline - time.monotonic()) * 1000))
        assistant_turn = _turn_for_role_marker(
            page,
            role="assistant",
            marker=request.response_marker,
            timeout_ms=remaining_ms,
        )
        assistant_turn_id = assistant_turn.get_attribute("data-testid")
        response_text = _wait_for_stable_turn(page, assistant_turn, deadline=deadline)
        if request.response_marker not in response_text:
            raise BrowserRoundTripUncertain(
                "Captured assistant response lost the expected response marker. "
                "Inspect the Worker tab before any retry."
            )
        if turns.count() < baseline_turns + 2:
            raise BrowserRoundTripUncertain(
                "Expected new user and assistant turns were not both present. "
                "Inspect the Worker tab before any retry."
            )
        final_turns = turns.count()
        captured = True

        if normalize_chatgpt_url(page.url) != source_url:
            page.goto(source_url, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_url(source_url, timeout=timeout_ms)
        _wait_for_idle_composer(page, timeout_ms=min(timeout_ms, 120_000))
        returned = True

        return BrowserRoundTripReceipt(
            status="succeeded",
            worker_url=worker_url,
            return_url=source_url,
            request_marker=request.request_marker,
            response_marker=request.response_marker,
            baseline_turns=baseline_turns,
            final_turns=final_turns,
            user_turn_id=user_turn_id,
            assistant_turn_id=assistant_turn_id,
            response_text=response_text,
            returned_to_source=returned,
            submission_uncertain=False,
        )
    except BrowserRoundTripError:
        raise
    except Exception as exc:
        if sent and not captured:
            raise BrowserRoundTripUncertain(
                "Submission occurred, but the Worker response was not safely captured. "
                "The Worker tab was left open; inspect it before any retry. "
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
    parser.add_argument("--response-marker", required=True)
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
            f"STOPPED: browser round trip requires --send --confirm-send {SEND_CONFIRMATION}.",
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
        receipt = run_round_trip(request)
    except BrowserRoundTripUncertain as exc:
        print(f"STOPPED_AFTER_SEND: {exc}", file=sys.stderr)
        return 3
    except BrowserRoundTripError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print("BROWSER_ROUNDTRIP_OK")
    print(f"{RECEIPT_PREFIX}{receipt.to_json()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
