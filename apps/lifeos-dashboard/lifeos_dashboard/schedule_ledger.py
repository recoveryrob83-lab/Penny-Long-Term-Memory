"""Cloud-visible Google Sheets mirror for scheduled occurrences."""
from __future__ import annotations

import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from urllib.parse import quote

import google.auth
import httpx
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account

SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"
DEFAULT_SHEET_NAME = "Run Ledger"
DEFAULT_API_BASE_URL = "https://sheets.googleapis.com/v4"
COLUMN_COUNT = 16


def utc_iso(timestamp: float | int | None) -> str:
    """Return an unambiguous UTC timestamp for the cloud ledger."""
    if timestamp is None:
        return ""
    return (
        datetime.fromtimestamp(float(timestamp), timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def occurrence_key(schedule_id: int | str, due_at: float | int) -> str:
    """Return the stable identity for one expected scheduled occurrence."""
    return f"v1:{int(schedule_id)}:{int(float(due_at))}"


class ScheduleLedger(Protocol):
    """Small publication boundary used by the Command Center."""

    def record_planned(self, schedule: dict[str, object]) -> bool: ...

    def record_state(
        self,
        schedule: dict[str, object],
        state: str,
        reason: str,
    ) -> bool: ...

    def record_result(
        self,
        schedule: dict[str, object],
        due_at: float,
        result: dict[str, object],
    ) -> bool: ...

    def status(self) -> dict[str, object]: ...


class DisabledScheduleLedger:
    """No-op publication boundary when Google Sheets is not configured."""

    def record_planned(self, schedule: dict[str, object]) -> bool:
        return False

    def record_state(
        self,
        schedule: dict[str, object],
        state: str,
        reason: str,
    ) -> bool:
        return False

    def record_result(
        self,
        schedule: dict[str, object],
        due_at: float,
        result: dict[str, object],
    ) -> bool:
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
    """Best-effort Google Sheets mirror for schedule plans and results."""

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
                    self._credentials = (
                        service_account.Credentials.from_service_account_file(
                            str(self.credentials_file),
                            scopes=[SHEETS_SCOPE],
                        )
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
        a1_range = f"{self._quoted_sheet()}!{cell_range}"
        return quote(a1_range, safe="")

    @staticmethod
    def _padded_row(values: list[object] | None) -> list[str]:
        clean = [str(value) for value in (values or [])]
        return (clean + [""] * COLUMN_COUNT)[:COLUMN_COUNT]

    def _find_occurrence(self, key: str) -> tuple[int | None, list[str]]:
        data = self._request(
            "GET",
            (
                f"/spreadsheets/{self.spreadsheet_id}/values/"
                f"{self._range_path('A:P')}"
            ),
            params={"majorDimension": "ROWS"},
        )
        rows = data.get("values")
        if not isinstance(rows, list):
            return None, [""] * COLUMN_COUNT
        for row_number, row in enumerate(rows[1:], start=2):
            if isinstance(row, list) and row and str(row[0]) == key:
                return row_number, self._padded_row(row)
        return None, [""] * COLUMN_COUNT

    def _row_values(
        self,
        schedule: dict[str, object],
        *,
        due_at: float,
        state: str,
        started_at: float | None = None,
        finished_at: float | None = None,
        reason: str = "",
        existing: list[str] | None = None,
    ) -> list[str]:
        previous = self._padded_row(existing)
        return [
            occurrence_key(schedule["id"], due_at),
            str(schedule["id"]),
            str(schedule.get("name") or ""),
            str(schedule.get("destination") or ""),
            str(schedule.get("cadence") or ""),
            utc_iso(due_at),
            str(schedule.get("timezone") or "America/Chicago"),
            state,
            str(schedule.get("mode") or ""),
            str(schedule.get("prompt_type") or ""),
            utc_iso(started_at),
            utc_iso(finished_at),
            reason,
            utc_iso(time.time()),
            previous[14],
            previous[15],
        ]

    def _upsert_occurrence(
        self,
        schedule: dict[str, object],
        *,
        due_at: float,
        state: str,
        started_at: float | None = None,
        finished_at: float | None = None,
        reason: str = "",
    ) -> None:
        key = occurrence_key(schedule["id"], due_at)
        row_number, existing = self._find_occurrence(key)
        values = self._row_values(
            schedule,
            due_at=due_at,
            state=state,
            started_at=started_at,
            finished_at=finished_at,
            reason=reason,
            existing=existing,
        )
        if row_number is None:
            self._request(
                "POST",
                (
                    f"/spreadsheets/{self.spreadsheet_id}/values/"
                    f"{self._range_path('A:P')}:append"
                ),
                params={
                    "valueInputOption": "RAW",
                    "insertDataOption": "INSERT_ROWS",
                },
                body={"majorDimension": "ROWS", "values": [values]},
            )
            return
        self._request(
            "PUT",
            (
                f"/spreadsheets/{self.spreadsheet_id}/values/"
                f"{self._range_path(f'A{row_number}:P{row_number}')}"
            ),
            params={"valueInputOption": "RAW"},
            body={"majorDimension": "ROWS", "values": [values]},
        )

    def _safe_write(self, callback: object) -> bool:
        with self._lock:
            self._last_attempt_at = time.time()
        try:
            callback()  # type: ignore[operator]
        except Exception as exc:  # noqa: BLE001 - mirror failures must not stop schedules
            with self._lock:
                self._last_error = str(exc)
            return False
        with self._lock:
            self._last_success_at = time.time()
            self._last_error = ""
        return True

    def record_planned(self, schedule: dict[str, object]) -> bool:
        due_at = schedule.get("next_run_at")
        if due_at is None or not bool(schedule.get("enabled")):
            return False
        return self._safe_write(
            lambda: self._upsert_occurrence(
                schedule,
                due_at=float(due_at),
                state="planned",
            )
        )

    def record_state(
        self,
        schedule: dict[str, object],
        state: str,
        reason: str,
    ) -> bool:
        due_at = schedule.get("next_run_at")
        if due_at is None:
            return False
        return self._safe_write(
            lambda: self._upsert_occurrence(
                schedule,
                due_at=float(due_at),
                state=state,
                reason=reason,
            )
        )

    def record_result(
        self,
        schedule: dict[str, object],
        due_at: float,
        result: dict[str, object],
    ) -> bool:
        return self._safe_write(
            lambda: self._upsert_occurrence(
                schedule,
                due_at=due_at,
                state=str(result.get("status") or "unknown"),
                started_at=float(result["started_at"]),
                finished_at=float(result["finished_at"]),
                reason=str(result.get("reason") or ""),
            )
        )


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
