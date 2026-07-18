"""Cloud-visible Google Sheets mirror for Command Center schedules."""
from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Protocol
from urllib.parse import quote

import google.auth
import httpx
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account

SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"
DEFAULT_SHEET_NAME = "Run Ledger"
DEFAULT_API_BASE_URL = "https://sheets.googleapis.com/v4"
COLUMN_COUNT = 18
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
    """No-op publication boundary when Google Sheets is not configured."""

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


class GoogleSheetsScheduleLedger:
    """Best-effort Google Sheets mirror with one row per schedule definition."""

    def __init__(
        self,
        spreadsheet_id: str,
        *,
        sheet_name: str = DEFAULT_SHEET_NAME,
        credentials_file: Path | None = None,
        api_base_url: str = DEFAULT_API_BASE_URL,
        timeout_seconds: float = 20.0,
    ) -> None:
        self.spreadsheet_id = spreadsheet_id.strip()
        self.sheet_name = sheet_name.strip() or DEFAULT_SHEET_NAME
        self.credentials_file = credentials_file
        self.api_base_url = api_base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self._credentials: Credentials | None = None
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

    def _credentials_for_request(self) -> Credentials:
        with self._lock:
            if self._credentials is None:
                if self.credentials_file is not None:
                    self._credentials = service_account.Credentials.from_service_account_file(
                        str(self.credentials_file),
                        scopes=[SHEETS_SCOPE],
                    )
                else:
                    credentials, _ = google.auth.default(scopes=[SHEETS_SCOPE])
                    self._credentials = credentials
            if not self._credentials.valid:
                self._credentials.refresh(GoogleAuthRequest())
            if not self._credentials.token:
                raise RuntimeError("Google credentials did not produce an access token.")
            return self._credentials

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        body: dict[str, object] | None = None,
    ) -> dict[str, object]:
        credentials = self._credentials_for_request()
        response = httpx.request(
            method,
            f"{self.api_base_url}{path}",
            params=params,
            json=body,
            headers={"Authorization": f"Bearer {credentials.token}"},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        if not response.content:
            return {}
        data = response.json()
        return data if isinstance(data, dict) else {}

    def _quoted_sheet(self) -> str:
        return f"'{self.sheet_name.replace(chr(39), chr(39) * 2)}'"

    def _range_path(self, cell_range: str) -> str:
        return quote(f"{self._quoted_sheet()}!{cell_range}", safe="")

    def _find_schedule_row(self, schedule_id: int) -> int | None:
        data = self._request(
            "GET",
            f"/spreadsheets/{self.spreadsheet_id}/values/{self._range_path('A:A')}",
            params={"majorDimension": "ROWS"},
        )
        rows = data.get("values")
        if not isinstance(rows, list):
            return None
        for row_number, row in enumerate(rows[1:], start=2):
            if isinstance(row, list) and row and str(row[0]) == str(schedule_id):
                return row_number
        return None

    @staticmethod
    def _weekdays(schedule: dict[str, object]) -> str:
        values = schedule.get("weekdays")
        if not isinstance(values, list):
            return ""
        labels = [WEEKDAY_LABELS[int(day)] for day in values if 0 <= int(day) <= 6]
        return ", ".join(labels)

    @staticmethod
    def _health_formula(row_number: int) -> str:
        return (
            f'=IF(J{row_number}<>"Active",J{row_number},'
            f'IF(M{row_number}="","No future run",'
            f'IF(M{row_number}+TIME(0,5,0)<NOW(),"OVERDUE","On schedule")))'
        )

    def _row_values(
        self,
        schedule: dict[str, object],
        row_number: int,
    ) -> list[object]:
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
            self._health_formula(row_number),
        ]

    def _upsert_schedule(self, schedule: dict[str, object]) -> None:
        schedule_id = int(schedule["id"])
        row_number = self._find_schedule_row(schedule_id)
        if row_number is None:
            row_number = 2
            data = self._request(
                "GET",
                f"/spreadsheets/{self.spreadsheet_id}/values/{self._range_path('A:A')}",
                params={"majorDimension": "ROWS"},
            )
            rows = data.get("values")
            if isinstance(rows, list):
                row_number = max(2, len(rows) + 1)
            self._request(
                "POST",
                (
                    f"/spreadsheets/{self.spreadsheet_id}/values/"
                    f"{self._range_path('A:R')}:append"
                ),
                params={
                    "valueInputOption": "USER_ENTERED",
                    "insertDataOption": "INSERT_ROWS",
                },
                body={
                    "majorDimension": "ROWS",
                    "values": [self._row_values(schedule, row_number)],
                },
            )
            return
        self._request(
            "PUT",
            (
                f"/spreadsheets/{self.spreadsheet_id}/values/"
                f"{self._range_path(f'A{row_number}:R{row_number}')}"
            ),
            params={"valueInputOption": "USER_ENTERED"},
            body={
                "majorDimension": "ROWS",
                "values": [self._row_values(schedule, row_number)],
            },
        )

    def _clear_schedule(self, schedule_id: int) -> None:
        row_number = self._find_schedule_row(schedule_id)
        if row_number is None:
            return
        self._request(
            "POST",
            (
                f"/spreadsheets/{self.spreadsheet_id}/values/"
                f"{self._range_path(f'A{row_number}:R{row_number}')}:clear"
            ),
            body={},
        )

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
        return self._safe_write(lambda: self._upsert_schedule(schedule))

    def remove_schedule(self, schedule_id: int) -> bool:
        return self._safe_write(lambda: self._clear_schedule(schedule_id))


def schedule_ledger_from_environment() -> ScheduleLedger:
    """Build the ledger publication boundary without failing dashboard startup."""
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_LEDGER_SPREADSHEET_ID", "").strip()
    if not spreadsheet_id:
        return DisabledScheduleLedger()
    credentials_value = os.getenv("GOOGLE_SHEETS_LEDGER_CREDENTIALS_FILE", "").strip()
    credentials_file = Path(credentials_value).expanduser() if credentials_value else None
    return GoogleSheetsScheduleLedger(
        spreadsheet_id,
        sheet_name=os.getenv("GOOGLE_SHEETS_LEDGER_SHEET_NAME", DEFAULT_SHEET_NAME),
        credentials_file=credentials_file,
        api_base_url=os.getenv(
            "GOOGLE_SHEETS_LEDGER_API_BASE_URL",
            DEFAULT_API_BASE_URL,
        ),
    )
