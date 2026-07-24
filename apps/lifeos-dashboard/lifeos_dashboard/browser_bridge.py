"""Guarded local Edge CDP bridge launch and dashboard service."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Mapping, Sequence
from urllib.parse import urlsplit

from .command_center import CommandCenterService
from .worker_operations import DEFAULT_CDP_ENDPOINT, browser_health
from .worker_runtime import WorkerRuntimeError

BRIDGE_RECEIPT_PREFIX = "LIFEOS_EDGE_BRIDGE_RECEIPT="
DEFAULT_START_URL = "https://chatgpt.com/"

HealthProbe = Callable[[str], dict[str, object]]
PopenFactory = Callable[..., subprocess.Popen]
Sleep = Callable[[float], None]


def _loopback_port(cdp_endpoint: str) -> int:
    parsed = urlsplit(str(cdp_endpoint or "").strip())
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise WorkerRuntimeError(
            "Browser bridge launch requires a local http loopback CDP endpoint."
        )
    try:
        port = parsed.port
    except ValueError as exc:
        raise WorkerRuntimeError("Browser bridge CDP port is invalid.") from exc
    if port is None or port < 1 or port > 65535:
        raise WorkerRuntimeError("Browser bridge CDP endpoint must include a valid port.")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise WorkerRuntimeError("Browser bridge CDP endpoint must not include a path or query.")
    return port


def _edge_candidates(configured: str | None = None) -> list[Path]:
    values: list[Path] = []
    explicit = configured or os.getenv("LIFEOS_EDGE_EXECUTABLE")
    if explicit:
        values.append(Path(explicit).expanduser())

    for variable in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
        root = os.getenv(variable)
        if root:
            values.append(
                Path(root) / "Microsoft" / "Edge" / "Application" / "msedge.exe"
            )

    for command in ("msedge.exe", "msedge"):
        resolved = shutil.which(command)
        if resolved:
            values.append(Path(resolved))

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in values:
        key = str(candidate).casefold()
        if key not in seen:
            unique.append(candidate)
            seen.add(key)
    return unique


def resolve_edge_executable(configured: str | None = None) -> Path:
    for candidate in _edge_candidates(configured):
        if candidate.is_file():
            return candidate.resolve()
    raise WorkerRuntimeError(
        "Microsoft Edge was not found. Set LIFEOS_EDGE_EXECUTABLE to msedge.exe."
    )


def _creation_flags() -> int:
    if os.name != "nt":
        return 0
    return int(
        getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        | getattr(subprocess, "DETACHED_PROCESS", 0)
    )


def launch_edge_bridge(
    *,
    app_root: Path,
    cdp_endpoint: str = DEFAULT_CDP_ENDPOINT,
    timeout_seconds: int = 20,
    edge_executable: str | None = None,
    user_data_dir: Path | None = None,
    start_url: str | None = None,
    health_probe: HealthProbe = browser_health,
    popen_factory: PopenFactory = subprocess.Popen,
    sleep: Sleep = time.sleep,
) -> dict[str, object]:
    """Start one dedicated Edge CDP profile and verify its loopback endpoint."""

    if timeout_seconds < 5 or timeout_seconds > 60:
        raise WorkerRuntimeError("Bridge timeout must be between 5 and 60 seconds.")
    port = _loopback_port(cdp_endpoint)
    before = health_probe(cdp_endpoint)
    if before.get("available") is True:
        return {
            "status": "ready",
            "started": False,
            "endpoint": cdp_endpoint,
            "browser": before.get("browser"),
            "reason": "Browser bridge was already ready; no Edge process was launched.",
        }

    executable = resolve_edge_executable(edge_executable)
    configured_profile = os.getenv("LIFEOS_EDGE_CDP_USER_DATA_DIR")
    profile = user_data_dir or (
        Path(configured_profile).expanduser()
        if configured_profile
        else app_root / ".local" / "edge-cdp-profile"
    )
    profile = Path(profile).expanduser().resolve()
    profile.mkdir(parents=True, exist_ok=True)

    target_url = str(
        start_url or os.getenv("LIFEOS_EDGE_CDP_START_URL") or DEFAULT_START_URL
    ).strip()
    if urlsplit(target_url).scheme != "https":
        raise WorkerRuntimeError("Browser bridge start URL must use https.")

    command = [
        str(executable),
        "--remote-debugging-address=127.0.0.1",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        target_url,
    ]
    try:
        process = popen_factory(
            command,
            cwd=app_root,
            env=os.environ.copy(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=_creation_flags(),
        )
    except OSError as exc:
        raise WorkerRuntimeError(f"Microsoft Edge could not be launched: {exc}") from exc

    deadline = time.monotonic() + timeout_seconds
    last_health: Mapping[str, object] = before
    while time.monotonic() < deadline:
        last_health = health_probe(cdp_endpoint)
        if last_health.get("available") is True:
            return {
                "status": "ready",
                "started": True,
                "endpoint": cdp_endpoint,
                "browser": last_health.get("browser"),
                "pid": getattr(process, "pid", None),
                "reason": "Dedicated Edge CDP bridge launched and verified.",
            }
        poll = getattr(process, "poll", None)
        if callable(poll) and poll() is not None:
            break
        sleep(0.25)

    detail = str(last_health.get("reason") or "CDP endpoint did not become ready.")
    raise WorkerRuntimeError(
        f"Edge launched, but the browser bridge was not verified: {detail}"
    )


def parse_bridge_receipt(stdout: str) -> dict[str, object]:
    lines = [
        line.removeprefix(BRIDGE_RECEIPT_PREFIX)
        for line in (stdout or "").splitlines()
        if line.startswith(BRIDGE_RECEIPT_PREFIX)
    ]
    if len(lines) != 1:
        raise WorkerRuntimeError(
            "Browser bridge launcher did not emit exactly one machine-readable receipt."
        )
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise WorkerRuntimeError("Browser bridge launcher receipt is not valid JSON.") from exc
    if not isinstance(payload, dict) or payload.get("status") != "ready":
        raise WorkerRuntimeError("Browser bridge launcher did not verify a ready endpoint.")
    return payload


class BrowserBridgeService:
    """Run the local launcher under the dashboard's shared execution gate."""

    def __init__(
        self,
        command_center: CommandCenterService,
        app_root: Path,
        *,
        cdp_endpoint: str = DEFAULT_CDP_ENDPOINT,
    ) -> None:
        self.command_center = command_center
        self.app_root = Path(app_root).resolve()
        self.cdp_endpoint = cdp_endpoint

    def reconnect(
        self,
        *,
        confirm_launch: bool,
        timeout_seconds: int = 20,
    ) -> dict[str, object]:
        if not confirm_launch:
            raise WorkerRuntimeError("Browser bridge reconnect requires explicit confirmation.")
        if timeout_seconds < 5 or timeout_seconds > 60:
            raise WorkerRuntimeError("Bridge timeout must be between 5 and 60 seconds.")
        if self.command_center.running:
            raise WorkerRuntimeError(
                "Another automation job is running. Reconnect the bridge after it finishes."
            )
        run_lock = self.command_center._run_lock  # noqa: SLF001 - shared local action gate
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError(
                "Another automation job is running. Reconnect the bridge after it finishes."
            )
        try:
            command = [
                sys.executable,
                str(self.app_root / "automation" / "reconnect_edge_cdp_bridge.py"),
                "--cdp-endpoint",
                self.cdp_endpoint,
                "--timeout-seconds",
                str(timeout_seconds),
            ]
            completed = subprocess.run(
                command,
                cwd=self.app_root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                timeout=timeout_seconds + 10,
                check=False,
            )
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout).strip()
                raise WorkerRuntimeError(detail or "Browser bridge reconnect failed.")
            return parse_bridge_receipt(completed.stdout)
        except subprocess.TimeoutExpired as exc:
            raise WorkerRuntimeError("Browser bridge reconnect timed out.") from exc
        finally:
            run_lock.release()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconnect the local Edge CDP bridge.")
    parser.add_argument(
        "--cdp-endpoint",
        default=os.getenv("LIFEOS_CHATGPT_CDP_ENDPOINT", DEFAULT_CDP_ENDPOINT),
    )
    parser.add_argument("--timeout-seconds", type=int, default=20)
    parser.add_argument("--edge-executable", default=None)
    parser.add_argument("--user-data-dir", type=Path, default=None)
    parser.add_argument("--start-url", default=None)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    app_root = Path(__file__).resolve().parents[1]
    try:
        receipt = launch_edge_bridge(
            app_root=app_root,
            cdp_endpoint=args.cdp_endpoint,
            timeout_seconds=args.timeout_seconds,
            edge_executable=args.edge_executable,
            user_data_dir=args.user_data_dir,
            start_url=args.start_url,
        )
    except WorkerRuntimeError as exc:
        print(f"STOPPED: {exc}", file=sys.stderr)
        return 2
    print(BRIDGE_RECEIPT_PREFIX + json.dumps(receipt, sort_keys=True))
    return 0


__all__ = [
    "BRIDGE_RECEIPT_PREFIX",
    "BrowserBridgeService",
    "launch_edge_bridge",
    "main",
    "parse_bridge_receipt",
    "resolve_edge_executable",
]
