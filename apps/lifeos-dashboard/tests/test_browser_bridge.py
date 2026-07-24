from __future__ import annotations

import json
import subprocess
import threading
from pathlib import Path

import pytest

from lifeos_dashboard import browser_bridge
from lifeos_dashboard.browser_bridge import (
    BRIDGE_RECEIPT_PREFIX,
    BrowserBridgeService,
    launch_edge_bridge,
    parse_bridge_receipt,
)
from lifeos_dashboard.worker_runtime import WorkerRuntimeError


class FakeProcess:
    pid = 4242

    def poll(self) -> None:
        return None


def test_launch_returns_without_duplicate_when_bridge_is_ready(tmp_path: Path) -> None:
    def fail_popen(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("Edge should not launch when CDP is already ready.")

    result = launch_edge_bridge(
        app_root=tmp_path,
        health_probe=lambda endpoint: {
            "available": True,
            "endpoint": endpoint,
            "browser": "Edg/1",
            "reason": "ready",
        },
        popen_factory=fail_popen,
    )

    assert result["status"] == "ready"
    assert result["started"] is False


def test_launch_uses_dedicated_profile_and_verifies_endpoint(tmp_path: Path) -> None:
    edge = tmp_path / "msedge.exe"
    edge.write_text("stub", encoding="utf-8")
    calls: list[list[str]] = []
    health_results = iter(
        [
            {"available": False, "reason": "offline"},
            {"available": True, "browser": "Edg/1", "reason": "ready"},
        ]
    )

    def fake_popen(command, **kwargs):  # noqa: ANN001
        calls.append(list(command))
        assert kwargs["cwd"] == tmp_path
        return FakeProcess()

    result = launch_edge_bridge(
        app_root=tmp_path,
        edge_executable=str(edge),
        health_probe=lambda endpoint: next(health_results),
        popen_factory=fake_popen,
        sleep=lambda seconds: None,
    )

    assert result["status"] == "ready"
    assert result["started"] is True
    assert result["pid"] == 4242
    assert len(calls) == 1
    command = calls[0]
    assert "--remote-debugging-address=127.0.0.1" in command
    assert "--remote-debugging-port=9222" in command
    assert f"--user-data-dir={tmp_path / '.local' / 'edge-cdp-profile'}" in command
    assert command[-1] == "https://chatgpt.com/"


def test_launch_rejects_non_loopback_endpoint(tmp_path: Path) -> None:
    with pytest.raises(WorkerRuntimeError, match="loopback"):
        launch_edge_bridge(
            app_root=tmp_path,
            cdp_endpoint="http://192.168.1.5:9222",
        )


def test_parse_bridge_receipt_requires_one_verified_receipt() -> None:
    receipt = {"status": "ready", "started": True, "endpoint": "http://127.0.0.1:9222"}

    assert parse_bridge_receipt(
        BRIDGE_RECEIPT_PREFIX + json.dumps(receipt)
    ) == receipt

    with pytest.raises(WorkerRuntimeError, match="exactly one"):
        parse_bridge_receipt("")


class FakeCommandCenter:
    def __init__(self) -> None:
        self.running = False
        self._run_lock = threading.Lock()


def test_service_calls_launcher_under_shared_lock(monkeypatch, tmp_path: Path) -> None:
    center = FakeCommandCenter()
    service = BrowserBridgeService(center, tmp_path)
    observed: dict[str, object] = {}

    def fake_run(command, **kwargs):  # noqa: ANN001
        observed["command"] = command
        observed["locked"] = center._run_lock.locked()
        receipt = {"status": "ready", "started": True, "endpoint": service.cdp_endpoint}
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=BRIDGE_RECEIPT_PREFIX + json.dumps(receipt),
            stderr="",
        )

    monkeypatch.setattr(browser_bridge.subprocess, "run", fake_run)

    result = service.reconnect(confirm_launch=True, timeout_seconds=20)

    assert result["status"] == "ready"
    assert observed["locked"] is True
    assert str(tmp_path / "automation" / "reconnect_edge_cdp_bridge.py") in observed["command"]
    assert center._run_lock.locked() is False


def test_service_refuses_when_execution_lock_is_busy(tmp_path: Path) -> None:
    center = FakeCommandCenter()
    center._run_lock.acquire()
    service = BrowserBridgeService(center, tmp_path)

    try:
        with pytest.raises(WorkerRuntimeError, match="Another automation job"):
            service.reconnect(confirm_launch=True)
    finally:
        center._run_lock.release()
