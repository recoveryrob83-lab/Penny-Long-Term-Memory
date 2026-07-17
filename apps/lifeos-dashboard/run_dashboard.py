"""Launch the LifeOS dashboard on localhost."""

from __future__ import annotations

import os
import threading
import time
import webbrowser

import uvicorn

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def _open_browser_later(url: str) -> None:
    time.sleep(1.0)
    webbrowser.open(url)


def main() -> None:
    host = os.getenv("LIFEOS_HOST", DEFAULT_HOST)
    if host not in {"127.0.0.1", "localhost"}:
        raise SystemExit(
            "LifeOS Dashboard binds only to localhost by default. "
            "Set LIFEOS_HOST to 127.0.0.1 or localhost."
        )

    try:
        port = int(os.getenv("LIFEOS_PORT", str(DEFAULT_PORT)))
    except ValueError as error:
        raise SystemExit("LIFEOS_PORT must be an integer.") from error

    url = f"http://{host}:{port}"
    should_open = os.getenv("LIFEOS_OPEN_BROWSER", "1").lower() not in {
        "0",
        "false",
        "no",
    }
    if should_open:
        threading.Thread(target=_open_browser_later, args=(url,), daemon=True).start()

    uvicorn.run(
        "lifeos_dashboard.main:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
