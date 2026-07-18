"""Cloud-visible Google Sheets mirror for Command Center schedules."""
from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timezone
from typing import Callable, Protocol

import httpx

DEFAULT_SHEET_NAME = "Run Ledger"
COLUMN_COUNT = 17
GOOGLE_EPOCH_OFFSET_DAYS = 25569.0
WEEKDAY_LABELS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DEBUG_COMPLETION_MARKER = "Debug recurrence test completed after two attempts."


def google_datetime(timestamp: float | int | None) -> float | str:
    """Convert a Unix timestamp to the numeric date format used by Google Sheets."""
    if timestamp is None:
        return ""
    return float(timestamp) / 86400.0 + GOOGLE_EPOCH_OFFSET_DAYS


def utc_iso(timestamp: float | int | None) -> str:
    """Return an unambiguous UTC timestamp for logs and tests."""
    if timestamp is None:
        return ""
    return (
        datetime.fromtimestamp(float(timestamp), timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def schedule_state(schedule: dict[str, object]) -> str:
    """Return a stable visible lifecycle label for one schedule definition."""
    if bool(schedule.get("enabled")):
        return "Active"
    cadence = str(schedule.get("cadence") or "")
    last_status = str(schedule.get("last_status") or "")
    last_reason = str(schedule.get("last_reason") or "")
    if DEBUG_COMPLETION_MARKER in last_reason:
        return "Completed"
    if cadence == "once" and last_status == "succeeded":
        return "Completed"
    if cadence == "once" and last_status in {"failed", "refused"}:
        return "Failed"
    return "Paused"


class ScheduleLedger(Protocol):
    """Small publication boundary used by the Command Center."""

    def record_schedule(self, schedule: dict[str, object]) -> bool: ...

    def remove_schedule(self, schedule_id: int) -> bool: ...

    def status(self) -> dict[str, object]: ...


class DisabledScheduleLedger:
    """No-op publication boundary when the Sheet mirror is not configured."""

    def record_schedule(self, schedule: dict[str, object]) -> bool:
        return False

    def remove_schedule(self, schedule_id: int) -> bool:
        return False

    def status(self) -> dict[str, object]:
        return {
            "configured": False,
            "state": "disabled",
            "spreadsheet_id": "",
            "spreadsheet_url": "",
            "sheet_name": DEFAULT_SHEET_NAME,
            "last_attempt_at": None,
            "last_success_at": None,
            "last_error": "",
        }


class ConfigurationErrorScheduleLedger(DisabledScheduleLedger):
    """Visible error state for incomplete Apps Script configuration."""

    def __init__(self, spreadsheet_id: str, sheet_name: str, error: str) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.error = error

    def status(self) -> dict[str, object]:
        return {
            "configured": True,
            "state": "error",
            "spreadsheet_id": self.spreadsheet_id,
            "spreadsheet_url": (
                f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
                if self.spreadsheet_id
                else ""
            ),
            "sheet_name": self.sheet_name,
            "last_attempt_at": None,
            "last_success_at": None,
            "last_error": self.error,
        }


class AppsScriptScheduleLedger:
    """Best-effort Sheet mirror through a secret-protected Apps Script web app."""

    def __init__(
        self,
        spreadsheet_id: str,
        web_app_url: str,
        shared_secret: str,
        *,
        sheet_name: str = DEFAULT_SHEET_NAME,
        timeout_seconds: float = 20.0,
    ) -> None:
        self.spreadsheet_id = spreadsheet_id.strip()
        self.web_app_url = web_app_url.strip()
        self.shared_secret = shared_secret
        self.sheet_name = sheet_name.strip() or DEFAULT_SHEET_NAME
        self.timeout_seconds = timeout_seconds
        self._lock = threading.RLock()
        self._last_attempt_at: float | None = None
        self._last_success_at: float | None = None
        self._last_error = ""

    @property
    def spreadsheet_url(self) -> str:
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"

    def status(self) -> dict[str, object]:
        with self._lock:
            if self._last_error:
                state = "error"
            elif self._last_success_at is not None:
                state = "synced"
            else:
                state = "ready"
            return {
                "configured": True,
                "state": state,
                "spreadsheet_id": self.spreadsheet_id,
                "spreadsheet_url": self.spreadsheet_url,
                "sheet_name": self.sheet_name,
                "last_attempt_at": self._last_attempt_at,
                "last_success_at": self._last_success_at,
                "last_error": self._last_error,
            }

    def _post(self, payload: dict[str, object]) -> dict[str, object]:
        response = httpx.post(
            self.web_app_url,
            json={
                **payload,
                "secret": self.shared_secret,
                "spreadsheet_id": self.spreadsheet_id,
                "sheet_name": self.sheet_name,
            },
            timeout=self.timeout_seconds,
            follow_redirects=True,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise RuntimeError("Apps Script returned an invalid response.")
        if not bool(data.get("ok")):
            raise RuntimeError(str(data.get("error") or "Apps Script rejected the request."))
        returned_id = str(data.get("spreadsheet_id") or "")
        returned_sheet = str(data.get("sheet_name") or "")
        if returned_id != self.spreadsheet_id or returned_sheet != self.sheet_name:
            raise RuntimeError("Apps Script responded from an unexpected spreadsheet or tab.")
        return data

    @staticmethod
    def _weekdays(schedule: dict[str, object]) -> str:
        values = schedule.get("weekdays")
        if not isinstance(values, list):
            return ""
        labels = [WEEKDAY_LABELS[int(day)] for day in values if 0 <= int(day) <= 6]
        return ", ".join(labels)

    def _row_values(self, schedule: dict[str, object]) -> list[object]:
        """Return columns A:Q. Apps Script owns the row-specific Health formula in R."""
        return [
            int(schedule["id"]),
            str(schedule.get("name") or ""),
            str(schedule.get("destination") or ""),
            str(schedule.get("cadence") or ""),
            str(schedule.get("schedule_date") or ""),
            str(schedule.get("schedule_time") or ""),
            self._weekdays(schedule),
            str(schedule.get("timezone") or "America/Chicago"),
            bool(schedule.get("enabled")),
            schedule_state(schedule),
            str(schedule.get("mode") or ""),
            str(schedule.get("prompt_type") or ""),
            google_datetime(schedule.get("next_run_at")),
            google_datetime(schedule.get("last_run_at")),
            str(schedule.get("last_status") or ""),
            str(schedule.get("last_reason") or ""),
            google_datetime(time.time()),
        ]

    def _safe_write(self, callback: Callable[[], None]) -> bool:
        with self._lock:
            self._last_attempt_at = time.time()
        try:
            callback()
        except Exception as exc:  # noqa: BLE001 - mirror failures must not stop schedules
            with self._lock:
                self._last_error = str(exc)
            return False
        with self._lock:
            self._last_success_at = time.time()
            self._last_error = ""
        return True

    def record_schedule(self, schedule: dict[str, object]) -> bool:
        return self._safe_write(
            lambda: self._post(
                {
                    "action": "upsert",
                    "schedule_id": int(schedule["id"]),
                    "values": self._row_values(schedule),
                }
            )
        )

    def remove_schedule(self, schedule_id: int) -> bool:
        return self._safe_write(
            lambda: self._post(
                {
                    "action": "remove",
                    "schedule_id": int(schedule_id),
                }
            )
        )


# Retain the old import name for local callers while the transport changes underneath it.
GoogleSheetsScheduleLedger = AppsScriptScheduleLedger


def schedule_ledger_from_environment() -> ScheduleLedger:
    """Build the ledger publication boundary without failing dashboard startup."""
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_LEDGER_SPREADSHEET_ID", "").strip()
    web_app_url = os.getenv("GOOGLE_SHEETS_LEDGER_WEB_APP_URL", "").strip()
    shared_secret = os.getenv("GOOGLE_SHEETS_LEDGER_SHARED_SECRET", "")
    sheet_name = os.getenv("GOOGLE_SHEETS_LEDGER_SHEET_NAME", DEFAULT_SHEET_NAME).strip()
    configured_values = (spreadsheet_id, web_app_url, shared_secret)
    if not any(configured_values):
        return DisabledScheduleLedger()
    missing = [
        name
        for name, value in (
            ("GOOGLE_SHEETS_LEDGER_SPREADSHEET_ID", spreadsheet_id),
            ("GOOGLE_SHEETS_LEDGER_WEB_APP_URL", web_app_url),
            ("GOOGLE_SHEETS_LEDGER_SHARED_SECRET", shared_secret),
        )
        if not value
    ]
    if missing:
        return ConfigurationErrorScheduleLedger(
            spreadsheet_id,
            sheet_name or DEFAULT_SHEET_NAME,
            f"Missing ledger setting(s): {', '.join(missing)}",
        )
    return AppsScriptScheduleLedger(
        spreadsheet_id,
        web_app_url,
        shared_secret,
        sheet_name=sheet_name,
    )
