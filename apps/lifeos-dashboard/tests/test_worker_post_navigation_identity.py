import importlib.util
import sys
from pathlib import Path


AUTOMATION = Path(__file__).parents[1] / "automation"
ROUNDTRIP_SCRIPT = AUTOMATION / "chatgpt_worker_browser_roundtrip.py"
ROUNDTRIP_SPEC = importlib.util.spec_from_file_location(
    "chatgpt_worker_browser_roundtrip_identity", ROUNDTRIP_SCRIPT
)
assert ROUNDTRIP_SPEC is not None and ROUNDTRIP_SPEC.loader is not None
roundtrip = importlib.util.module_from_spec(ROUNDTRIP_SPEC)
sys.modules[ROUNDTRIP_SPEC.name] = roundtrip
ROUNDTRIP_SPEC.loader.exec_module(roundtrip)


class ExactWorkerPage:
    def __init__(self, url: str) -> None:
        self.url = url
        self.locator_calls: list[str] = []

    def locator(self, selector: str):
        self.locator_calls.append(selector)
        raise AssertionError(
            "Post-navigation identity verification must not reacquire the sidebar anchor."
        )


def request(worker_url: str | None):
    return roundtrip.BrowserRoundTripRequest(
        worker_url=worker_url,
        worker_chat_title="Engineering_Worker",
        project_title="LifeOS",
        prompt_text="SYNTHETIC_ZERO_AUTHORITY_MARKER",
        request_marker="SYNTHETIC_ZERO_AUTHORITY_MARKER",
        response_marker="UNUSED_RESPONSE_MARKER",
    )


def test_pre_navigation_resolution_uses_registered_url_without_sidebar() -> None:
    worker_url = "https://chatgpt.com/g/project/c/engineering-worker"
    page = ExactWorkerPage("https://chatgpt.com/g/project/c/source")

    resolved = roundtrip._resolve_worker_url(
        page,
        request(worker_url),
        timeout_ms=1_000,
    )

    assert resolved == worker_url
    assert page.locator_calls == []


def test_pre_navigation_resolution_requires_registered_url() -> None:
    page = ExactWorkerPage("https://chatgpt.com/g/project/c/source")

    try:
        roundtrip._resolve_worker_url(
            page,
            request(None),
            timeout_ms=1_000,
        )
    except roundtrip.BrowserRoundTripError as exc:
        assert "registered exact conversation URL" in str(exc)
        assert "Nothing was sent" in str(exc)
    else:
        raise AssertionError("A missing registered Worker URL must fail closed.")

    assert page.locator_calls == []


def test_post_navigation_identity_uses_already_resolved_exact_url() -> None:
    worker_url = "https://chatgpt.com/g/project/c/engineering-worker"
    page = ExactWorkerPage(f"{worker_url}?model=gpt-5")

    roundtrip._verify_worker_identity(
        page,
        request(worker_url),
        worker_url=worker_url,
        timeout_ms=1_000,
    )

    assert page.locator_calls == []


def test_post_navigation_identity_rejects_a_different_active_conversation() -> None:
    worker_url = "https://chatgpt.com/g/project/c/engineering-worker"
    page = ExactWorkerPage("https://chatgpt.com/g/project/c/different-room")

    try:
        roundtrip._verify_worker_identity(
            page,
            request(worker_url),
            worker_url=worker_url,
            timeout_ms=1_000,
        )
    except roundtrip.BrowserRoundTripError as exc:
        assert "Exact Worker conversation URL was not reached" in str(exc)
    else:
        raise AssertionError("A mismatched active conversation URL must fail closed.")

    assert page.locator_calls == []
