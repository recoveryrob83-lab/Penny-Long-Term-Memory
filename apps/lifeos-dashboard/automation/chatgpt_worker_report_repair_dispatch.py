"""Dispatch one correction-only Worker wake with durable stale-draft proof.

This entrypoint reuses the standard one-tab Worker dispatch implementation. It only
adds permission to clear one exact stale LifeOS draft whose wrapper and run IDs were
proven by the authoritative execution row before this process was launched.
"""
from __future__ import annotations

import argparse
import sys

import chatgpt_worker_browser_dispatch as browser_dispatch
from chatgpt_worker_browser_roundtrip import (
    DEFAULT_CDP_ENDPOINT,
    SEND_CONFIRMATION,
    BrowserRoundTripError,
    BrowserRoundTripRequest,
    BrowserRoundTripUncertain,
)

RECEIPT_PREFIX = browser_dispatch.RECEIPT_PREFIX


def _install_trusted_stale_clear(*, wrapper_id: str, run_id: str) -> None:
    clean_wrapper = str(wrapper_id or "").strip()
    clean_run = str(run_id or "").strip()
    if not clean_wrapper or not clean_run:
        raise BrowserRoundTripError("Trusted stale-draft markers cannot be empty.")

    original_prepare = browser_dispatch._prepare_existing_draft

    def prepare_existing_draft(page, prompt, request: BrowserRoundTripRequest):
        draft = browser_dispatch._composer_text(prompt)
        markers = browser_dispatch._lifeos_draft_markers(draft)
        if markers != (clean_wrapper, clean_run):
            return original_prepare(page, prompt, request)

        prompt.fill("")
        if browser_dispatch._composer_text(prompt):
            raise BrowserRoundTripError(
                "Durably proven stale LifeOS composer residue could not be cleared. "
                "Nothing was sent."
            )
        return False

    browser_dispatch._prepare_existing_draft = prepare_existing_draft


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-url")
    parser.add_argument("--worker-chat-title", required=True)
    parser.add_argument("--project-title", default="LifeOS")
    parser.add_argument("--text", required=True)
    parser.add_argument("--request-marker", required=True)
    parser.add_argument("--response-marker", required=True, help="Canonical run ID.")
    parser.add_argument("--trusted-stale-wrapper-id", required=True)
    parser.add_argument("--trusted-stale-run-id", required=True)
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
            f"STOPPED: report repair dispatch requires --send --confirm-send {SEND_CONFIRMATION}.",
            file=sys.stderr,
        )
        return 2

    try:
        _install_trusted_stale_clear(
            wrapper_id=args.trusted_stale_wrapper_id,
            run_id=args.trusted_stale_run_id,
        )
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
        receipt = browser_dispatch.run_dispatch(request)
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
