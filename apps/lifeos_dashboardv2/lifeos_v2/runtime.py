"""Restart-safe JSON transport state and reconciliation service."""
from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .contracts import Advisory, CommandState, DeliveryCommand, Route

LOG = logging.getLogger(__name__)
_SECRET = re.compile(r"(?i)(authorization|token|password)\s*[:=]\s*[^\s,]+")


def redact(value: str) -> str:
    return _SECRET.sub(lambda m: m.group(1) + "=[REDACTED]", value)


def now() -> str:
    return datetime.now(UTC).isoformat()


class RuntimeStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, Any] = {"paused": False, "routes": {}, "commands": {}, "events": [], "extension": {"connected": False, "last_heartbeat_at": None}}
        if path.exists():
            self.data.update(json.loads(path.read_text(encoding="utf-8")))
        self.data.setdefault("tab_readiness", {})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.data, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(self.path)

    def event(self, message: str) -> None:
        safe = redact(message)
        self.data["events"] = (self.data.get("events", []) + [{"at": now(), "message": safe}])[-100:]
        LOG.info("%s", safe)


class CourierService:
    def __init__(self, store: RuntimeStore) -> None:
        self.store = store

    @property
    def paused(self) -> bool:
        return bool(self.store.data["paused"])

    def routes(self) -> list[dict[str, Any]]:
        return list(self.store.data["routes"].values())

    def register_route(self, route: Route) -> dict[str, Any]:
        self.store.data["routes"][route.route_name] = route.to_dict()
        self.store.event(f"route registered {route.route_name}")
        self.store.save()
        return route.to_dict()

    def delete_route(self, name: str) -> bool:
        result = self.store.data["routes"].pop(name, None) is not None
        if result:
            self.store.event(f"route deleted {name}")
            self.store.save()
        return result

    def commands(self) -> list[dict[str, Any]]:
        return list(self.store.data["commands"].values())

    def readiness(self) -> dict[str, Any]:
        return self.store.data["tab_readiness"]

    def set_source_sync(self, status: dict[str, Any]) -> None:
        """Persist non-secret source evidence and block dispatch while unverifiable."""
        self.store.data["source_sync"] = dict(status)
        self.store.save()

    @property
    def source_dispatch_allowed(self) -> bool:
        return self.store.data.get("source_sync", {}).get("sync_state", "CURRENT") == "CURRENT"

    def report_readiness(self, route_name: str, url: str, content_script: bool, composer_ready: bool, composer_empty: bool, send_control: bool, test_armed: bool) -> dict[str, Any]:
        route = self.store.data["routes"].get(route_name)
        exact_url = bool(route and route["chatgpt_url"] == url)
        ready = exact_url and content_script and composer_ready and composer_empty and send_control
        record = {"route_name": route_name, "url": url, "exact_url": exact_url, "content_script": content_script, "composer_ready": composer_ready, "composer_empty": composer_empty, "send_control": send_control, "test_armed": test_armed, "state": "READY" if ready else "NOT_READY", "verified_at": now()}
        self.store.data["tab_readiness"][route_name] = record
        self.store.event(f"tab readiness {route_name} {record['state']}")
        self.store.save()
        return record

    def _route_dispatch_allowed(self, route_name: str) -> bool:
        if not self._route_available(route_name):
            return False
        readiness = self.store.data["tab_readiness"].get(route_name, {})
        return readiness.get("state") == "READY" and (not route_name.startswith("slice_three_test") or readiness.get("test_armed") is True)

    def _route_available(self, route_name: str) -> bool:
        route = self.store.data["routes"].get(route_name)
        return bool(route and str(route.get("health", "AVAILABLE")).upper() == "AVAILABLE")

    def discover_candidate(self, route_name: str) -> dict[str, Any] | None:
        """Return a pending route candidate without granting dispatch authority."""
        if self.paused or not self.source_dispatch_allowed or not self._route_available(route_name):
            return None
        return next((c for c in self.commands() if c["route_name"] == route_name and c["state"] == CommandState.PENDING and c.get("attempts", 0) < 3), None)

    def begin_attempt(self, command_id: str) -> dict[str, Any] | None:
        command = self.store.data["commands"].get(command_id)
        if not command or self.paused or not self.source_dispatch_allowed or not self._route_dispatch_allowed(command["route_name"]) or command["state"] != CommandState.PENDING or command.get("attempts", 0) >= 3:
            return None
        command.update({"state": CommandState.DISPATCHING, "attempts": command.get("attempts", 0) + 1, "last_attempt_at": now(), "updated_at": now()})
        self.store.event(f"dispatch attempt {command_id}")
        self.store.save()
        return command

    def reconcile(self, advisories: list[Advisory]) -> list[dict[str, Any]]:
        current = {a.advisory_id: a for a in advisories}
        commands = self.store.data["commands"]
        for command in commands.values():
            source = current.get(command["advisory_id"])
            if source:
                command.update({
                    "source_repository": source.source_repository,
                    "source_branch": source.source_branch,
                    "source_commit_sha": source.source_commit_sha,
                    "source_path": source.source_path,
                    "source_revision": source.revision,
                    "source_verified_at": source.source_verified_at,
                })
            if command["state"] in {CommandState.PENDING, CommandState.BLOCKED_ROUTE} and (
                not source or not source.actionable or source.revision != command["revision"]
            ):
                command["state"], command["updated_at"] = CommandState.STALE, now()
                self.store.event(f"stale command suppressed {command['command_id']}")
        if not self.paused:
            for advisory in advisories:
                if advisory.actionable:
                    self._ensure_command(advisory)
        else:
            self.store.event("poll suppressed by global pause")
        self.store.save()
        return self.commands()

    def _ensure_command(self, advisory: Advisory) -> None:
        commands = self.store.data["commands"]
        command = commands.get(advisory.command_id)
        route = self.store.data["routes"].get(advisory.target_department)
        stamp = now()
        if command:
            if command["state"] == CommandState.BLOCKED_ROUTE and route:
                command.update({"state": CommandState.PENDING, "blocker": "", "updated_at": stamp, "route_name": route["route_name"]})
                self.store.event(f"route resolved for {advisory.command_id}")
            return
        if route:
            state, blocker, route_name = CommandState.PENDING, "", route["route_name"]
        else:
            state, blocker, route_name = CommandState.BLOCKED_ROUTE, f"No registered route for target '{advisory.target_department}'", advisory.target_department
        command = DeliveryCommand(advisory.command_id, advisory.advisory_id, advisory.revision, route_name,
            advisory.target_department, f"Read and act only on advisory {advisory.advisory_id} revision {advisory.revision} at {advisory.source_url}.", state, stamp, stamp, blocker,
            source_repository=advisory.source_repository, source_branch=advisory.source_branch,
            source_commit_sha=advisory.source_commit_sha, source_path=advisory.source_path,
            source_revision=advisory.revision, source_verified_at=advisory.source_verified_at)
        commands[command.command_id] = command.to_dict()
        self.store.event(f"command created {command.command_id} state={state}")

    def update_telemetry(self, command_id: str, state: CommandState, note: str = "") -> dict[str, Any] | None:
        command = self.store.data["commands"].get(command_id)
        if not command:
            return None
        if state == CommandState.FAILED and command.get("attempts", 0) < 3:
            state = CommandState.PENDING
        command.update({"state": state, "telemetry_note": redact(note), "updated_at": now()})
        self.store.event(f"telemetry {command_id} {state}")
        self.store.save()
        return command

    def heartbeat(self, version: str = "") -> dict[str, Any]:
        self.store.data["extension"] = {"connected": True, "last_heartbeat_at": now(), "version": version}
        self.store.save()
        return self.store.data["extension"]

    def pause(self) -> None:
        self.store.data["paused"] = True
        self.store.event("global pause enabled")
        self.store.save()

    def resume(self) -> None:
        self.store.data["paused"] = False
        self.store.event("global pause disabled; reconcile current source truth required")
        self.store.save()
