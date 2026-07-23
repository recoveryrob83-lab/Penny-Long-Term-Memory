"""Safe capture, rollover, and canary promotion for Worker conversation routes."""
from __future__ import annotations

import json
import sqlite3
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Callable, Mapping

from .command_center import CommandCenterService
from .worker_operations import DEFAULT_CDP_ENDPOINT, WorkerOperationsService
from .worker_runtime import WorkerRegistryEntry, WorkerRuntimeError, _conversation_url
from .worker_runtime_service import WorkerRuntimeService

ENGINEERING_CANARY_WORKER_ID = "engineering_worker"


@dataclass(frozen=True)
class WorkerRouteWitness:
    """Exact registered route observed immediately before a zero-authority canary."""

    worker_id: str
    conversation_url: str
    route_revision: int


@dataclass(frozen=True)
class CapturedConversation:
    """One normalized ChatGPT conversation target observed through local CDP."""

    url: str
    title: str


CaptureConversation = Callable[[str], CapturedConversation]


def capture_chatgpt_conversation(cdp_endpoint: str) -> CapturedConversation:
    """Read exactly one ChatGPT conversation page from the local CDP target list."""

    target_url = cdp_endpoint.rstrip("/") + "/json/list"
    try:
        with urllib.request.urlopen(target_url, timeout=2.0) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise WorkerRuntimeError(
            f"Could not read the local browser target list: {exc}"
        ) from exc

    if not isinstance(payload, list):
        raise WorkerRuntimeError("The local browser target list has the wrong shape.")

    candidates: dict[str, str] = {}
    for item in payload:
        if not isinstance(item, dict) or str(item.get("type") or "") != "page":
            continue
        try:
            normalized = _conversation_url(item.get("url"))
        except WorkerRuntimeError:
            continue
        if normalized is not None:
            candidates[normalized] = str(item.get("title") or "").strip()

    if len(candidates) != 1:
        raise WorkerRuntimeError(
            "Route capture requires exactly one open ChatGPT conversation tab; "
            f"found {len(candidates)}. Nothing was changed."
        )
    url, title = next(iter(candidates.items()))
    if not title:
        raise WorkerRuntimeError(
            "The open ChatGPT conversation has no readable browser title. Nothing was changed."
        )
    return CapturedConversation(url=url, title=title)


class WorkerRouteManager:
    """Manage one authoritative route per existing Worker without creating new identity rows."""

    def __init__(
        self,
        command_center: CommandCenterService,
        *,
        cdp_endpoint: str = DEFAULT_CDP_ENDPOINT,
        capture_conversation: CaptureConversation | None = None,
    ) -> None:
        self.command_center = command_center
        self.database_path = Path(command_center.store.database_path)
        self.runtime = WorkerRuntimeService(self.database_path)
        self.cdp_endpoint = cdp_endpoint
        self._capture_conversation = capture_conversation or capture_chatgpt_conversation

    def _route_payload(self, entry: WorkerRegistryEntry) -> dict[str, object]:
        route = self.runtime.store.route_state(entry.worker_id)
        return {
            **entry.to_dict(),
            "route": asdict(route) if route is not None else {
                "worker_id": entry.worker_id,
                "availability": "unknown",
                "last_seen_at": None,
                "pause_reason": None,
            },
        }

    def capture_active_route(
        self,
        worker_id: str,
        *,
        expected_route_revision: int,
        confirm_capture: bool,
    ) -> dict[str, object]:
        """Capture the sole ChatGPT conversation and hold a changed route for canary verification."""

        clean_worker_id = str(worker_id or "").strip()
        if not clean_worker_id:
            raise WorkerRuntimeError("worker_id cannot be empty.")
        if not confirm_capture:
            raise WorkerRuntimeError("Route capture requires explicit confirmation.")
        if expected_route_revision < 0:
            raise WorkerRuntimeError("expected_route_revision must be nonnegative.")
        if not self.command_center.paused:
            raise WorkerRuntimeError(
                "Pause automation before changing a Worker route. Nothing was changed."
            )
        if self.command_center.running:
            raise WorkerRuntimeError(
                "Another automation job is running. Nothing was changed."
            )

        run_lock = self.command_center._run_lock  # noqa: SLF001 - shared route/write gate
        if not run_lock.acquire(blocking=False):
            raise WorkerRuntimeError(
                "Another automation job is running. Nothing was changed."
            )
        try:
            current = self.runtime.worker(clean_worker_id, require_enabled=True)
            if current.route_revision != expected_route_revision:
                raise WorkerRuntimeError(
                    "The Worker route changed after this dashboard view loaded. "
                    "Refresh before trying again. Nothing was changed."
                )

            captured_target = self._capture_conversation(self.cdp_endpoint)
            captured = _conversation_url(captured_target.url)
            if captured is None:
                raise WorkerRuntimeError(
                    "The active browser page is not a ChatGPT conversation. Nothing was changed."
                )
            if current.chat_title.casefold() not in captured_target.title.casefold():
                raise WorkerRuntimeError(
                    "The sole open ChatGPT conversation does not match the selected Worker title "
                    f"{current.chat_title!r}. Observed browser title: "
                    f"{captured_target.title!r}. Nothing was changed."
                )
            if captured == current.conversation_url:
                return {
                    "changed": False,
                    "message": "The active ChatGPT conversation already matches this Worker route.",
                    "worker": self._route_payload(current),
                }

            next_revision = current.route_revision + 1 if current.route_revision else 1
            candidate = replace(
                current,
                conversation_url=captured,
                route_revision=next_revision,
            )
            hold_reason = (
                f"Direct URL route revision {next_revision} awaiting zero-authority browser canary."
            )
            now = time.time()

            try:
                with sqlite3.connect(self.database_path) as connection:
                    connection.row_factory = sqlite3.Row
                    connection.execute("PRAGMA foreign_keys = ON")
                    duplicate = connection.execute(
                        """
                        SELECT worker_id FROM worker_registry
                        WHERE conversation_url = ? AND worker_id <> ?
                        LIMIT 1
                        """,
                        (candidate.conversation_url, candidate.worker_id),
                    ).fetchone()
                    if duplicate is not None:
                        raise WorkerRuntimeError(
                            "That ChatGPT conversation is already registered to another Worker. "
                            "Nothing was changed."
                        )

                    updated = connection.execute(
                        """
                        UPDATE worker_registry
                        SET conversation_url = ?, route_revision = ?, updated_at = ?
                        WHERE worker_id = ? AND route_revision = ?
                        """,
                        (
                            candidate.conversation_url,
                            candidate.route_revision,
                            now,
                            candidate.worker_id,
                            expected_route_revision,
                        ),
                    )
                    if updated.rowcount != 1:
                        raise WorkerRuntimeError(
                            "The Worker route changed during capture. Nothing was changed."
                        )
                    connection.execute(
                        """
                        INSERT INTO worker_route_state(
                            worker_id, availability, last_seen_at, pause_reason, updated_at
                        ) VALUES (?, 'unknown', NULL, ?, ?)
                        ON CONFLICT(worker_id) DO UPDATE SET
                            availability = 'unknown',
                            last_seen_at = NULL,
                            pause_reason = excluded.pause_reason,
                            updated_at = excluded.updated_at
                        """,
                        (candidate.worker_id, hold_reason, now),
                    )
            except sqlite3.IntegrityError as exc:
                raise WorkerRuntimeError(
                    "The Worker route could not be saved without violating registry constraints."
                ) from exc

            saved = self.runtime.worker(candidate.worker_id, require_enabled=True)
            return {
                "changed": True,
                "message": (
                    f"Captured route revision {saved.route_revision}. "
                    "The route is held until the zero-authority courier canary succeeds."
                ),
                "worker": self._route_payload(saved),
            }
        finally:
            run_lock.release()

    def canary_witness(self, worker_id: str = ENGINEERING_CANARY_WORKER_ID) -> WorkerRouteWitness:
        """Return the exact route that a canary is expected to verify."""

        entry = self.runtime.worker(worker_id, require_enabled=True)
        if not entry.conversation_url or entry.route_revision < 1:
            raise WorkerRuntimeError("The Worker has no initialized direct route to verify.")
        route = self.runtime.store.route_state(worker_id)
        if route is not None and route.availability in {"unavailable", "ambiguous"}:
            raise WorkerRuntimeError(
                f"The Worker route is {route.availability}; canary dispatch is blocked."
            )
        return WorkerRouteWitness(
            worker_id=entry.worker_id,
            conversation_url=entry.conversation_url,
            route_revision=entry.route_revision,
        )

    def promote_after_canary(
        self,
        witness: WorkerRouteWitness,
        receipt: Mapping[str, object],
    ) -> dict[str, object]:
        """Promote only the unchanged route proven by a successful zero-authority canary."""

        if receipt.get("status") != "succeeded":
            raise WorkerRuntimeError("The courier canary did not report success.")
        if receipt.get("durable_authority_created") is not False:
            raise WorkerRuntimeError("The courier canary did not preserve zero authority.")
        if receipt.get("returned_to_source") is not True:
            raise WorkerRuntimeError("The courier canary did not verify return to HQ.")
        if not str(receipt.get("user_turn_id") or "").strip():
            raise WorkerRuntimeError("The courier canary has no correlated user-turn witness.")

        current = self.runtime.worker(witness.worker_id, require_enabled=True)
        if (
            current.conversation_url != witness.conversation_url
            or current.route_revision != witness.route_revision
        ):
            raise WorkerRuntimeError(
                "The Worker route changed during the canary. It remains on hold."
            )
        route = self.runtime.store.route_state(witness.worker_id)
        if route is not None and route.availability in {"unavailable", "ambiguous"}:
            raise WorkerRuntimeError(
                f"The Worker route became {route.availability} during the canary."
            )

        self.runtime.set_route_state(
            witness.worker_id,
            "available",
            last_seen_at=time.time(),
            pause_reason=None,
        )
        return {
            "message": (
                f"Route revision {witness.route_revision} is verified and available."
            ),
            "worker": self._route_payload(current),
        }


class RouteAwareWorkerOperationsService(WorkerOperationsService):
    """Worker Operations with safe route capture and automatic canary promotion."""

    def __init__(
        self,
        command_center: CommandCenterService,
        repository_root: Path,
        *,
        cdp_endpoint: str | None = None,
    ) -> None:
        super().__init__(
            command_center,
            repository_root,
            cdp_endpoint=cdp_endpoint,
        )
        self.routes = WorkerRouteManager(
            command_center,
            cdp_endpoint=self.cdp_endpoint,
        )

    def courier_self_test(
        self,
        *,
        confirm_send: bool,
        timeout_seconds: int = 300,
    ) -> dict[str, object]:
        witness = self.routes.canary_witness()
        result = super().courier_self_test(
            confirm_send=confirm_send,
            timeout_seconds=timeout_seconds,
        )
        receipt = result.get("receipt")
        if not isinstance(receipt, dict):
            raise WorkerRuntimeError("Courier self-test returned no receipt to verify.")
        result["route_promotion"] = self.routes.promote_after_canary(witness, receipt)
        result["operations"] = self.status()
        return result


__all__ = [
    "CapturedConversation",
    "ENGINEERING_CANARY_WORKER_ID",
    "RouteAwareWorkerOperationsService",
    "WorkerRouteManager",
    "WorkerRouteWitness",
    "capture_chatgpt_conversation",
]
